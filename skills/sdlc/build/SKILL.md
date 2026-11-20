---
name: build
description: "Use once the frame skill has agreed what to build now, or when the person says to go ahead on a change already framed in this session. Never the first step for a new change to code: that is the frame skill's. How to change code here: attack the design with a pre-mortem, make the smallest complete change in its own worktree, and call it done only when a check passed."
license: MIT
metadata:
  version: "5.0.0"
---
# Build

* **Attack the user's design** before building on it: one pre-mortem pass ("this failed in six months: how?"), strongest objection first, each pinned to a file, caller or real input you checked in this codebase; no style, no case nothing can produce. A large plan also gets one review by a fresh subagent following [references/design-review.md](references/design-review.md), on your strongest model. A one-way door waits for the user's choice; anything else gets one line, then the task as asked.
* **Worktree:** a feature, bug fix or refactor goes in its own git worktree on a new branch, never the user's checkout.
* **KISS, YAGNI:** the smallest change that fully does the task, with every caller, test and fixture it breaks. Reuse this codebase, then the standard library, then an installed dependency. Beyond the ask, no feature, option, abstraction or fallback; error handling only for a trigger you can name; a comment only for a why the code cannot show. Never cut trust-boundary validation, data-loss handling or security. Name what you left out.
* **Done means a check passed,** never your judgement: name the command, its result and what you did not check.
* **Fix the harness, not the promise:** on the second correction of the same mistake, propose a check, hook or test that catches it.
