---
name: framing
description: "Use first, before editing any file, for every request that changes code, configuration, dependencies or tooling, however small, clear or casually phrased, even a one-line change or a quick tweak to a value, format or threshold: a feature, a bug or wrong output to fix, a refactor, deleting unused code, a new flag, adding a tool or bumping a dependency, a change to how something is computed, or implementing a story or a spec section, like 'add a CSV export', 'the export crashes on an empty order list, fix it', 'rename total to order_total everywhere' or 'bump the requests dependency'. Not for reviewing a finished change, an experiment, or a question about code. Agrees with the person what to build and how done is checked, grilling a vague request, then hands to the building skill to build it now, or to the story skill to write it down for later."
license: MIT
metadata:
  version: "5.1.0"
---
# Frame

* **Treat a story or bug report in the request as already framed:** ask only what it leaves open.
* **Grill a vague request,** one whose readings lead to materially different work: the goal and why, and the constraints, each question with a concrete case. A question that hangs on an open answer waits a round.
* **Ask why** when a request names a fix but not the problem (XY problem).
* **Say where the request, the code and its docs disagree.** Between code and docs, trust the code.
* **Probe the edge cases:** none, one and many; duplicates, order, ties and what counts as equal (case, rounding, time zone); a second or missed run; one bad item in a batch; what expires, leaks or costs money unattended; what the person sees and what is saved when another system fails; a person not allowed to act.
* **Mark each answer** about an unfamiliar library or API `doc`, with the link, or `memory`.
* **Spike first** when an unknown that questions and docs cannot settle could change the plan: load the spike skill.
* **Split a change too big for one merge request** into vertical slices, each written as a story with the story skill.

## Acceptance criteria

The person writes the criteria. Critique them against these rules and fill the gaps.

* **One per business rule,** in the product's words, measurable: not "is fast" but "under 200 ms at 1,000 rows".
* **A Given/When/Then example in real values.** The Given says how its state came about, the When is one action, and the Then states every result the rule decides. A rule with several cases gets a table, one row per case.
* **A check someone can run or watch.** When the change reads real data or calls another system, one check runs on real input, read-only or as a dry run.
* **Follow the person's rule,** not what the code does today.
* **Add a criterion with its reason,** why you think it is needed, and keep it only once the person agrees.
* **Mark an open question `unknown`.**
* **No new rule** (a rename, refactor, dependency bump or config value): no criteria, one `Done when:` line, such as the existing tests unchanged and green. Before a refactor, add characterization tests where the tests miss the moved code.

## Play back and hand off

* **Play back** the goal, the criteria and what this change will not do. End the play-back by asking whether to build it now or write it as a story for later. "I want to build X" says what the person wants, not when.
* **Offer up to 3 parts to explore,** new to this codebase or to the person, each with the question that matters for this task. None when there is no new rule.
* **Built now:** load the building skill.
* **For later or for others:** load the story skill.
