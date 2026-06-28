from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.economics import downgrade_frac


def test_downgrade_rises_with_age():
    p = ModelParams()
    assert abs(downgrade_frac(30.0, 0.0, p) - 0.032) < 1e-6   # 3.2% at 30 wk
    assert abs(downgrade_frac(80.0, 0.0, p) - 0.238) < 1e-6   # 23.8% at 80 wk
    assert downgrade_frac(55.0, 0.0, p) > downgrade_frac(30.0, 0.0, p)


def test_downgrade_clamped_and_stress_additive():
    p = ModelParams(downgrade_stress_coeff=0.10)
    base = downgrade_frac(30.0, 0.0, p)
    assert downgrade_frac(30.0, 1.0, p) == base + 0.10       # stress adds
    assert downgrade_frac(30.0, 100.0, p) <= 0.95            # clamped
