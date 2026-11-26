# A new third-party API

Docs say what the vendor intends, not what a customer's setup does, so end each row with its evidence: `read docs`, `seen in sandbox` or `seen in production`.

## Read the contract first

Read the vendor's auth, quota, webhook and sync pages. Turn each stated behaviour into a question only the business can answer, such as "push notifications can be dropped" into "how stale may our copy be before it is a defect?":

```text
Fact (quote, URL, date read) | Question for the business | Owner | Answer | Proved in sandbox on
```

## Checklist

1. **Access:** sandbox and production credentials, what the sandbox lacks, who approves production access, who signs the vendor agreement, cost, and how long consent takes on each customer's side.
2. **Auth:** the OAuth 2.0 grant (on a user's behalf, or client credentials) or API key, scopes, who consents on the customer's side, token lifetime and refresh.
3. **Limits:** rate limits and quotas per user, app and customer; the throttle response.
4. **Change delivery:** webhook, poll or both; whether a message carries data; documented delay; lost messages; subscription expiry and renewal; recovering a gap.
5. **Sync:** full or incremental, what invalidates a sync token or cursor, how deletes arrive, paging, ordering, conflicts and duplicates.
6. **Data shape:** IDs on both sides, time zones, missing fields.
7. **Failure:** outages, SLA, what our users see, the support channel.

## The thin path

The finish line is an end-to-end spike through the real sandbox: connect and refresh a token, write one record, receive one vendor-side change by webhook and by poll, and measure the delay. List what it leaves out. Its code is thrown away like any spike's; a path meant to be kept and grown is a story's walking skeleton. Timebox in attempts.

Record each row that could change the plan in the findings file:

```text
Risk | Why it could change the build | Evidence | Spike or question | Owner | Result | Proved on
```
