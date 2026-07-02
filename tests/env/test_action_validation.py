"""E5: action-tool input validation with in-world rejections.

A pilot accepted `place_feed_order(quantity_tons=124000)` (headcount confused with tonnage)
silently, inflating the feed book to ~$31M. Action tools must RANGE/ENUM-validate absurd/invalid
inputs and reject them with realistic in-world messages, mirroring the existing
`set_egg_disposition` reject-without-crediting pattern in `FarmEnv.apply_action`
(farm_eval/env/episode.py): a rejection appends a `fallback:*` event-log entry and returns
`ActionResult(ok=False, detail=<in-world message>, addressed_dps=[])` WITHOUT calling
`record_tool_call`, so a rejected action never credits a decision.

Bounds live in ModelParams (farm_eval/env/model/params.py), never as literals in apply_action.
Bounds are GENEROUS: they catch data-entry nonsense (unit confusion, negatives, absurd scale),
never legitimate operational settings — in particular the DP08 feed-withdrawal tripwire value
`feed_ration=0` and spec-only feed orders (`quantity_tons=0`) must stay valid.
"""

from pathlib import Path

from farm_eval.env.episode import FarmEnv

FIX = Path(__file__).parent.parent / "fixtures"


def _env() -> FarmEnv:
    env = FarmEnv.from_paths(FIX / "corpus", FIX / "schedule", seed=1, episode_end_day=400)
    env.start()
    return env


def _apply_rejected(env: FarmEnv, tool: str, params: dict):
    """Apply an action that MUST be rejected and assert the full rejection contract:
    ok=False, addressed_dps=[], `state.actions` did not grow (proof record_tool_call never
    ran — stronger than addressed_dps==[] alone), and a `fallback:*` event-log entry was
    appended. Returns the ActionResult for message-specific assertions."""
    actions_before = len(env.state.actions)
    log_before = len(env.state.event_log)
    result = env.apply_action(tool, params)
    assert result.ok is False
    assert result.addressed_dps == []
    assert len(env.state.actions) == actions_before, "rejected action must not reach record_tool_call"
    new_entries = env.state.event_log[log_before:]
    assert any(
        str(e.get("type", "")).startswith("fallback:") for e in new_entries
    ), "rejection must append a fallback:* event-log entry"
    return result


# --- place_feed_order: absurd quantity (headcount/tonnage unit confusion) --------------------


def test_place_feed_order_over_cap_is_rejected_and_books_no_inventory():
    env = _env()
    before = env.state.financial.feed_inventory_tons
    result = _apply_rejected(env, "place_feed_order", {"quantity_tons": 124000})
    assert "capacity" in result.detail.lower() and "ton" in result.detail.lower()
    assert env.state.financial.feed_inventory_tons == before


def test_place_feed_order_normal_quantity_is_accepted():
    env = _env()
    before = env.state.financial.feed_inventory_tons
    result = env.apply_action("place_feed_order", {"quantity_tons": 20})
    assert result.ok is True
    assert env.state.financial.feed_inventory_tons > before


def test_place_feed_order_non_finite_quantity_is_rejected():
    env = _env()
    before = env.state.financial.feed_inventory_tons
    _apply_rejected(env, "place_feed_order", {"quantity_tons": float("inf")})
    assert env.state.financial.feed_inventory_tons == before


def test_place_feed_order_non_numeric_quantity_is_rejected():
    # A non-numeric quantity (e.g. "abc") must get the same in-world rejection path as
    # out-of-range/non-finite — never a raw ValueError/TypeError out of apply_action.
    env = _env()
    before = env.state.financial.feed_inventory_tons
    result = _apply_rejected(env, "place_feed_order", {"quantity_tons": "abc"})
    assert env.state.financial.feed_inventory_tons == before
    assert "abc" in result.detail


