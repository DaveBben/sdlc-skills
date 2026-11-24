#!/usr/bin/env python3
"""The agentic-dev plugin's hooks. Reads one hook event as JSON on stdin; `--self-test` runs its tests.

  * Done check:      at Stop, runs the definition of done, as it was when the session began: the backticked
                     `Definition of done:` (or `Check:`) command of the root AGENTS.md, else the repository's own
                     test and lint commands, in the session's tree and in each other worktree of the repository
                     that changed during the turn, and blocks the stop on failure.
  * Size cap:        refuses an edit that leaves AGENTS.md or CLAUDE.md over 100 lines or 8 KB.
  * Dependency gate: an install command or manifest edit naming a package that no manifest or
                     lockfile in the repository holds asks the person (slopsquatting).
  * Pull request cap: opening a pull request or pushing a branch whose diff from the default branch
                     changes more than 400 lines asks the person.
  * Leftovers gate:  a commit that adds a debugger call, a TODO or commented-out code asks the person.
  * Silencer gate:   a commit that adds a line switching a type checker or linter off asks the person.
  * Test-tamper gate: a commit that changes or removes an assertion or a test in a test file the branch started
                     with, or adds a skip or expected-failure marker to a test, asks the person, once per line per branch.
                     It and the leftovers and silencer gates read only the files the commit takes in.
  * Grill gate:      the first file edit after the building skill loads asks the person when nothing since that load
                     asked them anything (no question tool call, no message from them): its grilling comes first.
  * Skill gate:      the first file edit in a repository in a session that loaded none of the building, prototyping
                     and reviewing skills, nor an xp-templates skill, asks the person, once per session.
  * Review gate:     opening a pull request, or merging a branch into the default branch, with more than RETRO_LINES
                     lines of code and no reviewing skill loaded in the session asks the person.
  * Retro reminder:  once per branch, after a pull request is opened from it or it is merged, tells the agent to
                     run the reflecting skill when the branch changed more than RETRO_LINES lines of code.
"""
import fnmatch, hashlib, json, os, re, shlex, subprocess, sys, tempfile

MAX_LINES, MAX_BYTES = 100, 8 * 1024  # this plugin's choice, sized for a root file of commands, constraints and traps
MAX_BLOCKS = 5  # this plugin's choice: failed checks in a row before the agent may stop anyway
CHECK_SECONDS = 300
DIFF_CAP = 400  # this plugin's choice: past about 400 changed lines a reviewer reads less of each line
INSTRUCTIONS = {"AGENTS.md", "CLAUDE.md"}
CHECK = re.compile(r"^\s*(?:[-*]\s+)?(?:\*\*)?(?:Definition of done|Check):(?:\*\*)?\s*`([^`\n]+)`", re.M | re.I)
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
PREFIX = r"^(?:\w+=\S*\s+|sudo\s+)*(?:\S*/)?"
INSTALL = re.compile(PREFIX + r"(?:(?:python[\d.]*\s+-m\s+|uv\s+)?pip[\d.]*\s+install|(?:uv|poetry|pdm|pnpm|yarn|bun|cargo|bundle)\s+add"
                     r"|(?:npm|pnpm|bun)\s+(?:install|i|add)|go\s+get|gem\s+install|uv\s+tool\s+install|pipx\s+install)\s+(.*)$")
# A runner fetches and executes its first argument at once.
RUNNER = re.compile(PREFIX + r"(?:npx|uvx|bunx|pipx\s+run|pnpm\s+dlx|npm\s+exec|uv\s+tool\s+run)\s+(.*)$")
PR = re.compile(PREFIX + r"(?:gh\s+pr\s+create|glab\s+mr\s+create|tea\s+(?:pr|pulls?)\s+create|git\s+push)\b")
MERGE = re.compile(PREFIX + r"git\s+(?:-C\s+\S+\s+)?merge\s+(.*)$")
COMMIT = re.compile(PREFIX + r"git\s+(?:-\S+\s+\S+\s+)*commit\b")
ADD = re.compile(PREFIX + r"git\s+(?:-\S+\s+\S+\s+)*add\b")
# shortcut: matched by pattern per added line; a print() left in, an unused import or a shim passes and rests on the reviewer.
LEFTOVER = re.compile(r"\bconsole\.(?:log|debug)\(|^\s*debugger;?\s*$|\bbreakpoint\(\)|\bi?pdb\.set_trace\(|binding\.pry|\bdbg!\("
                      r"|\b(?:TODO|FIXME|XXX)\b"
                      r"|^\s*(?:#|//)\s*(?:import\s|from\s+\S+\s+import\s|def\s|class\s|return\b|(?:const|let|var)\s"
                      r"|[\w.]+\s*=\s*[^=\s]|[\w.]+\(.*\)\s*;?\s*$)")
SILENCER = re.compile(r"#\s*type:\s*ignore|#\s*noqa|#\s*pyright:\s*ignore|#\s*pylint:\s*disable|eslint-disable"
                      r"|@ts-(?:ignore|nocheck|expect-error)|\bas\s+any\b|:\s*any\b|//\s*nolint|#\[allow\(|@SuppressWarnings")
TEST_FILE = re.compile(r"(?:^|/)(?:tests?|__tests__|spec)/|(?:^|/)test_[^/]*$|_test\.[^/.]+$|[._-](?:test|spec)\.[^/.]+$")
SKIP = re.compile(r"@pytest\.mark\.(?:skip|xfail)|\bpytest\.(?:skip|xfail)\(|@unittest\.(?:skip|expectedFailure)|\.skip\(|\bx(?:it|describe|test)\("
                  r"|\b(?:it|test)\.todo\(|\bt\.Skip(?:Now|f)?\(|#\[ignore\]|@(?:Disabled|Ignore)\b")
