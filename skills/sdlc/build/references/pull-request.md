# Pull request body

Write the body for a person who saw none of the build: nothing outside the repository and the pull request, and no term this plugin coins, such as red commit.

* **Under 40 lines outside `<details>`:** when it cannot fit, split the change by criterion, as a `Decided:` line.
* **Rewrite, never append:** at every push, rewrite the body against the final diff. A person's answer replaces the line it reverses.
* **Risks** are what could go wrong once this merges, each ending one of three ways: mitigated, with how; filed as an issue, with its number; or asked under `Needs you`. List every one, including:
  * a hard-to-reverse choice the change makes;
  * a test from before the branch, or committed before the code it tests, changed since: its file, commit and why;
  * a changed function whose complexity or warnings rose, from the `Quality:` line;
  * a mutant the tests let survive, from the `Mutation:` line;
  * a path no test reaches, or one tested only with an outside service replaced;
  * a criterion whose result was not seen in the running app, the command line or a real request;
  * a check not run: no `Mutation:` or `Quality:` line in `AGENTS.md`.
* **Decided by people:** only choices that change the ticket or something costly to reverse.
* **Decided by AI:** every `Decided:` line from the build and its agents, the ones a reviewer is likeliest to question first. Past 5, put the rest in a `<details>` block.

```markdown
## Why
<2 to 4 sentences: the problem, why this approach, what it costs. Link the ticket and any decision record.>

## Risks
- <what could go wrong, and where>: mitigated by <how> | filed #<n> | see Needs you
<or "None found">

## Needs you
- [ ] Decide: <question>. <your pick, because <reason>; else <options>; a one-way door's options as equals, your pick last>
- [ ] Before deploy: <step>
- [ ] After deploy: <check, with its pass bar>

## Decided by people
- <person>: <decision>

## Decided by AI
- <choice>, because <reason> — <file>:<line>, where one applies
```
