# Guide for agents

`sdlc-skills` is two plugins. `agentic-dev` is built on one rule: the person drives a loose loop (Frame, Explore, Build, Verify, Review), and a machine decides when it is done. A session-start hook also adds house rules for how the agent works with the user. `xp-templates` writes, reviews, splits, forecasts and files XP artifacts.

Definition of done: `python3 plugins/agentic-dev/hooks/guard.py --self-test`

## The test for every change

[docs/principles.md](docs/principles.md) is the owner's cheat sheet of 18 principles, and it says which ones the plugin enforces. Most principles are habits for the person, so they stay out of the plugin. Before adding anything, apply these tests in order:

0. **The premise:** a convention or template format the owner would otherwise retype deserves a skill; something that must happen every time deserves a hook; everything else is cut, or at most one line in the working agreement.
1. **Can a hook, script or check enforce it?** Then put it in `plugins/agentic-dev/hooks/guard.py` with a self-test case, and write no instruction.
2. **Does a capable model already do it when asked?** Then leave it out.
3. **Does it beat a plain prompt?** Run `python3 tools/baseline.py`. A part that does not beat the `prompted` arm, a plain prompt plus one sentence of the plugin's rule, gets cut. Rerun it whenever a new model ships.

When an agent using the plugin fails, add a check that catches the failure. Do not add wording.

## Key files

- `plugins/agentic-dev/hooks/guard.py` is the 11 hooks in one script: done check, size cap, dependency gate, pull request cap, leftovers gate, silencer gate, test-tamper gate, skill gate, grill gate, review gate and retro reminder. `hooks.json` beside it registers the events.
- `skills/agentic-dev/` holds 4 skills. `building` is the single entry for any change to code, a story or a chore. Its core is the grilling (silent assumptions, the walking skeleton, lifecycles, edge cases, failing integration points, one-way doors, the UAT); then it explores (a spike with `prototyping`), plans, builds test-first and finishes on a passing check. A story or bug report the person brings is its frame, whatever wrote it. `prototyping` answers one question with throwaway code in a scratch directory: no tests, clean code or what-ifs, then a finding and the code deleted. `reviewing` takes a finished change through one fresh review, a verification of each finding and test-first fixes of the blocking ones, within 3 rounds; it owns the review directory (`diff.patch`, `story.md`, `findings.md`) that its reviewer and verifier reference files read. `reflecting` reads the session of a finished non-trivial change against the loop and tells the person what to do next time. Edit a skill only there.
- **Artifacts are `xp-templates`:** `skills/xp-templates/` holds `story`, `spike`, `bug` and `tracker`: formats, review checks and, in `story`, an interview that draws a story out of the person; no building, no questions asked for a build, no hand-off that tells an agent how to code. Neither plugin depends on the other being installed.
- **Reviewer prompts are reference files, not agents:** `reviewing/references/reviewer.md` and `verifier.md`, and `building/references/design-review.md`. A skill launches each as a fresh general subagent on a named model, so the plugin ships no agents and nothing competes with a skill's trigger.
- `plugins/<plugin>/` is a thin Claude Code wrapper: a `.claude-plugin/plugin.json`, a README, and the symlink `skills` into `skills/<plugin>`. Do not replace the symlink with a real directory.
- `plugins/agentic-dev/hooks/working-agreement.md` is the house rules, printed at session start, with the Explain lines for teaching an idea. A skill's own rules win where they differ, so no skill repeats them.
- `tools/baseline.py` compares the plugin against a plain prompt on the tasks in `tools/tasks/`.
- `tools/trigger-gauge.py` checks that each skill fires on its requests and stays quiet on others, over the cases in `tools/trigger-cases.json` (generated, mined from real sessions, and cross-skill confusions; a case with `needs_context` is listed but not run), with a target of 9 hits in 10 each. Rerun it after changing a `description`, and keep its held-out cases unlike any description's wording.
- `research/` is local and git-ignored. `research/design-history.md` holds the rationale for each design.

## Rules for changes

- **Skill paths** in `marketplace.json` are `./skills/<skill>`, relative to the plugin `source`, with no `..`.
- **Version:** keep each plugin's version in its `plugin.json` equal to its `marketplace.json` entry, and bump both together.
- **Runtime reach:** only `skills/` and the wrappers' `hooks/` reach an agent. This file, the READMEs, `docs/`, `research/` and `tools/` do not, so a term this repo coins is defined inside the skill that uses it.
- **Portable skills:** name a tool as an example, never as a requirement. The hooks are Claude Code's, and the skill must still read correctly without them.
- **Skill format:** follow the [Agent Skills specification](docs/agent-skills-spec.md). Lead the `description` with the trigger.
- **Wording:** write for the agent. Give it the knowledge it lacks, with no shouted words, no step-by-step procedure and no rule it would follow unprompted.
