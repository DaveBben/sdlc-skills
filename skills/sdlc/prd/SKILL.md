---
name: prd
description: "Use at the start of a new product, and whenever a product requirements document (PRD) or the product's problem, users, goal, non-goals or success metric are written, reviewed or changed, such as 'write a PRD', 'what are we building and why', 'review our PRD' or 'we're dropping a user group': the person writes one short PRD and the agent critiques it, as the north star each story is checked against. Not for a single feature, which is a story."
license: MIT
metadata:
  version: "1.0.0"
---
# PRD

A PRD is the north star each story is checked against, with no acceptance criteria, design or costly decisions: those go to the `story`, `spec` and `adr` skills.

* **When:** only when more than one person must agree what the product is for, or it will run for weeks across many stories. Otherwise say so and use the `story` skill.
* **Size:** solo, the 4 lines of the form; a team, one page, 40 lines at most.
* **The file:** the path on the `PRD:` line in `AGENTS.md`, else `docs/prd.md`. Add the `PRD:` line when you create it. Each commit holds one change, with the reason in the message.

## Paths

* **Create:** fill in the form's headings and the repository's facts, each with its `file:line`, and nothing else. The person writes Problem, Goal and Not; ask why until the problem names no solution. Critique it against Failure modes, each finding with its source, until none remain. Commit it, then offer the `story` skill.
* **Review** a PRD against the form and Failure modes: report `<section>: <failure mode> — "<quoted text>" — <fix>`, then `Sound: <sections with no finding>`. Change nothing without its owner's yes.
* **Change** a section when its problem, users, goal or scope changes: the person writes the edit, you critique it, and list the open stories it now contradicts.
* **Check** a story, spike, chore or request against it: name the goal it serves, or the non-goal it breaks. One that serves none is a question for the user: drop it, or change the goal by the Change path. Never refuse silently.
* **No person in the session:** create or change nothing; report the question and what waits on it.

When the user asks you to write it, draft it with each line marked `(agent)`, and critique each line they keep like Create.

## The form

```text
# <Product>
Problem: <who has it, what it costs them today>
Goal: <outcome>, known by <metric, target, date>
Not: <each non-goal>
Appetite: <the time it is worth>
```

A team adds `Open:` lines, each with who answers it, and `Owner:`, who agrees a change. Use the terms in `docs/glossary.md`; no technology or code names.

## Failure modes

* **Solution first:** a problem or goal that names a feature.
* **A feeling:** a goal no finished product could fail, or a metric with no target or date.
* **Invented evidence:** a user, number or need no person gave or confirmed.
* **Requirements dump:** acceptance criteria, screens, architecture or a feature list. Move each to a story, a design doc or an ADR.
* **Stale:** a line that shipped stories or measured results contradict.
