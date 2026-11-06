---
name: design
description: "Use when a project, service or change spanning several stories must be designed or its design written down before its stories are built, or when the person has lost track of the design they were building toward, such as 'write a design doc', 'what was the design we settled on' or 'how should the new analyzer fit with the tracker': the person designs, the agent fills in the facts and critiques, and the doc is edited until building starts, then kept as the record."
license: MIT
metadata:
  version: "1.0.0"
---
# Design

A design doc says how a project, or a change spanning several stories, will be built and why, while changing it is still cheap. One story's design is a spec, by the `spec` skill; one decision a revert cannot undo is an ADR, by the `adr` skill.

* **None** when the problem has no real trade-off: say so and go to the `story` skill.
* **Size:** 1 to 3 pages. Past that, split the project.
* **Who writes what:** you fill in the template's headings and the repository's facts, each with its `file:line`. The goals, non-goals, design and each decision are the person's; you critique them. Mark each decision `Decided:`, `Assumed:` or `Open:`.
* **Status:** `Draft` while it is worked out, `Building` once its first story is built, `Built` when its last ships. Edit a Draft freely. From Building on, change only its status and links: a changed decision goes in a new ADR, or a new design doc that links back.

## Paths

* **Create:** [references/create.md](references/create.md).
* **Resume:** read the doc and the ADRs and stories it links, then show its `Open:` lines and what changed in the code since its `Updated:` date. Go on at the first open decision by create.md.
* **Review** one someone wrote against create.md's critique list. Report `<section>: <gap> — "<quoted text>" — <fix>`, then `Ready for stories` when none remain. Change nothing without its owner's yes.

## Where it lives

`docs/design/<slug>.md`, or the wiki the project already keeps design docs in. Each story it produces links it.
