from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.layers.red_mite import red_mite_step


def test_red_mite_grows_logistically_toward_carrying():
    p = ModelParams()
    idx = 0.05
    for _ in range(120):
        idx = red_mite_step(idx, p)
    assert idx > 1.0                       # established infestation (relative units)
    assert idx <= p.red_mite_carrying + 1e-9


def test_red_mite_growth_is_monotone_until_carrying():
    p = ModelParams()
    a = red_mite_step(0.1, p)
    b = red_mite_step(a, p)
    assert b > a                           # grows when below carrying capacity
