---
name: spec
description: "Use first, before answering, whenever the person asks how an agreed story should be built or what its design, approach, endpoints, tables or contract should be, wants a design, plan or notes of theirs critiqued, coached or poked at, or asks anything about a spec, such as 'what am I missing in my approach' or 'is this spec too long': works through it with the person one decision at a time and attaches it to the story."
license: MIT
metadata:
  version: "1.0.0"
---
# Spec

A spec says how one agreed story gets built: the decisions, contracts, failure handling and rollout its criteria leave open. It cites criteria by number, such as AC2, and never restates them.

## Size it to the story

Risk-driven design: estimate the lines of code the story produces, then pick the smallest size that holds:

* **None:** no section holds a decision or a risk. Write `Spec: none, <reason>` on the story.
* **Short:** only the sections of [references/full.md](references/full.md) that hold a decision or a risk, and its `Promote before delete` list, shorter than the code it produces.
* **Full:** every section of full.md, where `N/A, <reason>` is a complete answer. Required for a story that changes a contract another team or outside client consumes, migrates existing data, or ships in stages behind a flag, once its code would run longer than a full spec.

## Paths

* **Create** one with the person: [references/create.md](references/create.md).
* **Review** a spec someone wrote against the rules above and full.md. Report `<section>: <gap> — "<quoted text>" — <fix>`, a gap the story owns as a question for it, and `Ready to build` when none remain. Change nothing without its owner's yes.
* **Close** when the story closes: move each `Promote before delete` item to its home, a decision by the `adr` skill, tick it, then delete the spec.

## Where it lives

* **With a tracker:** one comment on the story's issue headed `## Spec`, edited in place, by the `tracker` skill.
* **Without one:** a `## Spec` block in `docs/stories/<slug>.md`.
