# Split the criteria into stories

A story describes one small, complete piece of value from the point of view of someone who uses the system, in SKILL.md's template.

## Slice vertically, never horizontally

* **Each story delivers something a real user can see, use or benefit from on its own.** It cuts through every layer it needs, such as interface, logic and storage; firmware, driver and hardware; or source, model and dashboard, to do one thin, complete thing.
* **Never a story for a single technical layer,** such as "set up the database", "build the API" or "create the frontend". Technical work belongs inside the story that needs it.
* **The test:** if this story were the only thing finished, could you show it to a user and have it mean something?

## Map it

For a whole product or a PRD, map it first; for one feature, go to step 5.

1. **Identify the users:** every distinct type of person who interacts with the system, such as customer, staff member, admin or owner.
2. **Map each user's journey:** the main steps they take, in order, from start to finish.
3. **List the tasks under each step:** the specific things the user needs to do.
4. **Find the thinnest usable version (the MVP):** the smallest set of stories that lets a user complete the whole core journey end to end, even crudely. Mark these Release 1.
5. **Make the first story the thinnest end-to-end version:** for a new product or system, the walking skeleton, the thinnest path through every layer, running where its users will run it; for a feature in an existing product, the feature's thinnest end-to-end version.
6. **Group the rest into later releases,** ordered by value, so each release improves something that already works.
7. **Place each confirmed criterion in exactly one story.** One that fits no story is a question for the person, not a new story you invent.

## Splitting patterns

When a story is too big, split it by one or more of these:

* **Workflow steps:** a process into its stages, such as enter address, choose shipping, pay, confirm.
* **Happy path first:** the case where everything goes right, then stories for errors, invalid input and edge cases.
* **Business rule variations:** the simplest rule first (flat fee), then the complex ones (fee by distance).
* **Data variations:** one type first (credit cards), then the others (Apple Pay, PayPal).
* **CRUD operations:** "manage X" into view, add, edit and delete.
* **User roles:** a story for what each type of user needs.
* **Simple now, better later:** a basic version first (a hard-coded list, a fixed estimate, a manual step), then stories that improve or automate it.
* **A spike for an unknown:** when the approach is unclear, a time-boxed spike to investigate, then split once it is resolved.

## Show it

1. **Project summary:** one or two sentences on the goal.
2. **Users:** the user types.
3. **Stories by release,** the MVP first, each with a short ID (S1, S2, ...), the story, its criteria, the splitting pattern used and its dependencies. Each is independent where it can be, valuable on its own and testable by its criteria; split one that joins several capabilities with "and", and never write one giant story for the whole project.
4. **Deferred ideas:** stories that may have value later.
5. **Open questions:** each assumption or unknown that needs the person's decision.

Before you show it, check that Release 1 alone lets a user complete the core journey end to end.
