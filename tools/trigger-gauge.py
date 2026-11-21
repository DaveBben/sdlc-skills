#!/usr/bin/env python3
"""Measure whether each agentic-dev skill and agent fires on the requests meant for it, and stays quiet otherwise.

Each case is a first message to a fresh `claude -p` session in a small fixture repository, with this working
copy's plugin loaded and the user's own settings and plugins left out. The run stops at the first agentic-dev skill
or agent it reaches, so no agent's work runs:

  * a skill case passes when the first agentic-dev skill or agent is that skill;
  * an agent case passes when the first agent launched is that agent, whatever skill loaded before it;
  * a negative case passes when no agentic-dev skill or agent fires. Built-in agents such as Explore are allowed.

Target: 9 hits in 10 per skill and agent. Runs go under ~/.sdlc-trigger-runs, outside this repository and
outside the system temp directory, where skills do not load. Each run is a short headless session and costs
API money. Usage:

    python3 tools/trigger-gauge.py                       # every case once, on Sonnet
    python3 tools/trigger-gauge.py --only retro --runs 3
    python3 tools/trigger-gauge.py --self-test
"""
import argparse, concurrent.futures as cf, json, os, shutil, subprocess, sys, time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN, RUNS = os.path.join(REPO, "plugins", "agentic-dev"), os.path.expanduser("~/.sdlc-trigger-runs")
SKILLS = {"bug", "building", "explaining", "reflecting", "reviewing", "spike", "story", "tracker", "chore"}
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
    ("Run a retro on the export change we just finished.", "reflecting"),
    ("The bulk discount is merged. What could I do better next time when working with you?", "reflecting"),
    ("Look back over the change we just made to pricing.py and tell me how to get better output from you.", "reflecting"),
    ("We gave up on the async export. Review how we worked on it.", "reflecting"),
    # Held out: phrased unlike any description, to catch wording tuned to the cases above.
    ("That refactor of pricing.py is done. Any lessons for how I prompt you?", "reflecting"),
    ("The new JSON endpoint shipped. Where did we lose time, and what should I do differently?", "reflecting"),
    ("The empty-cart change to pricing.py is finished. Review it and fix what really matters before I open the pull request.", "reviewing"),
    ("Take my uncommitted change through review: verify what the reviewer finds and fix the blocking findings.", "reviewing"),
    ("Get my working-tree change reviewed and ready to merge.", "reviewing"),
    # Held out.
    ("I think the pricing edit is good to go. Have it checked properly and sort out anything serious first.", "reviewing"),
    # Talk about review, with no finished change to review, gets none.
    ("What should a good code review checklist cover?", "explaining"),  # a question about review, not a change to review
    ("Summarise what my uncommitted change does, for a pull request description.", None),
    ("Bump the requests dependency to the latest version.", "chore"),
    # Held out.
    ("Can you wire up a new endpoint that returns order totals as JSON?", "story"),
    ("pricing.py is a mess of nested ifs, tidy it up without changing what it does.", "chore"),
    ("Why does total give 9.999999 instead of 10 for some carts? I want to understand it before anything changes.", "explaining"),
    ("How does the export decide which columns to write?", "explaining"),
    # Held out.
    ("I don't get what a merge base is. Walk me through it.", "explaining"),
    # A change about to start, or a trivial one, gets no retro.
    ("Add a CSV export to the orders page.", "story"),
    ("The export crashes on an empty order list. Fix it.", "story"),
    ("Rename total to order_total everywhere.", "chore"),
    ("Write a story for letting customers download their order history.", "story"),
    ("Break the order-history PRD in docs/prd/history.md into stories.", "story"),
    ("Critique the story in docs/stories/export.md before the team picks it up.", "story"),
    # Held out.
    ("Order history is far too much for one go. Carve it into pieces that each ship on their own, for the backlog.", "story"),
    # Implementing a story starts at the story skill; a question about stories is not the story skill's.
    ("Implement the story in docs/stories/export.md.", "story"),
    ("Management wants a date: how many weeks will the remaining order-history stories take?", "story"),
    ("What makes a good acceptance criterion?", "explaining"),
    ("Do a spike on using Polars for the export.", "spike"),
    ("How hard would it be to make the export async?", "spike"),
    ("Would streaming the export keep memory flat at a million orders? Try it and see.", "spike"),
    # Held out.
    ("Before we commit to sqlite, knock together something disposable to find out if it copes with our order volume.", "spike"),
    # The real change, or a question about spikes, is not the spike skill's.
    ("Make the export async.", "story"),
    ("What is a spike, and when is one worth running?", "explaining"),
    ("File a bug: the export writes a blank file when there are no orders. Don't fix it yet.", "bug"),
    ("Customers say the export sometimes drops the last order. Reproduce it and write it up; no fix for now.", "bug"),
    ("Go through our open bug backlog and decide what to do with each one.", "bug"),
    # Held out.
    ("The empty-cart crash went live last week although CI was green and two people approved it. What let it through?", "bug"),
    # A fix, or a question about bug reports, is not the bug skill's; so is 'The export crashes ... Fix it.' above.
    ("total returns 9.99 for a 10.00 cart. Find the cause and patch it.", "story"),
    ("What belongs in a good bug report?", "explaining"),
    ("I just bumped the export timeout in AGENTS.md from 30 to 60 seconds. Done.", None),
    ("What does pricing.py do?", "explaining"),
    ("Find every caller of total.", None),
    ("Explain what a property-based test is.", "explaining"),
    ("How do I run the tests here?", None),
    ("Commit this.", None),
]

