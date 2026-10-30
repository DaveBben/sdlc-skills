---
name: onboard
description: "Use when a repository's AGENTS.md or CLAUDE.md must be written, trimmed or reviewed, or an agent must orient itself, such as 'write AGENTS.md', 'my CLAUDE.md is too long' or 'orient yourself': keeps only what an agent cannot learn from the repository."
license: MIT
metadata:
  version: "1.0.0"
---
# Onboard

`AGENTS.md` at the repository root loads into every session. Keep a line only when deleting it would cause a mistake nothing else in the repository prevents.

## What goes in

* **Boundaries:** a `Boundaries:` line that draws the system on one page: each system, store and repository the product reads, writes or runs inside, in the order data flows, the repository that owns each step, and who writes each store it reads. When it outgrows 5 lines, stop and redraw it with the user before the next story.
* **Project tracker:** the issue tracker's URL, when the team uses one.
* **Commands** the repository does not make obvious, exact and copy-pasteable:
  * `Check:` runs at turn end, `Full check:` before a pull request, `Setup:` the install step a fresh checkout needs, and `Scheduled check:` the slow check a scheduled job runs.
  * How to run one test, and tool choices the agent would get wrong, such as "run Python through `uv run`; never `pip install`".
* **Lines only a person writes:** `Build:`, the standing choice of pair mode or autopilot for the paths it names, such as `Build: pair for src/billing; otherwise autopilot`; and `Sensitive:`, the paths a person reads in every review, such as `Sensitive: src/billing/, migrations/`. Never draft or propose either. When `Sensitive:` is missing, ask once which paths, with no suggestions.
* **Constraints no program checks,** each as its mechanism and what breaks: "Never hold a worker longer than one HTTP round trip; the pool has 5 and a full pool returns 502 to every user", not "keep the pool safe".
* **Traps,** one line each, such as a file changed only through its generator, or a test that already fails on main.
* **Pointers:** a document the agent would not find, and when to read it, such as `Cross-repository ADRs:` or `docs/glossary.md`, read before naming code or tests.

Keep the `Check:`, `Full check:`, `Setup:`, `Scheduled check:`, `Build:`, `Sensitive:` and `Cross-repository ADRs:` lines as found, even where the README repeats one.

## What stays out

* **What a check enforces,** such as formatter, lint and type rules. A rule a program could check but none does: propose the check, and keep the line until one holds it.
* **What the repository already says:** its purpose, stack, directory map, features and architecture past the `Boundaries:` line.
* **Session state:** plans, handoff notes, status and superseded designs. The branch, the issues and the PRD hold them; offer to delete any found.

Order the file `Boundaries:`, the tracker, then only the headings with content: Commands, Constraints, Traps, Pointers. A module's conventions go in a nested `AGENTS.md`. Link `CLAUDE.md`, and any other instructions-file name the repository uses, to `AGENTS.md`.

## Write or trim it

1. **Read** the existing `AGENTS.md` and any real `CLAUDE.md` whole, and run each command once. Report a failing `Check:` or `Full check:` as a trap; drop any other command that fails.
2. **Ask** each existing line you would move to a check or drop as its own question, as equals, then only the questions the repository cannot answer. Ask about response time, locales, browsers and devices, or regulations such as HIPAA or PCI only when the repository shows they apply, and write each yes as a constraint with its number.
3. **Rewrite** the whole file by the answers and these rules rather than append, and replace a real `CLAUDE.md` with the symlink.
4. **Size cap,** only on the user's yes, where the agent runs Claude Code hooks: copy [scripts/size_guard.py](scripts/size_guard.py) to `.claude/hooks/` and merge [scripts/size-guard-settings.json](scripts/size-guard-settings.json) into `.claude/settings.json`. It holds every `AGENTS.md` and `CLAUDE.md` to 100 lines and 8 KB.

## Orient or review

Report the commands, constraints and traps in one message. On a review, also list each finding, quoting its line: a line that belongs out, a command that does not run, or a constraint with no mechanism; otherwise give their count and offer them. Rewrite nothing unless the user accepts a finding. With no `AGENTS.md`, offer to write one. With no check command, ask for one and record it as a `Check:` line.
