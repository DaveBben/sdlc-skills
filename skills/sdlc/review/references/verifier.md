# Verify

Each row of `findings.md` reads `<id>|<section>|<type>|<file>:<line>|<trigger>|<wrong>|<fix>|<support>`, without the reasoning behind it. Edit nothing in the tree and commit nothing; run a changed version in worktree `wt-verify` beside `findings.md`.

## Check every row

A row is false until the code shows it:

* **Keep** it on a run that fails for the stated reason or, where no run here can show it, lines traced from an entry point to the wrong result. A test gap: the tests pass the named wrong implementation. A `suggestion` needs only the lines that show it; a `question` only a person can answer, the lines that raise it.
* **Drop** it, naming the line that stops it: a guard, a type, a caller that never passes that input, or a misreading of `story.md`. An `issue` holding the code to a feature or format `story.md` never asks for, with no correctness, security or production fault at stake, is dropped or kept as a `question`.
* **No basis:** neither the code nor a run settles it. Drop it and say what would.
* **Unchecked:** a row you did not reach is listed as such, never dropped.

A kept row is **`blocking`** when a caller reaches it under production's configuration and a person or system sees the failure, `story.md` is not met, another system breaks, or a security fault has a path from outside. Otherwise it is **`non-blocking`**, as is every `suggestion` and `question`, and every fault the merge base already has that the diff does not newly reach, its proof starting `pre-existing:`. Then run the test command once: a failure is a kept blocking issue, its output the proof.

## Return

Rewrite `findings.md` with the kept rows only, blocking first, as `<id>|<blocking|non-blocking>|<section>|<type>|<file>:<line>|<trigger>|<wrong>|<fix>|<proof>`, then return:

```text
rows: <n>; kept: <n> (<n> blocking); dropped: <n>
<each kept row>
dropped: <id> <the stopping line, or "no basis: what would settle it">, one per line
unchecked: <ids>, or none
tests: <command> -> <pass | fail>
```
