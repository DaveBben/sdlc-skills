---
name: story
description: "Use first when work is to be written down or cut up for later or for other people instead of built now: writing a user story, a chore or a ticket, or writing work up for someone else to pick up, or its acceptance criteria, reviewing or critiquing a story someone wrote, splitting an epic, a PRD or a large feature into stories, or forecasting when a set of stories will be finished, such as 'write a story for X', 'critique the story in docs/stories/x.md', 'break this PRD into stories', 'this is too big for one merge request, cut it down' or 'how many weeks for the remaining stories'. Not for building a story: that is the building skill's. A story is a short frame written ahead of the build for one vertical slice that fits one merge request: why, scope, and one acceptance criterion per business rule, each with a worked example and a check someone can run."
license: MIT
metadata:
  version: "5.1.0"
---
# Story

* **Write no story** for work that fits a sentence and one merge request and is built now: say so in one line.
* **Send a defect** to the `bug` skill, and an unknown that blocks sizing to the `spike` skill.

## Write one

Frame it with the framing skill's grilling, edge cases and acceptance criteria, at the business level. Read the code only for what is already built or decided that shapes the story, and tell the person each in one line with `file:line`.

```markdown
# <what a person can do once this merges: an outcome, not a task>

Why: <who hits this, what they do today, why now; 1 or 2 sentences>

## Context

<2 or 3 sentences for a reader outside the team: this part of the product today, and related work or decisions>

## Acceptance criteria

1. <one business rule>
   Given a cart of 3 items at 10.00, added through the product page
   When the shopper applies code SAVE10
   Then the total shows 27.00 and the order summary lists SAVE10 −3.00
   Check: <the command or test that will show it, or `by eye: <what to look at>`>

## Out of scope

- <what a reader would expect here and this story will not do>

## Dependencies

- <who must review, sign off or supply data, and the wait; or the story this waits on>

## Open questions

- <one per line, with who can answer it>

Reach: <the page, route or command where a person or test meets the new behaviour>
Hint: <files or APIs to start from; optional, never a design>
```

* **Size it by INVEST,** where small means about 400 changed lines and a few days of work at most. More than about 5 criteria is usually two stories. Split a bigger story, or one nobody can size, by [references/split.md](references/split.md).

## Review one

Change nothing without its owner's yes. Report `<story>: <rule broken> — "<quoted text>" — <fix>` per finding, then `Ready: <stories with no finding>`. Check the framing skill's acceptance criteria rules, the size rule above, and these:

* **Ready to build:** name each missing goal, why, scope or done-check.
* **Reach:** a story with no entry point where a person or test meets the new behaviour is a layer, not a vertical slice.
* **Dependencies:** name each other team it needs that no dependency line covers with who and how long.
* **Duplicate rule:** a rule another story also states goes to one of them.
* **Stale:** delete a criterion main already meets, naming the code or test; rewrite an example whose starting state main can no longer reach.
* **In flight:** leave a story with an open or merged merge request alone; a change now is a question for that build.

## Where it lives, where it goes

* **Lives** in the team's tracker when a tool here reaches it, one issue per story; else `docs/stories/<slug>.md`. File only what the person approved.
* **To build:** one story, one merge request. Its criteria are the build's done-check, each ticked by seeing its `Check:` run. They and its `Out of scope` go into the review's `story.md` in the story's words and numbering.
* **After the merge** it is a record, never edited. A miss or a change of mind is a new story.
* **How long will it take:** [references/forecast.md](references/forecast.md).
