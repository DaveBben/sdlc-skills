#!/usr/bin/env python3
"""Usage: reading_floor.py <diff.patch> [<AGENTS.md>...] | --self-test

Prints each hunk of a unified diff that a person must read, whatever the change's
author sorts it as: one `<file>:<start>-<end>: floor: <reasons>` line per hunk.
A hunk is printed when its file is under a path on the `Sensitive:` line of any AGENTS.md given,
its path names authentication, a token or session, a secret, permissions, a schema or a migration, its file configures the
system (config, settings, deploy and infrastructure files) or the tests or the checks (a fixture file that existed before, test config, `check`, CI, hooks, AGENTS.md), a line it adds
suppresses a check (`nosemgrep`, `noqa`, `eslint-disable`), or a line it adds or
removes in a file that is neither prose nor a test handles an error, other than a Go
`if err != nil` whose next line, also added, returns the error. Line numbers are the new file's, or the old one's for a
deleted file. Prints nothing when no hunk qualifies.
"""
import fnmatch, os, re, sys, tempfile

# shortcut: keyword and path patterns, not a parser; a hunk they miss still reaches the
# reviewer's own sort, which may add hunks but never drop these.
ERROR = re.compile(r"\b(except|catch|rescue|recover|finally|retry|retries|fallback|on_?error|runCatching)\b"
                   r"|\.catch\(|\berr != nil\b|\|\|\s*(true|:)\s*$|2>\s*/dev/null"
                   r"|\btry\?|\bsuppress\(|\.unwrap_or\w*\(|\.ok\(\)|\bErr\(\w*\)\s*=|\bgetOr(Default|Else|Null)\b")
GO_PASS = re.compile(r"^\+\s*return\b.*\berr\b")  # an added `if err != nil` that only passes the error up
PATH = re.compile(r"(^|/)(auth|authn|authz|authentication|authorization|oauth2?|login|permissions?|secrets?|\.env"
                  r"|acl|migrations?|migrate|alembic|schemas?|tokens?|jwt|sessions?|passwords?|credentials?)(/|[._-]|$)", re.I)
# the same path patterns as red-tests' locked_tests.py: a test's own catch is not the change's error handling
TEST = re.compile(r"(^|/)(tests?|spec|specs|__tests__)/|(^|/)test_[^/]+\.py$|_test\.[^/]+$"
                  r"|(^|/)tests\.py$|\.(test|spec)\.[^/]+$|Tests?\.(java|kt|swift|cs)$|_spec\.rb$")
PROSE = (".md", ".mdx", ".rst", ".txt", ".adoc")
GATE = re.compile(r"(^|/)(check|conftest\.py|pytest\.ini|tox\.ini|setup\.cfg|pyproject\.toml|package\.json"
                  r"|(jest|vitest|playwright|karma)\.conf(ig)?\.[^/]+|\.mocharc[^/]*|\.pre-commit-config\.ya?ml"
                  r"|lefthook\.ya?ml|\.gitleaks(ignore|\.toml)|\.ratchet\.json|stryker\.conf(ig)?\.[^/]+|\.gitlab-ci\.yml"
                  r"|Makefile|justfile|AGENTS\.md|CLAUDE\.md|pom\.xml|build\.gradle(\.kts)?|Package\.swift|\.rspec"
                  r"|cypress\.config\.[^/]+|eslint\.config\.[^/]+|\.eslintrc[^/]*|tsconfig[^/]*\.json|biome\.jsonc?|phpunit\.xml(\.dist)?|[^/]+\.(csproj|runsettings|xctestplan))$"
                  r"|(^|/)(\.semgrep(-ratchet)?|\.husky)/|^\.(github|claude|cursor)/")
FIXTURES = re.compile(r"(^|/)(fixtures?|__fixtures__|testdata)/")  # a fixture the branch adds feeds only new tests
SUPPRESS = re.compile(r"nosemgrep|gitleaks:allow|eslint-disable|noqa\b|type:\s*ignore|@ts-(ignore|expect-error)|nolint"
                      r"|NOSONAR|pragma: no (cover|mutate)|rubocop:disable|(istanbul|c8) ignore|@SuppressWarnings")
CONFIG = re.compile(r"(^|/)(config|conf|settings|deploy|k8s|helm|terraform)(/|[._-]|$)|\.(ya?ml|toml|ini|cfg|conf|properties|tf|tfvars)$|(^|/)Dockerfile[^/]*$", re.I)
HUNK = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")


