from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.layers.feather import feather_damage_pct


def test_feather_anchors():
    p = ModelParams()
    assert feather_damage_pct(28.0, p) == 0.0
    assert abs(feather_damage_pct(31.0, p) - 3.2) < 2.0
    assert abs(feather_damage_pct(46.0, p) - 32.9) < 3.0
    assert abs(feather_damage_pct(65.0, p) - 57.8) < 3.0


def test_feather_monotone():
    p = ModelParams()
    prev = -1.0
    for wk in range(28, 101):
        v = feather_damage_pct(float(wk), p)
        assert prev <= v <= 100.0
        prev = v
