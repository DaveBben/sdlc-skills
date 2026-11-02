# Create a story

1. **Find the need:** ask why until the goal names no solution. Offer a cheaper way to it as an option. Where the product has a PRD, check the request against it by the `prd` skill's Check path.
2. **Ask** by SKILL.md's "Questions", in rounds of product questions, until you and the user would write the same criteria. One the user will research goes under `Open questions`.
3. **Propose each criterion,** one at a time: the criterion with its examples, why it may be needed, and the source of that why: the user's words, a rule they stated, a `file:line`, an ADR, or `(guess)`. Ask it as Accept, Reject or Modify. Each `then` comes from the user's words or a rule they stated, never from what the code does today, which carries its bugs into the tests.
4. **Failure examples:** a criterion whose action saves data or calls another system gets an example of that failing, proposed the same way: what the person sees and what is saved. An invariant, such as `a card is never charged twice`, is its own criterion.
5. **Write it** in this form, leaving out empty sections:

```text
Title: Account holder withdraws cash
As a <role>, I want <action> so that <outcome>.
Context: <who hits this, today's workaround, why now, a link>

Acceptance criteria
1. A withdrawal up to the balance dispenses it and reduces the balance by the same amount.
   Given the balance is $100, when they request $20, then it dispenses $20 and the balance is $80.
2. ...

Out of scope: overdraft limits
Open questions: <one per line>
Contacts: Product @mchen; Engineering @okafor
Measure: <the number that shows the `so that`: where to read it, now, target, date>
```

* **Product language:** the terms in `docs/glossary.md`, no technology or code names; a number or event, never faster or robust.
* **New terms:** each one the user confirms goes in `docs/glossary.md`, in the form its entries use.
* **Examples:** one action each, every fact the outcome depends on in its Given, and a boundary value per range. `(checked by the user)` ends a result only an eye can judge; `changes: <old behaviour>` marks a changed one.

6. **Ask what was missed:** "Is there a criterion we have not considered?" Propose each one they name like step 3.
7. **Review it blind:** have a fresh subagent, given only the story, the titles of the stories already filed, this file, split.md and SKILL.md's Review path, review it by that path and return its report; it changes nothing. Read each quote before keeping its finding, then propose each kept fix like step 3.
8. **Agree it:** show its `Decided:` lines, and ask each part no answer settled, such as `so that` or `Measure:`. File it by SKILL.md. Its spec waits until the `build` skill picks it up.
