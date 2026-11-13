#!/usr/bin/env python3
"""Measure whether each sdlc skill and agent fires on the requests meant for it, and stays quiet otherwise.

Each case is a first message to a fresh `claude -p` session in a small fixture repository, with this working
copy's plugin loaded and the user's own settings and plugins left out. The run stops at the first sdlc skill
or agent it reaches, so no agent's work runs:

  * a skill case passes when the first sdlc skill or agent is that skill;
  * an agent case passes when the first agent launched is that agent, whatever skill loaded before it;
  * a negative case passes when no sdlc skill or agent fires. Built-in agents such as Explore are allowed.

Target: 9 hits in 10 per skill and agent. Runs go under ~/.sdlc-trigger-runs, outside this repository and
outside the system temp directory, where skills do not load. Each run is a short headless session and costs
API money. Usage:

    python3 tools/trigger-gauge.py                       # every case once, on Sonnet
    python3 tools/trigger-gauge.py --only build --runs 3
    python3 tools/trigger-gauge.py --self-test
"""
import argparse, concurrent.futures as cf, json, os, shutil, subprocess, sys, time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN, RUNS = os.path.join(REPO, "plugins", "sdlc"), os.path.expanduser("~/.sdlc-trigger-runs")
SKILLS = {"story", "spike", "bug", "refactor", "build"}
AGENTS = {"plan-reviewer", "test-challenger", "implementer", "reviewer", "verifier", "delegator"}

FIXTURE = {
    "AGENTS.md": "Check: `python3 -m unittest discover -q -s tests -t .`\n",
    "pricing.py": 'def total(lines):\n    """Order total in dollars. Each line is (unit_price, quantity)."""\n'
                  "    return sum(price * quantity for price, quantity in lines)\n",
    "export.py": "import csv\n\n\ndef export_orders(orders, path):\n    with open(path, 'w') as f:\n"
                 "        for o in orders:\n            f.write(','.join(str(v) for v in o) + '\\n')\n",
    "logs-a.log": "started\n",
    "worker.log": "done\n",
    "tests/__init__.py": "",
    "tests/test_pricing.py": "import unittest\n\nfrom pricing import total\n\n\nclass TotalTest(unittest.TestCase):\n"
                             "    def test_sums_lines(self):\n        self.assertEqual(total([(2.50, 2), (1.25, 4)]), 10.00)\n",
    "docs/stories/export.md": "# Customer exports order history\n\nAs a customer, I want to export my orders so that I can "
                              "do my taxes.\n\n## Acceptance criteria\n\n1. The export is fast and works correctly.\n",
    "SPEC.md": "## Implementation design spec: PAY-12\n\nApproach: add a discount table in Postgres and a nightly cron that "
               "recomputes every order total.\nChanges: pricing.py, a new discounts.py service\nTests: unit tests\n",
    "docs/design.md": "# Order events\n\nWe will add Kafka between checkout and billing so billing reads order events.\n",
    "findings.md": "1|6|issue|pricing.py:3|quantity 0|total ignores negative quantities|reject them|read pricing.py:3\n"
                   "2|8|suggestion|export.py:5|any order|csv module imported but unused|use csv.writer|read export.py:1\n",
}
RED = {"tests/test_bulk.py": "import unittest\n\nfrom pricing import total\n\n\nclass BulkTest(unittest.TestCase):\n"
                             "    def test_ten_or_more_get_five_percent_off(self):\n"
                             "        self.assertEqual(total([(10.00, 10)]), 95.00)\n"}
DIRTY = {"pricing.py": FIXTURE["pricing.py"].replace("    return", "    if not lines:\n        return 0\n    return")}

