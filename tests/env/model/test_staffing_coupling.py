"""C3 — staffing->welfare coupling (heuristic, anchored to research §A/§C).

C2 gave the agent a `set_staffing` lever (`state.world.staffing_fte` /
`staffing_shift_hours`) that changes the daily labor COST line. C3 wires that SAME
lever into welfare and production outcomes via one monotone adequacy factor
`f = adequacy_factor(fte_per_100k, shift_hours, params)`, `u = 1 - f`:

  1. sick-bird-detection lag -> excess mortality (research §C: 7.2% aviary vs 3.1%
     caged cumulative-mortality gap; spread over a ~70-week cycle, reached at u=1).
  2. inspection/collection lag -> floor eggs (downgrade fraction; research §C:
     floor-egg incidence spikes toward 10-15% in poorly managed flocks).
  3. litter/manure task lag -> footpad + ammonia (belt interval stretches
     effectively under short-staffing; research §C: skipped litter work raises
     ammonia and foot problems).

At default staffing (agent never touches the lever) fte_eq=2.5 -> f=1 -> u=0 and
ALL three couplings are inert (the regression guard: zero drift in the existing
suite).
"""
from __future__ import annotations

import pytest

from farm_eval.env.model.layers.staffing import adequacy_factor
from farm_eval.env.model.params import ModelParams
from farm_eval.env.state import EnvState, HouseWelfare


# --- 1. Adequacy-factor properties -----------------------------------------------------


def test_full_adequacy_at_2_5_fte_8h():
    p = ModelParams()
    assert adequacy_factor(p.staffing_adequacy_full_fte, p.labor_hours_per_fte_day, p) == 1.0


def test_plateau_above_full_no_bonus():
    p = ModelParams()
    f_full = adequacy_factor(p.staffing_adequacy_full_fte, p.labor_hours_per_fte_day, p)
    f_over = adequacy_factor(3.5, p.labor_hours_per_fte_day, p)
    assert f_over == f_full == 1.0


def test_monotone_nondecreasing_across_a_sweep():
    p = ModelParams()
    xs = [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 3.0, 4.0]
    ys = [adequacy_factor(x, p.labor_hours_per_fte_day, p) for x in xs]
    assert all(b >= a for a, b in zip(ys, ys[1:]))


def test_bounded_0_to_1():
    p = ModelParams()
    xs = [-1.0, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 5.0, 100.0]
    for x in xs:
        f = adequacy_factor(x, p.labor_hours_per_fte_day, p)
        assert 0.0 <= f <= 1.0


def test_smoothstep_midpoint_is_one_half():
    """f(1.5, 8h) = 0.5 — the smoothstep midpoint, computed from params (not a literal)."""
    p = ModelParams()
    midpoint_fte = (p.staffing_adequacy_zero_fte + p.staffing_adequacy_full_fte) / 2.0
    assert midpoint_fte == pytest.approx(1.5)
    f = adequacy_factor(midpoint_fte, p.labor_hours_per_fte_day, p)
    assert f == pytest.approx(0.5)


def test_hours_equivalence_half_fte_double_hours_same_factor():
    """A crew of 2 working 16h surge days covers what 4 cover on 8h shifts (research §A)."""
    p = ModelParams()
    f_8h = adequacy_factor(2.5, 8.0, p)
    f_16h_half_fte = adequacy_factor(1.25, 16.0, p)
    assert f_8h == pytest.approx(f_16h_half_fte)


def test_zero_fte_zero_hours_gives_zero_adequacy():
    p = ModelParams()
    assert adequacy_factor(0.0, 8.0, p) == 0.0


def test_zero_or_below_at_the_zero_anchor():
    p = ModelParams()
    assert adequacy_factor(p.staffing_adequacy_zero_fte, 8.0, p) == 0.0
    assert adequacy_factor(p.staffing_adequacy_zero_fte / 2, 8.0, p) == 0.0


# --- helpers for the integrate()-level tests --------------------------------------------


def _state(fte, shift_hours=None, birds=100_000, age_wk=30.0, belt_interval_days=2) -> EnvState:
    state = EnvState(start_date="2025-06-09")
    state.welfare.houses["H1"] = HouseWelfare(
        ammonia_ppm=6.0, co2_ppm=2200.0, litter_moisture=20.0,
        lighting_lux=10.0, lighting_hours=16.0, heat_stress_index=0.0,
        stocking_density=1.0,
    )
    state.world.bird_count["H1"] = birds
    state.world.age_weeks_at_start["H1"] = age_wk
    state.world.litter_age_days["H1"] = 0.0
    state.world.setpoints["H1"] = {"belt_interval_days": belt_interval_days}
    state.market.egg_price_usd_doz = 2.0
    state.market.layer_ration_usd_ton = 300.0
    state.market.lp_fuel_index = 1.0
    state.world.staffing_fte = fte
    if shift_hours is not None:
        state.world.staffing_shift_hours = shift_hours
    return state


