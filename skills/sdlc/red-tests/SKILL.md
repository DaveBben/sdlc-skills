---
name: red-tests
description: "Use first whenever a test must be added or corrected before code or a fix changes, such as a regression or failing test for a bug, test-first work, a challenge to existing tests, or a locked test that looks wrong: writes one test per example, confirms each fails for its reason, and commits them alone."
license: MIT
metadata:
  version: "1.0.0"
---
# Red tests

Write a change's tests from its criteria before the code exists, and commit them so the code must meet them unchanged.

## Words used here

* **Red commit:** a commit holding only tests written before the code.
* **Locked tests:** each test in a red commit and each test that existed before the branch. Change one only to remove its marker once it passes, in a signature commit, in a red commit that lists it on `Changes existing:`, or in a commit of its own whose message names the test, its file and where a person agreed it was wrong.
* **Signature commit:** a Change Signature refactoring of a stub, alone in a commit whose subject starts `refactor(signature):`; no expected value, fixture or assertion changes.

## Write them

1. **Read** the interface, the nearby tests, and `docs/glossary.md` where it exists, and name the tests in its terms. Run that area's tests once.
2. **List** one test per example, and no other: `<n>. <criterion> — <test name> — <fixture values> — rejects: <a plausible wrong implementation this fixture fails>`.
3. **Write** each through the interface, at the lowest level that shows its result. Never invent a public name.
   * **Expected values** come from the criterion's words, never from what the code does now.
   * **Sociable tests** on production's database engine: double only an outside service, the clock and randomness, preferring the repository's own fake.
   * **Fixtures a wrong implementation fails:** several items with the odd one in the middle, a distinct value per field, no identity values such as quantity 1 or discount 0, unsorted input, more rows than a page, and a unique key per test. An error test asserts the state left behind, not only the raise. Poll with a deadline; never sleep.
   * **Assertions** on exact values a caller sees, never on private calls, call order or logs.
   * **No test** for an example marked `(checked by the user)`. A criterion with no observable result goes on `Questions:`.
4. **Existing tests:** change one only where a criterion states the new behaviour, and list it on `Changes existing:`.
5. **Red:** run them. Each must fail because the behaviour is missing, not from a typo, import or fixture. Mark each failing test with the framework's strict expected-fail marker: pytest `@pytest.mark.xfail(strict=True, reason="red")`, Jest `test.failing`, Vitest `test.fails`, Playwright `test.fail()`, RSpec `pending`, XCTest `XCTExpectFailure("red")`, or Swift Testing `withKnownIssue("red") {` closed by `} // red`. With no such marker, leave them unmarked. One that already passes stays unmarked, listed `already passing`, or goes.
6. **Commit** them alone on a branch, never main, the message holding the criteria, the test list and `Changes existing:`. A hook a red test fails is skipped alone, by its id.

## Challenge

Have a fresh subagent challenge the tests blind, given the criteria, the worktree and branch, the interface commit or `none`, the red commit, this file's path, and, before any code exists, the holdout directory `<git common dir>/holdout/<branch>/`. It returns `Questions:` and `Disagrees:` lines: ask each disagreement as which reading holds, giving both. To challenge tests a person wrote, commit them first and write none yourself.

* **Holdout:** never read that directory before the whole suite passes. Then copy its files in at the same paths, commit them alone as a red commit, run them, and remove each marker as its test passes. A failure is a fault in the code.

## Report

```text
Red: <hash>; tests: <paths>; <n> failing, <n> already passing; marker: <marker, or "none">
Tests: <the numbered list>
Changes existing: <test — criterion>, or "none"
Doubles: <each double and why the real one cannot run>, or "none"
Questions: <criterion — what must be decided>, or "none"
```
