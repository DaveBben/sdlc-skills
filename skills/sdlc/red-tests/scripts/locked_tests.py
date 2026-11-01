#!/usr/bin/env python3
"""Usage: locked_tests.py <merge target> [<red commit>...] | --self-test

Run in the branch's worktree. Prints each change the branch makes to a locked test
file, a test file that existed where the branch left the merge target or one a red
commit holds, one line each:

  <commit> <file>: marker | signature | own commit | changes existing | adds to existing | undone | refused (<why>): <subject>

  * marker:     the change only removes an expected-fail marker.
  * signature:  the commit's subject starts `refactor(signature):`.
  * own commit: the commit changes only test files and its message names this file
                or a test in it; a person's agreement must still be named in it.
  * changes existing: a red commit changes a line of a test file from before the branch.
  * adds to existing: a red commit only adds lines to a locked test file; in Python, only new
                top-level defs, classes, imports and assignments to new names, none autouse.
  * refused:    any other change, an uncommitted one included; a red commit's change to
                another red commit's test; and a red test file holding more markers at HEAD
                than it held on the merge target (`HEAD <file>: refused (still marked)`); and a
                red commit not on the branch, such as after a rebase; a red commit whose added
                lines rebind a top-level name already bound in that Python file (`rebinds <name>`);
                and a conftest.py added outside a red commit.
  * undone:     a refused change to a file whose content at a later commit is its locked one, with
                markers removed but none added.

Exits 1 when any line is refused, else 0. Prints nothing when no locked test changed.
"""
import ast, os, re, subprocess, sys, tempfile

# shortcut: test files are found by path patterns; a test file named otherwise is not
# locked by this check, only by the rule the reviewer agent enforces.
TEST = re.compile(r"(^|/)(tests?|spec|specs|__tests__)/|(^|/)test_[^/]+\.py$|_test\.[^/]+$"
                  r"|(^|/)tests\.py$|(^|/)conftest\.py$|\.(test|spec)\.[^/]+$|Tests?\.(java|kt|swift|cs)$|_spec\.rb$")
MARKER_LINE = re.compile(r"^(@pytest\.mark\.xfail\b.*|test\.fail\(\);?|pending(\(|\s+[\x27\"]|$).*"
                         r"|XCTExpectFailure\(.*\)|withKnownIssue\(.*\)\s*\{|\}\s*//\s*red)$")
FAILING = re.compile(r"\.fail(?:ing|s)\(")  # Jest test.failing(, Vitest test.fails(
# shortcut: an added line that skips a test; in Python, any added statement other than a new top-level
# def, class, import or assignment to a new name. Other insertions that defeat an existing test, such as
# a new assignment whose call patches a module, `@pytest.fixture(name=...)`, or an early return added to
# a test in another language, pass here and rest on the reviewer's rule.
SKIPS = re.compile(r"(?i)\bskip|@disabled\b|@ignore\b|\bx(it|describe|test)\(|\bpytestmark\b")



def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, errors="surrogateescape", check=True).stdout  # keeps a binary fixture's bytes distinct


def changed(commit):
    return [l for l in git("diff-tree", "--no-commit-id", "--no-renames", "-r", "--name-only",
                           "--root", commit).splitlines() if l]


def lines_at(rev, path):
    try:
        return git("show", f"{rev}:{path}").splitlines()
    except subprocess.CalledProcessError:  # the file does not exist at rev
        return None


def markers(lines):
    return sum(bool(MARKER_LINE.match(l.strip())) + len(FAILING.findall(l)) for l in lines or [])


def same_unmarked(old, new):
    # Swift's withKnownIssue wraps the body, so removing it re-indents the body; elsewhere,
    # as in Python, indentation can move an assertion where it never runs.
    norm = str.strip if any("withKnownIssue(" in l for l in old) else str.rstrip
    def unmarked(lines):
        return [norm(FAILING.sub("(", l)) for l in lines if not MARKER_LINE.match(l.strip())]
    return unmarked(old) == unmarked(new)


def marker_only(commit, path):
    old, new = lines_at(f"{commit}^", path), lines_at(commit, path)
    return old is not None and new is not None and markers(new) < markers(old) and same_unmarked(old, new)


def names_test(message, commit, path):
    if os.path.basename(path) in message or os.path.splitext(os.path.basename(path))[0] in message:
        return True
    body = [l for l in git("show", "--format=", commit, "--", path).splitlines()
            if not l.startswith(("diff ", "index ", "--- ", "+++ "))]
    return any(n in message for n in re.findall(r"\b([Tt]est[_A-Z0-9]\w*)", "\n".join(body)))  # not "tests"


