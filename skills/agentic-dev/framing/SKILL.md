---
name: framing
description: "Use first, before editing any file, for every request that changes code, configuration, dependencies or tooling, however small, clear or casually phrased, even a one-line change or a quick tweak to a value, format or threshold: a feature, a bug or wrong output to fix, a refactor, deleting unused code, a new flag, adding a tool or bumping a dependency, a change to how something is computed, or implementing a story or a spec section, like 'add a CSV export', 'the export crashes on an empty order list, fix it', 'rename total to order_total everywhere' or 'bump the requests dependency'. Not for reviewing a finished change, an experiment, or a question about code. Agrees with the person what to build and how done is checked, grilling a vague request, then hands to the building skill to build it now, or to the story skill to write it down for later."
license: MIT
metadata:
  version: "5.0.0"
---
# Frame

Agree what to build and how done is checked before any code.

* **Grill a vague request:** one whose readings lead to materially different work; otherwise state your assumption and build. A request that names a fix but not the problem gets one question, the why: a cheaper way, even no code, may meet it. Then read what the request touches: raise where the request contradicts the code or its docs, and where those two disagree, trust the code and say so. Ask what only the user knows (the goal and why, constraints, a done-check they can watch run), each question with a concrete case; a question that hangs on an open answer waits a round. Stop when the user confirms your play-back, which names what this change will not do, not at a question count.
* **Acceptance criteria:** one per business rule, in the product's words, each with an example as Given/When/Then in real values, a few steps long (the Given says how its state came about, the When is one action, the Then states every result the rule decides) and a check someone can run or watch; a rule with several cases gets a table, a row per case. Mark each `confirmed` (the user's words or a linked source), `assumed` (yours) or `unknown` (an open question, never a guess written as a rule); the frame is done when no `assumed` is left. The result follows the user's rule, not what the code does today. A criterion is measurable: not "is fast" but "under 200 ms at 1,000 rows". When the change reads real data or calls another system, one check runs on real input, read-only or as a dry run.
* **No new rule** (a rename, refactor, dependency bump or config value): no criteria, one `Done when:` line, such as the existing tests unchanged and green; for a refactor, characterization tests first where tests miss the moved code.
* **Where gaps hide:** first none, one and many; duplicates, order, ties and what counts as equal (case, rounding, time zone); then a second run, a missed run, one bad item in a batch; what expires, leaks or costs money unattended; what the user sees and what is saved when a store or a call to another system fails; a person not allowed to act.
* **Mark each answer** about an unfamiliar library or API `doc`, with the link, or `memory`.
* **An unknown that questions and docs cannot settle,** and that could change the plan, goes to the spike skill before any is built.
* **A story or bug report in the request is the frame already:** ask only what it leaves open.
* **Too big:** several features, or more than about 400 changed lines, is split into stories with the story skill before any is built.

## Hand off

The request says which; ask only when it does not.

* **First name what may be new to the user:** at most 3 parts this change touches that are new to this codebase or that their answers showed unfamiliar, each with the question that matters for this task, drawn from the gaps above. They pick which to explore, by question and answer, or skip. None for a change with no new rule.
* **Built now:** add the technical context the code shows (exact names, paths, the data's real shape), then load the building skill.
* **For later or for others:** stop at the business level and load the story skill to write it down.
