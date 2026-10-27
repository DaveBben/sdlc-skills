# GitLab

* **Blocking relation:** `blocks` issue links, on Premium and above. Free has only `relates to`: tell the user and ask.
* **Subtask relation:** a Task work item with the story's issue as its parent, where the instance's version has tasks: the GraphQL `workItemCreate` mutation with the Task type and `hierarchyWidget: {parentId: <the issue's global ID>}`, since REST and `glab` cannot set the parent. Without them, an issue labelled `subtask` that blocks the story, or relates to it on Free.
* **Board placement:** a view over labels; the label places the issue.
* **State:** a scoped label, `status::draft`, `status::todo`, `status::in-progress`, `status::in-review` or `status::testing`, which also moves the issue to that label's board list. Done closes the issue and removes the label. Scoped labels keep one per issue on Premium and above; on Free, remove the old one yourself.
