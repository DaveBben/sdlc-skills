---
name: prd
description: "Use at the start of a new product, and whenever a product requirements document (PRD) or the product's vision, problem, target users, goals, non-goals or success metrics are written, reviewed or changed, such as 'write a PRD', 'what are we building and why', 'review our PRD' or 'we're dropping a user group': agrees one short PRD with the person, item by item, as the north star each story is checked against. Not for a single feature, which is a story."
license: MIT
metadata:
  version: "1.0.0"
---
# PRD

A product requirements document (PRD) states why a product exists and what success means: the problem, who has it, the outcomes to reach and what the product will not do. It is the north star each story is checked against. It holds no acceptance criteria, design or decisions costly to reverse; those belong to the `story`, `spec` and `adr` skills. It stays under 100 lines; past that, move the detail to them. A product one story covers needs no PRD: say so and use the `story` skill.

## Where it lives

* **The file:** the path on the `PRD:` line in `AGENTS.md`, else `docs/prd.md` or `PRD.md`. Ask only when none exists.
* **Its terms:** in `docs/glossary.md` only, the one glossary every skill reads. The PRD uses the terms and defines none.
* **Commits:** on the default branch, create `prd/<product-slug>` first. Each commit holds one change to the PRD and its glossary entries, with the reason in the message; git history is the changelog. With no git, end the file with a `Changed: <date> <section>: <reason>` line per change.

## Paths

* **Create** one: by "Create" below.
* **Review** a PRD: check each section against "Write it" and "Failure modes", and report `<section>: <failure mode> — "<quoted text>" — <fix>`, then `Sound: <sections with no finding>`. Change nothing without the Owner's yes to that finding, else the user's.
* **Change** a section when a problem, user, goal, metric or scope changes: propose the edit like Create's step 3, with what made it change, and commit it on a yes. List the open stories it now contradicts.
* **Check** a story, spike, chore or request against it: name the goal question it helps answer, or the non-goal or constraint it breaks. One that helps answer none is a question for the user: drop it, or swap a goal by the Change path. Never add a fourth goal, and never refuse silently.
* **Resume:** read the PRD and continue Create at the first section of the form missing from it.
* **No person in the session:** create or change nothing; report the question and what waits on it.

## Create

1. **Ask where it lives** by "Questions": `docs/prd.md` or `PRD.md`, as equals. Write the file with its title, and add `PRD: <path>` to `AGENTS.md` where there is one.
2. **Find the problem first:** ask why until the problem names no solution: who has it, what they do today, what it costs them, and the evidence.
3. **Propose each item,** section by section in the order of the form, one at a time: the item, why it may be needed, and the source of that why: the user's words, a document, data with its source, or `(assumption)`. Ask it as Accept, Reject or Modify, and write each accepted item to the file at once.
4. **Agree the terms:** propose each domain noun and verb the users say, in their words, one term per concept, like step 3, and write it to `docs/glossary.md` as `<term>: <meaning>. Not: <a synonym to avoid or a concept it is confused with>`. A term already there with another meaning is its own question.
5. **Ask what was missed:** "Is there a user, goal, non-goal or term we have not considered?" Propose each one they name like step 3.
6. **Review it blind:** have a fresh subagent review it by the Review path, given only the PRD, each item's source from step 3, `docs/glossary.md` and this file's Review path, "Write it" and "Failure modes" without Stale; it changes nothing. Read each quote before keeping its finding, then propose each kept fix like step 3.
7. **Agree it:** show its `Decided:` lines, commit it, then offer the `story` skill to split the first release.

When the user says "just write it", draft every section with each item marked `(assumption)`, then propose only the required sections and the terms by step 3.

## Write it

```text
# <Product name>
Vision: For <target user> who <need>, <product> is a <category> that <key benefit>. Unlike <current alternative>, it <differentiator>.
Problem: <who has it, what they do today, what it costs them, the evidence and its source>
Users: <role: the context they use it in and the job it does for them>, primary first
Goals: 1 to 3, each a question the finished product must answer, naming no feature: <question> → <the decision or action its answer drives>; e.g. <one answer in real values>
Non-goals: <what it will not do>, because <reason>
Success metrics: <metric: where to read it, baseline or "none yet, first read <date>", target, date>, a leading and a lagging one per goal
Constraints: <appetite, deadline, budget, regulation or platform it must fit>, each with its source
First release: <capability>, in priority order, each one or more stories; the rest under Later
Assumptions: <what must be true>, its risk (value, usability, feasibility or viability) and how it gets tested, such as a spike or a metric
Open questions: <one per line, with who answers it>
Owner: <who agrees a change>
```

* **Product language:** the terms in `docs/glossary.md`, no technology or code names outside Constraints, and a number or an event, never fast, easy or scalable.
* **Required:** Problem, Goals, Non-goals and Success metrics. Leave out any other section with nothing in it.

## Failure modes

* **Solution first:** a problem or goal that names a feature, or a goal that restates the vision.
* **A feeling:** a goal no finished product could fail, such as "a personal Google Trends", or an answer that drives no decision. Ask what it must answer and what the user would do with the answer.
* **Unmeasurable:** a goal with no metric, or a metric with no target, date, or baseline or first-read date.
* **No boundary:** no non-goals, or one with no reason.
* **Invented evidence:** a user quote, number or need no person gave or confirmed, unmarked. Mark it `(assumption)` and list it under Assumptions.
* **Requirements dump:** acceptance criteria, screens, architecture, or capabilities planned past the first release. Move each to a story, a spec, an ADR or Later.
* **Ambiguous language:** one concept under 2 terms, one term for 2 concepts, or a domain term missing from `docs/glossary.md`.
* **Stale:** a section that shipped stories, measured results or another section contradict.

## Questions

* **A fact a tool can reach:** look it up.
* **Every section and term is the user's,** proposed by Create's step 3. Decide only the wording inside an accepted item, and list each such choice as `Decided: <choice>, because <reason>`.
* **How to ask:** one decision per question, through the multiple-choice tool where there is one (Claude Code's AskUserQuestion), naming the decision and what waits on it. Options are equals, none marked recommended, except a proposed item, which is Accept, Reject or Modify. "I need to research this" is always the last option, and its item goes under Open questions.
