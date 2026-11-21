---
name: tracker
description: "Use when work is to be recorded for later, such as the slices beyond the one being built now or a spike that blocks it, and for every read or write of an issue tracker or project board (GitHub, GitLab, Gitea, Jira): filing written stories, spikes or bugs as issues, opening, closing, commenting on, listing, labelling or linking issues, marking one issue as blocking another, or finding the next unblocked story, like 'build the first slice, record the rest for later', 'put these three stories in Gitea', 'close #12', 'mark the spike as blocking the export story', 'list the open issues labelled bug' or 'what is the next unblocked story?'. Not for writing or critiquing one story, bug report or spike on its own: those skills hold the format, and this one files it. Holds the filing rules: one labelled issue per item in build order, blocking by the tracker's own relation, and every write read back."
license: MIT
metadata:
  version: "1.1.0"
---
# Tracker

* **Find it** from the git remote, a tracker URL in `AGENTS.md` or the README, or the person's link; ask when none names one. With none, write each item to `docs/<kind>/<NN>-<slug>.md`, such as `docs/stories/02-pdf-export.md`. A read proves no write access.
* **Credentials:** never ask for a token in chat or print one. Use the CLI's stored login (such as `gh auth status`, `glab auth status` or `tea login list`), an environment variable, or a keychain item the person names. With none, name the scope needed and how to store it, then stop.
* **Find an issue** by its link or key, the key in the branch name, else a title search, and read it whole, every comment and relation included.
* **Record each slice beyond the current one** as a story by the story skill's template, with what this session learned that it needs, so a fresh session can build it.
* **One issue per story, spike, bug or chore,** labelled with its kind, the label created when missing. No epic or tracking issue unless asked: a feature is its issues.
* **File in build order.** Block an issue by the tracker's own relation, never in prose, and only on what it truly waits on, such as a spike:

  | Tracker | Blocking relation |
  |---|---|
  | GitHub | a "blocked by" issue relationship, not a sub-issue |
  | GitLab | a `blocks` issue link (Premium); on Free, `relates to` with the blocker named in a comment |
  | Gitea | an issue dependency, `POST /repos/{o}/{r}/issues/{n}/dependencies`, where `n` is the blocked issue |
  | Jira | an issue link of type Blocks |

* **Read each write back** and fix any difference before the next; report each issue's URL.
* **Next story:** the lowest-numbered open story with no open blocker and no open merge request.
* **Delete** an issue or a shared label only on the person's explicit request.
