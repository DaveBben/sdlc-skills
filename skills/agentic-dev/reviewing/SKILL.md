---
name: reviewing
description: "Use first, before launching any reviewer or reading the diff yourself, for any review of a code change, however small, asked by a person or another agent: a diff, branch, commit or uncommitted change, such as 'review my changes', 'find the bugs in my working-tree diff', 'check my diff for bugs before I push' or 'get this branch ready to merge', and once the building skill's check passes on a non-trivial change, before it is merged or opened as a pull request. Not for a design or plan, a one- or two-line edit, or a question about code. Packs the diff and its intent for a fresh reviewer, has a second fresh agent prove or drop each finding, shows the person what was kept, fixes the blocking findings test-first and stops after 3 rounds."
license: MIT
metadata:
  version: "6.2.0"
---
# Review

## The review directory

Make a new directory outside the tree, such as `<temp>/review-<timestamp>/`, holding:

* **`diff.patch`:** the change against its merge base, uncommitted work included, without lockfiles, generated or vendored files.
* **`story.md`:** the ask and nothing else, under four headings. `Criteria`: numbered, in the person's or the story's words. `Out of scope`: what you left out on purpose. `Changed tests`: each test that predates the change and that you changed, with the criterion behind it. `Test command`: the command that runs them.

Over about 400 changed lines, give each group of files that change together its own reviewer, directory and slice of the diff, then join and renumber the findings.

## The pass

* **Brief each agent** with only the paths of its reference file and the review directory, never your view of the change or of a finding. Use a fresh subagent for each, or a new session where there are none.
* **The reviewer,** on your strongest model (such as Opus), follows [references/reviewer.md](references/reviewer.md) and writes `findings.md` in the review directory.
* **The verifier,** on a smaller model (such as Sonnet), follows [references/verifier.md](references/verifier.md) and rewrites `findings.md` with the rows it kept.
* **No return is not a clean review:** a subagent that returned nothing, errored, could not run commands or left rows `unchecked` did not review. Rerun it or say so.
* **Tell the person** each kept finding in one line, blocking first; then each `question`, each row dropped for `no basis`, and each `not judged:` line. Say the review does not replace their own reading of one-way doors (architecturally significant decisions).

## The fixes

* **Fix blocking findings only, test-first:** a fail-to-pass test on the finding's trigger, then the smallest fix. A non-blocking finding waits for the person's word.
* **Mark a kept finding you cannot reproduce `disagree`,** with the line that stops it, and take it to the person.
* **Revert a fix that breaks a passing test.**
* **Review only the fix diff in a later round,** in a new directory whose `story.md` also lists the settled findings. After 3 rounds, stop: list what is open and ask whether to change approach.
* **Once no blocking finding is open** and the change is finished, load the reflecting skill.
