---
name: ticket
description: "Use when work is to be written down for later instead of built now: a user story, a bug report or a spike to file in a tracker or docs/tickets/, such as 'write a story for X', 'file a bug: Y', 'log a spike on Z for later', 'turn these notes into a ticket' or 'critique this story'. A short ticket template."
license: MIT
metadata:
  version: "4.0.0"
---
# Ticket

A ticket holds work for later. Work done now needs none. File it in the person's tracker, else `docs/tickets/<slug>.md`. Keep it to 15 lines and at most 3 criteria; leave out empty lines.

```markdown
# <title>

Type: story | bug | spike
<what> so that <why>. For: <who, when it matters>

- <context, at most 3 bullets: who hits this, today's workaround, why now>

AC1: <a rule a test can decide>
  Given <state> When <one action> Then <what a person or caller sees>

Open: <a question the person must answer, one per line>
```

* **Bug:** AC1 is the reproduction, its Then the expected result, followed by `Actual: <what happens now>`.
* **Spike:** in place of criteria, `Question: <an outcome that can fail, with its bar>` and `Decides: pass → <step>; fail → <step>`.
