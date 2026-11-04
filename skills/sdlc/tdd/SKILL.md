---
name: tdd
description: "Use only in the build skill's autopilot mode, at its TDD step or when the implementer asks to unlock a locked test: writes one failing test per example, confirms each fails for its reason, commits them alone, has them challenged blind, and settles each unlock."
license: MIT
metadata:
  version: "1.0.0"
---
# TDD

## Words used here

* **Red commit:** a commit holding only tests written before the code.
* **Locked tests:** each test in a red commit and each test that existed before the branch. Change one only to remove its marker once it passes, in a signature commit, in a red commit that lists it on `Changes existing:`, or in a commit of its own whose message names the test, its file and where a person agreed it was wrong or the unlock that allowed it.
* **Signature commit:** a Change Signature refactoring of a stub, alone in a commit whose subject starts `refactor(signature):`; no expected value, fixture or assertion changes.

## Write them

1. **Name** the tests in `docs/glossary.md`'s terms where it exists. Run that area's tests once.
2. **List** one test per example row, plus one each side of each boundary a criterion's rule states, and no other: `<n>. <criterion> — <test name> — <fixture values> — rejects: <a plausible wrong implementation this fixture fails>`.
3. **Write** each through the interface, at the lowest level that shows its result. Never invent a public name.
   * **Expected values** come from the criterion's words, never from what the code does now.
   * **Sociable tests** on production's database engine: double only an outside service, the clock and randomness, preferring the repository's own fake.
   * **Fixtures a wrong implementation fails:** several items with the odd one in the middle, a distinct value per field, no identity values such as quantity 1 or discount 0, unsorted input, more rows than a page, and a unique key per test. An error test asserts the state left behind, not only the raise. Poll with a deadline; never sleep.
   * **Assertions** on exact values a caller sees.
   * **No test** for an example marked `(checked by the user)`. A criterion with no observable result goes on `Questions:`.
4. **Existing tests:** change one only where a criterion states the new behaviour, and list it on `Changes existing:`.
5. **Red:** run them; each fails for the right reason. Mark each failing test with the framework's strict expected-fail marker: pytest `@pytest.mark.xfail(strict=True, reason="red")`, Jest `test.failing`, Vitest `test.fails`, Playwright `test.fail()`, RSpec `pending`, XCTest `XCTExpectFailure("red")`, or Swift Testing `withKnownIssue("red") {` closed by `} // red`. With no such marker, leave them unmarked. One already passing stays unmarked, listed `already passing`, or goes.
6. **Commit** them alone on a branch, never main, the message holding the criteria, the test list and `Changes existing:`. A hook a red test fails is skipped alone, by its id.

## Challenge

Have a fresh subagent challenge the tests blind, given the criteria, the worktree and branch, the interface commit or `none`, the red commit, this file's path and, before any code exists, the holdout directory `<git common dir>/holdout/<branch>/`. Ask each `Disagrees:` line as which reading holds, giving both.

* **Holdout:** never read that directory before the whole suite passes. Then copy its files in at the same paths, commit them alone as a red commit, run them, and remove each marker as its test passes. A failure is a fault in the code.

## Unlock

An implementer that meets a locked test calling an interface the real code does not have returns `unlock: <test> <file>:<line> — assumed <what the test calls> — actual <what exists> — <file:line showing it>`. Settle it yourself; the person is not asked.

1. **Check it deserves it:** grant only when the criterion and every expected value, assertion and fixture value stay as written, and only how the test reaches the code changes: a name, a signature, an import, an argument's shape or a fixture's setup. The evidence must be code from before the branch, the spec or an ADR. When it is code the branch wrote, the code changes to fit the test. Anything else is a `blocked:` line.
2. **Allow:** launch the implementer again with `unlocked: <test> <file>`. It changes only that test's call or setup, alone in a commit whose subject is `test(unlock): <test> — <assumed> → <actual>` and whose message names the file and `agreed: unlock, <evidence file:line>`.
3. **Re-lock:** read that commit's diff: no expected value, assertion or fixture value changed, and no test removed, skipped or marked. Run `python3 scripts/locked_tests.py <merge target> <each red commit>`; the commit must read `own commit`. The test is locked again from the next commit. When either check fails, revert the commit and treat the request as a `blocked:` line.

## Report

```text
Red: <hash>; tests: <paths>; <n> failing, <n> already passing; marker: <marker, or "none">
Tests: <the numbered list>
Changes existing: <test — criterion>, or "none"
Doubles: <each double and why the real one cannot run>, or "none"
Questions: <criterion — what must be decided>, or "none"
```
