---
name: spec
description: "Use first, before answering, whenever the person asks how an agreed story should be built or what its design, approach, endpoints, tables or contract should be, wants a design, plan or notes of theirs critiqued, coached or poked at, or asks anything about a spec, such as 'what am I missing in my approach' or 'is this spec too long': works through it with the person one decision at a time and attaches it to the story."
license: MIT
metadata:
  version: "1.0.0"
---
# Spec

A spec says how one agreed story gets built: the decisions, contracts, failure handling and rollout its criteria leave open. It never restates the story; it cites criteria by number, such as AC2.

## Size it to the story

Use risk-driven design. Estimate the lines of code the story produces, then pick the smallest size that holds:

* **None:** no section holds a decision or a risk, such as one module following the pattern beside it. Write `Spec: none, <reason>` on the story.
* **Short:** only the sections of [references/full.md](references/full.md) that hold a decision or a risk, a few lines each, and its `Promote before delete` list. It stays shorter than the code it produces: longer is a red flag, so cut it.
* **Full:** every section of full.md, where `N/A, <reason>` is a complete answer. Required for a story that changes a contract another team or outside client consumes, migrates existing data, or ships in stages behind a flag, once its code would run longer than a full spec.

## Paths

* **Create** one with the person: [references/create.md](references/create.md).
* **Review** a spec someone wrote: check it against the rules above and each section against full.md, then report `<section>: <gap> — "<quoted text>" — <fix>`, a gap the story owns as a question for the story, and `Ready to build` when none remain. Change nothing without its owner's yes to that finding.
* **Close** when the story closes: move each item on its `Promote before delete` list to its home, a decision record by the `adr` skill, tick it, then delete the spec.

## Where it lives

* **With a tracker:** one comment on the story's issue headed `## Spec`, edited in place, through the `tracker` skill.
* **Without one:** a `## Spec` block in `docs/stories/<slug>.md`.
