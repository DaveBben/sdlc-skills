---
name: build
description: "Use when the person wants to pair, mob, take turns driving or build something together, or when agreed work such as a story file, a ticket or a triaged bug must be built, such as 'let's pair on X' or 'implement story PAY-12': pairs with the person or builds alone on autopilot, test-first, through one fresh review to a pull request."
license: MIT
metadata:
  version: "1.0.0"
---
# Build

Build one ticket to a pull request a person merges. A bug follows [references/bug.md](references/bug.md), a chore or refactoring [references/chore.md](references/chore.md), over any step below.

1. **Criteria:** with neither criteria nor a `Done when:` line, the person writes them by the `story` skill.
2. **Mode:** from the request, else `AGENTS.md`'s `Build:` line, else ask. Pair for code the person must understand; autopilot for code they just want built.
3. **Branch:** a worktree from main, `<story|bug|chore|refactor>/<key>-<title-words>`. Move its issue through In progress, In review and Testing.
4. **Build** by [references/pair.md](references/pair.md) or [references/autopilot.md](references/autopilot.md).
5. **Check:** run `AGENTS.md`'s `Full check:` or `Check:` line, else what CI runs. Run `python3 ../red-tests/scripts/locked_tests.py <merge target> <each red commit>`; each `refused` line is a stop. Where the change reads real data or calls a real service, run it once on the newest real input, writing nothing live, against each criterion's bar.
6. **Review** by the `review` skill. Fix each finding test-first, then redo step 5 and the reading list on the final diff.
7. **Pull request** into main, titled `[<key>] <what it does, imperative>`, body by [references/pull-request.md](references/pull-request.md). Fix CI failures the same way, then wait. Never merge or push to main.
8. **After merge:** remove the worktree and branch. Once in production, observe each criterion, read-only; close the ticket, its spec first by the `spec` skill, or hand a failure to the `bug` skill.
9. **Retro** (After Action Review), each answer citing its evidence: what you assumed wrongly, what the person had to correct or supply, what cost the most time and which check would have caught it. Offer the ones worth keeping, in one multi-select question, as `AGENTS.md` facts by the `onboard` skill or as checks.

## Questions

* **Decide** what a later edit undoes for free: `Decided: <choice>, because <reason>`.
* **Ask** what the criteria leave open and every one-way door: data stored or sent, a contract others call, a dependency, auth, how it deploys. Record each answer by the `adr` skill. Offer the options as equals, and build nothing the answer could change until it comes.
* **Ask before changing** anything a person agreed, however cheap: `<name>: <A> → <B>, because <reason>`.
* **Stuck:** a test you cannot pass, or a locked test you think is wrong, is a question, never a workaround.
* **No person** in the session: read [references/unattended.md](references/unattended.md) first.

## Resume

Read the branch, find the red commits by their messages, and go on at the first step not done.
