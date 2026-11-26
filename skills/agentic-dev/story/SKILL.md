---
name: story
description: "Use first, before writing requirements or any code, for a feature or anything bigger than one check can prove done: a capability with several rules, a whole app or product idea, an existing PRD, or a written story to build, such as 'add a CSV export', 'I want to build a booking site for my bakery', 'turn this PRD into stories', 'interview me for a story about refunds', 'implement docs/stories/02-export.md' or 'build the next story'. Not for a change one check proves done, which is the task skill's, nor for a throwaway experiment, which is the prototyping skill's. Writes stories: interviews the person until nothing is ambiguous, confirms the acceptance criteria in plain language, splits them into vertical slices with a walking skeleton first, has a subagent verify them against the interview, and files them. Builds one story: a reviewed plan, design choices settled with the person, hidden failing tests, slices of at most 200 lines each built as a task and reviewed, a final review, a merge request watched to merge, and the UAT."
license: MIT
metadata:
  version: "10.0.0"
---
# Story

A story is one vertical slice: a thin path through every layer that does one complete, small thing a user cares about. Stories are sized by slice, never by lines of code. Writing stories and building one are separate runs.

## Write

### Interview

* **Take what the person brought as the input,** from one feature to a whole product idea or an existing PRD, and read what the product already does.
* **Interview until nothing is left to interpret,** failure paths included, by [references/interview.md](references/interview.md).
* **Record each question and answer as you go** in `story-<slug>/interview.md` under the OS temp directory, so later steps and the verifier read it.

### Confirm

* **Play back every acceptance criterion in chat in plain language,** each sentence one a high-school reader understands at first read: the rule as Given/When/Then, then an example with real values in the product's terms.
* **Go on only once the person confirms them;** each change goes into the interview file.

### Split

* **Split the confirmed criteria into stories** by [references/split.md](references/split.md): the walking skeleton first, each criterion in exactly one story.
* **Write each story in the template,** by [references/template.md](references/template.md).

### Verify

* **Launch a fresh subagent** by [references/verify-stories.md](references/verify-stories.md), with the paths of the interview file, the stories and [references/template.md](references/template.md), and nothing of your reasoning.
* **Show the person its findings and ask before fixing them.** Fix, then verify again, for at most 3 rounds; then hand over what is still open.

### File

* **Ask where the stories go** when the person has not said: their tracker, such as GitHub Issues, Jira or Gitea, or files on disk at `docs/stories/<NN>-<slug>.md`, numbered in build order.
* **Link the order with the tracker's own blocking relation** where it has one. Write `Depends on:` and `Blocks:` lines only into files on disk.
* **Read each write back.**

## Build

One story per run.

### Plan

* **Create the story branch** in the person's checkout, with no worktree yet.
* **Explore what the story touches:** the code, its callers, its tests and the data.
* **Write a plan for the whole story:** the components and how they connect, the interfaces, and the slices in build order, each a set of criteria whose tests it makes green in at most 200 lines of related change.
* **Bring each design choice in the plan to the person** by [references/design-choices.md](references/design-choices.md), with the options, your pick and why. Push back where you disagree or the field's practice says otherwise, and agree the approach together.
* **Have a fresh subagent review the plan** by [references/plan-review.md](references/plan-review.md), and settle each blocking finding before the tests.

### Tests

* **Launch a fresh test-writer subagent** in a worktree off the story branch, given only the story and the reviewed plan. It commits the interfaces with stubs, writes the failing tests by [references/tests.md](references/tests.md), sees each fail for the right reason, leaves the tests uncommitted, and reports only that they are written.
* **Hide the tests:** move them into `task-checks/<story-slug>/` under the repository's shared git directory (`git rev-parse --path-format=absolute --git-common-dir`), merge the interface commit into the story branch, and remove the test-writer's worktree.
* **Give the tests a `run`** that takes criterion ids, copies the worktree to a scratch directory, puts the tests in, runs those criteria's tests and prints only each failure's message.

### Slices

* **Build each slice as a task,** by the task skill from its hand-off, one after another, on a branch `slice/<story-slug>-<n>` off the story branch. Its check is `run` with the slice's criteria and every criterion already green.
* **Review each slice** with the reviewer agent, send its findings back to the slice's implementer, resumed, and merge the slice into the story branch once they are settled.
* **Give each review a directory outside the tree** holding `diff.patch`, the change against its base, and `story.md` under four headings: `Criteria`, the ones it covers; `Out of scope`, what it leaves out on purpose; `Changed tests`, each test that predates the change and changed, with the criterion behind it; `Test command`. For a slice, `story.md` also says the tests are held out.

### Finish

* **Move the tests into the repository's tests** and commit them.
* **Review the whole story's diff** with the reviewer agent, then the verifier agent on its findings, and fix each blocking finding the verifier keeps, test-first.
* **Check the implementation against the story yourself,** criterion by criterion, and fix what falls short.
* **Open the merge request and push.** Watch CI, review comments and conflicts for up to 24 hours, and fix each.
* **Merge once it is green,** unless the person said not to.
* **Run the UAT** step by step once it is live, and report each expected and actual result. When every step passes, mark the story done in the tracker or its file.
