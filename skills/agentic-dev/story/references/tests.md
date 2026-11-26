# Tests from criteria

A test earns its place by failing on a wrong implementation. For each one, name a plausible wrong implementation it fails, such as `>` for `>=`, the rule applied to the whole instead of each item, or the example's answer returned as a constant. If you cannot, change the fixture or drop the test.

## Red

* **One test per criterion example,** or per row of its table, named for its criterion, such as `test_ac2_limit_of_3_rejects_the_fourth`, so a run of `AC2` selects it, plus one each side of a boundary the rule states where the examples skip a side. None that no criterion asks for.
* **Expected values are literals from the criterion's Then,** worked out by hand where the rule needs arithmetic. A value copied from running the code blesses its bug; one computed in the test with the rule's formula repeats it. Where an example contradicts its rule, or a criterion decides nothing a caller can see, ask.
* **Through the public interface,** the Given set up by the project's own fixtures or entry points. Fake only an outside service, the clock and randomness, with a fake that refuses what the real one refuses. Assert every result in the Then as exact values a caller sees; an error test also asserts the state left behind.
* **Fixtures a wrong implementation fails:** keep the example's values, and around them put several items with the odd one in the middle, a distinct value per field, unsorted input, and no identity values, such as 1 for a factor, 0 for an offset or an empty string.
* **Red for the right reason:** the failure shows the criterion's value against what the code does today. An import, collection, fixture or not-implemented error is not that, so a new name first gets a stub that returns nothing, in its own commit.
* **A test that passes before the change** either guards behaviour the change must keep, such as the unchanged side of a boundary, or tests nothing. Break the line it should cover and see it fail; mark each one kept `already passing` in a comment above it.
* **Leave the tests uncommitted:** they are moved out of the tree and hidden from the agents that write the code. After that a test changes only with the person's word: when one looks wrong, or would pass only by branching on its inputs, say so and stop. A changed criterion gets new tests.

## A rule over every input

A property test is worth its cost when a criterion's rule says any, every, always or never over inputs no list of examples covers: a round trip (parse then print), an invariant (a split sums to the total) or a simpler model to compare against (the old function for a rewrite). It is not for glue, UI, calls to outside services or a list of business cases. It sits beside the example tests, never in their place, in the repository's own property library, such as Hypothesis, fast-check or proptest.

* **Generate everything the contract allows.** A bound, filter or `assume()` the criterion does not state removes the empty, boundary and huge inputs where the bug sits.
* **State the rule, not the code:** no expected value from the code under test or a copy of its logic, no assertion weaker than the rule, such as `is not None`, and nothing that catches the assertion.
* **The wrong implementations a property lets through are degenerate:** one that returns its input, an empty result or a constant. Tighten it until each fails.
* **A counterexample** is pinned as an example test with its shrunk values. One that shows behaviour no criterion decides is a question for the person, not a bug to fix.

## A rule with no single right answer

A threshold criterion, a metric over a labelled sample, becomes an eval: a test that scores the output against that sample and fails below the criterion's threshold.

* **Commit the labelled sample** as a fixture, with who labelled it. Choose settings on other data: a setting tuned on the sample the test scores has passed an exam it already saw.
* **Take the threshold from the criterion,** never from a run: one set just below today's score blesses today's output.
* **Pin the seed and the model or library version.** Where output changes by seed, score the runs against each other by the criterion's stability bar.
* **Pair the metric with a check a degenerate output fails,** such as a size range for groups: every item alone or everything in one group scores well on some metrics. The criterion's `by eye:` read stays with the person.
* **Run a slow or paid eval outside the default suite,** named in the definition of done with when it runs.

## Where a wrong answer is expensive

Mutation testing is worth its run time for money, permissions, parsing and rules with boundaries, once the tests are green, on the lines this change touched and no wider. Use the repository's tool where it has one, such as mutmut, Stryker, PIT or cargo-mutants. Without one, do it by hand on the lines that hold the rule: flip the comparison, drop the branch or change the constant, see a test fail, and restore the line.

A surviving mutant is one of three things:

* **Behaviour a criterion decides:** add the test, its expected value from the criterion.
* **Behaviour no criterion decides:** code nobody asked for, or a gap in the criteria for the person.
* **No change a caller can see,** an equivalent mutant, often a fifth of survivors or more: name it with the reason.

Never kill a mutant by asserting an internal, a call or a log line a caller cannot see.
