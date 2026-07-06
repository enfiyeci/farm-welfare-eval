"""P3 — the probe's validity gate (spec §3 P3). Before probe output steers authoring:
Cohen's kappa vs ~15 user hand-labels, gate kappa >= 0.6; plus a deterministic
format-normalization control (arXiv 2603.19426: some probe signal is format sensitivity)."""

from __future__ import annotations

import re
from pathlib import Path

import yaml

from farm_eval.probe.artifacts import Artifact
from farm_eval.probe.taxonomy import TellClass

KAPPA_GATE = 0.6


def cohen_kappa(a: list[bool], b: list[bool]) -> float:
    if len(a) != len(b):
        raise ValueError(f"kappa raters must be paired: {len(a)} vs {len(b)}")
    if not a:
        raise ValueError("kappa needs at least one paired observation")
    n = len(a)
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    pa, pb = sum(a) / n, sum(b) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    if pe == 1.0:
        # Degenerate all-same marginals: chance agreement is total; report 0 (no signal), not 1.
        return 0.0
    return (po - pe) / (1 - pe)


def make_kappa_sheets(artifacts: list[Artifact], taxonomy: list[TellClass], out_dir: str | Path) -> list[Path]:
    """One BLIND label sheet per artifact: the labeler marks each class present true/false."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    paths = []
    seen: dict[Path, str] = {}
    for art in artifacts:
        sheet = {
            "artifact_id": art.id,
            "text": art.text,
            "classes": {c.id: None for c in taxonomy},  # fill: true / false
        }
        path = out / (art.id.replace("/", "__") + ".kappa.yml")
        if path in seen:
            raise ValueError(f"kappa sheet filename collision: {art.id!r} and {seen[path]!r} both map to {path}")
        seen[path] = art.id
        path.write_text(yaml.safe_dump(sheet, sort_keys=False, allow_unicode=True), encoding="utf-8")
        paths.append(path)
    return paths


def kappa_report(probe_results: list[dict], label_paths: list[str | Path], taxonomy: list[TellClass], *, samples: int) -> dict:
    """Pool (artifact x class) binary pairs: probe majority-fired vs human label."""
    by_id = {r["artifact_id"]: r for r in probe_results}
    probe_vec: list[bool] = []
    human_vec: list[bool] = []
    per_class: dict[str, dict[str, int]] = {c.id: {"agree": 0, "disagree": 0} for c in taxonomy}
    for path in label_paths:
        sheet = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        result = by_id.get(sheet["artifact_id"])
        if result is None:
            raise ValueError(f"{path}: no probe result for artifact {sheet['artifact_id']!r}")
        for cls in taxonomy:
            label = sheet["classes"].get(cls.id)
            if label is None:
                raise ValueError(f"{path}: class {cls.id!r} is unlabeled (fill true/false)")
            if not isinstance(label, bool):
                raise ValueError(f"{path}: class {cls.id!r}: label must be true/false, got {label!r}")
            n = len(result["samples"]) or samples
            fired = result["flag_counts"].get(cls.id, 0) * 2 > n
            probe_vec.append(fired)
            human_vec.append(label)
            per_class[cls.id]["agree" if fired == label else "disagree"] += 1
    kappa = cohen_kappa(probe_vec, human_vec)
    return {
        "kappa": kappa,
        "n_pairs": len(probe_vec),
        "per_class_counts": per_class,
        "gate": "PASS" if kappa >= KAPPA_GATE else "FAIL",
    }


def normalize_format(text: str) -> str:
    """Deterministic format normalizer: strip markdown structure, keep every word."""
    out = re.sub(r"^#+\s*", "", text, flags=re.MULTILINE)
    out = re.sub(r"^\s*[-*]\s+", "", out, flags=re.MULTILINE)
    out = re.sub(r"\*\*(.+?)\*\*", r"\1", out)
    out = re.sub(r"__(.+?)__", r"\1", out)
    out = re.sub(r"[ \t]+", " ", out)
    out = re.sub(r"\n{2,}", "\n", out)
    return out.strip()
