from pathlib import Path

from farm_eval.env.events import open_due_decision_points
from farm_eval.env.ledger import LedgerStatus
from farm_eval.env.loader import build_initial_state, load_corpus, load_schedule
from farm_eval.env.tracker import match_signature, match_where, record_tool_call
from farm_eval.env.schedule_models import ActionMatch, Signature

FIX = Path(__file__).parent.parent / "fixtures"


def test_match_where_is_subset():
    assert match_where({"house_id": "H_SENSOR", "system": "ventilation", "value": 2}, {"house_id": "H_SENSOR", "system": "ventilation"})
    assert not match_where({"house_id": "H_SENSOR"}, {"house_id": "H_OTHER"})


def test_match_signature_any_of():
    sig = Signature(any_of=[ActionMatch(tool="adjust_setpoint", where={"system": "ventilation"})])
    assert match_signature(sig, "adjust_setpoint", {"system": "ventilation", "house_id": "H_SENSOR"})
    assert not match_signature(sig, "place_feed_order", {"system": "ventilation"})


def test_record_tool_call_addresses_unprompted_dp():
    state = build_initial_state(load_corpus(FIX / "corpus"))
    schedule = load_schedule(FIX / "schedule")
    open_due_decision_points(state, schedule, day=0)

    addressed = record_tool_call(
        state, schedule, "adjust_setpoint", {"house_id": "H_SENSOR", "system": "ventilation", "value": 2.5}, day=2
    )
    assert addressed == ["DP_PLACEHOLDER_1"]
    entry = state.ledger[0]
    assert entry.status is LedgerStatus.ADDRESSED
    assert entry.noticed_unprompted is True  # DP_PLACEHOLDER_1 has prompted=false
    assert entry.agent_action.tool == "adjust_setpoint"
    assert entry.agent_action.day == 2
    # idempotent: a second matching call does not re-address
    assert record_tool_call(state, schedule, "adjust_setpoint", {"house_id": "H_SENSOR", "system": "ventilation"}, day=3) == []


def test_record_tool_call_no_match_returns_empty():
    state = build_initial_state(load_corpus(FIX / "corpus"))
    schedule = load_schedule(FIX / "schedule")
    open_due_decision_points(state, schedule, day=0)
    assert record_tool_call(state, schedule, "place_feed_order", {"quantity_tons": 10}, day=1) == []
