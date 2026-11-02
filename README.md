# sdlc-skills

Agent skills that built on Extreme Programming (XP): stories, test-first, pairing and small releases.

## What you get

- You agree every acceptance criterion before any code is written. The agent proposes each one and you accept, reject or modify it.
- Tests come first, from your examples, and the agent can't change them to make its code pass.
- Two ways to build: pair mode, where you take turns at the wheel, or autopilot, where the agent builds it alone.
- A fresh review of every change, with a short reading list of the code you actually need to read before you merge.

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
- "Let's pair on PAY-12" or "just build PAY-12" builds it.
- "The export times out past 10k orders" reproduces and fixes a bug.
- "Review my branch" runs a review.

Skills: prd, story, spec, spike, bug, chore, tracker, adr, build, red-tests, review, refactor and onboard. More detail in [plugins/sdlc](plugins/sdlc/README.md).

working-agreement is optional. It adds house rules for how the agent works with you, like one question at a time and plain explanations. See [plugins/working-agreement](plugins/working-agreement/README.md).

MIT license.
