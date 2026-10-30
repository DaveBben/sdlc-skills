#!/usr/bin/env python3
"""Score each sdlc agent's description by whether a session launches it unprompted.

The skills describe a step ("have a fresh subagent challenge the tests blind")
without naming an agent, so the harness must pick the agent from its
description. Skills are disallowed by default (--skills allows them), so each
case measures the description at the moment it describes, not whether a capped
session walks a skill from its first step to the delegating one. Each case is a first message to a fresh `claude -p` session in a
gauge.py fixture; the gauge records the first subagent launched, ignoring the
harness's own scouts (Explore, Plan), and stops the session there.

Cases live in a JSON file written blind to the descriptions:
{"train": [{"q", "want", "fixture"}], "holdout": [...]}, want null for a
negative, which passes when no sdlc agent launches before a skill loads or the
session ends.

Usage:
    python3 tools/agent-gauge.py CASES.json                  # train split
    python3 tools/agent-gauge.py CASES.json --split holdout
    python3 tools/agent-gauge.py CASES.json --only mapper,none --jobs 12
"""
import argparse
import json
import os
import subprocess
import sys

from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gauge

TARGET = 0.85
AGENTS = {"router", "reviewer", "verifier", "test-challenger", "implementer", "mapper"}
SKILLS = False
SCOUTS = {"Explore", "Plan", "claude-code-guide", "statusline-setup"}

ISSUE = """# #{n} {title}

Labels: {label}

{body}

## Comments

**maria** ({day} Oct): {comment}
"""
ISSUES = [
    ("bug", "Export times out past 10k orders", "Given 12,000 orders, when I export, then I get a file, but the request times out after 30 s.", "Repro on staging with the seed script."),
    ("story", "Cancel an order before it ships", "As a customer I want to cancel an unshipped order.", "Question for @dave: refund to card or store credit?"),
    ("bug", "Dashboard toast never fades on Safari", "Given Safari 18, when an order arrives, then the toast fades, but it stays.", "Low priority."),
    ("story", "Show order count per day", "As an operator I want a daily count on the dashboard.", "Ready once #104 lands."),
    ("chore", "Bump pg to 8.13", "Done when tests pass on 8.13.", "Blocked by #110."),
]


def add_extras(mid):
    for i in range(30):
        label, title, body, comment = ISSUES[i % len(ISSUES)]
        n = 101 + i
        path = os.path.join(mid, "issues", f"{n}.md")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as fh:
            fh.write(ISSUE.format(n=n, title=f"{title} ({n})", label=label,
                                  body=body, day=1 + i % 28, comment=comment))
    for i in range(1, 13):
        with open(os.path.join(mid, "docs", "adr", f"{i:04d}-decision-{i}.md"), "w") as fh:
            fh.write(f"# Decision {i}\n\nStatus: accepted\n\n## Decision\n\n"
                     f"Orders service rule {i}: money in cents; Postgres is the only store.\n\n"
                     "## Why\n\nOne source of truth.\n\n## Rejected\n\nA cache in Redis.\n")
    spec = os.path.join(mid, "docs", "spec", "cursor-pagination", "spec.md")
    os.makedirs(os.path.dirname(spec), exist_ok=True)
    with open(spec, "w") as fh:
        fh.write("## Spec\n\nCursor pagination for exportOrders: 50 rows a page ordered by id; "
                 "nextCursor is the last id, null on the last page.\n")
    review = os.path.join(mid, ".review")
    os.makedirs(review, exist_ok=True)
    diff = subprocess.run(["git", "diff"], cwd=mid, capture_output=True, text=True).stdout
    files = {
        "diff.patch": diff,
        "story.md": "# Cursor pagination\n\n1. Given 120 orders, when I export page 1, then I get 50 and nextCursor order_50.\n",
        "reading-list.md": "tier: full-read\nsrc/orders.js:2-6: criterion 1\nCheck: the cursor query on an empty page\n",
        "findings.md": "1|orders.js|bug|src/orders.js:3|page undefined|query with ''|default cursor|none\n",
    }
    for n in (1, 2, 3):
        files[f"findings-{n}.md"] = f"{n}|orders.js|bug|src/orders.js:3|page undefined|query with ''|default cursor|none\n"
    for rel, body in files.items():
        with open(os.path.join(review, rel), "w") as fh:
            fh.write(body)
    gauge._git(mid, "add", "-A")
    gauge._git(mid, "commit", "-qm", "issues, ADRs, review directory")


def run_one(case):
    """Run one case; stop at the first non-scout subagent, or a skill for a negative."""
    query, want, cwd = case
    cmd = ["claude", "-p", query,
           *[a for d in gauge.PLUGIN_DIRS for a in ("--plugin-dir", d)],
           "--output-format", "stream-json", "--verbose",
           "--max-turns", str(gauge.TURNS), "--setting-sources", "project",
           "--model", gauge.MODEL, *([] if SKILLS else ["--disallowedTools", "Skill"])]
    proc = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE,
                            stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                            text=True)
    tools, got, stop = [], None, False
    try:
        for line in proc.stdout:
            if not line.startswith("{"):
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            if d.get("type") != "assistant":
                continue
            for b in d.get("message", {}).get("content", []):
                if b.get("type") != "tool_use":
                    continue
                inp = b.get("input", {})
                if b["name"] in ("Agent", "Task"):
                    kind = inp.get("subagent_type", "general-purpose")
                    tools.append(f"Agent:{kind}")
                    if kind not in SCOUTS:
                        got, stop = kind.split(":")[-1], True
                else:
                    tools.append(b["name"] if b["name"] != "Skill" else f"Skill:{inp.get('skill', '')}")
                    stop = stop or (b["name"] == "Skill" and want is None)
                if stop:
                    break
            if stop:
                break
    finally:
        proc.kill()
        proc.wait()
    return query, want, tools, got


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cases")
    ap.add_argument("--split", default="train")
    ap.add_argument("--only", help="comma-separated agents; 'none' for negatives")
    ap.add_argument("--jobs", type=int, default=10)
    ap.add_argument("--model", default="sonnet")
    ap.add_argument("--skills", action="store_true")
    args = ap.parse_args()
    gauge.MODEL = args.model
    global SKILLS
    SKILLS = args.skills
    only = set(args.only.split(",")) if args.only else None

    root = os.path.join(gauge.REPO, ".gauge-fixtures")
    subprocess.run(["rm", "-rf", root], check=True)
    os.makedirs(root)
    fresh, mid, _ = gauge.build_fixtures(root)
    add_extras(mid)
    where = {"fresh": fresh, "mid": mid}

    cases = [(c["q"], c["want"], where[c.get("fixture", "mid")])
             for c in json.load(open(args.cases))[args.split]
             if not only or (c["want"] or "none") in only]
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(run_one, cases))

    buckets = {}
    for query, want, tools, got in results:
        hit = got == want if want else got not in AGENTS
        buckets.setdefault(want or "none", []).append(hit)
        if not hit:
            print(f"FAIL  want={want or 'none':15s} got={got or '(none)':15s} "
                  f"{query[:80]}  tools={tools[:6]}")
    print()
    ok = True
    for name in sorted(buckets):
        hits = buckets[name]
        rate = sum(hits) / len(hits)
        ok &= rate >= TARGET
        print(f"  {name:15s} {sum(hits)}/{len(hits)}  ({rate:.0%})")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
