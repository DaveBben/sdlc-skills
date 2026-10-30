# Break a story into subtasks

Read the story whole, with its spec and the code it lands on. Show these four options in this fixed order, which is the same for every story and is not your pick, and ask which the user wants:

1. **Smaller stories,** by split.md: each person owns a slice that ships alone.
2. **Pair or mob on it:** for a story that will not split and is complex or risky; it costs more person-hours.
3. **Subtasks along boundaries, interface first:** fix the contract the parts meet at, then each person builds a part that rarely touches the others'.
4. **Subtasks by layer,** such as frontend and backend: each waits on another, and nothing works end to end until the last lands.

For subtasks:

* **Interface first:** the subtask that fixes the contract blocks the rest. Two subtasks editing one file are one subtask.
* **Coverage:** every criterion is covered by a subtask, and no subtask adds behaviour the story lacks. The spec stays on the story.
* **Done:** the story is done when its criteria hold, not when its subtasks close.
* **Each one says only:**

```markdown
Title: <a verb and what it delivers>
Delivers: <what exists when it is done>
Story: <key>; covers acceptance criteria <numbers>
Done when: <the observable result, test or check>
```

List each as a `Decided:` line and file them through the `tracker` skill as subtasks of the story, or as a `[ ]` checklist under the story in `docs/stories/<slug>.md`. Ask for each assignee's handle, and leave a subtask unassigned when they name nobody. A subtask assigned to a person leaves the story to people: a build skips it.
