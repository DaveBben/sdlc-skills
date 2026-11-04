# Route a change before any work

For a request to change software, load the skill that fits first:

* **Shipped behaviour that is wrong:** the `bug` skill.
* **Structure only, behaviour unchanged:** the `refactor` skill.
* **Work no person or caller will notice:** the `chore` skill.
* **A question throwaway code would answer,** including what to build while the design is still changing: the `spike` skill.
* **An agreed story, ticket or triaged bug to build or pair on:** the `build` skill.
* **How an agreed story gets built:** the `spec` skill.
* **A decision costly to reverse,** one a revert cannot undo: the `adr` skill, before any code.
* **A new product, or its vision, goals, users or non-goals:** the `prd` skill.
* **A change with one visible result,** such as a colour, a label, a timing or a config value: the `build` skill, with a one-line `Done when:` the person writes instead of a story.
* **Otherwise, a change to what the product does:** the `story` skill.

Where the product has a PRD, first name the goal question the request helps answer, by the `prd` skill's Check path.