# Requests to review a change, which the reviewing skill takes; the last 6 are held out, phrased unlike any description.
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
# A request to review a change goes through the reviewing skill, which launches the code-reviewer itself.
CASES += [(p, "reviewing" if a == "code-reviewer" else "agent:" + a) for a, ps in AGENT_CASES.items() for p in ps]


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
    """The agentic-dev skills and every agent one stream-json event launches from the main session, in order."""
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
    assert fires(ev(skill("agentic-dev:reflecting"), agent("agentic-dev:code-reviewer"))) == ["skill:reflecting", "agent:code-reviewer"]
    assert fires(ev(skill("agentic-dev:reflecting"), parent="x")) == [], "a subagent's own calls are not counted"
    assert passed(["skill:reflecting", "agent:code-reviewer"], "agent:code-reviewer") and not passed(["agent:Explore"], "agent:delegator")
    assert passed(["agent:Explore"], None) and passed(["agent:general-purpose"], None), "a general subagent is not ours"
    assert passed(["skill:reflecting"], "reflecting") and not passed(["skill:reviewing", "skill:reflecting"], "reflecting")
    assert not passed(["skill:reflecting"], None) and passed(["skill:other"], None), "only agentic-dev skills count"
    assert done(["skill:reflecting"], "reflecting") and not done(["skill:reflecting"], "agent:code-reviewer") and done(["agent:Explore"], "agent:x")
    print("self-test passed")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="expected skill or agent names, comma-separated, such as build,code-reviewer; 'none' for negatives")
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--model", default="sonnet")
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--timeout", type=int, default=150, help="seconds per run")
    ap.add_argument("--cases", default=os.path.join(REPO, "tools", "trigger-cases.json"),
                    help="JSON list of {prompt, expected, source}; expected is a skill name or null. Falls back to CASES")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    label = lambda e: e.split(":")[-1] if e else "none"
    # A case that refers to an earlier conversation cannot pass as a first message, so it is listed but not run.
    pool_ = [(c["prompt"], c["expected"]) for c in json.load(open(a.cases)) if not c.get("needs_context")] if os.path.exists(a.cases) else CASES
    cases = [(i, p, e) for i, (p, e) in enumerate(pool_) if not a.only or label(e) in a.only.split(",")]
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
