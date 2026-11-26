---
name: story
description: "Use first, before writing requirements or any code, for a feature or anything bigger than one check can prove done: a capability with several rules, a new script, report or export, support for a new kind of rule such as tax or discounts, a whole app or product idea, an existing PRD, or a written story to build, such as 'add a CSV export', 'add offline mode to the iOS app', 'add a weekly churn model to the dbt project', 'implement the spec in SPEC.md', 'I want to build a booking site for my bakery', 'turn this PRD into stories', 'interview me for a story about refunds', 'implement docs/stories/02-export.md' or 'build the next story'. Not for a change one check proves done, which is the task skill's, nor for a throwaway experiment, which is the spike skill's. Interviews the person and writes stories as vertical slices, or builds one story from hidden failing tests to a merged, accepted change."
license: MIT
metadata:
  version: "10.0.0"
---
# Story

A story is one vertical slice: a thin path through every layer that does one complete, small thing a user cares about. Stories are sized by value, never by lines of code; to build one, the story is cut into build slices of at most 200 lines each. Writing stories and building one are separate runs.

## Write

### Interview

* **Take what the person brought as the input,** from one feature to a whole product idea or an existing PRD, and read what the product already does.
* **Interview until nothing is left to interpret,** failure paths included, by [references/interview.md](references/interview.md).
* **Record each question and answer as you go** in `story-<slug>/interview.md` under the OS temp directory, so later steps and the verifier read it.

### Confirm

* **Play back every acceptance criterion in chat in plain language,** each sentence one its user understands at first read: a high-school reader for a consumer product, the field's own terms for developers or operators. Give the rule as Given/When/Then, then an example with real values in the product's terms.
* **Go on only once the person confirms them;** each change goes into the interview file.

### Split

* **Split the confirmed criteria into stories** by [references/split.md](references/split.md), each criterion in exactly one story.
* **Write each story in the template below.**

### Verify

* **Launch a fresh subagent** by [references/verify-stories.md](references/verify-stories.md), with the paths of the interview file and the stories and nothing of your reasoning.
* **Show the person its findings and ask before fixing them.** Fix, then verify again, for at most 3 rounds; then hand over what is still open.

### File

* **Ask where the stories go** when the person has not said: their tracker, such as GitHub Issues, Jira or Gitea, or files on disk at `docs/stories/<NN>-<slug>.md`, numbered in build order.
* **Link the order with the tracker's own blocking relation** where it has one. Write `Depends on:` and `Blocks:` lines only into files on disk.
* **Read each write back.**

### Template

```markdown
As a <specific user>, I want <a capability>, so that <the benefit to them>.

Context: <2 or 3 short plain-language sentences for a reader outside the team>

## Acceptance criteria

1. Given <how the state came about>, when <one action>, then <every result the rule decides>.
   Example: <the same rule with real values in the product's terms>
   Check: <only for a rule with no single right answer: the metric, threshold, labelled sample and who labelled it; or `by eye:` what the person judges themselves>

## UAT

1. <a concrete step on the product as its user meets it: the live site, the installed app or CLI, the device, the published package in a sample project, the warehouse table>
   Expected: <what the user sees>

Depends on: <story>
Blocks: <story>
```

## Build

One story per run.

### Plan

* **Create the story branch without checking it out,** such as `git branch story/<slug>`, so the person's working copy stays as it is.
* **Explore what the story touches:** the code, its callers, its tests and the data.
* **Write a plan for the whole story:** the components and how they connect, the interfaces, and the build slices in order, each a set of the story's tests it makes green in at most 200 lines of related change. Generated files, IDE project files and scenes do not count; where the repository's generated files are not marked `linguist-generated` in `.gitattributes`, say so in the plan.
* **Bring each design choice in the plan to the person** by [references/design-choices.md](references/design-choices.md), with the options, your pick and why. Push back where you disagree or the field's practice says otherwise, and agree the approach together.
* **Have a fresh subagent review the plan** by [references/plan-review.md](references/plan-review.md), and settle each blocking finding before the tests.

### Tests

* **Launch a fresh test-writer subagent** in a worktree off the story branch, given only the story and the reviewed plan. It commits the interfaces with stubs that compile, writes the failing tests by [references/tests.md](references/tests.md), sees each fail for the right reason, leaves the tests uncommitted, and reports only that they are written.
* **Hide the tests:** move them into `task-checks/<story-slug>/` under the repository's shared git directory (`git rev-parse --path-format=absolute --git-common-dir`), with any build-file lines that register them, merge the interface commit into the story branch, and remove the test-writer's worktree.
* **Give each slice its own `run`** in `task-checks/<story-slug>-<n>/`, taking no arguments: it syncs the slice's worktree into one scratch directory it reuses, such as with `rsync`, so builds stay incremental; puts the tests in; runs that slice's tests and every test already green; and prints only each failure's message, from a machine-readable report such as `jest --json`, `go test -json` or JUnit XML. A test that no longer builds prints only which interface no longer matches its stub.

### Slices

* **Build each slice as a task,** by the task skill from its hand-off, one after another, in its own worktree on a branch `slice/<story-slug>-<n>` off the story branch, with that slice's `run` as its check.
* **Review each slice** with the reviewer agent, or a fresh subagent briefed with its prompt where agents are not available. Read each finding against the code, send the ones that hold back to the slice's implementer (resumed where the tool allows), and merge the slice into the story branch once each blocking one is fixed.
* **Give each review a directory outside the tree** holding `diff.patch`, the change against its base, and `story.md` under four headings: `Criteria`, the ones it covers; `Out of scope`, what it leaves out on purpose; `Changed tests`, each test that predates the change and changed, with the criterion behind it; `Test command`. For a slice, `story.md` also says the story's tests are held out.

### Finish

* **Move the tests into the repository's tests** and commit them.
* **Review the whole story's diff** with the reviewer agent, then the verifier agent on its findings, or fresh subagents briefed with their prompts where agents are not available. Fix each blocking finding the verifier keeps, test-first, and show the person each kept `question` and `non-blocking` row.
* **Check the implementation against the story yourself,** criterion by criterion, and fix what falls short.
* **Push and open the merge request.** Watch CI to its end and fix each failure, for up to 24 hours, with a scheduled check-in where the tool has one; when the wait outlasts the session, tell the person what is pending. With no CI, run the definition of done locally; with no remote or review host, ask how it merges.
* **Bring each person's review comment to the person** with a proposed fix, rather than answering it yourself.
* **Ask before merging,** unless the person said to merge it; where a merge deploys or publishes, say so in the question.
* **Run the UAT** step by step once it is live: run each step that changes nothing real yourself, and hand the person the steps that move money, publish, flash a device, or need their eyes or hands, recording what they report. When every step passes, mark the story done in the tracker or its file.
