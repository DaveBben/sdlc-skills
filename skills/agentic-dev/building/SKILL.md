---
name: building
description: "Use once the story skill has framed a change and the person chose to build it now, or when the person says a change framed or agreed earlier in this session should now be built, such as 'that's agreed, go ahead and build it'. Never the first step for a new change to code: that is the story skill's. How to change code here: attack the design with a pre-mortem, make the smallest complete change in its own worktree, and call it done only when a check passed, then hand a non-trivial change to the reviewing skill."
license: MIT
metadata:
  version: "6.3.0"
---
# Building

## Before the Plan

* **Read the code the change touches first, and its definition of done:** the exact names, paths and the data's real shape, what to reuse and the patterns to follow, and the CI jobs, linters, type checker, import rules and coverage floor the change must pass.
* **Read the docs of each library or API the plan calls,** each answer marked `doc`, with the link, or `memory`.
* **Ask the design decisions only the person can make,** after reading the code and its ADRs: each one-way door (architecturally significant decision) the story and its walking skeleton imply, implementation choices included. Decide the two-way doors yourself as `Decided: X, because Y`.

## Writing a Plan

* **Only write a plan** when you cannot state the diff in one sentence.
* **Design it:** the components and how they connect, then small steps, each a readable diff, risk rising down the list.
* **Pre-mortem the design:** the bug reports it would get, each pinned to a file, caller, doc or real input you checked, and add the defence against each to the steps. Skip cases nothing can produce.
* **Have a fresh subagent review the plan** before you present it, on your strongest model, by [references/design-review.md](references/design-review.md), when it touches security (auth, permissions, secrets, a trust boundary), stored data (a schema change or migration) or concurrency (shared state, retries, ordering), or is large (more than about 400 changed lines).
* **Present it in chat** for the person to review, in plain English, at the level of intent, not code, ending with the one-way doors for them to decide.

## Writing the Code

* **Build on a new branch in its own git worktree,** never in the person's checkout.
* **Build in this order** when the frame has acceptance criteria or a bug's reproduction; a change with no new rule keeps its `Done when:` line:
  1. **Interfaces with no implementation:** each new name's signature and a stub that returns an empty value, committed alone.
  2. **Red:** failing tests first, by [references/tests.md](references/tests.md): one per criterion example, each seen failing on its assertion, committed alone as `test(red): <title>`. After that commit a test changes only with the person's word.
  3. **Green:** implement until those tests pass, changing no test.
* **Make the smallest complete change (KISS, YAGNI):** the whole task with every caller, test and fixture it breaks. Add error handling only for a trigger you can name. Never cut trust-boundary validation, data-loss handling or security. Name what you left out.

## Finishing

* **Report done with a passing check:** its command, its result and what you did not check.
* **On the second correction of the same mistake,** propose a check, hook or test that catches it.
* **Once the check passes,** load the reviewing skill for any change beyond a one- or two-line edit.
