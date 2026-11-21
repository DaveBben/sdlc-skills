---
name: story
description: "Use first when work is to be written down or cut up for later or for other people instead of built now: writing a user story, a chore or a ticket, or writing work up for someone else to pick up, or its acceptance criteria, reviewing or critiquing a story someone wrote, splitting an epic, a PRD or a large feature into stories, or forecasting when a set of stories will be finished, such as 'write a story for X', 'critique the story in docs/stories/x.md', 'break this PRD into stories', 'this is too big for one merge request, cut it down' or 'how many weeks for the remaining stories'. Not for building a story: that is the building skill's. A story is a short frame written ahead of the build for one vertical slice that fits one merge request: why, scope, and one acceptance criterion per business rule, each with a worked example and a check someone can run."
license: MIT
metadata:
  version: "5.0.0"
---
# Story

A story is the loop's Frame step written ahead of the build, for another person or a later session: one thing a person can do once it merges, small enough for one merge request. It is a placeholder for a conversation, not a spec.

Work that fits a sentence and one merge request, and is built now, needs no story: say so in one line. A defect is the `bug` skill's report; an unknown that blocks sizing is a `spike`.

## Write one

Frame it by the framing skill, at the business level: its grilling, gaps and criteria format, in the product's words. Leave file paths, data shapes and design to the build; read the code only for what is already built or decided that shapes the story, one line each with `file:line`.

```markdown
# <what a person can do once this merges: an outcome, not a task>

Why: <who hits this, what they do today, why now; 1 or 2 sentences>

## Context

<2 or 3 short sentences for a reader outside the team: the part of the product this touches, how it works today, and any related work or decision; in the product's words, no file paths>

## Acceptance criteria

1. <one business rule>
   Given a cart of 3 items at 10.00, added through the product page
   When the shopper applies code SAVE10
   Then the total shows 27.00 and the order summary lists SAVE10 −3.00
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

Change nothing without its owner's yes. Report `<story>: <rule broken> — "<quoted text>" — <fix>` per finding, then `Ready: <stories with no finding>`. Besides the framing skill's criteria rules and the size rule above:

* **Frame-ready:** could a build start from this without asking anything? Name each missing piece: goal, why, scope, done-check.
* **Reach:** with no entry point where a person or test meets the new behaviour, it is a layer, not a vertical slice.
* **Another team** is needed and no dependency line says who and how long.
* **A rule another story also states** goes to one of them.
* **Stale:** a criterion main already meets is deleted, naming the code or test; an example whose starting state main can no longer reach is rewritten.
* **Open or merged** merge request: leave the story alone; a change now is a question for that build.
* **A story you drafted in this session** goes to a fresh subagent given only the story and this file.

## Where it lives, where it goes

* **Lives** in the team's tracker when a tool here reaches it, one issue per story, its status moving with the work; else `docs/stories/<slug>.md`. File only what the person approved.
* **To build:** one story, one merge request. The story is the build's frame; its criteria are the done-check, each ticked by seeing its `Check:` run, and, in the story's words and numbering with `Out of scope` as what was left out, the review's `story.md`.
* **After the merge** it is a record, never edited. A miss or a change of mind is a new story.
* **How long will it take:** [references/forecast.md](references/forecast.md).
