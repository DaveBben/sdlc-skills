---
name: spike
description: "Use first, before answering or building, when the person asks whether something would work, how much work or how hard a change would be, whether it would break something, or what adopting a library or platform would do to the codebase, or wants a prototype, a quick test in a scratch directory, an experiment or a spike filed for later, such as 'do a spike on X', 'how hard would it be to make the export async', 'would Postgres full-text search be fast enough' or 'try the decimal module and see if it fixes the rounding'. Not for the real change: a request to build it is the building skill's. Frames a question that can fail and the decision it changes, runs throwaway code in a scratch directory inside a timebox, records the finding and deletes the code."
license: MIT
metadata:
  version: "5.0.0"
---
# Spike

A spike is the loop's Explore step run as a real experiment: throwaway code that answers one question whose answer could change the plan, the estimate or a build-or-buy choice. When a doc, the source or one command answers the question, answer it from there and stop.

## Frame it

State these 4 in one message and start.

1. **The decision:** the next step if it passes and if it fails. When both are the same step, there is no spike: say so.
2. **The question:** a falsifiable outcome with its bar and the data size, load and environment it is measured under, on realistic data, such as "under 200 ms at 1,000 rows on staging".
3. **The finish line:** the signal that answers it; for a judgement only the person can make, such as a layout, their choice.
4. **The timebox:** a number of attempts when you run it now. A question that will not fit is narrowed.

## Build it

* **Throwaway:** a scratch directory, or a worktree with no branch when it needs the repository's code. No tests except the one the question is observed through.
* **Negative control first:** run the measurement on the baseline or an input past the bar.
* **Several approaches:** each through one measurement at its smallest, in parallel subagents.
* **A missing credential:** never fake one or point the spike at a live system.
* **A working prototype** is evidence for the question measured and nothing else.
* **A new third-party API or platform:** follow [references/integration.md](references/integration.md).

## Record and finish

Write each finding as it surfaces, in `docs/spikes/<question-slug>.md`, or on the spike's ticket:

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

* **Timebox spent first:** mark it inconclusive and give your pick of extend by a stated amount, drop or defer. The person decides; never run on.
* **Delete the code** and its worktree, and commit the findings file alone. Keeping code is an exception the `Code:` line names, on a branch or in a scratch folder, never merged as it is.
* **To build:** the real change starts from the finding, in a fresh session, and goes through the loop like any new code, kept spike code included. `Quirks` and `Open questions` belong in its frame; `Follow-ups` become stories by the `story` skill.

## File one for later

On a team, a spike that waits its turn is a ticket labelled `spike` holding the 4 frame lines and the story or epic it unblocks.

* **Timebox in calendar time:** a day by default, 3 at most. It carries no story points: the timebox is its estimate.
* **Throwaway code** is outside the definition of done; the finding is the deliverable.
* **Schedule it** ahead of the story it feeds, in the same iteration. When the answer could kill the idea, the epic's stories are written after it.
