# Autopilot

Stop only for a question, a locked test you cannot satisfy, and the open pull request.

1. **Spec,** when the story has none: decide by the `spec` skill whether one is due, and write it alone, each choice a `Decided:` line or a question where build's Questions says ask. When you write one, have a fresh subagent review it by the `spec` skill's Review path, given only the spec, the story and that `SKILL.md`'s path; it changes nothing. Fix each gap whose quote you find in the spec, settle each gap the story owns by build's Questions, and go on at `Ready to build`.
2. **Interface:** commit the signatures the change adds as stubs whose bodies only raise, and those it alters with their bodies kept. Skip when existing interfaces carry every criterion.
3. **TDD** by the `tdd` skill, then its challenge, with a holdout directory. Settle every `Questions:` and `Disagrees:` line before any code. Show the test list and go on.
4. **Implement** by a fresh subagent, one launch at a time, given the worktree, the red commits with at most 8 of their tests, the criteria, the spec, the `Decided:` lines, the check command and the `tdd` `SKILL.md` path, never the holdout directory. Trust `git log` and the check over its return. Settle each `unlock:` line by that skill's Unlock, settle each `blocked:` line by build's Questions, keep its `Decided:` lines, then launch the next. Review and CI fixes go the same way.
5. **Green:** the whole suite passes with no marker left. Then run the holdout tests by the `tdd` skill.
