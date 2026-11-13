---
name: build
description: "Use when code is to be built and shipped from agreed work or a plain request, such as a story, a ticket, a bug fix, a chore or a refactoring, like 'implement story PAY-12', 'fix this bug' or 'just build X': the person's acceptance criteria decide done, failing tests come first and are challenged blind, fresh agents implement and review, and a small pull request goes to the person."
license: MIT
metadata:
  version: "3.0.0"
---
# Build

Build one change to a pull request a person merges. Whoever made a thing, someone else attacks it, and a check decides when it is done. A bug follows [references/bug.md](references/bug.md), a chore or refactoring [references/chore.md](references/chore.md), over any step below.

A change with one obvious result and no trade-off, such as a colour, a config value or a rename, needs none of this: make it and let the check run.

1. **Criteria:** the ticket's; for a request that states the change in full, its items as `Done when:` lines. Otherwise the person writes them, each a rule with an examples table in real values that a test or the running app can show. Critique what they write in one-line notes, each with your fix; never write a criterion for them. The agent that builds never defines done.
2. **Branch:** a worktree from main, `<story|bug|chore|refactor>/<key>-<title-words>`.
3. **Build** by [references/autopilot.md](references/autopilot.md).
4. **Check:** run `AGENTS.md`'s `Full check:` or `Check:` line, else what CI runs. Where `AGENTS.md` has a `Mutation:` line, run it on the changed files and add a test for each surviving mutant in a changed line. Then see each criterion hold in the running app, through a browser, the command line or a real request, writing nothing live; a passing suite is not that evidence.
5. **Review:** commit, then make a review directory, `<temp>/review-<timestamp>/`, holding `diff.patch` (`git diff --no-color <merge target>...HEAD`) and `story.md` (the ticket, its criteria and each locked-test change the person said yes to). Have one fresh subagent review it, given only the review directory, the worktree, the merge target and the red commits. Then have another verify its findings, given only its `findings.md`, the worktree, `diff.patch`, `story.md` and the check command. Never verify your own change yourself. Tell the person each kept finding in one line, naming the idea, then fix it test-first; redo step 4 on the final diff, and remove the review directory.
6. **Pull request** into main, titled `[<key>] <what it does, imperative>`, body by [references/pull-request.md](references/pull-request.md). Past about 400 changed lines, split it by criterion. Fix CI failures the same way.
7. **After merge:** remove the worktree, the branch and its holdout directory. Once in production, observe each criterion, read-only; a failure is a new bug.
8. **Retro** (After Action Review), each answer citing its evidence: what you assumed wrongly, what the person had to correct or supply, what cost the most time, and which check would have caught it.

## Locked tests

Each committed test is locked: the code changes to fit it. Change a line of one, or add a line that switches tests off, only with the person's yes; in Claude Code a hook asks them. Adding tests is always free. A locked test you think is wrong is a question, never a workaround.

## Questions

* **Decide** what a later edit undoes for free: `Decided: <choice>, because <reason>`.
* **Before you ask, strike every option that:**
  1. fails a criterion's example, or
  2. exists only for something the ticket's `Out of scope` lists, or for a future change no ticket asks for.

  One left: take it as a `Decided:` line naming what would reopen it. Several left: take the one that is no one-way door (data stored or sent, a contract others call, a dependency, auth, how it deploys, how the parts are split) and matches how the repository already does it. Ask only when every option left is a one-way door, offering them as equals, or when the ticket leaves open a result the person will see, such as how a list is ranked, with your pick first. Build nothing the answer could change until it comes. Record a one-way-door answer where the repository keeps decision records, else under the pull request's `Decided by people`.
* **Ask before changing** anything a person agreed, however cheap: `<name>: <A> → <B>, because <reason>`.
* **Stuck:** a test you cannot pass is a question, never a workaround.
* **No person** in the session: ask on the ticket's issue or the pull request, say what waits on the answer, and stop.

## Resume

Read the branch, find the red commits by their messages, and go on at the first step not done.
