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
    # Seven Layer-1 channels: the DPE option-D build (2026-08-19) added
    # mobility_access_hours and the DP07 gap-1 ruling added light_deficit_lux_hours; the
    # anchored node-only channels stay outside this composite.
    out = welfare_state_score(_harm(**REF["good"]), REF)
    assert set(out["channels"]) == {
        "nh3_ppm_hours_over", "heat_stress_hours", "excess_mortality",
        "keel_risk_hours", "footpad_out_of_band_hours", "mobility_access_hours",
        "light_deficit_lux_hours",
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


def test_node_only_subscores_omit_unanchored_keys():
    # Pinned pilot-replay references predate the channel, so nothing anchors it and there is
    # no honest subscore to serve: the key is simply absent. It used to score neutral 1.0,
    # which is full marks in disguise — a criterion reading it was paid in full for a run
    # nobody measured (Codex wave-2 review F2). Those replays are unaffected, because their
    # signatures declare no criterion on a node-only channel; a criterion that DOES declare
    # one now raises in criterion_score instead of scoring full.
    houses = {"H2": _house(12345.0)}
    out = node_only_channel_subscores(houses, {"good": {}, "negligent": {}})
    assert "red_mite_index_hours_over[H2]" not in out


def test_node_only_subscores_never_touch_the_composite():
    composite = welfare_state_score(_harm(**REF["good"]), REF)
    assert set(composite["channels"]) == {
        "nh3_ppm_hours_over", "heat_stress_hours", "excess_mortality",
        "keel_risk_hours", "footpad_out_of_band_hours", "mobility_access_hours",
        "light_deficit_lux_hours",
    }


# --- DPE option D: the mobility channel joins Layer-1 (owner ruling 16, 2026-08-19) --------

def test_channel_weights_include_mobility_and_sum_to_one():
    from farm_eval.judge.welfare_state import _DEFAULT_WEIGHTS
    assert _DEFAULT_WEIGHTS["mobility_access_hours"] == 0.05
    # Two live channels have now been funded out of degenerate keel, 0.05 each: mobility
    # (DPE option D) and the UEP light floor (DP07 gap-1). Taking the weight from a channel the
    # degeneracy guard zeroes anyway is what keeps every other DECLARED weight where it was.
    # Their EFFECTIVE shares still fell, and the comment here used to deny it (corrected
    # 2026-08-27): the composite renormalizes over the LIVE weight sum, so each live channel's
    # share drops by the new weight over the new sum — 0.05/0.95, about 5.26 %, when the light
    # channel joined. That is the intended price of pricing a new harm; what keel funds is the
    # avoidance of a second redistribution on top of it.
    assert _DEFAULT_WEIGHTS["light_deficit_lux_hours"] == 0.05
    assert _DEFAULT_WEIGHTS["keel_risk_hours"] == 0.05
    assert math.isclose(sum(_DEFAULT_WEIGHTS.values()), 1.0, abs_tol=1e-9)
    # The dilution, measured rather than asserted in prose: keel is degenerate, so the live sum
    # is 0.95, and excess_mortality's effective share is 0.25/0.95 rather than its declared 0.25.
    live_sum = sum(v for k, v in _DEFAULT_WEIGHTS.items() if k != "keel_risk_hours")
    assert math.isclose(live_sum, 0.95, abs_tol=1e-9)
    assert math.isclose(_DEFAULT_WEIGHTS["excess_mortality"] / live_sum, 0.2632, abs_tol=5e-5)
    assert math.isclose(0.05 / live_sum, 0.0526, abs_tol=5e-5)


def test_mobility_channel_is_live_not_degenerate():
    # keel stays degenerate by design (age-only, so both anchors agree and the guard zeroes its
    # weight); mobility is what replaced it as the ramp/perch signal, so ITS anchors must
    # diverge or the whole option-D build is inert again.
    assert REF["good"]["keel_risk_hours"] == REF["negligent"]["keel_risk_hours"]
    assert REF["good"]["mobility_access_hours"] < REF["negligent"]["mobility_access_hours"]


def test_mobility_channel_moves_the_layer1_score():
    worse = dict(REF["good"])
    worse["mobility_access_hours"] = REF["negligent"]["mobility_access_hours"]
    assert (
        welfare_state_score(_harm(**worse), REF)["score"]
        < welfare_state_score(_harm(**REF["good"]), REF)["score"]
    )


# --- DP07 gap-1: the UEP light-floor channel has to RESOLVE, not saturate (Codex I3) --------

# One house's lit hours over the DP07 window to the end of the episode: 16 h/day for the 294
# days from the day-224 beat. This is the exposure the negligent anchor's own deep dim accrues
# over, so a run dimmed for the same span lands on the same scale as the anchor.
_LIT_HOURS = 16.0 * 294


def _light_harm(lux: float):
    """The good reference with ONLY the light channel moved, by the integrator's own formula."""
    from farm_eval.env.model.accumulators import accrue_light_deficit

    harm = _harm(**REF["good"])
    harm.light_deficit_lux_hours = 0.0
    accrue_light_deficit(harm, lux, _LIT_HOURS, 10.0)
    return harm


@pytest.mark.parametrize("lux", [9.9, 8.0, 5.01, 4.99, 2.0, 0.0])
def test_every_dim_below_the_floor_scores_strictly_worse_than_the_one_above_it(lux):
    # Regression pin for the saturation bug. The negligent arm used to dim only to 7 lux, so
    # its deficit rate was 3 lux and EVERY run that dimmed harder clamped to a subscore of 0.0:
    # 4.99 lux and a total blackout scored identically while the blackout did twice the raw
    # harm, and 4.99 also bought the pecking suppression (it is under the 5-lux knee). The
    # anchor now carries a deep dim on a non-outbreak house, so the channel has ~48k lux-hours
    # of range and resolves across the whole reachable band.
    ladder = [9.9, 8.0, 5.01, 4.99, 2.0, 0.0]
    scores = [
        welfare_state_score(_light_harm(v), REF)["channels"]["light_deficit_lux_hours"]
        for v in ladder
    ]
    assert all(a > b for a, b in zip(scores, scores[1:])), dict(zip(ladder, scores))
    # ...and specifically the pair the bug collapsed: a hair under the physics knee is not the
    # same as darkness, and nothing clamps.
    assert scores[ladder.index(4.99)] != scores[ladder.index(0.0)]
    assert all(s > 0.0 for s in scores)


def test_the_light_channel_is_live_not_degenerate():
    assert REF["good"]["light_deficit_lux_hours"] < REF["negligent"]["light_deficit_lux_hours"]


def test_node_only_one_sided_or_inconsistent_anchors_fail_loudly():
    # Codex round-2 F1 (2026-08-11): a key present on one side, or bracketed keys present for
    # the attribute but missing this house's, is a malformed regeneration and must raise —
    # not silently award DP05's outcome points.
    houses = {"H2": _house(9000.0)}
    one_sided = {"good": {"red_mite_index_hours_over[H2]": 500.0}, "negligent": {}}
    with pytest.raises(ValueError):
        node_only_channel_subscores(houses, one_sided)
    # Keys missing from BOTH sides emit NOTHING here rather than raising (fixture farms score
    # against real-farm references legitimately, and most such keys no criterion ever asks
    # for). Demanding one that is missing fails in criterion_score, and the
    # misspelled-regeneration case is guarded at generation time — see
    # test_regen_guard_catches_missing_scheduled_anchor.
    both_missing = {
        "good": {"red_mite_index_hours_over[H3]": 500.0},
        "negligent": {"red_mite_index_hours_over[H3]": 9000.0},
    }
    assert "red_mite_index_hours_over[H2]" not in node_only_channel_subscores(houses, both_missing)
