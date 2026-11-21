# A new third-party API

Feasibility risk in an integration surfaces only on a real call. Docs say what the vendor intends, not what a customer's tenant does, so each row ends `read docs`, `seen in sandbox` or `seen in production`.

## Read the contract first

Read the vendor's auth, quota, webhook and sync pages, and turn each stated behaviour into a question only the business can answer:

```text
Fact (quote, URL, date read) | Question for the business | Owner | Answer | Proved in sandbox on
```

For example, "push notifications can be dropped" becomes "how stale may the screen be before it is a defect?". The vendor's limits set what a quality word such as "fast" can honestly mean.

## Checklist

1. **Access:** sandbox and production credentials, who signs the vendor agreement, cost, and how long each customer's admin consent takes.
2. **Auth:** flow, scopes, delegated or app permission, who approves in the customer's tenant, token expiry and refresh.
3. **Limits:** rate limits and quotas per user, app and tenant; the throttle response; back-off.
4. **Change delivery:** webhook, poll or both; whether a message carries data; documented delay; lost messages; subscription expiry and renewal; recovering a gap.
5. **Sync:** full vs incremental, what invalidates a sync token, how deletes arrive, paging, ordering and conflicts, idempotency and duplicates.
6. **Data shape:** the vendor's object against ours: IDs on both sides, time zones, recurrence, missing fields.
7. **Sandbox vs production:** what the sandbox lacks, and who approves production access.
8. **Failure:** outages, SLA, what our users see, the support channel.

## The thin path

The finish line is a walking skeleton through the real sandbox: connect and refresh a token, write one record, receive one vendor-side change by webhook and by poll, and measure the delay. Say up front whether the code is kept as a tracer bullet or deleted, and list what it leaves out.

Record each could-change-the-plan row in the findings file:

```text
Risk | Why it could change the build | Evidence | Spike or question | Owner | Result | Proved on
```
