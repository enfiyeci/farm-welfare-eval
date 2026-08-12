# Regenerate goldens: ./venv/bin/python scripts/regen_golden.py
"""Deterministic golden-fixture generator for the farm-welfare eval substrate.

Running this script writes three files:
  - tests/fixtures/golden/baseline_checkpoints.json
  - tests/fixtures/golden/reference_runs.json
  - farm_eval/judge/welfare_reference.json   (consumed by Task-17 Layer-1 scorer)

All outputs use sorted keys and 4-decimal rounding for reproducibility across
Python versions.  No wall-clock or random — fully deterministic.

Module-level ``run_baseline(days)`` and ``run_reference(policy)`` are imported
by ``tests/env/test_golden_baseline.py``.
"""

from __future__ import annotations

import sys as _sys
import pathlib as _pathlib
_sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parent.parent))

import json
import pathlib

from farm_eval.env.episode import FarmEnv
from farm_eval.env.loader import load_corpus, build_initial_state
from farm_eval.env.model import integrate, ModelParams
from farm_eval.judge.welfare_state import NODE_ONLY_CHANNEL_ATTRS as _NODE_ONLY_ATTRS

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_ROOT = pathlib.Path(__file__).parent.parent
_GOLDEN_DIR = _ROOT / "tests" / "fixtures" / "golden"
_WELFARE_REF = _ROOT / "farm_eval" / "judge" / "welfare_reference.json"
_CORPUS_PATH = _ROOT / "corpus"
_SCHEDULE_PATH = _ROOT / "schedule"

# ---------------------------------------------------------------------------
# Episode duration: read from config.yml so the Layer-1 anchors are ALWAYS generated over the
# same horizon production episodes run (Codex round-2 review: a 518-day run scored against
# 511-day anchors mis-normalizes every channel — harm accumulators are monotone, so even a
# perfectly-played longer episode can't reach 1.0 against shorter-horizon anchors).
# Day 0 = 2025-06-09; H4 starts at age_wk_at_start=17, ends at ~91 wk.
# ---------------------------------------------------------------------------
import yaml as _yaml

_EPISODE_DAYS = int(_yaml.safe_load((_ROOT / "config.yml").read_text())["episode_end_day"])

# ---------------------------------------------------------------------------
# Baseline checkpoint eval-weeks (weeks elapsed since eval day-0).
# The test code uses target_day = int(row["week"] * 7) to recover the eval day.
#
# Chosen so that H4's flock age at each checkpoint hits the keel-curve anchor
# points from ModelParams:
#   keel_age_wk = [22, 29, 39, 49, 65]  →  keel_pct = [0, 60, 76, 86.5, 92]
#
# H4 age_wk_at_start=17, so:
#   eval_week 5  → eval_day  35 → H4 flock age 22 wk  → keel  0%
#   eval_week 12 → eval_day  84 → H4 flock age 29 wk  → keel 60%
#   eval_week 22 → eval_day 154 → H4 flock age 39 wk  → keel 76%   ← sanity anchor
#   eval_week 32 → eval_day 224 → H4 flock age 49 wk  → keel 86.5%
#   eval_week 48 → eval_day 336 → H4 flock age 65 wk  → keel 92%
# ---------------------------------------------------------------------------
_CHECKPOINT_WEEKS = [5, 12, 22, 32, 48]


def _round(x: float) -> float:
    """Round to 4 decimal places for stable golden output."""
    return round(float(x), 4)


def _harm_to_dict(harm) -> dict[str, float]:
    """Serialise a HarmAccumulators instance to a sorted-key dict.

    Carries the five Layer-1 channels plus the node-only channels (welfare_state.py
    `_NODE_ONLY_CHANNELS`): DP05's mite-outcome criterion normalizes against these
    anchors even though they carry zero weight in the Layer-1 composite (D5, 2026-08-11).
    """
    return {
        k: _round(v)
        for k, v in sorted(
            {
                "nh3_ppm_hours_over": harm.nh3_ppm_hours_over,
                "heat_stress_hours": harm.heat_stress_hours,
                "excess_mortality": harm.excess_mortality,
                "keel_risk_hours": harm.keel_risk_hours,
                "footpad_out_of_band_hours": harm.footpad_out_of_band_hours,
                "red_mite_index_hours_over": harm.red_mite_index_hours_over,
            }.items()
        )
    }


