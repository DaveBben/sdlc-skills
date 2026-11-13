#!/usr/bin/env python3
"""The sdlc plugin's hooks. Reads one hook event as JSON on stdin; `--self-test` runs its tests.

  * Test lock:       an edit that changes or removes a line of a committed test file asks the
                     person; adding tests passes. A shell command that does the same is reported
                     back to the agent as soon as it has run.
  * Done check:      at Stop, runs the `Check:` line of the root AGENTS.md when the tree changed
                     since the session began or since the last pass, and blocks the stop on failure.
  * Size cap:        refuses an edit that leaves AGENTS.md or CLAUDE.md over 100 lines or 8 KB.
  * Dependency gate: an install command or manifest edit naming a package that no manifest or
                     lockfile in the repository holds asks the person (slopsquatting).
"""
import difflib, hashlib, json, os, re, shlex, subprocess, sys

MAX_LINES, MAX_BYTES = 100, 8 * 1024  # this plugin's choice, sized for a root file of commands, constraints and traps
MAX_BLOCKS = 5  # this plugin's choice: failed checks in a row before the agent may stop anyway
CHECK_SECONDS = 300
INSTRUCTIONS = {"AGENTS.md", "CLAUDE.md"}
# shortcut: test files are found by path; a test file named otherwise is not locked.
TEST = re.compile(r"(^|/)(tests?|spec|specs|__tests__)/|(^|/)test_[^/]+\.py$|_test\.[^/]+$"
                  r"|(^|/)tests\.py$|\.(test|spec)\.[^/]+$|Tests?\.(java|kt|swift|cs)$|_spec\.rb$")
CHECK = re.compile(r"^\s*(?:[-*]\s+)?(?:\*\*)?`?Check:(?:\*\*)?`?\s*(.+?)\s*$", re.M)
# Each manifest's pattern captures a dependency's name from one added line.
MANIFESTS = {
    "package.json": r'^\s*"([^"]+)"\s*:\s*"(?:[\^~<>=*\d]|npm:|git|https?:|file:|workspace:|latest)',
    "pyproject.toml": r'^\s*"([A-Za-z0-9][\w.-]*)\s*(?:\[[^\]]*\])?\s*(?:[<>=!~;@].*)?",?\s*$',
    "requirements.txt": r"^([A-Za-z0-9][\w.-]*)",
    "Pipfile": r'^([A-Za-z0-9][\w.-]*)\s*=',
    "Cargo.toml": r'^([A-Za-z0-9][\w-]*)\s*=\s*["{]',
    "go.mod": r"^\s*(?:require\s+)?([\w.-]+\.[\w.-]+/[\w./-]+)\s+v",
    "Gemfile": r"^\s*gem\s+[\"']([^\"']+)",
}
LOCKFILES = {"package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lock", "uv.lock", "poetry.lock",
             "Pipfile.lock", "Cargo.lock", "go.sum", "Gemfile.lock"}
INSTALL = re.compile(r"^(?:(?:python3?\s+-m\s+|uv\s+)?pip3?\s+install|(?:uv|poetry|pdm|pnpm|yarn|bun|cargo|bundle)\s+add"
                     r"|npm\s+(?:install|i|add)|go\s+get|gem\s+install)\s+(.*)$")
VALUE_FLAGS = {"-r", "-c", "-e", "-i", "-f", "-t", "-p", "--requirement", "--constraint", "--editable", "--index-url",
               "--extra-index-url", "--find-links", "--target", "--prefix", "--python", "--group", "--registry"}
# Commands that change files from git's own history, which the test lock leaves alone.
GIT_MOVES = re.compile(r"\bgit\s+(pull|merge|rebase|checkout|switch|reset|stash|cherry-pick|revert|restore|am|worktree)\b")


def git(cwd, *args):
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, errors="replace")
    return r.stdout if r.returncode == 0 else None


def manifest_kind(path):
    base = os.path.basename(path)
    return "requirements.txt" if re.fullmatch(r"requirements.*\.txt", base) else base if base in MANIFESTS else None


def read(path):
    try:
        return open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return ""


def after(tool, inp, old):
    """The file's text once the edit tool runs, or None when the edit cannot apply."""
    if tool == "Write":
        return inp.get("content", "")
    text = old
    for e in (inp.get("edits") if tool == "MultiEdit" else [inp]) or []:
        a, b = e.get("old_string", ""), e.get("new_string", "")
        if a not in text:
            return None
        text = text.replace(a, b) if e.get("replace_all") else text.replace(a, b, 1)
    return text


