# Code a reviewer merges

A passing check is necessary, not sufficient: reviewers reject agent changes that pass, for a wrong or partial fix, for code that ignores the module around it, and for a diff too big to read. Judge the change as the maintainer reading it cold, who must be able to say what it is for, why here and what else it touches.

## Fit the codebase

* **Search before you write.** For each new function, type or constant, search for the verb and the noun it handles, and read the neighbouring files. Use the helper that exists; the copy you write lacks the fix the original already has, such as its time zone handling.
* **A near-twin is a copy.** A function copied with one name changed, several functions alike but for one line, a third `User` type or a one-line wrapper under a new name all fail the same search. A rename changes every caller and leaves no forwarding function behind.
* **Follow the file's own idiom,** its error style, layering and naming, over what you would write in a fresh project. A Java-shaped abstraction in a Go package compiles and still gets sent back.
* **Take a convention from a written rule or from the file you edit,** not from a sibling directory. Agents copy whatever code sits nearest, so where the repository's rules file names a helper or a layer boundary, that wins over any example.

## Abstraction

* **Add a branch before an abstraction.** One `else` for a new format is fine; a map of format to function, a base class or a plugin point waits until the cases repeat.
* **A helper earns its name** by being called twice or by hiding a detail the reader should not need. One that is short, called once and named for its body only adds a jump.
* **Fix the cause once, in the shared code,** not at each call site. Keep a parameter required where every caller passes it: an optional one, a cast or `any` added to shrink the diff moves the bug to the next caller.

## Scope and size

* **Every changed line serves a criterion.** A parameter with a default no caller overrides, a flag, a validation or a doc nobody asked for is cut or put to the person.
* **Keep moves and renames out of logic commits.** A diff that is half renames hides the three new `if`s inside an authorization function. Where the task is a cleanup in code for auth, data or money, change only what was asked.
* **Split past what one reader holds in mind,** one concern per pull request. A mechanical change, such as a rename or a formatter run, may be larger.
* **Leave no trace of the work:** comments that narrate the diff ("used to", "now", "Stage 3"), unused names, or a workaround that says `for now`. A comment states the why the code cannot.

## Evidence for the reviewer

* **The description says what and why** in the problem's terms, and what you ran: the command and its result, and for a performance claim the measurement before and after. For a visible change, a before and after picture.
* **State what you are unsure of** and what you did not check. A reviewer told where to look finds more than one who must guess.
