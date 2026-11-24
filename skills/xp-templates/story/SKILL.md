---
name: story
description: "Use when a user story is to be created, reviewed, split, forecast or filed, not built: interviewing the person to turn an idea into a story, writing a story or ticket for later or for someone else, critiquing a story someone wrote, splitting an epic, a PRD or a large feature into stories, or forecasting when a set of stories will be finished, such as 'interview me for a story about X', 'write a story for X', 'critique the story in docs/stories/x.md', 'are these criteria testable', 'break this PRD into stories', 'this is too big for one merge request, cut it down' or 'how many weeks for the remaining stories'. Not for building a story or changing code. Interviews the person at the business level and writes the story from their answers (why, context, one acceptance criterion per business rule with a Given/When/Then example and a check, a UAT, out of scope); holds the checks a story is reviewed against, the splitting rules and the forecast format."
license: MIT
metadata:
  version: "2.0.0"
---
# Story

A story is one vertical slice that fits one merge request, written at the business level for a reader outside the conversation. It has the 3 C's: the card is the story you write, the conversation is your interview of the person, and the confirmation is its acceptance criteria and UAT.

* **Create one** by interviewing the person: [references/create.md](references/create.md).
* **Review one** by [references/review.md](references/review.md).
* **Split** an epic, a PRD or a story that is too big by [references/split.md](references/split.md).
* **Forecast** a set of stories by [references/forecast.md](references/forecast.md).
* **File** only what the person approved: in the team's tracker when a tool here reaches it, by the tracker skill, else `docs/stories/<NN>-<slug>.md`, numbered in build order.
* **Leave a merged story alone:** it is a record. A miss or a change of mind is a new story.

## Acceptance criteria

You write the criteria from the person's answers. The rules in them are the person's.

* **One per business rule,** in the product's words, measurable: not "is fast" but "under 200 ms at 1,000 rows".
* **A Given/When/Then example in real values.** The Given says how its state came about, the When is one action, and the Then states every result the rule decides. A rule with several cases gets a table, one row per case.
* **A check someone can run** for each criterion.
* **A user acceptance test (UAT)** for the story: how the person will see it work on the live system, with real credentials and services, read-only or as a dry run where it writes.
* **Follow the person's rule,** not what the code does today.
* **Mark an open question `unknown`,** with who can answer it.

## How a story fails

Each one is a gap to close in the interview, or a finding in a review.

* **A solution, not a problem** (XY problem): "add a Redis cache" where the need is "exports show data more than 15 minutes old". Ask why.
* **"As a user":** a role that hides who it is for and their job to be done.
* **A why you supplied:** the why is the person's, in their words.
* **A silent assumption:** a gap you filled and wrote as a decision or a won't-do instead of asking.
* **An overloaded term** not pinned to one meaning (ubiquitous language), checked against the glossary and the code: does "account" mean the customer or the user?
* **Vague words** such as fast, easy, robust, tidy or "handles errors": each needs a number or a stated result.
* **The story sentence without rules:** the rules and their examples carry the story, not the sentence.
* **A Given reachable several ways, or a Then that states part of the result:** tests built on it pass and miss the rule.
* **Several asks joined by "and":** each is its own vertical slice.
* **A layer, not a vertical slice:** no page, route or command where a person or test meets the change.
* **Too big:** several features, more than about 400 changed lines or 5 criteria, or nobody can size it. Split it.
* **Not a story:** a change no user would notice (a refactor, rename, dependency bump or CI) needs one `Done when:` line, not a story.
* **Design in the story:** files, tables or layout before the rules are agreed.
* **Conflicts:** a rule another story also states, or one main already meets.
* **An unknown that could change the story fundamentally:** name up to 3, and write each as a spike, by the spike skill, listed under `Dependencies` as blocking it.
