# GitHub

* **Blocking relation:** "blocked by" relationships, never sub-issues.
* **Subtask relation:** a sub-issue of the story, `POST /repos/{o}/{r}/issues/{n}/sub_issues` with `sub_issue_id` set to the subtask's global `id`, not its `#` number.
* **Board placement:** a separate container; `gh project item-add`, or the project's auto-add workflow.
* **State:** on a Projects board, the item's Status field: `gh project item-edit --id <item> --project-id <project> --field-id <Status> --single-select-option-id <option>`, with the ids from `gh project field-list` and `gh project item-list`. Off a board, a label `status: draft`, `status: todo`, `status: in progress`, `status: in review` or `status: testing`. Done closes the issue.
