#!/usr/bin/env python3
"""Score each SDLC skill's description against 30 phrases the user types for it.

Reuses gauge.py's fixtures and methodology notes (read them before believing a
number). Adds a UI, an LED controller, an AGENTS.md and a story file to the
fresh fixture so phrases about them have something to land on, and stops each
session as soon as a skill fires instead of running out the turn budget.

Usage:
    python3 tools/trigger-gauge.py                   # every skill, sonnet
    python3 tools/trigger-gauge.py --only spike      # one skill's phrases
    python3 tools/trigger-gauge.py --repeat 2 --jobs 10
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
TIMEOUT = 300

EXTRA = {
    "public/login.html": """<!doctype html>
<title>Sign in</title>
<form action="/login" method="post">
  <input type="email" name="email" placeholder="Email">
  <input type="password" name="password" placeholder="Password">
  <button>Sign in</button>
</form>
""",
    "public/dashboard.html": """<!doctype html>
<title>Orders dashboard</title>
<style>.toast { transition: opacity 300ms; }</style>
<div id="orders"></div><div class="toast" id="toast"></div>
<script>
function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg; t.style.opacity = 1;
  setTimeout(() => { t.style.opacity = 0; }, 2000);
}
fetch('/orders').then(r => r.json()).then(rows => {
  document.getElementById('orders').textContent = rows.length + ' orders';
});
</script>
""",
    "firmware/status_led.py": """# Drives the RGB status LED on the packing-station controller.
from machine import Pin

RED, GREEN, BLUE = Pin(2, Pin.OUT), Pin(3, Pin.OUT), Pin(4, Pin.OUT)

def set_color(r, g, b):
    RED.value(r); GREEN.value(g); BLUE.value(b)

def on_order_status(status):
    if status == "paid":
        set_color(0, 1, 0)
""",
    "AGENTS.md": """# orders-api

Express + Postgres service. Run `npm test` before committing.

## Layout
- src/ holds the service code; src/db.js is the only module that talks to Postgres.
- public/ holds the operator pages.
- firmware/ holds the packing-station LED controller (MicroPython).

## Conventions
- Use async/await everywhere.
- Money is stored in cents.
- Write good code and follow best practices.
- Be careful with the database.
""",
    "docs/stories/cancel-order.md": """# Story: cancel an order

As a customer, I want to cancel an order within 30 minutes of placing it,
so that I am not charged for a mistake.

## Acceptance criteria
1. Given an order placed 10 minutes ago with status pending, when the customer
   cancels it, then its status becomes cancelled and no payment is captured.
2. Given an order placed 31 minutes ago, when the customer cancels it, then the
   request is refused with "Cancellation window has closed".
