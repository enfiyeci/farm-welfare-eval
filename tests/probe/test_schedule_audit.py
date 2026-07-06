"""P8 — read-only spacing audit of the schedule (spec §3 P8). Measures; never edits."""

from pathlib import Path

from farm_eval.env.loader import load_schedule
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
