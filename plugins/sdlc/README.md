# sdlc

Extreme Programming with an agent. You decide what gets built and write the intent; the tests carry the rest. `sdlc` turns a request into user stories with acceptance criteria you agree, files spikes, bugs, chores, specs and decision records, and builds each to a pull request you merge, in 1 of 2 modes. In both, each test's expected values come from your examples, and a script refuses any change to a locked test outside the commits allowed for it.

* **Pair mode, for code you will run, debug or extend:** you and the agent take turns at the wheel, and either of you can take it at any moment. When the agent takes it, it reads your saved changes with `git status` and `git diff`, states the intent it infers in 1 line, and drives test-first. When you take it back, it gives a 3-line where-we-are. Before review, a blind test challenger checks the tests you both wrote, then you walk the data flow and defend each decision, and the agent names what you missed, unless you ask to skip it, which the pull request then records.
* **Autopilot, for code you just want built:** failing tests come first, then a fresh agent that never reads the function bodies adds tests for wrong implementations, with its second-value and property tests held out of the builder's sight until the code passes, then the code with refactoring inside the loop, 1 fresh review, and a pull request that records the agent designed it.

Say "let's pair on X" or "just build X", or write a `Build:` line in `AGENTS.md`, such as `Build: pair for src/billing; otherwise autopilot`. With neither, the agent asks, with no pick.

## What runs in a session

* **One hook.** At session start, [`hooks/route.md`](hooks/route.md) prints the routing list, 162 words, which sends each change request to `prd`, `bug`, `refactor`, `chore`, `spike`, `build`, `spec`, `adr` or `story`.
* **Descriptions:** 12 skills and 4 agents, 5,735 characters, about 1,434 tokens at 4 characters a token. A skill's body loads only when a request matches it.
* **Rules read:** pair mode's session reads 1,728 words of skill text in 117 lines. Autopilot's reads 2,195 words, or 3,112 when a choice costly to reverse also loads the `adr` skill.
* **Subagents:** in both modes, 1 reviewer (Opus) and a verifier (Opus) that keeps only the findings it can prove. Both run the test challenger (Sonnet): autopilot before the code, pair mode once before the teach-back. On autopilot, an implementer (Sonnet) makes the failing tests pass, one launch at a time, and never sees the held-out tests. Past 10 issues or ADRs, read-only subagents read them in parallel and return one sourced row each.
* **With no person in the session,** such as a scheduled job, autopilot alone runs. Questions go to the story's contacts on its issue.

## One story, traced in pair mode

"Lock an account after 5 failed logins".

| Step | Who | What happens |
|---|---|---|
| Route | the routing list | It is a change to what the product does, so `story` |
| Criteria | you write | The agent says how the existing login code and ADRs affect the story. You write 3 to 5 criteria; it critiques them until no finding remains, then asks whether any was missed |
| Spec | you design | Its size, then each costly decision as a tree, the ones others hang on first: your approach, then the agent's critique. `unknown:` gets options |
| Build | agent at the wheel | Branches, writes a failing test for the 5th failed login, makes it pass, commits |
| You take it | you | The agent gives `Changed:`, `Decided:` and `Next:`. You add an unlock after 15 minutes, with no test |
| It takes it back | agent | No criterion covers the unlock, so it asks `Intent: given 5 failed logins, the last at 10:00, when the right password is entered at 10:15, then what?`. Your answer joins the criteria |
| Challenge | test challenger | Without reading the code, adds a test that 5 failed logins on one account leave another account open |
| Teach-back | you | You walk a login from the route to the counter. The agent names the step you skipped: a successful login resets the counter |
| Review | reviewer, verifier | The reviewer flags that the counter is never cleared after the 15-minute unlock; the verifier proves it with a failing run, and the agent fixes it test-first |
| Pull request | you merge | `Built: paired with a person`, and your decisions under `Decided by people` |

`red-tests`, `refactor`, `adr` and `onboard` also work installed alone. `build` and `red-tests` need the 4 agents installed as subagents: the skills name none, so the harness picks each by its description.
