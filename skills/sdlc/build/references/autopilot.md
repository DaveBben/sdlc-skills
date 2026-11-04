# Autopilot

Stop only for a question, a locked test you cannot satisfy, and the open pull request.

1. **Spec,** when the story has none: size and write it alone by the `spec` skill, each choice a `Decided:` line or a question where build's Questions says ask.
2. **Interface:** commit the signatures the change adds as stubs whose bodies only raise, and those it alters with their bodies kept. Skip when existing interfaces carry every criterion.
3. **Red tests** by the `red-tests` skill, then its challenge, with a holdout directory. Settle every `Questions:` and `Disagrees:` line before any code. Show the test list and go on.
4. **Implement** by a fresh subagent, one launch at a time, given the worktree, the red commits with at most 8 of their tests, the criteria, the spec, the `Decided:` lines, the check command and the `red-tests` `SKILL.md` path, never the holdout directory. Trust `git log` and the check over its return. Ask each `blocked:` line, keep its `Decided:` lines, then launch the next. Review and CI fixes go the same way.
5. **Green:** the whole suite passes with no marker left. Then run the holdout tests by the `red-tests` skill.