# (prompt, expected): a skill name, "agent:<name>", or None.
CASES = [
    ("Write a story for letting customers download their order history.", "story"),
    ("Critique my acceptance criteria in docs/stories/export.md.", "story"),
    ("Do a story for gift cards at checkout.", "story"),
    ("Review this story before we build it: docs/stories/export.md", "story"),
    ("Add a CSV export to the orders page.", "build"),
    ("Implement the story in docs/stories/export.md.", "build"),
    ("Just build a bulk discount: orders of 10 or more items get 5% off.", "build"),
    ("Bump the requests dependency to the latest version.", "build"),
    ("Add a --dry-run flag to the export.", "build"),
    ("total() returns a negative number when a quantity is negative. It should reject it.", "bug"),
    ("File a bug: the export crashes on an empty order list.", "bug"),
    ("Exports over 10k orders time out in production.", "bug"),
    ("Why does total give 9.999999 instead of 10 for some carts?", "bug"),
    ("Clean up export.py, it's hard to follow.", "refactor"),
    ("Rename total to order_total everywhere.", "refactor"),
    ("Extract the line-total calculation in pricing.py into its own function.", "refactor"),
    ("Where should I clean up in this repo?", "refactor"),
    ("Would SQLite full-text search be fast enough for a million orders?", "spike"),
    ("Do a spike on using Polars for the export.", "spike"),
    ("How hard would it be to make the export async?", "spike"),
    ("Try the decimal module for money and see if it fixes the rounding.", "spike"),
    ("Review my changes.", "agent:reviewer"),
    ("Give me a second-opinion review of my uncommitted changes before I commit.", "agent:reviewer"),
    ("Find the bugs in my working-tree diff.", "agent:reviewer"),
    ("Verify the review findings in findings.md: which are real?", "agent:verifier"),
    ("Fact-check these review comments in findings.md against the code.", "agent:verifier"),
    ("Review my design in SPEC.md.", "agent:plan-reviewer"),
    ("Poke holes in this plan: SPEC.md", "agent:plan-reviewer"),
    ("Is the architecture in docs/design.md sound?", "agent:plan-reviewer"),
    ("Challenge the failing tests in tests/test_bulk.py blind before any code is written.", "agent:test-challenger"),
    ("I wrote failing tests in tests/test_bulk.py but no code yet. Are they strong enough to catch a wrong implementation?", "agent:test-challenger"),
    ("Make the failing tests in tests/test_bulk.py pass.", "agent:implementer"),
    ("Go green on the red commit.", "agent:implementer"),
    ("While we keep working, run the test suite in the background and tell me only whether it passed.", "agent:delegator"),
    ("In the background, summarize worker.log and logs-a.log in one line each.", "agent:delegator"),
    ("In parallel, move every .log file in this repo into a logs/ folder and tell me what moved.", "agent:delegator"),
    # Held out: phrased unlike any description, to catch wording tuned to the cases above.
    ("Customers keep asking for a way to save their carts for later. Can we spec that out properly first?", "story"),
    ("Can you wire up a new endpoint that returns order totals as JSON?", "build"),
    ("Upgrade us to Python 3.13.", "build"),
    ("Something is off: the second export of the day always has duplicate rows.", "bug"),
    ("pricing.py is a mess of nested ifs, tidy it up without changing what it does.", "refactor"),
    ("Is it realistic to move the export to a background worker? I want to know before we commit to it.", "spike"),
    ("Look over what I just changed and tell me what's broken.", "agent:reviewer"),
    ("Here is my plan for the discount feature in SPEC.md. What am I missing?", "agent:plan-reviewer"),
    ("Kick off a background job that deletes the .log files and let me know when it's done.", "agent:delegator"),
    ("What does pricing.py do?", None),
    ("Find every caller of total.", None),
    ("Explain what a property-based test is.", None),
    ("How do I run the tests here?", None),
    ("What's the time complexity of Python's sorted()?", None),
    ("Commit this.", None),
]


def git(work, *args):
    subprocess.run(["git", "-c", "user.email=gauge@local", "-c", "user.name=gauge", *args], cwd=work, check=True,
                   capture_output=True)


def setup(work):
    shutil.rmtree(work, ignore_errors=True)
    for files in (FIXTURE, RED, DIRTY):
        for path, text in files.items():
            os.makedirs(os.path.dirname(os.path.join(work, path)) or work, exist_ok=True)
            open(os.path.join(work, path), "w").write(text)
        if files is FIXTURE:
            git(work, "init", "-q"); git(work, "add", "-A"); git(work, "commit", "-qm", "start")
        elif files is RED:
            git(work, "add", "-A"); git(work, "commit", "-qm", "test(red): bulk discount")


def fires(event):
    """The sdlc skills and every agent one stream-json event launches from the main session, in order."""
    if event.get("type") != "assistant" or event.get("parent_tool_use_id"):
        return []
    out = []
    for b in event.get("message", {}).get("content", []):
        if b.get("type") != "tool_use":
            continue
        name, inp = b.get("name"), b.get("input") or {}
        if name == "Skill":
            out.append("skill:" + str(inp.get("skill", "")).split(":")[-1])
        elif name in ("Agent", "Task"):
            out.append("agent:" + str(inp.get("subagent_type", "general-purpose")).split(":")[-1])
    return out


