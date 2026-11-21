---
name: spike
description: "Use first, before answering or building, when the person asks whether something would work, how much work or how hard a change would be, whether it would break something, or what adopting a library or platform would do to the codebase, or wants a prototype, a quick test in a scratch directory, an experiment or a spike filed for later, such as 'do a spike on X', 'how hard would it be to make the export async', 'would Postgres full-text search be fast enough' or 'try the decimal module and see if it fixes the rounding'. Not for the real change: a request to build it is the building skill's. Frames a question that can fail and the decision it changes, runs throwaway code in a scratch directory inside a timebox, records the finding and deletes the code."
license: MIT
metadata:
  version: "7.0.0"
---
# Spike

When a doc, the source or one command answers the question, answer from there and stop.

## Frame it

State these 4 in one message, then start without waiting for answers.

1. **The decision:** the next step if it passes and if it fails. When both are the same step, there is no spike: say so.
2. **The question:** a falsifiable outcome with its bar, on realistic data at a stated size, load and environment, such as "under 200 ms at 1,000 rows on staging".
3. **The finish line:** the signal that answers it, or the person's choice for a judgement only they can make, such as which of two designs reads better.
4. **The timebox:** a number of attempts. Narrow a question that will not fit it.

## Build it

* **Work in a scratch directory,** or in a detached worktree when it needs the repository's code. Write no tests except the one the question is observed through.
* **Run a negative control first:** the measurement on the baseline or on an input past the bar.
* **Compare approaches** through the same measurement, each at its smallest, in parallel, such as in subagents.
* **Never fake a missing credential** or point the spike at a live system.
* **Claim only the question measured.**
* **A new third-party API or platform:** follow [references/integration.md](references/integration.md).

## Record and finish

Write each finding as it surfaces, in `docs/spikes/<question-slug>.md` or on the spike's ticket:

```text
## <date> — spike: <the question> — timebox: <attempts> — decides: pass → <step>; fail → <step>
* **Outcome:** proven | disproven | inconclusive — <the reading> against <the bar>; measured on <data, load, environment>; differs from production in <what>
* **Approach used:** <libraries, APIs and calls>
* **Quirks and surprises:** <each, as the real build will meet it>
* **Dead ends:** <approach> — <what it did instead>
* **Decided alone:** <choice> over <alternative> — <why>; cost to change later: <what>
* **Open questions:** <what the real build must settle>
* **Follow-ups:** <new stories, or the parent story's revised size>
* **Code:** deleted | kept at <path> because <reason>
```

* **Stop when the timebox is spent:** mark it inconclusive and give your pick of extend by a stated amount, drop or defer.
* **Delete the code** and its worktree, and commit the findings file alone, unless it is a tracer bullet: kept at the path the `Code:` line names and grown into the real build through the story and building skills.
* **To build:** the real change starts from the finding in a fresh session, at the story skill. `Quirks` and `Open questions` go into its frame; `Follow-ups` become stories by the `story` skill.

## File one for later

A spike that waits its turn is a ticket labelled `spike`, filed by the tracker skill as blocking the story or epic it unblocks, holding the 4 frame lines.

* **Timebox it in calendar time:** a day by default, 3 at most, and no story points.
* **Schedule it** ahead of the story it feeds, in the same iteration. When the answer could kill the idea, write the epic's stories after it.