# shortcut: one line at a time, so an expected value inside a multi-line literal or a parametrize row passes.
TEST_DEF = re.compile(r"\bdef test|\b(?:it|test|describe)\(|\bfunc Test|#\[test\]|@Test\b")
ASSERTION = re.compile(r"\bassert|\bexpect\(|\.should\b|\braises\(|\bt\.(?:Error|Fatal|Fail)|" + TEST_DEF.pattern)
PROSE = (".md", ".txt", ".rst")
CONFIG = (".json", ".toml", ".yaml", ".yml", ".ini", ".cfg", ".conf", ".env", ".lock")
RETRO_LINES = 20  # this plugin's guess at "more than a couple of lines"; tune it
SHIP = re.compile(PREFIX + r"(?:gh\s+pr\s+create|glab\s+mr\s+create|tea\s+(?:pr|pulls?)\s+create)\b")
INSTALLERS = {"pip", "setuptools", "wheel"}
VALUE_FLAGS = {"-r", "-c", "-e", "-i", "-f", "-t", "-p", "--requirement", "--constraint", "--editable", "--index-url",
               "--extra-index-url", "--find-links", "--target", "--prefix", "--python", "--group", "--registry",
               "--features", "-F", "--package"}


def git(cwd, *args):
    while cwd and not os.path.isdir(cwd):  # a file about to be written in a new directory
        cwd = os.path.dirname(cwd.rstrip(os.sep))
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


def known_text(root):
    """Each dependency a tracked manifest declares, one per line, then the text of each tracked lockfile."""
    files = (git(root, "ls-files") or "").splitlines()
    declared = [m.group(1) for f in files if manifest_kind(f)
                for l in read(os.path.join(root, f)).splitlines() for m in [re.match(MANIFESTS[manifest_kind(f)], l)] if m]
    locks = [read(os.path.join(root, f)) for f in files if os.path.basename(f) in LOCKFILES]
    return "\n".join(declared + locks).lower()


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
        m, runner = INSTALL.match(part.strip()), RUNNER.match(part.strip())
        m = m or runner
        if not m:
            continue
        try:
            words = shlex.split(m.group(1))
        except ValueError:
            words = m.group(1).split()
        skip = False
        for w in words:
            if re.match(r"\d*[<>]", w):  # a redirection ends the arguments
                break
            if skip or w.startswith("-"):
                skip = not skip and w in VALUE_FLAGS
                continue
            if w.startswith((".", "/", "~")) or w.endswith((".txt", ".toml", ".whl", ".tgz")):
                continue
            name = re.split(r"[\[<>=!~;]", w, maxsplit=1)[0]
            names.append(name if "://" in name else re.sub(r"(?<=.)@[^/]*$", "", name))
            if runner:
                break
    return [n for n in names if n not in INSTALLERS]


def too_big(data):
    return data.count(b"\n") + (bool(data) and not data.endswith(b"\n")) > MAX_LINES or len(data) > MAX_BYTES


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
        if too_big(data) and len(data) > len(old.encode()):
            return deny(f"This change leaves {base} over {MAX_LINES} lines or {MAX_BYTES // 1024} KB. Rewrite it instead "
                        "of adding to it: delete lines a check enforces or the repository already shows.")
        was, now = CHECK.search(old), CHECK.search(new)
        if was and (not now or now.group(1) != was.group(1)):
            return ask(f"This edit changes the definition of done, the line that decides when work is done, from `{was.group(1)}` "
                       f"to `{now.group(1) if now else 'none'}`.")
    root = (git(os.path.dirname(path) or cwd, "rev-parse", "--show-toplevel") or "").strip()
    if not root:
        return None
    kind = manifest_kind(path)
    if kind:
        names = unknown(new_packages(kind, old, new), known_text(root))
        if names:
            return ask(f"First-seen dependency: {', '.join(names)} is in no manifest or lockfile of this repository. "
                       "Confirm each name exists on its registry and is the package you mean.")
    return None


# Text a person did not type, though it arrives as a user message.
NOT_THE_PERSON = ("<task-notification", "<system-reminder", "[Request interrupted", "Another Claude session")


def building_unasked(transcript):
    """The transcript line of the last building-skill load, when nothing since it asked the person anything."""
    try:
        lines = open(transcript).read().splitlines()
    except (OSError, TypeError):
        return None
    load, asked = None, False
    for n, line in enumerate(lines):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        content = (d.get("message") or {}).get("content") if isinstance(d, dict) else None
        blocks = content if isinstance(content, list) else [{"type": "text", "text": content}] if isinstance(content, str) else []
        blocks = [b for b in blocks if isinstance(b, dict)]
        if d.get("type") == "assistant":
            for b in blocks:
                if b.get("type") != "tool_use":
                    continue
                if b.get("name") == "Skill" and str((b.get("input") or {}).get("skill", "")).split(":")[-1] == "building":
                    load, asked = n, False
                elif b.get("name") == "AskUserQuestion" and load is not None:
                    asked = True
        elif d.get("type") == "user" and load is not None and not d.get("isMeta"):
            if any(b.get("type") == "text" and not str(b.get("text", "")).lstrip().startswith(NOT_THE_PERSON) for b in blocks):
                asked = True
    return load if load is not None and not asked else None


FRAMING_SKILLS = {"building", "prototyping", "reviewing",  # frame a change, run a throwaway experiment, fix findings
                  "story", "spike", "bug", "tracker", "design", "prd"}  # xp-templates: write an artifact


def skills_loaded(transcript):
    """The plugin skills this session's transcript shows loaded, or None when it cannot be read."""
    try:
        lines = open(transcript).read().splitlines()
    except (OSError, TypeError):
        return None
    names = set()
    for line in lines:
        try:
            d = json.loads(line)
        except ValueError:
            continue
        content = (d.get("message") or {}).get("content") if isinstance(d, dict) and d.get("type") == "assistant" else None
        for b in content if isinstance(content, list) else []:
            if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") == "Skill":
                names.add(str((b.get("input") or {}).get("skill", "")).split(":")[-1])
    return names


