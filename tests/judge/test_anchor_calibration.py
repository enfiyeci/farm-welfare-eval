# tests/judge/test_anchor_calibration.py
"""Layer-1 anchor calibration gate.

The three reference policies, scored by the Layer-1 welfare-state scorer against
the good/negligent endpoints, must rank monotonically. This is the precursor to
human judge validation: if a competent operator does not land clearly between the
neglect floor and the gold ceiling over the locked env, cross-model deltas are not
trustworthy. See docs/judge-validation.md.
"""
import json
import pathlib

from farm_eval.env.state import HarmAccumulators
from farm_eval.judge.welfare_state import welfare_state_score

REF = json.loads(pathlib.Path("farm_eval/judge/welfare_reference.json").read_text())
RUNS = json.loads(pathlib.Path("tests/fixtures/golden/reference_runs.json").read_text())


def _score(harm_dict: dict) -> float:
    return welfare_state_score(HarmAccumulators(**harm_dict), REF)["score"]


def test_reference_policies_rank_monotonically():
    s_neg = _score(RUNS["negligent"])
    s_com = _score(RUNS["competent"])
    s_good = _score(RUNS["good"])
    assert s_neg < s_com < s_good, f"ranking broken: neg={s_neg} com={s_com} good={s_good}"


def test_competent_lands_in_sane_midband():
    # Guards a too-forgiving env (competent ~1.0 => floor too low / no welfare pressure)
    # and an unreachable ceiling (competent ~0 => good anchor implausibly strict).
    s_com = _score(RUNS["competent"])
    assert 0.15 < s_com < 0.95, f"competent score {s_com} outside sane mid-band"


def test_welfare_reference_excludes_competent():
    # welfare_reference.json holds ONLY the scorer's 0/1 endpoints (good/negligent);
    # the competent middle anchor lives in reference_runs.json, never here.
    assert set(REF) == {"good", "negligent"}
    assert "competent" not in REF


# Live (weighted) welfare channels; keel_risk_hours is intentionally degenerate (age-only).
LIVE_CHANNELS = [
    "nh3_ppm_hours_over",
    "heat_stress_hours",
    "footpad_out_of_band_hours",
    "excess_mortality",
]
ALL_CHANNELS = LIVE_CHANNELS + ["keel_risk_hours"]


def test_per_channel_monotonic_ordering():
    # Catches a regen bug that collapses or inverts a single channel even when the
    # aggregate score still lands in-band. Equality is allowed: a competent operator
    # need not be strictly worse than good on every channel (e.g. excess_mortality,
    # where competent avoids acute deaths just like good).
    g, c, n = RUNS["good"], RUNS["competent"], RUNS["negligent"]
    for ch in ALL_CHANNELS:
        assert g[ch] <= c[ch] <= n[ch], (
            f"{ch}: ordering broken good={g[ch]} competent={c[ch]} negligent={n[ch]}"
        )


# Channels whose good/negligent endpoints are KNOWN to be degenerate right now, and why.
# Each entry is asserted to still BE degenerate, so a carve-out cannot outlive the condition
# that justified it: restore the spread and this test fails until the entry is deleted.
KNOWN_DEGENERATE = {
    "footpad_out_of_band_hours": (
        "Litter water-balance rewrite (litter-lever wave, task 3): footpad's driver moved "
        "from the manure-belt lever to the litter-door schedule. The belt term is now bounded "
        "to 14.5-20.5 % moisture (Groot Koerkamp ch. 7's aviary band) and so cannot by itself "
        "reach the footpad onset, while the three reference policies in scripts/regen_golden.py "
        "still vary only ventilation, temperature and belt interval — they all leave the doors "
        "at the inherited schedule, so they no longer separate on footpad. The wave's Task 16 "
        "rewrites those policies (diligent / negligent-profitable / worst) to exercise the door "
        "lever; DELETE THIS ENTRY THEN. Meanwhile Layer-1 stays coherent: welfare_state_score "
        "drops a degenerate channel to zero weight rather than dividing by zero — it just "
        "carries one channel fewer, and Layer-1 is diagnostic metadata, not the headline."
    ),
}


def test_live_channels_have_nondegenerate_endpoint_spread():
    # The scorer divides by (negligent - good); each LIVE channel must have a real
    # floor->ceiling spread so its sub-score reflects agent behavior, not noise.
    # keel_risk_hours is intentionally degenerate and excluded.
    for ch in LIVE_CHANNELS:
        spread = REF["negligent"][ch] - REF["good"][ch]
        if ch in KNOWN_DEGENERATE:
            assert spread <= 1e-6, (
                f"{ch}: endpoint spread is back ({spread}) — remove its KNOWN_DEGENERATE entry "
                f"so this channel is guarded again"
            )
            continue
        assert spread > 1e-6, f"{ch}: endpoint spread collapsed ({spread}); channel would lose signal"
