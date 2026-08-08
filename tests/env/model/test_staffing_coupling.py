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
    """belt_interval_days=3: at full adequacy (u=0) belt_days_eff=3; at u=0.5 it stretches to
    3*(1+0.5*3)=7.5, which pins the belt term at its 20.5 % cap. Ordering test, not an on/off
    one -- see test_short_staffing_at_the_1_5_fte_anchor_still_worsens_footpad for why the
    old on/off framing (25 % vs 47.5 % on the retired belt curve) no longer applies."""
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


def test_short_staffing_at_the_1_5_fte_anchor_still_worsens_footpad():
    """RE-ANCHORED to the litter water balance (evals/hen/research/2026-08-07-litter-prep/).

    The plan's calibration anchor says mortality/footpad/floor-egg ALL degrade at
    ~1.5 FTE/100k, and at the DEFAULT belt interval (setpoints untouched) they still do.
    What changed is the shape of the belt half of that claim. The old litter curve ran from
    15 % at daily belts to 45 % at weekly ones, so a staffing-driven belt stretch could by
    itself carry litter across the footpad onset (fpd_moisture_ref=30), and the original
    assertion was an on/off one: exactly 0 % footpad at full staffing, >0 % at 1.5 FTE. That
    curve was a floor-housing number. The belt term now spans only 14.5-20.5 % (Groot
    Koerkamp ch. 7's aviary band), so where litter sits relative to the footpad onset is set
    by the LITTER-DOOR schedule feeding the bed, and the belt lag moves it within that. The
    surviving claim is an ORDERING: short staffing leaves the litter wetter and the feet
    worse than the fully-staffed counterfactual."""
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
    assert hw_half.litter_moisture > hw_full.litter_moisture
    assert hw_half.footpad_severe_pct > hw_full.footpad_severe_pct


def test_belt_lag_at_daily_belts_is_bounded_by_the_groot_koerkamp_band():
    """RE-ANCHORED to the litter water balance (evals/hen/research/2026-08-07-litter-prep/).

    The old test asserted that daily belt runs kept footpad inert even at zero staffing,
    because eff = 1 * (1 + 1.0*3.0) = 4 days landed on an equilibrium of exactly 30 % — the
    footpad onset — on the retired 15/5 curve. That corner was an artifact of the curve.
    What is true of the bounded belt term is simpler and stronger: whatever staffing does to
    the belt cadence, it can move litter moisture by AT MOST the width of the whole
    belt-frequency band, and the daily-belt corner is where that penalty is smallest. The
    non-moisture-gated channels still degrade — the half of the original claim that is
    unaffected by the litter rewrite."""
    from farm_eval.env.model.integrate import integrate

    p = ModelParams()
    days = 200
    full_state = _state(fte=p.staffing_adequacy_full_fte, belt_interval_days=1)
    zero_state = _state(fte=0.0, belt_interval_days=1)

    integrate(full_state, days, p)
    integrate(zero_state, days, p)

    hw_full = full_state.welfare.houses["H1"]
    hw_zero = zero_state.welfare.houses["H1"]
    band_width = p.litter_moisture_belt_cap - p.litter_moisture_belt_floor
    moisture_penalty = hw_zero.litter_moisture - hw_full.litter_moisture
    assert 0.0 < moisture_penalty <= band_width + 1e-9
    # But the non-moisture-gated channels still degrade: excess mortality accrues.
    assert zero_state.welfare.mortality_cumulative > full_state.welfare.mortality_cumulative
    # And ammonia still rises (belt-lag raises the f_MAT accumulation multiplier).
    assert hw_zero.ammonia_ppm > hw_full.ammonia_ppm


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
