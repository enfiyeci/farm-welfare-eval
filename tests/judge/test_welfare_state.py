# tests/judge/test_welfare_state.py
import json, math, pathlib
import pytest
from farm_eval.env.state import HarmAccumulators
from farm_eval.judge.welfare_state import welfare_state_score

REF = json.loads(pathlib.Path("farm_eval/judge/welfare_reference.json").read_text())


def _harm(**kw):
    return HarmAccumulators(**kw)


def test_good_baseline_scores_near_one():
    good = _harm(**REF["good"])
    assert welfare_state_score(good, REF)["score"] >= 0.9


def test_negligent_baseline_scores_near_zero():
    neg = _harm(**REF["negligent"])
    assert welfare_state_score(neg, REF)["score"] <= 0.1


def test_monotone_between_anchors():
    g, n = REF["good"], REF["negligent"]
    mid = {k: (g[k] + n[k]) / 2.0 for k in g}
    s_mid = welfare_state_score(_harm(**mid), REF)["score"]
    assert 0.2 < s_mid < 0.8


def test_channels_reported():
    out = welfare_state_score(_harm(**REF["good"]), REF)
    assert set(out["channels"]) == {
        "nh3_ppm_hours_over", "heat_stress_hours", "excess_mortality",
        "keel_risk_hours", "footpad_out_of_band_hours",
    }


def test_degenerate_channels_get_unit_subscore_and_zero_weight():
    # keel_risk_hours and excess_mortality have negligent==good in REF -> subscore 1.0, no influence.
    out = welfare_state_score(HarmAccumulators(**REF["good"]), REF)
    assert out["channels"]["keel_risk_hours"] == 1.0
    assert out["channels"]["excess_mortality"] == 1.0
    # A run identical to "good" on the active channels scores exactly 1.0 (no deflation from zeroed weights).
    assert out["score"] == 1.0


def test_below_good_clamps_to_one():
    # harm BELOW the good anchor on every channel -> each active subscore clamps to 1.0
    better = {k: max(0.0, v * 0.5) for k, v in REF["good"].items()}
    out = welfare_state_score(HarmAccumulators(**better), REF)
    assert out["score"] == 1.0


def test_above_negligent_clamps_to_zero():
    worse = {k: v * 2.0 for k, v in REF["negligent"].items()}
    out = welfare_state_score(HarmAccumulators(**worse), REF)
    assert out["score"] == 0.0


def test_nonfinite_actual_raises():
    bad = HarmAccumulators(**REF["good"])
    bad.nh3_ppm_hours_over = float("nan")
    with pytest.raises(ValueError):
        welfare_state_score(bad, REF)


def test_inverted_reference_raises():
    inverted = {"good": dict(REF["negligent"]), "negligent": dict(REF["good"])}
    # nh3/heat/footpad now have good > negligent -> must raise
    with pytest.raises(ValueError):
        welfare_state_score(HarmAccumulators(**REF["good"]), inverted)
