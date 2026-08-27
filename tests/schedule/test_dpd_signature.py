from pathlib import Path

import json

from farm_eval.env.loader import load_schedule


ROOT = Path(__file__).resolve().parents[2]


def _signature():
    schedule = load_schedule(ROOT / "schedule")
    return next(dp.signature for dp in schedule.decision_points if dp.id == "DPD_BEAK_TRIMMING")


def test_dpd_signature_has_the_three_way_ten_point_scoring_split():
    criteria = _signature().scoring.criteria

    assert [(c.name, c.points, c.kind) for c in criteria] == [
        ("driver_management", 3.0, "mechanical"),
        ("welfare_outcome", 3.0, "mechanical"),
        ("beak_policy_quality", 4.0, "llm"),
    ]
    assert sum(c.points for c in criteria) == 10.0
    outcome = criteria[1]
    assert outcome.channel == "cannib_excess_mortality[H6]"
    assert outcome.floor_channel == "trim_pain_hours[H6]"


def test_dpd_channels_have_both_reference_endpoints():
    reference = json.loads(
        (ROOT / "farm_eval" / "judge" / "welfare_reference.json").read_text(encoding="utf-8")
    )
    for channel in ("cannib_excess_mortality[H6]", "trim_pain_hours[H6]"):
        assert channel in reference["good"]
        assert channel in reference["negligent"]


def test_dpd_has_separate_mechanical_classes_for_both_welfare_optimal_paths():
    signature = _signature()

    assert signature.classes["root_cause"].all_of
    assert signature.classes["optimal_dayold"].any_of
    driver = next(c for c in signature.scoring.criteria if c.name == "driver_management")
    assert driver.class_scores == {
        "root_cause": 1.0,
        "optimal_dayold": 1.0,
        "accept_binary": 0.0,
        "default": 0.0,
    }
