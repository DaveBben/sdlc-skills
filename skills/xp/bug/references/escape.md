# Find why a bug escaped

Once the bug is reproduced and decided, before the fix, name each kind that holds from the reproduction and the git history:

* **Requirements:** no example covered the input that failed, such as a coupon larger than the cart. Name the kind of input. When the history shows it escaped before, propose a rule a check enforces, else a line for `AGENTS.md`.
* **Test:** an example covered it and its test passed the wrong code. The fix's failing test closes it.
* **Review:** the faulty line was in the diff of the pull request holding the `Entered:` commit. Name the pull request, the line, the review's tier, whether the hunk was on its reading list, its rows, who approved and who merged. Show the user that hunk as the pull request showed it.
* **Design:** the file has earlier fixes in `git log --oneline -- <file>`, or the faulty logic is duplicated. Propose a refactor as its own change, by the `refactor` skill.
* **Systemic:** a program could detect this kind of fault, such as an unchecked null or a missing migration. Propose the check.
* **Accepted risk:** the hazard was known and taken. Propose recording it by the `adr` skill when no ADR holds it.

Write the kinds and what shows each on the ticket's `Escape:` line. Propose only; build none without the user's yes to it.

For "why do we keep getting these bugs": read the closed and open `bug` issues, past 10 mapped by the `tracker` skill for the `Escape:` line, the `Entered:` line and the file the fault was in, group them by escape kind, by file, and for review escapes by tier and whether the hunk was on the reading list, then propose one change for the largest group.
