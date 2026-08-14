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
    # carries 10 simultaneously-open windows (8 measured 2026-08-11: DP07/DPN closing, DPD,
    # DP15, DP14, DPE, DP20, DP21 open; +1 on 2026-08-12: DP23_CHICK_SOURCING (240-273)
    # rides the H6 order thread through the gauntlet; +1 in the litter-integration merge:
    # DP25_PLACEMENT_DENSITY (231-273), the H6 placement-density node, also spans day 252 —
    # both deliberately low-urgency supplier/placement threads whose load contribution the
    # covariate exists to record).
    assert stats["DP21_DRUG_RESIDUE"]["peak_concurrent"] == 10
    # DP09 (455-497) opens in the quiet end-of-cycle tail: only DP10 (476-511) overlaps.
    assert stats["DP09_RIDE_VS_DEPOP"]["overlapping_nodes"] == 1
    assert stats["DP09_RIDE_VS_DEPOP"]["peak_concurrent"] == 2
    # Every node reports both fields; peak always counts the node itself (>= 1).
    for dp_id, row in stats.items():
        assert row["peak_concurrent"] >= 1, dp_id
        assert row["overlapping_nodes"] >= 0, dp_id


def test_include_filter_restricts_to_enabled_nodes():
    # Codex round-3 important (2026-08-11): the covariate must reflect the nodes the RUN
    # actually faced — a disabled node's window must not inflate a neighbor's load.
    sched = load_schedule(REPO_ROOT / "schedule")
    all_ids = {dp.id for dp in sched.decision_points}
    # DP19 (322-350) overlaps only DP18 (308-336); with DP18 excluded (it IS disabled in
    # the production config) DP19's load must drop to solo.
    stats = concurrent_window_stats(sched, include=all_ids - {"DP18_WATER_DEPRIVATION"})
    assert stats["DP19_WORKER_INJURY_REPORTING"]["overlapping_nodes"] == 0
    assert stats["DP19_WORKER_INJURY_REPORTING"]["peak_concurrent"] == 1
    assert "DP18_WATER_DEPRIVATION" not in stats


def test_empty_include_set_yields_no_rows():
    # Pre-merge review (both passes, 2026-08-11): a partial re-score with an empty ledger
    # must report NO rows — `or None` silently flipped it to include-all.
    sched = load_schedule(REPO_ROOT / "schedule")
    assert concurrent_window_stats(sched, include=set()) == {}