def removed(old, new):
    """Lines of old that new changes or drops."""
    a, b = old.splitlines(), new.splitlines()
    return [l for tag, i, j, _, _ in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes()
            if tag in ("delete", "replace") for l in a[i:j]]


def known_text(root):
    files = (git(root, "ls-files") or "").splitlines()
    return "\n".join(read(os.path.join(root, f)) for f in files
                     if manifest_kind(f) or os.path.basename(f) in LOCKFILES).lower()


def unknown(names, known):
    return [n for n in names if not re.search(r"(?<![\w-])" + re.escape(n.lower()) + r"(?![\w-])", known)]


def new_packages(kind, old, new):
    old_lines = set(old.splitlines())
    hits = (re.match(MANIFESTS[kind], l) for l in new.splitlines() if l not in old_lines)
    return [m.group(1) for m in hits if m]


def installs(command):
    """Package names an install command adds. A URL or git source counts as a name, a local path does not."""
    names = []
    for part in re.split(r"&&|\|\||[;|\n]", command):
        m = INSTALL.match(part.strip())
        if not m:
            continue
        try:
            words = shlex.split(m.group(1))
        except ValueError:
            words = m.group(1).split()
        skip = False
        for w in words:
            if skip or w.startswith("-"):
                skip = not skip and w in VALUE_FLAGS
                continue
            if w.startswith((".", "/", "~")) or w.endswith((".txt", ".toml", ".whl", ".tgz")):
                continue
            name = re.split(r"[\[<>=!~;]", w, maxsplit=1)[0]
            names.append(name if "://" in name else re.sub(r"(?<=.)@[^/]*$", "", name))
    return names


def ask(reason):
    return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "ask",
                                   "permissionDecisionReason": reason}}


def deny(reason):
    return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                   "permissionDecisionReason": reason}}


def pre_edit(tool, inp, cwd):
    path = os.path.join(cwd, inp.get("file_path", ""))
    base, old = os.path.basename(path), read(path)
    new = after(tool, inp, old)
    if new is None:
        return None
    if base in INSTRUCTIONS:
        data = new.encode()
        lines = data.count(b"\n") + (bool(data) and not data.endswith(b"\n"))
        if (lines > MAX_LINES or len(data) > MAX_BYTES) and len(data) > len(old.encode()):
            return deny(f"This change leaves {base} over {MAX_LINES} lines or {MAX_BYTES // 1024} KB. Rewrite it instead "
                        "of adding to it: delete lines a check enforces or the repository already shows.")
        was, now = CHECK.search(old), CHECK.search(new)
        if was and (not now or now.group(1) != was.group(1)):
            return ask(f"This edit changes the `Check:` line that decides when work is done, from `{was.group(1)}` "
                       f"to `{now.group(1) if now else 'none'}`.")
    root = (git(os.path.dirname(path) or ".", "rev-parse", "--show-toplevel") or "").strip()
    if not root:
        return None
    rel = os.path.relpath(os.path.realpath(path), os.path.realpath(root))
    if TEST.search(rel):
        head = git(root, "show", f"HEAD:{rel}")
        gone = removed(head, new) if head is not None else []
        gone = [l for l in gone if l.strip()]
        if gone:
            return ask(f"Locked test: {rel} is committed and this edit changes or removes {len(gone)} of its lines, "
                       f"first `{gone[0].strip()[:80]}`. Code changes to fit a committed test. Approve only when the "
                       "test itself is wrong.")
    kind = manifest_kind(path)
    if kind:
        names = unknown(new_packages(kind, old, new), known_text(root))
        if names:
            return ask(f"First-seen dependency: {', '.join(names)} is in no manifest or lockfile of this repository. "
                       "Confirm each name exists on its registry and is the package you mean.")
    return None


def test_removals(root, rev):
    out = git(root, "diff", "--numstat", "--no-renames", rev, "--") or ""
    rows = (l.split("\t") for l in out.splitlines())
    return {r[2]: int(r[1]) for r in rows if len(r) == 3 and r[1].isdigit() and int(r[1]) and TEST.search(r[2])}


def state_path(root):
    d = (git(root, "rev-parse", "--absolute-git-dir") or "").strip()
    return os.path.join(d, "sdlc-guard.json") if d else None


def load(root):
    try:
        return json.load(open(state_path(root)))
    except (OSError, ValueError, TypeError):
        return {}


def save(root, state):
    if state_path(root):
        json.dump(state, open(state_path(root), "w"))


def fingerprint(root):
    h = hashlib.sha256()
    for part in (git(root, "rev-parse", "HEAD"), git(root, "diff", "HEAD")):
        h.update((part or "").encode(errors="replace"))
    for f in (git(root, "ls-files", "-o", "--exclude-standard") or "").splitlines():
        try:
            s = os.stat(os.path.join(root, f))
            h.update(f"{f}{s.st_size}{s.st_mtime_ns}".encode())
        except OSError:
            pass
    return h.hexdigest()


