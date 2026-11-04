---
name: chore
description: "Use first, before editing, for upkeep no user will notice, such as upgrading or pinning dependencies, the runtime or the database, fixing a CVE, CI jobs, Docker, lockfiles, package managers, deploys or alerts, moving config into the environment, rotating keys or credentials, renewing certificates or replacing deprecated calls: writes a short ticket with its why and its done-when, ready to build."
license: MIT
metadata:
  version: "1.0.0"
---
# Chore

A chore is necessary work that changes nothing a user or caller can observe and is more than restructuring code. A refactoring belongs to the `refactor` skill; a change anyone would notice is a story or a bug.

1. **Ask** the user only why now and what done looks like.
2. **Write it:**

```markdown
Title: <a verb and what changes, five to eight words>
Why: <what it removes, saves or allows, and what happens if it is skipped>
Done when: <an observable check, such as a version a command prints or a pipeline that passes>
Out of scope: <what it leaves alone; delete when nothing tempts>
```

3. **Check it,** and any chore someone else wrote, quoting its text, for a hidden behaviour change (a story or bug), structure only (a refactoring), a why with no consequence such as "tech debt", a done-when no one step can check, and more than one pull request's work (split it).
4. **Agree it:** show it and ask whether to build it now. A choice costly to reverse, such as a new CI provider, goes to the `adr` skill first. File it by the `tracker` skill as a chore, or let the pull request hold it.
5. **Build** it with the `build` skill. One small enough for a single short commit needs no ticket.
