# sdlc-skills

One plugin for coding agents, built on one rule: you drive a loose loop, Frame, Explore, Plan, Build, Verify, Review, and a machine decides when it is done.

## What you get

- **Framing:** the agent grills you one question at a time when a change is vague, and looks first where gaps hide, such as one item where the job meets many.
- **A retro after each non-trivial change:** a fresh agent reads the session and tells you, with cases from it, what to do next time to get better output.
- **Fresh agents on call:** one reviews a design, one reviews the diff, and one proves or drops each finding.
- **Hooks enforce the rest:** the definition of done, every test and the linter, must pass before the agent stops, first-seen packages ask you, `AGENTS.md` stays under 100 lines, a pull request over 400 changed lines asks you, and so does a commit that leaves in a debugger call or TODO or switches a checker off.

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

Ask for the change as you would a colleague. When it is vague, the agent asks you one question at a time until you agree what done looks like; then you plan, build and verify it in small steps. When the change is finished, the agent runs a retro on the session, or say "run a retro". The definition of done is your repository's own test and lint commands, such as `npm test && npm run lint`. To name it yourself, add a line to `AGENTS.md`, such as ``Definition of done: `make lint test` ``; an older `Check:` line still works. More detail is in [plugins/sdlc](plugins/sdlc/README.md).

At session start, a hook also adds house rules for how the agent works with you, such as one decision per question and plain explanations. They are in [`plugins/sdlc/hooks/working-agreement.md`](plugins/sdlc/hooks/working-agreement.md). If you installed the old `working-agreement` plugin, uninstall it: `claude plugin uninstall working-agreement@sdlc-skills`.

MIT license.
