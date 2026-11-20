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
    python3 tools/trigger-gauge.py --only retro --runs 3
    python3 tools/trigger-gauge.py --self-test
"""
import argparse, concurrent.futures as cf, json, os, shutil, subprocess, sys, time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN, RUNS = os.path.join(REPO, "plugins", "sdlc"), os.path.expanduser("~/.sdlc-trigger-runs")
SKILLS = {"build", "explain", "retro", "review"}
AGENTS = set()  # the plugin ships no agents; reviewers are reference files its skills launch

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
    ("Run a retro on the export change we just finished.", "retro"),
    ("The bulk discount is merged. What could I do better next time when working with you?", "retro"),
    ("Look back over the change we just made to pricing.py and tell me how to get better output from you.", "retro"),
    ("We gave up on the async export. Review how we worked on it.", "retro"),
    # Held out: phrased unlike any description, to catch wording tuned to the cases above.
    ("That refactor of pricing.py is done. Any lessons for how I prompt you?", "retro"),
    ("The new JSON endpoint shipped. Where did we lose time, and what should I do differently?", "retro"),
    ("The empty-cart change to pricing.py is finished. Review it and fix what really matters before I open the pull request.", "review"),
    ("Take my uncommitted change through review: verify what the reviewer finds and fix the blocking findings.", "review"),
    ("Get my working-tree change reviewed and ready to merge.", "review"),
    # Held out.
    ("I think the pricing edit is good to go. Have it checked properly and sort out anything serious first.", "review"),
    # Talk about review, with no finished change to review, gets none.
    ("What should a good code review checklist cover?", "explain"),  # a question about review, not a change to review
    ("Summarise what my uncommitted change does, for a pull request description.", None),
    ("Bump the requests dependency to the latest version.", "build"),
    # Held out.
    ("Can you wire up a new endpoint that returns order totals as JSON?", "build"),
    ("pricing.py is a mess of nested ifs, tidy it up without changing what it does.", "build"),
    ("Why does total give 9.999999 instead of 10 for some carts? I want to understand it before anything changes.", "explain"),
    ("How does the export decide which columns to write?", "explain"),
    # Held out.
    ("I don't get what a merge base is. Walk me through it.", "explain"),
    # A change about to start, or a trivial one, gets no retro.
    ("Add a CSV export to the orders page.", "build"),
    ("The export crashes on an empty order list. Fix it.", "build"),
    ("Rename total to order_total everywhere.", "build"),
    ("Write a story for letting customers download their order history.", None),
    ("Do a spike on using Polars for the export.", None),
    ("Break the order-history PRD in docs/prd/history.md into stories.", None),
    ("I just bumped the export timeout in AGENTS.md from 30 to 60 seconds. Done.", None),
    ("What does pricing.py do?", "explain"),
    ("Find every caller of total.", None),
    ("Explain what a property-based test is.", "explain"),
    ("How do I run the tests here?", None),
    ("Commit this.", None),
]

# Requests to review a change, which the review skill takes; the last 6 are held out, phrased unlike any description.
AGENT_CASES = {
    "code-reviewer": [
        "Review my changes.",
        "Give me a second-opinion review of my uncommitted changes before I commit.",
        "Find the bugs in my working-tree diff.",
        "Do a code review of my uncommitted change to pricing.py.",
        "Review the diff against main.",
        "Code review please: the change in pricing.py.",
        "Check my diff for bugs before I push.",
        "Give my working-tree changes an independent, blind review.",
        "Review the uncommitted edits before I open a pull request.",
        "Do an unbiased review of what's uncommitted.",
        "Is my uncommitted change to total() correct? Review it.",
        "Review the last commit and my uncommitted changes.",
        "Have someone other than me review the change to pricing.py.",
        "Review pricing.py's diff for edge cases I missed.",
        "Look over what I just changed and tell me what's broken.",
        "Before this goes in, can a fresh pair of eyes go through my edit to pricing.py?",
        "Sanity-check the empty-cart handling I just added.",
        "I'm about to commit. Anything wrong with my edit?",
        "Tear apart my latest edit.",
        "Would you approve this if it were a merge request?",
    ],
}
# A request to review a change goes through the review skill, which launches the code-reviewer itself.
CASES += [(p, "review" if a == "code-reviewer" else "agent:" + a) for a, ps in AGENT_CASES.items() for p in ps]


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
    assert fires(ev(skill("sdlc:retro"), agent("sdlc:code-reviewer"))) == ["skill:retro", "agent:code-reviewer"]
    assert fires(ev(skill("sdlc:retro"), parent="x")) == [], "a subagent's own calls are not counted"
    assert passed(["skill:retro", "agent:code-reviewer"], "agent:code-reviewer") and not passed(["agent:Explore"], "agent:delegator")
    assert passed(["agent:Explore"], None) and passed(["agent:general-purpose"], None), "a general subagent is not ours"
    assert passed(["skill:retro"], "retro") and not passed(["skill:review", "skill:retro"], "retro")
    assert not passed(["skill:retro"], None) and passed(["skill:other"], None), "only sdlc skills count"
    assert done(["skill:retro"], "retro") and not done(["skill:retro"], "agent:code-reviewer") and done(["agent:Explore"], "agent:x")
    print("self-test passed")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="expected skill or agent names, comma-separated, such as build,code-reviewer; 'none' for negatives")
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--model", default="sonnet")
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--timeout", type=int, default=150, help="seconds per run")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    label = lambda e: e.split(":")[-1] if e else "none"
    cases = [(i, p, e) for i, (p, e) in enumerate(CASES) if not a.only or label(e) in a.only.split(",")]
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
