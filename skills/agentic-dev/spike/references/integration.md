# A new third-party web API or SaaS integration

Docs say what the vendor intends, not what a customer's setup does, so give each row its evidence: `read docs`, `seen in sandbox` or `seen in production`.

## Read the contract first

Read the vendor's auth, quota, webhook, sync and versioning pages. Turn each stated behaviour into a question only the business can answer, such as "push notifications can be dropped" into "how stale may our copy be before it is a defect?". Record each fact or risk that could change the plan in the finding, in one table:

```text
Fact or risk (quote, URL, date read) | Question for the business | Owner | Answer | Evidence: read docs, seen in sandbox or seen in production
```

## Checklist

1. **Access:** sandbox and production credentials, what the sandbox lacks, who approves production access, who signs the vendor agreement, cost, and how long consent takes on each customer's side.
2. **Auth:** the OAuth 2.0 grant (on a user's behalf, or client credentials) or API key, scopes, who consents on the customer's side, token lifetime and refresh.
3. **Limits:** rate limits and quotas per user, app and customer; the throttle response.
4. **Change delivery:** webhook, poll or both; whether a message carries data; documented delay; lost messages; subscription expiry and renewal; recovering a gap.
5. **Sync:** full or incremental, what invalidates a sync token or cursor, how deletes arrive, paging, ordering, conflicts and duplicates.
6. **Data shape:** IDs on both sides, time zones, missing fields.
7. **Failure:** outages, SLA, what our users see, the support channel, and retry safety: idempotency keys for writes, so a retried payment does not charge twice.
8. **Versioning:** the version we pin, how the vendor versions, the deprecation notice, and how breaking changes are announced.

## The thin path

The finish line is the thinnest end-to-end path through the real sandbox that touches each risk the checklist raised, such as connecting and refreshing a token, writing one record, and receiving one vendor-side change by webhook and by poll with its delay. List what it leaves out. Its code is thrown away like any spike's; a path meant to be kept and grown is a story's walking skeleton. Timebox in attempts.
