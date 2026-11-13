# Implementation design spec

How the change will be built, written before any test. Put it in a comment on the ticket's issue, else in `SPEC.md` at the worktree root, deleted before the pull request. Keep it to one screen and write only the lines that hold a choice.

```markdown
## Implementation design spec: <key>

Approach: <2 to 4 sentences: how the change works, and why this way>
Changes: <file or module — what changes in it>, one per line
Interfaces: <each signature, endpoint, event or schema added or changed, and who calls it>
Data: <tables, keys or stored formats, and what happens to existing data>
Decided: <choice>, because <reason>. Rejected: <alternative>
One-way doors: <each, with its options as equals>, or none
Tests: <criterion — the level it is tested at — the doubles it needs>
Risks: <what could fail in production, and how it would show>
```
