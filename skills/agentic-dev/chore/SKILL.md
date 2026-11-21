---
name: chore
description: "Use first, before editing any file, for a chore: a change to code, configuration, dependencies or tooling that no user of the software would notice, however small or casually phrased, such as a refactor, a rename, deleting dead code, bumping a dependency, formatting, lint, type-check, hook or CI setup, moving to another host with the same behaviour, or installing a dev tool, like 'rename total to order_total everywhere', 'bump the requests dependency', 'tidy pricing.py without changing what it does' or 'set up pre-commit'. Not for a change a user would notice: that is the story skill's. Sets one done-check, explores what is unfamiliar, runs or files the spikes it needs, then hands to the building skill."
license: MIT
metadata:
  version: "7.0.0"
---
# Chore

A chore changes nothing a user would notice, so it gets no story, no acceptance criteria and no UAT.

* **Write one `Done when:` line,** such as the existing tests unchanged and green, or the CI job passing on a branch.
* **Grill a vague chore:** what "tidy" or "harden" means here, and how we will know it is done.
* **Ask why** when it names a fix but not the problem (XY problem).
* **Offer up to 3 parts to explore,** new to this codebase or to the person, each with the question that matters. Mark each answer `doc`, with the link, or `memory`.
* **Spike an unknown that could change the plan:** run it now in a subagent when it fits this session. When it needs a day, or someone else's access or data, file it with the spike skill, blocking the chore, and stop.
* **Before a refactor,** add characterization tests where the tests miss the moved code.
* **More than one chore, or one for later:** file each with the tracker skill, labelled `chore`, and build one per session.
* **Then load the building skill.**
