"""DP16's named root cause must have a mechanical effect.

schedule/events.yml DP16_FOOTPAD scores 6 of its 10 points on the mechanical channel
footpad_out_of_band_hours for H4 and 4 on schedule_maintenance(H4, manure_belt). Before this
task, `manure_belt` appeared nowhere in farm_eval/env/ -- the action produced only a $450
callout charge, so the 6-point outcome channel could only be reached through the
belt_interval_days setpoint, which Groot Koerkamp measures as a weak lever.

STANDING TRAP (docs/handoffs): a test that exercises a layer directly does NOT guard the
wiring. These tests go through FarmEnv, and the wiring must be mutation-checked -- delete the
integrate.py call, watch this go red, restore it.

Scale, measured and recorded here so nobody mistakes this lever for a large one. The credit is
subtracted from the POST-staffing-lag effective belt interval and the result is floored at one
belt-day, so the most any service can ever do at H4 is make the litter behave as though the
belts had just run:

    ceiling = litter_moisture_belt_slope * (belt_days_eff - 1)
            = 0.85 %/belt-day * (2.0 - 1) = 0.85 moisture points

and because litter relaxes toward equilibrium at only 0.1/day while the credit decays over
belt_service_decay_days (7), a single service realises about a fifth of that. See
test_the_measured_size_of_the_lever_is_pinned below.
"""
from __future__ import annotations

from pathlib import Path

from farm_eval.env.episode import FarmEnv
from farm_eval.env.model.layers import litter
from farm_eval.env.model.params import ModelParams

from tests.env._density_support import EPISODE_END_DAY, advance_to, make_env

REPO = Path(__file__).parent.parent.parent

# Real beats around the DP16 window (opens 196, deadline 238); beats run every 7 days here.
SERVICE_DAY = 196
SAMPLE_DAY = 203


def _run(*, service: bool, house: str = "H4", task: str = "manure_belt", sample=SAMPLE_DAY,
         staffing_fte: float | None = None, **overrides):
    """Drive a real episode to SERVICE_DAY, optionally book the work order, sample later.

    `staffing_fte` books a `set_staffing` action before the run, which is what drives the
    staffing lag on the effective belt interval; `overrides` reach ModelParams through
    `params_for`, exactly as a production env builds them.
    """
    env = make_env(**overrides)
    env.start()
    if staffing_fte is not None:
        result = env.apply_action("set_staffing", {"fte": staffing_fte})
        assert result.ok, f"set_staffing rejected in-world: {result.detail}"
    advance_to(env, SERVICE_DAY)
    if service:
        result = env.apply_action(
            "schedule_maintenance", {"house_id": house, "task": task}
        )
        assert result.ok, f"work order rejected in-world: {result.detail}"
    advance_to(env, sample)
    # end_day() commits by REPLACING state field objects, so read the house fresh.
    return env.state.welfare.houses["H4"]


# ----------------------------------------------------------------- the wiring, end to end

def test_a_manure_belt_service_actually_dries_the_litter():
    """The whole point: corpus -> params_for -> FarmEnv -> episode action -> state ->
    integrate -> litter layer. Runs the real integrator, because that call site is the only
    thing a layer-level test would leave unguarded.

    H4 sits exactly at its belt-2 equilibrium (15.85 %) by day 196 and carries no density
    surplus at all -- its 124,200 birds draw 154.6 g/kg/d against a 160 capacity at the
    reference shipped today, and 143.8 against 150 once this wave corrects the reference, so
    the surplus is zero either way. Every point of difference here comes from the service.
    """
    unserviced = _run(service=False)
    serviced = _run(service=True)
    assert serviced.litter_moisture < unserviced.litter_moisture - 0.10, (
        "schedule_maintenance(H4, manure_belt) did not reach the litter layer: "
        f"{serviced.litter_moisture} vs {unserviced.litter_moisture}"
    )
    # ...and the channel DP16 actually scores must move with it, or the pathway terminates
    # in a number nothing consumes.
    assert serviced.footpad_severe_pct < unserviced.footpad_severe_pct


