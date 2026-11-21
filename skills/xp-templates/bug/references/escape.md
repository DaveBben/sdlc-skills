# Why a bug escaped

Find the escape point (8D): the first check after the fault entered that should have caught it, and whether closing it costs less than the bug did. Pick its kind from the reproduction and git history:

* **No criterion:** no example in the story covered the input that failed. Name the kind of input.
* **No test:** a criterion covered it and no test did.
* **Weak oracle:** a test ran the faulty line and passed. The reproduction replaces it.
* **Review:** the faulty line was in the diff of the `Entered:` commit's merge request. Name it and the line.
* **Detectable:** name the lint rule, type or check that would catch this kind.
* **Accepted escape:** a one-off, or the check costs more than the bug did. Add nothing.

Write the kind and its evidence on the report's `Escape:` line, with at most one proposal, built as its own change only when the person asks.

For "why do we keep getting these": group the reports' `Escape:`, `Entered:` and faulty files by kind and by file, and propose one change for the largest group. A file with a run of earlier fixes in `git log --oneline -- <file>` is a design finding: propose the refactor as its own change.
