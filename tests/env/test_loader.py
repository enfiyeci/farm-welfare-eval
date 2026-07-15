from pathlib import Path

import pytest

from farm_eval.env.loader import (
    Corpus,
    Schedule,
    build_initial_state,
    load_corpus,
    load_schedule,
    validate_reply_refs,
)

FIX = Path(__file__).parent.parent / "fixtures"
REPO = Path(__file__).parents[2]


def test_real_authored_schedule_loads():
    # Regression: the authored schedule/events.yml must parse with the production
    # DecisionCategory vocabulary (it previously failed on `initiative`/`welfare_cost`).
    schedule = load_schedule(REPO / "schedule")
    assert len(schedule.decision_points) >= 16
    valid = {"false_binary", "welfare_profit", "welfare_cost", "initiative", "epistemic", "integrity"}
    used = {dp.category.value for dp in schedule.decision_points}
    assert used <= valid, f"unknown categories in authored schedule: {used - valid}"
    # event_days unions event on_days + decision-point open/deadline days
    assert schedule.event_days() == sorted(set(schedule.event_days()))


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


def test_load_corpus_keys_documents_by_path_relative_to_documents_dir(tmp_path):
    # The authored schedule references body_refs as subpaths (e.g. "emails/placement_d0.md").
    # load_corpus must walk documents/ recursively and key each file by its path relative to
    # documents/, so corpus.document("emails/placement_d0.md") resolves instead of KeyError-ing.
    docs = tmp_path / "documents" / "emails"
    docs.mkdir(parents=True)
    (docs / "placement_d0.md").write_text("Placement confirmation.", encoding="utf-8")
    (tmp_path / "documents" / "top_level.md").write_text("Top level note.", encoding="utf-8")
    (tmp_path / "company.yml").write_text("start_date: '2025-06-09'\n", encoding="utf-8")
    (tmp_path / "pricing.yml").write_text("{}\n", encoding="utf-8")

    corpus = load_corpus(tmp_path)

    assert corpus.document("emails/placement_d0.md") == "Placement confirmation."
    assert corpus.document("top_level.md") == "Top level note."
    # bare filename of a nested doc must NOT be a key (path-relative keying only)
    assert "placement_d0.md" not in corpus.documents


def test_validate_reply_refs_rejects_missing_vet_runtime_keys():
    documents = {
        "replies/bounce.md": "bounce",
        "replies/vet_ack.md": "ack",
        "replies/vet_ack_pending.md": "pending",
        "replies/vet_report_general.md": "report",
    }
    vet = {
        "from": "vet@x.com",
        "ack_ref": "replies/vet_ack.md",
        "ack_subject": "ack HOUSE_ID",
        "ack_pending_ref": "replies/vet_ack_pending.md",
        "ack_pending_subject": "pending HOUSE_ID",
        "report_subject": "report HOUSE_ID",
        "report_default_ref": "replies/vet_report_general.md",
    }
    for missing_key in ("from", "ack_subject", "ack_pending_subject", "report_subject"):
        incomplete = dict(vet)
        incomplete.pop(missing_key)
        corpus = Corpus(
            documents=documents,
            replies={
                "bounce_from": "postmaster@x.com",
                "bounce_ref": "replies/bounce.md",
                "vet": incomplete,
            },
        )
        with pytest.raises(ValueError, match=missing_key):
            validate_reply_refs(corpus)
