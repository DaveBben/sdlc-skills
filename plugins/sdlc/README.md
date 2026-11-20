# sdlc

4 skills, 8 hooks and the house rules. You drive a loose loop, Frame, Explore, Plan, Build, Verify, Review, and a machine decides when it is done.

## What runs in a session

- **Framing:** the house rules have the agent grill you when a change is vague, in rounds of questions only you can answer, until you agree the goal and why, the context and a done-check you can watch run. It looks first where gaps hide (none, one and many; duplicates and order; a second run, a missed run; what expires when it runs unattended) and marks each answer about an unfamiliar API as `doc` or `memory`.
- **The `build` skill:** loads for any change to code: a pre-mortem on your design, strongest objection first; the smallest change that fully does the task; its own worktree; done only when a check passed.
- **The `explain` skill:** loads when you need to understand something: it bridges from what you know, shows one concrete case before the mechanism, and gives the source of every number.
- **The `retro` skill:** once a non-trivial change is finished or given up, you say what you would do differently, then a fresh agent reads the session's transcript against the loop. You get at most 5 findings, each with a quote from the session, what it cost and what to type next time, to keep or drop. An agent mistake becomes a proposed `AGENTS.md` line.
- **The `review` skill:** before a non-trivial change is merged or opened as a pull request, or when you ask, a fresh agent reviews the diff against what you asked for, a second proves or drops each finding, and you get each kept finding in one line. The agent fixes the blocking ones test-first, and after 3 rounds it stops and asks you.
- **House rules:** at session start, and again after `/clear` or a compaction, a hook prints [`hooks/working-agreement.md`](hooks/working-agreement.md): how the agent works with you, asks you questions and explains things.
- **8 hooks,** all in [`hooks/guard.py`](hooks/guard.py):
  - **Done check:** when the agent stops, the definition of done runs in each worktree that changed: the `Definition of done:` command of `AGENTS.md` if it has one, else the repository's own test and lint commands. A failure sends it back.
  - **Size cap:** `AGENTS.md` and `CLAUDE.md` stay under 100 lines and 8 KB.
  - **Dependency gate:** a package that no manifest or lockfile holds asks you.
  - **Pull request cap:** opening or pushing a branch past 400 changed lines asks you.
  - **Leftovers gate:** a commit that adds a debugger call, a TODO or commented-out code asks you.
  - **Silencer gate:** a commit that adds `# type: ignore`, `eslint-disable`, `as any` or the like asks you.
  - **Test-tamper gate:** a commit that changes or removes a line of a test the branch started with, or adds a skip or expected-failure marker, asks you.
  - **Retro reminder:** once per branch, after a pull request is opened from it or it is merged, a branch with more than 20 changed lines of code, prose and config left out, tells the agent to run the retro.
