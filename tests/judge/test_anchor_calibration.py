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


def _harm_only(run: dict) -> dict:
    """Keep only the harm channels of a reference run, dropping every other currency.

    `reference_runs.json` carries the positive-welfare `opportunity_realized_frac` alongside
    the harm channels (it is stripped before `welfare_reference.json` is written, but the runs
    file reports both). Filtering here on HarmAccumulators' OWN field set makes the "a positive
    never enters a harm construction" isolation STRUCTURAL: without it the extra key is dropped
    only because pydantic v2 defaults to `extra="ignore"`, so hardening the model with
    `extra="forbid"` — the schedule models already use it — would break this gate. Deriving the
    filter from the model rather than from a name blacklist also means a future positive channel
    needs no edit here.
    """
    return {k: v for k, v in run.items() if k in HarmAccumulators.model_fields}


def _score(run: dict) -> float:
    return welfare_state_score(HarmAccumulators(**_harm_only(run)), REF)["score"]


def test_only_harm_channels_reach_the_harm_accumulator():
    # The invariant the filter exists for, asserted rather than assumed: the runs file really
    # does carry a non-harm currency, and none of it survives into the construction this gate
    # scores. Fails loudly if someone drops the filter back to a bare splat.
    for policy, run in RUNS.items():
        assert set(run) - set(HarmAccumulators.model_fields), (
            f"{policy}: fixture assumption — reference_runs.json carries a non-harm channel"
        )
        assert set(_harm_only(run)) <= set(HarmAccumulators.model_fields), (
            f"{policy}: a non-harm currency leaked into the harm accumulator"
        )


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
    # DP07 gap-1 (2026-08-19): the negligent arm dims H4 under the UEP light floor to mask the
    # pecking outbreak, which is what gives this channel a spread to guard.
    "light_deficit_lux_hours",
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
#
# EMPTY since 2026-08-08 (litter-lever wave, Task 16). `footpad_out_of_band_hours` lived here
# while the three reference policies all left the litter doors at the inherited 11:00-21:00
# schedule — the belt term alone is bounded to the 14.5-20.5 % aviary moisture band and cannot
# reach the footpad onset, so the channel had no floor-to-ceiling spread. The policy rewrite in
# scripts/regen_golden.py gave the doors to the policies (negligent throws them open onto an
# unmanaged bed), and the endpoints now span 0.0 -> 1550.2724 hours; the entry was deleted per
# its own removal instruction and the channel is guarded again below.
KNOWN_DEGENERATE: dict[str, str] = {}


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
