# Report to a person

Write each row as a Conventional Comment (conventionalcomments.org). The label is the row's type (`issue`, `suggestion` or `question`), decorated `(blocking)` or `(non-blocking)`, and `security` too for a section 7 row. Put the reading list first, against anchoring on the rows. End with `Agents: no blocking issue.` or `Agents: <n> blocking.`, then `Short read: <n> hunks, about <n> lines.`, `Full read: <n> hunks, about <n> lines.` or `Split: <why>.` Never write `Merge.`: approval is the person's.

```text
<file>:<line>
<label> (<blocking | non-blocking>[, security]): <what goes wrong, in one line>

<the trigger and what a caller sees>. Rests on: <the proof>.
<the fix>
```

## On a merge request

Print the comments, and post them only when the user says to. Anchor each to the one line that must change, on the new side of the diff at the head commit. Name any other line as `<file>:<line>` in the text. A line outside the diff anchors to the changed line that causes it. On GitHub, post a review comment with `line` and `side: RIGHT`.

After a report to a person, for a finding a checker could catch next time: name the check.
