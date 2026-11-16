# sdlc

2 skills, 5 agents, 6 hooks and the house rules. Whoever made a change, someone else attacks it, and a machine decides when it is done.

## What runs in a session

- **The `build` skill:** loads for any change: a feature, a bug or a refactor. It first agrees with you in chat what you want, why, and the happy and failure paths, as Given/When/Then criteria in real values, and reviews them against the failure modes of bad criteria. A bug is reproduced first; a refactor keeps every test unchanged. It plans the change and has the plan reviewed, asks you each hard-to-reverse decision, writes failing tests from your examples and commits them, then delegates the rest. Ask for a story and it writes the criteria up as one, such as for a ticket at work.
- **The `spike` skill:** "do a spike on X" frames a question that can fail, builds throwaway code in a scratch directory, records the findings and deletes the code.
- **5 agents:** a plan reviewer attacks a spec, design or plan before any code, an implementer makes the tests pass, a reviewer reads the diff, a verifier proves or drops each finding, and a delegator (Sonnet) runs a non-coding task in parallel and returns only its status, result, and what it created or deleted.
- **House rules:** at session start, and again after `/clear` or a compaction, a hook prints [`hooks/working-agreement.md`](hooks/working-agreement.md): how the agent works with you, asks you questions and explains things.
- **6 hooks,** all in [`hooks/guard.py`](hooks/guard.py):
  - **Done check:** when the agent stops, the `Check:` command of `AGENTS.md` runs in each worktree that changed, and a failure sends it back.
  - **Size cap:** `AGENTS.md` and `CLAUDE.md` stay under 100 lines and 8 KB.
  - **Dependency gate:** a package that no manifest or lockfile holds asks you.
  - **Pull request cap:** opening or pushing a branch past 400 changed lines asks you.
  - **Leftovers gate:** a commit that adds a debugger call, a TODO or commented-out code asks you.
  - **Silencer gate:** a commit that adds `# type: ignore`, `eslint-disable`, `as any` or the like asks you.

A change with no trade-off, such as a colour or a config value, skips the skill: the agent makes it and the done check runs.

Finish branches started under sdlc 1.x before upgrading. Their red tests carry expected-fail markers that 3.0 no longer removes.

## One build, traced

"Build PAY-12: orders of 10 or more get 5% off."

| Step | Who | What happens |
|---|---|---|
| Align | you, agent | You give the rule and why; the agent asks for the boundary and you give an examples table: 9 items full price, 10 items 5% off |
| Red tests | agent | Writes a test per row and each side of the boundary, sees each fail, and commits them |
| Implement | implementer | Makes the tests pass. A mutation run finds one weak test, and the agent adds a test that kills it |
| Review | reviewer, verifier | 3 candidates found, 1 proved: a discount applied twice on retry |
| Pull request | agent | Fixes it test-first, and opens a pull request under 400 lines |
