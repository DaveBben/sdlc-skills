---
name: slicing
description: "Use when work is too big for one reviewable pull request and must be split before it is built: a PRD, an epic, a feature with several outcomes, a large refactor or a migration, such as 'break this down', 'split this epic into stories', 'how should we slice the reporting feature', 'plan the reports work in pieces' or 'this is too big for one PR'. Splits it into vertical slices, a walking skeleton or the thinnest end-to-end case first, each shippable alone, in risk-then-value order, and hands the first to be built."
license: MIT
metadata:
  version: "4.1.0"
---
# Slicing

Read the request and every document it links first. A gap or a contradiction is a question for the person.

## A slice

* **Vertical:** it cuts through every layer one action touches, such as the screen, the API and the table, and changes something a person or caller can see and a test can check. A layer alone, such as "the schema" or "the API", is a task, not a slice: fold it into the slice that first uses it.
* **Big enough:** one pull request under 400 changed lines, and one fresh session for an agent. Split only what that cannot hold, because each slice costs a review, a merge and a handoff. Merge slices nobody would use or test apart.
* **Independent:** a slice waits only on what it truly needs, and says why. A rule two slices share belongs to one of them.
* **Enablers and hardening,** such as performance, logging or security, are criteria on the slice that needs them, not slices of their own.

## The first slice

* **Something new,** with no path running end to end yet, such as a new service, app or integration: the walking skeleton. That is the smallest real function that runs end to end through the main parts, deployed the way the rest will be. It is kept code, not a prototype; its job is to prove the wiring and the deploy before features pile on.
* **A feature in a running system:** the skeleton already exists, so building one is wasted work. The first slice is the simplest end-to-end case of the feature: one user, one common input, the happy path.

## Splitting one that is too big

Try Lawrence's story-splitting patterns in this order, and take the first that gives pieces of similar size, at least one of which could be deferred or dropped: workflow steps (the simple end-to-end case first, not step 1 alone), operations (create, read, update, delete), business-rule variations, data variations, data-entry methods, major effort (the first case hard, the rest easy), simple then complex, and performance deferred. When an unknown blocks every pattern, the first piece is a spike; split again once it answers.

## Work that does not slice vertically

* **A refactor a feature needs:** make the change easy, then make the easy change (preparatory refactoring). The refactor ships first, as its own slice, with every test passing unchanged.
* **A large refactor:** the Mikado method. Try the goal, note what breaks, revert, and do the prerequisites first, leaves of the graph first, each a slice that keeps main working.
* **A schema or API change:** expand-contract (parallel change), as 3 slices: add the new beside the old, move every caller, remove the old. Plan the remove slice from the start; stopping halfway leaves two paths to maintain.
* **Replacing a system:** strangler fig, moving one route or feature at a time to the new one.

## Order

Before proposing the order, show the risks you see and ask for the ones only the person knows, in the same round as any gaps: what in their stack, environments, other teams or deadlines could sink a slice.

Riskiest first: the slice whose failure would most change the plan, such as an unproven integration or a hard performance bar. Then by value, what the person needs soonest; when they have not said, propose an order and let them change it.

## Hand-off

Show the slices as a numbered list, each with its title, what someone sees when it ships, and what it waits on and why, plus `Decided:` lines for the first slice and the order. Map each requirement in the request to a slice, a criterion or an `Out of scope` line, and show any left over. File the later slices as tickets, with criteria agreed when each one starts. Then offer to build the first slice.
