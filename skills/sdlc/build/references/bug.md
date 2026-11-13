# A bug

* **Reproduce first,** at the lowest level that shows it, with the exact output; that reproduction is the first red test, and its criteria are what should happen instead. Cannot reproduce: never fix blind; ask for the missing fact by name and stop.
* **Same fault elsewhere:** search the other callers and copies; a hit under the same rule is fixed by the same change.
* **Fix the root cause,** not the caller that reported it, unless the person names a fix at a caller: build theirs and note the root cause's `file:line` in one line as a symptom fix.
* **No interface or design step.** The review's design is the confirmed cause.
* **Why it escaped:** in the retro, name the check that would have caught it, and propose adding it.