def pre_bash(command, root):
    names = unknown(installs(command), known_text(root))
    state = load(root)
    state["head"] = (git(root, "rev-parse", "HEAD") or "").strip()
    state["tests"] = test_removals(root, state["head"]) if state["head"] else {}
    save(root, state)
    if names:
        return ask(f"First-seen dependency: {', '.join(names)} is in no manifest or lockfile of this repository. "
                   "Confirm each name exists on its registry and is the package you mean.")
    return None


def post_bash(command, root):
    state = load(root)
    if not state.get("head") or GIT_MOVES.search(command):
        return None
    before = state.get("tests", {})
    hit = sorted(f for f, n in test_removals(root, state["head"]).items() if n > before.get(f, 0))
    if hit:
        return {"decision": "block", "reason":
                f"That command changed or removed lines of committed tests, which are locked: {', '.join(hit)}. "
                f"Restore each with `git checkout {state['head'][:10]} -- <file>` and change the code to fit the test. "
                "When the test itself is wrong, ask the person."}
    return None


def stop(root):
    state, fp = load(root), fingerprint(root)
    if fp in (state.get("baseline"), state.get("passed")):
        return None
    m = CHECK.search(read(os.path.join(root, "AGENTS.md")) or read(os.path.join(root, "CLAUDE.md")))
    if not m:
        return None
    cmd = m.group(1).strip("`")
    if fp == state.get("failed"):
        return {"systemMessage": f"sdlc: `{cmd}` still fails, and nothing changed since it last ran."}
    try:
        r = subprocess.run(cmd, shell=True, cwd=root, capture_output=True, text=True, errors="replace", timeout=CHECK_SECONDS)
        ok, out = r.returncode == 0, (r.stdout + r.stderr)
    except subprocess.TimeoutExpired:
        ok, out = False, f"timed out after {CHECK_SECONDS} s. Move slow checks to a `Full check:` line."
    fp = fingerprint(root)  # the check may write files
    if ok:
        state.update(passed=fp, blocks=0)
        save(root, state)
        return None
    state.update(failed=fp, blocks=state.get("blocks", 0) + 1)
    save(root, state)
    if state["blocks"] > MAX_BLOCKS:
        return {"systemMessage": f"sdlc: `{cmd}` failed {state['blocks']} times in a row. The work is not done."}
    return {"decision": "block", "reason":
            f"The work is not done: `{cmd}` fails.\n" + "\n".join(out.splitlines()[-40:]) +
            "\nFix the cause in the code. To stop instead, for a question or because the failure is in the person's "
            "own unfinished work, stop again without changing a file and say what fails."}


def main():
    try:
        inp = json.load(sys.stdin)
    except ValueError:
        return
    event, tool, ti = inp.get("hook_event_name"), inp.get("tool_name"), inp.get("tool_input") or {}
    cwd = inp.get("cwd") or os.getcwd()
    root = (git(cwd, "rev-parse", "--show-toplevel") or "").strip()
    out = None
    if event == "PreToolUse" and tool in ("Edit", "Write", "MultiEdit"):
        out = pre_edit(tool, ti, cwd)
    elif not root:
        return
    elif event == "PreToolUse" and tool == "Bash":
        out = pre_bash(ti.get("command", ""), root)
    elif event == "PostToolUse" and tool == "Bash":
        out = post_bash(ti.get("command", ""), root)
    elif event == "SessionStart":
        if inp.get("source") in (None, "startup", "clear"):
            save(root, {"baseline": fingerprint(root)})
    elif event == "Stop":
        out = stop(root)
    if out:
        print(json.dumps(out))


