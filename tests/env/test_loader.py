from pathlib import Path

from farm_eval.env.loader import Corpus, Schedule, build_initial_state, load_corpus, load_schedule

FIX = Path(__file__).parent.parent / "fixtures"


def test_load_corpus_and_document():
    corpus = load_corpus(FIX / "corpus")
    assert corpus.company["start_date"] == "2025-06-09"
    assert "PLACEHOLDER_doc.md" in corpus.documents
    assert corpus.document("PLACEHOLDER_doc.md").startswith("PLACEHOLDER")


def test_load_schedule_event_days_sorted():
    schedule = load_schedule(FIX / "schedule")
    assert [dp.id for dp in schedule.decision_points] == ["DP_PLACEHOLDER_1"]
    assert schedule.event_days() == [0, 5]


def test_build_initial_state_from_corpus():
    corpus = load_corpus(FIX / "corpus")
    state = build_initial_state(corpus, seed=7)
    assert state.seed == 7
    assert state.start_date == "2025-06-09"
    assert state.nh3_sensor_houses == ["H_SENSOR"]
    assert state.world.bird_count["H_SENSOR"] == 1000
    assert state.welfare.houses["H_SENSOR"].ammonia_ppm == 8.0
    assert state.world.setpoints["H_SENSOR"]["ventilation"] == 1.0
