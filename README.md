# sdlc-skills

One plugin for coding agents, built on one rule: whoever made a change, someone else attacks it, and a machine decides when it is done.

## What you get

- **You decide done:** before any work, the agent agrees with you in chat what you want and why, pushes back when there is a cheaper way, and agrees a few criteria that matter for how it will be used. The agent that builds never defines done.
- **You design:** the agent coaches rather than hands you the design, bringing in one option you may not know at a time. Say "just build it" to skip that.
- **Tests come first:** failing tests from your examples, committed before any code; mutation testing finds the weak ones.
- **Fresh agents attack the work:** one implements, one reviews the diff, and one proves or drops each finding before you see it.
- **Hooks enforce the rest:** the definition of done, every test and the linter, must pass before the agent stops, first-seen packages ask you, `AGENTS.md` stays under 100 lines, a push, pull request or merge is refused until it passes again and each criterion has a test, a pull request over 400 changed lines asks you, and so does a commit that leaves in a debugger call or TODO or switches a checker off.

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

Ask for the change, such as "build PAY-12", and the agent first agrees with you in chat what you want, why, and one criterion per rule the change must hold. The same goes for a bug, such as "the export times out past 10k orders", or a refactor. Say "write a story for X" or "file a bug for later" to write work down for later, or "do a spike on X" for a throwaway experiment. To merge straight into main without a pull request, as in a personal repository, add `Ship: merge` to `AGENTS.md`. With a `Deploy:` line there too, the agent deploys after the merge and smoke-tests each criterion. The definition of done is your repository's own test and lint commands, such as `npm test && npm run lint`. To name it yourself, add a line to `AGENTS.md`, such as ``Definition of done: `make lint test` ``; an older `Check:` line still works. More detail is in [plugins/sdlc](plugins/sdlc/README.md).

At session start, a hook also adds house rules for how the agent works with you, such as one decision per question and plain explanations. They are in [`plugins/sdlc/hooks/working-agreement.md`](plugins/sdlc/hooks/working-agreement.md). If you installed the old `working-agreement` plugin, uninstall it: `claude plugin uninstall working-agreement@sdlc-skills`.

MIT license.
