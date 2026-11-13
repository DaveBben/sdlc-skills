#!/usr/bin/env python3
"""Compare the sdlc plugin against a plain prompt on the same tasks, by outcome.

Each task is a directory under tools/tasks/:

  task.json   {"prompt": ..., "check": <shell command>, "defect": <regex, one match per defect>,
               "repo": <optional git URL or path>, "ref": <optional commit>}
  repo/       the starting tree, when task.json names no "repo"
  hidden/     files copied over the tree after the agent stops, such as held-out tests

Each arm runs `claude -p` on a fresh copy of the tree: `plain` with the task's prompt alone,
`prompted` with one sentence of the plugin's rule added, and `sdlc` with this working copy's
plugin. The plugin has to beat `prompted`, the cheapest rival. Scored per run:

  * defects:  matches of "defect" in the check's output once the hidden files are in, or 1
              when it exits non-zero with none.
  * red:      1 when the check already failed on the tree as the agent left it, a false "done".
  * tampered: lines the run changed or removed in test files that the task started with.
  * minutes, dollars, turns: from the CLI's own result.

No person is in a headless run, so a person's interventions are not measured; count those by
hand in real sessions. The plugin's agents name their own models, so `--model` sets only the
main session.

Runs go under ~/.sdlc-baseline-runs: outside this repository, whose AGENTS.md would load into
every arm, and outside the system temp directory, where skills do not load. Usage:

    python3 tools/baseline.py                      # every task, every arm, once
    python3 tools/baseline.py --only bulk-discount --runs 3 --model sonnet
"""
import argparse, json, os, re, shutil, subprocess, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TASKS, RUNS = os.path.join(REPO, "tools", "tasks"), os.path.expanduser("~/.sdlc-baseline-runs")
RULE = " Write the tests first, and have a fresh subagent that did not write the code review the diff before you finish."
ARMS = {"plain": ("", []), "prompted": (RULE, []), "sdlc": ("", ["--plugin-dir", os.path.join(REPO, "plugins", "sdlc")])}
# Project settings only, so neither arm loads the user's installed plugins or instructions.
# shortcut: commands run unsandboxed with edits and Bash approved; run only tasks you trust.
CLAUDE = ["--setting-sources", "project", "--permission-mode", "acceptEdits", "--allowedTools", "Bash",
          "--output-format", "json", "--max-turns", "150"]


def sh(*args, cwd):
    subprocess.run(args, cwd=cwd, check=True, capture_output=True)


def run_one(name, arm, n, model):
    task_dir = os.path.join(TASKS, name)
    task = json.load(open(os.path.join(task_dir, "task.json")))
    work = os.path.join(RUNS, name, f"{arm}-{n}")
    shutil.rmtree(work, ignore_errors=True)
    if task.get("repo"):
        sh("git", "clone", "-q", task["repo"], work, cwd=REPO)
        sh("git", "checkout", "-q", task.get("ref", "HEAD"), cwd=work)
    else:
        shutil.copytree(os.path.join(task_dir, "repo"), work)
        sh("git", "init", "-q", cwd=work)
        sh("git", "add", "-A", cwd=work)
        sh("git", "-c", "user.email=baseline@local", "-c", "user.name=baseline", "commit", "-qm", "start", cwd=work)
    start = subprocess.run(["git", "rev-parse", "HEAD"], cwd=work, capture_output=True, text=True).stdout.strip()
    suffix, flags = ARMS[arm]
    r = subprocess.run(["claude", "-p", task["prompt"] + suffix, *CLAUDE, *flags, *(["--model", model] if model else [])],
                       cwd=work, capture_output=True, text=True)
    try:
        out = json.loads(r.stdout)
    except ValueError:
        out = {"is_error": True}
    open(work + ".json", "w").write(r.stdout or r.stderr)
    stat = subprocess.run(["git", "diff", "--numstat", "--no-renames", start, "--"], cwd=work, capture_output=True, text=True).stdout
    tampered = sum(int(row[1]) for row in (l.split("\t") for l in stat.splitlines())
                   if row[1].isdigit() and re.search(r"(^|/)(tests?|spec|__tests__)/|test_|_test\.|\.(test|spec)\.", row[2]))
    red = subprocess.run(task["check"], shell=True, cwd=work, capture_output=True).returncode != 0
    hidden = os.path.join(task_dir, "hidden")
    if os.path.isdir(hidden):
        shutil.copytree(hidden, work, dirs_exist_ok=True)
    c = subprocess.run(task["check"], shell=True, cwd=work, capture_output=True, text=True)
    open(work + ".check.txt", "w").write(c.stdout + c.stderr)
    found = len(re.findall(task.get("defect", r"(?!)"), c.stdout + c.stderr, re.M))
    return {"task": name, "arm": arm, "defects": found or int(c.returncode != 0),
            "red": int(red), "tampered": tampered, "minutes": out.get("duration_ms", 0) / 60000,
            "dollars": out.get("total_cost_usd", 0), "turns": out.get("num_turns", 0), "error": bool(out.get("is_error"))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="one task's directory name")
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--model")
    a = ap.parse_args()
    names = [a.only] if a.only else sorted(d for d in os.listdir(TASKS) if os.path.isdir(os.path.join(TASKS, d)))
    rows = [run_one(name, arm, n, a.model) for name in names for arm in ARMS for n in range(1, a.runs + 1)]
    print(f"{'task':24}{'arm':7}{'runs':>5}{'defects':>9}{'red':>5}{'tampered':>10}{'minutes':>9}{'dollars':>9}{'turns':>7}")
    for name in names + ["ALL"]:
        for arm in ARMS:
            rs = [r for r in rows if r["arm"] == arm and name in (r["task"], "ALL")]
            mean = lambda k: sum(r[k] for r in rs) / len(rs)
            print(f"{name:24}{arm:7}{len(rs):>5}{mean('defects'):>9.1f}{mean('red'):>5.1f}{mean('tampered'):>10.1f}{mean('minutes'):>9.1f}"
                  f"{mean('dollars'):>9.2f}{mean('turns'):>7.0f}" + ("  (a run errored)" if any(r["error"] for r in rs) else ""))
    os.makedirs(RUNS, exist_ok=True)
    json.dump(rows, open(os.path.join(RUNS, "last.json"), "w"), indent=1)


if __name__ == "__main__":
    sys.exit(main())