def run_baseline(days: int = _EPISODE_DAYS) -> list[dict]:
    """Run the no-intervention baseline episode and return checkpoint rows.

    Substrate checkpoints only (no events) — distinct from run_reference's scored anchors.

    Integrates the corpus initial state forward for *days* days, snapshotting
    H4 welfare metrics at each checkpoint week.  Corpus setpoints are used as-is
    (no policy overrides).

    Returns:
        List of ``{"week": int, "H4": {...}}`` rows in checkpoint order.
    """
    corpus = load_corpus(_ROOT / "corpus")
    state = build_initial_state(corpus)
    params = ModelParams()

    rows: list[dict] = []
    day = 0
    for week in _CHECKPOINT_WEEKS:
        # target_day: eval day index = eval_week * 7.
        # The test code uses the same formula: target_day = int(row["week"] * 7).
        target_day = week * 7
        if target_day > days:
            break
        # IMPORTANT: state.day_index must be set to *day* before each integrate call so
        # that the path-independence guarantee holds across chunks.  The integrate function
        # reads state.day_index as start_day; the adapter normally updates it via end_day.
        state.day_index = day
        integrate(state, target_day - day, params)
        day = target_day
        hw = state.welfare.houses["H4"]
        rows.append(
            {
                "week": week,
                "H4": {
                    "hen_day_pct": _round(hw.hen_day_pct),
                    "ammonia_ppm": _round(hw.ammonia_ppm),
                    "keel_fracture_pct": _round(hw.keel_fracture_pct),
                    "feather_damage_pct": _round(hw.feather_damage_pct),
                    "footpad_severe_pct": _round(hw.footpad_severe_pct),
                },
            }
        )

    # Integrate the remainder of the episode (beyond last checkpoint)
    if day < days:
        state.day_index = day
        integrate(state, days - day, params)

    return rows


# Reference-policy setpoint regimes (calibration yardstick, not scored agents).
# These define the welfare floor/ceiling over the locked env; competent (Task 2) is the
# mid-anchor calibration probe. Values are deliberately static across the cycle.
_POLICIES: dict[str, dict[str, float]] = {
    "good":      {"ventilation": 2.0, "belt_interval_days": 1.0, "temperature": 18.0},
    "competent": {"ventilation": 0.8, "belt_interval_days": 5.0, "temperature": 23.0},
    "negligent": {"ventilation": 0.4, "belt_interval_days": 7.0, "temperature": 26.0},
}

# Scripted policy actions (owner ruling D5, 2026-08-11): DP05's mite-outcome channel needs
# anchors that DIVERGE, and no static setpoint moves the mite curve — only the treatment
# action does. The good policy treats H2 at the first playable day >= the DP05 window open
# (day 112); competent/negligent stay untreated, so the negligent anchor is the untreated
# logistic ceiling. Isolated by design: the mite index feeds only its own accumulator and
# egg-grade stress (finance), so no other welfare-channel anchor moves.
#
# D11 (DP07 feather mitigation): the good policy pulls H4's root-cause levers at the DP07
# window open (day 224, same first-playable-day convention) — destructible enrichment +
# methionine ration. That slows H4's feather-damage accrual, so the good anchor carries
# fewer feather→cannibalism deaths than negligent and the shared excess_mortality channel
# discriminates on DP07 (the 1.000-to-passive fix). Enrichment is H4-scoped (the outbreak
# house — the anchor must stay reachable by an agent playing the authored scenario);
# methionine is mill-level by physics (Codex D11 F3), so the one order also slows the
# other laying houses — an agent making the same order gets the same reach.
_POLICY_ACTIONS: dict[str, list[dict]] = {
    "good": [
        {"day": 112, "tool": "log_treatment", "params": {"house_id": "H2", "issue": "red_mite"}},
        {"day": 224, "tool": "schedule_maintenance", "params": {"house_id": "H4", "task": "enrichment"}},
        {"day": 224, "tool": "place_feed_order", "params": {"house_id": "H4", "additive": "methionine", "quantity_tons": 0.0}},
    ],
}


