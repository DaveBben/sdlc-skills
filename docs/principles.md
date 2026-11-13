# AI developer lifecycle: principles

Reference for the sdlc-skills v2 redesign (Nov 2026). Nine principles from experience, plus eight added from 2026 research.

**Core rule:** whoever made it, someone else attacks it, and a machine decides when it's done.

## Who authors, who attacks

1. You design, Claude attacks it.
2. If Claude designs or writes the spec, a separate agent attacks it.
3. A separate agent reviews the code, never the one that wrote it.
4. For learning, you write the code and Claude tweaks it. Use Claude to explain things, not to do the work for you.

## Tests and "done"

5. Agree on testable acceptance criteria before the build. The agent that builds doesn't get to define "done."
6. Give the agent a deterministic check that tells it when it's done.
7. Check against the running app (browser, CLI or computer use), not just the test suite.
8. Lock tests so the agent can't change them to make them pass.
9. Agents write weak tests, so use a separate test reviewer, mutation testing, and property-based tests as harder-to-game checks.

## Deterministic over instructions

10. If a hook, script, linter, type checker or CI can enforce something, use that instead of a written instruction.
11. When the agent fails, fix the harness (add a check or sensor), not the prompt.
12. Gate new dependencies: block unknown or first-seen packages to stop slopsquatting.

## Context

13. Keep AGENTS.md short and write it yourself, not with `/init`.
14. Prefer fresh sessions with a progress file and git history over long, compacted chats. Use subagents for exploration.

## Safety

15. Run agents in a sandbox with network-egress control, and auto-approve inside it instead of relying on permission prompts.

## Human review

16. Treat your review attention as scarce: keep PRs small and watch whether you're approving more while reading less.

## Measure the harness itself

17. Compare every skill against a plain-prompt baseline. Cut what doesn't beat it, and test again whenever a new model ships.
18. Measure outcomes, not how fast it feels. People reliably overestimate the speed-up.

## Drop

- Shouted CRITICAL/MUST wording
- Anti-laziness prompting
- Step-by-step procedures
- Heavy spec rituals for small changes

## Where each principle lives in v2

| Principle | Held by |
|---|---|
| 1 to 4 | `build` skill, `critic` and `reviewer` agents |
| 5 | `build` skill |
| 6 | done-check hook, `Check:` line |
| 7 | `verifier` agent |
| 8 | test-lock hook |
| 9 | `critic` agent, `onboard` setup |
| 10, 11 | `onboard` skill |
| 12 | dependency-gate hook |
| 13 | size-cap hook, `onboard` skill |
| 14, 16 | `build` skill |
| 15 | `onboard` skill |
| 17, 18 | `tools/baseline.py` |

## Key sources

- Anthropic, harness design for long-running apps: https://www.anthropic.com/engineering/harness-design-long-running-apps
- Anthropic, effective harnesses for long-running agents: https://anthropic.com/engineering/effective-harnesses-for-long-running-agents
- SkillsBench (skills vs. no-skill baseline): https://arxiv.org/html/2602.12670v4
- ETH Zurich, AGENTS.md study: https://arxiv.org/abs/2602.11988v1
- Habituation at the Gate (review fatigue): https://arxiv.org/html/2606.22721v1
- Anthropic, AI assistance and coding skills RCT: https://www.anthropic.com/research/AI-assistance-coding-skills
- Simon Willison on sandboxing: https://simonwillison.net/2025/Oct/22/living-dangerously-with-claude/
- ImpossibleBench (reward hacking on tests): https://www.lesswrong.com/posts/qJYMbrabcQqCZ7iqm/impossiblebench-measuring-reward-hacking-in-llm-coding-1
