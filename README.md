# sdlc-skills

Two Claude Code plugins. `agentic-dev` is for coding with AI agents: you drive a short loop, the plugin keeps you in it, and a machine decides when work is done.

## Install

```bash
claude plugin marketplace add DaveBben/sdlc-skills
claude plugin install agentic-dev@sdlc-skills
claude plugin install xp-templates@sdlc-skills   # optional: stories, spikes and bug reports
```

Then start a new session, or run `/reload-plugins`. If you had the old `sdlc` plugin: `claude plugin uninstall sdlc@sdlc-skills`.

## The loop

| Step | Why it matters | Here |
|---|---|---|
| **1. Frame** | Agents rarely ask the question that matters, and a vague request gets built as a guess. Most of the gain is hearing what you do not know, are missing, or do not know that you do not know. | xp-templates' `discovery` interviews you into a story or a PRD, and `design` talks your design options through against the code and the data. The `task` skill asks at most one clarifying question and for a done check when you gave none. |
| **2. Explore** | Code built on an unchecked answer about an unfamiliar library fails late. Settle unknowns before you plan. | `prototyping` settles an unknown that questions cannot: a timeboxed experiment with no tests or clean code, deleted once you are done with it. |
| **3. Build** | Small steps give diffs you can read; the smallest complete change gives less to get wrong. | `task`: a held-out check the agent writing the code never sees, seen failing for the right reason, then a subagent that makes it pass from the simplest solution up, in its own git worktree. A hook denies the subagent any read of the check. |
| **4. Verify** | "Done" on the agent's word is not done. | A hook runs your tests and linter every time the agent stops, and sends it back on failure. A commit that edits, deletes or skips an existing test asks you first. |
| **5. Review** | An author misses their own mistakes, and an unchecked review is mostly noise. | The `reviewing` skill: one fresh reviewer, a second agent that proves or drops each finding, and test-first fixes of the blocking ones, within 3 rounds. A hook asks you before a pull request or merge no review preceded. |

After a non-trivial change, the `reflecting` skill reads the session and tells you what to do next time to get better output; a hook reminds the agent when a branch is merged or opened as a pull request.

## Stories, spikes, bugs, designs and PRDs

The `xp-templates` plugin writes, reviews and files XP artifacts, and builds nothing. `task` builds a change whose done one check proves, and needs neither.

* **`discovery`** interviews you and writes what the scope calls for: a user story for one vertical slice, or a PRD and its story map for several features or a product.
* **`story`** holds the story template, reviews one, splits an epic or PRD into stories, and forecasts a set from throughput.
* **`spike`** frames a question that can fail in 4 lines, reviews one, and records what the experiment found. `prototyping` runs it.
* **`bug`** reproduces a bug, reports it with a severity and a decision, triages a backlog, and names the check a bug escaped.
* **`design`** talks a design through with you: you bring the options and decide; it draws each out by seven questions, holds it against the code and a real sample of the data, and raises the unknowns you have not. It then writes the design doc or ADR (under 200 lines, the decision first, readable from outside the team), and reviews one.
* **`prd`** holds the PRD template, including who runs, maintains and pays for it after launch, and reviews a PRD you were handed for what it leaves out.
* **`tracker`** files each as a labelled issue in GitHub, GitLab, Gitea or Jira, with blockers linked by the tracker's own relation.

## Hooks

All in [`plugins/agentic-dev/hooks/guard.py`](plugins/agentic-dev/hooks/guard.py):

* **Done check:** your `Definition of done:` command from `AGENTS.md`, else the repository's own test and lint commands, at every stop.
* **Test-tamper gate:** a commit that changes or removes an assertion or a test the branch started with, or skips a test, asks you once per line.
* **Dependency gate:** a package no manifest or lockfile holds asks you.
* **Pull request cap:** a branch over 400 changed lines asks you.
* **Leftovers and silencer gates:** a commit that adds a debugger call, a TODO, commented-out code or a switched-off checker asks you.
* **Size cap:** `AGENTS.md` and `CLAUDE.md` stay under 100 lines.
* **Check gate:** a subagent's read, search or edit that reaches a task's held-out check is denied; it may only run the check.
* **Skill gate:** the first file edit in a session that loaded none of the task, prototyping and reviewing skills, nor an xp-templates skill, asks you.
* **Review gate:** a pull request, or a merge into the default branch, of more than a few lines of code that the reviewing skill has not seen in the session asks you.
* **Retro reminder:** once per branch, after a merge or pull request of more than a few lines of code.

House rules for how the agent talks, explains and asks you questions print at session start: [`working-agreement.md`](plugins/agentic-dev/hooks/working-agreement.md).

MIT license.