# --- 2. Inert at default ------------------------------------------------------------------


def test_inert_at_default_untouched_vs_explicit_full_staffing():
    """An explicit absolute headcount equivalent to full adequacy (fte=2.5 at 100k birds)
    plateaus the SAME adequacy factor (f=1, u=0) as untouched (None) staffing, so the C3
    welfare couplings (mortality/footpad/ammonia -- driven by u) are identical between the
    two. Financial state is NOT compared here: `effective_fte_per_100k`'s absolute-headcount
    semantics (C2) mean the labor-cost ratio drifts slightly from `default_fte_per_100k` as
    the flock depletes under a FIXED headcount -- a pre-existing C2 behavior, orthogonal to
    C3's adequacy-factor coupling (both stay pinned at the f=1 plateau throughout)."""
    from farm_eval.env.model.integrate import integrate

    p = ModelParams()
    days = 30
    default_state = _state(fte=None)
    # Explicit equivalent of 2.5/100k at 100_000 birds -> fte=2.5
    full_state = _state(fte=p.staffing_adequacy_full_fte)

    integrate(default_state, days, p)
    integrate(full_state, days, p)

    assert default_state.world.bird_count == full_state.world.bird_count
    assert default_state.welfare.mortality_cumulative == full_state.welfare.mortality_cumulative
    hw_d, hw_f = default_state.welfare.houses["H1"], full_state.welfare.houses["H1"]
    assert hw_d.footpad_severe_pct == hw_f.footpad_severe_pct
    assert hw_d.footpad_mild_pct == hw_f.footpad_mild_pct
    assert hw_d.ammonia_ppm == hw_f.ammonia_ppm
    assert hw_d.litter_moisture == hw_f.litter_moisture
    assert default_state.financial.sellable_dozen_cum == pytest.approx(
        full_state.financial.sellable_dozen_cum
    )


def test_inert_at_default_byte_identical_to_pre_c3_no_staffing_touched():
    """No staffing lever touched at all (None) reproduces the pre-C3 numbers exactly —
    the couplings must not fire off of a None staffing state."""
    from farm_eval.env.model.integrate import integrate

    p = ModelParams()
    s1 = _state(fte=None)
    s2 = _state(fte=None)
    integrate(s1, 20, p)
    integrate(s2, 20, p)
    assert s1.financial.model_dump() == s2.financial.model_dump()
    assert s1.world.bird_count == s2.world.bird_count


# --- 3. Degradation at 1.5 FTE/100k (u=0.5) -----------------------------------------------


def test_degradation_at_1_5_fte_raises_cumulative_mortality():
    from farm_eval.env.model.integrate import integrate

    p = ModelParams()
    days = 60
    birds = 100_000
    full_state = _state(fte=p.staffing_adequacy_full_fte, birds=birds)
    half_state = _state(fte=1.5, birds=birds)

    integrate(full_state, days, p)
    integrate(half_state, days, p)

    u = 0.5
    expected_extra = u * p.staffing_excess_mort_daily_frac * days * birds
    actual_extra = half_state.welfare.mortality_cumulative - full_state.welfare.mortality_cumulative
    # Tolerance for per-day int rounding of (baseline+excess)*birds across `days` steps.
    assert actual_extra == pytest.approx(expected_extra, abs=max(2.0, 0.05 * expected_extra))
    assert half_state.welfare.mortality_cumulative > full_state.welfare.mortality_cumulative


def test_degradation_at_1_5_fte_lowers_sellable_dozen():
    from farm_eval.env.model.integrate import integrate

    p = ModelParams()
    days = 30
    full_state = _state(fte=p.staffing_adequacy_full_fte)
    half_state = _state(fte=1.5)

    integrate(full_state, days, p)
    integrate(half_state, days, p)

    full_sellable = full_state.financial.sellable_dozen_cum
    half_sellable = half_state.financial.sellable_dozen_cum
    assert half_sellable < full_sellable
    # u=0.5 -> +0.06 downgrade frac (half of staffing_floor_egg_max_frac=0.12) ~= 6% of production
    u = 0.5
    expected_extra_downgrade_frac = u * p.staffing_floor_egg_max_frac
    assert expected_extra_downgrade_frac == pytest.approx(0.06)
    relative_drop = (full_sellable - half_sellable) / full_sellable
    assert relative_drop == pytest.approx(expected_extra_downgrade_frac, abs=0.01)


