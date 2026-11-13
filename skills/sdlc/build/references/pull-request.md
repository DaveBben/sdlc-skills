# Pull request body

Write the body for a person who saw none of the build: nothing outside the repository and the pull request, and no term this plugin coins, such as red commit or holdout.

* **Under 40 lines outside `<details>`:** when it cannot fit, split the change by criterion, as a `Decided:` line.
* **Rewrite, never append:** at every push, rewrite the body against the final diff. A person's answer replaces the line it reverses.
* **Each shortcoming ends one of three ways:** fixed, filed as an issue with its number, or asked under `Needs you`.
* **Decided by people:** only choices that change the ticket, a locked test, or something costly to reverse. The agent's `Decided:` lines go in `<details>`.

```markdown
## Why
<2 to 4 sentences: the problem, why this approach, what it costs. Link the ticket and any decision record.>

## Shortcomings
- <gap>: fixed | filed #<n> | see Needs you
<or "None">

## Needs you
- [ ] Decide: <question>. <your pick, because <reason>; else <options>; a one-way door's options as equals, your pick last>
- [ ] Before deploy: <step>
- [ ] After deploy: <check, with its pass bar>

## Decided by people
- <person>: <decision>

## Tests
<n> added in <n> files. `<check command>` passes (<n> tests, <n>% coverage). Mutation: <n> of <n> killed, or not set up.
Running app: <criterion>: <what was run> -> <what it showed>
Real check: `<command>` on <input>: <result> against <bar>, or none, <reason>.
Tests from before the branch or written before the code, changed with a person's agreement: <hash> <file>: <why>, or none.

<details><summary>Agent decisions, test names, results of the check on changed tests</summary>

<each as given>
</details>
```
