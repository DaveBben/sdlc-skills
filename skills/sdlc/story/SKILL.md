---
name: story
description: "Use first when work is to be written down or cut up for later or for other people instead of built now: writing a user story or its acceptance criteria, reviewing or critiquing a story someone wrote, splitting an epic, a PRD or a large feature into stories, or forecasting when a set of stories will be finished, such as 'write a story for X', 'critique the story in docs/stories/x.md', 'break this PRD into stories', 'this is too big for one merge request, cut it down' or 'how many weeks for the remaining stories'. Not for building a story: that is the build skill's. A story is a short frame written ahead of the build for one vertical slice that fits one merge request: why, scope, and one acceptance criterion per business rule, each with a worked example and a check someone can run."
license: MIT
metadata:
  version: "5.0.0"
---
# Story

A story is the loop's Frame step written ahead of the build, for another person or a later session: one thing a person can do once it merges, small enough for one merge request. It points at a conversation and is not a spec; the design stays in the talk and the repository.

Work that fits a sentence and one merge request, and is built now, needs no story: say so in one line. A story earns its cost when work must be split, estimated, handed over or kept as a record. A defect is the `bug` skill's report; an unknown that blocks sizing is a `spike`.

## Write one

Frame it by the frame skill, at the business level: its grilling, gaps and criteria format, in the product's words. Leave file paths, data shapes and design to the build, where they are current; read the code only for what is already built or decided that shapes the story, one line each with `file:line`.

```markdown
# <what a person can do once this merges: an outcome, not a task>

Why: <who hits this, what they do today, why now; 1 or 2 sentences>

## Acceptance criteria

1. <one business rule>
   Example: a cart of 3 items at 10.00 with code SAVE10 totals 27.00.
   Check: <the command or test that will show it, or `by eye: <what to look at>`>

## Out of scope

- <what a reader would expect here and this story will not do>

## Dependencies

- <who must review, sign off or supply data, and the expected wait; or the story this waits on, with the reason>

## Open questions

- <one per line, with who can answer it>

Reach: <the page, route or command where a person or test meets the new behaviour>
Hint: <files or APIs to start from; optional, never a design>
```

* **Size:** INVEST, where small means one merge request a reviewer reads in one sitting, about 400 changed lines, and a few days of work at most. More than about 5 criteria is usually two stories. When nobody can name an upper bound, split it by [references/split.md](references/split.md).

## Review one

For a story someone wrote, or one waiting in a backlog before it is picked up. Change nothing without its owner's yes. Report `<story>: <rule broken> — "<quoted text>" — <fix>` per finding, then `Ready: <stories with no finding>`. Besides the frame skill's criteria rules and the size rule above:

* **Frame-ready:** could a build start from this without asking anything? Name each missing piece: goal, why, scope, done-check.
* **Reach:** after it merges, where does a person or test meet the new behaviour? With no entry point it is a layer, not a vertical slice.
* **Another team** is needed and no dependency line says who and how long.
* **A rule another story also states** goes to one of them.
* **Stale:** a criterion main already meets is deleted, naming the code or test; an example whose starting state main can no longer reach is rewritten.
* **Open or merged** merge request: leave the story alone; a change now is a question for that build.
* **A story you drafted in this session** goes to a fresh subagent given only the story and this file: your own read shares the draft's blind spots.

## Where it lives, where it goes

* **Lives** in the team's tracker when a tool here reaches it, one issue per story, its status moving with the work; else `docs/stories/<slug>.md`. File only what the person approved.
* **To build:** the story is the frame. A build that starts from one asks only about what the story leaves missing or ambiguous; the criteria are its done-check, each ticked by seeing its `Check:` run; and the criteria in the story's words and numbering, with `Out of scope` as what was left out, are the review's `story.md`. One story, one merge request.
* **After the merge** it is a record: never edited. A miss or a change of mind is a new story.
* **How long will it take:** [references/forecast.md](references/forecast.md).
