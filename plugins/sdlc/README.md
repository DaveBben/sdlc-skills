# sdlc

Extreme Programming with an agent. You decide what gets built and write the intent; the tests carry the rest. `sdlc` turns a request into user stories with acceptance criteria you agree, files spikes, bugs, chores, specs and decision records, and builds each to a pull request you merge, by pair programming or on autopilot.

* **Pair programming, for code you want to understand or learn from:** you steer each turn. Explore the code, propose a design, have the agent write part and leave part for you, or write signatures for it to critique and fill in. The agent answers as a senior engineer: it names the technique behind its feedback and disagrees when your idea is worse. When you want the change shipped, it hands the branch to `build`'s review and pull request.
* **Autopilot, for code you just want built:** failing tests come first, from your examples, then a fresh agent that never reads the function bodies adds tests for wrong implementations, with its second-value and property tests held out of the builder's sight until the code passes, then the code with refactoring inside the loop, 1 fresh review, and a pull request that records the agent designed it. A script refuses any change to a locked test outside the commits allowed for it.

Say "let's pair on X" or "just build X", or write a `Build:` line in `AGENTS.md`, such as `Build: pair for src/billing; otherwise autopilot`. With none of these, or a ticket comment naming the mode, the agent asks, with no pick.

## What runs in a session

* **One hook.** At session start, [`hooks/route.md`](hooks/route.md) prints the routing list, 205 words, which sends each change request to `prd`, `bug`, `refactor`, `chore`, `spike`, `pair-programming`, `build`, `spec`, `adr` or `story`.
* **Descriptions:** 13 skills and 4 agents, 6,467 characters, about 1,617 tokens at 4 characters a token. A skill's body loads only when a request matches it.
* **Rules read:** a pair-programming session reads 474 words of skill text in 16 lines. Autopilot's reads 1,899 words, or 2,307 when a choice costly to reverse also loads the `adr` skill.
* **Subagents:** at review, 1 reviewer (Opus) and a verifier (Opus) that keeps only the findings it can prove. On autopilot, the test challenger (Sonnet) runs before the code, and an implementer (Sonnet) makes the failing tests pass, one launch at a time, and never sees the held-out tests. When a locked test calls an interface that turns out different, the session checks the implementer's unlock request, allows it in a commit of its own and re-locks the test, without asking you. Past 10 issues or ADRs, read-only subagents read them in parallel and return one sourced row each.
* **With no person in the session,** such as a scheduled job, autopilot alone runs. Questions go to the story's contacts on its issue.

## One session, traced in pair programming

"Show me every call to the billing service."

| Turn | Who | What happens |
|---|---|---|
| Explore | agent | Lists the 7 calls with `file:line`, grouped by what varies: 3 retry, 4 do not |
| Idea | you | "I'm thinking one class for these calls" |
| Critique | agent | Agrees: **Extract Class** ends the **Shotgun Surgery** of 7 copies. Warns that 2 callers need the raw response, so the class must expose it |
| Split | you | "Write it, explain each function, leave one for me" |
| Write | agent | Writes the class with a line on why each function exists, and leaves `retry_policy` as a stub with its contract and a failing test, because it holds the most judgement |
| You write | you | You fill in `retry_policy`. The agent reads your diff and points out it retries a POST that is not idempotent |
| Ship | agent | Asks for a `Done when:` line, then `build` reviews the branch and opens the pull request, `Built: paired with a person` |

`refactor`, `adr` and `onboard` also work installed alone. `build` needs the 4 agents installed as subagents: the skills name none, so the harness picks each by its description.
