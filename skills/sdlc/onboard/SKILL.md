---
name: onboard
description: "Use when a repository is set up for work with an agent, or its AGENTS.md or CLAUDE.md is written, trimmed or reviewed, such as 'set this repo up', 'write AGENTS.md', 'my CLAUDE.md is too long' or 'add a check command': the person writes a short AGENTS.md, and the agent sets up the check that decides done, mutation testing, property-based tests and a sandbox."
license: MIT
metadata:
  version: "2.0.0"
---
# Onboard

Set up the machine checks that an instruction cannot guarantee, and keep `AGENTS.md` to what no check can hold. Prefer a hook, script, linter, type checker or CI job to a written rule. When the agent fails at something, add a check that catches it and leave the instructions alone.

## AGENTS.md

The person writes it. You supply facts from the repository with their `file:line`, and critique what they write. Never generate it whole. Keep a line only when deleting it would cause a mistake that nothing else in the repository prevents. A hook caps the file at 100 lines and 8 KB.

* **`Check:`** the command that decides when work is done, in backticks: fast, deterministic, and non-zero on failure. Usually the type checker, the linter and the tests the change touches. A hook runs it whenever the agent stops with changed files. A session runs only the command it started with, so a changed line takes effect in the next session. Run it once before recording it.
* **`Full check:`** the slow suite that runs before a pull request.
* **`Mutation:`** the mutation-testing command for a set of changed files.
* **`Build:`** the person's standing choice of who authors, such as `Build: learn for src/billing, otherwise delegate`. Only the person writes it.
* **Constraints that no program checks:** each as its mechanism and what breaks, such as "the pool has 5 workers, and a full pool returns 502 to every user".
* **Traps and pointers:** one line each.

Leave out what a check enforces, what the repository already shows, and session state such as plans and status. Link `CLAUDE.md` to `AGENTS.md`.

## Harder-to-game checks

Agents write tests that pass without proving much. Offer each of these once, and install it only on the person's yes, because each adds a development dependency.

* **Mutation testing:** install the tool the language has, such as mutmut for Python, Stryker for JavaScript and TypeScript, cargo-mutants for Rust or PIT for Java. Scope the run to changed files so it finishes in minutes, and record the command as the `Mutation:` line.
* **Property-based tests:** where the code has parsers, serializers, money arithmetic or any rule over a range of inputs, install the library the language has, such as Hypothesis, fast-check or proptest, and write one property as the example to copy.

## Sandbox

Offer to run the agent in a sandbox that limits network egress and approves commands inside it automatically, in place of permission prompts. In Claude Code that is this block in `.claude/settings.json`, with the domains the build needs:

```json
{"sandbox": {"enabled": true, "autoAllowBashIfSandboxed": true, "network": {"allowedDomains": ["github.com"]}}}
```

## Review an existing file

Report each line that belongs out, each command that fails when run, and each constraint with no mechanism, quoting the line. Change nothing until the person accepts a finding.
