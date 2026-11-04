# Review checklist

Skip what CI already checks, such as formatting, secret scanning and static analysis.

1. **Does it do the right thing?** The story's problem and only that; each criterion implemented and tested; errors of omission: a criterion, branch or check the story implies that the diff leaves out.
2. **Does it fit the system?** Existing patterns and architecture, no parallel approach; YAGNI.
3. **Does it break anyone else?** No unversioned breaking change to an API, event, schema or CLI; stored data and queued messages compatible both ways through a rolling deploy; each config value it adds or changes does what the story needs and exists in every environment.
4. **Are its assumptions true?** Each holds, or the code enforces it.
5. **Is it tested?** Failure paths, tests that fail when the code is broken, behaviour over implementation; a fault-injection test for each guarantee it promises or relies on, such as no lost writes, exactly-once or ordering.
6. **Is it correct?** Edge cases (empty, null, zero, one, many, large, time zones); errors handled, not swallowed; races; off-by-one; idempotent retries and duplicates; atomic multi-step writes.
7. **Is it secure?** Authorization enforced, input validated; no sensitive data in logs or URLs; each new dependency justified, maintained and pinned.
8. **Can the next person change it?** Clear names, comments that explain why, the docs it affects updated.
9. **Will it hold up in production?** No N+1 query or unbounded loop or result set; connections, files and locks released; timeouts, and retries that back off with a limit; a failing dependency degrades the feature, not the system; reversible migrations and rollout; logs and metrics that can diagnose it.
