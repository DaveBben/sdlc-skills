---
name: spike
description: "Use first, before writing any code, when a question is to be answered by building something throwaway: a spike, a prototype, a proof of concept, a feasibility try, an ML or eval experiment, a test on a real board or phone, a benchmark or load test, a race or failure test, an exploit proof of concept, a cloud cost trial, a check of how a library or third-party API really behaves, or a clickable mock to react to, such as 'does fine-tuning beat prompting on our labelled tickets', 'will the sensor read reliably at 3.3 V', 'does background fetch still fire on iOS after the app is killed', 'does the Gmail API return threads in date order? try it' or 'write a spike for whether Postgres full-text search is fast enough'. Not for the real change, nor a benchmark or test suite to keep, which are the task or story skill's. Frames the question, runs it now or logs it, answers it with the least throwaway code outside the repository, and records the finding."
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
  Question: <a falsifiable outcome with its bar, under the conditions the answer depends on, such as data size, load, device, OS or browser version and environment: "under 200 ms at 1,000 rows on staging", "p99 frame time under 16.7 ms on the minimum-spec phone">
  Finish line: <the script that prints pass or fail against the bar, or the person's verdict where only they can judge>
  Timebox: <in the unit its kind uses: attempts at the approach, time, bench sessions, money, or the compute budget the person states>
  ```

* **Fix a frame that fails:** pass and fail lead to the same step; no bar, or one no result could miss; toy data, or none of the conditions the answer depends on; several questions, each its own spike; a question too big for its timebox; or something a user would notice once done, which is the real change, the task or story skill's.
* **Ask whether to run it now or log it in the person's tracker** when the request does not make it clear, as "write a spike for X" does not. A logged spike holds the 4 lines, is linked by the tracker's own blocking relation as blocking the story it unblocks where there is one, and nothing is built.

## Kinds

* **ML or eval experiment:** read [references/ml.md](references/ml.md) and follow it.
* **Hardware or a real device,** a board, a phone or a console: read [references/hardware.md](references/hardware.md) and follow it.
* **Performance or load:** read [references/performance.md](references/performance.md) and follow it.
* **A new third-party web API or SaaS integration:** read [references/integration.md](references/integration.md) and follow it.
* **Security, can this be exploited:** only against a local or staging copy the person owns, never production or a third party's system. The finish line is a proof of concept that shows the impact, such as reading one planted secret, with the patched or unaffected version as the negative control. Record it only where the person says is private, never in a public issue. Timebox in time.
* **Infrastructure or cost:** in a sandbox account, project or namespace with its own state, never the shared state file. Tag every resource with the spike, and tear it all down, showing the person it is gone, before the finding is recorded. Answer a cost question from a short real run's billing data beside the provider's price list. Timebox in money and time.
* **Feasibility of a change,** how hard it would be: make it in the scratch copy until the build and the existing tests pass or the timebox ends. The finding lists each breakage met, what is left, and an estimate. Timebox in time.
* **Concurrency or failure:** a race or a failure shows rarely, so one green run proves nothing. Run it under the language's race detector where one exists, such as `go test -race`, ThreadSanitizer or loom, and stress it with many runs, injected delays, killed processes or dropped connections, against a stated count of runs that must pass. A pass is evidence, not proof; the finding says so. Timebox in time.
* **UI or UX:** a throwaway clickable version put in front of the person, or of the users they name; the finish line is their verdict, the timebox attempts.
* **Library behaviour:** the smallest script that runs the behaviour on the pinned version; timebox in attempts.

## Hack it

* **Work in a scratch directory outside the repository,** where it survives the timebox, so nothing lands in the person's checkout or branches. When it needs the repository's code, clone the repository into it, and copy in what the clone lacks and the spike needs, asking before secrets or personal data. Where a clone is too heavy, such as a game-engine project, or the code is not in git, ask the person where to work.
* **Write the least code that shows the signal:** hard-coded values, copy and paste, one script or a REPL, no error handling or structure.
* **Cover only the cases the question names.**
* **Have a script decide the bar wherever one can,** printing pass or fail with the reading; it is the only test a spike writes. Run it first on the baseline, or on an input past the bar, so a pass means something.
* **Repeat any reading that varies and report the spread;** a difference inside the spread is no difference.
* **Compare approaches** through the same measurement, each at its smallest.
* **Ask for a missing credential or device;** never stub, mock or simulate the system the question is about, since that answers nothing. Call a live system read-only, or with the person's yes for a write.
* **Ask before copying production or personal data out of where it lives, or sending it to an outside service;** prefer a masked or synthetic copy at production size.
* **Undo every write** and remove every webhook, subscription, resource or test account the spike created before recording the finding.

## Check in

* **At the finish line, show the result** and let the person decide what is next: keep going, keep the code, or stop.
* **When the timebox is spent,** say what you learned and give your pick of extend by a stated amount, drop or defer.
* **Move it into a git repository of its own** when they want to keep hacking on it, still with no tests or structure.

## Record the finding

* **Ask where the finding goes:** a file such as `docs/spikes/<question-slug>.md`, or the spike's ticket.
* **Write it in this form,** claiming only the question measured:

  ```text
  ## <date> — spike: <the question> — timebox: <spent> — decides: pass → <step>; fail → <step>
  * **Outcome:** proven | disproven | inconclusive — <the reading> against <the bar>; measured on <data, load, device, environment>; differs from production in <what>
  * **Approach used:** <libraries, APIs and calls>
  * **Quirks and surprises:** <each, as the real work will meet it>
  * **Dead ends:** <approach> — <what it did instead>
  * **Decided without the person:** <choice> over <alternative> — <why>; cost to change later: <what>
  * **Open questions:** <what is still to settle>
  * **Follow-ups:** <what the finding suggests next; the person decides>
  * **Code:** deleted | kept at <path> because <reason>
  ```

* **A timebox spent before the finish line is `inconclusive`.**
* **Ask before deleting the scratch directory,** once the finding is recorded.
