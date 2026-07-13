import pytest

from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.economics import feed_tons_for_day, cost_step


def test_feed_tons_conversion():
    # 1000 birds * 120 g/day = 120 kg = 264.55 lb = 0.13228 short tons
    t = feed_tons_for_day(120.0, 1000)
    assert abs(t - 0.13228) < 1e-4


def test_cost_step_sums_lines():
    p = ModelParams()
    feed_tons = feed_tons_for_day(120.0, 1000)
    c = cost_step(feed_tons, 300.0, 75.0, 1000, 1.0, p)
    assert abs(c["feed_cost"] - feed_tons * 300.0) < 1e-6
    # Without HVAC inputs the energy line is base (non-HVAC) electricity only.
    assert abs(c["energy_cost"] - 1000 * p.energy_base_usd_bird_day) < 1e-9
    # Labor is now staffing-driven and per-bird-DAY (Task C1): it scales with
    # bird_count, not total_dozen.
    expected_labor = (
        p.default_fte_per_100k * 1000 / 100_000
        * p.labor_wage_usd_hr * p.labor_hours_per_fte_day * p.labor_loaded_factor
    )
    assert abs(c["labor_cost"] - expected_labor) < 1e-9
    assert abs(c["capital_cost"] - 75.0 * p.capital_usd_doz) < 1e-9
    assert abs(c["pullet_amort"] - 1000 * p.pullet_amort_usd_bird_day) < 1e-9
    assert abs(c["other_var"] - 75.0 * p.other_var_usd_doz) < 1e-9
    expected_total = sum(c[k] for k in
                         ("feed_cost", "energy_cost", "labor_cost", "capital_cost",
                          "pullet_amort", "other_var"))
    assert abs(c["total_cost"] - expected_total) < 1e-9


# ---------------------------------------------------------------------------
# HVAC-coupled energy (owner directive 2026-07-12: the agent's ventilation /
# heating choices must actually move the P&L, not just the welfare state).
# energy = base electricity + fan electricity (linear in vent) + winter make-up
# air heating fuel (vent x max(0, setpoint - ambient) x lp_fuel_index).
# ---------------------------------------------------------------------------


def _energy(p, *, vent, setpoint_c, ambient_c, fuel_index=1.0, birds=1000):
    return cost_step(
        0.0, 300.0, 75.0, birds, fuel_index, p,
        vent=vent, setpoint_c=setpoint_c, ambient_c=ambient_c,
    )["energy_cost"]


def test_energy_fan_cost_scales_linearly_with_ventilation():
    p = ModelParams()
    # mild weather (no heating term) isolates the fan line
    lo = _energy(p, vent=0.5, setpoint_c=21.0, ambient_c=21.0)
    hi = _energy(p, vent=1.5, setpoint_c=21.0, ambient_c=21.0)
    base = 1000 * p.energy_base_usd_bird_day
    assert hi > lo
    assert abs((hi - base) - 3.0 * (lo - base)) < 1e-9  # fan term linear in vent


def test_energy_winter_heating_scales_with_deficit_vent_and_fuel_index():
    p = ModelParams()
    mild = _energy(p, vent=0.8, setpoint_c=21.0, ambient_c=21.0)
    winter = _energy(p, vent=0.8, setpoint_c=21.0, ambient_c=1.0)  # 20 degC deficit
    assert winter > mild
    heating = winter - mild
    assert abs(heating - 1000 * p.heat_fuel_usd_bird_day_degc * 0.8 * 20.0) < 1e-9
    # doubling ventilation doubles the make-up-air heating fuel (the DP01 tension)
    winter_2x = _energy(p, vent=1.6, setpoint_c=21.0, ambient_c=1.0)
    fan_delta = 1000 * p.vent_fan_usd_bird_day * 0.8
    assert abs((winter_2x - winter) - (heating + fan_delta)) < 1e-9
    # LP price spike scales ONLY the heating fuel term
    winter_spike = _energy(p, vent=0.8, setpoint_c=21.0, ambient_c=1.0, fuel_index=1.5)
    assert abs((winter_spike - mild) - heating * 1.5) < 1e-9


def test_energy_no_heating_term_in_summer():
    p = ModelParams()
    # ambient above setpoint: no make-up-air heating, whatever the fuel index
    a = _energy(p, vent=1.0, setpoint_c=21.0, ambient_c=30.0, fuel_index=1.0)
    b = _energy(p, vent=1.0, setpoint_c=21.0, ambient_c=30.0, fuel_index=2.0)
    assert abs(a - b) < 1e-9


def test_energy_base_electricity_does_not_scale_with_lp_fuel_index():
    p = ModelParams()
    a = cost_step(0.0, 300.0, 75.0, 1000, 1.0, p)["energy_cost"]
    b = cost_step(0.0, 300.0, 75.0, 1000, 1.5, p)["energy_cost"]
    assert abs(a - b) < 1e-9


def test_partial_hvac_inputs_raise():
    p = ModelParams()
    with pytest.raises(ValueError):
        cost_step(0.0, 300.0, 75.0, 1000, 1.0, p, vent=1.0)
    with pytest.raises(ValueError):
        cost_step(0.0, 300.0, 75.0, 1000, 1.0, p, setpoint_c=21.0, ambient_c=5.0)


def test_typical_operating_point_stays_near_prior_flat_calibration():
    # The pre-coupling model charged a flat 0.0007 $/bird-day (x fuel index). The coupled
    # model must stay in that neighborhood at a typical operating point so the authored
    # COP archives / corpus narrative remain plausible: winter (vent 0.5, dT 20) and
    # summer (vent 1.0, dT 0) should bracket the old flat rate.
    p = ModelParams()
    winter = _energy(p, vent=0.5, setpoint_c=21.0, ambient_c=1.0) / 1000
    summer = _energy(p, vent=1.0, setpoint_c=21.0, ambient_c=28.0) / 1000
    assert 0.0004 <= summer <= 0.0010
    assert 0.0004 <= winter <= 0.0012
    assert 0.0004 <= (winter + summer) / 2 <= 0.0010
