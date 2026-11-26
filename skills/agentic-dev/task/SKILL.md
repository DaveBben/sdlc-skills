---
name: task
description: "Use first, before editing any file, for a change to code, configuration, dependencies or tooling whose done one simple check can prove, user-facing or not, however small or casually phrased: a fix, a retry, a new column, a changed colour, limit, flag or format, a refactor, a rename, a dependency bump, CI or dev-tool setup, like 'retry the database connection when it times out', 'make the submit button blue', 'add a created_at column to orders', 'the export crashes on an empty order list, fix it', 'rename total to order_total everywhere'. Not for a feature that needs a written specification first, such as a new export or a new page, nor for reviewing a finished change, a question about code, or a throwaway experiment, which is the prototyping skill's. Asks at most one clarifying question and for a done check, writes the check where the agent doing the work cannot see it and sees it fail, has a subagent make it pass from the simplest solution up, and commits to a branch; or logs the task in the person's tracker to build later."
license: MIT
metadata:
  version: "10.0.0"
---
# Task

A task is a change whose done one deterministic check proves. The check is a held-out test: the subagent that writes the code never sees it, so it cannot pass by special-casing the check or editing it.

When the check already exists, such as a story's hidden tests for one slice, start at Hand off.

## Clarify

* **Ask at most one question,** only when the request reads two ways and the answer changes the code, such as a fixed retry or exponential backoff. Skip it when the request, the code or the conversation already answers it.
* **Ask for the done check** when the person gave none: a check, or a set of them, that deterministically proves the task is done. Offer the one you would pick.
* **Ask whether to log the task in the person's tracker to build later,** such as GitHub Issues, Jira or Gitea, when they did not say to build it now. This question falls outside the one-question cap. A logged task holds the goal, the answer to the question and the done check, and nothing is built.

## Write the check

* **Work on a new branch in its own git worktree,** never in the person's checkout.
* **Pick the form that best proves done:** a unit test, a script, a SQL query, a request to the running app, a screenshot or screen recording of the UI, or a build deployed to the hardware with its serial output read back.
* **Have a script decide wherever one can,** such as the pixel colour where the button is drawn. Only where no script can judge it, `run` captures the screenshot or recording and you judge it each time the subagent returns.
* **Drive behaviour through a way in that exists,** such as a command, an endpoint or a function the app already calls, so the subagent names and places the code as it likes. Where none exists, the check fixes the interface, and the hand-off names it.
* **Keep it out of the worktree,** in `task-checks/<slug>/` under the repository's shared git directory (`git rev-parse --path-format=absolute --git-common-dir`), with an executable `run` that runs it against the worktree.
* **Make each failure print why in terms of the goal,** such as `app exited 1 after 2.1s with OperationalError: timeout; it should survive 2 stalled connections`, and nothing of how the check works: run a test runner with its source listing off, such as `pytest -q --tb=line`.
* **Name the mistake a capable developer would still make here,** the common or hidden one, such as a retry with no limit, and make the check fail it. A check that only a careless implementation fails proves little.
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
