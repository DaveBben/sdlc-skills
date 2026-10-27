# Autopilot

You design and build the change alone, test-first. Stop only for a question, a locked test you cannot satisfy, and the open pull request.

1. **Interface.** Commit the signatures the change adds as stubs whose bodies only raise, and those it alters with their bodies kept. Skip it when existing interfaces carry every criterion.
2. **Red tests** by the `red-tests` skill, then its challenge, with a holdout directory. Settle every `Questions:` and `Disagrees:` line before any code. Show the test list and go on.
3. **Implement** by a fresh subagent that makes the failing tests pass, one at a time in this worktree, given the worktree and branch, the red commits with at most 8 of their tests, the criteria, the spec's path, the `Decided:` lines so far, the check command and the `red-tests` skill's `SKILL.md` path; never the holdout directory. Trust `git log` and the Check step over its return. Ask each `blocked:` line, keep its `Decided:` lines, then launch the next. Review and CI fixes go the same way.
4. **Green.** The whole suite passes with no marker left. Then run the holdout tests by the `red-tests` skill.
