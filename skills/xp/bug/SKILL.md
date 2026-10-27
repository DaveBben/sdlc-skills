---
name: bug
description: "Use first when existing code misbehaves, such as an error, crash, hang, flicker, wrong output, regression or a rule the code fails to enforce, when asked why a kind of bug keeps happening, or when a bug backlog needs triage: reproduces it, files it with why it escaped, and decides fix now, story or won't fix."
license: MIT
metadata:
  version: "1.0.0"
---
# Bug

A bug is shipped behaviour that contradicts what the code was built to do: an acceptance criterion, a documented contract, a crash, an error the caller cannot act on, lost or exposed data, or a slowdown past a stated limit. A defect on a story's unmerged branch is unfinished work there; behaviour nobody built is a story. A bug is reproduced, filed and decided; it never waits open "for later".

* **Contain first** when it loses or exposes data, or blocks a path for every user in production: tell the user at once, and ask, as equals, which step stops the harm: revert, turn off its flag or roll back.
* **The reporter's guess:** when a person reports it here, ask once, as optional, for their guess at the cause, and start reproducing meanwhile.
* **Issues** are read and written through the `tracker` skill.

## Report a bug

1. **Reproduce** it at the lowest level that shows it, and record the exact output. Force an intermittent one's timing, seed or clock until it fails every run, and shrink a large input. Find the commit it entered by `git log -S` or `git bisect run` where cheap. Cannot reproduce: never fix blind; ask for the missing fact by name and stop.
2. **Decide:**
   * **Fix now,** the default: the fix needs no answer from the user.
   * **Story,** by the `story` skill: the fix needs a product decision or changes more than the reproduction. Close the bug as `became #N`.
   * **Won't fix:** the harm costs less than the fix and the user agrees. Close it with the workaround.
   * **Same fault elsewhere:** search other callers and copies; a hit under the same rule is fixed by the same change.
3. **File it,** as one issue labelled `bug` (or the tracker's bug type), else in the report:

```text
Title: <what goes wrong, five to eight words>
Reproduction: Given <the starting state, real values>, when <one action>, then <what should happen>, but <the exact output now>.
Version: <commit or release>; environment: <what it needs>
Severity: live harm | wrong result with a workaround | cosmetic
Entered: <commit or "not found">; missed by: <the story whose criteria missed it, or "none">
Guess: <the reporter's guess, or "none asked">; held | wrong, once the cause is found
Same fault: <each same-rule hit, or "none">
Decision: fix now | story #N | won't fix — <why>
Escape: <by references/escape.md>
```

4. **Find why it escaped** by [references/escape.md](references/escape.md), before the fix.
5. **Fix** it, when decided fix now, with the `build` skill; else the ticket is the hand-off.

## Triage a backlog

Read the open bugs by the user's label or query, else `bug`; past 10, map them by the `tracker` skill for title, reproduction, severity, the reporter's guess and the last comment. Ask one question per bug, with `duplicate of #N` and `cannot reproduce: ask for <fact>` beside the three decisions as equals, reproducing only where the answer turns on it. Find the escape once per group in one file or of one kind. Apply each answer, then show `| Issue | Decision | Escape |`.

## Report

Give the filed ticket, the fix's pull request or "none", and each rule, check, refactor or ADR proposed, or "none".
