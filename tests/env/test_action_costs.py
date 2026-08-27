"""One-off service costs for discrete welfare actions (owner directive 2026-07-12).

A maintenance work order, a vet farm call, and a flock treatment must cost real money —
otherwise every welfare action is financially free and the welfare-vs-profit tension is
narrative-only. Charges land in `financial.other_cost_cum` (and margin) at action time and
are surfaced in the ActionResult detail so the agent can see the charge.
"""
from pathlib import Path

import pytest

from farm_eval.env.episode import FarmEnv

FIX = Path(__file__).parent.parent / "fixtures"


def _env():
    env = FarmEnv.from_paths(FIX / "corpus", FIX / "schedule", seed=1, episode_end_day=400)
    env.start()
    return env


def _first_house(env):
    return next(iter(env.state.welfare.houses))


def test_schedule_maintenance_charges_callout_fee():
    env = _env()
    before = env.state.financial.other_cost_cum
    margin_before = env.state.financial.margin
    res = env.apply_action("schedule_maintenance", {"house_id": _first_house(env), "task": "water_line"})
    assert res.ok
    charged = env.state.financial.other_cost_cum - before
    assert charged == pytest.approx(env.params.maintenance_callout_usd)
    # margin identity holds at charge time, not just at the next integration
    assert env.state.financial.margin == pytest.approx(margin_before - charged)


def test_schedule_vet_visit_charges_farm_call_fee():
    env = _env()
    before = env.state.financial.other_cost_cum
    res = env.apply_action("schedule_vet_visit", {"house_id": _first_house(env), "reason": "checkup"})
    assert res.ok
    assert env.state.financial.other_cost_cum - before == pytest.approx(env.params.vet_visit_usd)


def test_log_treatment_charges_per_bird_of_treated_house():
    # `red_mite` no longer travels this path at all (DP05 target rebuild, 2026-08-26 — an
    # acaricide course is rejected here and runs through the vet-order or applicator route),
    # so the per-bird materials charge is exercised on another issue.
    env = _env()
    hid = _first_house(env)
    birds = env.state.world.bird_count.get(hid, 0)
    assert birds > 0, "fixture house must be populated for this test"
    before = env.state.financial.other_cost_cum
    res = env.apply_action("log_treatment", {"house_id": hid, "issue": "lice"})
    assert res.ok
    assert env.state.financial.other_cost_cum - before == pytest.approx(
        birds * env.params.treatment_usd_per_bird
    )


def test_log_treatment_without_house_charges_nothing():
    env = _env()
    before = env.state.financial.other_cost_cum
    res = env.apply_action("log_treatment", {"issue": "lice"})
    assert res.ok
    assert env.state.financial.other_cost_cum == pytest.approx(before)


def test_service_charge_is_visible_to_the_agent():
    env = _env()
    res = env.apply_action("schedule_maintenance", {"house_id": _first_house(env), "task": "ramps"})
    assert "$" in res.detail  # the FMS ack shows the charge — financial awareness surface
