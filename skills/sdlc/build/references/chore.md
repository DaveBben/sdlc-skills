# A chore, or a refactoring on its own

A chore changes nothing a user or caller can observe. Its criteria are its done-when and every existing test passing unchanged.

* **No interface, red tests or challenge.** Run the check command first and note any test already failing on main. Where no test covers code the chore can affect, commit characterization tests first, alone: the chore's red commit.
* **Existing tests stay as written.** A syntax change the chore forces, or deleting a test of code the chore removes, is a question first; once a person agrees, it goes in a commit of its own naming each test, its file and that agreement.
* **Small steps:** one change, the check command, a commit, the next.
  * **A dependency or runtime:** read the release notes for every version crossed, cross at most one major version, and commit the lock file.
  * **CI, build or config:** use a parallel run where the system allows.
  * **A secret:** never print or commit it; confirm the new one works before revoking the old.
* **A test you cannot pass unchanged** means the chore changed behaviour: stop and hand that change on as a story or bug.
* **A refactoring** follows the `refactor` skill.
* **Pull request body:** also how to undo it.
