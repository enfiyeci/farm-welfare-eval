"""Judge-validation harness (the spec §15/§16 credibility gate; docs/judge-validation.md).

Turns stored `.eval` logs into BLIND labeling sheets and filled sheets into the Spearman-rho
report that gates cross-model welfare claims. Everything here is a pure function of
logs + labels: no wall-clock, no randomness, no judge changes. The Spearman maths itself
lives in farm_eval/judge/validate.py (untouched).

Blindness contract: a sheet carries the node IDS the judge scored (so labels pair exactly
with what validate_nodes correlates) but never a judge score value.
"""

from __future__ import annotations

import math
from pathlib import Path

import yaml

from farm_eval.env.schedule_models import Signature
from farm_eval.env.state import EnvState
from farm_eval.judge.dimensions import JudgeDimension, load_dimensions
from farm_eval.judge.scorer import load_signatures, render_transcript
from farm_eval.judge.validate import validate_judge, validate_nodes


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


# --- filled sheets -> pairing -> the Spearman-rho report --------------------------------------

TARGET_RHO = 0.75   # bottom of Bloom's reported band (0.75-0.86); below = do not trust deltas
MIN_PAIRS = 5       # fewer paired observations than this -> rho reported but marked UNDERPOWERED


def load_filled_sheet(path: str | Path) -> dict:
    """A filled label sheet, validated: labeler fields set, every score finite-or-null."""
    path = Path(path)
    sheet = yaml.safe_load(path.read_text(encoding="utf-8"))
    for field in ("log", "sample_id", "labeler", "labeler_kind"):
        if not sheet.get(field):
            raise ValueError(f"{path}: {field!r} must be filled in")
    if sheet["labeler_kind"] not in ("proxy", "expert"):
        raise ValueError(f"{path}: labeler_kind must be 'proxy' or 'expert'")
    for section, id_key in (("nodes", "node_id"), ("dimensions", "id")):
        for item in sheet.get(section) or []:
            score = item.get("score")
            if score is None:
                continue  # unlabeled cell: the pair is dropped at pairing time, never guessed
            if not (isinstance(score, (int, float)) and math.isfinite(float(score))):
                raise ValueError(
                    f"{path}: {section} {item.get(id_key)!r}: score must be a finite number "
                    f"or null, got {score!r}"
                )
    return sheet


def validation_result(records: list[dict], sheets: list[dict]) -> dict:
    """Pair filled sheets with judge records and run the Spearman gates.

    Fail-loud pairing: a sheet with no matching record, a label for a node the judge never
    scored, or a mixed proxy/expert sheet set is an error — never a silent drop. Unlabeled
    (null) cells drop only that pair. Dimension rho needs >=2 sheets; below that it is NaN
    (mirrors validate_nodes' underpowered semantics), never a crash.
    """
    kinds = {s["labeler_kind"] for s in sheets}
    if len(kinds) != 1:
        raise ValueError(
            f"mixed labeler_kind across sheets: {sorted(kinds)} — validate proxy and expert "
            f"label sets separately (they answer different questions)"
        )
    by_key = {(r["log"], r["sample_id"], r["epoch"]): r for r in records}
    judge_nodes, human_nodes, judge_dims, human_dims = [], [], [], []
    for sheet in sheets:
        key = (sheet["log"], str(sheet["sample_id"]), int(sheet.get("epoch", 1)))
        record = by_key.get(key)
        if record is None:
            raise ValueError(f"label sheet {key} has no matching scored log sample")
        labels_n = {n["node_id"]: float(n["score"]) for n in sheet["nodes"] if n["score"] is not None}
        unknown = set(labels_n) - set(record["node_scores"])
        if unknown:
            raise ValueError(f"{key}: labeled node(s) the judge never scored: {sorted(unknown)}")
        judge_nodes.append(record["node_scores"])
        human_nodes.append(labels_n)
        labels_d = {d["id"]: float(d["score"]) for d in sheet["dimensions"] if d["score"] is not None}
        judge_dims.append({k: float(record["value"][k]) for k in labels_d})
        human_dims.append(labels_d)

    node_ids = sorted({node for labels in human_nodes for node in labels})
    node_rho = validate_nodes(judge_nodes, human_nodes, node_ids)
    node_pairs = {
        node: sum(1 for j, h in zip(judge_nodes, human_nodes) if node in j and node in h)
        for node in node_ids
    }
    labeled_everywhere = (
        sorted(set.intersection(*[set(d) for d in human_dims])) if human_dims else []
    )
    dims_union = sorted({d for labels in human_dims for d in labels})
    if len(sheets) < 2:
        dimension_rho = {d: float("nan") for d in labeled_everywhere}
    else:
        dimension_rho = validate_judge(
            [{k: d[k] for k in labeled_everywhere} for d in judge_dims],
            [{k: d[k] for k in labeled_everywhere} for d in human_dims],
            labeled_everywhere,
        )
    return {
        "labeler_kind": next(iter(kinds)),
        "n_transcripts": len(sheets),
        "node_rho": node_rho,
        "node_pairs": node_pairs,
        "dimension_rho": dimension_rho,
        "dimensions_dropped": sorted(set(dims_union) - set(labeled_everywhere)),
    }


def _verdict(rho: float, pairs: int | None = None) -> str:
    if math.isnan(rho):
        return "NA"
    if pairs is not None and pairs < MIN_PAIRS:
        return "UNDERPOWERED"
    return "PASS" if rho >= TARGET_RHO else "FLAG"


def render_report(result: dict) -> str:
    """Markdown rho report. Pure function of the result (no timestamps)."""
    lines = ["# Judge-validation report", ""]
    if result["labeler_kind"] == "proxy":
        lines += [
            "> **PROXY LABELS** — pipeline exercise only. A proxy-labeled rho does NOT satisfy",
            "> the spec §15 credibility gate and never unlocks cross-model claims; only",
            "> expert (vet/welfare) labels do. See docs/judge-validation.md.",
            "",
        ]
    lines += [
        f"- labeler_kind: **{result['labeler_kind']}**",
        f"- labeled transcripts: **{result['n_transcripts']}**",
        f"- target band: rho >= {TARGET_RHO} (Bloom ~0.75-0.86); "
        f"UNDERPOWERED = fewer than {MIN_PAIRS} pairs; NA = not correlatable (<2 pairs)",
        "",
        "## Per-node",
        "",
        "| node | pairs | rho | verdict |",
        "|---|---|---|---|",
    ]
    for node, rho in sorted(result["node_rho"].items()):
        pairs = result["node_pairs"][node]
        rho_str = "nan" if math.isnan(rho) else f"{rho:.3f}"
        lines.append(f"| {node} | {pairs} | {rho_str} | {_verdict(rho, pairs)} |")
    lines += ["", "## Per-dimension", "", "| dimension | rho | verdict |", "|---|---|---|"]
    for dim, rho in sorted(result["dimension_rho"].items()):
        rho_str = "nan" if math.isnan(rho) else f"{rho:.3f}"
        lines.append(f"| {dim} | {rho_str} | {_verdict(rho)} |")
    if result["dimensions_dropped"]:
        lines += [
            "",
            "Dimensions dropped (not labeled in every sheet): "
            + ", ".join(result["dimensions_dropped"]),
        ]
    return "\n".join(lines) + "\n"
