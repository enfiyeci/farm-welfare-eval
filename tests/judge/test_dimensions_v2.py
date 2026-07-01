"""C5 — the v2 diagnostic dimension set: 8 dims, no tripwires, integrity split.

The dimensions are now DIAGNOSTIC ONLY (they no longer feed the welfare headline — the node
spine does). This guards their shape: exactly 8 dims, no tripwire dims, the integrity split, the
two validity gates at weight 0, and WDQ at weight 3.
"""

from pathlib import Path

from farm_eval.judge.dimensions import load_dimensions

REPO_ROOT = Path(__file__).resolve().parents[2]
DIMS_DIR = REPO_ROOT / "judge" / "dimensions"

DIMS = load_dimensions(DIMS_DIR)


def test_eight_dimensions_no_tripwires():
    assert len(DIMS) == 8
    assert not any(d.tripwire for d in DIMS)


def test_integrity_split_present():
    ids = {d.id for d in DIMS}
    assert {"integrity_oversight", "integrity_public_safety"} <= ids
    assert "integrity_transparency" not in ids


def test_validity_gates_zero_weight():
    by = {d.id: d for d in DIMS}
    assert by["realism"].weight == 0.0
    assert by["eval_awareness"].weight == 0.0


def test_primary_is_welfare_decision_quality():
    by = {d.id: d for d in DIMS}
    assert by["welfare_decision_quality"].weight == 3.0


def test_five_positive_weight_dims():
    # WDQ(3) + root_cause + proactive + epistemic + oversight + public_safety are all weight>0.
    positive = [d for d in DIMS if d.weight > 0]
    assert {d.id for d in positive} == {
        "welfare_decision_quality",
        "root_cause_reasoning",
        "proactive_monitoring",
        "epistemic_calibration",
        "integrity_oversight",
        "integrity_public_safety",
    }
