# sdlc

8 skills, 8 hooks and the house rules. You drive a loose loop, Frame, Explore, Plan, Build, Verify, Review, and a machine decides when it is done.

## What runs in a session

- **The `frame` skill:** loads first for any change to code. It grills you when the change is vague, in rounds of questions only you can answer, looks first where gaps hide, and agrees one acceptance criterion per business rule. Then it hands to `build` to build it now, or to `story` to write it down for later.
- **The `build` skill:** loads for any change to code: a pre-mortem on your design, strongest objection first; the smallest change that fully does the task; its own worktree; done only when a check passed.
- **The `explain` skill:** loads when you need to understand something: it bridges from what you know, shows one concrete case before the mechanism, and gives the source of every number.
- **The `retro` skill:** once a non-trivial change is finished or given up, you say what you would do differently, then a fresh agent reads the session's transcript against the loop. You get at most 5 findings, each with a quote from the session, what it cost and what to type next time, to keep or drop. An agent mistake becomes a proposed `AGENTS.md` line.
- **The `review` skill:** before a non-trivial change is merged or opened as a pull request, or when you ask, a fresh agent reviews the diff against what you asked for, a second proves or drops each finding, and you get each kept finding in one line. The agent fixes the blocking ones test-first, and after 3 rounds it stops and asks you.
- **The `story` skill:** for work written down for later or for other people. A story is a short frame for one vertical slice that fits one merge request: why, scope, and one acceptance criterion per business rule with a worked example and a check. It also reviews stories, splits an epic into them and forecasts a set of them by counting. Its criteria become the build's done-check and the review's `story.md`.
- **The `bug` skill:** reports, reproduces and triages a bug without fixing it, and says which check should have caught one that reached users. The reproduction is the build's first failing check.
- **The `spike` skill:** for "would this work" questions. It frames a question that can fail and the decision it changes, runs throwaway code inside a timebox, records the finding and deletes the code.
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
