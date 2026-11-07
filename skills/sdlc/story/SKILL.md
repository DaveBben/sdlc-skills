---
name: story
description: "Use first for any request to add, change or remove what users see or the product does, such as a new field, rule or flow, for writing or judging user stories and acceptance criteria, and for what to build next, unless the person wants to pair or build together, an agreed story is being built or designed, or the person is still finding out what to build: agrees acceptance criteria with the person before any code is written."
license: MIT
metadata:
  version: "1.0.0"
---
# Story

A story is one thing a person can do once a change ships, with 3 to 5 numbered acceptance criteria the user writes, each with an examples table in real values.

## Paths

* **Create:** [references/create.md](references/create.md); too big for one reviewable pull request, split it first by [references/split.md](references/split.md).
* **Refine** an agreed story not built yet: [references/refine.md](references/refine.md).
* **Review** stories someone wrote against INVEST by create.md and split.md, and for a duplicate story or an abuse case no criterion states. Change nothing without its owner's yes, and report `<story>: <rule broken> — "<quoted text>" — <fix>`, then `Ready to build: <stories with no finding>`.
* **Subtasks:** [references/subtasks.md](references/subtasks.md).
* **Next story:** list the ready ones, the first as your pick: with a tracker, by the `tracker` skill's Next story; without one, in build order, each with criteria and no open question, blocker, pull request or subtask assigned to a person.
* **Measure** a story's `Measure:` line once its date passes: write the value and date on `Result:` and whether it met the target. A miss becomes new stories; a merged story never reopens. A result that contradicts a PRD goal is a change to the PRD, by the `prd` skill.

## Questions

* **Easy to reverse,** such as who the contacts are: decide it as `Decided: <choice>, because <reason>`.
* **Everything else that shapes the story** is the user's to write: the need, what a person can and cannot do, the business rules and each expected result. A concern about one they wrote is a critique, never a question.
* **Ask** only what their words leave open, once, all of it in one message, each multiple-choice with "I need to research this" last. Lead with your pick; for a one-way door, such as stored data or a contract others call, give the options as equals and your pick after they answer.

## Where stories live

* **With a tracker:** one issue per story, filed in build order by the `tracker` skill, in Todo once agreed.
* **Without one:** `docs/stories/<slug>.md` on its own branch until it is built; then the red commit's message and the pull request hold it.
