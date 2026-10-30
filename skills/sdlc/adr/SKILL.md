---
name: adr
description: "Use when a decision must be recorded, written up or documented, or one costly to reverse changed or checked, such as 'record why we chose X', 'we're going with X instead of Y' or 'review our ADRs': writes one decision record with the user's reasons, the rejected alternatives and a check that detects a breach."
license: MIT
metadata:
  version: "1.0.0"
---
# ADR

An ADR records one decision costly to reverse, one a revert cannot undo, in one Markdown file: what was decided, why, and what it gave up. Write it when the decision is made.

* **Where:** `docs/adr/<decision-name>.md`, short and kebab-case, using the term from `docs/glossary.md` where there is one. A decision across repositories: ask the user where it goes every time, offering as an equal option the home a `Cross-repository ADRs:` line in an affected repository's `AGENTS.md` names, and add that line to each affected repository.
* **In force:** committed, with no `Superseded by:` line and no `Status:` of rejected or deprecated. Read the titles of those in force before writing.
* **Reasons are the user's:** never record a reason the user has not given, confirmed or deferred to. One a person wrote down, such as in a spec, counts: quote it. With no user in the session, ask on the work's issue through the `tracker` skill.
* **Commit each ADR alone** on the current branch; on the default branch, create `adr/<decision-name>` first.

## Record a decision

By [references/create.md](references/create.md).

## Supersede a decision

An accepted ADR is never rewritten; fix only a broken link in place. A changed, reversed or dropped decision gets a new ADR by create.md with `**Supersedes:** <old path>`, and the old one gains `**Superseded by:** <new path>` and nothing else. The new ADR's fitness function says whether the old one is replaced, kept or removed; change that test with the code change that breaks it, not in the ADR's commit.

## Review ADRs

Read those the user names, else every one in force. Past 10, have fresh subagents in parallel map them to one sourced row each, 5 ADRs per subagent with the code root, for the decision in one sentence, the components it touches, its `Supersedes:` and `Superseded by:` lines, and each finding below that needs only that ADR. Find contradictions and broken chains across the rows yourself, and read each quote before keeping its finding. Change nothing without the user's yes to that finding. Keep a finding only when quoted text or a `file:line` shows it:

* **No reasons,** or a why that restates the decision, or no rejected alternative.
* **No working fitness function:** none, or a test or rule that does not exist.
* **A rejected alternative** back in the code.
* **Stale:** the code no longer does what it decides, or its `Revisit when` has happened.
* **Contradiction:** two ADRs in force decide the same question differently.
* **Broken chain:** a `Supersedes:` or `Superseded by:` that names a missing file or is not answered by its pair.
* **Not one ADR:** several decisions in one file, or one that is not an ADR by create.md.

```text
<ADR path>: <finding> — "<quoted text>" or <file:line> — <what to change>
Sound: <ADRs with no finding>
```
