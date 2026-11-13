---
name: bug
description: "Use first, before debugging or answering, when existing code misbehaves or gives a surprising result, such as an error, crash, hang, wrong or odd output, a regression or a rule the code fails to enforce, like 'the export times out past 10k orders', 'why does total return 9.999 instead of 10' or 'file a bug for X': reproduces it before any fix, writes the reproduction as Given/When/Then, finds why it escaped and which check would have caught it, and decides fix now, story or won't fix."
license: MIT
metadata:
  version: "3.1.0"
---
# Bug

Behaviour nobody built is a feature request: say so in one line and hand it to the `story` skill.

* **Contain first** when it loses or exposes data, or blocks every user in production: tell the person at once with the step that stops the harm, such as a revert, a flag off or a rollback, and take it on their yes.

## Reproduce it

Reproduce it before any fix. Cannot reproduce: never fix blind; ask for the missing fact by name and stop.

## Write it up

On the tracker as one issue labelled `bug`, else in the report:

```text
Title: <what goes wrong, 5 to 8 words>
Given <the starting state, real values>
When <one action>
Then <what should happen>
But <the exact output now>
Severity: live harm | wrong result with a workaround | cosmetic
Entered: <commit or "not found">
Same fault: <each same-rule hit, or "none">
Escape: <each kind below that holds, and what shows it>
Decision: fix now | story | won't fix — <why>
```

## Why it escaped

Name each kind that holds, from the reproduction and the git history, before the fix:

* **Requirements:** no criterion or example covered the input that failed. Name the kind of input.
* **Test:** an example covered it and its test passed the wrong code.
* **Review:** the faulty line was in the diff of the pull request that added it. Name the pull request and the line.
* **Design:** the file has earlier fixes, or the faulty logic is duplicated.
* **Systemic:** a program could detect this kind of fault.

For each kind, propose in one line the check, test or rule that would have caught it. A check beats a written rule. Build a proposal only when the person asks.

## Decide

* **Fix now:** build it by the `build` skill, with these over its steps:
  * The reproduction is the first failing test, its Then the criterion, and running the reproduction again the done check.
  * Each `Same fault:` hit is fixed by the same change.
  * Fix the root cause, not the caller that reported it, unless the person names a fix at a caller: build theirs and note the root cause's `file:line` in one line as a symptom fix.
  * The retro adds the `Escape:` proposals.
* **Story:** by the `story` skill.
* **Won't fix:** only with the person's agreement; close it with the workaround.
