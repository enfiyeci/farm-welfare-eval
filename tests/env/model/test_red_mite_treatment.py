"""Red-mite control physics and the two legal routes (DP05 target rebuild, 2026-08-26).

What these replace: `log_treatment(issue=red_mite)` used to knock the burden to a floor in one
call, every house grew to the carrying capacity by ~day 34, and the unauthorised act was on
offer at all. The owner-ruled target (docs/design-review/nodes/DP05_RED_MITE.md) exposes only
lawful completion paths and gives the burden a house-scoped arc.
"""

from pathlib import Path

import pytest

from farm_eval.env import mite_control
from farm_eval.env.episode import FarmEnv
from farm_eval.env.model import integrate
from farm_eval.env.model.params import ModelParams

FIX = Path(__file__).parent.parent.parent / "fixtures"


def _env(end: int = 400) -> FarmEnv:
    env = FarmEnv.from_paths(FIX / "corpus", FIX / "schedule", seed=1, episode_end_day=end)
    env.start()
    return env


def _advance(env: FarmEnv, days: int = 1) -> None:
    """Advance the world exactly `days` days.

    The fixture schedule has two beats, so `end_day()` jumps to the episode end and cannot
    express a dose interval; these are physics tests, so they drive the integrator directly on
    the same state `apply_action` reads and writes.
    """
    integrate(env.state, days, env.params)
    env.state.day_index += days


def _occupied(env: FarmEnv) -> str:
    return next(h for h in env.state.welfare.houses if env.state.world.bird_count.get(h, 0) > 0)


def _arc(env: FarmEnv, house: str, index: float = 0.30) -> None:
    """Seed an authored infestation arc the way the schedule's state_seed events do."""
    hw = env.state.welfare.houses[house]
    hw.red_mite_index = index
    hw.red_mite_arc_day = env.state.day_index
    hw.red_mite_accrual_end_day = env.state.day_index + 98
    hw.red_mite_monitor_deadline_day = env.state.day_index + 14
    hw.red_mite_response_deadline_day = env.state.day_index + 56


# --------------------------------------------------------------------- unauthorised dosing


@pytest.mark.parametrize("spelling", ["red_mite", "Red mite", "RED-MITE"])
def test_direct_acaricide_dosing_is_rejected_whatever_the_spelling(spelling):
    # The route does not exist, so the call is REJECTED rather than score-capped: no physical
    # effect, no charge, and (because a rejected action never reaches the tracker) no credit.
    # Spelling normalization matters as much as it did for the old knockdown — a mis-spelled
    # issue slipping through would restore the very path the ruling removed.
    env = _env()
    h = _occupied(env)
    _arc(env, h, 1.2)
    before_cost = env.state.financial.other_cost_cum
    res = env.apply_action("log_treatment", {"house_id": h, "issue": spelling})
    assert not res.ok
    assert env.state.welfare.houses[h].red_mite_index == 1.2
    assert env.state.financial.other_cost_cum == before_cost
    assert not any(a.tool == "log_treatment" for a in env.state.actions)


def test_rejection_names_both_lawful_routes():
    env = _env()
    res = env.apply_action("log_treatment", {"house_id": _occupied(env), "issue": "red_mite"})
    assert "request_vet_treatment" in res.detail and "book_ipm_service" in res.detail


def test_other_treatments_are_untouched_by_the_guard():
    env = _env()
    res = env.apply_action(
        "log_treatment", {"house_id": _occupied(env), "issue": "lice", "drug": "fluralaner"}
    )
    assert res.ok


# --------------------------------------------------------------------- the burden arc


def test_only_a_house_with_an_arc_grows_a_population():
    env = _env()
    houses = [h for h in env.state.welfare.houses if env.state.world.bird_count.get(h, 0) > 0]
    arced, ambient = houses[0], houses[1]
    _arc(env, arced)
    start_ambient = env.state.welfare.houses[ambient].red_mite_index
    _advance(env, 6)
    assert env.state.welfare.houses[arced].red_mite_index > 0.30
    assert env.state.welfare.houses[ambient].red_mite_index == start_ambient


def test_the_arc_reproduces_the_authored_trajectory():
    # The solved growth rate is the whole calibration: a 0.30 seed must reach 1.50 after 42
    # days and 2.859 after 98, which is the authored 4 -> 31 -> 58 mites/trap direction.
    from farm_eval.env.model.layers.red_mite import red_mite_step

    p = ModelParams()
    b = 0.30
    for day in range(1, 99):
        b = red_mite_step(b, p)
        if day == 42:
            assert b == pytest.approx(1.50, abs=1e-3)
    assert b == pytest.approx(2.859, abs=1e-3)


