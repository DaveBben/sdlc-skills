---
name: story
description: "Use first for any request to add, change or remove what users see or the product does, however small, such as a UI tweak, a timing, a colour or a new field, for writing or judging user stories and acceptance criteria, and for what to build next, unless the person wants to pair or build together or an agreed story is being built or designed: agrees acceptance criteria with the person before any code is written."
license: MIT
metadata:
  version: "1.0.0"
---
# Story

A story is one thing a person can do once a change ships, with numbered acceptance criteria whose Given/When/Then examples in real values can be tested without asking anyone.

## Paths

* **Create** one: [references/create.md](references/create.md). More than one path, variation or outcome: split it first by [references/split.md](references/split.md).
* **Refine** an agreed story that is not built yet: [references/refine.md](references/refine.md).
* **Review** stories someone wrote: check each against INVEST by create.md's and split.md's rules, and for a duplicate story or an abuse case that no criterion states. Change nothing without its owner's yes to that finding, and report `<story>: <rule broken> — "<quoted text>" — <fix>`, then `Ready to build: <stories with no finding>`.
* **Subtasks** for an existing story: [references/subtasks.md](references/subtasks.md).
* **Next story:** list the ready ones in build order for the user to pick: with criteria, and no open question, blocker, pull request or subtask assigned to a person.
* **Build** an agreed story: the `build` skill.
* **Measure** a story with a `Measure:` line once its date passes: write the value and the date on `Result:`, say whether it met the target. A miss becomes new stories; a merged story never reopens. A result that contradicts a PRD goal or metric is a change to the PRD, by the `prd` skill.
* **Resume:** read the story with its comments; continue at the first step not done.

## Questions

* **A fact a tool can reach:** look it up.
* **Easy to reverse,** such as an example's illustrative amount or who the contacts are: decide it and list it as `Decided: <choice>, because <reason>`.
* **Everything else that shapes the story** is the user's: the need, what a person can and cannot do, the business rules and each expected result.
* **How to ask:** one decision per question, through the multiple-choice tool where there is one (Claude Code's AskUserQuestion), naming the story, the decision, what waits on it and whether it is easy to reverse.
* **Options as equals:** none marked recommended and none placed first because it is yours, except a proposed criterion, which is Accept, Reject or Modify by create.md. Once they answer, give your pick in one line when it differs. "I need to research this" is always the last option.

## Where stories live

* **With a tracker:** one issue per story, filed in build order through the `tracker` skill, in Todo once agreed.
* **Without one:** `docs/stories/<slug>.md` on its own branch until it is built; then the red commit's message and the pull request hold it.
