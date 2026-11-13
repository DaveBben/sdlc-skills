# sdlc

Whoever made the change, someone else attacks it, and a machine decides when it's done.

## What runs in a session

One script, [`hooks/guard.py`](hooks/guard.py), handles 4 hooks. `python3 hooks/guard.py --self-test` runs its tests.

* **Test lock:** a test file is locked once it is committed. An edit that changes or removes one of its lines asks you first, and in a session with no person it is refused. So does an added line that switches tests off, such as a skip marker, in a test file, `conftest.py` or the test runner's configuration. Other added lines pass. A shell command that changes a locked test is reported to the agent right after it runs, with the command that restores the file.
* **Done check:** when the agent stops and the tree changed during the turn, the hook runs the backticked `Check:` command of the root `AGENTS.md`, as it read when the session began. A `Check:` line that changed mid-session does not run, and you are told. A failure sends the agent back with the last 40 lines of output. The agent may stop anyway by stopping again with no file changed, for a question, and then you see a message that the check still fails.
* **Dependency gate:** `pip install`, `uv add`, `npm install`, `pnpm add`, `yarn add`, `bun add`, `cargo add`, `go get`, `gem install`, `bundle add`, runners such as `npx` and `uvx`, and edits to a manifest ask you when they name a package that no manifest or lockfile in the repository holds.
* **Size cap:** an edit that leaves `AGENTS.md` or `CLAUDE.md` over 100 lines or 8 KB is refused.

Three agents run only when the `build` skill calls for them.

* **critic** (Opus) attacks a design, criteria or tests the session wrote. For tests, it names wrong implementations that pass them, without reading the code under test.
* **reviewer** (Opus) reads the diff, the criteria and the tree, and reports candidate bugs.
* **verifier** (Sonnet) proves or drops each finding without the reviewer's reasoning, and runs each criterion against the running app.

Two skills load when a request matches.

* **build** (about 850 words) covers who authors and who attacks, plus the branch and pull request conventions.
* **onboard** (about 530 words) sets up `AGENTS.md`, the `Check:` line, mutation testing, property-based tests and a sandbox.

## Known limits

* **Test files are found by path,** such as `tests/`, `test_*.py` and `*.test.ts`. A test file named another way is not locked.
* **An added line can still weaken a test,** such as an early return or a second function with the same name. The reviewer checks for that.
* **A weakened test that is committed becomes the locked version.** The shell check reports it once, and after that only the reviewer sees it.
* **The check command runs outside any sandbox,** and a script it calls is the agent's to edit. Point `Check:` at tools, not at a script in the repository.
* **The dependency gate checks the repository, not the registry.** You confirm that a first-seen name is real.
* **A shell command that switches branch or rewrites history** is not checked for test changes.
* **The dependency gate misses** `uv run --with`, `bash -c`, poetry tables and anything outside a git repository.

## One change, traced

"Build PAY-12: orders over 10 units get 10% off."

| Step | Who | What happens |
|---|---|---|
| Criteria | you | Agree 3 criteria, each with an example |
| Tests | agent | Writes failing tests from the examples and commits them |
| Attack | critic | Finds that a constant return passes 2 of them, and the agent adds tests |
| Code | agent | Tries to edit a committed assertion, and the hook asks you |
| Stop | hook | Runs `Check:`, which fails on rounding, and sends the agent back |
| Review | reviewer, verifier | 4 candidates, 1 proved, and each criterion run from the command line |
| Pull request | agent | 180 lines, with the evidence in the body |
