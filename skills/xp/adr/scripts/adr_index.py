#!/usr/bin/env python3
"""Claude Code SessionStart hook for the adr skill: prints one line per ADR under
docs/adr/ that has no `Superseded by:` line, its title and path, so a session
knows which decisions exist without loading them. Prints nothing when the
repository has no docs/adr/.

Reads the hook input on stdin for the working directory. Registered by the SDLC
plugin's hooks.json. Run with --self-test to check it.
"""
import json, os, re, subprocess, sys

MAX = 40
# A status line that takes an ADR out of force: "Superseded by: x" (this skill), "Status: superseded by x",
# a Nygard "## Status" body line "Superseded by [3](0003.md)", and a bare "Rejected" or "Status: Deprecated".
OUT_OF_FORCE = re.compile(r"^\W*(status\W*)?(superseded by\b|(rejected|deprecated)\W*$)", re.M | re.I)
NOT_ADR = re.compile(r"^(readme|index|(\d+-)?template)\.md$", re.I)


def root(cwd):
    try:
        out = subprocess.run(["git", "-C", cwd, "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, timeout=5)
        return out.stdout.strip() or cwd
    except (OSError, subprocess.SubprocessError):
        return cwd


def prose(text):
    """The text with fenced code blocks removed, so an example inside one never counts."""
    lines, fenced = [], False
    for line in text.splitlines():
        if line.startswith("```"):
            fenced = not fenced
        elif not fenced:
            lines.append(line)
    return "\n".join(lines)


def heading(text):
    return next((line[2:].strip() for line in text.splitlines() if line.startswith("# ")), "")


def index(top):
    # walks subfolders too, so ADRs filed in the older per-feature folders still show
    paths = sorted(os.path.join(d, f) for d, _, files in os.walk(os.path.join(top, "docs", "adr"))
                   for f in files if f.endswith(".md") and not NOT_ADR.search(f))
    rows = []
    for path in paths:
        try:
            text = prose(open(path, encoding="utf-8-sig", errors="replace").read())
        except OSError:
            continue
        if not OUT_OF_FORCE.search(text):
            title = heading(text) or os.path.basename(path)[:-3]
            rows.append(f"- {title}: {os.path.relpath(path, top)}")
    return rows


def render(rows):
    if not rows:
        return ""
    lines = ["Decisions in force (docs/adr/). Read the one that applies before choosing "
             "a library, a data shape or a boundary:"] + rows[:MAX]
    if len(rows) > MAX:
        lines.append(f"- and {len(rows) - MAX} more under docs/adr/")
    return "\n".join(lines)


def main():
    try:
        cwd = json.load(sys.stdin).get("cwd") or os.getcwd()
    except (ValueError, AttributeError):
        cwd = os.getcwd()
    out = render(index(root(cwd)))
    if out:
        print(out)


def self_test():
    import tempfile
    with tempfile.TemporaryDirectory() as t:
        assert render(index(t)) == "", "no docs/adr prints nothing"
        a = os.path.join(t, "docs", "adr")
        os.makedirs(os.path.join(a, "old-feature"))
        files = {
            "use-redis.md": "# Use Redis\n\n**Supersedes:** none.\n",
            "use-memcached.md": "# Use Memcached\n\n**Superseded by:** docs/adr/use-redis.md\n",
            "notes.txt": "# Not an ADR\n",
            "README.md": "# Index\n",
            "0000-template.md": "# Template\n",
            "0002-nygard.md": "# Old\n\n## Status\n\nSuperseded by [3](0003.md)\n",
            "0003-status.md": "# Older\nStatus: superseded by 0004\n",
            "0004-rejected.md": "# Refused\n\n## Status\n\nRejected\n",
            "0005-deprecated.md": "---\nstatus: deprecated\n---\n# Dropped\n",
            "fenced.md": "```text\n# not this\nSuperseded by: example only\n```\n# Fenced title\n**Supersedes:** none.\n",
            "prose.md": "# Drop the legacy importer\n\n- Superseded exports in old files stay unreadable.\n",
            "use-jinja-templates-for-email.md": "# Use Jinja templates\n",
            "bom.md": "\ufeff# Has a BOM\n",
            "old-feature/nested.md": "# Nested\n",
        }
        for name, text in files.items():
            open(os.path.join(a, name), "w", encoding="utf-8").write(text)
        out = render(index(t))
        for kept in ("- Use Redis: docs/adr/use-redis.md", "- Fenced title: docs/adr/fenced.md",
                     "- Drop the legacy importer:", "- Use Jinja templates:", "- Has a BOM:",
                     "- Nested: docs/adr/old-feature/nested.md"):
            assert kept in out, (kept, out)
        for gone in ("Memcached", "Not an ADR", "Index", "Template", "Old", "Refused", "Dropped", "not this"):
            assert gone not in out, (gone, out)
        run = subprocess.run([sys.executable, __file__], input=json.dumps({"cwd": t}),
                             capture_output=True, text=True, timeout=10)
        assert run.returncode == 0 and "- Use Redis: docs/adr/use-redis.md" in run.stdout, run
        for i in range(MAX + 2):
            open(os.path.join(a, f"d{i:02}.md"), "w").write(f"# D{i}\n**Supersedes:** none.\n")
        out = render(index(t))
        assert out.endswith(f"- and {len(index(t)) - MAX} more under docs/adr/"), out
    print("self-test passed")


if __name__ == "__main__":
    self_test() if sys.argv[1:] == ["--self-test"] else main()
