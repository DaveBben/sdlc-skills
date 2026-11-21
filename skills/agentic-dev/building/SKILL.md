---
name: building
description: "Use once the story skill has framed a change and the person chose to build it now, or when the person says a change framed or agreed earlier in this session should now be built, such as 'that's agreed, go ahead and build it'. Never the first step for a new change to code: that is the story skill's. How to change code here: attack the design with a pre-mortem, make the smallest complete change in its own worktree, and call it done only when a check passed, then hand a non-trivial change to the reviewing skill."
license: MIT
metadata:
  version: "6.1.0"
---
# Build

* **Read the code the change touches first:** the exact names, paths and the data's real shape, what to reuse and the patterns to follow.
* **Ask the design decisions only the person can make,** after reading the code and its decision records: each one-way door the story and its walking skeleton imply, implementation choices included, such as "the criteria need each verdict stored: in the warehouse, in a new schema, or in a local SQLite file?". Decide the two-way doors yourself as `Decided: X, because Y`.
* **Sketch the components and how they connect** when the change spans more than one; this is the design the pre-mortem attacks.
* **Pre-mortem the design,** the person's or yours, before building on it: strongest objection first, each pinned to a file, caller or real input you checked. Skip style and cases nothing can produce. Ask about a one-way door; give any other objection one line, then build as asked.
* **Plan small steps** when the change does not fit one sentence: each a readable diff, risk rising down the list, a commit before each risky one.
* **Have a fresh subagent review a large plan** once, on your strongest model, by [references/design-review.md](references/design-review.md).
* **Build on a new branch in its own git worktree,** never in the person's checkout.
* **Build in this order** when the frame has acceptance criteria or a bug's reproduction; a change with no new rule keeps its `Done when:` line:
  1. **Interfaces with no implementation:** each new name's signature and a stub that returns an empty value, committed alone.
  2. **Failing tests first,** by [references/tests.md](references/tests.md): one per criterion example, each seen failing on its assertion, committed alone as `test(red): <title>`. After that commit a test changes only with the person's word.
  3. **Implement until those tests pass,** changing no test.
* **Make the smallest complete change (KISS, YAGNI):** the whole task with every caller, test and fixture it breaks. Add error handling only for a trigger you can name. Never cut trust-boundary validation, data-loss handling or security. Name what you left out.
* **Report done with a passing check:** its command, its result and what you did not check.
* **On the second correction of the same mistake,** propose a check, hook or test that catches it.
* **Once the check passes,** load the reviewing skill for any change beyond a one- or two-line edit.
