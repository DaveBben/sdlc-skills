# Writing a story down, and critiquing one

## Write one

Write at the business level. Read the code only for what is already built or decided that shapes the story, and tell the person each in one line with `file:line`; keep paths out of the story.

```markdown
# <what a person can do once this merges: an outcome, not a task>

Why: <who hits this, what they do today, why now; 1 or 2 sentences>

## Context

<2 or 3 sentences for a reader outside the team: this part of the product today, and related work or decisions>

## Acceptance criteria

1. <one business rule>
   Given a key that made 99 requests in the last minute, through the public API
   When it makes one more
   Then the request succeeds and the response says 0 remain
   Check: <the command or test that will show it, or `by eye: <what to look at>`>

UAT: <how the person sees the story work on the live system: the credentials, services and data it uses, and read-only, dry run or a write they approve>

## Out of scope

- <what a reader would expect here and this story will not do>

## Dependencies

- <who must review, sign off or supply data, and the wait; the story this waits on; or a spike that blocks it>

## Open questions

- <one per line, with who can answer it>

Reach: <the page, route or command where a person or test meets the new behaviour>
Hint: <files or APIs to start from; optional, never a design>
```

## Critique one

Change nothing without its owner's yes. Report `<story>: <rule broken> — "<quoted text>" — <fix>` per finding, then `Ready: <stories with no finding>`. Check SKILL.md's "How a story fails" and its acceptance criteria rules, and these:

* **Ready:** name each missing goal, why, scope or check.
* **Dependencies:** name each other team it needs that no dependency line covers with who and how long.
* **Stale:** delete a criterion main already meets, naming the code or test; rewrite an example whose starting state main can no longer reach.
* **In flight:** leave a story with an open or merged merge request alone; a change now is a question for whoever is building it.

## Where it lives

* **Lives** in the team's tracker when a tool here reaches it, filed by the tracker skill; else `docs/stories/<NN>-<slug>.md`, numbered in build order, a blocker named in `Dependencies`. File only what the person approved.
* **After the merge** it is a record, never edited. A miss or a change of mind is a new story.
