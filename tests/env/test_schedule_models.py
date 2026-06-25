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
