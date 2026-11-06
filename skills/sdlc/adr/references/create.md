# Record a decision

A choice a later edit undoes for free, a workaround meant to be removed, or a rule a check already enforces is not an ADR unless the user asks: say so and write nothing. One decision per file.

## Get the reasons

First state how the ADRs in force and the code constrain this decision, each with its `file:line`. Then ask the user, one at a time: why this, and why not <the obvious route>. Skip one their words already answer, and quote them; never draft their reasons. **Still open:** give the options as equals and the trade-off they turn on.

* **What it gives up:** ask. Then add each cost the repository shows, with its `file:line`, as a critique.
* **Your own feedback:** ask each alternative nobody considered, hazard with no test, or reason the code contradicts as its own question. Record each the user accepts, marked as the agent's.
* **The user defers to you:** record your reason, marked as the agent's, with "The user deferred to the agent's recommendation.", once they say yes to the recorded text.
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