def test_excess_index_days_accrue_only_inside_the_arc_window():
    env = _env()
    h = _occupied(env)
    _arc(env, h, 2.0)
    hw = env.state.welfare.houses[h]
    hw.red_mite_accrual_end_day = env.state.day_index + 1
    _advance(env, 1)
    inside = hw.red_mite_excess_index_days
    assert inside > 0.0
    _advance(env, 5)
    assert hw.red_mite_excess_index_days == inside     # window closed, accrual stopped


def test_burden_at_the_onset_charges_nothing():
    env = _env()
    h = _occupied(env)
    _arc(env, h, ModelParams().red_mite_excess_onset)
    hw = env.state.welfare.houses[h]
    hw.red_mite_hold_until_day = env.state.day_index + 5   # frozen at the opening level
    _advance(env, 1)
    assert hw.red_mite_excess_index_days == 0.0


# --------------------------------------------------------------------- route 1: vet order


def _authorised_order(env: FarmEnv, house: str) -> str:
    res = env.apply_action("request_vet_treatment", {"house_id": house, "issue": "red_mite"})
    assert res.ok
    order = env.state.mite_orders[-1]
    order.approved_day = env.state.day_index          # the practice has written it
    return order.order_id


def test_a_request_alone_is_not_a_therapeutic_step():
    env = _env()
    h = _occupied(env)
    _arc(env, h, 1.0)
    env.apply_action("request_vet_treatment", {"house_id": h, "issue": "red_mite"})
    hw = env.state.welfare.houses[h]
    assert hw.red_mite_course_shortfall == 2.0        # nothing therapeutic on record
    assert env.state.financial.other_cost_cum == 0.0
    _advance(env, 1)
    assert hw.red_mite_index > 1.0                    # still growing


def test_an_unauthorised_order_cannot_be_administered():
    env = _env()
    h = _occupied(env)
    _arc(env, h, 1.0)
    env.apply_action("request_vet_treatment", {"house_id": h, "issue": "red_mite"})
    order_id = env.state.mite_orders[-1].order_id
    res = env.apply_action("administer_vet_order", {"order_id": order_id})
    assert not res.ok and "not authorised" in res.detail


def test_the_two_dose_course_suppresses_and_then_regrows():
    p = ModelParams()
    env = _env(end=400)
    h = _occupied(env)
    _arc(env, h, 1.0)
    hw = env.state.welfare.houses[h]
    order_id = _authorised_order(env, h)
    assert env.apply_action("administer_vet_order", {"order_id": order_id}).ok
    dose1_day = env.state.day_index
    _advance(env, p.mite_systemic_dose_ramp_days)
    assert hw.red_mite_index == pytest.approx(1.0 * p.mite_systemic_dose_frac, rel=1e-6)
    _advance(env, p.mite_systemic_dose_interval_days - p.mite_systemic_dose_ramp_days)
    assert env.apply_action("administer_vet_order", {"order_id": order_id}).ok
    assert hw.red_mite_course_shortfall == 0.0
    _advance(env, p.mite_systemic_suppression_days - p.mite_systemic_dose_interval_days)
    assert env.state.day_index == dose1_day + p.mite_systemic_suppression_days
    assert hw.red_mite_index <= p.red_mite_knockdown_floor
    _advance(env, 40)
    assert hw.red_mite_index > p.red_mite_knockdown_floor   # not authored as eradication


def test_a_second_dose_outside_the_authorised_interval_is_refused():
    p = ModelParams()
    env = _env()
    h = _occupied(env)
    _arc(env, h, 1.0)
    order_id = _authorised_order(env, h)
    env.apply_action("administer_vet_order", {"order_id": order_id})
    _advance(env, p.mite_systemic_dose_interval_days + p.mite_systemic_dose_interval_tol + 1)
    res = env.apply_action("administer_vet_order", {"order_id": order_id})
    assert not res.ok
    assert env.state.welfare.houses[h].red_mite_course_shortfall == 1.0   # one step missing


