# Create a design doc

1. **Find the need:** the problem, who has it and why now, from the request; ask only for what it leaves out. Where the product has a PRD, name the goal it serves by the `prd` skill's Check path.
2. **Show what affects it:** read the code it lands on, each ADR in force and `AGENTS.md`. Tell the person in plain sentences how what is already built or decided shapes the design, each with its `file:line`. Only the effects a decision depends on, never an approach.
3. **Fill in the template** below: its headings, and the facts from step 2 and today's parts under Context. Nothing else.
4. **The person writes** the goals and non-goals, then the parts, how they connect and where data lives, then each decision costly to reverse, the ones others hang on first; independent ones together. A reversible part they leave open is yours, as `Assumed:`. A costly one they cannot answer yet they write as `Open:`; give it 2 or 3 real options with their trade-offs, as equals, and your pick after their answer.
5. **Critique it,** each finding with its source: a criterion, a `file:line`, an ADR or `(guess)`. They revise or keep their choice; record a kept one under Decisions as their call, with the risk named.
   * a goal no part serves, or a non-goal the design builds;
   * a contradiction with the facts from step 2;
   * a decision with no rejected alternative;
   * an unhandled failure, cost, privacy or security concern;
   * a part that cannot ship in thin stories, or a store or contract change with no migration or rollback path;
   * a part only code can prove, for a spike by the `spike` skill.
6. **Ready** when no `Open:` line would change what gets built. Record each decision costly to reverse by the `adr` skill and shorten its line to `Decided: <choice>. ADR: <link>`, then the person writes the first story by the `story` skill.

```markdown
# <Project or change>

Status: Draft. Author: <person>. Updated: <date>.

## Context

- <the problem, and each fact from step 2 with its file:line>

## Goals and non-goals

- Goal: <a number or event, or the PRD goal it serves>
- Non-goal: <what it will not do>

## Design

<the parts, how they connect and where data lives: a few lines or one diagram>

## Decisions

- Decided: <choice>, because <reason>. Rejected: <alternative>. ADR: <link or none>
- Assumed: <working assumption>, until <what would change it>
- Open: <question>, <owner>, blocks <what>
```
