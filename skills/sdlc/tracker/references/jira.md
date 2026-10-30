# Jira

* **Blocking relation:** issue links of type Blocks.
* **Subtask relation:** the project's sub-task issue type, the one with `subtask: true` in `/rest/api/3/issue/createmeta/{project}/issuetypes` whatever an admin named it, with the story as its `parent`.
* **Board placement:** the board's filter places the issue.
* **State:** a workflow status, reached only by a transition: `GET /rest/api/3/issue/{key}/transitions`, then `POST` the `id` of the one whose `to.name` is the status. When none leads there from the current status, tell the user and ask.