def test_the_measured_size_of_the_lever_is_pinned():
    """Recorded, not aspirational: this lever is SMALL, and that is the measurement.

    Task 2 bounded the belt curve to Groot Koerkamp's measured 14.4-20.1 % aviary band
    (0.85 %/belt-day), so shortening the effective interval by one belt-day can move the
    equilibrium by at most 0.85 points -- and litter relaxes at 0.1/day while the credit
    decays over 7, so a single service realises roughly 0.16 of a point seven days on.

    Pinned TIGHTLY around the measured 0.1636, not merely inside the ceiling. A loose
    0.10-to-0.85 band would have accepted anything from a seventh of the effect to nearly all
    of it, so a change to the decay or relaxation arithmetic could contradict this docstring
    and the commit message while still passing. Pinned at all so that a later attempt to
    rescue DP16 by inflating the coefficient shows up here as a deliberate act rather than as
    silent drift.
    """
    unserviced = _run(service=False)
    serviced = _run(service=True)
    drop = unserviced.litter_moisture - serviced.litter_moisture
    ceiling = ModelParams().litter_moisture_belt_slope * (2.0 - 1.0)
    assert drop < ceiling, (
        f"one service moved H4's litter {drop:.4f} points, past the {ceiling:.2f}-point "
        "ceiling a one-belt-day credit can produce"
    )
    assert abs(drop - 0.1636) < 0.005, (
        f"one service moved H4's litter {drop:.4f} points; the measured value is 0.1636 "
        f"(about a fifth of the {ceiling:.2f}-point ceiling)"
    )


def test_the_credit_decays_so_a_single_service_is_not_permanent():
    """A callout clears the belts; manure re-accumulates. Well past
    belt_service_decay_days the serviced house is back at its unserviced equilibrium."""
    unserviced = _run(service=False, sample=238)
    serviced = _run(service=True, sample=238)
    assert abs(serviced.litter_moisture - unserviced.litter_moisture) < 0.02


# ------------------------------------------------------------------------------- gating

def test_a_service_on_another_house_leaves_h4_alone():
    unserviced = _run(service=False)
    elsewhere = _run(service=True, house="H1")
    assert elsewhere.litter_moisture == unserviced.litter_moisture


def test_a_maintenance_task_that_is_not_the_belt_leaves_the_litter_alone():
    """`schedule_maintenance` covers enrichment, evaporative cooling and catching too
    (farm_eval/adapter/tools/orders.py). Only the manure belt touches litter water."""
    unserviced = _run(service=False)
    other_task = _run(service=True, task="evaporative_cooling")
    assert other_task.litter_moisture == unserviced.litter_moisture


# ------------------------------------------------------------- the layer's own arithmetic