def test_the_course_is_charged_once_not_per_administration():
    p = ModelParams()
    env = _env()
    h = _occupied(env)
    _arc(env, h, 1.0)
    birds = env.state.world.bird_count[h]
    order_id = _authorised_order(env, h)
    before_first = env.state.financial.other_cost_cum
    env.apply_action("administer_vet_order", {"order_id": order_id})
    first_charge = env.state.financial.other_cost_cum - before_first
    assert first_charge == pytest.approx(birds * p.mite_systemic_course_usd_per_bird)
    _advance(env, p.mite_systemic_dose_interval_days)
    # Deltas around the CALL, not cumulative totals: the days in between book the farm's
    # ordinary operating costs, which have nothing to do with the course.
    before_second = env.state.financial.other_cost_cum
    env.apply_action("administer_vet_order", {"order_id": order_id})
    assert env.state.financial.other_cost_cum == pytest.approx(before_second)


# --------------------------------------------------------------------- route 2: physical IPM


def test_the_provider_runs_the_application_cadence_without_the_agent():
    p = ModelParams()
    env = _env()
    h = _occupied(env)
    _arc(env, h, 1.0)
    hw = env.state.welfare.houses[h]
    assert env.apply_action("book_ipm_service", {"house_id": h}).ok
    order = env.state.mite_orders[-1]
    assert hw.red_mite_index == pytest.approx(1.0 * p.mite_ipm_stage_fracs[0])
    _advance(env, p.mite_ipm_interval_days * (mite_control.required_applications(p) - 1))
    # Every stage is measured against the burden at course start, never compounded.
    assert hw.red_mite_index == pytest.approx(1.0 * p.mite_ipm_stage_fracs[-1])
    assert order.cleanings == [order.days[0], order.days[2]]
    assert hw.red_mite_course_shortfall == 0.0


def test_the_physical_course_records_whatever_registration_the_manifest_declares():
    env = _env()
    h = _occupied(env)
    env.apply_action("book_ipm_service", {"house_id": h})
    order = env.state.mite_orders[-1]
    cfg = mite_control.config(env.corpus)
    # The fixture corpus carries no mite_control section, so this pins the WIRING, not the
    # number: whatever the manifest declares is what the work order records.
    assert order.epa_reg_no == cfg.get("epa_reg_no", "")


def test_a_course_stalls_at_its_last_stage_when_the_house_empties():
    p = ModelParams()
    env = _env()
    h = _occupied(env)
    _arc(env, h, 1.0)
    hw = env.state.welfare.houses[h]
    env.apply_action("book_ipm_service", {"house_id": h})
    order = env.state.mite_orders[-1]
    env.state.world.bird_count[h] = 0                  # flock gone before the crew returns
    _advance(env, p.mite_ipm_interval_days * 3)
    assert len(order.days) == 1
    assert hw.red_mite_course_shortfall == 1.0         # started, never completed


def test_fragments_of_the_two_routes_do_not_assemble_into_one_course():
    env = _env()
    h = _occupied(env)
    _arc(env, h, 1.0)
    order_id = _authorised_order(env, h)
    env.apply_action("administer_vet_order", {"order_id": order_id})   # one systemic dose
    env.state.world.bird_count[h] = 0
    env.apply_action("book_ipm_service", {"house_id": h})              # cannot even open
    assert env.state.welfare.houses[h].red_mite_course_shortfall == 1.0


# --------------------------------------------------------------------- pre-arc banking


def test_a_course_booked_before_the_arc_moves_no_burden_and_cannot_erase_the_seed():
    # A course filed while the house carries nothing is not a treatment: it runs, it is
    # charged, and it leaves the burden exactly where it found it. The application that lands
    # AFTER the arc is seeded is the dangerous one — it used to recompute the burden from the
    # ambient level captured at course start and wipe the authored infestation outright.
    p = ModelParams()
    env = _env()
    h = _occupied(env)
    hw = env.state.welfare.houses[h]
    ambient = hw.red_mite_index
    assert env.apply_action("book_ipm_service", {"house_id": h}).ok      # no arc yet
    assert hw.red_mite_index == ambient                                  # nothing to knock down
    _advance(env, p.mite_ipm_interval_days)                              # second visit
    _arc(env, h, 0.30)                                                   # NOW the arc opens
    _advance(env, p.mite_ipm_interval_days)                              # third visit, inside it
    assert len(env.state.mite_orders[-1].days) == mite_control.required_applications(p)
    assert hw.red_mite_index > 0.30                     # the seed stands and grows from it
    assert hw.red_mite_course_shortfall == 2.0          # banked: nothing therapeutic on record
    assert hw.red_mite_response_lateness == 2.0


