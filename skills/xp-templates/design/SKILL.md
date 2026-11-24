---
name: design
description: "Use when a technical design or architecture decision is to be written down, reviewed or filed for others to read later, not built now: a design doc, an RFC, an ADR, a comparison of approaches for a team to review, or a critique of someone's design, such as 'write a design doc for the ticket-clustering pipeline', 'draft an ADR for moving to Postgres', 'compare a static site, WordPress and Squarespace for the bakery and write it up', 'review this RFC' or 'what is missing from this design doc'. Not for planning a change about to be built in this session, which the building skill plans, nor for business requirements, which are the prd and story skills'. Holds the design doc and ADR templates, the seven questions each option is weighed by, and the checks a design is reviewed against."
license: MIT
metadata:
  version: "1.0.0"
---
# Design

A design doc puts a choice to reviewers before it is built; an ADR records one decision once it is made. Both are read by people outside the conversation, later. A choice that is cheap to undo needs no design doc, at most an ADR.

## Write for a reader who joined this week

Design docs fail by being unread: too long, or written in the team's shorthand.

* **Under 200 lines,** ADRs under 40. Cut what does not change the pick; link the rest.
* **The pick first:** the summary line states the recommendation and why, before any context.
* **Define each term, acronym and internal name** at first use, or link it. A ticket number is not an explanation.
* **One concrete case** for each abstract claim, such as "a ticket about a one-off outage lands in the billing cluster".
* **The outsider test:** before review, give the doc alone to a fresh subagent and have it state the problem, the pick, why, and the one-way doors. Each one it gets wrong or cannot state is a gap in the doc.

## Before writing

* **Read what it serves:** the PRD, stories or request, and the code and ADRs it touches. A design that serves no stated requirement is a solution looking for a problem (XY problem): ask what it is for.
* **Ask the person only what only they know:** the decision the output feeds, and the constraints, such as budget, deadline, the team's skills and who will run it. Look up the rest yourself.

## Weigh each option

Weigh at least 2 real options, and doing nothing where that is viable. Answer the seven questions for each, marking each answer `doc` with its link, `seen` when you ran it, or `memory`:

1. **Job:** what it solves, and what it optimizes or guarantees.
2. **Assumptions:** what must be true of the input, the load and the team.
3. **Settings:** each knob, and which way it pushes the result.
4. **Failure modes:** how it fails, and what that looks like to a user or in the output.
5. **Fit:** when you would pick it over the others.
6. **Verification:** how you would show it works on real data or traffic, not only that it runs.
7. **Cost:** to build, to run, to maintain, and to undo.

* **Settle a `memory` answer that could flip the pick** with a spike, by the spike skill, before recommending.
* **Recommend one** with the reason that decided it, and keep the losing options in the doc: a reader's first question is "why not X?".
* **Flag each one-way door** (data stored or sent, a contract others call, a dependency, auth, how it deploys, how the parts are split), with who decides it.

## Design doc

```markdown
# <the decision as a question, such as "How should support tickets be grouped into themes?">

Summary: <the recommendation and the reason that decided it, in 2 sentences>
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

<each cell a phrase marked doc, seen or memory; a sentence under the table only where a cell cannot carry it>

## Recommendation
<the pick, the reason that decided it, and what would change it>

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

* **Over 200 lines,** or the pick not in the summary line.
* **Unreadable from outside the team:** an undefined term, acronym or internal name, or a claim the outsider test could not restate.
* **No requirement it serves,** or a goal nobody can measure.
* **One option,** or a straw man nobody would pick.
* **An option weighed without its failure modes or its cost to undo.**
* **A claim that decides the pick with no evidence,** about a library, a service, the data or the load.
* **Options compared on different criteria.**
* **An unflagged one-way door.**
* **No signal in production** that shows it works, or no rollback.
* **Life after launch missing:** who runs it, who is paged, what it costs each month.
* **Implementation detail,** such as file layout or class names, before the choice is agreed.

## File one

* **File the design doc** as `docs/design/<NN>-<slug>.md`, or in the team's doc tool, and each ADR in `docs/adr/`.
* **Write the work it implies as stories** by the story skill, filed by the tracker skill.
