# $PY scripts/node_reliability.py logs/<run>.eval [--headline-arm neutral]
"""Print the per-node reliability table (pass rate, pass^k, headline) for a farm_node_task log."""
import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from inspect_ai.log import read_eval_log  # noqa: E402

from farm_eval.report.reliability import (  # noqa: E402
    criteria_from_log,
    render_criteria,
    render_table,
    rows_from_log,
    summarize,
)


def _usage_lines(log) -> list[str]:
    lines: list[str] = []
    stats = getattr(log, "stats", None)
    if stats is None:
        return lines
    usage = getattr(stats, "model_usage", None) or {}
    if usage:
        totals = []
        for model_name, mu in sorted(usage.items()):
            input_tokens = getattr(mu, "input_tokens", None)
            output_tokens = getattr(mu, "output_tokens", None)
            totals.append(f"{model_name}: input={input_tokens} output={output_tokens}")
        lines.append("token usage: " + "; ".join(totals))
    started_at = getattr(stats, "started_at", None)
    completed_at = getattr(stats, "completed_at", None)
    if started_at and completed_at:
        lines.append(f"wall time: {started_at} -> {completed_at}")
    return lines


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("log")
    ap.add_argument("--headline-arm", default="neutral")
    args = ap.parse_args()
    log = read_eval_log(args.log)
    print(render_table(summarize(rows_from_log(log), headline_arm=args.headline_arm)))
    # D1 (WP2): why each node scored what it did. Logs from before the breakdown existed say so.
    breakdown = render_criteria(criteria_from_log(log))
    print(breakdown or "criterion breakdown: not recorded in this log (written before node_criteria existed)")
    for line in _usage_lines(log):
        print(line)


if __name__ == "__main__":
    main()
