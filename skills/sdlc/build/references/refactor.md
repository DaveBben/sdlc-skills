# Refactoring

The goal is code a reader can predict: from its names and shape alone they can tell what it does and where the next change goes. Judge each step by that, never by line count or a metric.

## What to refactor

* **Code you are about to change** (preparatory refactoring): make the change easy, then make the easy change.
* **Code you struggled to understand:** once you understand it, put that understanding into names and structure so the next reader does not repeat the work.
* **Hotspots,** when asked where to clean up: the files with the most commits and churn over the last year. Files that change together with no import between them share a hidden concept; give it one home.
* **Smells that stop a reader predicting the code:** a name that hides what a thing holds or does, a function working at several levels of abstraction, deep nesting (guard clauses), the same rule written in 2 places (shotgun surgery), a comment explaining what the next lines do (extract and name them), a flag argument, a data clump, primitive obsession, feature envy, magic numbers and dead code.

## What to leave

* **Code no change touches and nobody needs to read,** however it looks.
* **Coincidental duplication:** code that looks alike but changes for different reasons. Duplication is cheaper than the wrong abstraction; wait for the rule of three.
* **Length alone,** when the code reads straight through.
* **Code due for deletion.**
* **Indirection for a future no ticket asks for** (speculative generality). Inline as readily as you extract.
* **What a formatter or linter owns.**

## Refactor safely

* **Green first:** run the check and note any test already failing on main.
* **Characterization tests:** where no test covers code the refactoring can affect, commit tests of what it does now, alone, first.
* **One named refactoring per commit,** `refactor: <refactoring> (<smell>)`, with the check after each. Re-read for the smell it targeted; still there means the wrong refactoring, so revert it. Keep public names, except one the person asked to change, and keep error handling and comments that explain why. Change a name or signature that callers outside the repository use by parallel change.
* **Existing tests stay as written.** Deleting a test of code the refactoring removes is a question first; once agreed, it goes in its own commit naming each test.
* **Two hats:** a bug found mid-refactoring is a one-line note, fixed after as its own change, never in it.
* **A test you cannot pass unchanged** means the change alters behaviour: stop and hand that change on as its own.
* **After a green test** inside a build, refactor only code the change touches.
