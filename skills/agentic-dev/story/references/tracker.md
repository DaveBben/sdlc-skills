# Filing in a tracker

* **Find it** from the git remote, a tracker URL in `AGENTS.md` or the README, or the person's link; ask when none names one. A read proves no write access.
* **Credentials:** never ask for a token in chat or print one. Use the CLI's stored login (such as `gh auth status`, `glab auth status` or `tea login list`), an environment variable, or a keychain item the person names. With none, name the scope needed and how to store it, then stop.
* **One issue per story, spike, bug or chore,** labelled with its kind, the label created when missing. No epic or tracking issue unless asked: a feature is its issues.
* **File in build order.** Block an issue by the tracker's own relation, never in prose, and only on what it truly waits on, such as a spike:

  | Tracker | Blocking relation |
  |---|---|
  | GitHub | a "blocked by" issue relationship, not a sub-issue |
  | GitLab | a `blocks` issue link (Premium); on Free, `relates to` with the blocker named in a comment |
  | Gitea | an issue dependency, `POST /repos/{o}/{r}/issues/{n}/dependencies`, where `n` is the blocked issue |
  | Jira | an issue link of type Blocks |

* **Read each write back** and fix any difference before the next; report each issue's URL.
* **Next story,** for a fresh session: the lowest-numbered open story with no open blocker and no open merge request.
* **Delete** an issue or a shared label only on the person's explicit request.
