# A bug

* **Criteria:** the ticket's `Reproduction:` and `Same fault:` lines. With no confirmed reproduction, get one by the `bug` skill first.
* **Scientific debugging:** mark the ticket's `Guess:` line held or wrong, and tell the reporter which, with the cause's `file:line`.
* **Fix the root cause,** not the caller that reported it, unless the person names a fix at a caller: build theirs and note the root cause's `file:line` in one line as a symptom fix.
* **No interface step.** The review's design is the confirmed cause.
