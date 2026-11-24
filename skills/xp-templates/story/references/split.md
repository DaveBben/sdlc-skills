# Split work into stories

* **A PRD's gaps first:** check it by the prd skill's review, and raise what it leaves out, above all life after launch, as open questions before mapping.
* **Story map first:** read the source and everything it links, then lay it out as a user story map, each story a title and an outcome line. A gap or contradiction in the source is an open question.
* **First story:** a walking skeleton, deploy included.
* **Too big:** try Richard Lawrence's story-splitting patterns in his order and take the first whose slices pass the check below. Between two splits that work, take the one that lets a low-value slice be dropped.
* **A spike is the last pattern,** for one unknown that blocks sizing: a spike, by the spike skill, and the story scheduled after it, in the same iteration.
* **Not too thin:** the biggest piece that still fits one merge request. Merge slices no person would use apart.
* **Check each vertical slice:** after it merges, where does a person or test meet it? Fold a data or rules slice with no entry point of its own into the slice that exposes it. A workflow-step split that turns out to be a layer split fails.
* **Dependencies:** block a story only on what it truly waits for, with the reason. A slice that needs another team's review, sign-off or data goes early.
* **Coverage:** map each requirement in the source to a story, a criterion, an `Out of scope` line or an open question, and show what is left over.
* **Show the tree and stop:** titles, outcome lines, order and dependencies. File nothing before the person approves it. The first story is then created by [create.md](create.md); each later one when it is picked.
