---
name: frame
description: "Use first, before reading or editing code, for any change to code, however small: a feature, a bug or wrong output, a refactor, a new flag or a chore such as a dependency bump, like 'add a CSV export', 'the export crashes on an empty order list', 'rename total to order_total everywhere', 'bump the requests dependency' or 'implement the story in docs/stories/x.md'. Not for reviewing a finished change, an experiment, or a question about code. Agrees with the person what to build and how done is checked, grilling a vague request, then hands to the build skill to build it now, or to the story skill to write it down for later."
license: MIT
metadata:
  version: "5.0.0"
---
# Frame

Agree what to build and how done is checked before any code. The same frame serves both outputs; only who reads it and when differs.

* **Grill a vague request:** one whose readings lead to materially different work; otherwise state your assumption and build. Before code, ask what only the user knows (the goal and why, constraints, a done-check they can watch run), each question with a concrete case, a question that hangs on an open answer waiting a round, and stop when the user confirms your play-back, not at a question count.
* **Acceptance criteria:** one per business rule, in the product's words, each with an example in real values and a check someone can run or watch; a rule with several cases gets a table, a row per case. Mark each `confirmed` (the user's words or a linked source), `assumed` (yours) or `unknown` (an open question, never a guess written as a rule); the frame is done when no `assumed` is left. The result follows the user's rule, not what the code does today. "Works correctly", "handles errors" and "is fast" are not criteria: nobody can watch them fail.
* **Where gaps hide:** none, one and many; duplicates, order and ties; a second run, a missed run, one bad item in a batch; what expires, leaks or costs money unattended; what the user sees and what is saved when a store or a call to another system fails; a person not allowed to act.
* **Mark each answer** about an unfamiliar library or API `doc`, with the link, or `memory`.
* **A story or bug report in the request is the frame already:** ask only what it leaves open.
* **Too big:** several features, or more than about 400 changed lines, is split into stories with the story skill before any is built.

## Hand off

The request says which; ask only when it does not.

* **Built now:** add the technical context the code shows (exact names, paths, the data's real shape), then load the build skill.
* **For later or for others:** stop at the business level, since files and data shapes go stale before it is built, and load the story skill to write it down.
