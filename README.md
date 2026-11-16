# sdlc-skills

One plugin for coding agents, built on one rule: whoever made a change, someone else attacks it, and a machine decides when it is done.

## What you get

- **You decide done:** before any work, the agent agrees with you in chat what you want, why, and the happy and failure paths. The agent that builds never defines done.
- **Tests come first:** failing tests from your examples, committed before any code; mutation testing finds the weak ones.
- **Fresh agents attack the work:** one implements, one reviews the diff, and one proves or drops each finding before you see it.
- **Hooks enforce the rest:** your tests must pass before the agent stops, first-seen packages ask you, `AGENTS.md` stays under 100 lines, a push or pull request is refused until every agreed `Done when:` command passes and each criterion has a test, a pull request over 400 changed lines asks you, and so does a commit that leaves in a debugger call or TODO or switches a checker off.

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

Ask for the change, such as "build PAY-12", and the agent first agrees with you in chat what you want, why, and the happy and failure paths. The same goes for a bug, such as "the export times out past 10k orders", or a refactor. Say "write a story for X" for a user story in the template, or "do a spike on X" for a throwaway experiment. The done check runs your repository's test command, such as `npm test`, `make test` or `pytest`. To run a different one, add a `Check:` line to `AGENTS.md`, such as ``Check: `make lint test` ``. More detail is in [plugins/sdlc](plugins/sdlc/README.md).

At session start, a hook also adds house rules for how the agent works with you, such as one decision per question and plain explanations. They are in [`plugins/sdlc/hooks/working-agreement.md`](plugins/sdlc/hooks/working-agreement.md). If you installed the old `working-agreement` plugin, uninstall it: `claude plugin uninstall working-agreement@sdlc-skills`.

MIT license.
