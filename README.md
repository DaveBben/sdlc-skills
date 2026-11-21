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
| **1. Frame** | Agents rarely ask the question that matters, and a vague request gets built as a guess. Most of the gain is hearing what you do not know, are missing, or do not know that you do not know. | The `building` skill loads first for any change to code, a story or a chore, and grills it before any code: silent assumptions, the walking skeleton, each item's lifecycle, edge cases, integration points that fail once and every time, one-way doors, and acceptance criteria that are vague or untestable. A story or bug report you bring is its frame. |
| **2. Explore** | Code built on an unchecked answer about an unfamiliar library fails late. Settle unknowns before you plan. | `building` marks each answer `doc` or `memory`, names up to 3 unknown unknowns, and hands an unknown that questions cannot settle to `prototyping`: a timeboxed throwaway experiment with no tests or clean code, deleted once it answers. |
| **3. Build** | Small steps give diffs you can read; the smallest complete change gives less to get wrong. | `building`: a pre-mortem on the plan, red tests from the criteria committed alone, the smallest change that fully does the task, its own git worktree. |
| **4. Verify** | "Done" on the agent's word is not done. | A hook runs your tests and linter every time the agent stops, and sends it back on failure. A commit that edits, deletes or skips an existing test asks you first. |
| **5. Review** | An author misses their own mistakes, and an unchecked review is mostly noise. | The `reviewing` skill: one fresh reviewer, a second agent that proves or drops each finding, and test-first fixes of the blocking ones, within 3 rounds. A hook asks you before a pull request or merge no review preceded. |

After a non-trivial change, the `reflecting` skill reads the session and tells you what to do next time to get better output; a hook reminds the agent when a branch is merged or opened as a pull request.

## Stories, spikes and bugs

Writing, reviewing, splitting, forecasting and filing user stories, spikes and bug reports is the separate `xp-templates` plugin. `building` takes a story from there or from anywhere as its input, and needs neither.

## Hooks

All in [`plugins/agentic-dev/hooks/guard.py`](plugins/agentic-dev/hooks/guard.py):

* **Done check:** your `Definition of done:` command from `AGENTS.md`, else the repository's own test and lint commands, at every stop.
* **Test-tamper gate:** a commit that changes, removes or skips a test the branch started with asks you.
* **Dependency gate:** a package no manifest or lockfile holds asks you.
* **Pull request cap:** a branch over 400 changed lines asks you.
* **Leftovers and silencer gates:** a commit that adds a debugger call, a TODO, commented-out code or a switched-off checker asks you.
* **Size cap:** `AGENTS.md` and `CLAUDE.md` stay under 100 lines.
* **Skill gate:** the first file edit in a session that loaded none of the building, prototyping and reviewing skills asks you.
* **Grill gate:** the first file edit after the building skill loads asks you when the agent has asked you nothing since.
* **Review gate:** a pull request, or a merge into the default branch, of more than a few lines of code that the reviewing skill has not seen in the session asks you.
* **Retro reminder:** once per branch, after a merge or pull request of more than a few lines of code.

House rules for how the agent talks, explains and asks you questions print at session start: [`working-agreement.md`](plugins/agentic-dev/hooks/working-agreement.md).

MIT license.
