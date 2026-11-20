---
name: bug
description: "Use first when a bug is to be reported, reproduced, triaged or explained instead of fixed now, such as 'file a bug: Y', 'write this up, don't fix it yet', 'can you reproduce what the customer saw', 'triage the open bugs', 'how did this get past the tests and the review' or 'why do we keep getting bugs like this'. Not for fixing one: a request to fix misbehaving code is the build skill's, even when it starts from a bug report. Reproduces the bug with a check that fails for the reported symptom, files a short report with a severity and a decision, and for a bug that reached users names the check that should have caught it."
license: MIT
metadata:
  version: "5.0.0"
---
# Bug

A bug is merged behaviour that contradicts what the code was built to do: an acceptance criterion, a documented contract, a crash, lost data. A defect on an unmerged branch is unfinished work there. Behaviour nobody built is a feature request: say so in one line; it is a story.

* **Contain first** when it loses or exposes data, or blocks a path for every user in production: tell the person at once with the step you would take to stop the harm (revert, turn off its flag, roll back), and take it on their yes.
* **A report missing** its reproduction, its expected result or its environment: ask for each by name before anything else. The default is to guess and patch.

## Reproduce

* **Executable:** a failing test or one command at the lowest level that shows it, not prose steps. Shrink a large input (delta debugging); make an intermittent one deterministic by pinning the seed, clock or order, and record how often it failed before.
* **Red for the reported reason:** the failing run shows the symptom in the report. A check that fails some other way goes green later with the bug still in.
* **Confirmed means you ran it,** and the failing output is pasted in the report. A fault you or another agent only read in the code is filed `unconfirmed`. When it will not reproduce, ask for the missing fact by name and stop.
* **Where it entered:** `git bisect run` on the reproduction, or `git log -S`, where cheap. Read the introducing commit's story or ticket: the fix has to keep what that change set out to do.
* **Same fault elsewhere:** search the other callers and copies of the faulty logic and list each hit.

## Report

One bug per report, as an issue labelled `bug` where a tool here reaches the team's tracker, else `docs/bugs/<slug>.md`:

```text
Title: <what goes wrong, not the fix; under 60 characters>
Reproduction: <the command or test that fails>
Expected: <the result, and the criterion or contract it comes from>
Actual: <the exact output, pasted>
Unchanged: <nearby behaviour the fix must keep>
Environment: <commit or release, and what it needs>; fails <always | n runs in m>
Severity: live harm | wrong result with a workaround | cosmetic
Entered: <commit and its story, or "not found">
Guess: <suspected file or function, and a direction for the fix; or "none">
Same fault: <each hit, or "none">
Decision: fix now | fix by <date> | story | won't fix: <why, and the workaround> | duplicate of <id> | cannot reproduce: needs <fact>
Escape: <for a bug that reached users, by references/escape.md>
```

* **Severity** is the harm. Priority, its order against other work, is the owner's.
* **Guess** is a hypothesis and labelled as one. Ask the reporter for theirs once, as optional: agents resolve more reports that carry a suspected location.
* **Decision:** every bug leaves with one; none is parked for a vague later. `fix now` is the default when the fix fits one small merge request and needs no product decision. One that needs a product decision, spans features or will not fit becomes a story, by the `story` skill, and closes as `became <id>`. `won't fix` needs the owner's yes.

A backlog of them: [references/triage.md](references/triage.md). Why one got out, or why a kind keeps coming: [references/escape.md](references/escape.md).

## To build

This skill stops at the report. The fix is a build, and the report is its frame: the reproduction is the first failing check, already seen red, and the fix is done when that check is green and `Unchanged` still holds, both runs shown. `Expected` and `Unchanged` are the criteria in the review's `story.md`.
