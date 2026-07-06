"""P3 — the probe's own validity gate: Cohen's kappa vs hand labels + format control."""

import math

import pytest
import yaml

from farm_eval.probe.artifacts import Artifact
from farm_eval.probe.kappa import cohen_kappa, kappa_report, make_kappa_sheets, normalize_format
from farm_eval.probe.taxonomy import load_taxonomy

TAX = load_taxonomy()


def test_cohen_kappa_perfect_and_chance():
    assert cohen_kappa([True, False, True, False], [True, False, True, False]) == pytest.approx(1.0)
    # 50/50 marginals, agreement at chance level -> kappa ~ 0
    assert abs(cohen_kappa([True, True, False, False], [True, False, True, False])) < 1e-9


def test_cohen_kappa_rejects_mismatch_and_empty():
    with pytest.raises(ValueError):
        cohen_kappa([True], [True, False])
    with pytest.raises(ValueError):
        cohen_kappa([], [])


def test_kappa_sheets_are_blind(tmp_path):
    art = Artifact(id="emails/x.md", kind="email", text="hello")
    [path] = make_kappa_sheets([art], TAX, tmp_path)
    sheet = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert sheet["artifact_id"] == "emails/x.md"
    assert set(sheet["classes"]) == {c.id for c in TAX}
    assert all(v is None for v in sheet["classes"].values())  # blind


def test_kappa_report_gate(tmp_path):
    art = Artifact(id="emails/x.md", kind="email", text="hello")
    [path] = make_kappa_sheets([art], TAX, tmp_path)
    sheet = yaml.safe_load(path.read_text(encoding="utf-8"))
    for cls in sheet["classes"]:
        sheet["classes"][cls] = False
    sheet["classes"]["oversight_claim"] = True
    path.write_text(yaml.safe_dump(sheet, sort_keys=False), encoding="utf-8")
    probe_results = [{
        "artifact_id": "emails/x.md", "kind": "email", "samples": [],
        "flag_counts": {"oversight_claim": 3},  # majority of samples=3
    }]
    # kappa over one artifact x 8 classes, probe majority-fired matches labels exactly
    out = kappa_report(probe_results, [path], TAX, samples=3)
    assert out["n_pairs"] == len(TAX)
    assert out["kappa"] == pytest.approx(1.0)
    assert out["gate"] == "PASS"


def test_normalize_format_strips_structure_only():
    messy = "# Header\n\n- item one\n- item two\n\n**bold** claim   here"
    clean = normalize_format(messy)
    assert "#" not in clean and "- " not in clean and "**" not in clean
    for word in ("Header", "item", "bold", "claim", "here"):
        assert word in clean
