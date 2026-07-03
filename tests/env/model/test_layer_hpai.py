from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.layers.hpai import hpai_daily_mortality_frac


def test_no_onset_means_no_hpai_mortality():
    p = ModelParams()
    assert hpai_daily_mortality_frac(onset_day=-1, current_day=100, params=p) == 0.0


def test_subclinical_then_exponential_rise():
    p = ModelParams()
    onset = 50
    # During incubation: ~no excess mortality.
    assert hpai_daily_mortality_frac(onset, onset + 1, p) < 0.001
    # After incubation, mortality rises and crosses the 0.5%/day classic reporting threshold.
    early = hpai_daily_mortality_frac(onset, onset + p.hpai_incubation_days + 1, p)
    later = hpai_daily_mortality_frac(onset, onset + p.hpai_incubation_days + 4, p)
    assert later > early                                   # exponential growth
    assert later >= 0.005                                  # crosses 0.5%/day within days
    # Capped (cannot exceed the daily cap).
    assert hpai_daily_mortality_frac(onset, onset + 30, p) <= p.hpai_mort_cap + 1e-9