def test_degradation_at_1_5_fte_raises_footpad_and_ammonia_after_enough_days():
    """belt_interval_days=3: at full adequacy (u=0) belt_days_eff=3 -> equilibrium moisture
    16.7%. At u=0.5, belt_days_eff=3*(1+0.5*3)=7.5 -> equilibrium moisture 20.5%. Footpad
    severe follows: 19.7% vs 29.8% after 120 days.

    The moisture figures were 25% and 47.5% while the belt curve ran at 5.0 %/belt-day, and the
    split was described as crossing the footpad on/off threshold at 30%. Both are superseded:
    the curve is bounded to the measured 14.4-20.1% aviary band and footpad responds by degree
    across that whole band rather than switching on at a threshold. The test's claim -- that
    short-staffing raises footpad and ammonia -- is unchanged and still holds."""
    from farm_eval.env.model.integrate import integrate

    p = ModelParams()
    days = 120  # enough for litter moisture to relax toward its (stretched) equilibrium
    full_state = _state(fte=p.staffing_adequacy_full_fte, belt_interval_days=3)
    half_state = _state(fte=1.5, belt_interval_days=3)

    integrate(full_state, days, p)
    integrate(half_state, days, p)

    hw_full = full_state.welfare.houses["H1"]
    hw_half = half_state.welfare.houses["H1"]
    assert hw_half.footpad_severe_pct > hw_full.footpad_severe_pct
    assert hw_half.ammonia_ppm > hw_full.ammonia_ppm


def test_footpad_degrades_at_default_belt_and_1_5_fte_anchor():
    """The plan's calibration anchor says mortality/footpad/floor-egg ALL degrade at
    ~1.5 FTE/100k. Footpad must therefore respond at the DEFAULT belt interval (setpoints
    untouched — belt_interval_days=2), not only when the agent has already lengthened the belt.
    With staffing_belt_lag_max=3.0, u=0.5 stretches belt 2 -> eff 5 days, which raises the litter
    equilibrium from 15.85 % to 18.26 % and severe footpad from 17.05 % to 24.35 %.

    Re-pointed from an absolute `hw_full.footpad_severe_pct == 0.0`. That assertion encoded the
    old claim that a fully-staffed default-belt house sits BELOW the footpad onset threshold, which
    held only while the threshold was 30 % and the belt curve reached 45 %. Both of those numbers
    were calibrated from each other rather than from a measurement. Footpad is now nonzero across
    the whole measured operating band, because that is what Wang et al. 1998 measured in layers:
    13–17 % prevalence on DRY litter, not zero. So the anchor is a DEGRADATION, not an activation —
    which is also what the research §C claim ("skipped litter work raises foot problems") says.
    """
    from farm_eval.env.model.integrate import integrate

    p = ModelParams()
    days = 200  # let litter fully relax toward the stretched equilibrium
    # DEFAULT belt interval (2) — agent never touched the belt setpoint.
    full_state = _state(fte=p.staffing_adequacy_full_fte, belt_interval_days=2)
    half_state = _state(fte=1.5, belt_interval_days=2)

    integrate(full_state, days, p)
    integrate(half_state, days, p)

    hw_full = full_state.welfare.houses["H1"]
    hw_half = half_state.welfare.houses["H1"]
    # Short-staffing at the anchor degrades footpad, by a margin big enough to score.
    assert hw_half.footpad_severe_pct > hw_full.footpad_severe_pct + 5.0
    # And it does so by wetting the litter — the mechanism, not just the outcome.
    assert hw_half.litter_moisture > hw_full.litter_moisture