def binds(stmt):
    """Each name a top-level statement binds, keyed by what it binds it to where that is knowable."""
    if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        return {stmt.name: None}
    if isinstance(stmt, ast.Import):  # `import a.b` binds the module a: the same object as `import a.c`
        return {a.asname or a.name.split(".")[0]: ("import", a.name if a.asname else a.name.split(".")[0]) for a in stmt.names}
    if isinstance(stmt, ast.ImportFrom):
        return {a.asname or a.name: ("from", stmt.level, stmt.module, a.name) for a in stmt.names}
    targets = stmt.targets if isinstance(stmt, ast.Assign) else [getattr(stmt, "target", None)]
    return {n.id: None for t in targets if t for n in ast.walk(t) if isinstance(n, ast.Name)}


def python_addition(old, new):
    """`adds to existing`, `changes existing` or `refused (rebinds ...)` for a Python file whose diff only adds lines."""
    try:
        old_body, new_body = ast.parse("\n".join(old)).body, ast.parse("\n".join(new)).body
    except SyntaxError:
        return "changes existing"
    kept, added = [ast.dump(x) for x in old_body], []
    i = 0
    for stmt in new_body:  # every old statement must survive unchanged and in order
        if i < len(kept) and ast.dump(stmt) == kept[i]:
            i += 1
        else:
            added.append(stmt)
    if i < len(kept):
        return "changes existing"
    old_names = {}
    for stmt in old_body:
        old_names.update(binds(stmt))
    rebound = sorted(n for stmt in added for n, to in binds(stmt).items()
                     if n in old_names and (to is None or to != old_names[n]))
    if rebound:
        return f"refused (rebinds {', '.join(rebound)})"
    simple = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Import, ast.ImportFrom)
    for stmt in added:
        if isinstance(stmt, (ast.Assign, ast.AnnAssign)):
            targets = stmt.targets if isinstance(stmt, ast.Assign) else [stmt.target]
            if not all(isinstance(t, ast.Name) for t in targets):
                return "changes existing"
        elif not isinstance(stmt, simple) or any("autouse" in ast.dump(d) for d in getattr(stmt, "decorator_list", [])):
            return "changes existing"
    return "adds to existing"


def red_change(commit, path):
    """The label for a red commit's change to a locked test file."""
    new = lines_at(commit, path)
    stat = git("diff", "--numstat", "--no-renames", f"{commit}^", commit, "--", path).split("\t")
    added = [l[1:] for l in git("show", "--format=", "-U0", commit, "--", path).splitlines()
             if l[:1] == "+" and l[:3] != "+++"]
    if new is None or stat[0] == "-" or stat[1] != "0" or any(
            SKIPS.search(l) and not MARKER_LINE.match(l.strip()) for l in added):
        return "changes existing"  # deleted, binary, a removed line, or a skip
    return python_addition(lines_at(f"{commit}^", path), new) if path.endswith(".py") else "adds to existing"


def undone(lines, f, rev, at):
    old, new = lines_at(rev, f), lines_at(at, f)
    if old is None or new is None or not same_unmarked(old, new) or markers(new) > markers(old):
        return lines
    return [l.replace(": refused (", ": undone (", 1) if l.split(" ", 1)[1].startswith(f"{f}: refused") else l
            for l in lines]


def check(target, reds):
    base = git("merge-base", target, "HEAD").strip()
    commits = git("rev-list", "--reverse", f"{base}..HEAD").splitlines()
    reds = {git("rev-parse", r).strip() for r in reds}
    lines = [f"{r[:10]} (red commit): refused (not on the branch, such as after a rebase)" for r in sorted(reds - set(commits))]
    reds &= set(commits)
    before = {p for p in git("ls-tree", "-r", "--name-only", base).splitlines() if TEST.search(p)}
    locked = before.union(*(changed(r) for r in reds))
    lock = dict.fromkeys(before, base)  # each locked file -> the commit that fixed its content
    for c in commits:
        files = changed(c)
        subject = git("log", "-1", "--format=%s", c).strip()
        if c in reds:  # a red commit may change a test from before the branch: a person reads it
            for f in sorted(files):
                if f in lock:
                    kind = red_change(c, f)
                    if kind == "changes existing" and lock[f] != base:
                        kind = "refused (red commit changes a red test)"
                    lines.append(f"{c[:10]} {f}: {kind}: {subject}")
                    if kind.startswith("refused"):
                        continue  # the earlier version stays the locked one
                lock[f] = c
            continue
        message = git("log", "-1", "--format=%B", c)
        for f in sorted(files):  # a new conftest.py changes what every test beside it runs
            if os.path.basename(f) == "conftest.py" and f not in locked and lines_at(f"{c}^", f) is None:
                lines.append(f"{c[:10]} {f}: refused (new conftest outside a red commit): {subject}")
        for f in sorted(set(files) & locked):
            if marker_only(c, f):
                kind = "marker"
            elif subject.startswith("refactor(signature):"):
                kind = "signature"
            elif not all(TEST.search(x) or x in locked for x in files):
                kind = "refused (changed beside code)"
            elif not names_test(message, c, f):
                kind = "refused (message names no test in it)"
            else:
                kind = "own commit"
            lines.append(f"{c[:10]} {f}: {kind}: {subject}")
            if f in lock:
                lines = undone(lines, f, lock[f], c)
    for f, rev in sorted(lock.items()):
        now = lines_at("HEAD", f)
        if rev != base and now is not None and markers(now) > markers(lines_at(base, f)):
            lines.append(f"HEAD {f}: refused (still marked)")
    for l in git("status", "--porcelain", "--untracked-files=no").splitlines():
        if l[3:] in locked:
            lines.append(f"uncommitted {l[3:]}: refused (uncommitted)")
    return lines


