# Acceptance criteria

Each criterion is one rule with at least one example in Given/When/Then and values from the project's real data. The criteria are the person's; mark one you drafted as yours until they agree it. A request that names the result and every value it needs has no examples; its `Done when:` lines stand in for them.

* **Examples:** the fewest that show the rule. Where only values vary, keep one Given/When/Then and put the values in a table under it, a column per value. Give results, not the arithmetic behind them. `(checked by the user)` ends a result only an eye can judge; `changes: <old behaviour>` marks a changed one.
* **Terms:** each term the change coins or the reader may not know, defined once there, then used by that one name. Each new one the person confirms goes in `docs/glossary.md`.

## The acceptance file

`docs/acceptance/<key>.md`, committed with the failing tests:

```markdown
# <key>: <title>

AC1: A withdrawal over the balance dispenses nothing.
  Given a balance of $100
  When the holder requests $120
  Then nothing is dispensed, "Insufficient funds" shows, and the balance stays $100

Done when: `<command that exits 0 only when its result holds>`
Done when (checked by you): <what to look at, and what it must show>
```

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
* **Suite-only `Done when:`:** one that only runs the tests, where real data or the running app could show it.
* **`Done when:` a person must judge:** a result such as "looks right" or "works", with no exact output a run can match.
* **Contradicted by the code:** a criterion the code or a decision record contradicts; cite its `file:line`.
* **Unreadable:** a sentence over 25 words, a term in neither `Terms` nor the glossary, or prose describing output a sample could show.
