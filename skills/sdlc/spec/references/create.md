# Create a spec

1. **Show what affects it:** read the story, the code it lands on, its tests, each ADR in force and `AGENTS.md`. Tell the person in plain sentences how what is already built or decided shapes the design, each with its `file:line`. Effects only, never an approach.
2. **None or one,** by SKILL.md, as a `Decided:` line. With none, stop, unless the person asked for one: say in one line it is not due, and write it.
3. **List the decisions,** the ones others hang on first, such as the contract or the unit stored, and work them one at a time:
   * **Their approach first:** for each decision costly to reverse that the story or request leaves open, ask the person for theirs, all in one message. A part they cannot answer yet they write as `Open:`; give it 2 or 3 real options with their trade-offs: for a one-way door, such as data stored or sent, a contract others call, a dependency, auth, how it deploys or how the parts are split, as equals, with your pick after their answer; otherwise with your pick.
   * **Critique it:** what it breaks among the facts from step 1, a failure it leaves unhandled, code it duplicates, a criterion it misses, a one-way door it opens unnoticed, such as a dependency, stored data or auth, and more than the criteria need, each with its source: a criterion, a `file:line`, an ADR or `(guess)`. They revise or keep it; a kept one is `Decided: <choice>, their call. Risk: <risk>`.
   * **Decide** a choice that is easy to reverse: `Decided: <choice>, because <reason>`.
   * **A gap only the person can fill,** such as behaviour users would see, goes to the story's open questions by the `story` skill.
4. **Name what was missed,** each as a note, and work each one they take up like step 3. Show the whole spec once, at the end.
5. **Attach it** by SKILL.md, record each decision costly to reverse by the `adr` skill, then hand the story to the `build` skill.
