# Guide for agents

`sdlc-skills` is one plugin, `agentic-dev`, built on one rule: the person drives a loose loop (Frame, Explore, Build, Verify, Review), and a machine decides when it is done. A session-start hook also adds house rules for how the agent works with the user.

Definition of done: `python3 plugins/agentic-dev/hooks/guard.py --self-test`

## The test for every change

[docs/principles.md](docs/principles.md) is the owner's cheat sheet of 18 principles, and it says which ones the plugin enforces. Most principles are habits for the person, so they stay out of the plugin. Before adding anything, apply these tests in order:

1. **Can a hook, script or check enforce it?** Then put it in `plugins/agentic-dev/hooks/guard.py` with a self-test case, and write no instruction.
2. **Does a capable model already do it when asked?** Then leave it out.
3. **Does it beat a plain prompt?** Run `python3 tools/baseline.py`. A part that does not beat the `prompted` arm, a plain prompt plus one sentence of the plugin's rule, gets cut. Rerun it whenever a new model ships.

When an agent using the plugin fails, add a check that catches the failure. Do not add wording.

## Key files

- `plugins/agentic-dev/hooks/guard.py` is the 9 hooks in one script: done check, size cap, dependency gate, pull request cap, leftovers gate, silencer gate, test-tamper gate, plan gate and retro reminder. `hooks.json` beside it registers the events.
- `skills/agentic-dev/` holds 9 skills. `story` is the entry for any change to code: every change starts as a user story (who it is for, why, acceptance criteria, how a story fails), then the person chooses to build it now with `building` (the house rules for changing code) or write it down for later; `explaining` holds how to teach an idea; both were moved out of the working agreement so they load only when needed. `reviewing` takes a finished change through one fresh review, a verification of each finding and test-first fixes of the blocking ones, within 3 rounds; it owns the review directory (`diff.patch`, `story.md`, `findings.md`) that its reviewer and verifier reference files read. `reflecting` reads the session of a finished non-trivial change against the loop (Frame, Explore, Build, Verify, Review) and tells the person what to do next time. `chore` takes a change no user would notice: one `Done when:` line, the explore step, spikes run now or filed, then `building`. `tracker` reads and writes the issue tracker for the others, one labelled issue per item, blocked by the tracker's own relation. `story`, `bug` and `spike` never build: a story's criteria become the build's done-check and the review's `story.md`; a bug report's reproduction is the build's first failing check; a spike is the Explore step run as a throwaway experiment. The loop itself lives in the working agreement's Frame lines and in the person's head, not in a skill. Edit a skill only there.
- **A skill as a stored prompt:** a skill also earns its place when it holds the owner's own conventions, which a capable model would follow but the owner would otherwise retype each time. Keep such a skill to those conventions.
- **Reviewer prompts are reference files, not agents:** `reviewing/references/reviewer.md` and `verifier.md`, and `building/references/design-review.md`. A skill launches each as a fresh general subagent on a named model, so the plugin ships no agents and nothing competes with a skill's trigger.
- `plugins/<plugin>/` is a thin Claude Code wrapper: a `.claude-plugin/plugin.json`, a README, and for `agentic-dev` the symlink `skills` into `skills/agentic-dev`. Do not replace the symlink with a real directory.
- `plugins/agentic-dev/hooks/working-agreement.md` is the house rules, printed at session start. A skill's own rules win where they differ, so no skill repeats them.
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
