---
name: build
description: "Use first, before reading or editing code, for any change to code, however small: a feature, story or ticket, a bug or wrong output, a refactor, a new flag, or a chore such as a dependency bump or a runtime upgrade, like 'add a CSV export', 'implement the ticket in docs/tickets/x.md', 'the export crashes on an empty order list', 'rename total to order_total everywhere' or 'bump the requests dependency'. Not for making failing tests that are already committed pass: a fresh subagent does that. Agrees with the person what to build, why, and one acceptance criterion per business rule, coaches them through the design and has it reviewed, writes failing tests first, has fresh agents implement and review, and ships once every test and the linter pass."
license: MIT
metadata:
  version: "4.1.0"
---
# Build

Take one change from request to main, test-first, with fresh agents. The person owns the why and the hard-to-reverse choices: data stored or sent, a contract others call, a new dependency, auth, how it deploys, how the parts are split. A change with one obvious result, such as a config value, needs none of this.

## Set up

A new worktree from main, on branch `<story|bug|refactor|chore>/<key>-<title-words>`, keyed by the ticket, else a short slug.

`AGENTS.md` can hold:

* `Definition of done:` the one command every change must pass; else the repository's own test and lint commands.
* `Ship: merge`; else a pull request.
* `Deploy:` run after the merge.
* `Mutation:` a mutation-testing command.
* `Quality:` a command printing each function's complexity and linter warnings.

## Paths

| Change | Steps |
|---|---|
| Feature | 1 to 9. |
| Bug | Reproduce first, or ask for the missing fact and stop. The reproduction is AC1. With no hard-to-reverse choice, skip 3 and 4. |
| Refactor | No criteria or red commit; tests pass unchanged. 1, [references/refactor.md](references/refactor.md), 7 to 9. |
| Chore | No criteria. 1, the change, 7 to 9. |
| Already red | 6 to 9. |

## Steps

1. **Problem.** Agree what, why and for whom, citing code as `file:line`. Check for the XY problem and a cheaper way, even one with no code.
2. **Rules,** by Example Mapping: one acceptance criterion per business rule.
   * **Missing rules:** look at order, duplicates, ties, equality and empty collections, where you miss them unaided. Propose each with the case it breaks.
   * **Examples:** Given/When/Then in real values, by equivalence partitioning and boundary values. None, one and many are different groups.
   * **Wording:** each Given says how its state came about: "an order placed through checkout", not "an order". Each Then states every result the rule decides that a caller can see: the new total and the changed line, not only the 200.
   * **Too big** for one short conversation: offer the `slicing` skill.
3. **Design, by coaching.** Ask how they would build it, then offer one option they may not know and when it wins, never a menu. "Just build it" means you design.
4. **Design review** by a fresh subagent, given the criteria, the worktree and a summary of a page at most: approach, files changed, interfaces as signatures, constraints, hard-to-reverse choices, no codebase tour. The person settles what it could not check from the code.
5. **Red tests,** one per example, named for its criterion, such as `test_ac2_<what>`: acceptance tests through the public interface, faking only outside services. Set up each Given through the project's own fixtures or entry points, not state the test builds. Assert every result in the Then. Write none that no criterion asks for. See each fail for the right reason, then commit them alone as `test(red): <title>`, with every current criterion as an `AC<n>: <rule>` line and its examples. When a criterion changes, make a new red commit holding the full set.
6. **Implement** by a fresh subagent, given the worktree, the red commit, the definition of done and [references/refactor.md](references/refactor.md). Trust `git log` and command output over its report. With `Mutation:`, add a test for each surviving mutant.
7. **Code review** by fresh subagents: one reviews, another verifies. In a new `<temp>/review-<timestamp>/` folder, put `diff.patch` against main and `story.md`: the criteria, or the problem from 1, and why any test changed after the red commit. With `Quality:`, add each changed function that scores worse than at the merge base. Above about 300 changed lines, split by group of related files: each gets its own reviewer and `<group>/` folder with its `diff.patch` and the same `story.md`, and the findings are joined and renumbered into one `findings.md`. Tell the person each kept finding in one line, and fix blocking ones test-first.
8. **Definition of done** on the branch. Fix the code, never the check or a criterion.
9. **Ship.**
   * `Ship: merge`: show the person the diff summary, the kept findings and the open questions, and wait for their go. Merge, with the Risks and Decided by AI sections of [references/pull-request.md](references/pull-request.md) in the merge commit, and push.
   * Otherwise a pull request titled `[<key>] <what it does>`, with the body from [references/pull-request.md](references/pull-request.md), seen through to merge.
   * With `Deploy:`, ask before running it, then smoke-test each criterion read-only; report a failure with how to roll back.
   * Remove the worktree and the branch.

## When to stop

After the design, stop only for a rule a criterion needs, code that contradicts a criterion, or a fact only the person has. Otherwise write `Decided: <choice>, because <reason>` and keep going.
