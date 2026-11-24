---
name: design
description: "Use when the person is weighing technical design options or an architecture decision, or a design is to be written down, reviewed or filed for others to read later, not built now: 'help me decide between Leiden and HDBSCAN for grouping tickets', 'I'm thinking a static site or WordPress for the bakery, poke holes in it', 'write a design doc for the ticket-clustering pipeline', 'draft an ADR for moving to Postgres', 'review this RFC' or 'what is missing from this design doc'. Not for planning a change about to be built in this session, which the building skill plans, nor for business requirements, which are the discovery, prd and story skills'. A dialog where the person brings the options and decides, and the agent draws out each option, grounds it in the code and the data, and surfaces the unknowns; then the design doc and ADR templates and the checks a design is reviewed against."
license: MIT
metadata:
  version: "1.0.0"
---
# Design

The design is the person's: they bring the options and make the call. Your job is to help them weigh it: draw each option out, hold it against the code and the data, and find what they have not considered. A design doc puts the choice to reviewers before it is built; an ADR records one decision once it is made. A choice that is cheap to undo needs no design doc, at most an ADR.

## Start from the person's options

* **Read what it serves first:** the PRD, stories or request, and the code and ADRs it touches. A design that serves no stated requirement is a solution looking for a problem (XY problem): ask what it is for.
* **Ask for the options they are weighing,** which way they lean and why, in their words. When they have none, lay out the options the field uses as a menu, each with when it wins, and no pick.
* **Draw out each option by the seven questions,** from what they said, and mark each answer `theirs`, `checked` or `gap`:
  1. **Job:** what it solves, and what it optimizes or guarantees.
  2. **Assumptions:** what must be true of the input, the load and the team.
  3. **Settings:** each knob, and which way it pushes the result.
  4. **Failure modes:** how it fails, and what that looks like to a user or in the output.
  5. **Fit:** when they would pick it over the others.
  6. **Verification:** how they would show it works on real data or traffic, not only that it runs.
  7. **Cost:** to build, to run, to maintain, and to undo.
* **Ask only what only they know,** such as the decision the output feeds, the budget, the team's skills and who will run it. Look up or measure the rest yourself.

## Hold each option against reality

* **The code:** what the repository already solves this way or another, its conventions, layers and ADRs, and the callers a choice would break, each cited by `file:line`.
* **The data:** a real sample, measured, not described: shape, volume and growth, nulls, duplicates, languages and encodings, and the outliers.
* **The claims that decide the pick:** settle each `memory` answer with a doc, a command or a measurement, or a spike by the spike skill when it needs an experiment.
* **Report what contradicts their picture,** with the evidence, such as "you assumed English tickets; 18 in 100 in a sample of 500 are Spanish". Say what it changes for each option.

## Surface the unknowns

* **Known unknowns:** each open question that could flip the pick, with what would settle it and what it costs to find out.
* **Unknown unknowns:** up to 3 a round that they have not raised: a failure mode, a cost that arrives after launch, a one-way door, or an option they did not list, with the condition under which it would win.
* **Flag each one-way door** (data stored or sent, a contract others call, a dependency, auth, how it deploys, how the parts are split) as theirs to decide.

## Talk it through

* **Work in rounds:** what you found since the last round, what it changes for each option, then every question whose prerequisites are settled, numbered, with a question tool where there is one.
* **Hold your pick.** Recommend only when the person asks, after their own lean is on record, with the reason and what would change it.
* **Push back with evidence** when their lean contradicts the code, the data or a stated requirement. The call stays theirs; a choice they keep against the evidence is recorded as theirs, with its risk.
* **Stop when they decide,** or when they say the options are weighed enough to write up, each open question marked with who can answer it.

## Write for a reader who joined this week

Design docs fail by being unread: too long, or written in the team's shorthand.

* **Under 200 lines,** ADRs under 40. Cut what does not change the decision; link the rest.
* **The decision first:** the summary line states it and why, before any context.
* **Define each term, acronym and internal name** at first use, or link it. A ticket number is not an explanation.
* **One concrete case** for each abstract claim, such as "a ticket about a one-off outage lands in the billing cluster".
* **The outsider test:** before review, give the doc alone to a fresh subagent and have it state the problem, the decision, why, and the one-way doors. Each one it gets wrong or cannot state is a gap in the doc.

## Design doc

```markdown
# <the decision as a question, such as "How should support tickets be grouped into themes?">

Summary: <the decision and the reason that decided it, in 2 sentences>
Status: draft | in review | accepted | superseded by <link>
Author: <who> · Reviewers: <who must agree> · Date: <date>

## Context
<what exists today and the requirement this serves, with links; 3 to 5 sentences for a reader outside the team>

## Goals and non-goals
- Goal: <a measurable result, such as "monthly themes agree with 200 hand-grouped tickets at ARI ≥ 0.6">
- Non-goal: <what a reader would expect and this will not do>

## Options considered
| | <option A> | <option B> | <do nothing> |
|---|---|---|---|
| Job | | | |
| Assumptions | | | |
| Settings | | | |
| Failure modes | | | |
| Fit | | | |
| Verification | | | |
| Cost, and to undo | | | |

<each cell a phrase marked checked, with its evidence, or not checked; a sentence under the table only where a cell cannot carry it>

## Decision
Decided by <who>: <the option>, because <their reason>. <What would change it.>
<Each choice kept against the evidence, with its risk.>

## One-way doors
- <choice> — <why it is costly to undo> — <who decides>

## Risks and how we will know
- <risk> — <the signal in production that shows it> — <the response>

## Rollout and rollback
<the walking skeleton first; how it ships, behind what flag, and how it is undone>

## Open questions
- <question> — <who can answer it>
```

## ADR

One decision per file, `docs/adr/NNNN-<slug>.md`, numbered in order (Nygard's form):

```markdown
# NNNN. <the decision as a short phrase>

Status: proposed | accepted | deprecated | superseded by NNNN
Date: <date>

## Context
<the forces at play, and the options that lost>

## Decision
We will <...>.

## Consequences
<what gets easier, what gets harder, and what we must now do>
```

* **Supersede an accepted ADR, never edit it:** a change of mind is a new ADR that links the old one.

## Review one

Report `<doc>: <rule broken> — "<quoted text>" — <fix>`, then `Ready: yes | no`. Change nothing without its author's yes.

* **Over 200 lines,** or the decision not in the summary line.
* **Unreadable from outside the team:** an undefined term, acronym or internal name, or a claim the outsider test could not restate.
* **No requirement it serves,** or a goal nobody can measure.
* **One option,** or a straw man nobody would pick.
* **An option weighed without its failure modes or its cost to undo.**
* **A claim that decides the pick with no evidence,** about a library, a service, the data or the load, or an option never held against the code or a real sample of the data.
* **Options compared on different criteria.**
* **An unflagged one-way door.**
* **No signal in production** that shows it works, or no rollback.
* **Life after launch missing:** who runs it, who is paged, what it costs each month.
* **Implementation detail,** such as file layout or class names, before the choice is agreed.

## File one

* **File the design doc** as `docs/design/<NN>-<slug>.md`, or in the team's doc tool, and each ADR in `docs/adr/`.
* **Write the work it implies as stories** by the story skill, filed by the tracker skill.
