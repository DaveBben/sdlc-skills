---
name: building
description: "Use first, before editing any file, for every request that changes code, configuration, dependencies or tooling, however small, clear or casually phrased: a feature, a bug or wrong output to fix, a new flag, a changed limit or format, a refactor, a rename, a dependency bump, CI or dev-tool setup, or implementing a story, ticket or spec section, like 'add a CSV export', 'the export crashes on an empty order list, fix it', 'rename total to order_total everywhere', 'implement docs/stories/export.md'. Not for reviewing a finished change, a question about code, or a throwaway experiment or spike, which is the prototyping skill's. Grills the request before any code for what the person does not know or has not said (silent assumptions, the walking skeleton, lifecycles, edge cases, failing integration points, one-way doors, untestable criteria), then builds test-first in its own worktree, done only when a check passed."
license: MIT
metadata:
  version: "8.1.3"
---
# Building

The grilling is the work. The person gains most from what they do not know, are missing, or do not know that they do not know, so find it before any code.

## Frame

* **Read before asking:** the code the change touches and its ADRs, its definition of done (CI jobs, linters, type checker, coverage floor), and the docs of each library or API it calls.
* **Mark each answer** about an unfamiliar library or API `doc`, with the link, or `memory`.
* **Say where the request, the code and its docs disagree.** Between code and docs, trust the code.
* **Take a story, ticket or bug report the person brings as the frame,** and grill it like any request. A bug report's reproduction is the first red test; its expected and unchanged behaviour are the criteria.
* **Sort it:** a story changes something a user would notice; a chore does not (a refactor, rename, dependency bump, formatting, CI or a dev tool). A chore gets one `Done when:` line, such as the existing tests unchanged and green, in place of acceptance criteria and a UAT.

## Grill

Run every line against the request and the code. Each hit is a question with a concrete case from this codebase, or a gap you fill as `Assumed: X, because Y`.

### What was not said

* **Ask why** when the request names a solution, not a problem (XY problem): "add a Redis cache" where the need is "exports show data more than 15 minutes old".
* **Name who it is for** and their job to be done. The why is the person's, never yours.
* **Pin each overloaded term** to one meaning (ubiquitous language), checked against the glossary and the code: does "account" mean the customer or the user?
* **Pin each vague word** (fast, easy, robust, tidy, harden, "handles errors") to a number or a stated result.
* **List your silent assumptions:** each gap you would fill to keep going, as a question or an `Assumed:` line.
* **Name the unknown unknowns:** up to 3 parts new to this codebase or likely new to the person, each with the question that matters here and what goes wrong when it is skipped.

### How big it is

* **Split** several asks joined by "and", several features, or more than about 400 changed lines or 5 criteria into vertical slices. Grill and build the first; record the rest for later, each for a fresh session, with the tracker skill where it is installed.
* **Reject a layer as a slice:** each slice has a page, route or command where a person or test meets it.
* **Name each conflict:** a rule another story also states, or one main already meets.

### Where it breaks

* **Find the walking skeleton:** the thinnest version that runs end to end where it will really run. Each part the request leaves open (where it runs, what triggers it, where its data lives, how it signs in) is a question, and the first slice.
* **Trace each item's lifecycle (state transitions)** across runs: on the next run, after the person acts on it, when a step fails.
* **Walk each integration point** (each outside service, store or token): what the person sees and what is saved when it fails once, and when it fails every time.
* **Probe the edge cases:** none, one and many; duplicates, order, ties and what counts as equal (case, rounding, time zone); a second or missed run; one bad item in a batch; the format each side of a boundary expects; empty, huge, malformed and untrusted input; what expires, leaks or costs money unattended; a person not allowed to act.
* **Flag each one-way door** (data stored or sent, a contract others call, a dependency, auth, how it deploys, how the parts are split): options as equals, for the person to decide. Decide a two-way door yourself as `Decided: X, because Y`.

### Ask

* **Stop for** a gap whose readings lead to materially different work, and for a one-way door. Give the rest as notes and go on.
* **Ask in one round.** A question that hangs on an open answer waits a round.

## Criteria

The person writes the acceptance criteria. Critique them against these and fill the gaps.

* **One per business rule,** in the product's words, measurable: not "is fast" but "under 200 ms at 1,000 rows".
* **A Given/When/Then example in real values.** The Given says how its state came about, the When is one action, the Then states every result the rule decides. A rule with several cases gets a table.
* **A check someone can run** for each criterion.
* **A UAT:** how the person will see it work on the live system, with real credentials and services, read-only or as a dry run where it writes.
* **Follow the person's rule,** not what the code does today.
* **Add a criterion with its reason,** and keep it only once the person agrees.
* **Mark an open question `unknown`.**
* **Keep design out:** files, tables and layout wait for the plan.
* **Play back** for the person to confirm: the goal, the criteria, each `Assumed:` line and what this change will not do.

## Explore

* **Spike an unknown** that questions and docs cannot settle and that could change the plan, with the prototyping skill: now, in a subagent, when it fits this session. When it needs a day, or someone else's access or data, record it for later as blocking the change, with the tracker skill where it is installed, and stop.
* **Ask for what the UAT needs,** such as a test credential, a sandbox or read-only access, before you build.

## Plan

* **Write a plan** only when you cannot state the diff in one sentence: the components and how they connect, then small steps, each a readable diff, risk rising down the list.
* **Run a pre-mortem on it:** the bug reports it would get, each pinned to a file, caller, doc or real input you checked. Add the defence against each to the steps. Skip cases nothing can produce.
* **Have a fresh subagent review the plan,** on your strongest model, by [references/design-review.md](references/design-review.md), when it touches security (auth, permissions, secrets, a trust boundary), stored data (a schema change or migration) or concurrency (shared state, retries, ordering), or is over about 400 changed lines.
* **Present it in chat,** in plain English, as intent, not code, ending with the one-way doors for the person to decide.

## Build

* **Work on a new branch in its own git worktree,** never in the person's checkout.
* **Add characterization tests** before a refactor, where the tests miss the code that moves.
* **Build a story or a bug fix in this order;** a chore keeps its `Done when:` line:
  1. **Interfaces:** each new name's signature and a stub that returns an empty value, committed alone.
  2. **Red:** failing tests by [references/tests.md](references/tests.md), one per criterion example, each seen failing on its assertion, committed alone as `test(red): <title>`. After that commit a test changes only with the person's word.
  3. **Green:** implement until those tests pass, changing no test.
* **Make the smallest complete change (KISS, YAGNI):** the whole task with every caller, test and fixture it breaks. Add error handling only for a trigger you can name. Never cut trust-boundary validation, data-loss handling or security. Name what you left out.

## Finish

* **Check each `memory` answer** against its doc or a real call, and name each still unverified.
* **Report done with a passing check:** its command, its result and what you did not check. Done is every test green and the UAT run on the live system, with the person accepting its result.
* **Hand a change** beyond a one- or two-line edit to the reviewing skill.
