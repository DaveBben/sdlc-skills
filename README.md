# sdlc-skills

A plugin for coding agents built on one rule: whoever made the change, someone else attacks it, and a machine decides when it's done.

A plain prompt can't guarantee that. The agent that wrote the code also judges it, and it can edit a failing test until it passes. This plugin enforces the rule with hooks and fresh agents, and keeps its two skills to about 1,400 words.

## What you get

- **Test lock:** a hook asks you before the agent changes or removes a line of a committed test. Adding tests is free.
- **Done check:** a hook runs the `Check:` command from your `AGENTS.md` whenever the agent stops with changed files, and sends it back to work on a failure.
- **Dependency gate:** a hook asks you before the agent installs a package that no manifest or lockfile in the repository names.
- **Size cap:** a hook holds `AGENTS.md` and `CLAUDE.md` to 100 lines and 8 KB.
- **Three fresh agents:** a critic attacks designs and tests, a reviewer reads the diff, and a verifier proves each finding and checks each acceptance criterion against the running app.
- **Two modes:** you write the code to learn and the agent attacks it, or the agent writes it and the three agents attack it.

## Install

```bash
claude plugin marketplace add DaveBben/sdlc-skills
claude plugin install sdlc@sdlc-skills
claude plugin install working-agreement@sdlc-skills   # optional
```

Then start a new session. The hooks need `python3` and `git`.

Other agents: run `npx skills add DaveBben/sdlc-skills --all` and register `skills/sdlc/agents/` as subagents. The hooks are Claude Code hooks, and `plugins/sdlc/hooks/guard.py` reads the same events from any agent that sends them.

## How to use it

1. Say "set this repo up". The `onboard` skill records your `Check:` line and offers mutation testing, property-based tests and a sandbox.
2. Ask for the change. "Build PAY-12" has the agent write it. "Let's pair on the billing calls" or "I'll write it, you review" has you write it.

A small change with one obvious result skips the skills. The hooks still run.

## Does it beat a plain prompt

`python3 tools/baseline.py` runs each task in `tools/tasks/` twice, once with a plain prompt and once with the plugin, and scores defects against held-out tests, refused tool calls, minutes and dollars. Add your own tasks there, and rerun it whenever a new model ships. A part that doesn't beat the plain prompt gets cut.

More detail in [plugins/sdlc](plugins/sdlc/README.md). The principles behind the design are in [docs/principles.md](docs/principles.md).

working-agreement is optional. It adds house rules for how the agent works with you. See [plugins/working-agreement](plugins/working-agreement/README.md).

MIT license.
