# sdlc-skills

One Claude Code plugin. `agentic-dev` is for coding with AI agents: you drive a short loop, the plugin keeps you in it, and a machine decides when work is done.

## Install

```bash
claude plugin marketplace add DaveBben/sdlc-skills
claude plugin install agentic-dev@sdlc-skills
```

Then start a new session, or run `/reload-plugins`. If you had the old `sdlc` plugin: `claude plugin uninstall sdlc@sdlc-skills`.

## The loop

| Step | Why it matters | Here |
|---|---|---|
| **1. Frame** | Agents rarely ask the question that matters, and a vague request gets built as a guess. Most of the gain is hearing what you do not know, are missing, or do not know that you do not know. | `story` interviews you until nothing is ambiguous, failure paths included, and confirms the acceptance criteria with you in plain language before it splits them into stories. `task` asks at most one clarifying question and for a done check when you gave none. |
| **2. Explore** | Code built on an unchecked answer about an unfamiliar library fails late. Settle unknowns before you plan. | `spike` settles an unknown that questions cannot: a timeboxed question with a bar a script decides, answered with throwaway code in a scratch directory, with its own rules for ML experiments, hardware, performance, third-party APIs, races, UI mocks and library behaviour. |
| **3. Build** | Small steps give diffs you can read; the smallest complete change gives less to get wrong. | `task`: a held-out check the agent writing the code never sees, seen failing for the right reason, then a subagent that makes it pass from the simplest solution up, in its own git worktree. `story`: a reviewed plan, design choices settled with you, hidden failing tests, then slices of at most 200 lines, each built as a task. A hook denies the subagents any read of the checks. |
| **4. Verify** | "Done" on the agent's word is not done. | A hook runs your tests and linter every time the agent stops, and sends it back on failure. A commit that edits, deletes or skips an existing test asks you first. |
| **5. Review** | An author misses their own mistakes, and an unchecked review is mostly noise. | The `reviewer` agent on every slice, then the `reviewer` and the `verifier`, which proves or drops each finding, on the whole story. A hook asks you before a pull request or merge no reviewer preceded. |

## Hooks

All in [`plugins/agentic-dev/hooks/guard.py`](plugins/agentic-dev/hooks/guard.py):

* **Done check:** your `Definition of done:` command from `AGENTS.md`, else the repository's own test and lint commands, at every stop.
* **Test-tamper gate:** a commit that changes or removes an assertion or a test the branch started with, or skips a test, asks you once per line.
* **Dependency gate:** a package no manifest or lockfile holds asks you.
* **Leftovers and silencer gates:** a commit that adds a debugger call, a TODO, commented-out code or a switched-off checker asks you.
* **Size cap:** `AGENTS.md` and `CLAUDE.md` stay under 100 lines.
* **Check gate:** a subagent's read, search or edit that reaches a task's held-out check is denied; it may only run the check.
* **Slice cap:** merging a slice branch (`slice/...`) of a story that brings more than 200 lines of code is denied.
* **Skill gate:** the first file edit in a session that loaded none of the task, story and spike skills asks you.
* **Review gate:** a pull request, or a merge into the default branch, of more than a few lines of code that no reviewer agent saw in the session asks you.

House rules for how the agent talks, explains and asks you questions print at session start: [`working-agreement.md`](plugins/agentic-dev/hooks/working-agreement.md).

MIT license.