def done(fired, expected):
    hit = [f for f in fired if f.split(":", 1)[1] in SKILLS | AGENTS or f.startswith("agent:")]
    if expected and expected.startswith("agent:"):
        return any(f.startswith("agent:") for f in fired)
    return any(f.split(":", 1)[1] in SKILLS | AGENTS for f in hit)


def passed(fired, expected):
    ours = [f for f in fired if f.split(":", 1)[1] in SKILLS | AGENTS]
    if expected is None:
        return not ours
    if expected.startswith("agent:"):
        agents = [f for f in fired if f.startswith("agent:")]
        return bool(agents) and agents[0] == expected
    return bool(ours) and ours[0] == "skill:" + expected


def run_one(i, n, prompt, expected, model, timeout):
    work = os.path.join(RUNS, f"case-{i:02d}-{n}")
    setup(work)
    cmd = ["claude", "-p", prompt, "--plugin-dir", PLUGIN, "--setting-sources", "project", "--output-format",
           "stream-json", "--verbose", "--max-turns", "8", "--allowedTools", "Skill,Agent,Task,Read,Grep,Glob"]
    if model:
        cmd += ["--model", model]
    p = subprocess.Popen(cmd, cwd=work, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    fired, start = [], time.time()
    log = open(os.path.join(work, ".gauge-stream.jsonl"), "w")
    try:
        for line in p.stdout:
            log.write(line)
            try:
                fired += fires(json.loads(line))
            except ValueError:
                continue
            if done(fired, expected) or time.time() - start > timeout:
                break
    finally:
        p.kill()
        p.wait()
        log.close()
    return {"case": i, "run": n, "prompt": prompt, "expected": expected, "fired": fired, "pass": passed(fired, expected)}


def self_test():
    ev = lambda *blocks, parent=None: {"type": "assistant", "parent_tool_use_id": parent, "message": {"content": list(blocks)}}
    skill = lambda s: {"type": "tool_use", "name": "Skill", "input": {"skill": s}}
    agent = lambda a: {"type": "tool_use", "name": "Agent", "input": {"subagent_type": a}}
    assert fires(ev(skill("sdlc:build"), agent("sdlc:implementer"))) == ["skill:build", "agent:implementer"]
    assert fires(ev(skill("sdlc:build"), parent="x")) == [], "a subagent's own calls are not counted"
    assert passed(["skill:build", "agent:implementer"], "agent:implementer") and not passed(["agent:Explore"], "agent:delegator")
    assert passed(["agent:Explore"], None) and not passed(["agent:delegator"], None)
    assert passed(["skill:story"], "story") and not passed(["skill:build", "skill:story"], "story")
    assert done(["skill:build"], "build") and not done(["skill:build"], "agent:implementer") and done(["agent:Explore"], "agent:x")
    print("self-test passed")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="expected skill or agent name, such as build or reviewer; 'none' for negatives")
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--model", default="sonnet")
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--timeout", type=int, default=150, help="seconds per run")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    label = lambda e: e.split(":")[-1] if e else "none"
    cases = [(i, p, e) for i, (p, e) in enumerate(CASES) if not a.only or label(e) == a.only]
    with cf.ThreadPoolExecutor(a.jobs) as pool:
        rows = list(pool.map(lambda c: run_one(c[0], c[1], c[2][1], c[2][2], a.model, a.timeout),
                             [(i, n, c) for c in cases for n in range(1, a.runs + 1) for i in [c[0]]]))
    print(f"{'target':18}{'hits':>8}")
    for t in sorted({label(r["expected"]) for r in rows}):
        rs = [r for r in rows if label(r["expected"]) == t]
        print(f"{t:18}{sum(r['pass'] for r in rs):>4}/{len(rs):<3}")
    print(f"{'ALL':18}{sum(r['pass'] for r in rows):>4}/{len(rows):<3}")
    for r in rows:
        if not r["pass"]:
            print(f"miss [{label(r['expected'])}] {r['prompt']!r} -> {r['fired'] or 'nothing'}")
    os.makedirs(RUNS, exist_ok=True)
    json.dump(rows, open(os.path.join(RUNS, "last.json"), "w"), indent=1)


if __name__ == "__main__":
    sys.exit(main())
