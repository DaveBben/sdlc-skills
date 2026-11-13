---
name: spike
description: "Use first, before answering, when the person asks whether something would work, how hard or how much work it would be, or what adopting a library or platform would do to the codebase, or wants to try an approach and see if it works, a prototype or a quick experiment, such as 'do a spike on X', 'how hard would it be to make the export async', 'would Postgres full-text search be fast enough' or 'try the decimal module and see if it fixes the rounding': frames a question that can fail, builds throwaway code in a scratch directory, records what it found and deletes the code."
license: MIT
metadata:
  version: "3.1.0"
---
# Spike

When a doc, the source or one command answers the question, answer it from there and stop.

## Frame it

State these 4 in one message and start.

1. **The decision:** the next step if it passes and if it fails. When both are the same step, skip the spike and say so.
2. **The question:** a falsifiable outcome with its bar and the data size, load and environment it is measured under, such as "under 200 ms at 1,000 rows on staging".
3. **The finish line:** the signal that answers it; for a judgement only the person can make, such as a layout, their choice.
4. **The timebox:** a number of attempts.

## Build it

* **Throwaway:** a scratch directory, or a worktree with no branch when it needs the repository's code. No tests except the one the question is observed through.
* **Negative control first:** run the measurement on the baseline or an input past the bar, so you know it can fail.
* **Several approaches:** each through one measurement at its smallest, in parallel subagents.
* **A missing credential:** never fake one or point the spike at a live system.

## Record and finish

Write each finding as it surfaces, in `docs/spikes/<question-slug>.md`:

```text
## <date> — spike: <the question> — timebox: <attempts> — decides: pass → <step>; fail → <step>
* **Outcome:** proven | disproven | inconclusive — <the reading> against <the bar>; measured on <data, load, environment>; differs from production in <what>
* **Approach used:** <libraries, APIs and calls>
* **Quirks and surprises:** <each, as the real build will meet it>
* **Dead ends:** <approach> — <what it did instead>
* **Decided alone:** <choice> over <alternative> — <why>; cost to change later: <what>
* **Open questions:** <what the real build must settle>
```

When the timebox runs out first, mark it inconclusive with your pick of extend, drop or defer. State the verdict, the step it names and each `Decided alone` line, then delete the spike code and its worktree, and commit the findings file alone.