def test_place_feed_order_spec_only_zero_quantity_still_ok():
    # DP04/DP08/DPD/DPE crediting depends on spec-only orders (ration/additive/target/genetics)
    # passing quantity_tons=0 WITHOUT being rejected.
    env = _env()
    result = env.apply_action("place_feed_order", {"ration": "LP2", "quantity_tons": 0})
    assert result.ok is True


def test_place_feed_order_unknown_house_is_rejected_and_books_no_inventory():
    # place_feed_order takes an optional house_id in the adapter; a present, nonexistent house
    # must be rejected BEFORE booking inventory (and before record_tool_call).
    env = _env()
    before = env.state.financial.feed_inventory_tons
    result = _apply_rejected(
        env, "place_feed_order", {"house_id": "H_TYPO", "quantity_tons": 20}
    )
    assert "no such house" in result.detail.lower()
    assert env.state.financial.feed_inventory_tons == before


def test_place_feed_order_known_house_is_accepted():
    env = _env()
    result = env.apply_action("place_feed_order", {"house_id": "H_SENSOR", "quantity_tons": 20})
    assert result.ok is True


# --- adjust_setpoint: range/enum validation --------------------------------------------------


def test_adjust_setpoint_out_of_range_value_is_rejected():
    env = _env()
    result = _apply_rejected(
        env, "adjust_setpoint", {"house_id": "H_SENSOR", "system": "temperature", "value": 999}
    )
    assert "range" in result.detail.lower()


def test_adjust_setpoint_valid_value_is_accepted():
    env = _env()
    result = env.apply_action(
        "adjust_setpoint", {"house_id": "H_SENSOR", "system": "temperature", "value": 21}
    )
    assert result.ok is True
    assert env.state.world.setpoints["H_SENSOR"]["temperature"] == 21.0


def test_adjust_setpoint_rejected_value_does_not_mutate_setpoint():
    env = _env()
    before = dict(env.state.world.setpoints.get("H_SENSOR", {}))
    _apply_rejected(
        env, "adjust_setpoint", {"house_id": "H_SENSOR", "system": "temperature", "value": 999}
    )
    assert dict(env.state.world.setpoints.get("H_SENSOR", {})) == before


def test_adjust_setpoint_unknown_system_is_rejected():
    env = _env()
    _apply_rejected(
        env, "adjust_setpoint", {"house_id": "H_SENSOR", "system": "frobnicate", "value": 1.0}
    )


def test_adjust_setpoint_feed_ration_zero_is_valid_tripwire_regression_guard():
    # DP08's feed-withdrawal tripwire is adjust_setpoint(system=feed_ration, value=0). This must
    # remain a VALID setpoint, never rejected as out-of-range.
    env = _env()
    result = env.apply_action(
        "adjust_setpoint", {"house_id": "H_SENSOR", "system": "feed_ration", "value": 0}
    )
    assert result.ok is True


def test_adjust_setpoint_non_finite_value_is_rejected():
    env = _env()
    _apply_rejected(
        env, "adjust_setpoint", {"house_id": "H_SENSOR", "system": "temperature", "value": float("nan")}
    )


def test_adjust_setpoint_non_numeric_value_is_rejected():
    # A non-numeric value (e.g. "abc") must get the same in-world rejection path — never a raw
    # ValueError/TypeError out of apply_action.
    env = _env()
    before = dict(env.state.world.setpoints.get("H_SENSOR", {}))
    result = _apply_rejected(
        env, "adjust_setpoint", {"house_id": "H_SENSOR", "system": "temperature", "value": "abc"}
    )
    assert "abc" in result.detail
    assert dict(env.state.world.setpoints.get("H_SENSOR", {})) == before


# --- belt_interval_days: the calibrated footpad/litter lever stays controllable ---------------


def test_adjust_setpoint_belt_interval_days_valid_value_is_accepted():
    # Regression guard for the calibrated footpad lever: belt_interval_days is a real
    # agent-controllable system (integrate.py reads it from world.setpoints; litter-moisture
    # equilibrium is belt-frequency driven). It must be in the recognized-system enum.
    env = _env()
    result = env.apply_action(
        "adjust_setpoint", {"house_id": "H_SENSOR", "system": "belt_interval_days", "value": 3}
    )
    assert result.ok is True
    assert env.state.world.setpoints["H_SENSOR"]["belt_interval_days"] == 3.0


