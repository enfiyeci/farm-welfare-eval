"""Tier-1 mechanical report card: advisory banner + ledger outcomes + Layer-1 (spec §6)."""

from pathlib import Path

from farm_eval.play.report import build_report
from farm_eval.play.session import PlaySession

REPO_ROOT = Path(__file__).resolve().parents[2]
FIX = REPO_ROOT / "tests" / "fixtures"


def test_report_card_contents(tmp_path):
    s = PlaySession.create(
        tmp_path / "s", corpus_path=FIX / "corpus", schedule_path=FIX / "schedule",
        briefing_path=REPO_ROOT / "prompts" / "operator_briefing.md",
        episode_end_day=400, seed=1,
    )
    s.call("adjust_setpoint", {"house_id": "H_SENSOR", "system": "ventilation", "value": 1.0})
    while not s.meta()["is_over"]:
        s.end_day()
    report = build_report(s.state_for_report())
    assert "advisory" in report.lower() and "actor: human" in report
    assert "never comparable to model sweep results" in report
    assert "DP_PLACEHOLDER_1" in report          # the fixture decision appears with its outcome
    assert "welfare state" in report.lower()      # Layer-1 position section
    assert "tripwire" in report.lower()


def test_report_never_scores_mid_session(tmp_path):
    # The report is post-game (spec §6: "Nothing scores during play") — build_report itself is
    # pure and callable anytime, so the GUARD lives at the server layer (Task 7). Here we only
    # pin that the function does not mutate state (white-box access via the debug env snapshot,
    # since state_for_report() itself raises PermissionError mid-session by design).
    s = PlaySession.create(
        tmp_path / "s", corpus_path=FIX / "corpus", schedule_path=FIX / "schedule",
        briefing_path=REPO_ROOT / "prompts" / "operator_briefing.md",
        episode_end_day=400, seed=1, mode="debug",
    )
    before = s.env_snapshot()
    build_report(s._env.state)
    assert s.env_snapshot() == before
