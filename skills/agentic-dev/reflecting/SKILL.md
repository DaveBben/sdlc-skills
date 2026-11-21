---
name: reflecting
description: "Use whenever the person looks back on work just done with you, and once a non-trivial code change is finished, after its review, or given up: a retro or post-mortem, what went well or wrong, lessons from the session, where time was lost, why it took so many rounds, whether their instructions caused rework, or how to prompt or steer you better next time, however casually asked, such as 'what's the takeaway?'. Not after a one- or two-line edit, and not for reviewing the code itself. Reviews the session against the loop (Frame, Explore, Build, Verify, Review) and tells the person what to do next time to get better output from you."
license: MIT
metadata:
  version: "6.2.0"
---
# Reflecting

Give findings with cases from this session, never a score.

## The loop and how each step fails

**Frame:** the goal and why (theirs), the context, and a done-check they can watch run.
* A goal the platform cannot do; no check, or one that tests something else.
* An overloaded term never pinned to one meaning (ubiquitous language), such as "account" for both the customer and the user.
* Edge cases unstated: none or many, order, duplicates, ties, equality, or how it runs (unattended, a credential, a metered API, a second or missed run).
* A Then that states part of the result.
* The why written by you, not them.
* Several asks joined by "and" instead of vertical slices, or slices too thin to use apart.

**Explore:** unfamiliar parts asked about before code, each answer marked `doc` or `memory`.
* Code built on an unchecked `memory` answer.
* An unfamiliar part handed over whole, so they could not judge it.
* An error pasted back until it passed, the fix unexplained.
* A prototype judged on one hand-made example.
* A spike whose answer could not change the plan, or a step nobody could say how to do, built without one.

**Build:** the one-way doors asked first; one step at a time, each a readable diff, risk rising down the list, a commit before each risky one.
* A one-way door (architecturally significant decision) decided by you, or a two-way door put to them.
* Risks only they knew, never asked for in the pre-mortem.
* A step too big to read, writes before reads, or the real target before a test one.
* The same correction given twice.
* A failed approach retried unchanged instead of a new approach or taking over.
* Unrequested features, or tests special-cased to go green, left unchallenged.
* A derailed session carried on instead of restarted.
* Parallel agents on shared state.

**Verify:** they saw each step run.
* "Done" or "I tested it" taken on your word.
* A gamed metric (Goodhart's law).
* Your own tests as the only oracle.
* Everything checked once at the end.

**Review:** they can explain the change without you, and read deepest where a mistake costs most.
* The pull request description read instead of the diff.
* Auth, data or deploy skimmed.
* A fault no test can show missed, such as a token saved in the project folder.
* Your own review as the only one.

## How

* **Ask them first,** once, what they would do differently; on "skip", go on.
* **Give the transcript to a fresh subagent** with the section above and no view of yours. In Claude Code it is the newest `.jsonl` in `~/.claude/projects/<the working directory with / and . turned into ->/`, read through `jq -r -f extract.jq <file>` (`extract.jq` is in this skill's directory), never raw. It returns candidates, each with a verbatim quote and its cost in rework, quoting no credential.
* **Drop any quote not in the transcript.** Keep at most 5, by rework cost, plus one move that saved rework.
* **Show each** as what happened, in their words; what it cost; and what to type or check next time. Say which they had already named, and that the reader misses things.
* **Propose a fix:** an `AGENTS.md` line for your own failure, and a check or hook for one they corrected twice.
