# Split work into stories

For a request too big for one reviewable pull request, or a PRD with several outcomes.

1. **Read it all,** with every document it links. A gap or a contradiction is a question.
2. **Map it** as a user story map, each story a title and an outcome line.
3. **Slice it** vertically:
   * **First story:** the thinnest path a real person can use end to end; for something new, the walking skeleton.
   * **Too big:** split by the first of Lawrence's story-splitting patterns that works. An unknown that blocks every pattern is a spike, by the `spike` skill.
   * **Not too thin:** one medium story beats 5 thin ones. Split only what one reviewable pull request cannot hold, and merge slices no person would use apart.
   * **A non-functional requirement, enabler or hardening** is a criterion on the story that needs it.
4. **Keep them independent:** block a story only by its feature's first story and what it truly waits on, with the reason, never for order alone. A rule two stories share goes to one.
5. **Check coverage:** map each requirement to a story, a criterion, an `Out of scope` line or an open question, and show the leftovers.
6. **Agree it:** show the map, then ask the first story and each dependency with its reason, one question each, before filing. The first story gets its criteria now by create.md; each later one by refine.md when it starts.