""",
}

# skill -> 30 phrases. A phrase prefixed with "mid:" runs in the fixture that
# has an uncommitted diff, for phrases about the user's changes.
PHRASES = {
    "adr": [
        "let's capture this adr",
        "make an adr",
        "this is an architecture decision",
        "this is an archtiecture decision",
        "write an ADR for switching the export to keyset pagination",
        "capture this as an adr",
        "can you adr this",
        "we decided to go with postgres over mongo, make an adr for it",
        "record this decision",
        "let's document this architecture decision",
        "log this decision in our ADRs",
        "add an adr for using express over fastify",
        "we're going with SQS instead of kafka for the export jobs. capture that",
        "write up the decision we just made about storing money in cents",
        "this is a big decision, let's get it written down as an ADR",
        "create an architecture decision record for the payment capture flow",
        "make a decision record for moving auth into its own service",
        "put this decision in docs/adr: we never hard delete orders",
        "adr this choice",
        "let's capture why we chose raw pg over an ORM",
        "new adr: we're dropping offset pagination",
        "we should write an adr for this",
        "can you write the architecture decision for the caching approach we picked",
        "document why we picked jest over vitest",
        "this needs an ADR",
        "let's capture this architecture decision before we forget",
        "I want to record that we accept the risk of double-capturing payments on retry",
        "make an architectural decision record",
        "capture this adr: orders are soft deleted, never hard deleted",
        "we chose to keep the firmware in the same repo as the api. record the reasoning",
    ],
    "bug": [
        "fix the bug where placeOrder totals are wrong when qty is a string",
        "the export is broken, page 2 returns the same rows as page 1",
        "placeOrder stopped working after the last deploy",
        "users are getting a 500 when they place an order with no items",
        "exportOrders returns the wrong rows",
        "here is a bug report: orders placed with a negative quantity get a negative total",
        "the LED stays green when an order fails payment",
        "fix issue 42: the toast never disappears on the dashboard",
        "triage our bugs",
        "clean up the bug backlog",
        "why do we keep getting these pagination bugs?",
        "customers say they were charged twice for one order",
        "the login form submits even when the email is empty, that's a bug",
        "there's a bug in placeOrder",
        "the dashboard shows 0 orders even though there are orders in the database",
        "TypeError: Cannot read properties of undefined (reading 'reduce') in placeOrder",
        "orders are being exported twice",
        "the cancel window lets people cancel after 31 minutes, it should refuse",
        "we got a crash report from the packing station controller",
        "something is wrong with the order totals",
        "the export skips the 51st order",
        "this used to work last week and now placeOrder hangs",
        "a customer reported their order total was off by a cent",
        "our bug list has 40 open issues, help me sort them out",
        "go through the open bugs and tell me which to fix and which to close",
        "the dashboard toast flickers, fix it",
        "prod is leaking customer emails in the export, help",
        "placeOrder accepts items with a negative price, that shouldn't happen",
        "fix this regression in exportOrders",
        "the order count on the dashboard is wrong",
    ],
    "red-tests": [
        "write the failing tests for docs/stories/cancel-order.md",
        "write the tests first for cancelling an order",
        "red tests for the cancel order story",
        "TDD the cancel order story",
        "add a regression test for the export offset bug",
        "write a failing test that shows placeOrder accepts negative quantities",
        "this test is wrong: tests/orders.test.js expects 20 but the story says 22",
        "write failing tests for exportOrders returning a nextCursor",
        "write the tests before the code for the refund feature",
        "give me red tests for acceptance criterion 2 of the cancel story",
        "write test cases from the acceptance criteria in docs/stories/cancel-order.md",
        "lock in failing tests for the cancel order criteria",
        "let's do test-first: write the tests for order cancellation",
        "add a failing test for the bug where totals ignore qty",
        "I want failing tests for the 30 minute cancel window before anyone writes code",
        "write a test that reproduces the double-charge bug, don't fix it yet",
        "TDD this: cancelOrder(orderId) refuses after 30 minutes",
        "start with the failing tests for the csv export",
        "turn the cancel story's examples into failing jest tests",
        "the locked test for cancel window is wrong, correct it",
        "write a regression test for the empty items crash",
        "tests first please, for the refund endpoint",
        "red-green: write the red tests for exportOrders pagination",
        "write the expected-fail tests for the cancel order story",
        "add a regression test so the export bug can't come back",
        "write jest tests for the cancel order acceptance criteria before implementing",
        "write failing tests through the cancelOrder stub",
        "create the failing tests for the story, then stop",
        "one failing test per example in docs/stories/cancel-order.md",
        "the review found placeOrder accepts negative prices, write a failing test for it",
    ],
    "tracker": [
        "create the issues for docs/stories/cancel-order.md on github",
        "file these stories in jira",
        "put the cancel order story on the board",
        "open an issue for the export pagination work",
        "read issue 12",
        "update issue 12 with the new acceptance criteria",
        "link issue 4 as blocked by issue 3",
        "what is blocking issue 7?",
        "which issue is next?",
        "add the cancel story to our github project",
        "create a gitlab issue for the dark mode toggle",
        "file a gitea issue for the csv export",
        "put this on the board",
        "add it to the project board",
        "make issues for each story in docs/stories/cancel-order.md",
        "close issue 9 and comment the PR link",
        "what's in issue 15?",
        "show me the open issues",
        "label issue 3 as a spike",
        "create a jira ticket for the refund feature",
        "move issue 22 into the in progress column",
        "set issue 5 as blocking issue 6",
        "post the spike findings as a comment on issue 30",
        "add a comment to issue 12 saying it's ready for review",
        "import these stories into github issues",
        "push the stories to our tracker",
        "file the cancel order story as an issue",
        "can you read PAY-88 from jira",
        "which tracker issues are still open for the cancel feature",
        "create the issues and order them by dependency",
    ],
    "refactor": [
        "refactor placeOrder",
        "should src/orders.js be refactored?",
        "what code smells are in src/orders.js?",
        "clean up src/orders.js",
        "this code is messy, can you tidy it",
        "make src/db.js more readable",
        "simplify the exportOrders function",
        "tidy up the orders module",
        "reduce the duplication between placeOrder and exportOrders",
        "split src/orders.js into smaller modules",
        "remove dead code from src/",
        "where is our tech debt in this repo?",
        "extract the total calculation out of placeOrder into its own function",
        "rename db.insert to something clearer",
        "this function is too long, break it up",
        "I want to refactor before adding the refund feature",
        "make the change easy first: restructure orders.js so adding tax is a one-line change",
        "are there any smells in firmware/status_led.py?",
        "refactor the dashboard script, it's spaghetti",
        "the naming in src/db.js is confusing, clean it up",
        "inline the db wrapper, it's just a middle man",
        "replace the nested ifs in on_order_status with guard clauses",
        "which files in this repo most need cleaning up?",
        "can you restructure src/orders.js without changing behaviour",
        "get rid of the magic number 50 in exportOrders",
        "pay down some tech debt in the orders module",
        "is this code readable? src/orders.js",
        "deduplicate the order total logic",
        "move the SQL out of orders.js into db.js",
        "refactor this repo's orders code for readability",
    ],
    "onboard": [
        "onboard claude to this repo",
        "orient claude to this repo",
        "setup my claude.md",
        "setup my agents file",
        "review my agents.md",
        "review my claude.md",
        "is my claude.md good",
        "is my agent.md too long?",
        "write an AGENTS.md for this repo",
        "create a CLAUDE.md",
        "get claude up to speed on this codebase",
        "onboard yourself to this repo",
        "orient yourself",
        "familiarize yourself with this codebase and write down what the next agent needs",
        "my claude.md is getting huge, trim it",
        "what should go in my claude.md?",
        "audit my CLAUDE.md",
        "can you improve my agents.md",
        "rewrite our CLAUDE.md",
        "does my agents.md have anything useless in it?",
        "is my CLAUDE.md missing anything important?",
        "set up the agent instructions file for this repo",
        "help claude understand this repo",
        "onboard an ai agent to this project",
        "generate a claude.md",
        "check my agents.md",
        "update AGENTS.md now that we've added the firmware folder",
        "is there too much in my agents file",
        "make CLAUDE.md a symlink to AGENTS.md and clean it up",
        "is my agents.md any good for claude?",
    ],
    "review": [
        "mid:review this code",
        "mid:do a code review",
        "look at this merge request: https://gitlab.com/acme/orders-api/-/merge_requests/42",
        "review this pull request: https://github.com/acme/orders-api/pull/88",
        "review src/orders.js",
        "mid:can you review my changes",
        "mid:review the diff",
        "mid:code review please",
        "give me a code review on the export function",
        "mid:look over my changes before I merge them",
        "is PR 17 ready to merge?",
        "review MR !42",
        "review PR #17",
        "check src/orders.js for bugs",
        "mid:can you look at my changes in src/orders.js and tell me what's wrong",
        "review the last commit",
        "do a security review of src/db.js",
        "critique my implementation of placeOrder",
        "take a look at this pull request https://github.com/acme/orders-api/pull/91",
        "mid:review what's on this branch",
        "is the code in src/orders.js any good?",
        "poke holes in my placeOrder function",
        "look at MR 42 and tell me if it's good",
        "mid:review my uncommitted changes",
        "i'd like a second pair of eyes on the orders module",
        "can you give feedback on my code in src/",
        "mid:review the code I just wrote",
        "do a pr review on #88",
        "any problems with merge request 42?",
        "mid:sanity check my diff before I push",
    ],
    "spike": [
        "let's do a demo of websockets for live order updates",
        "I want to make an expirement on caching order totals in redis",
        "let's do a spike on keyset pagination",
        "what would a stripe integration into my codebase look like?",
        "how would incorporating prisma into my code affect it",
        "how hard would it be to setup graphql here",
        "would it be feasible to reach 1000 orders a second using express",
        "let's prototype a csv export",
        "can we try out bullmq for the export jobs",
        "build a quick proof of concept for partner webhooks",
        "I want to experiment with replacing pg with drizzle",
        "let's see if sqlite would work for local dev",
        "is it feasible to run this on cloudflare workers?",
        "how much work would it be to add multi-tenancy",
        "what would it take to migrate this to typescript",
        "mock up an admin page for refunds",
        "let's try a couple of approaches to rate limiting and see which is best",
        "spike out an integration with the shipping API",
        "would bun speed up our test suite?",
        "how hard would it be to move from jest to vitest?",
        "build a throwaway to see if streaming the export works",
        "could we use postgres listen/notify instead of polling? try it",
        "let's experiment with an LLM to categorise orders",
        "what would adding opentelemetry to this codebase look like",
        "quick experiment: does connection pooling fix the slow export",
        "would it be possible to get the export under 200ms with an index",
        "let's build a demo of the checkout flow for friday's meeting",
        "how would switching to fastify affect the codebase",
        "test out whether redis caching makes placeOrder faster",
        "is it realistic to do real-time order tracking with server-sent events",
    ],
    "story": [
        "let's add a forgot email link",
        "let's add a timer to the ui",
        "I want modify how long transitions show",
        "let's add this feature: customers can cancel an order",
        "let's create a feature to export orders as csv",
        "I want to modify this feature so the dashboard refreshes every 10 seconds",
        "review this story: docs/stories/cancel-order.md",
        "write the stories for letting customers reorder a past order",
        "I want the LED to turn red",
        "add a forgot password link to the login page",
        "users should be able to cancel an order within 30 minutes",
        "make the dashboard show total revenue for today",
        "add a dark mode toggle to the dashboard",
        "I want customers to get an email when their order ships",
        "change the toast so it stays up for 5 seconds",
        "let's let users filter orders by status",
        "add a button to retry failed payments",
        "the order total should include tax",
        "I want the export to include the customer's email",
        "let's add pagination to the order list",
        "can we show a spinner while the dashboard loads",
        "write a story for bulk order upload",
        "what should we build next?",
        "are the acceptance criteria in docs/stories/cancel-order.md any good?",
        "make the LED blink blue while an order is being packed",
        "add a confirmation dialog before deleting an order",
        "I want admins to be able to refund an order",
        "let's make the login page remember the user's email",
        "can we add a countdown on the dashboard until the next export runs",
        "when a payment fails, show the user why",
    ],
    "build": [
        "let's pair on the cancel order story",
        "build the cancel order story",
        "implement this story: docs/stories/cancel-order.md",
        "let's pair on docs/stories/cancel-order.md",
        "build docs/stories/cancel-order.md on autopilot",
        "pair with me on adding a cancel endpoint",
        "I'll drive, you take over when I get stuck: cancel order",
        "just build the cancel order story, I don't need to see it",
        "implement the cancel order story test-first",
        "let's build cancel order together",
        "take the wheel on cancel order, I've started the endpoint",
        "build story PAY-12",
        "implement story #12 from the tracker",
        "start building the cancel order story",
        "let's pair program the order cancellation",
        "autopilot the cancel order story to a pull request",
        "you build it: docs/stories/cancel-order.md",
        "pick up the cancel order story and build it",
        "build the fix for issue 42, it's already triaged",
        "implement the agreed chore: bump express to 5",
        "pair on the refund flow with me",
        "let's code the cancel order story together, you write the tests",
        "build this story and open a PR",
        "go ahead and implement docs/stories/cancel-order.md",
        "I want to pair on the cancellation window logic",
        "write the code for the cancel order story",
        "let's mob on cancel order, you and me",
        "develop the cancel order feature from the story file",
        "build cancel order on autopilot and ping me at the PR",
        "pair with me, I want to own this cancel order code",
    ],
    "chore": [
        "bump express to version 5",
        "upgrade pg to the latest version",
        "node 18 is end of life, move us to node 22",
        "create a chore to upgrade express",
        "file a chore for rotating the database password",
        "rotate the DATABASE_URL credentials",
        "move the hardcoded config into environment variables",
        "migrate our CI to GitHub Actions",
        "add a Dockerfile so we can build this in CI",
        "update all our npm dependencies",
        "npm audit says pg has a vulnerability, upgrade it",
        "create a task to upgrade to express 5",
        "we need to renew the TLS certificate before it expires",
        "add dependabot to this repo",
        "pin the node version in package.json",
        "switch the build from npm to pnpm",
        "add a lockfile and commit it",
        "set up a nightly CI job that runs the tests",
        "set up an alert when the api error rate goes over 5%",
        "cache node_modules in CI so builds are faster",
        "make a chore ticket: upgrade micropython on the LED controller",
        "review this chore: upgrade express to v5, done when npm ls shows 5.x",
        "is this a good chore ticket? 'clean up dependencies'",
        "the api key in the firmware leaked, rotate it",
        "bump the pg driver, there's a CVE",
        "upgrade the postgres server from 14 to 16",
        "move our deploy from heroku to fly.io",
        "write up a task to migrate CI off travis",
        "speed up CI, it takes 12 minutes",
        "replace the deprecated url.parse calls before node removes them",
    ],
    "spec": [
        "write the spec for the cancel order story",
        "spec out docs/stories/cancel-order.md",
        "how should we build the cancel order story?",
        "help me design the cancel order story before you build it",
        "review this spec: docs/stories/cancel-order.md has a ## Spec block",
        "I want to work out the technical approach for cancel order first",
        "let's do the tech spec for cancel-order",
        "what's the design for cancelling orders? walk me through it before any code",
        "here's my approach: add a cancelled_at column and check it in placeOrder. what am I missing?",
        "critique my plan for the cancel endpoint before you start",
        "is this spec too long for such a small story?",
        "before you implement cancel-order, let's agree how it gets built",
        "which endpoints and tables does the cancel order story need? write it up",
        "we need a design doc for cancel order, the mobile team consumes the api",
        "how will cancel order fail, and what's the rollout? put it in the spec",
        "spec for the refund flow please, it touches the payment provider",
        "poke holes in my design for cancelling orders",
        "do we even need a spec for the cancel window story?",
        "walk me through the key decisions for the cancel order story",
        "the cancel order story is done, close out its spec",
        "attach a spec to the cancel order story",
        "give me the technical plan for docs/stories/cancel-order.md, one decision at a time",
        "check my spec covers every acceptance criterion",
        "what's the interface contract for cancel order? the web team needs it",
        "design the data changes for order cancellation before building",
        "I want to learn how to design this, coach me through the cancel order spec",
        "review the spec on issue 12 before we build it",
        "how do we roll out cancel order safely behind a flag? spec it",
        "is my approach to cancel order sound? cancel endpoint, status column, refund job",
        "the story is agreed, now let's figure out how to build it",
    ],
}

NEGATIVE = [
    "What's the difference between optimistic and pessimistic locking?",
    "explain how keyset pagination works",
    "what does the -u flag do in git push?",
    "Run the test suite and show me the output.",
    "what does placeOrder do?",
    "summarise the README",
    "whats the difference between arq and celery?",
    "what is semgrep?",
]


def add_extras(fresh):
    for rel, body in EXTRA.items():
        path = os.path.join(fresh, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as fh:
            fh.write(body)
    os.symlink("AGENTS.md", os.path.join(fresh, "CLAUDE.md"))
    gauge._git(fresh, "add", "-A")
    gauge._git(fresh, "commit", "-qm", "ui, firmware, agents file, story")


def run_one(case):
    """Run one query; stop the session at the first Skill call."""
    query, expected, cwd = case
    cmd = ["claude", "-p", query,
           *[a for d in gauge.PLUGIN_DIRS for a in ("--plugin-dir", d)],
           "--output-format", "stream-json", "--verbose",
           "--max-turns", str(gauge.TURNS), "--setting-sources", "project",
           "--model", gauge.MODEL]
    proc = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE,
                            stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                            text=True)
    tools, fired = [], None
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
                if b.get("type") == "tool_use":
                    tools.append(b["name"])
                    if b["name"] == "Skill":
                        fired = b.get("input", {}).get("skill", "").split(":")[-1]
            if fired:
                break
    finally:
        proc.kill()
        proc.wait()
    return query, expected, tools, fired


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="comma-separated skills; 'none' for negatives")
    ap.add_argument("--jobs", type=int, default=10)
    ap.add_argument("--repeat", type=int, default=1)
    ap.add_argument("--model", default="sonnet")
    args = ap.parse_args()
    gauge.MODEL = args.model
    only = set(args.only.split(",")) if args.only else None

    root = os.path.join(gauge.REPO, ".gauge-fixtures")
    subprocess.run(["rm", "-rf", root], check=True)
    os.makedirs(root)
    fresh, mid, _ = gauge.build_fixtures(root)
    add_extras(fresh)
    add_extras(mid)

    cases = []
    for skill, phrases in PHRASES.items():
        if only and skill not in only:
            continue
        for p in phrases:
            cwd, q = (mid, p[4:]) if p.startswith("mid:") else (fresh, p)
            cases.append((q, skill, cwd))
    if not only or "none" in only:
        cases += [(q, None, fresh) for q in NEGATIVE]
    cases *= args.repeat

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(run_one, cases))

    buckets = {}
    for query, expected, tools, fired in results:
        hit = (fired == expected) if expected else (fired not in gauge.OURS)
        buckets.setdefault(expected or "none", []).append(hit)
        if not hit:
            print(f"FAIL  want={expected or 'none':12s} got={fired or '(none)':12s} "
                  f"{query[:70]}  tools={tools[:6]}")
    print()
    ok = True
    for skill, hits in buckets.items():
        rate = sum(hits) / len(hits)
        ok &= rate >= TARGET or skill == "none"
        print(f"  {skill:12s} {sum(hits)}/{len(hits)}  ({rate:.0%})")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
