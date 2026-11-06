---
name: design
description: "Use when a project, service or change spanning several stories must be designed or its design written down before its stories are built, or when the person has lost track of the design they were building toward, such as 'write a design doc', 'what was the design we settled on' or 'design the billing migration before we split it into stories': the person designs and the agent fills in the facts and critiques. Not for one story's design, which is a spec."
license: MIT
metadata:
  version: "1.0.0"
---
# Design

A design doc says how a project, or a change spanning several stories, will be built and why, while changing it is still cheap. One story's design is a spec, by the `spec` skill; one decision costly to reverse is an ADR, by the `adr` skill.

* **None** unless a decision costly to reverse binds more than one story. Otherwise say so: one story's design goes to the `spec` skill, a change with no trade-off to `story` or `build`.
* **Size:** under 100 lines, with what and why in its first 3. Past that, move per-story detail to specs.
* **Who writes what:** you fill in the template's headings and the repository's facts, each with its `file:line`. The goals, non-goals, design and each decision are the person's; you critique them. Mark each decision `Decided:`, `Assumed:` or `Open:`.
* **Status:** `Draft` until its first story is written, then `Agreed`. Edit it while any of its stories is unbuilt; afterwards change only links. A changed costly decision gets a new ADR.
* **Built:** when its last story ships, update `AGENTS.md`'s `Boundaries:` line by the `onboard` skill where the Design section adds a system or store or changes who writes one.

## Paths

* **Create:** [references/create.md](references/create.md).
* **Resume:** read the doc and the ADRs and stories it links, then show its `Open:` lines and each change since its `Updated:` date that contradicts a `Decided:` or `Assumed:` line, with its `file:line`. Go on at the first open decision by create.md.
* **Review** one someone wrote against create.md's critique list. Report `<section>: <gap> — "<quoted text>" — <fix>`, then `Ready for stories` when none remain. Change nothing without its owner's yes.

## Where it lives

`docs/design/<slug>.md`, or the wiki the project already keeps design docs in. Each story it produces links it.
