---
name: spike
description: "Use when a spike is to be written, reviewed, recorded or filed: framing an open question as a spike for later or for someone else, critiquing a spike someone wrote, writing up what an experiment found, or listing what to find out about a new third-party API or platform, such as 'write a spike for whether Postgres full-text search is fast enough', 'create a spike ticket that blocks the export story', 'is this spike well framed', 'write up what the Polars experiment found' or 'what do we need to learn about the Stripe API before we commit'. Not for running the experiment or building the real change. Holds the spike's 4 frame lines (decision, falsifiable question, finish line, timebox), the checks a spike is reviewed against, and the finding record."
license: MIT
metadata:
  version: "1.0.0"
---
# Spike

A spike is a timeboxed question whose answer changes a decision. When a doc, the source or one command answers the question, there is no spike: say so.

## Write one

```text
Decision: pass → <next step>; fail → <next step>
Question: <a falsifiable outcome with its bar, on realistic data at a stated size, load and environment, such as "under 200 ms at 1,000 rows on staging">
Finish line: <the signal that answers it, or the person's choice for a judgement only they can make>
Timebox: <a day by default, 3 at most; no story points>
```

* **A new third-party API or platform:** take its questions from [references/integration.md](references/integration.md).

## Review one

Report `<spike>: <rule broken> — "<quoted text>" — <fix>` per finding. Change nothing without its owner's yes.

* **No decision:** pass and fail lead to the same step.
* **Not falsifiable:** no bar, or a bar no result could miss.
* **Unrealistic:** toy data, or no stated size, load or environment.
* **Several questions:** each is its own spike.
* **No timebox,** or a question that will not fit it: narrow the question.
* **A story in disguise:** it delivers something a user would notice. Write it as a story.

## Record the finding

Write each finding as it surfaces, in `docs/spikes/<question-slug>.md` or on the spike's ticket:

```text
## <date> — spike: <the question> — timebox: <spent> — decides: pass → <step>; fail → <step>
* **Outcome:** proven | disproven | inconclusive — <the reading> against <the bar>; measured on <data, load, environment>; differs from production in <what>
* **Approach used:** <libraries, APIs and calls>
* **Quirks and surprises:** <each, as the real work will meet it>
* **Dead ends:** <approach> — <what it did instead>
* **Decided alone:** <choice> over <alternative> — <why>; cost to change later: <what>
* **Open questions:** <what is still to settle>
* **Follow-ups:** <new stories, or the parent story's revised size>
* **Code:** deleted | kept at <path> because <reason>
```

* **Claim only the question measured.**
* **Mark a spent timebox `inconclusive`,** with your pick of extend by a stated amount, drop or defer.
* **Write `Follow-ups` as stories** by the story skill.

## File one

* **File it** as a ticket labelled `spike`, by the tracker skill, blocking the story or epic it unblocks, holding the 4 frame lines.
* **Schedule it** ahead of the story it feeds, in the same iteration. When the answer could kill the idea, write the epic's stories after it.
