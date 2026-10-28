# working-agreement

Optional house rules for how the agent works with you, added to every session. Install it if you want them; nothing else in this repository needs it.

## What runs in a session

* **One hook.** At session start, and again after `/clear` or a compaction, it prints [`hooks/working-agreement.md`](hooks/working-agreement.md) into the context: 609 words and 3,427 characters, about 857 tokens at 4 characters a token.
* **No skills.** A loaded skill's own rules win where they differ, such as `plan`'s questions asked as equals.

## The rules

* **Work:** the smallest clean solution (KISS, YAGNI); look facts up instead of asking, with a subagent for a slow lookup; a subagent for a side task unrelated to the current work; batch tool calls.
* **Ask:** ask when a request is unclear; one decision per question, through the question tool or as `❓ **Q1** - **<title>**`; "yes" accepts the recommendation, except for a decision hard to reverse or one that sets a target; small reversible choices as `Decided:` lines; who set each number, and any change to one you agreed to.
* **Explain:** what it means for you, then a concrete case, then the mechanism, with rates as natural frequencies; few new ideas at a time and one name per number; where each number comes from; the canonical name of the idea behind feedback; a hinge question before a decision others hang on; a joking nudge to remember a trivial command, which you may run yourself; ELI5 when you seem confused, and a concrete case when you ask again.

## Install

```bash
claude plugin marketplace add DaveBben/sdlc-skills
claude plugin install working-agreement@sdlc-skills
```

Other agents: paste `hooks/working-agreement.md` into your `AGENTS.md` or global instructions file.
