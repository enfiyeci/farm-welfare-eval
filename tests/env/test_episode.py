from pathlib import Path

from farm_eval.env.episode import FarmEnv
from farm_eval.env.ledger import LedgerStatus

FIX = Path(__file__).parent.parent / "fixtures"


def _env() -> FarmEnv:
    return FarmEnv.from_paths(FIX / "corpus", FIX / "schedule", seed=1, episode_end_day=400)


def test_start_opens_day0_dp_and_delivers_email():
    env = _env()
    env.start()
    assert env.current_day() == 0
    assert env.current_date() == "2025-06-09"
    assert any(e.dp_id == "DP_PLACEHOLDER_1" and e.status is LedgerStatus.OPEN for e in env.state.ledger)
    assert len(env.list_emails(unread_only=True)) == 1


def test_sensor_availability_asymmetry():
    env = _env()
    env.start()
    ok = env.get_sensor("H_SENSOR", "ammonia_ppm")
    assert ok.available is True and ok.value is not None
    missing = env.get_sensor("H_NOSENSOR", "ammonia_ppm")
    assert missing.available is False
    assert "handheld" in missing.message.lower()


def test_action_addresses_decision_and_persists_through_advance():
    env = _env()
    env.start()
    result = env.apply_action("adjust_setpoint", {"house_id": "H_SENSOR", "system": "ventilation", "value": 2.5})
    assert result.addressed_dps == ["DP_PLACEHOLDER_1"]

    advance = env.end_day()
    assert advance.new_day == 5  # next beat is the day-5 sensor anomaly
    assert advance.elapsed_days == 5
    entry = next(e for e in env.state.ledger if e.dp_id == "DP_PLACEHOLDER_1")
    assert entry.status is LedgerStatus.ADDRESSED


def test_unaddressed_decision_lapses_after_deadline():
    env = _env()
    env.start()
    env.end_day()  # jump to day 5 (deadline_day == 5, not yet < 5? deadline is 5; lapse triggers when day > 5)
    env.end_day()  # jump to episode_end (400) -> lapses
    entry = next(e for e in env.state.ledger if e.dp_id == "DP_PLACEHOLDER_1")
    assert entry.status is LedgerStatus.LAPSED
    assert env.is_over() is True
