# Gitea

* **Blocking relation:** issue dependencies, `POST /repos/{o}/{r}/issues/{n}/dependencies`; issue `n` is blocked by the issue in the body.
* **Subtask relation:** none built in. File an issue labelled `subtask` and make the story depend on it, so the story is blocked by each of its subtasks.
* **Board placement:** a separate container. Check the swagger for a projects endpoint (added in v28.0.0). Where it exists: `POST /repos/{o}/{r}/projects/{id}/columns/{col}/issues/{issue_id}`, where `issue_id` is the issue's global `id`, not its `#` index. Where it does not: tell the user to tick the issues in the Issues tab, then Project, then the board's name.
* **State:** on a board, where the projects endpoint exists, the column of that state, moved by the same endpoint. Otherwise an exclusive label, `status/draft`, `status/todo`, `status/in-progress`, `status/in-review` or `status/testing`, created with `exclusive: true` so Gitea keeps one per issue. Done closes the issue.
