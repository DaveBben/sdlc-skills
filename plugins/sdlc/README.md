# sdlc

One skill, 4 agents and 6 hooks. Whoever made a change, someone else attacks it, and a machine decides when it is done.

## What runs in a session

- **The `build` skill:** loads when you ask for a change to be built or fixed. You write the acceptance criteria, it writes failing tests from your examples and commits them, then delegates the rest.
- **4 agents:** a test challenger adds tests for wrong implementations without reading the code and holds some back, an implementer makes the tests pass without seeing the held-back ones, a reviewer reads the diff, and a verifier proves or drops each finding.
- **6 hooks,** all in [`hooks/guard.py`](hooks/guard.py):
  - **Test lock:** an edit that changes or removes a line of a committed test asks you.
  - **Done check:** when the agent stops, the `Check:` command of `AGENTS.md` runs, and a failure sends it back.
  - **Size cap:** `AGENTS.md` and `CLAUDE.md` stay under 100 lines and 8 KB.
  - **Dependency gate:** a package that no manifest or lockfile holds asks you.
  - **Holdout guard:** the implementer can't read the held-back tests.
  - **Pull request cap:** opening or pushing a branch past 400 changed lines asks you.

A change with no trade-off, such as a colour or a config value, skips the skill: the agent makes it and the done check runs.

Finish branches started under sdlc 1.x before upgrading. Their red tests carry expected-fail markers that 3.0 no longer removes.

## One build, traced

"Build PAY-12: orders of 10 or more get 5% off."

| Step | Who | What happens |
|---|---|---|
| Criteria | you | Write the rule with an examples table: 9 items full price, 10 items 5% off |
| Red tests | agent | Writes a test per row and each side of the boundary, sees each fail, and commits them |
| Challenge | test challenger | Adds a test with 11 unsorted items and holds back a property test |
| Implement | implementer | Makes the tests pass. The hook asks you if it tries to edit a committed test |
| Holdout | agent | Copies the held-back test in. It passes |
| Review | reviewer, verifier | 3 candidates found, 1 proved: a discount applied twice on retry |
| Pull request | agent | Fixes it test-first, and opens a pull request under 400 lines |