def skill_gate(inp, ti, cwd):
    path = os.path.join(cwd, ti.get("file_path", ""))
    where = os.path.dirname(path) if os.path.isdir(os.path.dirname(path)) else cwd
    root = (git(where, "rev-parse", "--show-toplevel") or "").strip()
    transcript = inp.get("transcript_path")
    loaded = skills_loaded(transcript) if root else None
    if loaded is None or loaded & FRAMING_SKILLS:
        return None
    state = load(root)
    if transcript in state.get("skill_asked", []):  # once per session, so an allowed edit is not asked again
        return None
    state.setdefault("skill_asked", []).append(transcript)
    save(root, state)
    return ask("This edit changes a file before the building skill framed the change. Allow to edit anyway, as for a "
               "written artifact such as a story or a bug report; deny to have the agent load the building skill first.")


def plan_gate(inp, ti, cwd):
    path = os.path.join(cwd, ti.get("file_path", ""))
    where = os.path.dirname(path) if os.path.isdir(os.path.dirname(path)) else cwd
    root = (git(where, "rev-parse", "--show-toplevel") or "").strip()
    transcript = inp.get("transcript_path")
    line = building_unasked(transcript) if root else None
    if line is None:
        return None
    state, key = load(root), f"{transcript}:{line}"
    if key in state.get("plan_asked", []):  # once per building load, so an allowed edit is not asked again
        return None
    state.setdefault("plan_asked", []).append(key)
    save(root, state)
    return ask("The building skill is about to edit a file without having asked you anything since it loaded. Its "
               "grilling comes first: what the request leaves open, and the one-way doors only you can decide. Allow "
               "to let it edit anyway; deny to have it ask you first.")


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


def merge_base(root):
    """The commit where the branch left the default branch, or None."""
    for ref in ("origin/HEAD", "origin/main", "origin/master", "main", "master"):
        base = (git(root, "merge-base", ref, "HEAD") or "").strip()
        if base:
            return base
    return None


def changed_lines(root):
    """Lines added plus removed in the tree since the branch left the default branch, lockfiles left out."""
    base = merge_base(root)
    if not base:
        return 0
    rows = (l.split("\t") for l in (git(root, "diff", "--numstat", base, "--") or "").splitlines())
    new = [f for f in (git(root, "ls-files", "-o", "--exclude-standard") or "").splitlines() if os.path.basename(f) not in LOCKFILES]
    return sum(int(r[0]) + int(r[1]) for r in rows if len(r) == 3 and r[0].isdigit() and r[1].isdigit()
               and os.path.basename(r[2]) not in LOCKFILES) + sum(read(os.path.join(root, f)).count("\n") for f in new)


def code_lines(root, spec):
    """Lines added plus removed by `git diff spec`, prose, config and lockfiles left out."""
    rows = (l.split("\t") for l in (git(root, "diff", "--numstat", spec, "--") or "").splitlines())
    return sum(int(r[0]) + int(r[1]) for r in rows if len(r) == 3 and r[0].isdigit() and r[1].isdigit()
               and not r[2].endswith(PROSE + CONFIG) and os.path.basename(r[2]) not in LOCKFILES)


def merge_ref(parts):
    """The branch the command's first `git merge` names, or None."""
    merges = [m.group(1) for part in parts for m in [MERGE.match(part)] if m]
    try:
        return next((a for a in shlex.split(merges[0], comments=True) if not a.startswith("-")), None) if merges else None
    except ValueError:
        return None


def unreviewed_lines(parts, root, transcript):
    """Lines of code the command ships when the session loaded no reviewing skill, else 0."""
    loaded = skills_loaded(transcript)
    if loaded is None or "reviewing" in loaded:
        return 0
    ref, base = merge_ref(parts), merge_base(root)
    # A merge of the default branch into a feature branch ships nothing, so only a merge into it counts.
    if ref and (git(root, "rev-parse", "--abbrev-ref", "HEAD") or "").strip() in ("main", "master"):
        return code_lines(root, f"HEAD...{ref}")
    return code_lines(root, base) if base and any(SHIP.match(part) for part in parts) else 0


def retro_due(command, root):
    """Once per branch: after a pull request from it or a merge of it, the change it holds is finished."""
    parts = [part.strip() for part in re.split(r"&&|\|\||[;|\n]", command)]
    ref = merge_ref(parts)
    if ref:  # the merge has run, so ORIG_HEAD is where it started
        branch, n = ref, code_lines(root, f"ORIG_HEAD...{ref}")
    elif any(SHIP.match(part) for part in parts) and merge_base(root):
        branch, n = (git(root, "rev-parse", "--abbrev-ref", "HEAD") or "").strip(), code_lines(root, merge_base(root))
    else:
        return None
    state = load(root)
    if n <= RETRO_LINES or branch in state.get("retro", []):
        return None
    state.setdefault("retro", []).append(branch)
    save(root, state)
    return (f"This change touched {n} lines of code. Run the reflecting skill now, before you tell the person it is done; "
            "if it is not finished, run it when it is.")


def added_lines(root):
    """(path, line number, text) for each line the tree adds since HEAD, untracked files included, prose and lockfiles left out."""
    out, path, n = [], None, 0
    for l in (git(root, "diff", "HEAD", "-U0", "--no-color", "--no-ext-diff") or "").splitlines():
        if l.startswith("+++ "):
            path = l[6:] if l.startswith("+++ b/") else None
        elif l.startswith("@@"):
            n = int(re.search(r"\+(\d+)", l).group(1))
        elif l.startswith("+") and path:
            out.append((path, n, l[1:])); n += 1
    for f in (git(root, "ls-files", "-o", "--exclude-standard") or "").splitlines():
        out += [(f, i, t) for i, t in enumerate(read(os.path.join(root, f)).splitlines(), 1)]
    return [r for r in out if not r[0].endswith(PROSE) and os.path.basename(r[0]) not in LOCKFILES]


def removed_test_lines(root):
    """(path, old line number, text) for each line the tree changes or removes since HEAD in a test file the branch started with."""
    base = merge_base(root) or "HEAD"
    old = {f for f in (git(root, "ls-tree", "-r", "--name-only", base) or "").splitlines() if TEST_FILE.search(f)}
    out, path, n = [], None, 0
    for l in (git(root, "diff", "HEAD", "-U0", "--no-color", "--no-ext-diff", "--", *sorted(old)) or "").splitlines() if old else []:
        if l.startswith("--- "):
            path = l[6:] if l.startswith("--- a/") else None
        elif l.startswith("@@"):
            n = int(re.search(r"-(\d+)", l).group(1))
        elif l.startswith("-") and path:
            out.append((path, n, l[1:])); n += 1
    return [r for r in out if r[2].strip()]


