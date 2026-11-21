---
name: reflecting
description: "Use whenever the person looks back on work just done with you, and once a non-trivial code change is finished or given up: a retro or post-mortem, what went well or wrong, lessons from the session, where time was lost, why it took so many rounds, whether their instructions caused rework, or how to prompt or steer you better next time, however casually asked, such as 'what's the takeaway?'. Not after a one- or two-line edit, and not for reviewing the code itself. Reviews the session against the loop (Frame, Explore, Build, Verify, Review) and tells the person what to do next time to get better output from you."
license: MIT
metadata:
  version: "5.0.0"
---
# Reflecting

Tell the person, with cases from this session, what to do next time to get better output from you: findings to keep or drop, no score.

## The loop and how each stage fails

**Frame:** the goal and why (theirs), the context, and a done-check they can watch run.
* A goal the platform cannot do, or a check that tests something else.
* A noun hiding the data's shape, such as "a table" that is a view with a row per item per night.
* A check on one item where the job meets none or many.
* Order, duplicates, ties and equality unstated.
* A Then that states part of the result.
* The why written by you, not them, or several asks joined by "and".
* How it runs left out: unattended, a credential, a metered API, a second or missed run.
* A long, open-ended prompt with no check to run.

**Explore:** unfamiliar parts asked about before code, each answer marked `doc` or `memory`.
* Code built on an unchecked `memory` answer.
* An unfamiliar part handed over whole, so they could not judge it.
* An error pasted back until it passed, the fix unexplained.
* A prototype judged on one hand-made example.
* A spike whose answer could not change the plan.

**Plan:** only when the change does not fit a sentence; steps of one line and one readable diff, risk rising down the list.
* A plan for a change that fit a sentence.
* A step too big to read.
* Implementation detail instead of intent.
* Writes before reads, or the real target before a test one.
* A step nobody could say how to do, planned anyway.
* Risks only the person knows, never asked for, or work split finer than anyone used.

**Build:** one step at a time, a commit before each risky one.
* The same correction given twice.
* A failed approach retried unchanged instead of a new approach or taking over.
* Your loops, unrequested features or touched tests left running.
* Tests edited, deleted or special-cased to go green.
* A derailed session carried on instead of restarted.
* Parallel agents on shared state.

**Verify:** they saw each step run.
* "Done" or "I tested it" taken on your word.
* A metric that cheated, such as a "100% decrease" from deleted code.
* Your own tests as the only oracle.
* Everything checked once at the end, not after each step.

**Review:** they can explain the change without you, and read deepest where a mistake costs most.
* A part they could not have explained.
* The pull request description read instead of the diff.
* Auth, data or deploy skimmed.
* A fault no run can show, such as a token saved in the project folder.
* Your own review as the only one.

## How

1. **They go first.** Ask once what they would do differently; on "skip", go on.
2. **A fresh reader:** a subagent, given the section above and no view of yours, reads this session's transcript. In Claude Code that is the newest `.jsonl` in `~/.claude/projects/<the working directory with / and . turned into ->/`, read through `jq -r -f extract.jq <file>` (`extract.jq` is in this skill's directory), never raw. It returns candidates, each with a verbatim quote and its cost in rework, and quotes no credential.
3. **Check every quote** is in the transcript; drop any that is not. Keep at most 5, by rework cost, plus one move that saved rework.
4. **Show each** as: what happened, in their words; what it cost; what to type or check next time. Say which they had already named, and that the reader misses things.
5. **From the kept ones:** your own failure becomes a proposed `AGENTS.md` line; one they corrected twice, a proposed check or hook.
