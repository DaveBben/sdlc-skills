# Route a change before any work

For a request to change software, load the skill that fits first:

* **Shipped behaviour that is wrong:** the `bug` skill.
* **Structure only, behaviour unchanged:** the `refactor` skill.
* **Work no person or caller will notice:** the `chore` skill.
* **A question throwaway code would answer,** including what to build while the design is still changing: the `spike` skill.
* **Pairing with the person,** or working on code together from any starting point: the `pair-programming` skill.
* **An agreed story, ticket or triaged bug to build:** the `build` skill.
* **The design of a project or change spanning several stories,** or a design the person has lost track of: the `design` skill.
* **How an agreed story gets built:** the `spec` skill.
* **A decision costly to reverse,** one a revert cannot undo: the `adr` skill, before any code.
* **A new product, or its vision, goals, users or non-goals:** the `prd` skill.
* **A change with one visible result,** such as a colour, a label, a timing or a config value: the `build` skill, with a one-line `Done when:` the person writes instead of a story.
* **Otherwise, a change to what the product does:** the `story` skill.

Where the product has a PRD, first name the goal question the request helps answer, by the `prd` skill's Check path.

# Engineering docs: when each is due

The person writes each one. You may fill in its template with headings and facts already in the repository, each with its `file:line`, then critique what they write.

* **PRD:** the product's what and why, once the problem is known. Revised when goals change. The `prd` skill.
* **Design doc:** before building anything with real trade-offs that spans several stories. Edited until building starts, then a record. The `design` skill.
* **Spec:** how one agreed story is built, just before it is built. The `spec` skill.
* **ADR:** each decision a revert cannot undo, when it is made. Never edited, only superseded. The `adr` skill.
* **Architecture:** the parts, how they connect and where data lives: in the design doc while designing; once built, the `Boundaries:` line of `AGENTS.md` by the `onboard` skill, updated only when it hurts.
* **None:** a change with no trade-off.

When a session settles a design choice that no document holds, offer to write it down before the session ends.