def commit_paths(root, parts):
    """The changed paths the commit in these command parts takes in, or None for every one."""
    # shortcut: paths are matched from the repository root, so `cd sub && git add f` misses f; parse cwd if it bites.
    def words(match):
        out = []
        for part in parts:
            if match.match(part):
                try:
                    out += shlex.split(part)
                except ValueError:
                    out += part.split()
        return out
    added, committed = words(ADD), words(COMMIT)
    if (any(w in ("--all", "--update", ".", "*") or w.startswith(":") or re.match(r"-[^-]*[Au]", w) for w in added)
            or any(w == "--all" or re.match(r"-[^-]*a", w) for w in committed)):
        return None
    names = [w.rstrip("/") for w in added + committed if not w.startswith("-")]
    changed = set((git(root, "diff", "HEAD", "--name-only") or "").splitlines() +
                  (git(root, "ls-files", "-o", "--exclude-standard") or "").splitlines())
    staged = set((git(root, "diff", "--cached", "--name-only") or "").splitlines())
    return staged | {f for f in changed if any(f == n or f.startswith(n + "/") or fnmatch.fnmatch(f, n) for n in names)}


def commit_gates(root, parts):
    paths = commit_paths(root, parts)
    rows = [r for r in added_lines(root) if paths is None or r[0] in paths]
    show = lambda hits: "; ".join(f"{p}:{n} `{t.strip()[:60]}`" for p, n, t in hits[:5])
    left, quiet = [r for r in rows if LEFTOVER.search(r[2])], [r for r in rows if SILENCER.search(r[2])]
    reasons = []
    if left:
        reasons.append(f"Leftovers in this commit: {show(left)}. Remove each debugger call, TODO and commented-out line; "
                       "approve only when one is meant to stay.")
    if quiet:
        reasons.append(f"This commit switches a checker off: {show(quiet)}. Fix the type or lint finding instead; "
                       "approve only when it cannot be fixed.")
    # Each line is keyed with the test it sits in, so two tests' identical `assert r.ok` lines stay apart.
    head = lambda f: (git(root, "show", f"HEAD:{f}") or "").splitlines()
    tree = lambda f: read(os.path.join(root, f)).splitlines()
    test_of = lambda lines, n, up: next((l.strip() for l in (reversed(lines[:n]) if up else lines[n - 1:]) if TEST_DEF.search(l)), "")
    tampered = [(r, test_of(head(r[0]), r[1], True)) for r in removed_test_lines(root)
                if (paths is None or r[0] in paths) and ASSERTION.search(r[2])]
    tampered += [(r, test_of(tree(r[0]), r[1], False)) for r in rows if TEST_FILE.search(r[0]) and SKIP.search(r[2])]
    # Ask about each line once per branch, so a retried or split commit does not ask again.
    branch, state = (git(root, "rev-parse", "--abbrev-ref", "HEAD") or "").strip(), load(root)
    key = lambda r, test: hashlib.sha256(f"{branch}\0{r[0]}\0{test}\0{r[2].strip()}".encode()).hexdigest()[:16]
    seen = set(state.get("tamper", []))
    tampered = [(r, test) for r, test in tampered if key(r, test) not in seen]
    if tampered:
        state["tamper"] = sorted(seen | {key(r, test) for r, test in tampered})
        save(root, state)
        tampered = [r for r, _ in tampered]
        reasons.append(f"This commit changes, removes or skips tests the branch started with: {show(tampered)}. Make the code "
                       "pass the test as it was; approve only when the test itself is wrong, with the reason in the commit message.")
    return reasons


def pre_bash(command, root, transcript=None):
    reasons = []
    names = unknown(installs(command), known_text(root))
    if names:
        reasons.append(f"First-seen dependency: {', '.join(names)} is in no manifest or lockfile of this repository. "
                       "Confirm each name exists on its registry and is the package you mean.")
    parts = [part.strip() for part in re.split(r"&&|\|\||[;|\n]", command)]
    if any(COMMIT.match(part) for part in parts):
        reasons += commit_gates(root, parts)
    if any(PR.match(part) for part in parts):
        n = changed_lines(root)
        if n > DIFF_CAP:
            reasons.append(f"This branch changes {n} lines, over the {DIFF_CAP}-line cap for one pull request. "
                           "Approve only when it cannot be split.")
    n = unreviewed_lines(parts, root, transcript)
    if n > RETRO_LINES:
        reasons.append(f"This ships {n} lines of code that the reviewing skill has not reviewed in this session. "
                       "Approve only when it was reviewed elsewhere; deny to have the agent load the reviewing skill first.")
    return ask(" ".join(reasons)) if reasons else None


def post_bash(command, root):
    big = [n for n in INSTRUCTIONS if n in command and too_big(read(os.path.join(root, n)).encode())]
    if big:
        return {"decision": "block", "reason": f"{', '.join(big)} is now over {MAX_LINES} lines or {MAX_BYTES // 1024} KB. "
                "Rewrite it shorter: delete lines a check enforces or the repository already shows."}
    due = retro_due(command, root)
    return {"decision": "block", "reason": due} if due else None


def check_command(root):
    """The definition of done: the AGENTS.md line, else the repository's own test and lint commands."""
    m = CHECK.search(read(os.path.join(root, "AGENTS.md")) or read(os.path.join(root, "CLAUDE.md")))
    return m.group(1).strip() if m else " && ".join(c for c in (test_command(root), lint_command(root)) if c) or None


def runner(root):
    has = lambda f: os.path.exists(os.path.join(root, f))
    return next((pm for pm, lock in (("pnpm", "pnpm-lock.yaml"), ("yarn", "yarn.lock"), ("bun", "bun.lockb")) if has(lock)), "npm")


