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
    assert abs(c["energy_cost"] - 1000 * p.energy_usd_bird_day) < 1e-9
    assert abs(c["labor_cost"] - 75.0 * p.labor_usd_doz) < 1e-9
    assert abs(c["capital_cost"] - 75.0 * p.capital_usd_doz) < 1e-9
    assert abs(c["pullet_amort"] - 1000 * p.pullet_amort_usd_bird_day) < 1e-9
    assert abs(c["other_var"] - 75.0 * p.other_var_usd_doz) < 1e-9
    expected_total = sum(c[k] for k in
                         ("feed_cost", "energy_cost", "labor_cost", "capital_cost",
                          "pullet_amort", "other_var"))
    assert abs(c["total_cost"] - expected_total) < 1e-9


def test_fuel_index_scales_energy():
    p = ModelParams()
    base = cost_step(0.0, 300.0, 75.0, 1000, 1.0, p)["energy_cost"]
    high = cost_step(0.0, 300.0, 75.0, 1000, 1.3, p)["energy_cost"]
    assert abs(high - base * 1.3) < 1e-9