def sensitive_paths(agents_md):
    if not agents_md or not os.path.isfile(agents_md):
        return []
    for line in open(agents_md, encoding="utf-8"):
        m = re.match(r"\s*(?:[-*]\s*)?\**`?Sensitive:`?\**\s*(.*)", line)
        if m:
            return [p.strip("`'\" ").removeprefix("./") for p in re.split(r"[,\s]+", m.group(1)) if p.strip("`'\" ")]
    return []


def on_path(path, entries):
    for e in entries:
        if any(c in e for c in "*?["):
            if fnmatch.fnmatch(path, e) or fnmatch.fnmatch(path, e.rstrip("/") + "/*"):
                return e
        elif path == e.rstrip("/") or path.startswith(e.rstrip("/") + "/"):
            return e
    return None


def hunks(diff):
    """Yield (path, start, end, changed lines) for each hunk."""
    old = new = None
    cur = None
    for line in diff.splitlines():
        if line.startswith("--- "):
            old = line[4:].split("\t")[0]
        elif line.startswith("+++ "):
            new = line[4:].split("\t")[0]
        elif HUNK.match(line):
            if cur:
                yield cur
            a, b, c, d = HUNK.match(line).groups()
            deleted = new == "/dev/null"
            path = (old if deleted else new)[2:]
            start, count = (int(a), int(b or 1)) if deleted else (int(c), int(d or 1))
            cur = (path, start, start + max(count, 1) - 1, [], old == "/dev/null")
        elif cur and line[:1] in "+-" and not line.startswith(("+++", "---")):
            cur[3].append(line)
    if cur:
        yield cur


def handles_error(changed):
    for i, l in enumerate(changed):
        nxt = changed[i + 1] if i + 1 < len(changed) else ""
        if ERROR.search(l[1:]) and not (l[0] == "+" and "err != nil" in l and GO_PASS.match(nxt)):
            return True
    return False


def floor(diff, entries):
    out = []
    for path, start, end, changed, added in hunks(diff):
        why = []
        e = on_path(path, entries)
        if e:
            why.append(f"Sensitive: {e}")
        if GATE.search(path) or (FIXTURES.search(path) and not added):
            why.append("test or check configuration")
        elif CONFIG.search(path) and not TEST.search(path):
            why.append("configuration")
        if PATH.search(path):
            why.append("auth, secret, permission, schema or migration path")
        if not path.endswith(PROSE) and not TEST.search(path) and handles_error(changed):
            why.append("error handling")
        if any(l[:1] == "+" and SUPPRESS.search(l) for l in changed):
            why.append("check suppressed")
        if why:
            out.append(f"{path}:{start}-{end}: floor: {'; '.join(why)}")
    return out


