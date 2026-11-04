# Pair mode

Pair program; the person designs as you go. Whoever they name drives first, else you; offer them the wheel after each example you finish. They edit in the worktree: tell them its path.

## Taking the wheel

1. **Commit their saved work** before any edit of yours: first each change to a locked test, alone, naming the test, its file, the criterion and `agreed: the person's own edit`; then each test file they added, alone, as a red commit; then the rest.
2. **State the intent** in one line. Where no example covers code they wrote, give its Given and When in real values and ask "then what?". Never fill the Then from their code. Add their answer to the criteria.
3. **Drive test-first** to the next example, each failing test a red commit by the `red-tests` skill, in new test files.

## Handing it back

When they take the wheel, stop. Commit what passes, leave an unfinished step uncommitted, and say:

```text
Changed: <what the code does now that it did not, and the files>
Decided: <each choice you made and why, or "none">
Next: <the next test or step>
```

Change no code until the wheel comes back. A check failing on their work at your turn's end is expected: name the test and end the turn.

## Challenge

Once the check passes and every criterion holds, have a fresh subagent challenge the tests blind by the `red-tests` skill, given the branch head. Fix each challenger test that fails.

## Teach-back

Before the review, the person walks the data flow from where the change starts to its result, then each criterion's failure path, and each decision with its reason, in prose. Show no walk of yours first and offer no skip; a skip goes in the pull request body as `Person walked it back: skipped`. Then name each step they missed or got wrong, with its `file:line`, and each decision no criterion asks for; fix each gap in the code before the review. Their decisions go in the body by [pull-request.md](pull-request.md)'s `Decided by people` rule.
