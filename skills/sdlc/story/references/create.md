# Create a story

The user writes the story; you show them what affects it and critique what they write. Draft a criterion only when they ask, and mark it as yours.

1. **Find the need:** five whys, until the goal names no solution. Offer a cheaper way to it as an option. Where the product has a PRD, check the request against it by the `prd` skill's Check path.
2. **Show what affects it:** read the code the need touches, its tests, each ADR in force and `AGENTS.md`. Tell the user in plain sentences how what is already built or decided shapes this story, each with its `file:line`, such as "An ADR chose Haiku for cost and a test locks it, so Sonnet reverses that decision." Effects only, never a criterion or an approach.
3. **The user writes the criteria:** 3 to 5, each one rule with an examples table in values from the project's real data. More than 5 is a story to split by [split.md](split.md). A question they will research goes under `Open questions`.
4. **Critique them** against INVEST, in one list of `AC<n>: <problem> — <fix>` for the user to rewrite, until none remain. Also flag:
   * an example missing, not in real values, or whose result follows today's code instead of the user's rule;
   * a criterion the facts from step 2 contradict;
   * an action that saves data or calls another system with no failure row: what the person sees and what is saved;
   * an invariant, such as `a card is never charged twice`, not stated as its own criterion;
   * a sentence over 25 words, a term neither in `Terms` nor the glossary, or prose describing output a sample could show.
5. **Write it** in this form, leaving out empty sections:

```markdown
# Account holder withdraws cash

As a <role>, I want <action> so that <outcome>.

## Context

- <at most 3 bullets: who hits this, today's workaround, why now>

## Terms

- **<term>:** <half-sentence meaning>

## Acceptance criteria

1. A withdrawal up to the balance dispenses it and reduces the balance by the same amount.

   | Balance | Requests | Dispenses | Balance after |
   |---|---|---|---|
   | $100 | $20 | $20 | $80 |
   | $100 | $120 | nothing, shows "Insufficient funds" | $100 |

2. ...

## Out of scope

- Overdraft limits

## Open questions

- <one per line>

Contacts: Product @mchen, Engineering @okafor\
Measure: <the number that shows the `so that`>, read in <where>, now <value>, target <value> by <date>
```

* **Product language:** the terms in `docs/glossary.md`, no technology or code names; a number or event, never faster or robust.
* **Terms:** each term the story coins or the reader may not know, defined once there, then used by that one name. Each new one the user confirms goes in `docs/glossary.md`.
* **Examples:** the fewest rows that show the rule, one action each. A column per value that varies; a value every row shares goes in the criterion. Give results, not the arithmetic behind them. Boundaries go to the tests; missing data and ties get a one-line rule, not rows. `(checked by the user)` ends a result only an eye can judge; `changes: <old behaviour>` marks a changed one.
* **Output:** a criterion about what the person sees shows one sample of it, such as a row of the list.
* **Context:** what the reader needs to judge the story, never how it was found.

6. **Ask what was missed,** and critique each one they add like step 4.
7. **Review it blind:** a fresh subagent, given only the story, the titles of stories already filed, and the Review path with this file and split.md, reviews it and changes nothing. Check each quote before giving its finding to the user to fix.
8. **Agree it:** show its `Decided:` lines, and ask each part no answer settled, such as `so that` or `Measure:`. File it by SKILL.md.
