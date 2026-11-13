# Autopilot

Stop only for a question, a locked test you cannot satisfy, and the open pull request.

1. **Design,** only for a decision costly to reverse: write each option with what it costs, and have a fresh subagent attack them, given only the criteria and the options, never your reasoning. Then ask the person, the options as equals. Settle every other choice as a `Decided:` line.
2. **Interface:** commit the signatures the change adds as stubs whose bodies only raise, and those it alters with their bodies kept. Skip when existing interfaces carry every criterion.
3. **Red tests,** by Red tests below. Show the test list and go on.
4. **Challenge:** have a fresh subagent challenge the tests blind, given the criteria, the worktree and branch, the interface commit or `none`, the red commit, this file's path and the holdout directory `~/.sdlc-holdout/<repository>/<branch>/`, emptied first. Settle each `Disagrees:` line the criterion's words or examples decide, as a note. Ask only one both readings fit, your pick first.
5. **Implement** by a fresh subagent, one launch at a time, given the worktree, the red commits with at most 8 of their tests, the criteria, the `Decided:` lines, the check command and this file's path, never the holdout directory. Trust `git log` and the check over its return. Settle each `blocked:` line by build's Questions, keep its `Decided:` lines, then launch the next. Review and CI fixes go the same way.
6. **Green:** the whole suite passes. Only now read the holdout directory: copy its files in at the same paths, commit them alone as a red commit, and run them. A failure is a fault in the code; fix it as in step 5.

## Red tests

1. **Name** the tests in `docs/glossary.md`'s terms where it exists. Run that area's tests once.
2. **List** one test per example row, plus one each side of each boundary a criterion's rule states, and no other: `<n>. <criterion> — <test name> — <fixture values> — rejects: <a plausible wrong implementation this fixture fails>`.
3. **Write** each through the interface, at the lowest level that shows its result. Never invent a public name.
   * **Expected values** come from the criterion's words, never from what the code does now. An example that contradicts its criterion's rule goes on `Questions:`, quoting both.
   * **Sociable tests** on production's database engine: double only an outside service, the clock and randomness, preferring the repository's own fake.
   * **Fixtures a wrong implementation fails:** several items with the odd one in the middle, a distinct value per field, no identity values such as quantity 1 or discount 0, unsorted input, more rows than a page, and a unique key per test. An error test asserts the state left behind, not only the raise. Poll with a deadline; never sleep.
   * **Assertions** on exact values a caller sees.
   * **No test** for an example marked `(checked by the user)`. A criterion with no observable result goes on `Questions:`.
4. **Existing tests:** change one only where a criterion states the new behaviour, list it on `Changes existing:`, and get the person's yes; it is locked.
5. **Red:** run them; each fails for the right reason. One already passing is listed `already passing`, or goes.
6. **Commit** them alone on the branch, never main, the message starting `test(red):` and holding the criteria, the test list and `Changes existing:`. A commit hook a red test fails is skipped alone, by its id.

```text
Red: <hash>; tests: <paths>; <n> failing, <n> already passing
Tests: <the numbered list>
Changes existing: <test — criterion>, or "none"
Doubles: <each double and why the real one cannot run>, or "none"
Questions: <criterion — what must be decided — your pick>, or "none"
```
