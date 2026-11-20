---
name: retro
description: "Use once a non-trivial code change is finished or given up, before you tell the person it is done: a feature, a bug fix, a refactor or a new script of more than a few lines. Not after a one- or two-line edit or a config change. Reviews the session against the loop (Frame, Explore, Plan, Build, Verify, Review) and tells the person what to do next time to get better output from you."
license: MIT
metadata:
  version: "5.0.0"
---
# Retro

Tell the person, with cases from this session, what to do next time to get better output from you: findings to keep or drop, no score.

## The loop and how each stage fails

A name in brackets is a practitioner's report, an arXiv number a study, "walkthrough" a case seen in practice. None proves a failure is common in this person's work.

**Frame:** the goal and why (theirs), the context, and a done-check they can watch run.
* A goal the platform cannot do, or a check that tests something else (walkthrough: a playlist API that cannot write to Watch Later).
* A noun hiding the data's shape, such as "a table" that is a view with a row per item per night (walkthrough; 2610.36584).
* A check on one item where the job meets none or many (walkthrough; 2610.32548).
* Order, duplicates, ties and equality unstated: agents raise these under 2 times in 10 (2607.00711).
* A Then that states part of the result (2610.36584).
* The why written by you, not them, or several asks joined by "and" (2507.15157).
* How it runs left out: unattended, a credential, a metered API, a second or missed run (walkthrough).
* A long, open-ended prompt with no check to run (Hashimoto; Cherny).

**Explore:** unfamiliar parts asked about before code, each answer marked `doc` or `memory`.
* Code built on an unchecked `memory` answer (walkthrough: a token that expires in 7 days).
* An unfamiliar part handed over whole, so they could not judge it and learned less (2601.20245; Hashimoto).
* An error pasted back until it passed, the fix unexplained (Hashimoto).
* A prototype judged on one hand-made example (2402.17721).
* A spike whose answer could not change the plan.

**Plan:** only when the change does not fit a sentence; steps of one line and one readable diff, risk rising down the list.
* A plan for a change that fit a sentence (HN commenters; 2609.20804).
* A step too big to read: "don't draw the owl" (Hashimoto).
* Implementation detail instead of intent, which goes stale first (2608.25202).
* Writes before reads, or the real target before a test one (walkthrough).
* A step nobody could say how to do, planned anyway (walkthrough).
* Risks only the person knows, never asked for (2604.13814), or work split finer than anyone used (2605.07320).

**Build:** one step at a time, a commit before each risky one.
* The same correction given twice.
* A failed approach retried unchanged instead of a new approach or taking over (Hashimoto; Beck).
* Your loops, unrequested features or touched tests left running (Beck).
* Tests edited, deleted or special-cased to go green (Beck; Zechner; 2510.20270; 2611.23335).
* A derailed session carried on instead of restarted (Willison).
* Parallel agents on shared state (Ronacher; Carlini).

**Verify:** they saw each step run.
* "Done" or "I tested it" taken on your word (Willison; Reddit).
* A metric that cheated, such as a "100% decrease" from deleted code (Zechner).
* Your own tests as the only oracle (2608.25202; 2501.12793).
* Everything checked once at the end, not after each step (walkthrough).

**Review:** they can explain the change without you, and read deepest where a mistake costs most.
* A part they could not have explained (Hashimoto; Litt).
* The pull request description read instead of the diff (Willison).
* Auth, data or deploy skimmed (2509.10652; 2512.11922).
* A fault no run can show, such as a token saved in the project folder (walkthrough).
* Your own review as the only one: you miss your own mistakes (2507.02778).

## How

1. **They go first.** Ask once what they would do differently; on "skip", go on.
2. **A fresh reader,** for the reason in the last line above: a subagent, given that section and no view of yours, reads this session's transcript. In Claude Code that is the newest `.jsonl` in `~/.claude/projects/<the working directory with / and . turned into ->/`, read through `jq -r -f extract.jq <file>` (`extract.jq` is in this skill's directory), never raw. It returns candidates, each with a verbatim quote and its cost in rework, and quotes no credential.
3. **Check every quote** is in the transcript; drop any that is not. Keep at most 5, by rework cost, plus one move that saved rework.
4. **Show each** as: what happened, in their words; what it cost; what to type or check next time. Say which they had already named, and that the reader misses things.
5. **From the kept ones:** your own failure becomes a proposed `AGENTS.md` line; one they corrected twice, a proposed check or hook.