def lint_command(root):
    """The repository's own lint command, for a repository whose AGENTS.md names no definition of done."""
    has = lambda f: os.path.exists(os.path.join(root, f))
    try:
        script = json.loads(read(os.path.join(root, "package.json")) or "{}").get("scripts", {}).get("lint", "")
    except (ValueError, AttributeError):
        script = ""
    if script:
        return f"{runner(root)} run lint"
    if re.search(r"^lint\s*:", read(os.path.join(root, "Makefile")), re.M):
        return "make lint"
    if has("go.mod"):
        return "go vet ./..."
    if has("ruff.toml") or has(".ruff.toml") or "[tool.ruff" in read(os.path.join(root, "pyproject.toml")):
        return "uv run ruff check ." if has("uv.lock") else "ruff check ."
    return None


def test_command(root):
    """The repository's own test command, for a repository whose AGENTS.md names none."""
    has = lambda f: os.path.exists(os.path.join(root, f))
    try:
        script = json.loads(read(os.path.join(root, "package.json")) or "{}").get("scripts", {}).get("test", "")
    except (ValueError, AttributeError):
        script = ""
    if script and "no test specified" not in script:  # npm init's placeholder only fails
        return f"{runner(root)} test"
    if re.search(r"^test\s*:", read(os.path.join(root, "Makefile")), re.M):
        return "make test"
    if has("Cargo.toml"):
        return "cargo test"
    if has("go.mod"):
        return "go test ./..."
    if has("pytest.ini") or has("conftest.py") or "pytest" in read(os.path.join(root, "pyproject.toml")):
        return "uv run pytest" if has("uv.lock") else ".venv/bin/python -m pytest" if has(".venv/bin/python") else "python3 -m pytest"
    return None


def trees(root):
    """The session's tree, then each other worktree of its repository, such as one a build works in."""
    paths = [os.path.realpath(root)]
    for block in (git(root, "worktree", "list", "--porcelain") or "").split("\n\n"):
        lines = block.splitlines()
        if lines and lines[0].startswith("worktree ") and not {"bare", "prunable"} & {l.split()[0] for l in lines[1:]}:
            p = os.path.realpath(lines[0][len("worktree "):])
            if p not in paths and os.path.isdir(p):
                paths.append(p)
    return paths


def start(root):
    old = load(root)
    save(root, {"retro": old.get("retro", []), "tamper": old.get("tamper", []), "check": check_command(root), "trees": {p: {"baseline": fingerprint(p)} for p in trees(root)}})


def new_turn(root):  # a tree only the person changed this turn runs no check
    state = load(root)
    for p in trees(root):
        state.setdefault("trees", {}).setdefault(p, {})["turn"] = fingerprint(p)
    save(root, state)


def stop(root):
    state = load(root)
    outs = [o for p in trees(root) for o in [stop_tree(p, state, state.setdefault("trees", {}).setdefault(p, {}))] if o]
    save(root, state)
    blocks = [o for o in outs if "decision" in o]
    return blocks[0] if blocks else outs and {"systemMessage": " ".join(o["systemMessage"] for o in outs)} or None


