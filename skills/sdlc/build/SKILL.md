---
name: build
description: "Use when code is to be changed and shipped, from a ticket or a plain request: a feature, a fix, a chore or a refactoring, such as 'build X', 'fix this', 'let's pair on X' or 'I'll write it, you review'. Whoever authors the work, someone else attacks it and a check decides when it is done, in two modes: the person authors to learn, or the agent authors and fresh agents attack its design, tests and diff before a small pull request."
license: MIT
metadata:
  version: "2.0.0"
---
# Build

Whoever made it, someone else attacks it, and a machine decides when it is done.

A change with one obvious result and no trade-off, such as a colour, a config value or a rename, needs none of this: make it and let the check run. Everything below is for a change that can be wrong in a way its author would not see.

## Who authors

Take the mode from the request, else the `Build:` line of `AGENTS.md`, else ask once.

* **Learn:** the person designs and writes. You attack what they make: what it breaks, each with a case from this codebase, and the name of the technique or failure class. Explain instead of doing the work. Edit their code only when they ask, as the smallest tweak, and say what you changed and why.
* **Delegate:** you design and write. A fresh subagent attacks each thing you make before anything is built on it. It gets the artifact and the criteria, never your reasoning. Fix what it proves and note what you keep.

## What gets attacked

| Made | Learn | Delegate | Settled when |
|---|---|---|---|
| Criteria | you attack | the person agrees | each is observable in the running app |
| Design | you attack | a critic attacks | no attack is left unanswered |
| Tests | you attack | a critic attacks | each fails for its reason, then is committed |
| Code | you review | a reviewer, then a verifier | the check passes and the app shows each criterion |

* **Criteria:** agree testable acceptance criteria with the person before any code, each a rule with an example in real values. The author of the code never defines done. In delegate mode you may draft them, marked as yours, and the person agrees them.
* **Design:** write one only for a decision that is costly to reverse: data stored or sent, a contract others call, a dependency, auth, how it deploys. Ask the person about that decision with the options as equals. Settle every other choice yourself as `Decided: <choice>, because <reason>`.
* **Tests:** write them from the criteria's examples before the code, see each fail for its reason, and commit them alone. A committed test is locked: a hook asks the person before a line of it changes or a line that switches tests off is added, so the code changes to fit the test. A locked test you believe is wrong is a question for the person. Adding tests is always free.
* **Check:** the `Check:` command of `AGENTS.md`, as it read when the session began, runs when you stop, and a failure sends you back. Where `AGENTS.md` has a `Mutation:` line, run it on the changed files once the check passes, and add a test for each surviving mutant in a changed line.
* **Running app:** see each criterion hold in the running app, through a browser, the command line or a real request. A passing suite is not that evidence.
* **Review:** commit, then give a fresh reviewer only the diff against the merge target, the criteria and the tree. Then launch a fresh verifier even when the reviewer found nothing: it runs each criterion against the app, and proves or drops each finding without the reviewer's reasoning. Never verify your own change yourself. Fix every blocking finding test-first.

## Sessions

Start a fresh session for each ticket. For work that outlasts a session, keep `PROGRESS.md` at the branch's root: each criterion and whether it is met, the next step, and open questions. Resume from it and `git log`, and delete it before the pull request. Send a subagent to explore code you only need a conclusion from.

## Branch and pull request

* **Branch:** a worktree from main, named `<story|bug|chore|refactor>/<key>-<title-words>`.
* **Size:** one pull request per criterion group a person can read in one sitting. Past about 400 changed lines, split it.
* **Title:** `[<key>] <what it does, imperative>`.
* **Body:** under 40 lines, rewritten against the final diff at every push, for a reader who saw none of the build.

```markdown
## Why
<2 to 4 sentences: the problem, why this approach, what it costs. Link the ticket.>
Authored by: <the person, reviewed by the agent | the agent, attacked by fresh agents>

## Needs you
- [ ] Decide: <question, your pick first; for a decision costly to reverse, the options as equals>
- [ ] Read: <each locked test changed, each new dependency, each finding kept but not fixed>

## Evidence
`<check command>` passes. Mutation: <n> of <n> killed, or not set up.
<criterion>: <what was run against the app> -> <what it showed>
```
