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
    # Five Layer-1 channels plus the anchored node-only mite channel (D5, 2026-08-11).
    out = welfare_state_score(_harm(**REF["good"]), REF)
    assert set(out["channels"]) == {
        "nh3_ppm_hours_over", "heat_stress_hours", "excess_mortality",
        "keel_risk_hours", "footpad_out_of_band_hours",
    }


def test_keel_is_degenerate_with_zero_weight_but_excess_mortality_is_live():
    # keel_risk_hours has negligent==good in REF (age-only) -> degenerate, zero weight.
    # excess_mortality now DISCRIMINATES (negligent kills birds in the heat event, good
    # does not) -> it carries weight and a negligent value on it must lower the score.
    out_good = welfare_state_score(HarmAccumulators(**REF["good"]), REF)
    assert out_good["channels"]["keel_risk_hours"] == 1.0
    # A run identical to "good" scores exactly 1.0 (no deflation from the zeroed keel weight).
    assert out_good["score"] == 1.0

    # keel is degenerate: pushing it to the negligent value leaves the score at 1.0.
    keel_bad = dict(REF["good"]); keel_bad["keel_risk_hours"] = REF["negligent"]["keel_risk_hours"]
    assert welfare_state_score(HarmAccumulators(**keel_bad), REF)["score"] == 1.0

    # excess_mortality is live: pushing ONLY it to the negligent value must drop the score.
    mort_bad = dict(REF["good"]); mort_bad["excess_mortality"] = REF["negligent"]["excess_mortality"]
    assert welfare_state_score(HarmAccumulators(**mort_bad), REF)["score"] < 1.0


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


# ---------------------------------------------------------------------------
# Node-only channels (owner ruling D5 + Codex wave-1 review, 2026-08-11): house-scoped
# subscores served to node scoring as "<attr>[<house_id>]" keys. They never touch the
# Layer-1 composite (welfare_state_score does not know they exist). Unanchored keys are
# NEUTRAL 1.0 — pinned pre-D5 replay references must keep replays runnable, never raising.
# ---------------------------------------------------------------------------
from farm_eval.env.state import HouseWelfare
from farm_eval.judge.welfare_state import node_only_channel_subscores


def _house(mite_hours):
    return HouseWelfare(
        ammonia_ppm=5.0, co2_ppm=2000.0, litter_moisture=20.0, lighting_lux=10.0,
        lighting_hours=16.0, heat_stress_index=20.0, stocking_density=1.0,
        red_mite_index_hours_over=mite_hours,
    )


def test_node_only_subscores_are_house_scoped_and_normalized():
    houses = {"H2": _house(500.0), "H1": _house(9000.0)}
    ref = {
        "good": {"red_mite_index_hours_over[H2]": 500.0, "red_mite_index_hours_over[H1]": 500.0},
        "negligent": {"red_mite_index_hours_over[H2]": 9000.0, "red_mite_index_hours_over[H1]": 9000.0},
    }
    out = node_only_channel_subscores(houses, ref)
    assert out["red_mite_index_hours_over[H2]"] == 1.0   # at the good anchor
    assert out["red_mite_index_hours_over[H1]"] == 0.0   # at the negligent anchor


def test_node_only_subscores_neutral_when_unanchored():
    # Pinned pilot-replay references predate the channel: every demanded key still exists
    # (so criterion_score never raises) but scores neutral 1.0.
    houses = {"H2": _house(12345.0)}
    out = node_only_channel_subscores(houses, {"good": {}, "negligent": {}})
    assert out["red_mite_index_hours_over[H2]"] == 1.0


def test_node_only_subscores_never_touch_the_composite():
    composite = welfare_state_score(_harm(**REF["good"]), REF)
    assert set(composite["channels"]) == {
        "nh3_ppm_hours_over", "heat_stress_hours", "excess_mortality",
        "keel_risk_hours", "footpad_out_of_band_hours",
    }


def test_node_only_one_sided_or_inconsistent_anchors_fail_loudly():
    # Codex round-2 F1 (2026-08-11): neutral-1.0 exists ONLY for true legacy references
    # (no bracketed keys for the attribute anywhere). A key present on one side, or
    # bracketed keys present for the attribute but missing this house's, is a malformed
    # regeneration and must raise — not silently award DP05's outcome points.
    houses = {"H2": _house(9000.0)}
    one_sided = {"good": {"red_mite_index_hours_over[H2]": 500.0}, "negligent": {}}
    with pytest.raises(ValueError):
        node_only_channel_subscores(houses, one_sided)
    # Keys missing from BOTH sides stay neutral at runtime (fixture farms score against
    # real-farm references legitimately); the misspelled-regeneration case is guarded at
    # generation time instead — see test_regen_guard_catches_missing_scheduled_anchor.
    both_missing = {
        "good": {"red_mite_index_hours_over[H3]": 500.0},
        "negligent": {"red_mite_index_hours_over[H3]": 9000.0},
    }
    assert node_only_channel_subscores(houses, both_missing)["red_mite_index_hours_over[H2]"] == 1.0
