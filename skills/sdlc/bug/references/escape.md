# Find why a bug escaped

Name each kind that holds from the reproduction and the git history:

* **Requirements:** no example covered the input that failed. Name the kind of input. When the history shows it escaped before, propose a rule a check enforces, else a line for `AGENTS.md`.
* **Test:** an example covered it and its test passed the wrong code. The fix's failing test closes it.
* **Review:** the faulty line was in the diff of the pull request holding the `Entered:` commit. Name the pull request, the line, its `Built:` line, and who approved and merged; show the user that hunk as the pull request showed it.
* **Design:** the file has earlier fixes in `git log --oneline -- <file>`, or the faulty logic is duplicated. Propose a refactor as its own change, by the `refactor` skill.
* **Systemic:** a program could detect this kind of fault. Propose the check.
* **Accepted risk:** the hazard was known and taken. Propose recording it by the `adr` skill when no ADR holds it.

Write the kinds and what shows each on the ticket's `Escape:` line. Give each proposal as a one-line note in the report; build one only when the person asks for it.

For "why do we keep getting these bugs": read every `bug` issue, past 10 mapped by the `tracker` skill for `Escape:`, `Entered:` and the faulty file; group by escape kind, by file, and for review escapes by build mode; propose one change for the largest group.
