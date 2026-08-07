"""P8 — read-only spacing audit of the schedule (spec §3 P8). Measures; never edits."""

from pathlib import Path

import yaml

from farm_eval.env.loader import Schedule, load_schedule
from farm_eval.env.schedule_models import (
    ActionMatch,
    ClassMatch,
    DecisionPoint,
    ScheduledEvent,
    Signature,
)
from farm_eval.probe.schedule_audit import audit_schedule, render_schedule_report

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_audit_real_schedule_shape_and_determinism():
    schedule = load_schedule(REPO_ROOT / "schedule")
    a = audit_schedule(schedule)
    b = audit_schedule(schedule)
    assert a == b  # deterministic
    assert a["decision_gaps"], "real schedule has >1 decision point"
    # dead_air entries, when present, are all genuinely >30-day windows with sane bounds
    for w in a["dead_air"]:
        assert w["gap_days"] > 30 and w["to_day"] - w["from_day"] == w["gap_days"]
    assert isinstance(a["cadence_flag"], bool)
    assert sum(a["by_category"].values()) == len(schedule.decision_points)


def test_render_report_lists_dead_air_and_cadence():
    schedule = load_schedule(REPO_ROOT / "schedule")
    report = render_schedule_report(audit_schedule(schedule))
    assert "dead-air" in report.lower()
    assert "cadence" in report.lower()
    assert "irregular spacing is good" in report.lower()  # the design rule stays visible


def test_end_day_none_is_unchanged_default():
    # Existing callers/tests must keep seeing exactly the observed-days-only behavior.
    schedule = load_schedule(REPO_ROOT / "schedule")
    assert audit_schedule(schedule) == audit_schedule(schedule, end_day=None)


def test_end_day_reveals_tail_dead_air():
    dp = DecisionPoint(id="DP1", category="initiative", opens_day=10, deadline_day=15)
    schedule = Schedule(decision_points=[dp], events=[ScheduledEvent(on_day=10, type="email")])
    audit = audit_schedule(schedule, end_day=100)
    assert {"from_day": 10, "to_day": 100, "gap_days": 90} in audit["dead_air"]


def test_end_day_reveals_head_dead_air():
    dp = DecisionPoint(id="DP1", category="initiative", opens_day=50, deadline_day=55)
    schedule = Schedule(decision_points=[dp], events=[ScheduledEvent(on_day=50, type="email")])
    audit = audit_schedule(schedule, end_day=100)
    assert {"from_day": 0, "to_day": 50, "gap_days": 50} in audit["dead_air"]


def test_end_day_no_tail_window_when_horizon_close():
    dp = DecisionPoint(id="DP1", category="initiative", opens_day=10, deadline_day=15)
    schedule = Schedule(decision_points=[dp], events=[ScheduledEvent(on_day=10, type="email")])
    audit = audit_schedule(schedule, end_day=20)
    assert audit["dead_air"] == []


def test_real_schedule_full_horizon_includes_boundary_without_crashing():
    # The real schedule's last observed activity (event or decision-open) is day 497 — only
    # 14 days short of the day-511 horizon, so no >30-day tail actually exists here. This
    # pins that full-horizon mode is wired end-to-end (boundary considered, no false positive
    # manufactured) without hardcoding a tail window the real content doesn't have.
    schedule = load_schedule(REPO_ROOT / "schedule")
    config = yaml.safe_load((REPO_ROOT / "config.yml").read_text(encoding="utf-8"))
    end_day = config["episode_end_day"]
    audit = audit_schedule(schedule, end_day=end_day)
    for w in audit["dead_air"]:
        assert w["gap_days"] > 30 and w["to_day"] - w["from_day"] == w["gap_days"]
    assert all(w["to_day"] <= end_day for w in audit["dead_air"])


def test_target_house_id_attributed_to_by_house():
    dp = DecisionPoint(
        id="DP_TARGET",
        category="false_binary",
        opens_day=0,
        deadline_day=5,
        signature=Signature(
            kind="classified",
            classes={
                "root_cause": ClassMatch(
                    all_of=[ActionMatch(tool="place_feed_order", where={"target": "H6", "genetics": "low_pecking"})]
                ),
                "default": ClassMatch(default=True),
            },
        ),
    )
    schedule = Schedule(decision_points=[dp], events=[])
    audit = audit_schedule(schedule)
    assert audit["by_house"] == {"H6": 1}


def test_target_ignored_when_not_house_shaped():
    dp = DecisionPoint(
        id="DP_TARGET",
        category="false_binary",
        opens_day=0,
        deadline_day=5,
        signature=Signature(
            kind="classified",
            classes={
                "root_cause": ClassMatch(all_of=[ActionMatch(tool="schedule_maintenance", where={"target": "enrichment"})]),
                "default": ClassMatch(default=True),
            },
        ),
    )
    schedule = Schedule(decision_points=[dp], events=[])
    audit = audit_schedule(schedule)
    assert audit["by_house"] == {"-": 1}


def test_real_schedule_beak_trimming_attributed_to_h6():
    schedule = load_schedule(REPO_ROOT / "schedule")
    assert any(d.id == "DPD_BEAK_TRIMMING" for d in schedule.decision_points)
    audit = audit_schedule(schedule)
    assert audit["by_house"].get("H6", 0) >= 1


def test_committed_report_is_byte_equal_to_regeneration():
    # Staleness guard: the committed report must always match a fresh full-horizon
    # regeneration, so a schedule edit without re-running scripts/audit_schedule.py fails loudly.
    schedule = load_schedule(REPO_ROOT / "schedule")
    config = yaml.safe_load((REPO_ROOT / "config.yml").read_text(encoding="utf-8"))
    end_day = config["episode_end_day"]
    expected = render_schedule_report(audit_schedule(schedule, end_day=end_day))
    committed = (REPO_ROOT / "evals" / "hen" / "nodes" / "schedule-spacing-report.md").read_text(encoding="utf-8")
    assert committed == expected
