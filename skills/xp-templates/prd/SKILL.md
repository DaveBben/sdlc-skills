---
name: prd
description: "Use when a product requirements document is to be written, reviewed or filed: interviewing the person to turn a product idea into a PRD, writing a PRD for a team or stakeholders, or critiquing a PRD someone handed over for what it leaves out, such as 'interview me for a PRD for the bakery website', 'write a PRD for the support-ticket themes report', 'what is missing from this PRD' or 'review the PRD in docs/prd.md before we plan'. Not for breaking a PRD into stories, which is the story skill's, nor for the technical design, which is the design skill's. Interviews at the product level (problem, users, goals and non-goals, success measures, constraints, life after launch) and holds the PRD template and the checks a PRD is reviewed against."
license: MIT
metadata:
  version: "1.0.0"
---
# PRD

A PRD says what problem a product solves, for whom, and how everyone will know it worked. It holds no design and no stories: the design skill weighs how to build it, and the story skill splits it into vertical slices.

## Write for a reader who joined this week

* **Under 200 lines.** Cut what does not change what gets built; link the rest.
* **The outcome first,** in the title line, before any background.
* **Define each term, acronym and internal name** at first use, or link it.
* **The outsider test:** before review, give the PRD alone to a fresh subagent and have it state the problem, who it is for, how success is measured and what is out of scope. Each one it gets wrong or cannot state is a gap.

## Create one

You interview and the person answers, then you write it.

* **Look up facts yourself,** in the code, the docs, the tracker or the web. Ask the person only what only they know: who it is for, why, the rules and the constraints.
* **Ask in rounds:** every question whose prerequisites are settled, numbered, with a question tool where there is one. Recommend an answer for a rule, worded so "yes" accepts it; ask the who and the why open.
* **Start from the problem and the last real time it happened** (The Mom Test), not a hypothetical. Ask why again when an answer names a solution.
* **Ask what decision an output feeds** when the product makes a report, a grouping or a score. It decides whether to build it at all: sorting items into categories the team already has is classification, not clustering.
* **Ask about life after launch,** which PRDs skip most: who changes the content and how often, who runs and maintains it, who pays for hosting and services, and what happens when the builder leaves.
* **Make each success measure a number** with a baseline, a target and a date, or a check a person runs.
* **Stop when "what didn't I ask that I should have?" turns up nothing,** each open gap marked `unknown` with who can answer it.
* **Play back** the problem, the goals and non-goals and each assumption, and write it once the person agrees:

```markdown
# <product or feature>: <the outcome in one line>

Owner: <who> · Status: draft | in review | approved · Date: <date>

## Problem
<who hits it, what they do today, what it costs them and why now, with the last real case>

## Users
- <role>: <their job to be done>

## Goals and non-goals
- Goal: <an outcome>
- Non-goal: <what a reader would expect and this will not do>

## Success measures
- <measure> — baseline <today> — target <value> by <date> — measured by <how>

## Requirements
1. <a business rule or capability, in the product's words, with an example in real values>

## Constraints
<budget, deadline, legal and regulatory rules, data that may not leave, platforms, and who it must work for, such as screen-reader users>

## Life after launch
<who updates the content and how often; who runs, monitors and maintains it; running costs and who pays; what is handed over>

## Risks and assumptions
- <assumption> — <how we will find out it is wrong>

## Open questions
- <question> — <who can answer it>
```

## Review one

Report `<prd>: <rule broken> — "<quoted text>" — <fix>`, then `Ready: yes | no`. Change nothing without its owner's yes; interview the owner on the gaps when they are here and want them closed.

* **Over 200 lines,** or unreadable from outside the team: an undefined term, acronym or internal name, or a point the outsider test could not restate.
* **A solution, not a problem,** or a problem with no real case behind it.
* **Users with no role** or job to be done.
* **A success measure with no number,** baseline or way to measure it.
* **Vague words,** such as fast, easy, intuitive or scalable, with no number.
* **No non-goals.**
* **Life after launch missing:** nobody named to run, maintain, update or pay for it.
* **A constraint the PRD never states** that the code, the data or the person reveals, such as data that may not leave or a fixed date.
* **Design in the PRD:** a framework, table or architecture chosen before the problem is agreed. Move it to a design doc.
* **Requirements that contradict** each other or what the product does today.
* **An unknown that could kill the product:** write it as a spike, by the spike skill, before any story.

## Next

* **File it** as `docs/prd/<slug>.md`, or in the team's doc tool.
* **Split an approved PRD into stories** by the story skill, and weigh each costly-to-undo choice of how by the design skill.