def self_test():
    import tempfile
    t = os.path.realpath(tempfile.mkdtemp())
    run = lambda *a: subprocess.run(a, cwd=t, check=True, capture_output=True)
    put = lambda name, text: (os.makedirs(os.path.dirname(os.path.join(t, name)) or t, exist_ok=True),
                              open(os.path.join(t, name), "w").write(text))
    run("git", "init", "-q")
    run("git", "config", "user.email", "t@t"); run("git", "config", "user.name", "t")
    put("tests/test_a.py", "def test_a():\n    assert f(2) == 4\n")
    put("pyproject.toml", '[project]\ndependencies = [\n    "httpx>=0.27",\n]\n')
    put("package.json", '{\n  "scripts": {"test": "vitest"},\n  "dependencies": {\n    "react": "^19.0.0"\n  }\n}\n')
    put("AGENTS.md", "Check: `python3 -c \"import sys; sys.exit(open('flag').read() != 'ok')\"`\n")
    put("flag", "ok")
    run("git", "add", "-A"); run("git", "commit", "-qm", "base")
    decision = lambda o: o and o["hookSpecificOutput"]["permissionDecision"]

    # Test lock
    e = lambda old, new, f="tests/test_a.py": pre_edit("Edit", {"file_path": f, "old_string": old, "new_string": new}, t)
    assert decision(e("== 4", "== 5")) == "ask", "changing an assertion of a committed test asks"
    assert not e("assert f(2) == 4\n", "assert f(2) == 4\n\ndef test_b():\n    assert f(3) == 9\n"), "adding a test passes"
    assert decision(pre_edit("Write", {"file_path": "tests/test_a.py", "content": ""}, t)) == "ask", "emptying it asks"
    assert not pre_edit("Write", {"file_path": "tests/test_new.py", "content": "x"}, t), "a new test file passes"
    put("tests/test_new.py", "def test_n():\n    assert 1\n")
    assert not e("assert 1", "assert 2", "tests/test_new.py"), "an uncommitted test is not locked"
    assert removed("a\nb\n", "a\nx\nb\n") == [] and removed("a\nb\n", "a\n") == ["b"]
    assert not pre_bash("sed -i '' s/4/5/ tests/test_a.py", t)
    put("tests/test_a.py", "def test_a():\n    assert f(2) == 5\n")
    assert "tests/test_a.py" in post_bash("sed -i '' s/4/5/ tests/test_a.py", t)["reason"], "a shell edit is reported"
    assert not post_bash("git checkout other", t), "a branch switch is not"
    pre_bash("ls", t)
    assert not post_bash("ls", t), "a change from before the command is not reported again"
    run("git", "checkout", "--", "tests/test_a.py")

    # Size cap and the Check: line
    full = "line\n" * MAX_LINES
    w = lambda content, f="AGENTS.md": pre_edit("Write", {"file_path": os.path.join(t, f), "content": content}, t)
    assert not w(full, "CLAUDE.md") and decision(w(full + "x\n", "CLAUDE.md")) == "deny", "the cap is 100 lines"
    assert not w(full * 2, "README.md"), "other files pass"
    assert decision(w("Check: `true`\n")) == "ask", "weakening the check asks"
    assert not w(read(os.path.join(t, "AGENTS.md")) + "Trap: x\n"), "another line passes"
    assert CHECK.search("* **Check:** `make test`").group(1) == "`make test`" and not CHECK.search("Full check: x")

    # Dependency gate
    assert installs("pip install -r requirements.txt 'httpx[http2]>=0.27' -e . && npm i -D @types/node@20 left-pad") \
        == ["httpx", "@types/node", "left-pad"]
    assert installs("uv add --dev pytest; go get github.com/a/b@v1; echo pip install x") == ["pytest", "github.com/a/b"]
    assert decision(pre_bash("uv add reqeusts", t)) == "ask" and not pre_bash("pip install httpx", t)
    assert not pre_bash("npm install", t) and not pre_bash("npm i react@19", t)
    p = lambda old, new, f: pre_edit("Edit", {"file_path": f, "old_string": old, "new_string": new}, t)
    assert decision(p('"httpx>=0.27",', '"httpx>=0.27",\n    "reqeusts",', "pyproject.toml")) == "ask"
    assert not p('"httpx>=0.27",', '"httpx>=0.28",', "pyproject.toml"), "a version bump passes"
    assert not p("[project]", "[project]\nname = \"x\"", "pyproject.toml"), "a setting passes"
    assert decision(p('"react": "^19.0.0"', '"react": "^19.0.0",\n    "left-pad": "^1.3.0"', "package.json")) == "ask"
    assert not p('"test": "vitest"', '"test": "vitest", "lint": "eslint ."', "package.json"), "a script passes"

    # Done check
    save(t, {"baseline": fingerprint(t)})
    assert stop(t) is None, "an unchanged tree runs no check"
    put("flag", "no")
    assert stop(t)["decision"] == "block", "a failing check blocks the stop"
    assert "systemMessage" in stop(t), "stopping again with nothing changed is allowed, and the person is told"
    put("flag", "ok"); put("fix.py", "x = 1\n")
    assert stop(t) is None and load(t)["blocks"] == 0, "a passing check lets it stop"
    for i in range(MAX_BLOCKS + 1):
        put("flag", "no" + str(i))
        last = stop(t)
    assert "systemMessage" in last, "after 5 failures in a row it may stop, and the person is told"
    print("self-test passed")


if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test"]:
        self_test()
    else:
        main()
