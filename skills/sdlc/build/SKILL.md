---
name: build
description: "Use first, before reading or editing code, for any change to code, however small: a feature, story or ticket, a bug or wrong output, a refactor, a new flag, or a chore such as a dependency bump or a runtime upgrade, like 'add a CSV export', 'implement the story in docs/stories/x.md', 'critique my acceptance criteria', 'the export crashes on an empty order list', 'rename total to order_total everywhere' or 'bump the requests dependency'. Agrees with the person what to build and why as testable Given/When/Then criteria, plans it and has the plan reviewed, writes failing tests first, has fresh agents implement and review, and takes it through the pull request to merge."
license: MIT
metadata:
  version: "3.2.0"
---
# Build

Work in a new worktree from main, on a branch named `<story|bug|refactor|chore>/<key>-<title-words>`. The key is the ticket's, else a short slug.

A change with one obvious result, such as a colour or a config value, skips these steps.

The test command is the `Check:` line in `AGENTS.md`, else the repository's own, such as `npm test` or `pytest`.

1. **Align** with the person on what you are building, why it is needed, and what it enables once done.
   * First tell them what in the code affects it, with `file:line`.
   * Offer an easier way if there is one. Reuse what the repository already has.
   * Ask in chat, a few questions at a time, scaled to the change. A ticket that already answers them is the answer.
   * You are aligned when you agree on two things:
     * **Acceptance criteria** a test can decide. Each is a rule with a Given/When/Then example in real values. Include the failure paths.
     * **`Done when:` lines** checked before the pull request. Each is a command that exits 0 only when its result holds, on real data or the running app where it can. It writes nothing live. A result only an eye can judge is written `Done when (checked by you):`.
   * Every number or rule in them is the person's.
   * A request that already names the result and every value needs no examples. Its `Done when:` lines are enough.
   * Write them to `docs/acceptance/<key>.md`, as [references/criteria.md](references/criteria.md) shows.
2. **Review the criteria** for the failure modes in [references/criteria.md](references/criteria.md).
   * If you drafted any of them, a fresh subagent reviews them, given the criteria, the worktree and that file.
   * Fix wording slips yourself. Show the person the rest.
   * Asked only for a critique, stop here.
3. **Hard-to-reverse decisions** go to the person, the options as equals: data stored or sent, a contract others call, a new dependency, auth, how it deploys, how the parts are split.
4. **Plan** by [references/design-spec.md](references/design-spec.md). Skip it when there is one obvious approach. A hard-to-reverse decision the plan raises goes to the person, as in step 3.
5. **Review the plan** by a fresh subagent, given the plan, the criteria and the worktree. Fix what blocks.
6. **Write the failing tests first,** from the acceptance criteria, by [references/tests.md](references/tests.md). One test per example.
   * See each one fail for the right reason.
   * Name each test after its criterion, such as `test_ac3_<what>`.
   * Commit them alone with the acceptance file, the message starting `test(red):`.
   * If a criterion changes later, review it again (step 2) and commit its new failing tests before any code.
7. **Implement** by a fresh subagent, given the worktree, the red commit, the criteria, the test command, and the paths of the tests and refactor references.
   * Trust `git log` and the test command's output over what it reports.
   * Change a test only when its criterion shows the test is wrong, in a new `test(red):` commit.
   * If `AGENTS.md` has a `Mutation:` line, run it on the changed files. Add a test for each surviving mutant, in a `test:` commit.
8. **Review the implementation** by fresh subagents.
   * In a new `<temp>/review-<timestamp>/` folder, put `diff.patch` (the diff against main) and `story.md` (the criteria, plus each test changed after it was first committed, and why).
   * One subagent reviews it. Another verifies the findings.
   * Tell the person each kept finding in one line. Fix each blocking one test-first.
9. **Pull request** into main, titled `[<key>] <what it does>`, body by [references/pull-request.md](references/pull-request.md).
   * First run each `Done when:` command and the test command; all must pass. Fix what fails, test-first, never the criterion or the command. List the `Done when (checked by you):` lines in the pull request.
   * Watch CI and review comments until it merges. Fix what fails, reply to each comment.
   * After merge, remove the worktree and the branch.

## Bugs, refactors and chores

* **Bug:** reproduce it first. The reproduction is the first criterion, and running it again is its `Done when:`.
  * Can't reproduce it: ask for the missing fact and stop.
  * Losing or exposing data, or blocking every user: first tell the person how to stop the harm, such as a revert.
  * Behaviour nobody built is a feature. Say so and align on it as one.
  * Asked only why it happens: explain, show the reproduction, and offer the fix.
* **Refactor:** every existing test passes unchanged. Follow [references/refactor.md](references/refactor.md), then go to step 8.
* **Chore,** such as a dependency bump: `Done when:` the tests pass on the new version. Make the change, then go to step 8.

## When to stop

* Wait for the person at steps 1, 2 and 3.
* Anywhere else, stop only for a number or rule a criterion needs, code that contradicts a criterion, or a fact only the person has.
* Otherwise pick, write `Decided: <choice>, because <reason>`, and keep going. These go in the pull request.
* With no person in the session, ask on the issue or the pull request and keep going on what doesn't depend on the answer. Then stop and say what waits.