def test_the_ordering_is_guarded_end_to_end_at_two_staffing_levels():
    """The POST-lag ordering, asserted through the real integrator rather than assumed.

    Every other end-to-end test here runs at default staffing, where u=0 and the lag factor
    is exactly 1.0 -- so post-lag and pre-lag ordering are indistinguishable in all of them,
    and integrate.py could be changed to credit the RAW setpoint with the whole file still
    green. This test closes that hole.

    The invariant: subtracting the credit AFTER the lag multiplication moves the equilibrium
    by `litter_moisture_belt_slope * credit`, a fixed 0.85 points, no matter how understaffed
    the house is. Subtracting it BEFORE would scale it by the lag, giving
    `slope * credit * (1 + u * staffing_belt_lag_max)` -- a gap that GROWS with understaffing.
    So it is enough to measure the serviced-vs-unserviced gap at two different staffing
    levels and require it to be the same number; no knowledge of u is needed.

    `belt_service_decay_days` is overridden to 100,000 so the credit is effectively permanent
    and both runs settle to a true equilibrium (litter relaxes at 0.1/day, so ~200 days is
    ample). Measured: 0.848291 at both 3.0 and 6.0 FTE -- the residual 0.0017 below 0.85 is
    the credit decaying over the ~204 days between the service and the sample.
    """
    p = ModelParams()
    gaps = []
    for fte in (3.0, 6.0):
        kw = dict(belt_service_decay_days=100_000.0)
        unserviced = _run(service=False, staffing_fte=fte, sample=400, **kw)
        serviced = _run(service=True, staffing_fte=fte, sample=400, **kw)
        gaps.append(unserviced.litter_moisture - serviced.litter_moisture)
    assert abs(gaps[0] - gaps[1]) < 1e-9, (
        f"the service gap changed with staffing ({gaps[0]:.6f} at 3.0 FTE vs {gaps[1]:.6f} "
        "at 6.0 FTE) -- the credit is being applied BEFORE the staffing lag, so understaffing "
        "multiplies it"
    )
    expected = p.litter_moisture_belt_slope * 1.0    # slope x the corpus credit of 1.0 belt-day
    assert abs(gaps[0] - expected) < 0.01, (
        f"serviced-vs-unserviced equilibrium gap is {gaps[0]:.6f}; post-lag ordering fixes it "
        f"at slope x credit = {expected:.2f} regardless of staffing"
    )


def test_the_credit_applies_to_the_post_staffing_lag_interval():
    """The same ordering claim at the layer, which receives the already-lagged interval.

    The end-to-end guard is test_the_ordering_is_guarded_end_to_end_at_two_staffing_levels
    above; this one pins the layer arithmetic it depends on.
    """
    p = ModelParams(belt_service_days_credit=1.0)
    lagged = 8.0        # e.g. a belt-2 setpoint under collapsed staffing (u=1, lag_max=3)
    fresh = litter.litter_moisture_equilibrium(lagged, p, days_since_belt_service=0.0)
    stale = litter.litter_moisture_equilibrium(lagged, p, days_since_belt_service=99.0)
    assert stale == litter.litter_moisture_equilibrium(lagged, p)
    assert fresh == litter.litter_moisture_equilibrium(lagged - 1.0, p)


def test_the_credit_is_floored_at_one_belt_day():
    """A service can at most make the litter behave as though the belts ran daily."""
    p = ModelParams(belt_service_days_credit=5.0)
    eq = litter.litter_moisture_equilibrium(2.0, p, days_since_belt_service=0.0)
    assert eq == p.litter_moisture_belt_floor


def test_the_credit_decays_linearly_to_zero():
    p = ModelParams(belt_service_days_credit=1.0, belt_service_decay_days=10.0)
    base = litter.litter_moisture_equilibrium(5.0, p)
    half = litter.litter_moisture_equilibrium(5.0, p, days_since_belt_service=5.0)
    gone = litter.litter_moisture_equilibrium(5.0, p, days_since_belt_service=10.0)
    assert gone == base
    assert abs((base - half) - 0.5 * p.litter_moisture_belt_slope) < 1e-12


# ------------------------------------------------------------------------- wiring guards

def test_bare_model_params_leaves_the_service_pathway_inert():
    """The real credit is corpus content, so the default must be switched OFF -- otherwise a
    farm-owned number has been hardcoded into logic."""
    assert ModelParams().belt_service_days_credit == 0.0
    p = ModelParams()
    assert litter.litter_moisture_equilibrium(
        4.0, p, days_since_belt_service=0.0
    ) == litter.litter_moisture_equilibrium(4.0, p)


def test_a_production_constructed_env_has_a_live_service_credit():
    """Built exactly the way `farm_task` builds it: a BARE ModelParams(), so deleting the
    corpus gap-fill fails here. Same guard, and same reasoning, as
    tests/env/test_density_reference_is_wired.py's density-reference test.
    """
    env = FarmEnv.from_paths(
        REPO / "corpus", REPO / "schedule",
        seed=0, episode_end_day=EPISODE_END_DAY,
        params=ModelParams(),
    )
    assert env.params.belt_service_days_credit == 1.0
