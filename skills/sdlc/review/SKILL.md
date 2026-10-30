---
name: review
description: "Use for any request to review, critique, sanity-check or find bugs or security problems in code, a file, a module, a diff, uncommitted changes, a commit, or a pull or merge request: fresh agents check it against one checklist and a verifier keeps only the findings it can prove."
license: MIT
metadata:
  version: "1.0.0"
---
# Review code

Review one change with fresh agents, keep only the findings a verifier proves, and give a person a reading list. When the subject is unclear, ask once. Write code only when the user asks.

## Prepare

Make a review directory, `<temp>/review-<timestamp>/` in the OS temporary directory, and write into it:

* **`diff.patch`:** by `git -c core.quotePath=false diff --no-color --no-ext-diff --src-prefix=a/ --dst-prefix=b/`, with `<merge target>...<head>` for a branch, `<commit>^ <commit>` for a commit, `HEAD <snapshot>` for uncommitted code, or the empty tree and `HEAD -- <paths>` for a file or module. For a branch a calling skill built, use `<merge target>...<snapshot>`, the snapshot taken of its worktree. Check a merge request or another branch out detached in a worktree under the review directory, and run its install step there.
* **`story.md`:** what the change is for and its acceptance criteria: the ticket a calling skill gives, a merge request's description and linked ticket, or what the user says it is for.
* **`design.md`:** the design a calling skill gives, or a merge request's stated approach. Only the router reads it.
* **`mutants.txt`:** the surviving and no-coverage mutants on changed lines, from a calling skill, else one run of the check command, else of a mutation tool on the changed lines. Empty when none survived; absent when none could run.
* **`locked.txt`:** the locked-tests check's lines a calling skill gives.
* **`floor.txt`:** `python3 scripts/reading_floor.py diff.patch <the tree's AGENTS.md> base-agents.md`, where `base-agents.md` is `git show <merge target>:AGENTS.md`.

```sh
# snapshot of uncommitted code, untracked files included: prints the commit hash
i=$(mktemp -u); GIT_INDEX_FILE=$i git add -A && GIT_INDEX_FILE=$i git commit-tree $(GIT_INDEX_FILE=$i git write-tree) -p HEAD -m snapshot; rm -f $i
```

The check command is the one a calling skill gives, else the `Full check:` or `Check:` line of `AGENTS.md`, else what CI runs.

## Review

Run each step below but the merge in a fresh subagent, given only the paths and values listed, never this conversation.

1. **Route the change,** before any reviewer, into a review tier and the person's reading list: the review directory, the tree, `diff.patch` and `story.md`. The author never grades its own risk. Drop none of its `reading-list.md`. For a file or module, the tier is `full-read` and the list is the file.
2. **Review it against the checklist:** one reviewer for a short read, else three at once. Give each its number, its order of the sections of [references/checklist.md](references/checklist.md) (`1,2,3,4,5,6,7,8,9`, `9,8,7,6,5,4,3,2,1`, `7,8,9,1,6,2,5,3,4`), the tree, `diff.patch`, `story.md`, the review directory, the checklist's path, the merge target and the red commits.
3. **Merge** their `findings-<n>.md` into `findings.md`: rows naming the same line and wrong result become one; keep every other row; number them.
4. **Verify the findings:** `findings.md`, the tree, `diff.patch`, `story.md`, the checklist's path and the check command.

## Report

After the report, remove the review directory and its worktrees.

* **To an agent:**

  ```text
  verdict: no-blocking-findings | blocking=<n>
  rows: <found> found, <merged> merged, <kept> kept
  tier: short-read | full-read | split lines=<n>
  <each reading-list item>
  id|severity|section|type|location|trigger|wrong|fix|proof
  <each kept row>
  ```

* **To a person,** or on a merge request: by [references/person.md](references/person.md).
