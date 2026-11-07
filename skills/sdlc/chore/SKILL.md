---
name: chore
description: "Use first, before editing, for upkeep no user will notice, such as upgrading or pinning dependencies, the runtime or the database, fixing a CVE, CI jobs, Docker, lockfiles, package managers, deploys or alerts, moving config into the environment, rotating keys or credentials, renewing certificates or replacing deprecated calls: writes a short ticket with its why and its done-when, ready to build."
license: MIT
metadata:
  version: "1.0.0"
---
# Chore

A chore is necessary work that changes nothing a user or caller can observe and is more than restructuring code. A refactoring belongs to the `refactor` skill; a change anyone would notice is a story or a bug.

A chore small enough for one short commit goes straight to the `build` skill, its done-when as the commit's check.

1. **Why and done-when:** take them from the request; ask the person to write only the one it leaves open.
2. **Write it:**

```markdown
Title: <a verb and what changes, five to eight words>
Why: <what it removes, saves or allows, and what happens if it is skipped>
Done when: <an observable check, such as a version a command prints or a pipeline that passes>
Out of scope: <what it leaves alone; delete when nothing tempts>
```

3. **Check it,** and any chore someone else wrote, quoting its text, for a hidden behaviour change (a story or bug), structure only (a refactoring), a why with no consequence such as "tech debt", a done-when no one step can check, a done-when that hides the signal instead of fixing its cause, such as skipping a failing CI job, muting an alert or pinning a vulnerable version, and more than one pull request's work (split it).
4. **File it** by the `tracker` skill as a chore, or let the pull request hold it. A choice costly to reverse, such as a new CI provider or a database major version, goes to the `adr` skill first.
5. **Build** it with the `build` skill, unless the request asked only for the ticket.
