---
name: spike
description: "Use first, before answering, whenever the person asks whether something would work or is feasible, how hard or how much work it would be, or what adopting a library or platform would look like or do to the codebase, or wants a prototype, demo, mock-up or quick experiment: agrees a question that can fail and a timebox, builds throwaway code and records what it found."
license: MIT
metadata:
  version: "1.0.0"
---
# Spike

When a doc, the source or one command answers the question, answer it from there and stop.

## Frame it

Agree three things with the user, one question each:

1. **The question:** a falsifiable outcome, with the data size, load and environment it is measured under, such as "streams partial results under 200 ms at 1,000 rows on staging". Refuse an unfalsifiable one.
2. **The finish line:** the signal that answers it. For a judgement only the user can make, such as a layout, it is their choice, and rejecting every option is its failure.
3. **The timebox:** a number of attempts, each one approach run to a result or an error.

Read a linked spike issue's three through the `tracker` skill and ask only for what is missing. A story that waits on the answer is blocked by the spike's issue.

## Build it

* **Where:** a scratch directory, or a worktree with no branch when it needs the repository's code.
* **Throwaway style:** hardcode and copy-paste; no tests except the one the question is observed through.
* **Negative control first:** run the measurement on the baseline or an input past the threshold.
* **Several approaches:** run each through one measurement at its smallest, in parallel subagents where possible, and compare their numbers, not their opinions.
* **A missing credential:** ask for it by name; never fake one or point the spike at a live system.
* **One question:** a failed attempt does not widen it, and a second unknown goes to open questions; stop and say so when the work outgrows it.

## Record as you go

Write each finding the moment it surfaces: on the linked issue; else in `docs/spikes/<question-slug>.md` on branch `spike-findings/<question-slug>`, in its own worktree; else in the scratch directory.

```text
## <date> — spike: <the question> — timebox: <limit>
* **Outcome:** proven | disproven | inconclusive — <the reading>, measured on <data, load, environment>; differs from production in <what>
* **Approach used:** <libraries, APIs and calls, in prose>
* **Quirks and surprises:** <each>
* **Dead ends:** <approach> — <what it did instead>
* **Open questions:** <what the real build must settle>
* **Decided alone:** <choice> over <alternative> — <why>; cost to change later: <what>
* **Changes to the plan:** <stories added, dropped or reordered>
```

## When it resolves

When the timebox runs out first, mark it inconclusive and ask, as equals, whether to extend, drop or defer.

1. **State** the verdict and the reading that settles it, with the `Decided alone` lines under it, and ask, as equals, whether to build with an approach, drop it or re-scope it; give your pick after the answer. Ask about a `Decided alone` line only when it is costly to change: record it by the `adr` skill, or move it to open questions.
2. **Update the plan:** mark the question answered on the spike's issue or story, link the findings, apply `Changes to the plan`, and close the issue once the user accepts.
3. **Delete the spike code** once the user accepts; commit the findings file alone and offer a pull request of it. The real build starts fresh.
