# Guide for agents

`sdlc-skills` is one plugin, `sdlc`, built on one rule: whoever made a change, someone else attacks it, and a machine decides when it is done. An optional second plugin, `working-agreement`, has no skills: its one hook adds house rules for how the agent works with the user.

Check: `python3 plugins/sdlc/hooks/guard.py --self-test`

## The test for every change

[docs/principles.md](docs/principles.md) holds the 18 principles and where each one lives. Before adding anything, apply them in this order:

1. **Can a hook, script or check enforce it?** Then put it in `plugins/sdlc/hooks/guard.py` with a self-test case, and write no instruction.
2. **Does a capable model already do it when asked?** Then leave it out.
3. **Does it beat a plain prompt?** Run `python3 tools/baseline.py`. A part that does not beat the `plain` arm gets cut. Rerun it whenever a new model ships.

When an agent using the plugin fails, add a check that catches the failure. Do not add wording.

## Key files

- `plugins/sdlc/hooks/guard.py` is the 4 hooks in one script: test lock, done check, size cap and dependency gate. `hooks.json` beside it registers the events.
- `skills/sdlc/build/SKILL.md`, `skills/sdlc/onboard/SKILL.md` and `skills/sdlc/principles/SKILL.md` are the only skills. Edit a skill only there.
- `skills/sdlc/agents/` holds the 3 subagent prompts: `critic`, `reviewer` and `verifier`. Skills describe each delegated step and never name an agent, because the harness picks the agent by its `description`.
- `plugins/<plugin>/` is a thin Claude Code wrapper: a `.claude-plugin/plugin.json`, a README, and for `sdlc` the symlinks `skills` and `agents` into `skills/sdlc`. Do not replace the symlinks with real files.
- `plugins/working-agreement/hooks/working-agreement.md` is opt-in, so no other plugin may depend on it or repeat it.
- `tools/baseline.py` compares the plugin against a plain prompt on the tasks in `tools/tasks/`.
- `research/` is local and git-ignored. `research/design-history.md` holds the rationale for each design.

## Rules for changes

- **Skill paths** in `marketplace.json` are `./skills/<skill>`, relative to the plugin `source`, with no `..`.
- **Version:** keep each plugin's version in its `plugin.json` equal to its `marketplace.json` entry, and bump both together.
- **Runtime reach:** only `skills/` and the wrappers' `hooks/` reach an agent. This file, the READMEs, `docs/`, `research/` and `tools/` do not, so a term this repo coins is defined inside the skill that uses it.
- **Portable skills:** name a tool as an example, never as a requirement. The hooks are Claude Code's, and the skills must still read correctly without them.
- **Skill format:** follow the [Agent Skills specification](docs/agent-skills-spec.md). Lead the `description` with the trigger.
- **Wording:** write for the agent. Give it the knowledge it lacks, with no shouted words, no step-by-step procedure and no rule it would follow unprompted.
