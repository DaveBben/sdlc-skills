# Create a story

You interview and the person answers. They often know what they want but not in concrete terms, so draw it out with real cases and examples they correct, then write the story yourself.

## Before the first question

* **Read what the person brought** and what the product already does.
* **Tell them what shapes the story:** each thing already built or decided, in one line with `file:line`. Keep paths out of the story.
* **Split it first when it is too big,** by [split.md](split.md), and interview the first slice.
* **Look up facts yourself,** in the code, the docs, the tracker or the web. Ask the person only what only they know: who it is for, why, and the rules.

## Ask in rounds

* **Treat every open item** of SKILL.md's acceptance criteria rules and "How a story fails" as a branch of a design tree.
* **Ask the frontier each round:** every question whose prerequisites are settled, numbered. A question that hangs on an open answer, or on a fact you are still looking up, waits a round.
* **Offer options from this product** to pick from, with a question tool where there is one, such as AskUserQuestion.
* **Recommend an answer** for a rule or an edge case, worded so "yes" accepts it.
* **Ask the who and the why open,** with no recommendation: those are the person's.
* **Drop the recommendations from the next round** after the person accepted a whole round unchanged.

## Draw it out

* **Start from the problem:** who hits it, what they do today, what changes for them once it ships, and why now.
* **Ask about the last real time,** not a hypothetical (The Mom Test): "walk me through the last time a customer split a bill", not "would people want split bills?"
* **Ask for a specific example** when an answer is an opinion.
* **Ask why again** when an answer names a solution.
* **Propose a concrete example for each rule** for the person to correct (specification by example): "Given 3 friends on a $90 bill, one leaves before paying. Do the other two owe $45 each?"
* **Probe each rule's edge cases** in the product's terms: none, one and many; a tie; a repeat or an undo; someone not allowed to act.
* **Name each contradiction,** between two answers or between an answer and what the product does, and ask which is right.
* **Stop asking what talk cannot settle,** such as how a screen should look or feel. Offer a sketch or a spike for the person to react to.

## End the interview

* **Offer a questionnaire** for whoever can answer an `unknown`: the decision it feeds, one idea per question, most important first, and room to answer "I don't know".
* **Ask "what didn't I ask that I should have?"** once the frontier is empty.
* **Stop when that turns up nothing,** or when the person says to write it now, each open gap marked `unknown`.

## Write it

* **Play back** the goal, each rule with its example, each assumption and what the story will not do.
* **Write the story** once the person agrees, in this template:

```markdown
# <what a person can do once this merges: an outcome, not a task>

Why: <who hits this, what they do today, what changes once it ships, and why now; 1 or 2 sentences>

## Context

<2 or 3 sentences for a reader outside the team: this part of the product today, and related work or decisions>

## Acceptance criteria

1. <one business rule>
   Given a key that made 99 requests in the last minute, through the public API
   When it makes one more
   Then the request succeeds and the response says 0 remain
   Check: <the command or test that will show it, or `by eye: <what to look at>`>

## UAT
<how the person sees the story work on the live system: the credentials, services and data it uses, and read-only, dry run or a write they approve>

## Out of scope

- <what a reader would expect here and this story will not do>

## Dependencies

- <who must review, sign off or supply data, and the wait; the story this waits on; or a spike that blocks it>

## Open questions

- <one per line, with who can answer it>

Reach: <the page, route or command where a person or test meets the new behaviour>
Hint: <files or APIs to start from; optional, never a design>
```

* **Name in one line what you left out on purpose,** so the person can ask for it.
