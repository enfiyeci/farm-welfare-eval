"""P6 — diff a minimal-contrast pair of episode logs into a findings doc.

The pure part (render_findings) is unit-tested; the CLI shell reads the two .eval logs via
the validation harness's extractor (which already fails loud on unscored/partial logs).

Usage:
    ./venv/bin/python scripts/diff_pair.py --baseline a.eval --variant b.eval \\
        --node DP01_AMMONIA_VENT --out findings.md
"""

import argparse
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def render_findings(baseline: dict, variant: dict, *, node: str, baseline_name: str, variant_name: str) -> str:
    if not (variant.get("metadata") or {}).get("experimental_run"):
        raise ValueError(
            "variant log carries no experimental stamp — it was not run with ablation_overrides; "
            "refusing to diff two baselines"
        )
    b_node = baseline["node_scores"].get(node)
    v_node = variant["node_scores"].get(node)
    if b_node is None or v_node is None:
        raise ValueError(f"node {node!r} missing from a log's node_scores")
    b_ea = baseline["value"].get("eval_awareness")
    v_ea = variant["value"].get("eval_awareness")
    lines = [
        f"# Divergence findings — {node}",
        "",
        "> DIRECTIONAL / QUALITATIVE ONLY — single paired episodes, never a powered test;",
        "> findings, not p-values (docs/divergence-protocol.md).",
        "",
        f"| | baseline ({baseline_name}) | variant ({variant_name}) |",
        "|---|---|---|",
        f"| {node} node score | {b_node} | {v_node} |",
        f"| welfare_headline | {baseline['value'].get('welfare_headline')} | {variant['value'].get('welfare_headline')} |",
        f"| eval_awareness (verbal, lower bound) | {b_ea} | {v_ea} |",
        "",
    ]
    if v_node < b_node:
        lines += [
            "**BEHAVIOR-HOLDS FLAG (exam-driven virtue):** the restyled (more realistic) arm",
            "scored WORSE on this node — evidence the baseline's welfare behavior is partly",
            "exam-driven. This is a validity finding about the eval; report it prominently.",
            "",
        ]
    cues = (variant.get("metadata") or {}).get("cue_localization") or []
    lines += ["## Variant cue-localization panel", ""]
    if cues:
        lines += ["| dimension | sample | score | trigger_type | artifact | message |", "|---|---|---|---|---|---|"]
        for c in cues:
            lines.append(
                f"| {c['dimension']} | {c['sample']} | {c['score']} | "
                f"{c.get('trigger_type', 'unspecified')} | {c.get('artifact', 'unknown')} | {c.get('message_id', '')} |"
            )
    else:
        lines.append("(no localization rows — verbal awareness gate did not fire or grader gave none)")
    return "\n".join(lines) + "\n"


def _load(log_path: str) -> dict:
    from inspect_ai.log import read_eval_log

    from farm_eval.judge.validation_harness import extract_sample_record

    log = read_eval_log(log_path)
    if not log.samples:
        sys.exit(f"{log_path}: no samples")
    record = extract_sample_record(log.samples[0], pathlib.Path(log_path).name)
    score = log.samples[0].scores["welfare_judge"]
    return {"node_scores": record["node_scores"], "value": record["value"],
            "metadata": dict(score.metadata or {})}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--variant", required=True)
    parser.add_argument("--node", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    findings = render_findings(
        _load(args.baseline), _load(args.variant), node=args.node,
        baseline_name=pathlib.Path(args.baseline).name, variant_name=pathlib.Path(args.variant).name,
    )
    pathlib.Path(args.out).write_text(findings, encoding="utf-8")
    print(findings)


if __name__ == "__main__":
    main()
