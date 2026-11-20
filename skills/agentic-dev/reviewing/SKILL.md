---
name: reviewing
description: "Use first, before launching any reviewer or reading the diff yourself, for any review of a code change, however small, asked by a person or another agent: a diff, branch, commit or uncommitted change, such as 'review my changes', 'find the bugs in my working-tree diff', 'check my diff for bugs before I push' or 'get this branch ready to merge', and before a non-trivial change is merged or opened as a pull request. Not for a design or plan, a one- or two-line edit, or a question about code. Packs the diff and its intent for a fresh reviewer, has a second fresh agent prove or drop each finding, shows the person what was kept, fixes the blocking findings test-first and stops after 3 rounds."
license: MIT
metadata:
  version: "5.0.0"
---
# Review

One pass by a fresh reviewer, a second fresh agent proving or dropping each finding, and only proven blocking findings fixed.

## The packet

A new review directory outside the tree, such as `<temp>/review-<timestamp>/`:

* **`diff.patch`:** the change against its merge base, uncommitted work included; no lockfiles, generated or vendored files.
* **`story.md`:** the ask as numbered criteria, in the person's or the ticket's words; what you deliberately left out; each test that predates the change and that you changed, with the criterion behind it; the test command. No reasoning and no tour of the code.

Over about 400 changed lines, offer to split first; otherwise one reviewer per group of files that change together, each with its own directory and slice of the diff, the findings joined and renumbered.

## The pass

* **Review, then verify,** each in a fresh subagent, or a new session where there are none, briefed with the path of its reference file and of the review directory and never your opinion of the change or of a finding. The first, on your strongest model (such as Opus), follows [references/reviewer.md](references/reviewer.md): it reviews `diff.patch` against `story.md` and writes candidate findings to `findings.md` beside them. The second, on a smaller model (such as Sonnet), follows [references/verifier.md](references/verifier.md): it proves or drops each row of `findings.md` against `story.md` and the tree.
* **No return is not a clean review.** A subagent that returned nothing, errored, could not run commands or left rows `unchecked` did not review: rerun it or say so.
* **Tell the person** each kept finding in one line, blocking first; then each `question` to answer, each row dropped for `no basis`, and each `not judged:` line. The review is advisory: it does not replace their own reading of auth, data, migration or deploy changes.

## The fixes

* **Blocking findings only, test-first:** a test that fails on the finding's trigger, then the smallest fix. A non-blocking one waits for the person's word.
* **Push back:** a kept finding you cannot reproduce from its proof gets `disagree`, with the line that stops it, and goes to the person, not into the code.
* **Revert a fix that breaks a passing test;** do not patch over it.
* **A later round reviews only the fix diff,** in a new directory whose `story.md` also lists the settled findings. After 3 rounds, stop: list what is open and ask the person whether to change approach.
