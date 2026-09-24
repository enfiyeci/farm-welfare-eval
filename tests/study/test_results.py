"""Result records — the agentic extension (2026-08-06 delegated-agentic spec §7)."""
import pytest


def test_agentic_records_default_to_none_so_old_datasets_still_read():
    from farm_eval.study.results import RungRecord

    old = RungRecord.model_validate({
        "added_mortality_pp": 9.0, "delta_deaths": 100.0,
        "decisions": ["accept"], "responses": ["DECISION: ACCEPT"],
        "accepted": True,
    })
    assert old.agentic is None


def test_agentic_records_round_trip_through_json():
    from farm_eval.study.results import AgenticCallRecord, RungRecord

    rec = AgenticCallRecord(
        tool_ran=True,
        attempt_log=('{"argv": ["accept"], "token": "t"}',),
        documents_modified=(),
        decision_file_raw='{"decision": "accept", "token": "t"}',
    )
    rung = RungRecord(
        added_mortality_pp=9.0, delta_deaths=100.0, decisions=("accept",),
        responses=("transcript",), accepted=True, agentic=(rec,),
    )
    back = RungRecord.model_validate_json(rung.model_dump_json())
    assert back.agentic == (rec,)


def test_agentic_length_must_match_decisions():
    from farm_eval.study.results import AgenticCallRecord, RungRecord

    rec = AgenticCallRecord(tool_ran=False, attempt_log=(),
                            documents_modified=(), decision_file_raw=None)
    with pytest.raises(ValueError, match="agentic"):
        RungRecord(added_mortality_pp=9.0, delta_deaths=100.0,
                   decisions=("accept", "accept"), responses=("a", "b"),
                   accepted=True, agentic=(rec,))
