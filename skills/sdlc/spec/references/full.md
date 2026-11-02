# Spec sections

```markdown
## Spec

Author: <who>. Reviewers: <a person from each team that consumes or supplies it>.
Story assumptions: <each reading the person chose of a criterion the story leaves open, written back to the story>
Delete when: every Promote item is ticked, as the story closes.

1. Disciplines affected: each team as owner, consumer, supplier or not affected, and what that means here.
2. Interface contracts: each endpoint, message, event or schema added or changed, with its success, its errors and what a client shows. Promote: to the contract's home, such as the OpenAPI file.
3. Where each criterion is enforced: per AC, the one place that enforces it and what clients only reflect.
4. Data and state: tables, keys and indexes; consistency, such as read-your-writes; caches; what happens to existing data; deletion of personal data. Promote: the `Boundaries:` line of `AGENTS.md`, by the `onboard` skill, when this adds a store, system or repository or changes who writes one.
5. Failure handling: per failure, what the system does.
6. Compatibility and rollout: old clients and versions in the field, the feature flag and its off state, the rollout steps, and the rollback.
7. Constraints and budgets: latency, payload, rate limits, capacity, privacy.
8. Key decisions: ID, the ID it hangs off, decision, why, the alternative rejected, and Promote: an ADR for one costly to reverse, else where it is captured or `dies with the spec`.
9. Sequencing: what goes first so no team waits, such as the contract and a mock built from it. Tasks live in the tracker.
10. Verification: per AC, the test that stays in the repository, plus contract tests and the events the story's `Measure:` needs.
11. Open questions and risks: ID, the question or risk, its owner.

Promote before delete:
- [ ] <each Promote item above, and each other item that must outlive the spec, such as the AC tests, a runbook entry or a ticket to remove the flag>
```

For section 5, handle each failure this change can hit, or list it as a risk in section 11: broken object-level authorization (IDOR), a step failing halfway, idempotency under a retry or double submit, a race condition, an unbounded queue or result set, existing data and old clients, an outside service slow or down, time zones, personal data in logs, and a rollback after the new version wrote data.