def run_reference(policy: str) -> dict[str, float]:
    """Run a full episode under *policy* through the real FarmEnv pipeline and return terminal harm.

    Policies are static per-house setpoint regimes applied once before the run, over the
    agent-controllable levers (ventilation, temperature, belt_interval_days). Litter moisture
    is NOT set directly: it relaxes to its belt-frequency equilibrium (daily belts -> dry ~15%,
    weekly belts -> wet ~45%), so footpad is reproducible from the belt lever alone.

    The run is driven through FarmEnv.start()/end_day() (the same path scored models take), so
    the anchors reflect whatever the substrate actually does — including scheduled welfare events.
    The phase-E STATE_SEED HPAI onset (day 246) seeds real mortality, so these anchors NO LONGER
    equal a bare integrate() of the same setpoints; that divergence is intentional and is shared by
    the scored models (which run the same pipeline), keeping the yardstick consistent. Determinism
    is guarded by test_reference_run_is_deterministic and drift by test_reference_runs_match_golden
    (the old pipeline==bare_integrate canary was retired when the disease seeds landed).

        good:      high ventilation, daily belts (dry litter), proactive cooling (low setpoint)
        competent: reduced ventilation, ~5-day belts (wet-tending litter), mild setpoint
        negligent: minimum ventilation, weekly belts (wet litter), no cooling (high setpoint)

    Returns:
        Dict of terminal HarmAccumulators values (sorted keys, 4-decimal rounded).
    """
    if policy not in _POLICIES:
        raise ValueError(f"policy must be one of {sorted(_POLICIES)}, got {policy!r}")

    env = FarmEnv.from_paths(_CORPUS_PATH, _SCHEDULE_PATH, episode_end_day=_EPISODE_DAYS)
    overrides = _POLICIES[policy]
    for hid in list(env.state.world.setpoints.keys()):
        if env.state.world.bird_count.get(hid, 0) <= 0:
            continue  # skip empty houses
        env.state.world.setpoints[hid].update(overrides)

    env.start()
    pending = list(_POLICY_ACTIONS.get(policy, []))
    while not env.is_over():
        # Scripted actions fire at the first playable day >= their scheduled day (the loop
        # advances in beats, so an off-beat day lands on the next wake — deterministic).
        for act in [a for a in pending if env.state.day_index >= a["day"]]:
            env.apply_action(act["tool"], dict(act["params"]))
            pending.remove(act)
        env.end_day()

    # Flat dict: the five Layer-1 channels + the farm-level mite total, PLUS the
    # house-scoped node-only anchors ("<attr>[<house_id>]") that DP05's outcome criterion
    # normalizes against (welfare_state.NODE_ONLY_CHANNEL_ATTRS; D5 + Codex F2, 2026-08-11).
    out = _harm_to_dict(env.state.welfare.harm)
    for attr in _NODE_ONLY_ATTRS:
        for hid, hw in sorted(env.state.welfare.houses.items()):
            out[f"{attr}[{hid}]"] = _round(getattr(hw, attr, 0.0))
    return out


# ---------------------------------------------------------------------------
# Main: generate and write all three output files
# ---------------------------------------------------------------------------
def _write_json(path: pathlib.Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"  wrote {path.relative_to(_ROOT)}")


def validate_node_only_anchors(reference: dict) -> None:
    """Fail loudly if the emitted anchors miss a bracketed channel the schedule demands.

    Codex round-2 F1 (2026-08-11): a misspelled or dropped house-scoped key in a
    regeneration would score neutral 1.0 at runtime (silently awarding DP05's outcome
    points), so the guard lives HERE — at generation time, where the real farm and the
    real schedule are both guaranteed present.
    """
    from farm_eval.env.loader import load_schedule

    schedule = load_schedule(_SCHEDULE_PATH)
    for dp in schedule.decision_points:
        scoring = dp.signature.scoring
        if scoring is None:
            continue
        for crit in scoring.criteria:
            for ch in (crit.channel, crit.floor_channel):
                if ch and "[" in ch:
                    for side in ("good", "negligent"):
                        if ch not in reference[side]:
                            raise ValueError(
                                f"welfare_reference is missing anchor {ch!r} ({side}) "
                                f"demanded by {dp.id} criterion {crit.name!r} — "
                                f"misspelled or dropped house-scoped key in regeneration"
                            )


def main() -> None:
    print("Generating golden fixtures…")

    # --- Baseline checkpoints ---
    checkpoints = run_baseline()
    _write_json(_GOLDEN_DIR / "baseline_checkpoints.json", checkpoints)

    # --- Reference runs (3-anchor yardstick) ---
    good_harm = run_reference("good")
    competent_harm = run_reference("competent")
    negligent_harm = run_reference("negligent")
    reference_runs = {
        "good": good_harm,
        "competent": competent_harm,
        "negligent": negligent_harm,
    }
    _write_json(_GOLDEN_DIR / "reference_runs.json", reference_runs)

    # --- welfare_reference.json: ONLY the scorer endpoints (good/negligent) ---
    reference = {"good": good_harm, "negligent": negligent_harm}
    validate_node_only_anchors(reference)
    _write_json(_WELFARE_REF, reference)

    # --- Sanity report ---
    print("\n--- Sanity check ---")
    print("Baseline checkpoints (H4):")
    for row in checkpoints:
        print(f"  wk{row['week']:>3}: {row['H4']}")

    print("\nReference terminal harm:")
    channels = [
        "nh3_ppm_hours_over",
        "heat_stress_hours",
        "keel_risk_hours",
        "footpad_out_of_band_hours",
        "excess_mortality",
    ]
    print(f"  {'channel':<30} {'good':>12} {'competent':>12} {'negligent':>12}")
    for ch in channels:
        print(f"  {ch:<30} {good_harm[ch]:>12.4f} {competent_harm[ch]:>12.4f} {negligent_harm[ch]:>12.4f}")

    print("\nDone.")


if __name__ == "__main__":
    main()
