# Split work into stories

For an epic, a PRD or a request too big for one merge request.

* **Story map first:** read the source and everything it links, then lay it out as a user story map, each story a title and an outcome line. A gap or contradiction in the source is an open question.
* **Vertical slices only:** each story passes through every layer it needs and can be built, shown and tested alone, never "the schema", "the API" and "the UI" as three stories.
* **First story:** a walking skeleton, deploy included.
* **Too big:** try Lawrence's story-splitting patterns in his order and take the first whose slices pass the check below; a workflow-step split that turns out to be a layer split fails it. Between two splits that work, take the one that lets a low-value slice be dropped.
* **A spike is the last pattern,** for one unknown that blocks sizing after the others failed: split into the spike and the story built after it, by the `spike` skill, both in the same iteration.
* **Not too thin:** the biggest piece that still fits one merge request. Merge slices no person would use apart.
* **Check each slice:** after it merges, where does a person or test meet it? A data or rules slice often has no entry point of its own: fold it into the slice that exposes it.
* **Dependencies:** a story is blocked only by what it truly waits on, with the reason, never for order alone. A slice that needs another team's review, sign-off or data goes early.
* **Coverage:** map each requirement in the source to a story, a criterion, an `Out of scope` line or an open question, and show what is left over.
* **Show the tree and stop:** titles, outcome lines, order and dependencies. The person approves it before anything is filed. Then the first story gets its criteria; each later one gets them when it is picked. Titles are enough to count for a forecast.
