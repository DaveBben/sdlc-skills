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

* **Boundaries:** a `Boundaries:` line: each system, store and repository the product reads, writes or runs inside, in data-flow order, who owns each step and who writes each store it reads. Draft the systems and stores from the code, giving the user each one's `file:line`; the user names each owner. Edit it when a system, store or owner is added, removed or changes. Past 5 lines, or about 10,000 lines of code, move it to a one-page `docs/ARCHITECTURE.md`, a codemap, its invariants and at most one diagram, leave a Pointer, and note the move.
* **Project tracker:** the issue tracker's URL, when the team uses one.
* **Commands** the repository does not make obvious, exact and copy-pasteable:
  * `Check:` runs at turn end, `Full check:` before a pull request, `Setup:` the install step a fresh checkout needs, and `Scheduled check:` the slow check a scheduled job runs.
  * How to run one test, and tool choices the agent would get wrong.
* **Lines only a person writes:** `Build:`, the standing choice of pairing or autopilot for the paths it names, such as `Build: pair for src/billing; otherwise autopilot`; and `Sensitive:`, the paths a person reads in every review, such as `Sensitive: src/billing/, migrations/`. Never draft or propose either. When `Sensitive:` is missing, ask once which paths, with no suggestions.
* **Constraints no program checks,** each as its mechanism and what breaks: "the pool has 5 workers and a full pool returns 502 to every user", not "keep the pool safe".
* **Traps,** one line each.
* **Pointers:** a document the agent would not find, and when to read it, such as `Cross-repository ADRs:` or `docs/glossary.md`, read before naming code or tests.

Keep the `Check:`, `Full check:`, `Setup:`, `Scheduled check:`, `Build:`, `Sensitive:` and `Cross-repository ADRs:` lines as found, even where the README repeats one.

## What stays out

* **What a check enforces,** such as formatter, lint and type rules. A rule a program could check but none does: propose the check, and keep the line until one holds it.
* **What the repository already says,** such as its stack and directory map.
* **Session state:** plans, handoff notes, status and superseded designs. Delete any found and note it; on a review, list it as a finding.

Order the file `Boundaries:`, the tracker, then only the headings with content: Commands, Constraints, Traps, Pointers. A module's conventions go in a nested `AGENTS.md`. Link `CLAUDE.md`, and any other instructions-file name the repository uses, to `AGENTS.md`.

## Write or trim it

1. **Read** the existing `AGENTS.md` and any real `CLAUDE.md` whole, and run each command once. Report a failing `Check:` or `Full check:` as a trap and tell the user it fails; drop any other command that fails.
2. **Note** in one message each line you move to a check or drop, with its reason, and each dropped command with its error, and go on; ask in that message only what the repository cannot answer, such as owners or `Sensitive:`.
3. **Rewrite** the whole file, never append, and replace a real `CLAUDE.md` with the symlink.
4. **Size cap,** only on the user's yes, where the agent runs Claude Code hooks: copy [scripts/size_guard.py](scripts/size_guard.py) to `.claude/hooks/` and merge [scripts/size-guard-settings.json](scripts/size-guard-settings.json) into `.claude/settings.json`. It holds every `AGENTS.md` and `CLAUDE.md` to 100 lines and 8 KB.

## Orient or review

Report the commands, constraints and traps in one message. On a review, also list each finding, quoting its line: a line that belongs out, a command that does not run, or a constraint with no mechanism. Rewrite nothing unless the user accepts a finding. With no `AGENTS.md`, offer to write one. With no check command, ask once, giving the command you would run from the build files, and record the answer as a `Check:` line.
