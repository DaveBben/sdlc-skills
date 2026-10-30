# Record a decision

A choice a revert undoes, a workaround meant to be removed, or a rule a check already enforces is not an ADR unless the user asks: say so and write nothing. One decision per file.

## Get the reasons

Ask the user three questions, one at a time: why this, what it trades off, and why not <the obvious route>. Skip one their own words already answer, in the conversation or a spec, and quote them; never draft an answer for them. **Still open:** give the options as equals and the trade-off they turn on.

* **Your own feedback:** ask each trade-off not named, alternative nobody considered, hazard with no test, or reason the code contradicts as its own question. Record each the user accepts, marked as the agent's.
* **The user defers to you:** record your reason, marked as the agent's, with "The user deferred to the agent's recommendation."
* **No reasons,** or all three still "unknown": write no file, and say the decision is unrecorded.

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
* **Revisit when:** only for a decision resting on a guess or an unmeasured number: the observation that reopens it. One that accepts a hazard or follows an incident also gets `## The problem` and `## What it buys` sections.
