# Break a story into subtasks

Read the story and the code it lands on. Pick one of these four, in this fixed order, with its reason, and go on; the user may name another:

1. **Smaller stories,** by split.md: each person owns a slice that ships alone.
2. **Pair or mob on it:** for a story that will not split and is complex or risky; it costs more person-hours.
3. **Subtasks along boundaries, interface first:** the contract subtask blocks the rest, then each person builds a part that rarely touches the others'.
4. **Subtasks by layer,** such as frontend and backend: nothing works end to end until the last lands.

For subtasks:

* **Two subtasks editing one file** are one subtask.
* **Coverage:** every criterion is covered by a subtask, and no subtask adds behaviour the story lacks.
* **Done:** the story is done when its criteria hold, not when its subtasks close.
* **Each one says only:**

```markdown
Title: <a verb and what it delivers>
Delivers: <what exists when it is done>
Story: <key>; covers acceptance criteria <numbers>
Done when: <the observable result, test or check>
```

List each as a `Decided:` line and file them by the `tracker` skill as subtasks of the story, or as a `[ ]` checklist in `docs/stories/<slug>.md`. Ask each assignee's handle; leave a subtask unassigned when they name nobody. A subtask assigned to a person leaves the story to people: a build skips it.
