# Guide for agents

This file explains how to change `sdlc-skills` without breaking a plugin, a skill, or the way agents install them.

## What this repo contains

`sdlc-skills` is one plugin, `xp`, named for Extreme Programming, which decides what gets built and turns it into a reviewed pull request. An optional second, `working-agreement`, has no skills: its one hook adds house rules for how the agent works with the user. The skills are written in Markdown and take a software change from a request to a verified production change.

Skills work with any skills-compatible agent. Keep them portable. Do not write instructions that limit a skill to one agent's tools; name a tool as an example, not a requirement.

## Key files

- `skills/<plugin>/<skill>/SKILL.md` is the source of truth for each of the 12 skills, with its reference files one level deep in `references/` beside it: `xp` holds `story`, `spike`, `bug`, `chore`, `tracker`, `adr`, `spec`, `build`, `red-tests`, `review`, `refactor` and `onboard`. This is the only place to edit a skill.
- `skills/xp/build/` is the one build-and-ship procedure, for a story, a bug fix, a chore or a plain request. Its `SKILL.md` holds what both modes share; `references/pair.md` and `references/autopilot.md` hold each mode's steps; `references/unattended.md` holds the contacts, polling and scheduled pick, read only with no person in the session; `references/bug.md` and `references/chore.md` say how a bug fix or a chore differs; Autopilot's design is the story's spec and its own `Decided:` lines. The planning skills end at an agreed ticket and hand it to `build`.
- `skills/xp/agents/` holds the six subagent prompts: `test-challenger`, launched by `red-tests` and by `build`'s pair mode; `implementer`, launched by `build`'s autopilot; `mapper`, launched by `bug`, `adr` and `tracker` to read more than 10 items; and `router`, `reviewer` and `verifier`, launched by `review`. There is no refactorer agent: whoever writes the code refactors it inside its test-first loop. Skills describe each delegated step and never name an agent; the harness picks the agent by its `description`, which `tools/agent-gauge.py` scores. Edit agent files only here.
- `skills/xp/red-tests/scripts/locked_tests.py` and `skills/xp/review/scripts/reading_floor.py` check by script what an agent would otherwise judge alone: each change to a locked test, and the hunks a person must read. Each runs its own `--self-test`.
- `plugins/<plugin>/` is a thin Claude Code wrapper per plugin: a `.claude-plugin/plugin.json`, a README and a `skills` symlink to `../../skills/<plugin>`; `xp`'s also has an `agents` symlink to `../../skills/xp/agents`. The symlinks mean one copy, not two; do not replace them with real files. Claude Code follows a symlink only when it is the `agents` folder itself, not a symlinked subfolder or file inside it.
- `plugins/working-agreement/hooks/working-agreement.md` is printed at session start by its `hooks.json`; it is opt-in because not every user wants it, so no other plugin may depend on it or repeat it. Edit the rules only there.
- `plugins/xp/hooks/hooks.json` runs two hooks at session start: adr's `scripts/adr_index.py`, which lists each ADR in force by title and path and prints nothing when `docs/adr/` is absent, and `hooks/route.md`, the routing list that sends each change request to its skill. They live in the wrapper because no skill is loaded at session start. Edit the routing only in `route.md`; no skill repeats it. The `AGENTS.md` size cap is not a plugin hook: `onboard` installs `scripts/size_guard.py` and the entries in `scripts/size-guard-settings.json` into a repository only on the user's yes.
- `.claude-plugin/marketplace.json` lets users add this repo as a Claude marketplace and lists the plugins and their skills.
- `README.md` is the one-screen index: what the skills do, how to install and use them. Each `plugins/<plugin>/README.md` is that plugin's one-screen pitch: what runs in a session and one example traced.
- `research/` is local and git-ignored, never published: source material and `design-history.md`, the rationale for each design and the version history. It never loads into an agent. `tools/` holds the trigger, routing and agent gauges.

## Rules for changes

- **Skill paths** in `marketplace.json` must be `./skills/<skill>`, relative to the plugin `source`, with no `..`. The schema forbids `..`; the symlink is what reaches the canonical files.
- **Version:** keep each plugin's version in its `plugin.json` equal to its `marketplace.json` entry, and bump both together.
- **A plugin's `name`** is its slash-command prefix, so a skill invokes as `/<plugin>:<skill>`, such as `/xp:story`. Renaming one changes its `plugin.json`, `marketplace.json`, its README and the root README together.
- **No reach across plugins:** an installed plugin cannot see another plugin's folder, so no skill points at another plugin's files by relative path. A skill in another plugin is named as "where the `X` skill is installed, …; else …".
- **One place for shared rules:** the locked-tests and signature-commit definitions live only in `red-tests`' `SKILL.md`; other skills and agents use the terms by name or restate only the part they act on.
- **Runtime reach:** nothing outside `skills/` and the wrappers' `hooks/` reaches an agent, not this file, the READMEs, `research/` or `tools/`. A term this repo coins is defined inside the skill that uses it. A canonical name from the field is used bare, with an author's name only where it is part of the name, such as Lawrence's story-splitting patterns.

## Writing a skill

Every skill must follow the [Agent Skills specification](docs/agent-skills-spec.md): a `SKILL.md` with valid `name` and `description` frontmatter, references one level deep, kept under 500 lines. That doc is the format contract; the rules below are how this repo writes within it.

A skill orients a capable agent; it is not a step-by-step procedure. Assume the agent is smart and give it the knowledge and conventions it lacks, not instructions it already knows.

- Write for the agent, not a human reader.
- Prefer precise terms over slang or vague description; agents misread ambiguity and human jargon.
- Keep the YAML metadata valid, and lead its `description` with the trigger.
- Treat the prose below the metadata as the product.
- Prefer one short, clear instruction over another exception or repeated explanation.
