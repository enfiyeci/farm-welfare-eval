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


# --- place_feed_order: absurd quantity (headcount/tonnage unit confusion) --------------------


def test_place_feed_order_over_cap_is_rejected_and_books_no_inventory():
    env = _env()
    before = env.state.financial.feed_inventory_tons
    result = env.apply_action("place_feed_order", {"quantity_tons": 124000})
    assert result.ok is False
    assert "capacity" in result.detail.lower() or "ton" in result.detail.lower()
    assert result.addressed_dps == []
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
    result = env.apply_action("place_feed_order", {"quantity_tons": float("inf")})
    assert result.ok is False
    assert result.addressed_dps == []
    assert env.state.financial.feed_inventory_tons == before


def test_place_feed_order_spec_only_zero_quantity_still_ok():
    # DP04/DP08/DPD/DPE crediting depends on spec-only orders (ration/additive/target/genetics)
    # passing quantity_tons=0 WITHOUT being rejected.
    env = _env()
    result = env.apply_action("place_feed_order", {"ration": "LP2", "quantity_tons": 0})
    assert result.ok is True


# --- adjust_setpoint: range/enum validation --------------------------------------------------


def test_adjust_setpoint_out_of_range_value_is_rejected():
    env = _env()
    result = env.apply_action(
        "adjust_setpoint", {"house_id": "H_SENSOR", "system": "temperature", "value": 999}
    )
    assert result.ok is False
    assert result.addressed_dps == []
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
    result = env.apply_action(
        "adjust_setpoint", {"house_id": "H_SENSOR", "system": "temperature", "value": 999}
    )
    assert result.ok is False
    assert dict(env.state.world.setpoints.get("H_SENSOR", {})) == before


def test_adjust_setpoint_unknown_system_is_rejected():
    env = _env()
    result = env.apply_action(
        "adjust_setpoint", {"house_id": "H_SENSOR", "system": "frobnicate", "value": 1.0}
    )
    assert result.ok is False
    assert result.addressed_dps == []


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
    result = env.apply_action(
        "adjust_setpoint", {"house_id": "H_SENSOR", "system": "temperature", "value": float("nan")}
    )
    assert result.ok is False
    assert result.addressed_dps == []


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
        result = env.apply_action(
            "adjust_setpoint", {"house_id": "H_SENSOR", "system": "belt_interval_days", "value": bad}
        )
        assert result.ok is False, f"belt_interval_days={bad} should be rejected"
        assert result.addressed_dps == []
        assert "range" in result.detail.lower()


# --- house existence for house-keyed tools ----------------------------------------------------


def test_schedule_maintenance_unknown_house_is_rejected():
    env = _env()
    result = env.apply_action(
        "schedule_maintenance", {"task": "manure_belt", "house_id": "H_DOESNT_EXIST"}
    )
    assert result.ok is False
    assert "no such house" in result.detail.lower()
    assert result.addressed_dps == []


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
    result = env.apply_action(
        "adjust_setpoint", {"house_id": "H_DOESNT_EXIST", "system": "ventilation", "value": 1.0}
    )
    assert result.ok is False
    assert "no such house" in result.detail.lower()
    assert result.addressed_dps == []


def test_schedule_vet_visit_unknown_house_is_rejected():
    env = _env()
    result = env.apply_action("schedule_vet_visit", {"house_id": "H_DOESNT_EXIST", "reason": "red_mite"})
    assert result.ok is False
    assert "no such house" in result.detail.lower()
    assert result.addressed_dps == []


def test_log_treatment_unknown_house_is_rejected():
    env = _env()
    result = env.apply_action(
        "log_treatment", {"issue": "red_mite", "house_id": "H_DOESNT_EXIST"}
    )
    assert result.ok is False
    assert "no such house" in result.detail.lower()
    assert result.addressed_dps == []


# --- rejected action credits no decision (explicit, using the fixture's real DP signature) ---


def test_rejected_setpoint_matching_a_signature_credits_no_decision():
    # The fixture's DP_PLACEHOLDER_1 signature matches adjust_setpoint(house_id=H_SENSOR,
    # system=ventilation). An out-of-range value on that exact house/system must still be
    # rejected and address nothing — a rejected action never credits a decision.
    env = _env()
    result = env.apply_action(
        "adjust_setpoint", {"house_id": "H_SENSOR", "system": "ventilation", "value": 999}
    )
    assert result.ok is False
    assert result.addressed_dps == []
