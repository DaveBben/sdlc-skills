---
name: spike
description: "Use first, before writing any code, when a question is to be answered by building something throwaway: a spike, a prototype, a proof of concept, an ML or eval experiment, a hardware test on a real board, a benchmark or load test, a stress test for a race, a quick test of how a library or third-party API really behaves, or a clickable mock to react to, such as 'try the decimal module and see if it fixes the rounding', 'can pandas write this csv faster than the csv module', 'does fine-tuning beat prompting on our labelled tickets', 'will the sensor read reliably at 3.3 V', 'does the Gmail API return threads in date order? try it' or 'write a spike for whether Postgres full-text search is fast enough'. Not for the real change, which is the task or story skill's. Frames the question in 4 lines, asks whether to run it now or log it in the tracker, builds the least throwaway code that answers it in a scratch directory, decides the bar with a script where one can, records the finding, and leaves what comes next to the person."
license: MIT
metadata:
  version: "10.0.0"
---
# Spike

A spike is a timeboxed question whose answer changes a decision, answered with throwaway code. Its only quality is that the answer is true; what survives is the finding, not the code. Tests, structure, error handling and the what-ifs are the real build's. Code meant to grow into the product is a story's walking skeleton, not a spike.

## Frame

* **Answer from a doc, the source or one command** when one settles it, and write no code.
* **Take a spike the person brings as the frame,** and fill only the lines it lacks.
* **State 4 lines:**

  ```text
  Decision: pass → <next step>; fail → <next step>
  Question: <a falsifiable outcome with its bar, on realistic data at a stated size, load and environment, such as "under 200 ms at 1,000 rows on staging">
  Finish line: <the script that prints pass or fail against the bar, or the person's verdict where only they can judge>
  Timebox: <in the unit its kind uses: attempts, time, bench sessions, or the compute budget the person states>
  ```

* **Fix a frame that fails:** pass and fail lead to the same step; no bar, or one no result could miss; toy data, or no stated size, load or environment; several questions, each its own spike; a question too big for its timebox; or something a user would notice once done, which is a story.
* **Ask whether to run it now or log it in the person's tracker** when they did not say. A logged spike holds the 4 lines, is linked by the tracker's own blocking relation as blocking the story it unblocks, and nothing is built.

## Kinds

* **ML or eval experiment:** by [references/ml.md](references/ml.md).
* **Hardware:** by [references/hardware.md](references/hardware.md).
* **Performance or load:** by [references/performance.md](references/performance.md).
* **A new third-party API or platform:** by [references/integration.md](references/integration.md).
* **Concurrency:** a race shows rarely, so one green run proves nothing. Stress it with many runs and injected delays, against a stated count of runs that must pass; timebox in time.
* **UI or UX:** a throwaway clickable version put in front of the person; the finish line is their verdict, the timebox attempts.
* **Library behaviour:** the smallest script that runs the behaviour on the pinned version; timebox in attempts.

## Hack it

* **Work in a scratch directory outside the repository,** so nothing lands in the person's checkout or branches. When it needs the repository's code, clone the repository into it.
* **Write the least code that shows the signal:** hard-coded values, copy and paste, one script or a REPL, no error handling, logging or structure.
* **Cover only the cases the question names.**
* **Have a script decide the bar wherever one can,** printing pass or fail with the reading; it is the only test a spike writes.
* **Run a negative control first:** the measurement on the baseline, or on an input past the bar, so a pass means something.
* **Compare approaches** through the same measurement, each at its smallest.
* **Ask for a missing credential,** never fake one. Call a live system read-only, or with the person's yes for a write.

## Check in

* **At the finish line, show the result** and let the person decide what is next: keep going, keep the code, or stop.
* **When the timebox is spent,** say what you learned and give your pick of extend by a stated amount, drop or defer.
* **Move it into the person's project under git** when they want to keep hacking on it, still with no tests or structure.

## Record the finding

* **Ask where the finding goes:** a file such as `docs/spikes/<question-slug>.md`, or the spike's ticket.
* **Write it in this form,** claiming only the question measured:

  ```text
  ## <date> — spike: <the question> — timebox: <spent> — decides: pass → <step>; fail → <step>
  * **Outcome:** proven | disproven | inconclusive — <the reading> against <the bar>; measured on <data, load, environment>; differs from production in <what>
  * **Approach used:** <libraries, APIs and calls>
  * **Quirks and surprises:** <each, as the real work will meet it>
  * **Dead ends:** <approach> — <what it did instead>
  * **Decided alone:** <choice> over <alternative> — <why>; cost to change later: <what>
  * **Open questions:** <what is still to settle>
  * **Follow-ups:** <what the finding suggests next; the person decides>
  * **Code:** deleted | kept at <path> because <reason>
  ```

* **Mark a spent timebox `inconclusive`.**
* **Ask before deleting the scratch directory,** once the finding is recorded.