def self_test():
    with tempfile.TemporaryDirectory() as d:
        os.chdir(d)
        def sh(*a):
            subprocess.run(a, check=True, capture_output=True)
        def commit(msg, files):
            for p, text in files.items():
                os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
                open(p, "wb" if isinstance(text, bytes) else "w").write(text)
            sh("git", "add", "-A")
            sh("git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", msg)
            return git("rev-parse", "HEAD").strip()
        X = "@pytest.mark.xfail(strict=True, reason=\"red\")\n"
        sh("git", "init", "-q", "-b", "main")
        commit("base", {"src/a.py": "A = 1\n", "tests/test_a.py": "def test_a():\n    assert A == 1\n"})
        sh("git", "checkout", "-qb", "story/x")
        red = commit("test: red", {"tests/test_a.py": "def test_a():\n    assert A == 1  # criterion 2\n", "tests/test_b.py":
                                   "@pytest.mark.xfail(strict=True, reason=\"red\")\ndef test_b():\n    assert B == 2\n",
                                   "tests/test_c.py": X + "def test_c():\n    with raises(E):\n        c()\n    assert S == 1\n"})
        commit("feat: b", {"src/b.py": "B = 2\n", "tests/test_b.py": "def test_b():\n    assert B == 2\n"})
        commit("feat: c", {"src/c.py": "S = 0\n", "tests/test_c.py": "def test_c():\n    with raises(E):\n        c()\n        assert S == 1\n"})
        commit("feat: weaken", {"src/a.py": "A = 3\n", "tests/test_a.py": "def test_a():\n    assert A == 3\n"})
        commit("test: fix test_a, agreed in #4", {"tests/test_a.py": "def test_a():\n    assert A in (1, 3)\n"})
        commit("refactor(signature): b() -> b(x)", {"src/b.py": "B = 2 \n", "tests/test_b.py": "def test_b():\n    assert B == 2 \n"})
        commit("test: tidy", {"tests/test_a.py": "def test_a():\n    assert A in (3, 1)\n"})
        open("tests/test_b.py", "a").write("# local\n")
        got = [": ".join(l.split(" ", 1)[1].split(": ")[:2]) for l in check("main", [red])]
    assert got == [
        "tests/test_a.py: changes existing",
        "tests/test_b.py: marker",
        "tests/test_c.py: refused (changed beside code)",
        "tests/test_a.py: refused (changed beside code)",
        "tests/test_a.py: own commit",
        "tests/test_b.py: signature",
        "tests/test_a.py: refused (message names no test in it)",
        "tests/test_b.py: refused (uncommitted)",
    ], got
    with tempfile.TemporaryDirectory() as d:  # red commits after the code, markers left at HEAD
        os.chdir(d)
        sh("git", "init", "-q", "-b", "main")
        old = "def test_old():\n    assert A == 1\n"
        gone = commit("base", {"src/a.py": "A = 1\n", "shop/tests.py": "def test_s():\n    assert A == 1\n", "t/a_test.go": "x\n",
                               "tests/test_old.py": old, "tests/fixtures/logo.png": b"\x89PNG\xdd"})
        sh("git", "checkout", "-qb", "story/y")
        red = commit("test: red", {"tests/test_d.py": X + "def test_d():\n    assert D == 4\n",
                                   "src/r.test.ts": "test.fails('r', () => expect(r()).toBe(2))\n"})
        commit("feat: r", {"src/r.ts": "r = () => 2\n", "src/r.test.ts": "test('r', () => expect(r()).toBe(2))\n"})
        commit("feat: logo", {"src/a.py": "A = 1 \n", "tests/fixtures/logo.png": b"\x89PNG\xee"})
        commit("feat: s", {"src/a.py": "A = 2\n", "shop/tests.py": "def test_s():\n    assert A == 2\n"})
        commit("feat: s back", {"src/a.py": "A = 1\n", "shop/tests.py": "def test_s():\n    assert A == 1\n"})
        commit("test: test_s expects 2, agreed in #7", {"shop/tests.py": "def test_s():\n    assert A == 2\n"})
        commit("test: loosen the tests", {"tests/test_old.py": "from tests import h\n" + old})
        commit("feat: hide", {"src/a.py": "A = 3\n", "tests/test_old.py": X + old})
        hold = commit("test: holdout", {"tests/test_d.py": X + "def test_d():\n    assert D\n", "tests/test_e.py": "x\n"})
        skip = commit("test: red 2", {"t/a_test.go": "t.Skip()\nx\n"})
        got = [": ".join(l.split(" ", 1)[1].split(": ")[:2]) for l in check("main", [red, hold, skip, gone])]
    assert got == [
        "(red commit): refused (not on the branch, such as after a rebase)",
        "src/r.test.ts: marker",
        "tests/fixtures/logo.png: refused (changed beside code)",
        "shop/tests.py: undone (changed beside code)",
        "shop/tests.py: undone (changed beside code)",
        "shop/tests.py: own commit",
        "tests/test_old.py: refused (message names no test in it)",
        "tests/test_old.py: refused (changed beside code)",
        "tests/test_d.py: refused (red commit changes a red test)",
        "t/a_test.go: changes existing",
        "tests/test_d.py: refused (still marked)",
    ], got
    with tempfile.TemporaryDirectory() as d:  # additions to locked files, and a new conftest
        os.chdir(d)
        sh("git", "init", "-q", "-b", "main")
        commit("base", {"src/a.py": "A = 5\n", "tests/test_a.py": "from a import A\nLIMIT = 5\n\ndef test_a():\n    assert A == LIMIT\n"})
        sh("git", "checkout", "-qb", "story/z")
        red = commit("test: red", {"tests/test_a.py": "from a import A\nLIMIT = 5\n\ndef test_a():\n    assert A == LIMIT\n\n"
                                   "def test_y():\n    assert A\n", "tests/test_r.py": X + "def test_r():\n    assert R\n",
                                   "tests/conftest.py": "import pytest\n"})
        red2 = commit("test: red 2", {"tests/test_r.py": X + "def test_r():\n    assert R\n\ndef test_z():\n    assert R\n"})
        bad = commit("test: red 3", {"tests/test_a.py": "from a import A\nLIMIT = 5\n\ndef test_a():\n    assert A == LIMIT\n\n"
                                     "def test_y():\n    assert A\nLIMIT: int = 1\n\ndef test_a():\n    pass\n"})
        early = commit("test: red 4", {"tests/test_r.py": X + "def test_r():\n    return\n    assert R\n\ndef test_z():\n    assert R\n"})
        auto = commit("test: red 5", {"tests/test_q.py": "import os.path\nQ = '''\nLIMIT = 5\n'''\n", "tests/fix.sql": "-- 5 rows\n"})
        ok = commit("test: red 6", {"tests/test_q.py": "import os.path\nimport os.sep\nQ = '''\nLIMIT = 5\n'''\nP = '''\nLIMIT = 9\n'''\n"
                                    "from a import (\n    B,\n)\n@pytest.fixture\ndef f():\n    pass\n", "tests/fix.sql": "-- 6 rows\n"})
        tup = commit("test: red 7", {"tests/test_q.py": "import os.path\nimport os.sep\nQ = '''\nLIMIT = 5\n'''\nP = '''\nLIMIT = 9\n'''\n"
                                     "from a import (\n    B,\n)\n@pytest.fixture\ndef f():\n    pass\n@pytest.fixture(autouse=True)\ndef g():\n    pass\n"})
        commit("feat: r", {"src/r.py": "R = 1\n", "tests/unit/conftest.py": "import pytest\n", "conftest.py": "import pytest\n"})
        got = [": ".join(l.split(" ", 1)[1].split(": ")[:2]) for l in check("main", [red, red2, bad, early, auto, ok, tup])]
    assert got == [
        "tests/test_a.py: adds to existing",
        "tests/test_r.py: adds to existing",
        "tests/test_a.py: refused (rebinds LIMIT, test_a)",
        "tests/test_r.py: refused (red commit changes a red test)",
        "tests/fix.sql: refused (red commit changes a red test)",
        "tests/test_q.py: adds to existing",
        "tests/test_q.py: refused (red commit changes a red test)",
        "conftest.py: refused (new conftest outside a red commit)",
        "tests/unit/conftest.py: refused (new conftest outside a red commit)",
        "tests/test_r.py: refused (still marked)",
    ], got
    print("locked_tests self-test passed")


if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test"]:
        self_test()
    elif len(sys.argv) >= 2:
        out = check(sys.argv[1], sys.argv[2:])
        print("\n".join(out))
        sys.exit(1 if any(": refused" in l for l in out) else 0)
    else:
        sys.exit(__doc__)
