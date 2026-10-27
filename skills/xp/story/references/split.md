# Split work into stories

For a request with more than one path or variation, or a PRD with several outcomes.

1. **Read it all** first, with every document it links: the roles, outcomes, activities a person goes through in order, business rules, kinds of data, non-functional requirements, and non-goals. A gap or a contradiction is a question.
2. **Map it** as a user story map, each step's must-have story first. Each gets a title and an outcome line.
3. **Slice it:**
   * **First story:** the thinnest path a real person can use end to end. For something new, the walking skeleton.
   * **Too big:** split by the first of Lawrence's story-splitting patterns that works: workflow steps, operations, business rule variations, variations in data, interface variations, simple/complex. An unknown that blocks every pattern is a spike, by the `spike` skill.
   * **Vertical slices only:** a story that only adds a table or an endpoint is not one. A non-functional requirement, an enabler or hardening is a criterion on the story that needs it.
4. **Keep them independent:** block a story only by its feature's first story and what it truly waits on, with the reason; never for order alone. Two stories that would both need rewriting if one changed share a rule: give it to one.
5. **Check coverage:** map each requirement to a story, a criterion, an `Out of scope` line or an open question, and show the leftovers.
6. **Agree it:** show the map, then ask the first story and each dependency with its reason, one question each, before filing them. Write criteria for the first story only, by create.md; each later one gets them by refine.md when it starts.
