from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.layers.keel import keel_prevalence_pct


def test_keel_anchors():
    p = ModelParams()
    assert keel_prevalence_pct(20.0, p) == 0.0
    assert abs(keel_prevalence_pct(29.0, p) - 60.0) < 3.0
    assert abs(keel_prevalence_pct(39.0, p) - 76.0) < 3.0
    assert abs(keel_prevalence_pct(49.0, p) - 86.5) < 3.0


def test_keel_monotone_and_bounded():
    p = ModelParams()
    prev = -1.0
    for wk in range(18, 101):
        v = keel_prevalence_pct(float(wk), p)
        assert prev <= v <= 100.0
        prev = v


import pytest
from pydantic import ValidationError


def test_modelparams_rejects_mismatched_keel_lists():
    with pytest.raises(ValidationError):
        ModelParams(keel_age_wk=[22, 29, 39], keel_pct=[0, 60, 76, 86.5, 92])


def test_modelparams_rejects_nonmonotone_ages():
    with pytest.raises(ValidationError):
        ModelParams(keel_age_wk=[22, 20, 39, 49, 65])


def test_default_modelparams_still_valid():
    assert ModelParams().keel_age_wk[0] == 22
