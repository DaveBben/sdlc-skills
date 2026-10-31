---
name: build
description: "Use when the person wants to pair, mob, take turns driving or build something together, or when agreed work such as a story file, a ticket or a triaged bug must be built, such as 'let's pair on X' or 'implement story PAY-12': pairs with the person or builds alone on autopilot, test-first, through one fresh review to a pull request."
license: MIT
metadata:
  version: "1.0.0"
---
# Build

Build one ticket, a story, bug, chore or plain request, to a pull request that a person merges. A bug follows [references/bug.md](references/bug.md), and a chore or refactoring [references/chore.md](references/chore.md), over any step below.

1. **Criteria first.** Read the ticket and its comments; its `## Spec` is settled, so ask only what it leaves open. It needs numbered criteria, each with Given/When/Then examples in real values, and a failure example for each criterion that saves data or calls another system. Each invariant is a criterion of its own. Without them, write them by the `story` skill.
2. **Mode.** Take it from the person's request, else the `Build:` line of `AGENTS.md`, else ask: pair, for code the person will run, debug or extend; autopilot, for code they just want built. Then a story with neither a `## Spec` nor a `Spec: none` line gets its spec, so its design meets the code as it stands at pickup: on pair, with the person by the `spec` skill; on autopilot, by its Spec step.
3. **Branch.** A git worktree on a new branch from main, `<story|bug|chore|refactor>/<key>-<title-words>`. Move its issue, if any, by the `tracker` skill: In progress now, In review when the pull request opens, Testing once merged.
4. **Build** by [references/pair.md](references/pair.md) or [references/autopilot.md](references/autopilot.md). After each green step, refactor what it touched: one named refactoring per commit, `refactor: <refactoring> (<smell>)`, by TCR, keeping behaviour, public names and error handling.
5. **Check.** Run the check command, the `Full check:` or `Check:` line of `AGENTS.md`, else what CI runs. Then run `python3 ../red-tests/scripts/locked_tests.py <merge target> <each red commit>`, which checks the locked tests: each test in a red commit and each from before the branch. Each `refused` line is a stop: undo that change, or remake it by the `red-tests` skill once a person agrees.
6. **Review** by the `review` skill, given the ticket, the merge target, the red commits, the check command, the locked-tests lines, the surviving and no-coverage mutants and the design: the spec and every `Decided` line. A behaviour fault or test gap gets a test that fails on it, in a new test file, committed alone as a red commit, then the fix. Ask each question. Then redo step 5, and the review's reading list, on the final diff.
7. **Pull request** into main, titled `[<key>] <title>`. Its body: the review's tier and reading list first; `Build: pair` or `Build: autopilot`; `Decided by people:` and `Decided by the agent:`, one line per choice; the test lists; the locked-tests lines; how to verify it by hand.
8. **Ship.** Fix each CI failure this branch causes as step 6 fixes a finding, and update the pull request body; then wait for the person. Never merge or push to main. Once merged, remove its worktree and delete its branch. Once the merge reaches production, observe each criterion there, reading only. Close the ticket, closing its spec first by the `spec` skill, or hand a criterion that fails to the `bug` skill.
9. **Retro,** as an After Action Review. Answer each in a line or two, citing what showed it; "nothing" is an answer. Then offer each answer worth keeping in one multi-select question: a fact for `AGENTS.md` by the `onboard` skill, or a check for this repository.
   * **Surprised:** what did you assume about this project that turned out wrong, and what showed you?
   * **Corrected:** what did the person have to correct, repeat or supply that the repository did not tell you?
   * **Failed:** what failed or cost the most time, and what check would have caught it sooner?

## Questions

* **Decide** a choice a later edit undoes for free and no person agreed, and list it: `Decided: <choice>, because <reason>`.
* **Ask** what the criteria leave open, and every choice costly to reverse: a data shape stored or sent, a contract other code calls, a dependency, auth or permissions, how it deploys or runs, what a failure does to data. Ask a change to any number, bar or rule a person agreed, such as a criterion's value or a spike's bar, as `<name>: <A> → <B>, because <reason>`, however cheap the edit. Build nothing the answer could change until it comes.
* **How:** one decision per question, multiple-choice where the tool allows. Lead with the question in plain words, then one concrete case, then each option with what it changes for the person, then whether it is easy to reverse. Give an issue number or a term coined earlier only with half a sentence of what it means. Recommend one option, unless the choice is costly to reverse or sets a target or what success means: then give the options as equals, and your pick in one line after the answer if it differs.
* **Stuck:** a test you cannot pass, or a locked test you think is wrong, is a question, never a workaround.
* **Record** an answer costly to reverse by the `adr` skill.
* **No person** in the session, such as a scheduled run: read [references/unattended.md](references/unattended.md) first.

## Resume

Read the branch. Every red commit holds only tests and lists them in its message: find them by that. Go on at the first step not done.
