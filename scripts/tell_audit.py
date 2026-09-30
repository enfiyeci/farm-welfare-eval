# scripts/tell_audit.py
# $PY scripts/tell_audit.py > evals/hen/runs/<today>-tell-audit.md
"""Tell audit (overnight backlog A2): where each scored node's matcher vocabulary is visible.

Measurement only, no model calls. For every scored node episode it lists the strings the node's
signature matches on and every model-visible surface that prints them (tool docstrings, the
node's own emails, reply templates, reject strings, the pricing table, other mail). Logic lives in
`farm_eval/probe/tell_audit.py`.
"""

from __future__ import annotations

import datetime as _dt
import pathlib
import subprocess
import sys

_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))

from farm_eval.probe.tell_audit import audit_repo, render_tell_audit  # noqa: E402


def _git(*args: str) -> str:
    try:
        return subprocess.run(
            ["git", *args], cwd=_ROOT, capture_output=True, text=True, check=True
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "?"


def main() -> None:
    header = "\n".join([
        "# Tell audit: where each scored node's answer vocabulary is visible to the model",
        "",
        "Eval: hen",
        "",
        f"- Generated: {_dt.date.today().isoformat()} by `scripts/tell_audit.py` (no model calls) · "
        f"branch `{_git('rev-parse', '--abbrev-ref', 'HEAD')}` @ `{_git('rev-parse', '--short', 'HEAD')}`",
        "- Regenerate: `$PY scripts/tell_audit.py > evals/hen/runs/<today>-tell-audit.md`",
        "- A **term** is a string a node's signature matches on (a `where` value: task, ration, system,",
        "  method, beak key ...). A surface cell reads `where (matches)`. **tool doc** = the adapter tool",
        "  docstrings the model sees before any email; **trigger mail** = the node's own emails (all",
        "  variants); **other mail** = every other email body (a findable path, or a leak elsewhere).",
        "  **partial** = a multi-word term's single words (5+ letters) in the trigger mail.",
        "- This measures exact vocabulary. A lever described in other words (\"the pads\", \"the fixture",
        "  over that corner\") shows only in the partial column or not at all, so read the trigger mail",
        "  itself before calling a node clean.",
    ])
    sys.stdout.write(render_tell_audit(audit_repo(_ROOT), header=header))


if __name__ == "__main__":
    main()