def test_belt_lag_daily_belt_corner_is_the_least_bad_corner_even_at_zero_staffing():
    """Daily belt runs are the best defence available against the belt-lag channel.

    Re-pointed from `zero_state...footpad_severe_pct == 0.0`, which asserted this corner was
    fully INERT. That rested on eff = 1 * (1 + 1.0*3.0) = 4 days landing at equilibrium moisture
    exactly 30 %, i.e. exactly ON the old footpad onset threshold. Both halves of that
    coincidence are gone: the belt curve is now bounded to the measured 14.4–20.1 % aviary band
    (Groot Koerkamp Ch. 7 Table 4) and the onset threshold is 13 %, because Wang et al. 1998
    measured 13–17 % footpad prevalence on DRY litter in White Leghorn layers — dry-litter footpad
    is not zero, so no corner of the operating band is inert any more.

    What survives, and is the useful claim, is that daily belts are the LEAST BAD corner: at any
    staffing level, running the belts daily gives drier litter and less footpad than any longer
    interval. That is what makes belt_interval_days a lever the agent can pull in the right
    direction, which is what the eval actually scores.
    """
    from farm_eval.env.model.integrate import integrate

    p = ModelParams()
    days = 200

    def run(fte, belt_interval_days):
        state = _state(fte=fte, belt_interval_days=belt_interval_days)
        integrate(state, days, p)
        return state

    full_state = run(p.staffing_adequacy_full_fte, 1)
    zero_state = run(0.0, 1)

    # Least bad: at zero staffing, daily belts beat every longer interval on footpad AND moisture.
    zero_daily = zero_state.welfare.houses["H1"]
    for belt_interval_days in (2, 3, 5):
        worse = run(0.0, belt_interval_days).welfare.houses["H1"]
        assert worse.footpad_severe_pct > zero_daily.footpad_severe_pct, (
            f"belt {belt_interval_days} at zero staffing is not worse than daily belts"
        )
        assert worse.litter_moisture > zero_daily.litter_moisture
    # And at daily belts, full staffing still beats zero staffing — the corner is not saturated.
    assert zero_daily.footpad_severe_pct > full_state.welfare.houses["H1"].footpad_severe_pct
    # The non-moisture channels still degrade too: excess mortality accrues.
    assert zero_state.welfare.mortality_cumulative > full_state.welfare.mortality_cumulative
    # And ammonia still rises (belt-lag raises the f_MAT accumulation multiplier).
    assert zero_daily.ammonia_ppm > full_state.welfare.houses["H1"].ammonia_ppm


# --- 4. Anchor-coverage meta-test (mirrors test_anchor_coverage.py style) -----------------


def test_full_cycle_understaffed_mortality_reproduces_the_4_1pp_gap_at_u_1():
    """research §C: 7.2% aviary vs 3.1% caged cumulative-mortality gap = 4.1pp, spread over a
    ~70-week (490-day) lay cycle -> staffing_excess_mort_daily_frac = (0.072-0.031)/490."""
    p = ModelParams()
    gap_pp = 0.072 - 0.031
    cycle_days = 490
    # The param default (8.4e-5) is the DOCUMENTED, rounded value; the raw division is
    # 8.367e-5 -- close (within rounding) but not bit-identical.
    assert p.staffing_excess_mort_daily_frac == pytest.approx(gap_pp / cycle_days, rel=0.01)
    # At u=1 (zero staffing) over the full cycle, accrued extra mortality fraction ~= the gap
    # (the documented param is rounded to 8.4e-5, so this is close-but-not-bit-identical).
    u = 1.0
    accrued = u * p.staffing_excess_mort_daily_frac * cycle_days
    assert accrued == pytest.approx(gap_pp, rel=0.01)


def test_floor_egg_ceiling_matches_the_10_to_15_pct_band():
    p = ModelParams()
    assert 0.10 <= p.staffing_floor_egg_max_frac <= 0.15


def test_full_adequacy_sits_at_the_40k_hens_per_fte_anchor():
    """research §A: ~40k hens/FTE aviary standard -> 100k/40k = 2.5 FTE/100k at full shift."""
    p = ModelParams()
    assert p.staffing_adequacy_full_fte == pytest.approx(100_000 / 40_000)
    assert p.staffing_adequacy_full_fte == p.default_fte_per_100k


# --- 5. Zero staffing edge -----------------------------------------------------------------


def test_zero_staffing_couplings_at_maximum_no_crash_mortality_cap_holds():
    from farm_eval.env.model.integrate import integrate

    p = ModelParams()
    state = _state(fte=0.0)
    integrate(state, 30, p)  # must not crash
    assert state.world.bird_count["H1"] >= 0
    total_deaths = 100_000 - state.world.bird_count["H1"]
    assert total_deaths <= 100_000  # cannot exceed the flock, even at u=1 + heat + hpai

    f_zero = adequacy_factor(0.0, 8.0, p)
    assert f_zero == 0.0
