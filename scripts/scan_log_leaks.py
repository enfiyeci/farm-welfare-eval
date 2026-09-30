# scripts/scan_log_leaks.py
# $PY scripts/scan_log_leaks.py <log.eval | dir> ... > evals/hen/runs/<today>-log-leak-scan.md
"""Log leak scan (overnight backlog E2): day indices, "days pass", "[Time passes]"-style tags,
day-numbered ids, corpus file names, decision-point ids and eval vocabulary in what the model saw.

Reads `.eval` logs one sample at a time (read-only, no model calls) and prints a markdown
report. Directories are searched recursively for `*.eval`. Logic lives in
`farm_eval/probe/log_leaks.py`.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import pathlib
import subprocess
import sys

_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))

from inspect_ai.log import read_eval_log, read_eval_log_samples  # noqa: E402

from farm_eval.probe.log_leaks import SampleScan, render_report, scan_sample  # noqa: E402


def _git(*args: str) -> str:
    try:
        return subprocess.run(["git", *args], cwd=_ROOT, capture_output=True, text=True,
                              check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "?"


def _log_files(paths: list[str]) -> list[pathlib.Path]:
    out: list[pathlib.Path] = []
    for raw in paths:
        p = pathlib.Path(raw)
        out.extend(sorted(p.rglob("*.eval")) if p.is_dir() else [p])
    return out


def _tools_of(sample) -> list:
    for event in sample.events or []:
        if getattr(event, "event", "") == "model" and getattr(event, "tools", None):
            return list(event.tools)
    return []


def scan_log(path: pathlib.Path) -> tuple[str, str, list[SampleScan]]:
    header = read_eval_log(str(path), header_only=True)
    roles = {k: v.model for k, v in (header.eval.model_roles or {}).items()}
    note = (f"task `{header.eval.task}` · model `{header.eval.model}` · roles {roles or '-'} · "
            f"status `{header.status}`")
    scans: list[SampleScan] = []
    if header.status != "started":
        for sample in read_eval_log_samples(str(path), all_samples_required=False):
            scans.append(scan_sample(f"{sample.id} (epoch {sample.epoch})", list(sample.messages),
                                     _tools_of(sample)))
    return path.name, note, scans


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("paths", nargs="+", help=".eval files or directories")
    args = ap.parse_args(argv)
    files = _log_files(args.paths)
    results = [scan_log(f) for f in files]
    shown = ", ".join(f"`{p}`" for p in args.paths)
    header = "\n".join([
        "# Log leak scan: eval signals in what the model saw",
        "",
        "Eval: hen",
        "",
        f"- Generated: {_dt.date.today().isoformat()} by `scripts/scan_log_leaks.py` (read-only, no "
        f"model calls) · branch `{_git('rev-parse', '--abbrev-ref', 'HEAD')}` @ "
        f"`{_git('rev-parse', '--short', 'HEAD')}`",
        f"- Scanned: {shown}",
        "- **world** = system prompt, user turns (briefing, session digest), tool results and tool",
        "  definitions: a hit is a harness leak. **model echoes** = the target's own text and tool",
        "  arguments: reported apart, never counted as a leak. **info** patterns are not leaks under",
        "  the rulings; they are listed for the owner.",
    ])
    sys.stdout.write(render_report(results, header=header))
    return 0


if __name__ == "__main__":
    sys.exit(main())
