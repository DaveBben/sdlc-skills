# Design choices

Each item below in the plan is a design choice: bring it to the person with the options, your pick and why, and agree it before the tests. The implementation choices at the end you make yourself, within these rules.

## Data

* Adding, removing, renaming or changing the type of a database table, column, index or constraint
* Anything that needs a data migration or backfill
* Changing what is the source of truth for a piece of data
* Adding a cache or a copy of data that already lives somewhere else
* Changing how long data is kept, or when it is deleted

## Interfaces and contracts

* Adding, removing or changing a public API endpoint, request or response shape, event, webhook, CLI flag, config key or file format
* Changing anything another team, service or customer depends on
* Changing error codes or error formats that callers may handle

## Architecture and boundaries

* Creating a new service, package, module or top-level directory
* Moving responsibility from one component to another
* Adding a new dependency between components that did not talk before
* Adding a new third-party library, framework or external service
* Adding new infrastructure: a queue, database, cron job or background worker

## Guarantees and behaviour

* Changing consistency, ordering, retry, idempotency or transaction behaviour
* Choosing between failing loudly and failing silently or degrading
* Changing concurrency: locks, parallelism, async or sync
* Changing performance in a way users would notice, such as moving work into a request path

## Security and trust

* Anything touching authentication, authorization, permissions or roles
* Handling secrets, tokens, credentials or personal data
* Deciding which input is trusted or which validation is skipped

## Platform and budgets

* Raising a minimum OS, browser, runtime, language or hardware version
* A new app or OS permission
* Changing a memory, flash, battery, frame, bundle-size or cost budget
* A change that destroys and recreates live infrastructure, or changes how devices or installs update

## Product scope

* Behaviour the story does not define: edge cases, empty states, limits, cancellations
* Adding a feature, option or setting nobody asked for
* Removing or changing existing user-visible behaviour

## Implementation choices: decide freely

* Names of variables, functions, private classes and files inside an existing module
* How to structure code inside a function or module: splitting, extracting helpers, loops or map
* Which existing internal utility or installed library function to use
* Writing, extending or fixing tests
* Fixing a bug where the intended behaviour is already clear
* Refactors that change no behaviour or interface
* Logging, comments and docs for code you changed
* Formatting and lint fixes
