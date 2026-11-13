# Failing tests

When the change adds a signature, first commit it as a stub whose body only raises, so each test runs through the real interface.

1. **Name** the tests in `docs/glossary.md`'s terms where it exists.
2. **List** one test per example, or per row of an example's table, plus one each side of each boundary a criterion's rule states, and no other: `<n>. <criterion> — <test name> — <fixture values> — rejects: <a plausible wrong implementation this fixture fails>`.
3. **Write** each through the interface, at the lowest level that shows its result. Never invent a public name.
   * **Expected values** come from the criterion's words, never from what the code does now. An example that contradicts its criterion's rule goes on `Questions:`, quoting both.
   * **Sociable tests** on production's database engine: double only an outside service, the clock and randomness, preferring the repository's own fake.
   * **Fixtures a wrong implementation fails:** several items with the odd one in the middle, a distinct value per field, no identity values such as quantity 1 or discount 0, unsorted input, more rows than a page, and a unique key per test. An error test asserts the state left behind, not only the raise. Poll with a deadline; never sleep.
   * **Assertions** on exact values a caller sees.
   * **No test** for an example marked `(checked by the user)`. A criterion with no observable result goes on `Questions:`.
4. **Existing tests:** change one only where a criterion states the new behaviour, and list it on `Changes existing:`.
5. **Red:** run them; each fails for the right reason. One already passing is listed `already passing`, or goes.
6. **Commit** them alone on the branch, never main, the message starting `test(red):` and holding the criteria, the test list and `Changes existing:`: the red commit. A commit hook a red test fails is skipped alone, by its id.

```text
Red: <hash>; tests: <paths>; <n> failing, <n> already passing
Tests: <the numbered list>
Changes existing: <test — criterion>, or "none"
Doubles: <each double and why the real one cannot run>, or "none"
Questions: <criterion — what must be decided — your pick>, or "none"
```
