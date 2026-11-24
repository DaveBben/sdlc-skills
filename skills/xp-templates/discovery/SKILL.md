---
name: discovery
description: "Use when the person wants an idea, problem or request turned into written requirements for later or for someone else, by being interviewed, not built now: 'interview me for a story about X', 'write a story for X', 'help me write a PRD for the bakery website', 'turn this idea into requirements', 'I have a rough idea for a feature, help me pin it down' or 'write a ticket for X for the team'. Not for reviewing, splitting, forecasting or filing a story or PRD that already exists, which are the story and prd skills', nor for building one. Interviews at the business level, sizes what it finds, and writes one story for a single vertical slice, or a PRD and its story map for several features or a product."
license: MIT
metadata:
  version: "1.0.0"
---
# Discovery

You interview and the person answers, then you write the result yourself. People often know what they want but not in concrete terms, so draw it out with real cases and examples they correct.

## Before the first question

* **Read what the person brought** and what the product already does.
* **Tell them what shapes it:** each thing already built or decided, in one line with `file:line`. Keep paths out of what you write.
* **Look up facts yourself,** in the code, the docs, the tracker or the web. Ask the person only what only they know: who it is for, why, the rules and the constraints.

## Size it

Size it from the first answers, again whenever an answer changes it, and say so when it does.

* **A story:** one vertical slice that fits one merge request, under about 400 changed lines and 5 criteria. Its template, criteria rules and failure modes are the story skill's.
* **A PRD:** several features, or a product or area that does not exist yet. Its template and review checks are the prd skill's. Once the person approves it, lay out the story map by the story skill's split, then interview the first story.
* **Neither:** a change no user would notice, such as a refactor, rename, dependency bump or CI, needs one `Done when:` line, not an interview.
* **An unknown that could change it fundamentally:** name up to 3, each written as a spike by the spike skill, blocking it.

## Ask in rounds

* **Treat every open item** of the target's template and failure modes as a branch of a design tree.
* **Ask the frontier each round:** every question whose prerequisites are settled, numbered. A question that hangs on an open answer, or on a fact you are still looking up, waits a round.
* **Offer options from this product** to pick from, with a question tool where there is one, such as AskUserQuestion.
* **Recommend an answer** for a rule or an edge case, worded so "yes" accepts it.
* **Ask the who and the why open,** with no recommendation: those are the person's.
* **Drop the recommendations from the next round** after the person accepted a whole round unchanged.

## Draw it out

* **Start from the problem:** who hits it, what they do today, what changes for them once it ships, and why now.
* **Ask about the last real time,** not a hypothetical (The Mom Test): "walk me through the last time a customer split a bill", not "would people want split bills?"
* **Ask for a specific example** when an answer is an opinion, and why again when an answer names a solution.
* **Ask what decision an output feeds** when it is a report, a grouping or a score. It decides whether to build it at all: sorting items into categories the team already has is classification, not clustering.
* **Ask about life after launch** whenever it creates something someone must run: who changes the content and how often, who runs and maintains it, who pays for hosting and services, and what happens when the builder leaves.
* **Make each success measure a number** with a baseline, a target and a date, or a check a person runs.
* **Propose a concrete example for each rule** for the person to correct (specification by example): "Given 3 friends on a $90 bill, one leaves before paying. Do the other two owe $45 each?"
* **Probe each rule's edge cases** in the product's terms: none, one and many; a tie; a repeat or an undo; someone not allowed to act.
* **Name each contradiction,** between two answers or between an answer and what the product does, and ask which is right.
* **Stop asking what talk cannot settle,** such as how a screen should look or feel. Offer a sketch or a spike for the person to react to.

## End the interview

* **Offer a questionnaire** for whoever can answer an `unknown`: the decision it feeds, one idea per question, most important first, and room to answer "I don't know".
* **Ask "what didn't I ask that I should have?"** once the frontier is empty.
* **Stop when that turns up nothing,** or when the person says to write it now, each open gap marked `unknown` with who can answer it.

## Write it

* **Play back** the goal, each rule with its example, each assumption and what it will not do.
* **Write it** in the story or prd skill's template once the person agrees, and check it against that skill's failure modes or review checks before you show it.
* **Name in one line what you left out on purpose,** so the person can ask for it.
* **File only what the person approved,** by the story or prd skill's filing rule.
