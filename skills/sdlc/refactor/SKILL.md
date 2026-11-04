---
name: refactor
description: "Use first, before answering or editing, for any change to code's structure that keeps its behaviour, even a one-line clean-up, such as renaming, extracting or inlining, moving code, breaking up a long function, simplifying, deduplicating, or removing dead code or magic numbers, and for judging readability, smells or tech debt: refactors in small steps with the tests green."
license: MIT
metadata:
  version: "1.0.0"
---
# Refactoring

Refactor code you are about to change, code you struggled to understand, and hotspots. Leave the rest alone.

## Where to look

When the user asks where to clean up, rank hotspots (Tornhill): change count and churn per line over the last year, code files only, then each top file's change coupling. Coupled files with no import or call between them share a hidden concept: give it one owner. Read for smells only inside the top files, judged by whether a reader can predict what the code does, never by a single score.

Leave code alone when no change touches it, it is due for deletion, its duplication is coincidental, or length is the only complaint.

## Refactor safely

* **Green first:** run the tests. Code with no test gets characterization tests first, committed alone; kill one hand-made mutant to prove each can fail.
* **One named refactoring per step,** by TCR. After each step, re-read for the smell it targeted; still there means the wrong refactoring: revert it.
* **Two hats:** a bug found mid-refactoring is reported by the `bug` skill, not fixed in it.
* **Keep** public names and signatures (migrate them by parallel change), error handling, assertions, logging and comments that explain why. Read each commit's diff for deleted lines.
* **Commits:** each refactoring alone, `refactor: <refactoring> (<smell>)`.
* **Large:** a change that cannot be one pull request: [references/large.md](references/large.md).
* **On its own:** build it by the `build` skill as a refactoring.

## Report

```text
Hotspots: <path — commits — churn per line — coupled files>, when files were ranked
Keep: <what is good and stays, and why>
Smells: <file:line — smell — the lines that show it — refactoring — when: now | when <named change> | never>
Done: <each refactoring commit>; tests: <green before and after>
Not done: <what was left, and why>
```
