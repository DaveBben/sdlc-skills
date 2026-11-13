# Guide for agents

`sdlc-skills` is one plugin, `sdlc`, built on one rule: whoever made a change, someone else attacks it, and a machine decides when it is done. A session-start hook also adds house rules for how the agent works with the user.

Check: `python3 plugins/sdlc/hooks/guard.py --self-test`

## The test for every change

[docs/principles.md](docs/principles.md) is the owner's cheat sheet of 18 principles, and it says which ones the plugin enforces. Most principles are habits for the person, so they stay out of the plugin. Before adding anything, apply these tests in order:

1. **Can a hook, script or check enforce it?** Then put it in `plugins/sdlc/hooks/guard.py` with a self-test case, and write no instruction.
2. **Does a capable model already do it when asked?** Then leave it out.
3. **Does it beat a plain prompt?** Run `python3 tools/baseline.py`. A part that does not beat the `prompted` arm, a plain prompt plus one sentence of the plugin's rule, gets cut. Rerun it whenever a new model ships.

When an agent using the plugin fails, add a check that catches the failure. Do not add wording.

## Key files

- `plugins/sdlc/hooks/guard.py` is the 8 hooks in one script: test lock, done check, size cap, dependency gate, holdout guard, pull request cap, leftovers gate and silencer gate. `hooks.json` beside it registers the events.
- `skills/sdlc/` holds the 5 skills: `story` writes and critiques acceptance criteria, `spike` runs a throwaway experiment, `bug` reproduces a fault and finds why it escaped, `refactor` changes structure with every test unchanged, and `build` takes criteria to a pull request. `build/references/tests.md` holds how to write the failing tests. Edit a skill only there.
- **A skill as a stored prompt:** a skill also earns its place when it holds the owner's own conventions, which a capable model would follow but the owner would otherwise retype each time. Keep such a skill to those conventions.
- `skills/sdlc/agents/` holds the 6 subagent prompts: `plan-reviewer`, `test-challenger`, `implementer`, `reviewer`, `verifier` and `delegator`, which runs non-coding tasks in parallel. The skill describes each delegated step and never names an agent, because the harness picks the agent by its `description`. The holdout guard finds the implementer by its agent type, `sdlc:implementer`.
- `plugins/<plugin>/` is a thin Claude Code wrapper: a `.claude-plugin/plugin.json`, a README, and for `sdlc` the symlinks `skills` and `agents` into `skills/sdlc`. Do not replace the symlinks with real files.
- `plugins/sdlc/hooks/working-agreement.md` is the house rules, printed at session start. A skill's own rules win where they differ, so no skill repeats them.
- `tools/baseline.py` compares the plugin against a plain prompt on the tasks in `tools/tasks/`.
- `tools/trigger-gauge.py` checks that each skill and agent fires on its requests and stays quiet on others, with a target of 9 hits in 10 each. Rerun it after changing a `description`, and keep its held-out cases unlike any description's wording.
- `research/` is local and git-ignored. `research/design-history.md` holds the rationale for each design.

## Rules for changes

- **Skill paths** in `marketplace.json` are `./skills/<skill>`, relative to the plugin `source`, with no `..`.
- **Version:** keep each plugin's version in its `plugin.json` equal to its `marketplace.json` entry, and bump both together.
- **Runtime reach:** only `skills/` and the wrappers' `hooks/` reach an agent. This file, the READMEs, `docs/`, `research/` and `tools/` do not, so a term this repo coins is defined inside the skill that uses it.
- **Portable skills:** name a tool as an example, never as a requirement. The hooks are Claude Code's, and the skill must still read correctly without them.
- **Skill format:** follow the [Agent Skills specification](docs/agent-skills-spec.md). Lead the `description` with the trigger.
- **Wording:** write for the agent. Give it the knowledge it lacks, with no shouted words, no step-by-step procedure and no rule it would follow unprompted.
