# sdlc

3 skills, 5 agents, 7 hooks and the house rules. Whoever made a change, someone else attacks it, and a machine decides when it is done.

## What runs in a session

- **The `build` skill:** loads for any change: a feature, a bug or a refactor. It first agrees with you in chat what you want and why, offers a cheaper way if there is one, and agrees 1 to 3 Given/When/Then criteria in real values, proposing at most 2 more with the case behind each. Then it coaches you through the design, one option you may not know at a time, unless you say "just build it", and has the design reviewed. A bug is reproduced first; a refactor keeps every test unchanged. It commits failing tests with the criteria in the commit message, delegates the rest, and merges into main when `AGENTS.md` says `Ship: merge`, else opens a pull request. Nothing is written to a tracker for work done now.
- **The `ticket` skill:** a story, bug or spike written down for later, in at most 15 lines and 3 criteria.
- **The `spike` skill:** "do a spike on X" frames a question that can fail, builds throwaway code in a scratch directory, records the findings and deletes the code.
- **5 agents:** a design reviewer attacks a spec, design or plan before any code, an implementer makes the tests pass, a code reviewer reads the diff, a verifier proves or drops each finding, and a delegator (Sonnet) runs a non-coding task in parallel and returns only its status, result, and what it created or deleted.
- **House rules:** at session start, and again after `/clear` or a compaction, a hook prints [`hooks/working-agreement.md`](hooks/working-agreement.md): how the agent works with you, asks you questions and explains things.
- **7 hooks,** all in [`hooks/guard.py`](hooks/guard.py):
  - **Done check:** when the agent stops, the definition of done runs in each worktree that changed: the `Definition of done:` command of `AGENTS.md` if it has one, else the repository's own test and lint commands. A failure sends it back.
  - **Size cap:** `AGENTS.md` and `CLAUDE.md` stay under 100 lines and 8 KB.
  - **Dependency gate:** a package that no manifest or lockfile holds asks you.
  - **Pull request cap:** opening or pushing a branch past 400 changed lines asks you.
  - **Acceptance gate:** pushing, opening a pull request from or merging a branch checks that each `AC<n>` criterion in its latest `test(red):` commit message has a test named for it, then runs the definition of done. Any failure refuses it. A merge is checked on the branch's committed state.
  - **Leftovers gate:** a commit that adds a debugger call, a TODO or commented-out code asks you.
  - **Silencer gate:** a commit that adds `# type: ignore`, `eslint-disable`, `as any` or the like asks you.

A change with no trade-off, such as a colour or a config value, skips the skill: the agent makes it and the done check runs.

Finish branches started under sdlc 3.x before upgrading: 4.0 reads criteria from the red commit, not `docs/acceptance/`.

## One build, traced

"Build PAY-12: orders of 10 or more get 5% off."

| Step | Who | What happens |
|---|---|---|
| Align | you, agent | You give the rule and why; the agent proposes one more criterion, 9 items pay full price, because the boundary is where this goes wrong |
| Design | you, agent | You plan to change `total`; the agent asks where the 5% is rounded and you decide |
| Red tests | agent | Writes a test per criterion, sees each fail, and commits them with the criteria in the message |
| Implement | implementer | Makes the tests pass. A mutation run finds one weak test, and the agent adds a test that kills it |
| Review | code-reviewer, verifier | 3 candidates found, 1 proved: a discount applied twice on retry |
| Ship | agent | Fixes it test-first, then merges into main under `Ship: merge`, else opens a pull request under 400 lines |
