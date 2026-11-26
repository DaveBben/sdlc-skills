# Guide for agents

`sdlc-skills` is two plugins, soon one. `agentic-dev` is built on two rules: the hard part is the specification, so the agent interviews the person until nothing is ambiguous; and the agent that writes the code never sees the check that decides it is done. A session-start hook also adds house rules for how the agent works with the user. `xp-templates` holds only `spike` until it is redone.

Definition of done: `python3 plugins/agentic-dev/hooks/guard.py --self-test`

## The test for every change

[docs/principles.md](docs/principles.md) is the owner's cheat sheet of 18 principles, and it says which ones the plugin enforces. Most principles are habits for the person, so they stay out of the plugin. Before adding anything, apply these tests in order:

0. **The premise:** a convention or template format the owner would otherwise retype deserves a skill; something that must happen every time deserves a hook; everything else is cut, or at most one line in the working agreement.
1. **Can a hook, script or check enforce it?** Then put it in `plugins/agentic-dev/hooks/guard.py` with a self-test case, and write no instruction.
2. **Does a capable model already do it when asked?** Then leave it out.
3. **Does it beat a plain prompt?** Run `python3 tools/baseline.py`. A part that does not beat the `prompted` arm, a plain prompt plus one sentence of the plugin's rule, gets cut. Rerun it whenever a new model ships.

When an agent using the plugin fails, add a check that catches the failure. Do not add wording.

## Key files

- `plugins/agentic-dev/hooks/guard.py` is the 10 hooks in one script: done check, size cap, dependency gate, leftovers gate, silencer gate, test-tamper gate, check gate, slice cap, skill gate and review gate. `hooks.json` beside it registers the events.
- `skills/agentic-dev/` holds 3 skills. `task` builds a change whose done one deterministic check proves: at most one clarifying question, a done check written outside the worktree under the git directory's `task-checks/` and seen failing, a subagent that makes it pass from the simplest solution up without ever seeing the check (the check gate hook enforces that), and a commit to a branch. `story` takes a feature or a whole product: it interviews the person into a record in the OS temp directory, confirms the criteria in plain language, splits them into vertical slices with a walking skeleton first, has a subagent verify them against the record, and files them; or it builds one story: a reviewed plan, design choices settled with the person, hidden failing tests from a test-writer subagent, slices of at most 200 lines each built as a task on a `slice/` branch and reviewed, a final review and verification, a merge request watched up to 24 hours, and the UAT. `prototyping` answers one question with throwaway code in a scratch directory: no tests, clean code or what-ifs, then a finding and the code deleted. Edit a skill only there.
- `skills/xp-templates/` holds `spike` alone. Neither plugin depends on the other being installed.
- **Reviewer and verifier are agents:** `plugins/agentic-dev/agents/reviewer.md` and `verifier.md`, which read the review directory (`diff.patch`, `story.md`, `findings.md`) that `story` writes. The plan reviewer and the story verifier are reference files in `story/references/`, launched as fresh general subagents.
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
