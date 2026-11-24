---
name: building
description: "Use first, before editing any file, for every request that changes code, configuration, dependencies or tooling, however small, clear or casually phrased: a feature, a bug or wrong output to fix, a new flag, a changed limit or format, a refactor, a rename, a dependency bump, CI or dev-tool setup, or implementing a story, ticket or spec section, like 'add a CSV export', 'the export crashes on an empty order list, fix it', 'rename total to order_total everywhere', 'implement docs/stories/export.md'. Not for reviewing a finished change, a question about code, or a throwaway experiment or spike, which is the prototyping skill's. Plans the change, attacks the plan with a pre-mortem and a fresh review where it is risky, then builds test-first in its own worktree, with failing tests that fail for the right reason, done only when a check passed and the person accepted the UAT."
license: MIT
metadata:
  version: "9.0.0"
---
# Building

* **Take the criteria and the UAT from what the person brought:** a story, ticket, spec section or bug report, whose reproduction is the first red test. When nothing states them, ask for them before any code.
* **Follow a design doc or ADR the change falls under,** linked from what the person brought or in `docs/design/` or `docs/adr/`: its decision and one-way doors are settled, so plan within them. Put each place the code as it stands contradicts it to the person; a changed decision is a new ADR, never an edit to the old one.

## Plan

* **Write a plan** only when you cannot state the diff in one sentence: the components and how they connect, then small steps, each a readable diff, risk rising down the list.
* **Run a pre-mortem on it,** starting from the design's risks and the chosen option's failure modes where there is one: the bug reports it would get, each pinned to a file, caller, doc or real input you checked. Look for them in each item's lifecycle across runs, each integration point failing once and failing every time, and the edge cases: none, one and many, duplicates and ties, empty, huge, malformed and untrusted input. Add the defence against each to the steps. Skip cases nothing can produce.
* **Have a fresh subagent review the plan,** on your strongest model, by [references/design-review.md](references/design-review.md), with the design doc where there is one, when it touches security (auth, permissions, secrets, a trust boundary), stored data (a schema change or migration) or concurrency (shared state, retries, ordering), or is over about 400 changed lines.
* **Present it in chat,** in plain English, as intent, not code, ending with the one-way doors for the person to decide.

## Build

* **Work on a new branch in its own git worktree,** never in the person's checkout.
* **Add characterization tests** before a refactor, where the tests miss the code that moves.
* **Build a change in behaviour in this order;** a refactor, rename, dependency bump or other chore keeps the existing tests unchanged and green:
  1. **Interfaces:** each new name's signature and a stub that returns an empty value, committed alone.
  2. **Red:** failing tests by [references/tests.md](references/tests.md), one per criterion example, each seen failing on its assertion, committed alone as `test(red): <title>`. After that commit a test changes only with the person's word.
  3. **Green:** implement until those tests pass, changing no test.
* **Make the smallest complete change (KISS, YAGNI):** the whole task with every caller, test and fixture it breaks. Add error handling only for a trigger you can name. Never cut trust-boundary validation, data-loss handling or security. Name what you left out.

## Finish

* **Check each claim about a library or API you made from memory** against its doc or a real call, and name each still unverified.
* **Report done with a passing check:** its command, its result, what you did not check and each departure from the design doc. Done is every test green and the UAT run on the live system, with the person accepting its result.
* **Hand a change** beyond a one- or two-line edit to the reviewing skill.
