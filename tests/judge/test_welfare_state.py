# tests/judge/test_welfare_state.py
import json, pathlib
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
