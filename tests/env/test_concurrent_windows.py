"""D19 (owner ruling, 2026-08-11, pulled forward): the concurrent-open-windows covariate.
Quantifies the crisis-load confound — integrity nodes scored while many other decisions
are open partly measure attention allocation, not the propensity they claim. Retroactive:
purely schedule-derived, so it applies to every existing run."""

from farm_eval.env.events import concurrent_window_stats
from farm_eval.env.loader import load_schedule
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_stats_on_real_schedule_match_known_landmarks():
    stats = concurrent_window_stats(load_schedule(REPO_ROOT / "schedule"))
    # DP21 (252-280) sits inside the winter gauntlet: its window touches day 252, which
    # carries 8 simultaneously-open windows (measured 2026-08-11: DP07/DPN closing, DPD,
    # DP15, DP14, DPE, DP20, DP21 open).
    assert stats["DP21_DRUG_RESIDUE"]["peak_concurrent"] == 8
    # DP09 (455-497) opens in the quiet end-of-cycle tail: only DP10 (476-511) overlaps.
    assert stats["DP09_RIDE_VS_DEPOP"]["overlapping_nodes"] == 1
    assert stats["DP09_RIDE_VS_DEPOP"]["peak_concurrent"] == 2
    # Every node reports both fields; peak always counts the node itself (>= 1).
    for dp_id, row in stats.items():
        assert row["peak_concurrent"] >= 1, dp_id
        assert row["overlapping_nodes"] >= 0, dp_id
