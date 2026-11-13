# A chore, or a refactoring

A chore or refactoring changes nothing a user or caller can observe. Its criteria are its done-when and every existing test passing unchanged.

* **No interface, red tests or challenge.** Run the check command first and note any test already failing on main. Where no test covers code the change can affect, commit characterization tests first, alone: its red commit.
* **Existing tests stay as written.** A syntax change a chore forces is a locked-test change for the person's yes, its evidence the release note. Deleting a test of code the change removes is a question first; once agreed, it goes in its own commit naming each test and that agreement.
* **Small steps,** the check after each:
  * **A refactoring:** one named refactoring per commit, `refactor: <refactoring> (<smell>)`, keeping public names, error handling and comments that explain why.
  * **A dependency or runtime:** read the release notes for every version crossed; cross at most one major version.
  * **CI, build or config:** use a parallel run where the system allows.
  * **A secret:** confirm the new one works before revoking the old.
* **A test you cannot pass unchanged** means the change alters behaviour: stop and hand that change on as its own ticket.
* **Pull request body:** also how to undo it.
