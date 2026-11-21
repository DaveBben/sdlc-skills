---
name: prototyping
description: "Use first, before writing any code, when a question is to be answered by running throwaway code now: a spike to run, a prototype, a proof of concept, or a quick experiment to see whether something would work, how a library or API really behaves, or how hard a change would be, such as 'try the decimal module and see if it fixes the rounding', 'do a spike on async export', 'run the spike in docs/spikes/03.md', 'does the Gmail API return threads in date order? try it' or 'can pandas write this csv faster than the csv module, quick test'. Not for the real change, which is the building skill's, nor for writing a spike down for later. Writes disposable code that answers one question, with no tests, clean code or what-ifs beyond it, then reports the finding and deletes the code."
license: MIT
metadata:
  version: "8.1.0"
---
# Prototyping

A throwaway prototype is code written to answer one question, then deleted. Its only quality is that the answer is true. Tests, structure, error handling and the what-ifs are the real build's; leave them out here.

## Frame the question

* **Answer from a doc, the source or one command** when one settles it, and write no code.
* **Take a spike the person brings as the frame,** and fill only the lines it lacks.
* **State 4 lines, then start** without waiting for answers:
  1. **Decision:** the next step if it passes and if it fails. The same step both ways means no prototype.
  2. **Question:** a falsifiable outcome with its bar, on realistic data at a stated size, load and environment, such as "under 200 ms at 1,000 rows".
  3. **Finish line:** the signal that answers it, or the person's choice for a judgement only they can make.
  4. **Timebox:** a number of attempts. Narrow a question that will not fit it.

## Hack it

* **Work in a scratch directory outside the repository,** so nothing lands in the person's checkout or branches. When it needs the repository's code, clone the repository into it.
* **Write the least code that shows the signal:** hard-coded values, copy and paste, one script or a REPL, no error handling, logging or structure.
* **Cover only the cases the question names.**
* **Write no tests** except the one the question is observed through.
* **Run a negative control first:** the measurement on the baseline, or on an input past the bar, so a pass means something.
* **Compare approaches** through the same measurement, each at its smallest, in parallel.
* **Ask for a missing credential,** never fake one. Call a live system read-only, or with the person's yes for a write.

## Report

* **Stop at the finish line or when the timebox is spent.** A spent timebox is inconclusive: give your pick of extend by a stated amount, drop or defer.
* **Report the finding:** proven, disproven or inconclusive against the bar; what it ran on and how that differs from production; the quirks, dead ends and open questions the real build will meet. Claim only the question measured.
* **Record it** in the project's spike format where it has one, else in chat.
* **Delete the scratch directory** once the finding is recorded.
* **Leave the real change to the building skill,** started from the finding, never from the prototype's code. Code meant to be kept and grown (a tracer bullet) is building's walking skeleton, not a prototype.
