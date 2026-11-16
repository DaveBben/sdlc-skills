# Acceptance criteria

Each criterion is one rule with at least one example in Given/When/Then and values from the project's real data. The criteria are the person's; mark one you drafted as yours until they agree it. A `Done when:` line, for a request that names the result and every value it needs, is one result a test or run shows, and needs no example.

* **Examples:** the fewest that show the rule. Where only values vary, keep one Given/When/Then and put the values in a table under it, a column per value. Give results, not the arithmetic behind them. `(checked by the user)` ends a result only an eye can judge; `changes: <old behaviour>` marks a changed one.
* **Terms:** each term the change coins or the reader may not know, defined once there, then used by that one name. Each new one the person confirms goes in `docs/glossary.md`.

## Failure modes

* **Solution as the need:** the story names a screen, widget or technology, such as "add a dropdown" or "use Redis", and no outcome.
* **No real value:** a `so that` that restates the action, such as "so that I can export", or a generic "As a user" where the roles differ.
* **Technical slice:** "build the API" or "add the table", with nothing a person can do once it ships. Slice it vertically instead (INVEST: Valuable).
* **Epic in disguise:** "and" in the title, several roles, create-read-update-delete all at once, or more criteria than one pull request can carry (INVEST: Small). Split it.
* **Hidden dependency:** a criterion that needs another unbuilt story, unstated (INVEST: Independent).
* **Vague criterion:** fast, easy, user-friendly, robust, "handles errors gracefully" or "works correctly": nothing a test can fail (INVEST: Testable). Ask for the number or the event.
* **Two rules in one:** a criterion joined by "and" or "or" whose halves can pass and fail apart.
* **Implementation in the criterion:** tables, endpoints, classes or libraries instead of what a person sees.
* **Example missing or fake:** a criterion with no Given/When/Then, or values such as "foo", "test user" or "X".
* **Imperative steps:** a Given or When written as clicks and keystrokes, such as "Given I click Login and type my password", instead of the state and the one action. Write it declaratively.
* **Several actions:** more than one When in an example; each action is its own example.
* **Invisible Then:** "Then the data is saved" or "Then it is processed", with nothing a person or caller sees. Name what shows.
* **Example follows today's code:** an expected result copied from what the code does now rather than the person's rule, or one that contradicts its own criterion.
* **Happy path only:** an action that saves data or calls another system with no failure example, or no example for a person not allowed to act, an abuse case, empty input or the boundary.
* **Unstated invariant:** a rule that must always hold, such as "a card is never charged twice", left implied instead of its own criterion.
* **Suite-only check:** a way to see it work that only runs the tests, where real data or the running app could show the criteria.
* **Contradicted by the code:** a criterion the code or a decision record contradicts; cite its `file:line`.
* **Unreadable:** a sentence over 25 words, a term in neither `Terms` nor the glossary, or prose describing output a sample could show.

## Written up as a story

On the ticket's issue, else in `docs/stories/<slug>.md`, leaving out empty sections. Context and Terms are only for a reader who was not in the conversation.

```markdown
# Account holder withdraws cash

As a <role>, I want <action> so that <outcome>.

## Context

- <at most 3 bullets: who hits this, today's workaround, why now>

## Terms

- **<term>:** <half-sentence meaning>

## Acceptance criteria

1. A withdrawal up to the balance is paid out from the balance.

   Given a balance of $100\
   When the holder requests $20\
   Then $20 is dispensed and the balance is $80

2. A withdrawal over the balance dispenses nothing.

   Given a balance of $100\
   When the holder requests $120\
   Then nothing is dispensed, "Insufficient funds" shows, and the balance stays $100

## How we will see it work

`<command>`, or <what to do>: <what it shows, on which data or app>

## Out of scope

- Overdraft limits

## Open questions

- <one per line>
```
