# Pair mode

Pair program with the person, who designs as you go. Whoever they name drives first, else you; offer them the wheel after each example you finish. Tell them the worktree's path: they edit there.

## Taking the wheel

When they hand it to you:

1. **Commit their saved work** before any edit of yours. First each change to a locked test, alone, its message naming the test, its file, the criterion and `agreed: the person's own edit`. Then each test file they added, alone, as a red commit. Then the rest.
2. **State the intent** in one line. Where no example covers code they wrote, give its Given and When in real values and ask "then what?". Never fill the Then from their code. Add their answer to the criteria.
3. **Drive test-first** to the next example. Commit its failing test alone, under the framework's strict expected-fail marker where it has one, as a red commit; then the code that passes it, removing the marker. Put your tests and fixtures in new test files.

## Handing it back

When they take the wheel, stop. Commit what passes, leave an unfinished step uncommitted, and say:

```text
Changed: <what the code does now that it did not, and the files>
Decided: <each choice you made and why, or "none">
Next: <the next test or step>
```

Change no code until the wheel comes back. A check that fails at your turn's end on their work is expected: name the failing test and end the turn.

## Challenge

Once the check passes and every criterion holds, have a fresh subagent challenge the tests blind, given the criteria, the worktree and branch, the branch head, and the path of the `red-tests` skill's `SKILL.md`. Ask each `Disagrees:` line as which reading holds, giving both, and make the test follow the person's in its own commit, naming it, its file and `agreed: <their answer>`, then the code. Fix each challenger test that fails.

## Teach-back

Before the review, ask the person, in prose, to walk the data flow from where the change starts to its result and give each decision with its reason. Show no walk of yours first, and offer no skip. If they skip it, the pull request body says `Teach-back: skipped`. Then name each step they missed or got wrong, with its `file:line`, and each decision no criterion asks for. Fix a gap in the code before the review. Their decisions go under `Decided by people`.
