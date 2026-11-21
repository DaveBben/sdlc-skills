# agentic-dev

A Claude Code plugin for coding with AI agents: you drive a short loop, the plugin keeps you in it, and a machine decides when work is done.

## Install

```bash
claude plugin marketplace add DaveBben/sdlc-skills
claude plugin install agentic-dev@sdlc-skills
```

Then start a new session, or run `/reload-plugins`. If you had the old `sdlc` plugin: `claude plugin uninstall sdlc@sdlc-skills`.

## The loop

| Step | Why it matters | Here |
|---|---|---|
| **1. Frame** | Agents rarely ask the question that matters, and a vague request gets built as a guess. Agree the goal, the why and a done-check you can watch run before any code. | The `story` skill loads first for any change to code: every change starts as a user story, written to a file only when it is for later; it grills a vague request, writes one acceptance criterion per business rule with a Given/When/Then example, and looks where gaps hide (none, one and many; duplicates; a second run). |
| **2. Explore** | Code built on an unchecked answer about an unfamiliar library fails late. Settle unknowns before you plan. | `story` marks each answer `doc` or `memory` and names the parts that may be new to you. An unknown that questions cannot settle goes to the `spike` skill: a timeboxed throwaway experiment. |
| **3. Build** | Small steps give diffs you can read; the smallest complete change gives less to get wrong. | The `building` skill: a pre-mortem on your design, the smallest change that fully does the task, its own git worktree. |
| **4. Verify** | "Done" on the agent's word is not done. | A hook runs your tests and linter every time the agent stops, and sends it back on failure. A commit that edits, deletes or skips an existing test asks you first. |
| **5. Review** | An author misses their own mistakes, and an unchecked review is mostly noise. | The `reviewing` skill: one fresh reviewer, a second agent that proves or drops each finding, and test-first fixes of the blocking ones, within 3 rounds. |

After a non-trivial change, the `reflecting` skill reads the session and tells you what to do next time to get better output; a hook reminds the agent when a branch is merged or opened as a pull request.

## At work

* **`story`** writes, reviews or splits user stories for later or for others, and forecasts how long they will take. A story is a Frame written down for a reader outside the chat; work you build now needs none.
* **`bug`** reproduces, reports and triages a bug without fixing it; fixing starts at `story`.
* **`spike`** frames a question that can fail, builds throwaway code and records what it found.
* **`explaining`** loads when you want to understand something: one concrete case first, then the mechanism.

## Hooks

All in [`plugins/agentic-dev/hooks/guard.py`](plugins/agentic-dev/hooks/guard.py):

* **Done check:** your `Definition of done:` command from `AGENTS.md`, else the repository's own test and lint commands, at every stop.
* **Test-tamper gate:** a commit that changes, removes or skips a test the branch started with asks you.
* **Dependency gate:** a package no manifest or lockfile holds asks you.
* **Pull request cap:** a branch over 400 changed lines asks you.
* **Leftovers and silencer gates:** a commit that adds a debugger call, a TODO, commented-out code or a switched-off checker asks you.
* **Size cap:** `AGENTS.md` and `CLAUDE.md` stay under 100 lines.
* **Plan gate:** the first file edit after the building skill loads asks you when the agent has asked you nothing since.
* **Retro reminder:** once per branch, after a merge or pull request of more than a few lines of code.

House rules for how the agent talks and asks you questions print at session start: [`working-agreement.md`](plugins/agentic-dev/hooks/working-agreement.md).

MIT license.
