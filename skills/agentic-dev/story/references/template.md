# Story template

```markdown
As a <specific user>, I want <a capability>, so that <the benefit to them>.

Context: <2 or 3 short plain-language sentences for a reader outside the team>

## Acceptance criteria

1. Given <how the state came about>, when <one action>, then <every result the rule decides>.
   Example: <the same rule with real values in the product's terms>

## UAT

1. <a concrete step on the live system>
   Expected: <what the person sees>

Depends on: <story>
Blocks: <story>
```

* **The sentence:** the user is a real role, such as a returning customer or the shop owner, never "a user".
* **Context:** 2 or 3 plain-language sentences a reader outside the team follows: this part of the product today, and what changes.
* **Each criterion:** a Given/When/Then rule, then an example with real values in the product's terms, both in plain language a high-school reader understands at first read. The Given says how its state came about, the When is one action, and the Then states every result the rule decides.
* **UAT:** concrete steps on the live system, each with its expected result.
* **`Depends on:` and `Blocks:`** only in a story saved to disk; in a tracker, its own blocking relation carries them.
