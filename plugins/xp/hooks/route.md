# Route a change before any work

For a request to change software, load the skill that fits first:

* **Shipped behaviour that is wrong:** the `bug` skill.
* **Structure only, behaviour unchanged:** the `refactor` skill.
* **Work no person or caller will notice,** such as a dependency bump: the `chore` skill.
* **A question throwaway code would answer:** the `spike` skill.
* **An agreed story, ticket or triaged bug to build or pair on:** the `build` skill.
* **How an agreed story gets built:** the `spec` skill.
* **A decision costly to reverse,** one a revert cannot undo: the `adr` skill, before any code.
* **Otherwise, a change to what the product does:** the `story` skill.
