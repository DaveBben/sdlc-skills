---
name: story
description: "Use first, before editing any file, for every request that changes code, configuration, dependencies or tooling, however small, clear or casually phrased, even a one-line change or a quick tweak to a value, format or threshold: a feature, a bug or wrong output to fix, a refactor, deleting unused code, a new flag, adding a tool or bumping a dependency, or implementing a story or a spec section, like 'add a CSV export', 'the export crashes on an empty order list, fix it', 'rename total to order_total everywhere' or 'implement docs/stories/export.md'. Also when work is to be written down for later or for others, critiqued, split or forecast, like 'write a story for X', 'critique the story in docs/stories/x.md', 'break this PRD into stories' or 'how many weeks for the remaining stories'. Not for reviewing a finished change, an experiment, or a question about code. Every change starts as a user story: who it is for, why, and acceptance criteria; then the building skill builds it now, or it is written down for later."
license: MIT
metadata:
  version: "6.1.0"
---
# Story

Every change starts as a user story: who it is for, why, and how done is checked. It goes to a file only when it is for later or for others.

## Frame

* **Treat a story or bug report in the request as already framed:** ask only what it leaves open.
* **Grill a vague request,** one whose readings lead to materially different work: who it is for and the job they are trying to get done, why, and the constraints, each question with a concrete case. A question that hangs on an open answer waits a round.
* **Pin each overloaded term to one meaning** (ubiquitous language), checked against the project's glossary and the code: does "account" mean the customer or the user; is "the table" a table, or a view with a row per item per night?
* **Say where the request, the code and its docs disagree.** Between code and docs, trust the code.
* **Probe the edge cases:** none, one and many; duplicates, order, ties and what counts as equal (case, rounding, time zone); a second or missed run; one bad item in a batch; the format each side of a boundary expects; empty, huge and malformed input; untrusted input; what expires, leaks or costs money unattended; what the person sees and what is saved when another system fails; a person not allowed to act.
* **Find the walking skeleton:** the thinnest version that runs end to end where it will really run. Each part of it the request leaves open, such as where it runs, what triggers it, where its data lives or how it signs in, is a question, and the first slice.
* **Mark each answer** about an unfamiliar library or API `doc`, with the link, or `memory`.
* **Spike first** when an unknown that questions and docs cannot settle could change the plan: load the spike skill.

## How a story fails

Check the request, and any story you are given or write, for these. Each one found is a question for the person, or a gap you fill with its reason.

* **A solution, not a problem** (XY problem): "add a Redis cache" where the need is "exports show data more than 15 minutes old". Ask why.
* **"As a user":** a role that hides who it is for and the job they are trying to get done.
* **No "so that", or one you wrote:** the why is the person's.
* **A silent assumption:** a gap you filled and wrote as a decision or a won't-do instead of asking.
* **Several asks joined by "and":** each is its own vertical slice.
* **A layer, not a vertical slice:** no page, route or command where a person or test meets the change.
* **Vague words** such as fast, easy, robust or "handles errors": each needs a number or a stated result.
* **The story sentence without rules:** the rules and their examples carry the build, not the sentence.
* **A Given reachable several ways, or a Then that states part of the result:** tests built on it pass and miss the rule.
* **Design in the story:** files, tables or layout before the rules are agreed. How is the build's job.
* **Too big:** several features, more than about 400 changed lines or 5 criteria, or nobody can size it. Split it into vertical slices by [references/split.md](references/split.md).
* **Conflicts:** a rule another story also states, or one main already meets.

## Acceptance criteria

The person writes the criteria. Critique them against these rules and fill the gaps.

* **One per business rule,** in the product's words, measurable: not "is fast" but "under 200 ms at 1,000 rows".
* **A Given/When/Then example in real values.** The Given says how its state came about, the When is one action, and the Then states every result the rule decides. A rule with several cases gets a table, one row per case.
* **A check someone can run or watch.** When the change reads real data or calls another system, one check runs on real input, read-only or as a dry run.
* **Follow the person's rule,** not what the code does today.
* **Add a criterion with its reason,** why you think it is needed, and keep it only once the person agrees.
* **Mark an open question `unknown`.**
* **No new rule** (a rename, refactor, dependency bump or config value): no story and no criteria, one `Done when:` line, such as the existing tests unchanged and green. Before a refactor, add characterization tests where the tests miss the moved code.

## Play back and hand off

* **Play back** the goal, the criteria and what this change will not do. End the play-back by asking whether to build it now or write it down for later. "I want to build X" says what the person wants, not when.
* **Offer up to 3 parts to explore,** new to this codebase or to the person, each with the question that matters for this task. None when there is no new rule.
* **Built now:** the story stays in the conversation, with no file. Load the building skill.
* **For later or for others:** write it down by [references/write.md](references/write.md).
* **Critique a story someone wrote** by [references/write.md](references/write.md).
* **How long will it take:** [references/forecast.md](references/forecast.md).
