---
name: build
description: "Use first, before reading or editing code, whenever a change is to be built and shipped: a story or ticket to implement, a feature request with no story, a new flag or option, or a chore such as a dependency bump or a runtime upgrade, like 'implement the story in docs/stories/x.md', 'add a CSV export', 'add a --dry-run flag', 'bump the requests dependency' or 'just build X'. Agrees the acceptance criteria and the done check, writes an implementation design spec and has it reviewed, writes failing tests first and has them attacked, locks them, has fresh agents implement and review, opens a pull request, watches CI and comments, and runs a retro after merge."
license: MIT
metadata:
  version: "3.1.0"
---
# Build

Work in a worktree from main on branch `<story|bug|chore>/<key>-<title-words>`. A change with one obvious result and no trade-off, such as a colour or a config value, needs none of this: make it and let the check run.

1. **Criteria:** the story's or the ticket's. Without a story, agree at least one criterion with the person here, each with an example in real values; a request that states the change in full gives its items as `Done when:` lines.
2. **Done check:** the story's `Done check:`. Without one, agree with the person here: one command or observation that shows each criterion holds, ideally against real data or the running app, writing nothing live.
3. **Implementation design spec,** skipped for a trivial change, such as one file with an obvious approach: write how the change will be built, by [references/design-spec.md](references/design-spec.md); a plan the person brings is the spec. Have a fresh subagent review it, given only the spec, the criteria and the worktree. Fix each blocking finding in the spec, and ask the person about each one-way door it names, the options as equals.
4. **Failing tests first,** from each criterion's examples, by [references/tests.md](references/tests.md). A rule over a range or an invariant also gets a property test where the repository has a property-testing library.
5. **Challenge the tests:** have a fresh subagent challenge the tests blind, given the criteria, the worktree, the red commit, the tests reference's path and an empty holdout directory, `~/.sdlc-holdout/<repository>/<branch>/`. Fix each `Weak:` test, a change to a locked test only with the person's yes. Settle each `Disagrees:` line the criterion's words decide; ask only one both readings fit, your pick first.
6. **Lock the tests:** commit them alone, the message starting `test(red):`. Each committed test is locked: change a line of one, or add a line that switches tests off, only with the person's yes. A locked test you think is wrong is a question, never a workaround.
7. **Implement** by a fresh subagent, one launch at a time, given the worktree, the red commits and their tests, the criteria, the `Decided:` lines and the done check, never the holdout directory. Trust `git log` and the check over its return. Once the suite passes, copy the holdout files in at the same paths, commit them alone as a red commit, and run them; on a failure, fix the code, never the held-back test. Where `AGENTS.md` has a `Mutation:` line, run it on the changed files and add a test for each surviving mutant in a changed line. Then run the done check.
8. **Review:** make a review directory, `<temp>/review-<timestamp>/`, holding `diff.patch`, the diff against the merge target, and `story.md` (the ticket, its criteria and each locked-test change the person said yes to). Have one fresh subagent review it, given only the review directory, the worktree and the merge target, then another verify its findings, given only its `findings.md`, the worktree, `diff.patch`, `story.md` and the done check. Tell the person each kept finding in one line, naming the idea, and fix each blocking one test-first.
9. **Pull request** into main, titled `[<key>] <what it does, imperative>`, body by [references/pull-request.md](references/pull-request.md). Past about 400 changed lines, split it by criterion.
10. **Monitor** CI and review comments until it merges. Fix each failure and each comment you agree with test-first, reply to each comment, and rewrite the body against the new diff.
11. **After merge:** remove the worktree, the branch and its holdout directory, then a retro, each answer citing its evidence: what you assumed wrongly, what the person had to correct or supply, what cost the most time, and which check would have caught it.

Record each choice you make alone as `Decided: <choice>, because <reason>`. With no person in the session, ask on the ticket's issue or the pull request, say what waits on the answer, and stop.
