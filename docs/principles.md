# AI developer principles: a cheat sheet

Whoever made it, someone else attacks it, and a machine decides when it's done. Most of these are habits for you to remember, so they live here and not in a skill. The table after the list shows which ones the plugin enforces.

## Who authors, who attacks

1. **You design:** write the design yourself, then tell the agent "attack this: what breaks, with a case from this codebase".
2. **Claude designs:** have a fresh subagent attack it, given only the design and the criteria, never Claude's reasoning.
3. **Separate reviewer:** the agent that wrote the code never reviews it.
4. **Learning:** you write the code and Claude tweaks it. Ask it to explain, not to do the work.

## Tests and done

5. **Criteria first:** write testable acceptance criteria before the build. The building agent never defines done.
6. **Deterministic check:** give the agent a `Check:` command that says when it's done.
7. **Running app:** check the change in the browser, the command line or a real request, as well as the test suite.
8. **Locked tests:** the agent can't change a test to make it pass.
9. **Harder-to-game tests:** use a blind test challenger, mutation testing and property-based tests, because agents write weak tests.

## Deterministic over instructions

10. **Enforce, don't instruct:** if a hook, script, linter, type checker or CI can enforce it, use that.
11. **Fix the harness:** when the agent fails, add a check or sensor, not more prompt.
12. **Gate dependencies:** block unknown or first-seen packages (slopsquatting).

## Context

13. **Short AGENTS.md:** write it yourself, not with `/init`.
14. **Fresh sessions:** start one per ticket, with a progress file and git history, over a long compacted chat. Send subagents to explore.

## Safety

15. **Sandbox:** run agents in a sandbox with network-egress control and auto-approve inside it, instead of relying on permission prompts.

## Human review

16. **Scarce attention:** keep pull requests small, and watch whether you approve more while reading less.

## Measure the harness

17. **Plain-prompt baseline:** compare every skill against a plain prompt with `tools/baseline.py`. Cut what doesn't beat it, and rerun when a new model ships.
18. **Outcomes over feel:** measure results, because people overestimate the speed-up.

## Where the plugin enforces each one

| Principle | Enforced by |
|---|---|
| 2, 3, 5, 9 | The `build` skill and its 4 agents |
| 6 | Done-check hook, on the `Check:` line |
| 7 | `build`'s check step |
| 8 | Test-lock hook |
| 9 | Holdout guard hook, and a `Mutation:` line in `AGENTS.md` |
| 12 | Dependency-gate hook |
| 13 | Size-cap hook, 100 lines or 8 KB |
| 16 | Pull request cap hook, 400 changed lines |
| 17 | `tools/baseline.py` |
| 1, 4, 10, 11, 14, 15, 18 | You |