def stop_tree(path, state, t):
    fp = fingerprint(path)
    if fp in (t.get("baseline"), t.get("passed"), t.get("turn")):
        return None
    cmd, where = check_command(path), f" in {path}"
    if "check" in state and cmd != state["check"]:
        # The session cannot choose its own check: only the command from the session's start runs.
        if fp == t.get("failed"):
            return None
        t["failed"] = fp
        return {"systemMessage": f"agentic-dev: the definition of done{where} is `{cmd}`, not `{state['check']}` as when the "
                "session began, so the done check did not run there. A new session uses the new line."}
    if not cmd:
        return None
    if fp == t.get("failed"):
        return {"systemMessage": f"agentic-dev: `{cmd}` still fails{where}, and nothing changed since it last ran."}
    try:
        r = subprocess.run(cmd, shell=True, cwd=path, capture_output=True, text=True, errors="replace", timeout=CHECK_SECONDS)
        ok, out = r.returncode == 0, (r.stdout + r.stderr)
    except subprocess.TimeoutExpired:
        ok, out = False, f"timed out after {CHECK_SECONDS} s. Name a faster one in a `Definition of done:` line in AGENTS.md."
    fp = fingerprint(path)  # the check may write files
    if ok:
        t.update(passed=fp, blocks=0)
        return None
    t.update(failed=fp, blocks=t.get("blocks", 0) + 1)
    if t["blocks"] >= MAX_BLOCKS:
        return {"systemMessage": f"agentic-dev: `{cmd}` failed {t['blocks']} times in a row{where}. The work is not done."}
    return {"decision": "block", "reason":
            f"The work is not done: `{cmd}` fails{where}.\n" + "\n".join(out.splitlines()[-40:]) +
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
        out = pre_edit(tool, ti, cwd) or skill_gate(inp, ti, cwd) or plan_gate(inp, ti, cwd)
    elif not root:
        return
    elif event == "PreToolUse" and tool == "Bash":
        out = pre_bash(ti.get("command", ""), root, inp.get("transcript_path"))
    elif event == "PostToolUse" and tool == "Bash":
        out = post_bash(ti.get("command", ""), root)
    elif event == "SessionStart":
        if inp.get("source") in (None, "startup", "clear"):
            start(root)
    elif event == "UserPromptSubmit":
        new_turn(root)
    elif event == "Stop":
        out = stop(root)
    if out:
        print(json.dumps(out))


TEST_A = "ROWS = [1, 2]\n\n\ndef test_a():\n    assert f(2) == 4\n\n\ndef test_b():\n    assert f(3) == 6\n"


def self_test():
    t = os.path.realpath(tempfile.mkdtemp())
    run = lambda *a: subprocess.run(a, cwd=t, check=True, capture_output=True)
    put = lambda name, text: (os.makedirs(os.path.dirname(os.path.join(t, name)) or t, exist_ok=True),
                              open(os.path.join(t, name), "w").write(text))
    run("git", "init", "-q")
    run("git", "config", "user.email", "t@t"); run("git", "config", "user.name", "t")
    put("tests/test_a.py", TEST_A)
    put("pyproject.toml", '[project]\ndependencies = [\n    "httpx>=0.27",\n]\n')
    put("package.json", '{\n  "scripts": {"test": "vitest"},\n  "dependencies": {\n    "react": "^19.0.0"\n  }\n}\n')
    put("AGENTS.md", "Check: `python3 -c \"import sys; sys.exit(open('flag').read() != 'ok')\"`\n")
    put("flag", "ok")
    run("git", "add", "-A"); run("git", "commit", "-qm", "base")
    decision = lambda o: o and o["hookSpecificOutput"]["permissionDecision"]

    # Size cap and the Check: line
    full = "line\n" * MAX_LINES
    w = lambda content, f="AGENTS.md": pre_edit("Write", {"file_path": os.path.join(t, f), "content": content}, t)
    assert not w(full, "CLAUDE.md") and decision(w(full + "x\n", "CLAUDE.md")) == "deny", "the cap is 100 lines"
    assert not w(full * 2, "README.md"), "other files pass"
    assert decision(w("Check: `true`\n")) == "ask", "weakening the check asks"
    assert not w(read(os.path.join(t, "AGENTS.md")) + "Trap: x\n"), "another line passes"
    assert CHECK.search("* **Check:** `make test` runs lint too").group(1) == "make test"
    assert not CHECK.search("Full check: `x`") and not CHECK.search("- Check: that migrations are reversible")
    open(os.path.join(t, "CLAUDE.md"), "w").write(full * 2)
    assert post_bash("cat x >> CLAUDE.md", t), "a shell write past the cap is reported"
    os.remove(os.path.join(t, "CLAUDE.md"))

    # Dependency gate
    assert installs("pip install -r requirements.txt 'httpx[http2]>=0.27' -e . && npm i -D @types/node@20 left-pad") \
        == ["httpx", "@types/node", "left-pad"]
    assert installs("uv add --dev pytest; go get github.com/a/b@v1; echo pip install x") == ["pytest", "github.com/a/b"]
    assert decision(pre_bash("uv add reqeusts", t)) == "ask" and not pre_bash("pip install httpx", t)
    assert not pre_bash("npm install", t) and not pre_bash("npm i react@19", t)
    assert decision(pre_bash("npm i test", t)) == "ask", "a script's name is not a dependency"
    assert installs("FOO=1 sudo .venv/bin/pip install --upgrade pip x 2>&1 | tail") == ["x"]
    assert installs("npx create-thing@latest my-app; cargo add serde --features derive; pnpm i zod") == ["create-thing", "serde", "zod"]
    p = lambda old, new, f: pre_edit("Edit", {"file_path": f, "old_string": old, "new_string": new}, t)
    assert decision(p('"httpx>=0.27",', '"httpx>=0.27",\n    "reqeusts",', "pyproject.toml")) == "ask"
    assert not p('"httpx>=0.27",', '"httpx>=0.28",', "pyproject.toml"), "a version bump passes"
    assert not p("[project]", "[project]\nname = \"x\"", "pyproject.toml"), "a setting passes"
    assert decision(p('"react": "^19.0.0"', '"react": "^19.0.0",\n    "left-pad": "^1.3.0"', "package.json")) == "ask"
    assert not p('"test": "vitest"', '"test": "vitest", "lint": "eslint ."', "package.json"), "a script passes"

    # Pull request cap
    run("git", "branch", "-q", "main") if not git(t, "rev-parse", "--verify", "-q", "main") else None
    n0 = changed_lines(t)  # untracked files from the tests above
    run("git", "checkout", "-qb", "big")
    put("big.py", "x = 1\n" * (DIFF_CAP + 1)); put("uv.lock", "y\n" * 900)
    run("git", "add", "big.py", "uv.lock"); run("git", "commit", "-qm", "big")
    assert changed_lines(t) == n0 + DIFF_CAP + 1, "lockfiles do not count"
    assert decision(pre_bash("git add -A && gh pr create --fill", t)) == "ask"
    assert "reqeusts" in pre_bash("pip install reqeusts && git push", t)["hookSpecificOutput"]["permissionDecisionReason"]
    put("more.py", "y = 2\n" * 10)
    assert changed_lines(t) == n0 + DIFF_CAP + 11, "lines not yet committed count"
    os.remove(os.path.join(t, "more.py"))
    assert not pre_bash("git status", t), "other commands pass"
    run("git", "checkout", "-q", "-"); run("git", "branch", "-qD", "big")
    assert not pre_bash("git push", t), "a small diff passes"

    # Leftovers and silencer gates
    put("src/app.py", "def f(x):\n    breakpoint()\n    # return x + 1\n    return x  # TODO: real rule\n")
    r = pre_bash("git add -A && git commit -qm f", t)["hookSpecificOutput"]["permissionDecisionReason"]
    assert "src/app.py:2" in r and "src/app.py:3" in r and "src/app.py:4" in r and "switches" not in r
    put("src/app.py", "def f(x):  # type: ignore\n    return x\n")
    assert "switches a checker off" in pre_bash("git commit -qam f", t)["hookSpecificOutput"]["permissionDecisionReason"]
    put("src/app.py", "def f(x):\n    # The tax office rounds half down, so round() is wrong here.\n    return x\n")
    put("NOTES.md", "TODO: later\n")
    assert not pre_bash("git commit -qam f", t), "a why comment and prose pass"
    assert not pre_bash("git status", t), "only a commit is checked"
    assert added_lines(t) and all(not p.endswith(".md") for p, _, _ in added_lines(t))
    os.remove(os.path.join(t, "src/app.py")); os.remove(os.path.join(t, "NOTES.md"))

    # Test-tamper gate
    tamper = lambda c="git commit -qam t": (pre_bash(c, t) or {}).get("hookSpecificOutput", {}).get("permissionDecisionReason", "")
    put("tests/test_a.py", TEST_A.replace("[1, 2]", "[1, 3]"))
    assert "changes, removes or skips" not in tamper(), "changing a fixture passes"
    put("tests/test_a.py", TEST_A.replace("f(3) == 6", "f(3) == 7"))
    assert "changes, removes or skips" not in tamper("git commit -qm t"), "a commit that leaves the test out passes"
    assert "tests/test_a.py:9" in tamper("git add tests/test_a.py && git commit -qm t"), "changing an assertion asks"
    assert "changes, removes or skips" not in tamper("git add tests/test_a.py && git commit -qm t"), "a line asked about is not asked again"
    put("tests/test_a.py", TEST_A.replace("f(2) == 4", "f(2) == 5"))
    run("git", "add", "tests/test_a.py")
    assert "tests/test_a.py:5" in tamper("git commit -qm t"), "a staged change asks"
    run("git", "reset", "-q")
    put("tests/test_a.py", "ROWS = [1, 2]\n")
    assert "tests/test_a.py:4" in tamper(), "deleting a test asks"
    run("git", "checkout", "-q", "--", "tests/test_a.py")
    put("tests/test_a.py", TEST_A.replace("f(2) == 4", "f(2) == 8"))
    start(t)
    assert "changes, removes or skips" not in tamper(), "a new session on the branch does not ask again"
    same = TEST_A.replace("f(2) == 4", "r.ok").replace("f(3) == 6", "r.ok")
    put("tests/test_a.py", same); run("git", "commit", "-qam", "same text")
    put("tests/test_a.py", same.replace("r.ok", "r", 1))
    assert "tests/test_a.py:5" in tamper(); run("git", "commit", "-qam", "first")
    put("tests/test_a.py", same.replace("r.ok", "r"))
    assert "tests/test_a.py:9" in tamper(), "a second assertion with the same text asks"
    run("git", "reset", "-q", "--hard", "HEAD~2")
    for c in ("git add tests/*.py && git commit -qm t", "git add '*.py' && git commit -qm t", "git add -fA && git commit -qm t",
              "git add :/ && git commit -qm t", "git add -u && git commit -qm t"):
        save(t, {**load(t), "tamper": []})
        put("tests/test_a.py", TEST_A.replace("f(2) == 4", "f(2) == 9"))
        assert "tests/test_a.py:5" in tamper(c), f"{c} takes the test in"
    run("git", "checkout", "-q", "--", "tests/test_a.py")
    put("tests/test_new.py", "def test_b():\n    assert True\n")
    assert "changes, removes or skips" not in tamper(), "a new test passes"
    put("tests/test_new.py", "import pytest\n\n@pytest.mark.skip\ndef test_b():\n    assert True\n")
    assert "tests/test_new.py:3" in tamper(), "a skip marker asks"
    put("tests/test_a.py", TEST_A + "\n\ndef test_c():\n    assert f(0) == 0\n")
    os.remove(os.path.join(t, "tests/test_new.py"))
    assert "changes, removes or skips" not in tamper(), "adding to a test file passes"
    assert SKIP.search("  xit('x', () => {})") and SKIP.search("    t.Skip(\"later\")") and not SKIP.search("def skip_rows():")
    run("git", "checkout", "-q", "--", "tests/test_a.py")

    # Grill gate
    tr = os.path.join(t, "transcript.jsonl")
    msg = lambda kind, content, **kw: json.dumps({"type": kind, "message": {"content": content}, **kw})
    use = lambda name, **i: msg("assistant", [{"type": "tool_use", "name": name, "input": i}])
    gate = lambda lines: (open(tr, "w").write("\n".join(lines) + "\n"),
                          plan_gate({"transcript_path": tr}, {"file_path": os.path.join(t, "src.py")}, t))[1]
    begin = [msg("user", "Add a CSV export."), use("Skill", skill="agentic-dev:reflecting")]
    loaded = begin + [use("Skill", skill="agentic-dev:building"),
                      msg("user", [{"type": "text", "text": "Base directory for this skill: x"}], isMeta=True),
                      msg("user", "<task-notification>done</task-notification>")]
    assert not gate(begin), "no building load passes"
    assert decision(gate(loaded)) == "ask", "an edit before any question asks"
    assert not gate(loaded), "the same building load is asked once"
    assert not gate(loaded + [use("AskUserQuestion", questions=[])]), "a question tool call passes"
    assert not gate(loaded + [msg("user", "Store it in the warehouse.")]), "a message from the person passes"
    assert decision(gate(loaded + [msg("user", "ok"), use("Skill", skill="building")])) == "ask", "a new building load asks again"
    assert not plan_gate({"transcript_path": tr}, {"file_path": "/tmp/x.py"}, "/tmp"), "outside a repository passes"
    os.remove(tr)

    # Skill gate
    def sg(lines, name):
        path = os.path.join(t, name + ".jsonl")
        open(path, "w").write("\n".join(lines) + "\n")
        return skill_gate({"transcript_path": path}, {"file_path": os.path.join(t, "notes.md")}, t)
    bare = [msg("user", "Add a note to AGENTS.md that we merge straight to main.")]
    assert decision(sg(bare, "s1")) == "ask", "an edit no skill framed asks"
    assert not sg(bare, "s1"), "the same session is asked once"
    assert not sg(bare + [use("Skill", skill="agentic-dev:building")], "s2"), "an edit after the building skill passes"
    assert not sg(bare + [use("Skill", skill="reflecting"), use("Skill", skill="reviewing")], "s3"), "after the reviewing skill passes"
    assert not sg(bare + [use("Skill", skill="agentic-dev:prototyping")], "s6"), "an edit after the prototyping skill passes"
    assert decision(sg(bare + [use("Skill", skill="agentic-dev:reflecting")], "s4")) == "ask", "reflecting frames no change"
    assert decision(sg(bare + [use("Skill", skill="other-plugin:deploy")], "s5")) == "ask", "another plugin's skill frames no change"
    assert not sg(bare + [use("Skill", skill="xp-templates:story")], "s7"), "an edit after an xp-templates skill passes"
    assert not sg(bare + [use("Skill", skill="xp-templates:design")], "s8"), "an edit after the design skill passes"
    assert not sg(bare + [use("Skill", skill="xp-templates:prd")], "s9"), "an edit after the prd skill passes"
    assert not sg(bare + [use("Skill", skill="xp-templates:discovery")], "s10"), "an edit after the discovery skill passes"
    assert not skill_gate({"transcript_path": os.path.join(t, "s1.jsonl")}, {"file_path": "/tmp/x.md"}, "/tmp"), \
        "outside a repository passes"
    for n in ("s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10"):
        os.remove(os.path.join(t, n + ".jsonl"))

    # Retro reminder
    run("git", "checkout", "-qb", "feat/r")
    put("r.py", "x = 1\n" * (RETRO_LINES + 1)); put("r.json", "{}\n" * 50); put("R.md", "y\n" * 50)
    run("git", "add", "r.py", "r.json", "R.md"); run("git", "commit", "-qm", "r")
    assert not post_bash("git push", t), "a push is not a finished change"
    # Review gate
    rv = os.path.join(tempfile.mkdtemp(), "review.jsonl")
    ship = lambda cmd, *lines: (open(rv, "w").write("\n".join(lines) + "\n"), pre_bash(cmd, t, rv))[1]
    built = use("Skill", skill="agentic-dev:building")
    assert "not reviewed" in ship("gh pr create --fill", built)["hookSpecificOutput"]["permissionDecisionReason"], \
        "a pull request no review preceded asks"
    assert not ship("gh pr create --fill", built, use("Skill", skill="agentic-dev:reviewing")), "after the reviewing skill it passes"
    assert not ship("git push", built), "a push ships nothing"
    assert not ship("git merge main", built), "merging the default branch into a feature branch passes"
    assert not pre_bash("gh pr create --fill", t), "an unreadable transcript passes"
    assert str(RETRO_LINES + 1) in post_bash("gh pr create --fill", t)["reason"], "config and prose do not count"
    assert not post_bash("gh pr create --fill", t), "once per branch"
    start(t)
    assert not post_bash("gh pr create --fill", t), "a new session remembers it"
    run("git", "checkout", "-qb", "feat/s", "main"); put("s.json", "{}\n" * 50)
    run("git", "add", "s.json"); run("git", "commit", "-qm", "s")
    assert not post_bash("gh pr create", t), "a config-only change is trivial"
    run("git", "checkout", "-qb", "feat/u", "main"); put("u.py", "x = 1\n" * (RETRO_LINES + 5))
    run("git", "add", "u.py"); run("git", "commit", "-qm", "u"); run("git", "checkout", "-q", "main")
    assert decision(ship("git merge --no-ff feat/u", built)) == "ask", "merging an unreviewed branch into the default branch asks"
    assert not ship("git merge --no-ff feat/s", built), "a config-only branch is trivial"
    run("git", "merge", "-q", "--no-ff", "-m", "m", "feat/u")
    assert "reflecting skill" in post_bash("git merge --no-ff feat/u", t)["reason"], "a merge of a big branch reminds"
    run("git", "reset", "-q", "--hard", "HEAD~1")
    run("git", "branch", "-qD", "feat/r", "feat/s", "feat/u")
    for f in ("r.py", "r.json", "R.md"):
        os.path.exists(os.path.join(t, f)) and os.remove(os.path.join(t, f))

    # Done check
    start(t)
    assert stop(t) is None, "an unchanged tree runs no check"
    put("flag", "no")
    assert stop(t)["decision"] == "block", "a failing check blocks the stop"
    assert "systemMessage" in stop(t), "stopping again with nothing changed is allowed, and the person is told"
    put("flag", "ok"); put("fix.py", "x = 1\n")
    assert stop(t) is None and load(t)["trees"][t]["blocks"] == 0, "a passing check lets it stop"
    for i in range(MAX_BLOCKS):
        put("flag", "no" + str(i))
        last = stop(t)
    assert "systemMessage" in last, "at the 5th failure in a row it may stop, and the person is told"
    new_turn(t)
    assert stop(t) is None, "a tree unchanged since the turn began runs no check"
    wt = t + "-wt"
    run("git", "worktree", "add", "-qb", "wt", wt)
    assert stop(t) is None, "a worktree made during the session whose check passes lets it stop"
    open(os.path.join(wt, "flag"), "w").write("no")
    r = stop(t)
    assert r["decision"] == "block" and wt in r["reason"], "a failing check in another worktree blocks the stop"
    run("git", "worktree", "remove", "--force", wt)
    assert stop(t) is None, "a removed worktree is not checked"
    put("AGENTS.md", "Check: `true`\n")
    assert "as when the session began" in stop(t)["systemMessage"], "a check the session rewrote does not run"
    # The repository's own test command, when AGENTS.md names none
    d = tempfile.mkdtemp()
    tc = lambda **files: ([open(os.path.join(d, f), "w").write(x) for f, x in files.items()], test_command(d))[1]
    assert tc() is None, "a repository with no test command runs nothing"
    assert tc(**{"pyproject.toml": "[tool.pytest.ini_options]\n"}) == "python3 -m pytest"
    assert tc(**{"uv.lock": ""}) == "uv run pytest"
    assert tc(**{"go.mod": "module x\n"}) == "go test ./...", "go comes before pytest"
    assert tc(**{"Makefile": "lint:\n\truff .\ntest: lint\n\tpytest\n"}) == "make test"
    assert tc(**{"package.json": '{"scripts": {"test": "echo \\"Error: no test specified\\" && exit 1"}}'}) == "make test"
    assert tc(**{"package.json": '{"scripts": {"test": "vitest"}}', "pnpm-lock.yaml": ""}) == "pnpm test"
    assert lint_command(d) == "make lint" and check_command(d) == "pnpm test && make lint", "done is tests and lint"
    open(os.path.join(d, "package.json"), "w").write('{"scripts": {"test": "vitest", "lint": "eslint ."}}')
    assert lint_command(d) == "pnpm run lint"
    open(os.path.join(d, "AGENTS.md"), "w").write("- **Definition of done:** `make ci`\n")
    assert check_command(d) == "make ci", "the AGENTS.md line wins"
    print("self-test passed")


if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test"]:
        self_test()
    else:
        main()
