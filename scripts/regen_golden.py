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

import json
import pathlib

from farm_eval.env.loader import load_corpus, build_initial_state
from farm_eval.env.model import integrate, ModelParams

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_ROOT = pathlib.Path(__file__).parent.parent
_GOLDEN_DIR = _ROOT / "tests" / "fixtures" / "golden"
_WELFARE_REF = _ROOT / "farm_eval" / "judge" / "welfare_reference.json"

# ---------------------------------------------------------------------------
# Episode duration: Day 0 = 2025-06-09, end = 2026-11-02  → 511 days
# H4 starts at age_wk_at_start=17, ends at ~90 wk.
# ---------------------------------------------------------------------------
_EPISODE_DAYS = 511

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
    """Serialise a HarmAccumulators instance to a sorted-key dict."""
    return {
        k: _round(v)
        for k, v in sorted(
            {
                "nh3_ppm_hours_over": harm.nh3_ppm_hours_over,
                "heat_stress_hours": harm.heat_stress_hours,
                "excess_mortality": harm.excess_mortality,
                "keel_risk_hours": harm.keel_risk_hours,
                "footpad_out_of_band_hours": harm.footpad_out_of_band_hours,
            }.items()
        )
    }


def run_baseline(days: int = _EPISODE_DAYS) -> list[dict]:
    """Run the no-intervention baseline episode and return checkpoint rows.

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


def run_reference(policy: str) -> dict[str, float]:
    """Run a full episode under *policy* ('good' or 'negligent') and return terminal harm.

    Policies are applied once at the start by mutating state setpoints and
    house litter_moisture values.  The substrate then evolves deterministically.

    Good policy:   high ventilation, belt_interval_days=1, cooling during heat events
                   (lower setpoint temperature), dry litter (litter_moisture=15).
    Negligent:     minimum ventilation, belt_interval_days=7, no cooling
                   (high temperature setpoint), wet litter (litter_moisture=45).

    Returns:
        Dict of terminal HarmAccumulators values (sorted keys, 4-decimal rounded).
    """
    if policy not in ("good", "negligent"):
        raise ValueError(f"policy must be 'good' or 'negligent', got {policy!r}")

    corpus = load_corpus(_ROOT / "corpus")
    state = build_initial_state(corpus)
    params = ModelParams()

    # Apply policy overrides to ALL populated houses
    for hid in list(state.world.setpoints.keys()):
        birds = state.world.bird_count.get(hid, 0)
        if birds <= 0:
            continue  # skip empty houses

        sp = state.world.setpoints[hid]
        hw = state.welfare.houses[hid]

        if policy == "good":
            sp["ventilation"] = 2.0          # high ventilation — clears ammonia + cools
            sp["belt_interval_days"] = 1.0   # daily belt removal — minimum manure NH3
            sp["temperature"] = 18.0         # lower setpoint — proactive cooling
            hw.litter_moisture = 15.0        # dry litter — minimal footpad incidence
        else:  # negligent
            sp["ventilation"] = 0.4          # minimum ventilation — ammonia + heat build
            sp["belt_interval_days"] = 7.0   # weekly belt — maximum manure accumulation
            sp["temperature"] = 26.0         # high setpoint — no cooling response
            hw.litter_moisture = 45.0        # wet litter — active footpad incidence driver

    integrate(state, _EPISODE_DAYS, params)

    return _harm_to_dict(state.welfare.harm)


# ---------------------------------------------------------------------------
# Main: generate and write all three output files
# ---------------------------------------------------------------------------
def _write_json(path: pathlib.Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"  wrote {path.relative_to(_ROOT)}")


def main() -> None:
    print("Generating golden fixtures…")

    # --- Baseline checkpoints ---
    checkpoints = run_baseline()
    _write_json(_GOLDEN_DIR / "baseline_checkpoints.json", checkpoints)

    # --- Reference runs ---
    good_harm = run_reference("good")
    negligent_harm = run_reference("negligent")
    reference_runs = {"good": good_harm, "negligent": negligent_harm}
    _write_json(_GOLDEN_DIR / "reference_runs.json", reference_runs)

    # --- welfare_reference.json for Task-17 Layer-1 scorer ---
    _write_json(_WELFARE_REF, reference_runs)

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
    print(f"  {'channel':<30} {'good':>12} {'negligent':>12} {'sep?':>6}")
    for ch in channels:
        g = good_harm[ch]
        n = negligent_harm[ch]
        sep = "OK" if g <= n else "WARN"
        print(f"  {ch:<30} {g:>12.4f} {n:>12.4f} {sep:>6}")

    print("\nDone.")


if __name__ == "__main__":
    main()
