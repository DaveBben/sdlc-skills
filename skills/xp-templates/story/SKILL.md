---
name: story
description: "Use when a user story is to be written, reviewed, split, forecast or filed, not built: writing a story, a ticket or its acceptance criteria for later or for someone else, critiquing a story someone wrote, splitting an epic, a PRD or a large feature into stories, or forecasting when a set of stories will be finished, such as 'write a story for X', 'critique the story in docs/stories/x.md', 'are these criteria testable', 'break this PRD into stories', 'this is too big for one merge request, cut it down' or 'how many weeks for the remaining stories'. Not for building a story or changing code. Holds the story template (why, context, one acceptance criterion per business rule with a Given/When/Then example and a check, a UAT, out of scope), the checks a story is reviewed against, the splitting rules and the forecast format."
license: MIT
metadata:
  version: "1.0.0"
---
# Story

A story is one vertical slice that fits one merge request, written at the business level for a reader outside the conversation.

* **Write one** by [references/write.md](references/write.md).
* **Review one** against the two lists below, reported in the format in [references/write.md](references/write.md).
* **Split** an epic, a PRD or a story that is too big by [references/split.md](references/split.md).
* **Forecast** a set of stories by [references/forecast.md](references/forecast.md).
* **File** only what the person approved: in the team's tracker when a tool here reaches it, by the tracker skill, else `docs/stories/<NN>-<slug>.md`, numbered in build order.

## Acceptance criteria

The person writes the criteria. Critique them against these rules and fill the gaps.

* **One per business rule,** in the product's words, measurable: not "is fast" but "under 200 ms at 1,000 rows".
* **A Given/When/Then example in real values.** The Given says how its state came about, the When is one action, and the Then states every result the rule decides. A rule with several cases gets a table, one row per case.
* **A check someone can run** for each criterion.
* **A user acceptance test (UAT)** for the story: how the person will see it work on the live system, with real credentials and services, read-only or as a dry run where it writes.
* **Follow the person's rule,** not what the code does today.
* **Add a criterion with its reason,** and keep it only once the person agrees.
* **Mark an open question `unknown`.**

## How a story fails

Each one found is a question for the person, or a gap you fill with its reason.

* **A solution, not a problem** (XY problem): "add a Redis cache" where the need is "exports show data more than 15 minutes old". Ask why.
* **"As a user":** a role that hides who it is for and their job to be done.
* **No "so that", or one you wrote:** the why is the person's.
* **A silent assumption:** a gap you filled and wrote as a decision or a won't-do instead of asking.
* **An overloaded term** not pinned to one meaning (ubiquitous language): does "account" mean the customer or the user?
* **Several asks joined by "and":** each is its own vertical slice.
* **A layer, not a vertical slice:** no page, route or command where a person or test meets the change.
* **Vague words** such as fast, easy, robust or "handles errors": each needs a number or a stated result.
* **The story sentence without rules:** the rules and their examples carry the story, not the sentence.
* **A Given reachable several ways, or a Then that states part of the result:** tests built on it pass and miss the rule.
* **Design in the story:** files, tables or layout before the rules are agreed.
* **Too big:** several features, more than about 400 changed lines or 5 criteria, or nobody can size it. Split it.
* **Conflicts:** a rule another story also states, or one main already meets.
* **An unknown that could change the story fundamentally:** name up to 3, and write each as a spike, by the spike skill, listed under `Dependencies` as blocking it.
