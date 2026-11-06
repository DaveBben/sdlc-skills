# Create a spec

1. **Show what affects it:** read the story, the code it lands on, its tests, each ADR in force and `AGENTS.md`. Tell the person in plain sentences how what is already built or decided shapes the design, each with its `file:line`. Effects only, never an approach.
2. **None or one,** by SKILL.md, as a `Decided:` line. With none, stop.
3. **List the decisions,** the ones others hang on first, such as the contract or the unit stored, and work them one at a time:
   * **Their approach first:** for each decision costly to reverse, ask the person for theirs, one per question. A part they cannot answer yet they write as `Open:`; give it 2 or 3 real options with their trade-offs, as equals.
   * **Critique it:** what it breaks among the facts from step 1, a failure it leaves unhandled, code it duplicates, a criterion it misses, each with its source: a criterion, a `file:line`, an ADR or `(guess)`. They revise until none remain.
   * **Decide** a choice that is easy to reverse and the code settles: `Decided: <choice>, because <reason>`.
   * **A gap in the story,** such as a failure no criterion states, goes to its open questions by the `story` skill.
4. **Ask what was missed,** and work each one they name like step 3. Show the whole spec once, at the end.
5. **Attach it** by SKILL.md, record each decision costly to reverse by the `adr` skill, then hand the story to the `build` skill.
