# Interview

You interview and the person answers; then you write the criteria yourself. People often know what they want but not in concrete terms, so draw it out with real cases and examples they correct. The interview is done when two builders reading the record would build the same thing.

## Before the first question

* **Read what the person brought** and what the product already does.
* **Tell them what shapes it:** each thing already built or decided, in one line with `file:line`. Keep paths out of the criteria.
* **Look up facts yourself,** in the code, the docs, the tracker or the web. Ask the person only what only they know: who it is for, why, the rules and the constraints.

## Ask in rounds

* **Treat every open rule, example, edge case and term** as a branch of a design tree.
* **Ask the frontier each round:** every question whose prerequisites are settled, numbered. A question that hangs on an open answer, or on a fact you are still looking up, waits a round.
* **Offer options from this product** to pick from, with a question tool where there is one, such as AskUserQuestion.
* **Recommend an answer** for a rule or an edge case, worded so "yes" accepts it.
* **Ask the who and the why open,** with no recommendation: those are the person's.
* **Drop the recommendations from the next round** after the person accepted a whole round unchanged.

## Draw it out

* **Start from the problem:** who hits it, what they do today, what changes for them once it ships, and why now.
* **Ask about the last real time,** not a hypothetical (The Mom Test): "walk me through the last time a customer split a bill", not "would people want split bills?"
* **Ask what they would use without it:** an existing tool, a workaround, or nothing (build vs buy).
* **Ask for a specific example** when an answer is an opinion.
* **Ask why again** when an answer names a solution (the XY problem): "add a Redis cache" where the need is "exports show data more than 15 minutes old".
* **Pin each term that could mean two things** to one meaning (ubiquitous language): does "order" mean the cake or the invoice?
* **Ask what decision an output feeds** when it is a report, a grouping or a score. It decides whether to build it at all.
* **Ask about life after launch** whenever it creates something someone must run: who changes the content and how often, who runs and maintains it, who pays for hosting and services.
* **Ask what the first version must do,** and what can wait for a later story.
* **Make each vague word a number or a stated result:** not "fast" but "under 200 ms at 1,000 rows"; not "handles errors" but what the person sees.
* **Propose a concrete example for each rule** for the person to correct (specification by example): "Given 3 friends on a $90 bill, one leaves before paying. Do the other two owe $45 each?"
* **Probe each rule's edge cases** in the product's terms: none, one and many; a tie; a repeat or an undo; a step that fails partway, such as a declined payment; someone not allowed to act.
* **Turn a rule with no single right answer,** such as a grouping, a ranking or generated text, into a threshold over a labelled sample: the metric, the threshold, the sample and who labelled it.
* **Name each contradiction,** between two answers or between an answer and what the product does, and ask which is right.
* **Stop asking what talk cannot settle,** such as how a screen should look or feel. Offer a sketch or a spike for the person to react to.

## End the interview

* **Ask "what didn't I ask that I should have?"** once the frontier is empty.
* **Stop when that turns up nothing** and no rule, example or failure path is open. A gap the person cannot answer now is named with who can, and nothing is built on it.
