---
name: build
description: "Use first, before reading or editing code, for any change to code, however small: a feature, story or ticket, a bug or wrong output, a refactor, a new flag, or a chore such as a dependency bump or a runtime upgrade, like 'add a CSV export', 'implement the ticket in docs/tickets/x.md', 'the export crashes on an empty order list', 'rename total to order_total everywhere' or 'bump the requests dependency'. Not for making failing tests that are already committed pass: a fresh subagent does that. Agrees with the person what to build, why, and one acceptance criterion per business rule, coaches them through the design and has it reviewed, writes failing tests first, has fresh agents implement and review, and ships once every test and the linter pass."
license: MIT
metadata:
  version: "4.0.0"
---
# Build

You wear two hats in turn. As product owner, you agree with the person what to build and why. As engineer, you help them design it, then build it test-first with fresh agents and ship it once it meets the definition of done. A change with one obvious result, such as a colour or a config value, needs none of this.

* **Where:** a new worktree from main, on a branch named `<story|bug|refactor|chore>/<key>-<title-words>`. The key is the ticket's, else a short slug.
* **Definition of done:** the one command every change must pass, every test and the linter. It is the `Definition of done:` line in `AGENTS.md`, else the repository's own test and lint commands, such as `npm test && npm run lint`.
* **Record:** work built now is written down only in its commits and its merge. A ticket is for work left for later.
* **Already red:** when failing tests are already committed for the change, its criteria are agreed: start at Implement.

## Product owner

1. **What and why.** Agree what to build, why, and for whom. Show what in the code bears on it, with `file:line`. When the request names a solution, ask for the problem behind it (the XY problem). Offer a cheaper way if there is one, including one with no code. A ticket that already answers this is the answer.
2. **Acceptance criteria,** as in Example Mapping: one per business rule the change must hold to be right in real use and in this kind of project. A personal tool needs fewer rules than a service others rely on. The rules set the count. Under each rule go its key examples, as Given/When/Then in real values: one per group of inputs the rule treats differently, plus the boundary it states (equivalence partitioning and boundary values). A rule too obvious to get wrong needs no example. Propose a rule the person did not name only with the realistic case that breaks without it, and let them keep or drop it.
   * Too many rules for one small change, or for one short conversation to settle, means the change is too big: offer a split.
   * A rule that needs many examples is several rules, or a concept not yet named.

## Engineer

3. **Design, by coaching.** The person designs; you help them think. Ask how they would build it, then bring in one option they may not know that fits this problem and this codebase: what it is, tied to what they know, and when it wins. Never a menu. Hard-to-reverse choices are theirs, with the options as equals: data stored or sent, a contract others call, a new dependency, auth, how it deploys, how the parts are split. "Just build it" ends the coaching, and you design.
4. **Design review** by a fresh subagent, given a summary of the design (approach, files that change, interfaces, hard-to-reverse choices), the criteria and the worktree. Fix what blocks.
5. **Failing tests:** one per example, through the public interface, each named after its criterion such as `test_ac2_<what>`, with fixtures a wrong implementation would fail. Each is an acceptance test, run at the level where its result shows: against the real database engine for a schema or query, through the running app for what a user sees, with only outside services replaced. Write none that no criterion asks for. See each fail for the right reason, then commit them alone as `test(red): <title>`, with every current criterion in the message as `AC<n>: <rule>` and its examples. When a criterion changes, make a new red commit holding the full set.
6. **Implement** by a fresh subagent, given the worktree, the red commit, the definition of done and [references/refactor.md](references/refactor.md). Trust `git log` and the command output over its report. If `AGENTS.md` has a `Mutation:` line, run it on the changed files and add a test for each surviving mutant.
7. **Code review** by fresh subagents. In a new `<temp>/review-<timestamp>/` folder, put `diff.patch`, the diff against main, and `story.md`, the criteria plus each test changed after the red commit and why. One reviews, another verifies its findings. Tell the person each kept finding in one line, and fix each blocking one test-first.

## Done

8. **Definition of done:** run it on the branch, every test and not only the new ones, and the linter. All must pass before you ship. Fix what fails test-first, never the check or a criterion.
9. **Ship** as the `Ship:` line in `AGENTS.md` says:
   * `Ship: merge`: merge into main, and push main if it has a remote.
   * Otherwise, a pull request titled `[<key>] <what it does>`, with the body from [references/pull-request.md](references/pull-request.md). Watch CI and review comments until it merges, fixing what fails and replying to each comment.
   * After the merge, if `AGENTS.md` has a `Deploy:` line, run it, then smoke-test: one read-only check per criterion that its result shows where it was deployed, such as querying the new view. A failure goes to the person with how to roll back.
   * Then remove the worktree and the branch.

## Bugs, refactors and chores

* **Bug:** reproduce it first, and the reproduction is AC1. If you cannot reproduce it, ask for the missing fact and stop.
* **Refactor:** behaviour stays the same, so there are no new criteria and no red commit, and every existing test passes unchanged. Refactor by [references/refactor.md](references/refactor.md), then go on from code review.
* **Chore,** such as a dependency bump: no criteria; the definition of done on the new version is the proof. Make the change, then go on from code review.

## When to stop

Wait for the person through the design. After that, stop only for a rule a criterion needs, code that contradicts a criterion, or a fact only the person has. Otherwise write `Decided: <choice>, because <reason>` and keep going. These lines go in the pull request or the merge commit.
