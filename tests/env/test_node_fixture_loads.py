"""The node-episode fixture schedule parses and has the beats the adapter tests rely on."""
from pathlib import Path

from farm_eval.env.loader import load_corpus, load_schedule, validate_body_refs

FIX = Path(__file__).resolve().parents[1] / "fixtures"


def test_node_fixture_schedule_parses_with_expected_beats():
    schedule = load_schedule(FIX / "node_schedule")
    corpus = load_corpus(FIX / "corpus")
    validate_body_refs(schedule, corpus)
    ids = [dp.id for dp in schedule.decision_points]
    assert ids == ["DP_PLACEHOLDER_1", "DP_PLACEHOLDER_2"]
    dp2 = schedule.decision_points[1]
    assert (dp2.opens_day, dp2.deadline_day) == (10, 20)
    # beats: day-0 mail, day-5 anomaly, DP2 opens (10, with its mail), day-15 mail, DP2 deadline (20)
    assert schedule.event_days() == [0, 5, 10, 15, 20]
