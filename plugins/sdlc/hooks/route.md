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
* **A decision that gets costly to reverse once code or data builds on it,** such as a stored format, a contract or a dependency: the `adr` skill, when it is made.
* **A new product, or its vision, goals, users or non-goals:** the `prd` skill.
* **A change the request already states item by item,** such as a colour, a config value, or which tables and views to drop and add: the `build` skill, with the request's items as its `Done when:` lines instead of a story. An item it leaves open, such as how a new view ranks rows, is build's question.
* **Otherwise, a change to what the product does:** the `story` skill.

Where the product has a PRD, first name the goal the request serves, by the `prd` skill's Check path.

**Do what the person asked, and speak up as you go:** a concern about their choice is a one-line note with your fix and the name of the idea, and the work goes on. Stop to ask only for a gap you cannot fill, a one-way door, or a choice that contradicts their own stated goal.

# Engineering docs: when each is due

The person writes each one; on autopilot, you do. You may fill in its template with headings and facts already in the repository, each with its `file:line`, then critique what they write.

* **PRD:** the product's what and why, only when more than one person must agree what it is for, or it runs for weeks across many stories. Revised when goals change. The `prd` skill.
* **Design doc:** only when a decision costly to reverse binds more than one story. Edited until its stories are built. The `design` skill.
* **Spec:** how one agreed story is built, only when it changes a contract, stored data or rollout, or holds a decision costly to reverse. The `spec` skill.
* **ADR:** each decision that gets costly to reverse once code or data builds on it, when it is made. Never edited, only superseded. The `adr` skill.
* **Architecture:** while designing, the design doc's Design section; once built, the `Boundaries:` line of `AGENTS.md` by the `onboard` skill, edited when a system, store or owner is added, removed or changes. Past 5 lines, a one-page `docs/ARCHITECTURE.md`.
* **None:** a change with no trade-off, which is most changes.

When a session settles a decision costly to reverse that no document holds, offer an ADR.
