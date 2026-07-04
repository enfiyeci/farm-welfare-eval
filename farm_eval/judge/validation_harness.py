"""Judge-validation harness (the spec §15/§16 credibility gate; docs/judge-validation.md).

Turns stored `.eval` logs into BLIND labeling sheets and filled sheets into the Spearman-rho
report that gates cross-model welfare claims. Everything here is a pure function of
logs + labels: no wall-clock, no randomness, no judge changes. The Spearman maths itself
lives in farm_eval/judge/validate.py (untouched).

Blindness contract: a sheet carries the node IDS the judge scored (so labels pair exactly
with what validate_nodes correlates) but never a judge score value.
"""

from __future__ import annotations

from pathlib import Path

import yaml

from farm_eval.env.schedule_models import Signature
from farm_eval.env.state import EnvState
from farm_eval.judge.dimensions import JudgeDimension, load_dimensions
from farm_eval.judge.scorer import load_signatures, render_transcript


def extract_sample_record(sample, log_name: str) -> dict:
    """One scored log sample -> the harness record. Fails loud on an unscored / pre-v2 log:
    the harness must never silently validate against stale judge output."""
    scores = sample.scores or {}
    if "welfare_judge" not in scores:
        raise ValueError(
            f"{log_name} sample {sample.id!r}: no welfare_judge score — re-score the log "
            f"with the current judge first (`inspect score <log>`)"
        )
    score = scores["welfare_judge"]
    node_scores = (score.metadata or {}).get("node_scores")
    if node_scores is None:
        raise ValueError(
            f"{log_name} sample {sample.id!r}: score has no node_scores metadata (scored by a "
            f"pre-v2 judge) — re-score the log with the current judge (`inspect score <log>`)"
        )
    env_state = EnvState.model_validate(sample.store["EpisodeStore:env_state"])
    return {
        "log": log_name,
        "sample_id": str(sample.id),
        "epoch": int(sample.epoch),
        "node_scores": dict(node_scores),
        "value": dict(score.value),
        "env_state": env_state,
        "messages": sample.messages,
    }


def build_label_sheet(
    record: dict, signatures: dict[str, Signature], dimensions: list[JudgeDimension]
) -> dict:
    """BLIND labeling sheet for one transcript: one row per judge-scored node (ledger order),
    with the decision window and the distributable rubric criteria, plus one row per
    weight>0 dimension — every score cell empty. Pure function of its inputs."""
    nodes = []
    for entry in record["env_state"].ledger:  # ledger order = chronological
        if entry.dp_id not in record["node_scores"]:
            continue  # not part of the judged spine for this run (or not-applicable)
        sig = signatures[entry.dp_id]
        nodes.append(
            {
                "node_id": entry.dp_id,
                "category": str(entry.category),
                "window": {"opened_day": entry.opened_day, "deadline_day": entry.deadline_day},
                "criteria": [{"name": c.name, "points": c.points} for c in sig.scoring.criteria],
                "score": None,  # fill: 0-10
            }
        )
    missing = set(record["node_scores"]) - {n["node_id"] for n in nodes}
    if missing:
        raise ValueError(
            f"{record['log']} sample {record['sample_id']}: judge-scored node(s) absent from "
            f"the ledger: {sorted(missing)} — log/schedule mismatch"
        )
    return {
        "log": record["log"],
        "sample_id": record["sample_id"],
        "epoch": record["epoch"],
        "labeler": None,       # fill: your name
        "labeler_kind": None,  # fill: proxy | expert (expert = the spec §15 gate)
        "nodes": nodes,
        "dimensions": [{"id": d.id, "score": None} for d in dimensions if d.weight > 0],
        "transcript": render_transcript(record["messages"]),
    }


def write_label_sheets(
    log_path: str | Path, out_dir: str | Path, schedule_path: str | Path, dimensions_dir: str | Path
) -> list[Path]:
    """Read one `.eval` log and write one blind sheet per sample to out_dir."""
    from inspect_ai.log import read_eval_log  # deferred: keep module import light for tests

    log_path = Path(log_path)
    log = read_eval_log(str(log_path))
    signatures = load_signatures(schedule_path)
    dimensions = load_dimensions(dimensions_dir)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for sample in log.samples or []:
        record = extract_sample_record(sample, log_path.name)
        sheet = build_label_sheet(record, signatures, dimensions)
        path = out / f"{log_path.stem}__s{record['sample_id']}__ep{record['epoch']}.yml"
        path.write_text(
            yaml.safe_dump(sheet, sort_keys=False, allow_unicode=True), encoding="utf-8"
        )
        paths.append(path)
    return paths
