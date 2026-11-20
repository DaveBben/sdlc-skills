---
name: build
description: "Use first, before reading or editing code, for any change to code, however small: a feature, a bug or wrong output, a refactor, a new flag or a chore such as a dependency bump, like 'add a CSV export', 'the export crashes on an empty order list', 'rename total to order_total everywhere' or 'bump the requests dependency'. Not for reviewing a finished change, an experiment, or a question about code. How to change code here: attack the design with a pre-mortem, make the smallest complete change in its own worktree, and call it done only when a check passed."
license: MIT
metadata:
  version: "5.0.0"
---
# Build

* **Attack the user's design:** before building on it, one pre-mortem pass ("this failed in six months: how?"), strongest objection first, each pinned to a file, caller or real input in this codebase that you checked; skip style and cases nothing can produce. A large plan also gets one pass from a fresh-context reviewer. A one-way door stops for the user's choice; anything else gets one line and the task as asked.
* **KISS, YAGNI:** the smallest change that fully does the task, every caller, test and fixture it breaks included. Reuse this codebase, then the standard library, then an installed dependency; add no feature, option, abstraction or fallback beyond the ask, error handling only for a trigger you can name and a comment only for a why the code cannot show; keep trust-boundary validation, data-loss handling and security, and name what you left out.
* **Worktree:** a feature, bug fix or refactor goes in its own git worktree on a new branch, never the user's checkout.
* **Done means a check passed,** never your judgement: name the command, its result and what you did not check.
* **Fix the harness, not the promise:** on the second correction of the same mistake, propose a check, hook or test that catches it.
