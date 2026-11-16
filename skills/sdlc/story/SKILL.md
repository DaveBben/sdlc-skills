---
name: story
description: "Use when the person wants a user story written, or something turned into a user story, such as 'write a story for X', 'turn this ticket into a user story' or 'write this up as a user story'. A template for a user story."
license: MIT
metadata:
  version: "3.2.0"
---
# Story

Here is the story template. Leave out empty sections.

```markdown
# Account holder withdraws cash

As a <role>, I want <action> so that <outcome>.

## Context

- <at most 3 bullets: who hits this, today's workaround, why now>

## Terms

- **<term>:** <half-sentence meaning>

## Acceptance criteria

AC1: A withdrawal up to the balance is paid out from the balance.

   Given a balance of $100\
   When the holder requests $20\
   Then $20 is dispensed and the balance is $80

AC2: A withdrawal over the balance dispenses nothing.

   Given a balance of $100\
   When the holder requests $120\
   Then nothing is dispensed, "Insufficient funds" shows, and the balance stays $100

## Done when

Done when: `<command that exits 0 only when its result holds>`
Done when (checked by you): <what to look at, and what it must show>

## Out of scope

- Overdraft limits

## Open questions

- <one per line>
```
