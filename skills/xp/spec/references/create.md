# Create a spec

1. **Read the ground:** the story with its criteria and comments, through the `tracker` skill when it is an issue; the code it lands on and its tests; each ADR in force under `docs/adr/`; and `AGENTS.md`.
2. **Size it** by SKILL.md, as a `Decided:` line.
3. **Map the decisions as a tree (IBIS):** start with the decisions the others hang on, such as the interface contract or the unit stored. Each settled answer opens the decisions that hang off it; take those next, and close a branch once only minor, easily reversible choices remain. Write each answer into its section of full.md, in the sections the size keeps. After each answer, show the tree: each decision under the one it hangs off, marked settled, open or `Decided:`.
   * **Show your suggestion first,** as a worked example: the lines you would write, why they fit, and the source of each why: the story or their words, a `file:line`, an ADR, or `(guess)`.
   * **Ask** each decision, one per question, through the question tool, such as AskUserQuestion: your suggestion, one or two real alternatives each with its trade-off, and Modify. When they pick another, say in one line what it changes.
   * **Decide** a choice that is easy to reverse and the code settles, and write it as `Decided: <choice>, because <reason>` instead of asking.
   * **A gap in the story,** such as a failure no criterion states, goes to the story's open questions by the `story` skill.
   * **Fading:** once they pick an alternative or a Modify as sound as yours on a kind of decision, ask for their approach before showing yours.
4. **Ask what was missed:** "Is there a decision, risk or section we have not considered?" Work each one they name like step 3.
5. **Attach it** by SKILL.md, offer each decision costly to reverse to the `adr` skill, and hand the story to the `build` skill.
