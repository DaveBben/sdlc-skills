---
name: spike
description: "Use first, before answering, whenever the person asks whether something would work or is feasible, how hard or how much work it would be, or what adopting a library or platform would look like or do to the codebase, or wants a prototype, demo, mock-up or quick experiment, or is still finding out what to build: frames a question that can fail and a timebox, builds throwaway code and records what it found."
license: MIT
metadata:
  version: "1.0.0"
---
# Spike

When a doc, the source or one command answers the question, answer it from there and stop.

## Frame it

Draft these four from the request and what you read, state them in one message, and start. A question the person hands to the spike is the spike's to answer; ask only what their words leave open that you cannot pick, once, in that message, with your pick.

1. **The decision:** the next step if it passes and the next step if it fails, each a story, an approach or a drop. When both are the same step, skip the spike and say so.
2. **The question:** a falsifiable outcome, with the data size, load and environment it is measured under, and what crossing its bar means for the product, such as "under 200 ms at 1,000 rows on staging, or search reads as stalled". With no consequence, say so in one line with the consequence you will measure against, and go on.
3. **The finish line:** the signal that answers it; for a judgement only the user can make, such as a layout, their choice, and rejecting every option is its failure.
4. **The timebox:** a number of attempts, each one approach run to a result or an error.

Read a linked spike issue's four by the `tracker` skill and draft only what is missing. A story that waits on the answer is blocked by the spike's issue.

## Build it

* **Where:** a scratch directory, or a worktree with no branch when it needs the repository's code.
* **Throwaway style:** no tests except the one the question is observed through.
* **Negative control first:** run the measurement on the baseline or an input past the threshold.
* **Several approaches:** each through one measurement at its smallest, in parallel subagents.
* **A missing credential:** ask for it by name; never fake one or point the spike at a live system.
* **One question:** a failed attempt does not widen it; a second unknown goes to open questions; a finding that the question has two readings goes in the verdict with your pick, never a new round; stop and say so when the work outgrows it.

## Explore what to build

When the person is still finding out what to build, the question is whether a design gets a known success right, a real case the product must handle; the finish line is that case passing; where only the person can judge it, their choice, as in Frame it.

* **Small direct changes,** each run against the known success at once, with no story, criteria, challenge or review.
* **Revert** an attempt that misses rather than patch around it, and record it under Dead ends.
* **Held still:** once recent attempts pass without changing a data shape, screen or rule, cite them and propose stories from the findings by the `story` skill. The person decides when; the spike code still goes.

## Record as you go

Write each finding the moment it surfaces: on the linked issue; else in `docs/spikes/<question-slug>.md` on branch `spike-findings/<question-slug>`, in its own worktree; else in the scratch directory.

```text
## <date> — spike: <the question> — timebox: <limit> — decides: pass → <step>; fail → <step>
* **Outcome:** proven | disproven | inconclusive — <the reading> against the bar <the agreed bar>, and what that means for the decision; measured on <data, load, environment>; differs from production in <what>
* **Approach used:** <libraries, APIs and calls, in prose>
* **Quirks and surprises:** <each>
* **Dead ends:** <approach> — <what it did instead>
* **Open questions:** <what the real build must settle>
* **Decided alone:** <choice> over <alternative> — <why>; cost to change later: <what>
* **Changes to the plan:** <stories added, dropped or reordered>
```

## When it resolves

When the timebox runs out first, mark it inconclusive and state your pick of extend, drop or defer with the evidence for it, as a `Decided alone` line.

1. **State** the verdict, its reading and the step the decision named, with the `Decided alone` lines. When that step is easy to reverse, such as a view's rule, take it and say so; only for a one-way door, ask, as equals, whether to build, drop or re-scope, your pick after the answer. A `Decided alone` line costly to change is recorded by the `adr` skill or moved to open questions.
2. **Update the plan:** mark the question answered on the spike's issue or story, link the findings, apply `Changes to the plan`, and close the issue.
3. **Delete the spike code** and its worktree once the verdict is stated, and say so; commit the findings file alone and offer a pull request of it.