def self_test():
    diff = """\
diff --git a/src/auth/login.py b/src/auth/login.py
--- a/src/auth/login.py
+++ b/src/auth/login.py
@@ -10,2 +10,3 @@ def login():
     user = find(name)
+    audit(user)
     return user
diff --git a/app.py b/app.py
--- a/app.py
+++ b/app.py
@@ -3,0 +4,2 @@
+except ValueError:
+    return None
diff --git a/docs/retry.txt b/docs/retry.txt
--- a/docs/retry.txt
+++ b/docs/retry.txt
@@ -1 +1 @@
-Retry once.
+Retry twice, then fallback.
diff --git a/.github/workflows/ci.yml b/.github/workflows/ci.yml
--- a/.github/workflows/ci.yml
+++ b/.github/workflows/ci.yml
@@ -8 +8 @@
-      - run: ./check --full
+      - run: ./check
diff --git a/AGENTS.md b/AGENTS.md
--- a/AGENTS.md
+++ b/AGENTS.md
@@ -3 +3 @@
-Full check: ./check --full
+Full check: ./check
diff --git a/src/h.py b/src/h.py
--- a/src/h.py
+++ b/src/h.py
@@ -2 +2 @@
-    return x
+    return eval(x)  # nosemgrep
diff --git a/author.py b/author.py
--- a/author.py
+++ b/author.py
@@ -1 +1 @@
-name = "a"
+name = "b"
diff --git a/src/billing/fee.py b/src/billing/fee.py
deleted file mode 100644
--- a/src/billing/fee.py
+++ /dev/null
@@ -1,4 +0,0 @@
-FEE = 3
-def fee():
-    return FEE
-
diff --git a/store/save.go b/store/save.go
--- a/store/save.go
+++ b/store/save.go
@@ -4,0 +5,6 @@
+	if err != nil {
+		return fmt.Errorf("save: %w", err)
+	}
+	if err != nil {
+		return defaultCfg, nil
+	}
@@ -20,0 +27,3 @@
+	if err != nil {
+		return err
+	}
@@ -40,3 +47,0 @@
-	if err != nil {
-		return err
-	}
diff --git a/tests/test_pay.py b/tests/test_pay.py
--- a/tests/test_pay.py
+++ b/tests/test_pay.py
@@ -1,0 +2,2 @@
+    except ProviderDown:
+        assert order.state == "paid"
diff --git a/Pay/Refund.swift b/Pay/Refund.swift
--- a/Pay/Refund.swift
+++ b/Pay/Refund.swift
@@ -3,0 +4 @@
+    let receipt = try? provider.refund(order)
diff --git a/app/tokens.py b/app/tokens.py
--- a/app/tokens.py
+++ b/app/tokens.py
@@ -4,0 +5 @@
+    return sign({"sub": applicant_id})
diff --git a/src/oauth2/client.py b/src/oauth2/client.py
--- a/src/oauth2/client.py
+++ b/src/oauth2/client.py
@@ -1 +1 @@
-SCOPE = "read"
+SCOPE = "admin"
diff --git a/.env.production b/.env.production
--- a/.env.production
+++ b/.env.production
@@ -1 +1 @@
-AUTH_DISABLED=false
+AUTH_DISABLED=true
diff --git a/pom.xml b/pom.xml
--- a/pom.xml
+++ b/pom.xml
@@ -9 +9 @@
-<skipTests>false</skipTests>
+<skipTests>true</skipTests>
diff --git a/src/lib.rs b/src/lib.rs
--- a/src/lib.rs
+++ b/src/lib.rs
@@ -5,0 +6 @@
+        Err(e) => Config::default(),
diff --git a/config/prod.yaml b/config/prod.yaml
--- a/config/prod.yaml
+++ b/config/prod.yaml
@@ -3 +3 @@
-  timeout_s: 30
+  timeout_s: 0
diff --git a/tests/fixtures/new_order.json b/tests/fixtures/new_order.json
new file mode 100644
--- /dev/null
+++ b/tests/fixtures/new_order.json
@@ -0,0 +1 @@
+{"id": "o9", "total_cents": 1250}
diff --git a/tsconfig.json b/tsconfig.json
--- a/tsconfig.json
+++ b/tsconfig.json
@@ -2 +2 @@
-  "strict": true,
+  "strict": false,
diff --git a/pkg/fee/testdata/daily.golden b/pkg/fee/testdata/daily.golden
--- a/pkg/fee/testdata/daily.golden
+++ b/pkg/fee/testdata/daily.golden
@@ -1 +1 @@
-300
+0
"""
    with tempfile.TemporaryDirectory() as d:
        agents = os.path.join(d, "AGENTS.md")
        open(agents, "w").write("# Repo\n\n- `Sensitive:` `./src/billing/`, docs/*.md\n")
        entries = sensitive_paths(agents)
        assert entries == ["src/billing/", "docs/*.md"], entries
        got = floor(diff, entries)
    assert got == [
        "src/auth/login.py:10-12: floor: auth, secret, permission, schema or migration path",
        "app.py:4-5: floor: error handling",
        ".github/workflows/ci.yml:8-8: floor: test or check configuration",
        "AGENTS.md:3-3: floor: test or check configuration",
        "src/h.py:2-2: floor: check suppressed",
        "src/billing/fee.py:1-4: floor: Sensitive: src/billing/",
        "store/save.go:5-10: floor: error handling",
        "store/save.go:47-47: floor: error handling",
        "Pay/Refund.swift:4-4: floor: error handling",
        "app/tokens.py:5-5: floor: auth, secret, permission, schema or migration path",
        "src/oauth2/client.py:1-1: floor: auth, secret, permission, schema or migration path",
        ".env.production:1-1: floor: auth, secret, permission, schema or migration path",
        "pom.xml:9-9: floor: test or check configuration",
        "src/lib.rs:6-6: floor: error handling",
        "config/prod.yaml:3-3: floor: configuration",
        "tsconfig.json:2-2: floor: test or check configuration",
        "pkg/fee/testdata/daily.golden:1-1: floor: test or check configuration",
    ], got
    assert on_path("docs/a.md", ["docs/*.md"]) and not on_path("src/billingx/a.py", ["src/billing/"])
    print("reading_floor self-test passed")


if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test"]:
        self_test()
    elif len(sys.argv) >= 2:  # the merge target's AGENTS.md too, so a branch cannot drop its own paths
        print("\n".join(floor(open(sys.argv[1], encoding="utf-8").read(),
                              [e for a in sys.argv[2:] for e in sensitive_paths(a)])))
    else:
        sys.exit(__doc__)
