# Run a spike

A spike is throwaway code that answers one question the plan hangs on. When a doc, the source or one command answers it, answer from there.

* **State 4 lines, then start** without waiting for answers:
  1. **Decision:** the next step if it passes and if it fails. The same step both ways means no spike.
  2. **Question:** a falsifiable outcome with its bar, on realistic data at a stated size, load and environment, such as "under 200 ms at 1,000 rows on staging".
  3. **Finish line:** the signal that answers it, or the person's choice for a judgement only they can make.
  4. **Timebox:** a number of attempts. Narrow a question that will not fit it.
* **Work in a scratch directory,** or a detached worktree when it needs the repository's code. Write no tests except the one the question is observed through.
* **Run a negative control first:** the measurement on the baseline or on an input past the bar.
* **Compare approaches** through the same measurement, each at its smallest, in parallel.
* **Never fake a missing credential** or point the spike at a live system.
* **Stop when the timebox is spent:** call it inconclusive and give your pick of extend by a stated amount, drop or defer.
* **Record the finding** in the project's spike format where it has one, else in chat: proven, disproven or inconclusive against the bar; what it was measured on and how that differs from production; quirks, dead ends and open questions as the real build will meet them. Claim only the question measured.
* **Delete the code** and its worktree, unless it is a tracer bullet: kept, and grown into the real build.
