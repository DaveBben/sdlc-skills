# sdlc-skills

Agent skills that built on Extreme Programming (XP): stories, test-first, pairing and small releases.

## What you get

- You write 3 to 5 acceptance criteria before any code is written. The agent first tells you how the existing code and decisions affect the change, then critiques what you wrote.
- A change your request already spells out item by item, such as a colour or the tables to drop, skips the story: its items become the `Done when:` lines.
- Tests come first, from your examples, and the agent can't change them to make its code pass.
- Two ways to work: pair programming, where you steer each turn and the agent coaches, or autopilot, where the agent builds a story alone.
- A fresh review of every change, each finding proved by a verifier before you see it.

## Install

From your shell:

```bash
claude plugin marketplace add DaveBben/sdlc-skills
claude plugin install sdlc@sdlc-skills
claude plugin install working-agreement@sdlc-skills   # optional
```

Then start a new session, or run `/reload-plugins` in one that's open. Inside a session you can also run `/plugin marketplace add DaveBben/sdlc-skills`, then `/plugin install sdlc@sdlc-skills`.

Other agents: run `npx skills add DaveBben/sdlc-skills --all`, register `skills/sdlc/agents/` as subagents if your agent supports them, and paste `plugins/sdlc/hooks/route.md` into your `AGENTS.md`.

## How to use it

Just ask for what you want. A routing hook at session start picks the skill.

- "Write a PRD for an order-tracking app" agrees the north star every story is checked against.
- "Add a CSV export to the orders page" starts a story.
- "Let's pair on the billing calls" starts pair programming; "just build PAY-12" builds it on autopilot.
- "The export times out past 10k orders" reproduces and fixes a bug.

Skills: prd, story, design, spec, spike, bug, chore, tracker, adr, build, pair-programming, tdd, refactor and onboard. More detail in [plugins/sdlc](plugins/sdlc/README.md).

working-agreement is optional. It adds house rules for how the agent works with you, like one question at a time and plain explanations. See [plugins/working-agreement](plugins/working-agreement/README.md).

MIT license.
