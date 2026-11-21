# Tests from criteria

A test earns its place by failing on a wrong implementation. For each one, name a plausible wrong implementation it fails, such as `>` for `>=`, the rule applied to the order instead of the line, or the example's answer returned as a constant. If you cannot, change the fixture or drop the test.

## Red

* **One test per criterion example,** or per row of its table, named for it, such as `test_ac2_ten_units_get_ten_percent_off`, plus one each side of a boundary the rule states where the examples skip a side. None that no criterion asks for.
* **Expected values are literals from the criterion's Then,** worked out by hand where the rule needs arithmetic. A value copied from running the code blesses its bug; one computed in the test with the rule's formula repeats it. Where an example contradicts its rule, or a criterion decides nothing a caller can see, ask.
* **Through the public interface,** the Given set up by the project's own fixtures or entry points. Fake only an outside service, the clock and randomness, with a fake that refuses what the real one refuses. Assert every result in the Then as exact values a caller sees; an error test also asserts the state left behind.
* **Fixtures a wrong implementation fails:** keep the example's values, and around them put several items with the odd one in the middle, a distinct value per field, unsorted input, and no identity values such as quantity 1 or discount 0.
* **Red for the right reason:** the failure shows the criterion's value against what the code does today. An import, collection, fixture or not-implemented error is not that, so a new name first gets a stub that returns nothing, in its own commit.
* **A test that passes before the change** either guards behaviour the change must keep, such as the unchanged side of a boundary, or tests nothing. Break the line it should cover and see it fail; name the ones kept as `already passing` in the commit.
* **The red commit** holds the tests alone, as `test(red): <title>`, with each criterion as an `AC<n>: <rule>` line. After it a test changes only with the person's word: when one looks wrong, or would pass only by branching on its inputs, say so and stop. A changed criterion gets a new red commit.

## A rule over every input

A property test is worth its cost when a criterion's rule says any, every, always or never over inputs no list of examples covers: a round trip (parse then print), an invariant (a split sums to the total) or a simpler model to compare against (the old function for a rewrite). It is not for glue, UI, calls to outside services or a list of business cases. It sits beside the example tests, never in their place, in the repository's own property library, such as Hypothesis, fast-check or proptest.

* **Generate everything the contract allows.** A bound, filter or `assume()` the criterion does not state removes the empty, boundary and huge inputs where the bug sits.
* **State the rule, not the code:** no expected value from the code under test or a copy of its logic, no assertion weaker than the rule, such as `is not None`, and nothing that catches the assertion.
* **The wrong implementations a property lets through are degenerate:** one that returns its input, an empty result or a constant. Tighten it until each fails.
* **A counterexample** is pinned as an example test with its shrunk values. One that shows behaviour no criterion decides is a question for the person, not a bug to fix.

## Where a wrong answer is expensive

Mutation testing is worth its run time for money, permissions, parsing and rules with boundaries, once the tests are green, on the lines this change touched and no wider. Use the repository's tool where it has one, such as mutmut, Stryker, PIT or cargo-mutants. Without one, do it by hand on the lines that hold the rule: flip the comparison, drop the branch or change the constant, see a test fail, and restore the line.

A surviving mutant is one of three things:

* **Behaviour a criterion decides:** add the test, its expected value from the criterion.
* **Behaviour no criterion decides:** code nobody asked for, or a gap in the criteria for the person.
* **No change a caller can see,** an equivalent mutant, often a fifth of survivors or more: name it with the reason.

Never kill a mutant by asserting an internal, a call or a log line a caller cannot see.
