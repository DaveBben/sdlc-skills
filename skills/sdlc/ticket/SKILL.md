---
name: ticket
description: "Use when work is to be written down for later instead of built now: a user story, a bug report or a spike to file in a tracker or docs/tickets/, such as 'write a story for X', 'file a bug: Y', 'log a spike on Z for later', 'turn these notes into a ticket' or 'critique this story'. A short ticket template."
license: MIT
metadata:
  version: "4.1.0"
---
# Ticket

A ticket holds work for later. Work done now needs none. File it in the person's tracker, else `docs/tickets/<slug>.md`. Keep it to 15 lines and at most 3 criteria; leave out empty lines. Show the draft and file it once the person accepts it.

```markdown
# <title>

Type: story | bug | spike
<what> so that <why>. For: <who, when it matters>

- <context, at most 3 bullets: who hits this, today's workaround, why now>

AC1: <a rule a test can decide>
  Given <state, and how it came about> When <one action> Then <every result the rule decides that a caller sees>

Open: <a question the person must answer, one per line>
```

* **Bug:** AC1 is the reproduction, its Then the expected result, followed by `Actual: <what happens now>`.
* **Spike:** in place of criteria, `Question: <an outcome that can fail, with its bar>` and `Decides: pass → <step>; fail → <step>`.
* **The why is the person's:** when the notes lack it, it goes under `Open:`.
* **Critique:** give each problem as a finding with the case it breaks, for the person to keep or drop, never a score or a verdict. Look first for a missing or restated why, several asks joined by "and", a Given that can come about several ways, and a Then that states one sign of the result.
