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


def test_cohen_kappa_constant_but_different_raters_is_zero_not_degenerate():
    # Both raters constant, but DISAGREE throughout: po=0, pe=0 -> (po-pe)/(1-pe) = 0.
    # This must NOT hit the pe==1.0 degenerate guard (that's for constant-and-SAME marginals).
    assert cohen_kappa([True, True], [False, False]) == pytest.approx(0.0)


def test_kappa_sheets_are_blind(tmp_path):
    art = Artifact(id="emails/x.md", kind="email", text="hello")
    [path] = make_kappa_sheets([art], TAX, tmp_path)
    sheet = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert sheet["artifact_id"] == "emails/x.md"
    assert set(sheet["classes"]) == {c.id for c in TAX}
    assert all(v is None for v in sheet["classes"].values())  # blind


def test_kappa_sheets_collision_raises(tmp_path):
    arts = [
        Artifact(id="emails/x.md", kind="email", text="a"),
        Artifact(id="emails__x.md", kind="email", text="b"),
    ]
    with pytest.raises(ValueError, match="emails/x.md.*emails__x.md|emails__x.md.*emails/x.md"):
        make_kappa_sheets(arts, TAX, tmp_path)


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


def test_normalize_format_preserves_double_underscore_inside_words():
    assert normalize_format("foo__bar") == "foo__bar"
    assert normalize_format("__emphasis__") == "emphasis"


def _labeled_sheet(tmp_path, label_value):
    art = Artifact(id="emails/x.md", kind="email", text="hello")
    [path] = make_kappa_sheets([art], TAX, tmp_path)
    sheet = yaml.safe_load(path.read_text(encoding="utf-8"))
    for cls in sheet["classes"]:
        sheet["classes"][cls] = False
    sheet["classes"]["oversight_claim"] = label_value
    path.write_text(yaml.safe_dump(sheet, sort_keys=False), encoding="utf-8")
    return path


def _base_probe_results():
    return [{
        "artifact_id": "emails/x.md", "kind": "email", "samples": [],
        "flag_counts": {"oversight_claim": 3},
    }]


def test_kappa_report_rejects_quoted_string_label(tmp_path):
    art = Artifact(id="emails/x.md", kind="email", text="hello")
    [path] = make_kappa_sheets([art], TAX, tmp_path)
    raw = path.read_text(encoding="utf-8")
    sheet = yaml.safe_load(raw)
    for cls in sheet["classes"]:
        sheet["classes"][cls] = False
    # Write the YAML with the value quoted so it loads back as the string "false", not bool False.
    lines = yaml.safe_dump(sheet, sort_keys=False).splitlines()
    patched = []
    for line in lines:
        if line.strip() == "oversight_claim: false":
            indent = line[: len(line) - len(line.lstrip())]
            patched.append(f"{indent}oversight_claim: 'false'")
        else:
            patched.append(line)
    path.write_text("\n".join(patched) + "\n", encoding="utf-8")
    reloaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert reloaded["classes"]["oversight_claim"] == "false"  # confirm it loads as str, not bool
    with pytest.raises(ValueError, match="label must be true/false"):
        kappa_report(_base_probe_results(), [path], TAX, samples=3)


def test_kappa_report_rejects_empty_string_label(tmp_path):
    art = Artifact(id="emails/x.md", kind="email", text="hello")
    [path] = make_kappa_sheets([art], TAX, tmp_path)
    sheet = yaml.safe_load(path.read_text(encoding="utf-8"))
    for cls in sheet["classes"]:
        sheet["classes"][cls] = False
    sheet["classes"]["oversight_claim"] = ""
    path.write_text(yaml.safe_dump(sheet, sort_keys=False), encoding="utf-8")
    with pytest.raises(ValueError, match="label must be true/false"):
        kappa_report(_base_probe_results(), [path], TAX, samples=3)
