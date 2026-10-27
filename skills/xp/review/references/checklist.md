# Review checklist

Skip what CI already checks, such as formatting, secret scanning and static analysis. Each bullet must hold before the change merges.

1. **Does it do the right thing?**
   * It solves the story's problem, and only that problem.
   * Each acceptance criterion has code that implements it and a test that checks it. Look for errors of omission: a criterion, branch or check the story implies that the diff leaves out.
2. **Does it fit the system?**
   * It follows the existing patterns and architecture, with no parallel approach.
   * YAGNI.
3. **Does it break anyone else?**
   * No breaking change to an API, event, schema or CLI others depend on, unless versioned.
   * Stored data and queued messages stay backward and forward compatible through a rolling deploy.
   * Each config value and client setting it adds or changes does what the story needs, not merely a valid value, and exists in every environment.
4. **Are its assumptions true?**
   * Each assumption holds, such as "never null", "single-threaded", "returns sorted" or "this table is small", or the code enforces it.
5. **Is it tested?**
   * Tests cover failure paths, not only the happy path, and fail when the code is broken.
   * Tests check behaviour, not implementation.
   * Each guarantee it promises or relies on, such as no lost writes, exactly-once delivery or ordering, has a fault-injection test.
6. **Is it correct?**
   * Edge cases: empty, null, zero, one, many, large, time zones.
   * Errors are handled, not swallowed.
   * No race condition or off-by-one error.
   * Retries and duplicates are idempotent, and multi-step writes are atomic.
7. **Is it secure?**
   * Authorization is enforced and input validated.
   * No sensitive data in logs or URLs.
   * Each new dependency is justified, maintained and pinned.
8. **Can the next person change it?**
   * Names are clear, comments explain why, and the docs it affects are updated.
9. **Will it hold up in production?**
   * No N+1 query, unbounded loop or unbounded result set.
   * Connections, files and locks are released.
   * Network and database calls have timeouts, and retries back off with a limit.
   * A failing dependency degrades the feature, not the system.
   * Migrations and rollout are reversible, and logs and metrics can diagnose it.
