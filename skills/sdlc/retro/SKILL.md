---
name: retro
description: "Use once a non-trivial code change is finished or given up, before you tell the person it is done: a feature, a bug fix, a refactor or a new script of more than a few lines. Not after a one- or two-line edit or a config change. Reviews the session against the loop (Frame, Explore, Plan, Build, Verify, Review) and tells the person what to do next time to get better output from you."
license: MIT
metadata:
  version: "5.0.0"
---
# Retro

Tell the person, with cases from this session, what they could do next time to get better output from you. Findings for them to keep or drop; no score.

## The loop it is judged against

| Stage | Done well | Missed when |
|---|---|---|
| Frame | Goal and why from them; exact names and the data's real shape; a done-check they can watch run | A rule first appears mid-build; a check covers one item where the job meets none or many |
| Explore | Unfamiliar parts asked about first, answers marked `doc` or `memory` | Code built on a `memory` answer nobody checked |
| Plan | Only when it does not fit a sentence; steps of one line and one readable diff; risk rising down the list | A step whose diff was larger than they read |
| Build | One step at a time; an approach that keeps failing is changed or taken over | The same correction given twice; a failed approach retried unchanged |
| Verify | They saw each step run | "Done" taken on your word |
| Review | They can explain the change without you | A part they could not have explained |

## How

1. **They go first.** Ask once what they would do differently. If they say skip, go on.
2. **A fresh reader.** You miss your own mistakes, so a subagent reads this session's transcript: the newest `.jsonl` in `~/.claude/projects/<the working directory with / and . turned into ->/`, through `jq -r -f extract.jq <file>` (in this skill's directory), never the raw file. Give it the table above and no view of yours. It returns candidates, each with a verbatim quote and what it cost in rework, and never quotes a credential.
3. **Check every quote** is in the transcript and drop any that is not. Keep at most 5, by rework cost, plus one move that saved rework.
4. **Show each** as: what happened, in their words; what it cost; what to type or check next time. Say which they had already named, and that the reader misses things.
5. **From the kept ones:** your own failure becomes a proposed `AGENTS.md` line; one they corrected twice becomes a proposed check or hook.
