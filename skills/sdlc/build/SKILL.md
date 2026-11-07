---
name: build
description: "Use when agreed work such as a story file, a ticket or a triaged bug must be built, or a pair-programming branch shipped, such as 'implement story PAY-12' or 'just build X': asks whether to pair or run autopilot unless told, then builds it test-first through one fresh review to a pull request."
license: MIT
metadata:
  version: "1.0.0"
---
# Build

Build one ticket to a pull request a person merges. A bug follows [references/bug.md](references/bug.md), a chore or refactoring [references/chore.md](references/chore.md), over any step below.

1. **Criteria:** the ticket's, else the request's items as `Done when:` lines; with neither, the person writes them by the `story` skill.
2. **Mode:** from the request, else the ticket's comments, else `AGENTS.md`'s `Build:` line, else ask whether to pair or run autopilot, your pick first. To pair, run the `pair-programming` skill on the ticket. A branch it hands back goes straight to step 5.
3. **Branch:** a worktree from main, `<story|bug|chore|refactor>/<key>-<title-words>`. Move its issue through In progress, In review and Testing.
4. **Build** by [references/autopilot.md](references/autopilot.md).
5. **Check:** run `AGENTS.md`'s `Full check:` or `Check:` line, else what CI runs. Except on a branch from pairing, run `python3 ../tdd/scripts/locked_tests.py <merge target> <each red commit>`; each `refused` line is a stop. Where the change reads real data or calls a real service, run it once on the newest real input, writing nothing live, against each criterion's bar.
6. **Review:** commit, then make a review directory, `<temp>/review-<timestamp>/`, holding `diff.patch` (`git diff --no-color <merge target>...HEAD`), `story.md` (the ticket and its criteria) and, except from pairing, `locked.txt` (step 5's locked-tests lines). Have one fresh subagent review it, given only the review directory, the worktree, the merge target and the red commits. Then have another verify its findings, given only its `findings.md`, the worktree, `diff.patch`, `story.md` and the check command. Tell the person each kept finding in one line, naming the idea, then fix it test-first; redo step 5 on the final diff, and remove the review directory.
7. **Pull request** into main, titled `[<key>] <what it does, imperative>`, body by [references/pull-request.md](references/pull-request.md). Fix CI failures the same way.
8. **After merge:** remove the worktree and branch. Once in production, observe each criterion, read-only; close the ticket, its spec first by the `spec` skill, and the design doc it links by the `design` skill's Built rule when it was the last story left, or hand a failure to the `bug` skill.
9. **Retro** (After Action Review), each answer citing its evidence: what you assumed wrongly, what the person had to correct or supply, what cost the most time and which check would have caught it, and which question a `Decided:` line or a note would have served.

## Questions

* **Decide** what a later edit undoes for free: `Decided: <choice>, because <reason>`.
* **Before you ask, strike every option that:**
  1. fails a criterion's example, or
  2. exists only for something the story's `Out of scope` lists, or for a future change no story asks for.

  One left: take it as a `Decided:` line naming what would reopen it. Several left: take the one that is no one-way door (data stored or sent, a contract others call, a dependency, auth, how it deploys, how the parts are split) and matches how the repository already does it. Ask only when every option left is a one-way door, offering them as equals, or when the ticket leaves open a result the person will see, such as how a list is ranked, with your pick first. Build nothing the answer could change until it comes, and record a one-way-door answer by the `adr` skill, any other on the story.
* **Ask before changing** anything a person agreed, however cheap: `<name>: <A> → <B>, because <reason>`.
* **Stuck:** a test you cannot pass, or a locked test you think is wrong, is a question, never a workaround.
* **No person** in the session: read [references/unattended.md](references/unattended.md) first.

## Resume

Read the branch, find the red commits by their messages, and go on at the first step not done.