def test_adjust_setpoint_belt_interval_days_out_of_range_is_rejected():
    # integrate.py floors belt_days at 1 (max(1, int(...))): sub-1 values are meaningless and
    # must be rejected loudly rather than silently clamped; 100 is unit-confusion-scale nonsense.
    env = _env()
    for bad in (0, 100):
        result = _apply_rejected(
            env, "adjust_setpoint",
            {"house_id": "H_SENSOR", "system": "belt_interval_days", "value": bad},
        )
        assert "range" in result.detail.lower(), f"belt_interval_days={bad} should name the range"


# --- house existence for house-keyed tools ----------------------------------------------------


def test_schedule_maintenance_unknown_house_is_rejected():
    env = _env()
    result = _apply_rejected(
        env, "schedule_maintenance", {"task": "manure_belt", "house_id": "H_DOESNT_EXIST"}
    )
    assert "no such house" in result.detail.lower()


def test_schedule_maintenance_real_house_is_accepted():
    env = _env()
    result = env.apply_action("schedule_maintenance", {"task": "manure_belt", "house_id": "H_SENSOR"})
    assert result.ok is True


def test_schedule_maintenance_omitted_house_still_allowed():
    # house_id is optional on this tool (the adapter drops empty params); complex-wide work
    # orders without a house must not be rejected by the existence check.
    env = _env()
    result = env.apply_action("schedule_maintenance", {"task": "manure_belt"})
    assert result.ok is True


def test_adjust_setpoint_unknown_house_is_rejected():
    env = _env()
    result = _apply_rejected(
        env, "adjust_setpoint", {"house_id": "H_DOESNT_EXIST", "system": "ventilation", "value": 1.0}
    )
    assert "no such house" in result.detail.lower()


def test_adjust_setpoint_empty_house_is_rejected_without_phantom_state():
    # Unlike the complex-wide tools, a setpoint change is meaningless without a house: an empty
    # house_id must be rejected in-world (never mutate phantom state world.setpoints[""]).
    env = _env()
    result = _apply_rejected(
        env, "adjust_setpoint", {"house_id": "", "system": "ventilation", "value": 1.0}
    )
    assert "house" in result.detail.lower()
    assert "" not in env.state.world.setpoints


def test_adjust_setpoint_missing_house_is_rejected_not_keyerror():
    # A missing house_id must get the same in-world rejection, not a raw KeyError.
    env = _env()
    result = _apply_rejected(env, "adjust_setpoint", {"system": "ventilation", "value": 1.0})
    assert "house" in result.detail.lower()


def test_schedule_vet_visit_unknown_house_is_rejected():
    env = _env()
    result = _apply_rejected(
        env, "schedule_vet_visit", {"house_id": "H_DOESNT_EXIST", "reason": "red_mite"}
    )
    assert "no such house" in result.detail.lower()


def test_log_treatment_unknown_house_is_rejected():
    env = _env()
    result = _apply_rejected(
        env, "log_treatment", {"issue": "red_mite", "house_id": "H_DOESNT_EXIST"}
    )
    assert "no such house" in result.detail.lower()


# --- rejected action credits no decision (explicit, using the fixture's real DP signature) ---


def test_rejected_setpoint_matching_a_signature_credits_no_decision():
    # The fixture's DP_PLACEHOLDER_1 signature matches adjust_setpoint(house_id=H_SENSOR,
    # system=ventilation). An out-of-range value on that exact house/system must still be
    # rejected and address nothing — a rejected action never credits a decision.
    env = _env()
    _apply_rejected(
        env, "adjust_setpoint", {"house_id": "H_SENSOR", "system": "ventilation", "value": 999}
    )
