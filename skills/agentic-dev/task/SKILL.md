---
name: task
description: "Use first, before editing any file, for a change to code, configuration, dependencies or tooling whose done one simple check can prove, user-facing or not, however small or casually phrased: a fix, a retry, a new column, a changed colour, limit, flag or format, a refactor, a rename, a dependency bump, CI or dev-tool setup, like 'retry the database connection when it times out', 'make the submit button blue', 'add a created_at column to orders', 'the export crashes on an empty order list, fix it', 'rename total to order_total everywhere'. Not for a feature that needs a written specification first, such as a new export or a new page, nor for reviewing a finished change, a question about code, or a throwaway experiment, which is the prototyping skill's. Asks at most one clarifying question and for a done check, writes the check where the agent doing the work cannot see it and sees it fail, has a subagent make it pass from the simplest solution up, and commits to a branch; or writes the task down when asked."
license: MIT
metadata:
  version: "10.0.0"
---
# Task

A task is a change whose done one deterministic check proves. The check is a held-out test: the subagent that writes the code never sees it, so it cannot pass by special-casing the check or editing it.

## Clarify

* **Ask at most one question,** only when the request reads two ways and the answer changes the code, such as a fixed retry or exponential backoff. Skip it when the request, the code or the conversation already answers it. Never ask why.
* **Ask for the done check** when the person gave none: a check, or a set of them, that deterministically proves the task is done. Offer the one you would pick.
* **Write the task down instead of building it** when the person asks: the goal, the answer to the question and the done check, in the file or issue they name.

## Write the check

* **Work on a new branch in its own git worktree,** never in the person's checkout.
* **Pick the form that best proves done:** a unit test, a script, a SQL query or a request to the running app. Drive behaviour through a way in that exists, such as a command, an endpoint or a function the app already calls, so the subagent names and places the code as it likes. Where none exists, the check fixes the interface, and the hand-off names it.
* **Keep it out of the worktree,** in `task-checks/<slug>/` under the repository's shared git directory (`git rev-parse --path-format=absolute --git-common-dir`), with an executable `run` that runs it against the worktree.
* **Make each failure print why in terms of the goal,** such as `app exited 1 after 2.1s with OperationalError: timeout; it should survive 2 stalled connections`, and nothing of how the check works: run a test runner with its source listing off, such as `pytest -q --tb=line`.
* **Name a wrong implementation the check fails,** such as a retry with no limit. When you cannot, the check proves nothing; change it.
* **See it fail for the right reason:** the message names the missing behaviour, not an import, setup or typo error. Where the condition fails today, such as a column that does not exist, the check is the command that succeeds once it does, here a query that selects the column.

## Hand off

* **Launch a fresh subagent** with the goal as one sentence of behaviour, the interface when the check fixes one, the worktree, and the `run` command as its only way to the check.
* **Tell it to start from the simplest solution that could pass,** and to try a harder one only after a failure the message explains.
* **Tell it to keep the repository's existing checks green.**
* **Tell it to stop when it sees no path left,** returning each approach it tried and the message that ruled it out.

## Finish

* **Run the check and the repository's own checks yourself:** done is both passing.
* **Keep the check when it guards behaviour worth keeping,** such as the retry's unit tests, by moving it into the repository's tests. Drop a one-off, such as the column query.
* **Commit the code and any kept check to the branch.** Report the check's command and result, and what it does not cover.
* **Bring a subagent that gave up to the person** with its approaches and their messages, and decide the next move with them.
