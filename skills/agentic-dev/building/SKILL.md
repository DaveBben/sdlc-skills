---
name: building
description: "Use once the story skill has framed a change and the person chose to build it now, or when the person says a change framed or agreed earlier in this session should now be built, such as 'that's agreed, go ahead and build it'. Never the first step for a new change to code: that is the story skill's. How to change code here: attack the design with a pre-mortem, make the smallest complete change in its own worktree, and call it done only when a check passed, then hand a non-trivial change to the reviewing skill."
license: MIT
metadata:
  version: "6.2.1"
---
# Build

* **Read the code the change touches first:** the exact names, paths and the data's real shape, what to reuse and the patterns to follow.
* **Ask the design decisions only the person can make,** after reading the code and its ADRs: each one-way door (architecturally significant decision) the story and its walking skeleton imply, implementation choices included. Decide the two-way doors yourself as `Decided: X, because Y`.
* **Write a plan** when the change does not fit one sentence, and present it in chat for the person to review, in plain English, at the level of intent, not code: the components and how they connect, then small steps, each a readable diff, risk rising down the list. Start it with a **pre-mortem**: the bug reports this change would get, each pinned to a file, caller or real input you checked, and the defence the plan builds against each. Skip cases nothing can produce. End with the one-way doors for the person to decide.
* **Have a fresh subagent review the plan** before you build, on your strongest model, by [references/design-review.md](references/design-review.md), when it touches security (auth, permissions, secrets, a trust boundary), stored data (a schema change or migration) or concurrency (shared state, retries, ordering), or is large (more than about 400 changed lines).
* **Build on a new branch in its own git worktree,** never in the person's checkout.
* **Build in this order** when the frame has acceptance criteria or a bug's reproduction; a change with no new rule keeps its `Done when:` line:
  1. **Interfaces with no implementation:** each new name's signature and a stub that returns an empty value, committed alone.
  2. **Red:** failing tests first, by [references/tests.md](references/tests.md): one per criterion example, each seen failing on its assertion, committed alone as `test(red): <title>`. After that commit a test changes only with the person's word.
  3. **Green:** implement until those tests pass, changing no test.
* **Make the smallest complete change (KISS, YAGNI):** the whole task with every caller, test and fixture it breaks. Add error handling only for a trigger you can name. Never cut trust-boundary validation, data-loss handling or security. Name what you left out.
* **Report done with a passing check:** its command, its result and what you did not check.
* **On the second correction of the same mistake,** propose a check, hook or test that catches it.
* **Once the check passes,** load the reviewing skill for any change beyond a one- or two-line edit.
