---
name: tracker
description: "Use for every read or write of an issue tracker or project board (GitHub, GitLab, Gitea, Jira), such as creating a ticket or issue, putting work on the board, or opening, closing, commenting on, listing or linking issues: files one labelled issue per item, links blockers by the tracker's own relation, and reads every write back."
license: MIT
metadata:
  version: "1.0.0"
---
# Tracker

* **Find it** from the git remote, a tracker URL in `AGENTS.md` or the README, or the user's link; ask when none names one. Check its API supports an operation before promising it; a read proves nothing about write access.
* **Credentials:** never ask for a token in chat or print one. Use the CLI's stored login (`gh auth status`, `glab auth status`, `tea login list`), an environment variable, or a macOS Keychain item the user names or approves, loaded into a variable. None found: name the scope needed and how to store it, then stop.
* **Per tracker,** its blocking relation, subtask relation, board placement and states: [references/github.md](references/github.md), [references/gitlab.md](references/gitlab.md), [references/gitea.md](references/gitea.md), [references/jira.md](references/jira.md). Read only the one in use.

## File an issue

* **One issue** per story, bug, chore, spike or refactor. No epics or tracking issues: a feature is only its issues. The one child allowed is a subtask, by the tracker's subtask relation.
* **Title and body:** the item's `Title:`, and its text as its skill wrote it minus anything another field shows, such as labels or blockers.
* **Label** each with its kind, `story`, `bug`, `spike`, `refactor` or `chore`, created when missing, or the tracker's own bug or task type where it has one.
* **Order and blocking:** file a feature's issues in build order. Block an issue by the tracker's relation, never prose, only on what it truly waits on, with the reason in a comment; never for order alone.
* **Boards:** never place an issue through a web route with session cookies.

## Read

* **Find an issue** by the user's link or key, the key in the branch name, else a title search.
* **Read it whole:** the body and every comment, since a later one can change what was agreed, then its state, labels and relations.
* **Many issues:** past 10, save each whole to its own file, printing nothing, and have fresh subagents in parallel map them to one sourced row each, 25 issues per subagent, for the fields the reading needs. Read an issue yourself before a decision rests on its row.
* **Next story:** an open bug decided fix now first, then open `story`, `spike`, `chore` or `refactor` issues with no open blocker and no open pull request, lowest number first, stories only in Todo. Flag as not ready one with an `Open questions` section, an unanswered `Question for @<handle>:` comment, or an open subtask assigned to a person. Past 10, map them for kind, state, criteria, an `Open questions` section, an unanswered `Question for` comment, blockers, pull requests and subtasks assigned to a person.
* **Edit a body** in place with the whole new text; put findings and links in a comment.

## Set a state

Stories move through Draft, Todo, In progress, In review, Testing and Done. Map them to the team's flow by the `Story states:` line in `AGENTS.md`, such as `Story states: Draft=Backlog, Todo=Selected, In review=Code Review, Testing=QA, Done=Done`. Without one, map them to the tracker's existing statuses, columns or labels, ask about any with no match, and add the line; map a state the flow lacks to `-`. Keep one state at a time; Done closes the issue. Change no workflow, column or shared label without the user's request.

## Every write

* **Read the issue back** after each write and fix any difference before the next.
* **Report** each issue's URL and each step left for the user.
* **Delete** an issue, or delete or rename a shared label, only on the user's explicit request, after moving content no other issue holds.

