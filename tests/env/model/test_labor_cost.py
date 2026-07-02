# tests/env/model/test_labor_cost.py
"""Staffing-driven daily labor cost line (Task C1).

labor_cost is now a per-bird-DAY cost (direct_fte * wage * hours * loaded_factor),
not a per-dozen cost — it no longer scales with eggs laid. `fte_per_100k` is an
optional cost_step argument that defaults to params.default_fte_per_100k; Task C2
will thread a real staffing state value through it.
"""

from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.economics import cost_step


def test_labor_cost_matches_staffing_formula_and_research_band():
    p = ModelParams()
    bird_count = 100_000
    c = cost_step(0.0, 300.0, 7_500.0, bird_count, 1.0, p)
    expected = (
        p.default_fte_per_100k
        * p.labor_wage_usd_hr
        * p.labor_hours_per_fte_day
        * p.labor_loaded_factor
    )
    assert abs(c["labor_cost"] - expected) < 1e-9
    # Representative lay rate ~90% henday -> total_dozen = 100_000 * 0.90 / 12 = 7500
    per_doz = c["labor_cost"] / 7_500.0
    assert 0.05 <= per_doz <= 0.10


def test_labor_cost_continuity_with_old_flat_per_dozen_line():
    # Continuity guard: at default staffing, ~90% henday, 100k birds, the new
    # staffing-driven line lands within ~5% of the OLD flat 0.074 usd/doz line
    # (proves the COP calibration at default staffing is preserved).
    p = ModelParams()
    bird_count = 100_000
    total_dozen = bird_count * 0.90 / 12.0
    c = cost_step(0.0, 300.0, total_dozen, bird_count, 1.0, p)
    old_line = 0.074 * total_dozen
    assert abs(c["labor_cost"] - old_line) / old_line < 0.05


def test_labor_cost_scales_linearly_with_staffing():
    p = ModelParams()
    bird_count = 100_000
    total_dozen = 7_500.0
    default_cost = cost_step(0.0, 300.0, total_dozen, bird_count, 1.0, p)["labor_cost"]
    doubled_cost = cost_step(
        0.0, 300.0, total_dozen, bird_count, 1.0, p, fte_per_100k=5.0
    )["labor_cost"]
    zero_cost = cost_step(
        0.0, 300.0, total_dozen, bird_count, 1.0, p, fte_per_100k=0.0
    )["labor_cost"]
    assert abs(doubled_cost - 2.0 * default_cost) < 1e-9
    assert zero_cost == 0.0


def test_labor_cost_is_per_bird_day_not_per_dozen():
    # Same bird_count, wildly different total_dozen (e.g. low- vs high-lay) ->
    # IDENTICAL labor_cost: labor no longer scales with eggs laid.
    p = ModelParams()
    bird_count = 100_000
    low_lay = cost_step(0.0, 300.0, 100.0, bird_count, 1.0, p)["labor_cost"]
    high_lay = cost_step(0.0, 300.0, 9_000.0, bird_count, 1.0, p)["labor_cost"]
    assert low_lay == high_lay


def test_labor_cost_still_participates_in_total_cost():
    p = ModelParams()
    c = cost_step(1.0, 300.0, 7_500.0, 100_000, 1.0, p)
    expected_total = sum(
        c[k]
        for k in (
            "feed_cost",
            "energy_cost",
            "labor_cost",
            "capital_cost",
            "pullet_amort",
            "other_var",
        )
    )
    assert abs(c["total_cost"] - expected_total) < 1e-9
