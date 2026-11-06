---
name: spec
description: "Use first, before answering, whenever the person asks how an agreed story should be built or what its approach, endpoints, tables or contract should be, wants their approach for one story critiqued, or asks anything about a spec, such as 'what am I missing in my approach' or 'is this spec too long': works through it with the person one decision at a time and attaches it to the story. Not for a design spanning several stories, which is a design doc."
license: MIT
metadata:
  version: "1.0.0"
---
# Spec

A spec says how one agreed story gets built: only the choices its criteria leave open. It cites criteria by number, such as AC2, and never restates them.

* **None by default:** write `Spec: none` on the story and build. Write one only when the story changes a contract another team or client calls, changes stored data or its schema, ships behind a flag or in stages, or leaves open a decision costly to reverse by the `adr` skill.
* **Size:** only the sections below that hold a choice, on one screen.

```markdown
## Spec

Decided: <choice> (AC<n>), because <reason>. Rejected: <alternative>. ADR: <link or none>
Open: <question>, <owner>, blocks <AC>
Contract: <each endpoint, message, event or schema added or changed: success, errors, what a client shows, who consumes it>. Promote: <its home, such as the OpenAPI file>
Data: <tables, keys, what happens to existing data>. Promote: the `Boundaries:` line of `AGENTS.md`, by the `onboard` skill, when it adds a store or changes who writes one
Rollout: <the flag and its off state, the steps, the rollback>

Promote before delete:
- [ ] <each Promote item>
```

`Decided:` lines also hold where a criterion is enforced, a failure no criterion states, and a budget such as latency, when each is a choice.

## Paths

* **Create** one with the person: [references/create.md](references/create.md).
* **Review** a spec someone wrote against the rules above. Report `<section>: <gap> — "<quoted text>" — <fix>`, a gap the story owns as a question for it, and `Ready to build` when none remain. Change nothing without its owner's yes.
* **Close** when the story closes: move each `Promote before delete` item to its home, a decision by the `adr` skill, tick it, then delete the spec.

## Where it lives

* **With a tracker:** one comment on the story's issue headed `## Spec`, edited in place, by the `tracker` skill.
* **Without one:** a `## Spec` block in `docs/stories/<slug>.md`.