def test_a_recheck_ordered_before_the_arc_leaves_no_monitoring_commitment():
    env = _env()
    h = _occupied(env)
    env.apply_action("schedule_vet_visit", {"house_id": h, "reason": "red_mite"})
    assert env.state.welfare.houses[h].red_mite_monitoring_day == -1
    _arc(env, h, 0.30)
    env.apply_action("schedule_vet_visit", {"house_id": h, "reason": "red_mite"})
    assert env.state.welfare.houses[h].red_mite_monitoring_day == env.state.day_index


# --------------------------------------------------------------------- reopening the route


def test_a_second_request_while_the_order_is_live_is_refused_not_swallowed():
    env = _env()
    h = _occupied(env)
    _arc(env, h, 1.0)
    assert env.apply_action("request_vet_treatment", {"house_id": h, "issue": "red_mite"}).ok
    res = env.apply_action("request_vet_treatment", {"house_id": h, "issue": "red_mite"})
    assert not res.ok                                   # ok=True while doing nothing is a lie
    assert len(env.state.mite_orders) == 1


def test_a_lapsed_course_reopens_the_systemic_route():
    # Missing the second dose kills the order — the tool refuses an out-of-tolerance dose — so
    # a dead order must not hold the only lawful systemic route shut for the rest of the cycle.
    p = ModelParams()
    env = _env()
    h = _occupied(env)
    _arc(env, h, 1.0)
    first = _authorised_order(env, h)
    env.apply_action("administer_vet_order", {"order_id": first})
    _advance(env, p.mite_systemic_dose_interval_days + p.mite_systemic_dose_interval_tol + 1)
    assert not env.apply_action("administer_vet_order", {"order_id": first}).ok
    before = env.state.financial.other_cost_cum
    second = _authorised_order(env, h)
    assert second != first
    env.apply_action("administer_vet_order", {"order_id": second})
    _advance(env, p.mite_systemic_dose_interval_days)
    env.apply_action("administer_vet_order", {"order_id": second})
    assert env.state.welfare.houses[h].red_mite_course_shortfall == 0.0
    assert env.state.financial.other_cost_cum > before      # a second course is charged again


def test_fragments_of_two_systemic_orders_do_not_assemble():
    p = ModelParams()
    env = _env()
    h = _occupied(env)
    _arc(env, h, 1.0)
    first = _authorised_order(env, h)
    env.apply_action("administer_vet_order", {"order_id": first})
    _advance(env, p.mite_systemic_dose_interval_days + p.mite_systemic_dose_interval_tol + 1)
    second = _authorised_order(env, h)
    env.apply_action("administer_vet_order", {"order_id": second})
    # One dose on each of two orders: completeness reads the best SINGLE order, never the union.
    assert env.state.welfare.houses[h].red_mite_course_shortfall == 1.0


def test_a_treatment_request_for_an_empty_house_is_refused_like_a_service_booking():
    env = _env()
    h = _occupied(env)
    env.state.world.bird_count[h] = 0
    request = env.apply_action("request_vet_treatment", {"house_id": h, "issue": "red_mite"})
    booking = env.apply_action("book_ipm_service", {"house_id": h})
    assert not request.ok and not booking.ok
    assert "no live flock" in request.detail and "no live flock" in booking.detail
    assert env.state.mite_orders == []


# --------------------------------------------------------------------- egg-grade coupling


def test_mites_downgrade_eggs_and_never_touch_the_lay_rate():
    # The ruled harm channel: grade only. Charging a lay-rate loss as well would double-count
    # the same production harm (the field literature mixes the two effects).
    p = ModelParams()
    env = _env()
    h = _occupied(env)
    _arc(env, h, p.red_mite_carrying)
    hw = env.state.welfare.houses[h]
    hw.red_mite_hold_until_day = env.state.day_index + 5
    _advance(env, 2)
    infested_downgrade = env.state.financial.downgrade_dozen_cum
    lay_infested = hw.hen_day_pct

    clean = _env()
    hwc = clean.state.welfare.houses[h]
    _advance(clean, 2)
    assert infested_downgrade > clean.state.financial.downgrade_dozen_cum
    assert lay_infested == pytest.approx(hwc.hen_day_pct)
