# sdlc-skills

One plugin for coding agents, built on one rule: whoever made a change, someone else attacks it, and a machine decides when it is done.

## What you get

- **Your criteria decide done:** you write the acceptance criteria, and the agent critiques them. The agent that builds never defines done.
- **Tests come first:** failing tests from your examples, then a blind challenger adds tests for wrong implementations and holds some back until the code passes.
- **Fresh agents attack the work:** one implements, one reviews the diff, and one proves or drops each finding before you see it.
- **Hooks enforce the rest:** a committed test can't change without your yes, the `Check:` command must pass before the agent stops, first-seen packages ask you, `AGENTS.md` stays under 100 lines, the implementer can't read the held-back tests, a pull request over 400 changed lines asks you, and so does a commit that leaves in a debugger call or TODO or switches a checker off.

The 18 principles behind it are in [docs/principles.md](docs/principles.md). Most are habits for you, so the plugin holds only what a skill, an agent or a hook can enforce.

## Install

From your shell:

```bash
claude plugin marketplace add DaveBben/sdlc-skills
claude plugin install sdlc@sdlc-skills
```

Then start a new session, or run `/reload-plugins` in one that's open.

Other agents: run `npx skills add DaveBben/sdlc-skills --all` and register `skills/sdlc/agents/` as subagents if your agent supports them. The hooks are Claude Code's.

## How to use it

Say "write a story for X" to agree the criteria, "do a spike on X" for a throwaway experiment, report a bug such as "the export times out past 10k orders", or ask for the change, such as "build PAY-12". Add a `Check:` line to `AGENTS.md`, such as ``Check: `make test` ``, so the done check knows what to run. More detail is in [plugins/sdlc](plugins/sdlc/README.md).

At session start, a hook also adds house rules for how the agent works with you, such as one decision per question and plain explanations. They are in [`plugins/sdlc/hooks/working-agreement.md`](plugins/sdlc/hooks/working-agreement.md). If you installed the old `working-agreement` plugin, uninstall it: `claude plugin uninstall working-agreement@sdlc-skills`.

MIT license.
