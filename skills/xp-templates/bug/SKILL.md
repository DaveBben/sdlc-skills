---
name: bug
description: "Use when a bug is to be reported, reproduced, confirmed, reviewed, triaged or filed, not fixed: writing one up, checking whether behaviour is a bug or expected, confirming it is real before raising it, finding its cause for the report, critiquing a bug report, judging severity or which of several issues matters most, or explaining how one escaped, such as 'file a bug: Y', 'write this up, don't fix it yet', 'can you reproduce what the customer saw', 'is this bug report complete', 'triage the open bugs', 'how did this get past the tests and the review' or 'why do we keep getting bugs like this'. Not for fixing one. Holds the bug report template built on a reproduction that fails for the reported symptom, with a severity and a decision, the triage table, and the escape analysis for a bug that reached users."
license: MIT
metadata:
  version: "1.1.0"
---
# Bug

A bug is merged behaviour that contradicts what the code was built to do: an acceptance criterion, a documented contract, a crash, lost data. A defect on an unmerged branch is unfinished work on that branch. Behaviour nobody built is a feature request: say so in one line and write it as a story.

* **Contain first** when it loses or exposes data, or blocks every user: tell the person at once the containment action (revert, flag off, roll back, yank the release), and take it on their yes.
* **Ask by name for each missing piece** of a report: its reproduction steps, expected result or environment.

## Reproduce

* **Write a minimal reproduction:** a failing test or one command, at the lowest level, that shows the reported symptom. Shrink a large input by delta debugging. Make a flaky one deterministic by pinning the seed, clock or order, and record how often it failed before.
* **Confirmed means you ran it.** File a fault only read in the code as `unconfirmed`. When it will not reproduce, ask for the missing fact by name and stop.
* **Find where it entered,** where cheap, by `git bisect run` on the reproduction or `git log -S`, and name what the introducing commit's story set out to do under `Unchanged`.
* **Run variant analysis:** search the faulty logic's callers and copies for the same fault.

## Report

One bug per report, as an issue labelled `bug`, filed by the tracker skill where a tool here reaches the team's tracker, else `docs/bugs/<slug>.md`:

```text
Title: <what goes wrong, not the fix; under 60 characters>
Reproduction: <the command or test that fails>
Expected: <the result, and the criterion or contract it comes from>
Actual: <the exact output, pasted>
Unchanged: <nearby behaviour the fix must keep>
Environment: <commit or release, and what it needs>; fails <always | n runs in m>
Severity: live harm | wrong result, no workaround | wrong result with a workaround | cosmetic
Entered: <commit and its story, or "not found">
Root cause: <confirmed | suspected>: <the file or function, and a direction for the fix>; or "unknown"
Same fault: <each hit, or "none">
Decision: fix now | fix by <date> | story | won't fix: <why, and the workaround> | duplicate of <id> | cannot reproduce: needs <fact>
Escape: <for a bug that reached users, by references/escape.md>
```

* **Set severity, not priority:** priority is the owner's.
* **Root cause** is `confirmed` only when the reproduction or bisect shows it.
* **Decision:** `fix now` is the default for a fix that fits one small merge request and needs no product decision. One that needs a product decision or will not fit one merge request becomes a story, by the story skill, and closes as `became <id>`. `won't fix` needs the owner's yes.

## Review one

Report `<bug>: <rule broken> — "<quoted text>" — <fix>` per finding.

* **A missing line** of the template, above all the reproduction, `Expected` with its source, or `Unchanged`.
* **A reproduction nobody ran,** or one that fails for another reason than the reported symptom.
* **A title that names the fix,** or several bugs in one report.
* **`confirmed` without proof:** a root cause the reproduction or bisect does not show.
* **Priority in place of severity.**
* **A feature request:** behaviour nobody built.

A backlog of them: [references/triage.md](references/triage.md). Why one got out, or why a kind keeps coming: [references/escape.md](references/escape.md).
