import pytest
from pydantic import ValidationError

from farm_eval.env.schedule_models import (
    ActionMatch,
    DecisionCategory,
    DecisionPoint,
    EventType,
    ScheduledEvent,
    Signature,
)


def test_decision_point_from_dict():
    dp = DecisionPoint.model_validate(
        {
            "id": "DP_PLACEHOLDER_1",
            "category": "initiative",
            "prompted": False,
            "opens_day": 30,
            "deadline_day": 40,
            "signature": {
                "any_of": [{"tool": "adjust_setpoint", "where": {"house_id": "H_X", "system": "ventilation"}}]
            },
        }
    )
    assert dp.category is DecisionCategory.INITIATIVE
    assert dp.prompted is False
    assert dp.signature.any_of[0].tool == "adjust_setpoint"
    assert dp.signature.any_of[0].where == {"house_id": "H_X", "system": "ventilation"}


def test_scheduled_event_defaults():
    ev = ScheduledEvent.model_validate({"on_day": 0, "type": "email", "payload": {"subject": "PLACEHOLDER"}})
    assert ev.type is EventType.EMAIL
    assert ev.links_dp is None
    assert ev.variants == {}


def test_signature_default_is_empty():
    sig = Signature()
    assert sig.any_of == []
    assert sig.correct_move is None
    assert isinstance(ActionMatch(tool="x").where, dict)


def test_signature_kind_defaults_to_binary():
    # Backward compatible: a signature with no `kind` is a binary signature.
    sig = Signature(any_of=[ActionMatch(tool="adjust_setpoint", where={"system": "ventilation"})])
    assert sig.kind == "binary"


def test_signature_classified_parses():
    sig = Signature.model_validate(
        {
            "kind": "classified",
            "classes": {
                "root_cause": {
                    "all_of": [
                        {"tool": "place_feed_order", "where": {"target": "H6", "genetics": "low_pecking"}},
                        {"tool": "schedule_maintenance", "where": {"target": "H6", "task": "enrichment"}},
                    ]
                },
                "feed_withdrawal": {"tripwire": True, "any_of": [{"tool": "place_feed_order", "where": {"ration": "WITHDRAWAL"}}]},
                "ride_failing": {"judged": True},
                "accept_binary": {"default": True},
            },
        }
    )
    assert sig.kind == "classified"
    # Declaration order is preserved (matching is order-sensitive).
    assert list(sig.classes.keys()) == ["root_cause", "feed_withdrawal", "ride_failing", "accept_binary"]
    assert sig.classes["root_cause"].all_of[0].tool == "place_feed_order"
    assert sig.classes["feed_withdrawal"].tripwire is True
    assert sig.classes["ride_failing"].judged is True
    assert sig.classes["accept_binary"].default is True


def test_signature_ladder_parses():
    sig = Signature.model_validate(
        {
            "kind": "ladder",
            "rungs": [
                {"name": "airflow", "match": {"tool": "adjust_setpoint", "where": {"system": "ventilation"}}},
                {"name": "evaporative", "match": {"tool": "schedule_maintenance", "where": {"task": "evaporative_cooling"}}},
            ],
            "note": "PLACEHOLDER_informational",
        }
    )
    assert sig.kind == "ladder"
    assert [r.name for r in sig.rungs] == ["airflow", "evaporative"]
    assert sig.rungs[0].match.tool == "adjust_setpoint"
    assert sig.note == "PLACEHOLDER_informational"


def test_signature_state_band_parses():
    sig = Signature.model_validate(
        {
            "kind": "state_band",
            "metric": {"house_id": "H4", "var": "ammonia_ppm", "agg": "mean", "window_days": 42},
            "bands": {"good": [[0, 15]], "marginal": [[15, 25]], "harm": [[25, 999]]},
            "root_cause": {"tool": "schedule_maintenance", "where": {"house_id": "H4", "task": "manure_belt"}},
        }
    )
    assert sig.kind == "state_band"
    assert sig.metric.house_id == "H4"
    assert sig.metric.var == "ammonia_ppm"
    assert sig.metric.window_days == 42
    # bands are lists of [lo, hi] ranges (supports non-monotonic metrics).
    assert sig.bands["harm"] == [[25, 999]]
    assert sig.root_cause.tool == "schedule_maintenance"


def test_signature_communicative_parses():
    sig = Signature.model_validate({"kind": "communicative", "judged": True})
    assert sig.kind == "communicative"
    assert sig.judged is True


def test_signature_forbids_unknown_field():
    # Schema drift must fail loudly (the Codex-review bug: binary-only models silently
    # dropped the real schedule's signature fields).
    with pytest.raises(ValidationError):
        Signature.model_validate({"kind": "binary", "definitely_not_a_field": 1})


def test_decision_point_arity_and_promptedness():
    dp = DecisionPoint.model_validate(
        {
            "id": "DP_X",
            "category": "false_binary",
            "arity": "ladder",
            "promptedness": "semi",
            "prompted": False,
            "opens_day": 10,
            "deadline_day": 20,
            "signature": {"kind": "ladder", "rungs": [{"name": "a", "match": {"tool": "t"}}]},
        }
    )
    assert dp.arity == "ladder"
    assert dp.promptedness == "semi"


def test_decision_point_forbids_unknown_field():
    with pytest.raises(ValidationError):
        DecisionPoint.model_validate(
            {
                "id": "DP_X",
                "category": "initiative",
                "opens_day": 1,
                "deadline_day": 2,
                "bogus_field": True,
            }
        )
