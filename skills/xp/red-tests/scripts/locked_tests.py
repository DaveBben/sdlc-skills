#!/usr/bin/env python3
"""Usage: locked_tests.py <merge target> [<red commit>...] | --self-test

Run in the branch's worktree. Prints each change the branch makes to a locked test
file, a test file that existed where the branch left the merge target or one a red
commit holds, one line each:

  <commit> <file>: marker | signature | own commit | changes existing | refused (<why>): <subject>

  * marker:     the change only removes an expected-fail marker.
  * signature:  the commit's subject starts `refactor(signature):`.
  * own commit: the commit changes only test files and its message names this file
                or a test in it; a person's agreement must still be named in it.
  * changes existing: a red commit changes a line of a test file from before the branch.
  * refused:    any other change, an uncommitted one included; a red commit's change to
                another red commit's test; and a red test file holding more markers at HEAD
                than it held on the merge target (`HEAD <file>: refused (still marked)`); and a
                red commit not on the branch, such as after a rebase.
  * undone:     a refused change to a file whose content at a later commit is its locked one, with
                markers removed but none added.

Exits 1 when any line is refused, else 0. Prints nothing when no locked test changed.
"""
import os, re, subprocess, sys, tempfile

# shortcut: test files are found by path patterns; a test file named otherwise is not
# locked by this check, only by the rule the reviewer agent enforces.
TEST = re.compile(r"(^|/)(tests?|spec|specs|__tests__)/|(^|/)test_[^/]+\.py$|_test\.[^/]+$"
                  r"|(^|/)tests\.py$|\.(test|spec)\.[^/]+$|Tests?\.(java|kt|swift|cs)$|_spec\.rb$")
MARKER_LINE = re.compile(r"^(@pytest\.mark\.xfail\b.*|test\.fail\(\);?|pending(\(|\s+[\x27\"]|$).*"
                         r"|XCTExpectFailure\(.*\)|withKnownIssue\(.*\)\s*\{|\}\s*//\s*red)$")
FAILING = re.compile(r"\.fail(?:ing|s)\(")  # Jest test.failing(, Vitest test.fails(
# shortcut: an added line that skips a test; other insertions that defeat an existing test, such as
# an early return or a second test of the same name, pass here and rest on the reviewer's rule.
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
                d = git("show", "--format=", "-U0", c, "--", f)
                if f in lock and (re.search(r"^-(?!--)", d, re.M) or any(
                        SKIPS.search(l) and not MARKER_LINE.match(l[1:].strip())
                        for l in d.splitlines() if l[:1] == "+" and l[:3] != "+++")):
                    lines.append(f"{c[:10]} {f}: " + ("changes existing" if lock[f] == base else
                                                      "refused (red commit changes a red test)") + f": {subject}")
                    if lock[f] != base:
                        continue  # the earlier red version stays the locked one
                lock[f] = c
            continue
        message = git("log", "-1", "--format=%B", c)
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
