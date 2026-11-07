# Record a decision

A choice a later edit undoes for free, a workaround meant to be removed, or a rule a check already enforces is not an ADR: say so in one line, and write it only if the user asked for it. One decision per file.

## Get the reasons

First state how the ADRs in force and the code constrain this decision, each with its `file:line`; one that contradicts an ADR in force supersedes it: say which. Then ask in one message: why this, why not <the obvious route>, and what it gives up. Skip one their words already answer, and quote them; never draft their reasons. **Still open:** give the options as equals and the trade-off they turn on, and your pick after their answer.

* **What it gives up:** add each cost the repository shows, with its `file:line`, as a critique.
* **Your own feedback:** once they answer, each alternative nobody considered or hazard with no test is a one-line note with its `file:line`; a reason the code contradicts is a mistake: ask, quoting both. Record each they adopt, marked as the agent's; a choice they keep is recorded as their call with the risk named.
* **The user defers to you:** record your reason, marked as the agent's, with "The user deferred to the agent's recommendation."
* **No reasons,** or both still "unknown": write no file, and say the decision is unrecorded.

## Write it

Match this example's sections and density, and record only alternatives and facts the user or you named.

```markdown
# Call outside services with httpx, not requests

**Decision:** Every outbound HTTP call goes through `httpx.AsyncClient`. The service is async end to end, and one blocking `requests` call stalls the event loop for every request on that worker.

**Fitness function:** the banned-api rule in `pyproject.toml` (ruff `TID251`) fails on any import of `requests`.

## Alternatives rejected
- `requests` in a thread pool: one thread per call in flight, and the pool size becomes another limit to tune.

## What it gives up
- Two internal libraries still pin `requests`; they stay outside the service until they move.
```

* **Fitness function:** for a rejected alternative code could bring back, such as an import, a lint rule that fails on it. When nothing can detect it, write `none` and what to watch instead.
* **Revisit when:** only for a decision resting on a guess or an unmeasured number: the observation that reopens it. One that accepts a hazard opens its Decision with the problem in one sentence.
* **One sentence** is enough for one alternative and one cost: "In the context of <situation>, facing <concern>, we decided for <option> and against <alternative>, to achieve <quality>, accepting <cost>. Fitness function: <check>."
