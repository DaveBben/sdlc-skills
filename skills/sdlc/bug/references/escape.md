# Why a bug escaped

Escape analysis for a bug that reached users, as one question asked once the reproduction exists: which check should have caught this, and does adding it cost less than the bug did? Pick what the reproduction and the git history show:

* **No criterion:** no example in the story covered the input that failed. Name the kind of input.
* **No test:** a criterion covered it and no test did.
* **Weak oracle:** a test ran the faulty line and passed. The reproduction replaces it.
* **Review:** the faulty line was in the diff of the merge request that holds the `Entered:` commit. Name the merge request and the line.
* **A program could detect this kind:** name the lint rule, type or check.
* **Accepted escape:** a one-off, or the check costs more than the bug did. Add nothing.

Write the kind and what shows it on the report's `Escape:` line, with at most one proposal in one line, built as its own change and only when the person asks. Root-cause analysis on every bug grows checklists that slow the work.

For "why do we keep getting these": read each report's `Escape:`, `Entered:` and faulty file, group by kind and by file, and propose one change for the largest group. A file with a run of earlier fixes in `git log --oneline -- <file>` is a design finding: propose the refactor, as its own change.
