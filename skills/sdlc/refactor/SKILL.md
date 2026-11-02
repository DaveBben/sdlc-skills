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

When the user asks where to clean up, find the hotspots:

1. **Changes and churn** over the last year, code files only. Take files high on both change count and churn per line first.

   ```bash
   git log --since=1.year --numstat --format= | awk -F'\t' 'NF==3 {n[$3]++; c[$3]+=$1+$2} END {for (f in n) print n[f], c[f], f}' | sort -rn
   ```

2. **Change coupling:** for each top file, the files that change in the same commits. One with no import or call between them shares a hidden concept: give it one owner.

   ```bash
   git log --since=1.year --format=%H -- <file> | while read -r c; do git show --name-only --format= "$c"; done | sort | uniq -c | sort -rn
   ```

3. **Read for smells** only inside the top files. Judge code by whether a reader can predict what it does, never by a single score.

Leave code alone when no change touches it, it is due for deletion, its duplication is coincidental, or length is the only complaint. A speed, memory or security change is not a refactoring.

## Refactor safely

* **Green first:** run the tests. Code with no test gets characterization tests first, committed alone; kill one hand-made mutant to prove each can fail.
* **One named refactoring per step,** by TCR, using the editor's or language server's rename, extract and move where they exist. After each step, re-read for the smell it targeted; still there means the wrong refactoring: revert it.
* **Two hats:** never change behaviour in a step. A bug found mid-refactoring is finished or reverted, then reported, by the `bug` skill.
* **Keep** public names and signatures (migrate them by parallel change), error handling, assertions, logging and comments that explain why. Read each commit's diff for deleted lines.
* **Commits:** each refactoring alone, `refactor: <refactoring> (<smell>)`, such as `refactor: inline _classify (Middle Man)`, never mixed with a behaviour change.
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
