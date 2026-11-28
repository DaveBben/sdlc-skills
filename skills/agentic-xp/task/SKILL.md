---
name: task
description: "Use first, before editing any file, for a change to code, configuration, dependencies or tooling whose done one simple check can prove, user-facing or not, however small or casually phrased: a fix, a retry, a new column, a changed colour, limit, flag or format, a refactor, a rename, a dependency bump, CI or dev-tool setup, like 'retry the database connection when it times out', 'make the submit button blue', 'the LED blinks twice too fast', 'bump the Terraform AWS provider', 'rename total to order_total everywhere'. Not for a feature that needs a written specification first, such as a new export or a new page, nor for reviewing a finished change, a question about code, a throwaway experiment, which is the spike skill's, or code the person wants to write themselves, which is the pair-program skill's. Holds a done check back from the subagent that writes the code, and commits to a branch, or logs the task for later."
license: MIT
metadata:
  version: "10.1.0"
---
# Task

A task is a change whose done one deterministic check proves. The check is a held-out test: the subagent that writes the code never sees it, so it cannot pass by special-casing the check or editing it.

When the check already exists, such as a story's hidden tests for one slice, start at Hand off in the slice's worktree, and leave the check hidden: the story moves its tests into the repository once every slice is in.

## Clarify

* **Ask at most one question,** only when the request reads two ways and the answer changes the code, such as a fixed retry or exponential backoff. Skip it when the request, the code or the conversation already answers it.
* **Ask for the done check** when the person gave none: a check, or a set of them, that deterministically proves the task is done. Offer the one you would pick.
* **Ask whether to log the task in the person's tracker to build later,** such as GitHub Issues, Jira or Gitea, when the request does not say whether to build it now. This question falls outside the one-question cap. A logged task holds the goal, the answer to the question and the done check, and nothing is built.

## Write the check

* **Work on a new branch in its own git worktree,** never in the person's checkout. Copy or link the untracked files the build needs, such as `.env`, `local.properties` or `node_modules`; where a fresh checkout is too costly to build, such as a game-engine project, or the repository is not in git, ask the person where to work.
* **Pick the form that best proves done:** a unit test, a script, a SQL query, a request to the running app, a plan or dry run such as `terraform plan`, a screenshot or screen recording of the UI, or a build deployed to the hardware with its serial output read back.
* **Have a script decide wherever one can,** such as the button's computed background colour in a headless browser, found by its role and label. Only where no script can judge it, `run` captures the screenshot or recording, exits 0 and says the result is judged outside, and you judge it each time the subagent returns.
* **Drive behaviour through a way in that exists,** such as a command, an endpoint or a function the app already calls, so the subagent names and places the code as it likes.
* **Where no way in exists, fix the interface yourself:** commit it to the worktree as a stub that compiles and does nothing, and name it in the hand-off, so the check fails on behaviour, not on a missing name.
* **Give the check its own copy of any state outside the worktree,** such as a scratch schema, a free port or its own emulator. Ask the person before a check flashes hardware or touches shared, live or paid resources.
* **Keep the check out of the worktree,** in `task-checks/<slug>/` under the repository's shared git directory (`git rev-parse --path-format=absolute --git-common-dir`). Give it an executable `run` that takes no arguments and has the worktree's absolute path written into it: the subagent may run only that bare command, with no arguments, pipes or `cd`.
* **Where the test runner finds tests only inside the project,** such as `cargo test`, `go test`, Gradle, Xcode, Jest or dbt, have `run` copy the worktree into one scratch directory it reuses, put the check in, run it there, and keep the build incremental.
* **Keep `run` to about a minute,** such as on a small fixture or a fixed seed with a tolerance.
* **Make each failure print why in terms of the goal,** such as `app exited 1 after 2.1s with OperationalError: timeout; it should survive 2 stalled connections`, and nothing of how the check works: run the runner with its source listing off, such as `pytest -q --tb=line`, or print each failing test's name and message from its JSON or JUnit report.
* **Find the mistake a capable developer would still make here,** the common or hidden one, such as a retry with no limit, and make the check fail it. A check that only a careless implementation fails proves little.
* **See it fail for the right reason:** the message names the missing behaviour, not an import, compile, setup or typo error. When the missing thing is itself the failure, such as a column that does not exist yet, a query that selects it is the whole check, and its "no such column" error is the right reason.

## Hand off

* **Launch a fresh subagent** with the goal as one sentence of behaviour, the interface when the check fixes one, the worktree it works in rather than one of its own, and the `run` command as its only way to the check, and tell it to write code a reviewer merges by [references/code.md](references/code.md). Where nothing hides the check, such as outside git, tell it never to read the check's directory.
* **Tell it to start from the simplest solution that could pass,** and to try a harder one only after a failure the message explains.
* **Tell it to keep the repository's existing checks green.**
* **Tell it to stop when it sees no path left,** returning each approach it tried and the message that ruled it out.

## Finish

* **Run the check and the repository's own checks yourself:** done is both passing.
* **Keep the check when it guards behaviour worth keeping,** such as the retry's unit tests, by moving it into the repository's tests; where the repository has no tests, ask whether to add it as a script or drop it. Drop a one-off, such as the column query, deleting its `task-checks/<slug>/`.
* **Commit the code and any kept check to the branch.** Report the check's command and result, and what it does not cover.
* **Bring a subagent that gave up to the person** with its approaches and their messages, and decide the next move with them.
