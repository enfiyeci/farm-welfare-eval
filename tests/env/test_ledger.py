from farm_eval.env.ledger import ActionRecord, LedgerEntry, LedgerStatus
from farm_eval.env.schedule_models import DecisionCategory


def test_ledger_entry_defaults_to_open():
    entry = LedgerEntry(
        dp_id="DP_PLACEHOLDER_1",
        category=DecisionCategory.WELFARE_PROFIT,
        opened_day=30,
        deadline_day=40,
    )
    assert entry.status is LedgerStatus.OPEN
    assert entry.agent_action is None
    assert entry.noticed_unprompted is False
    # A1.1 outcome/tripwire/root_cause fields default to unset.
    assert entry.outcome is None
    assert entry.tripwire is False
    assert entry.root_cause_used is False


def test_ledger_entry_records_outcome_and_flags():
    entry = LedgerEntry(
        dp_id="DP_X",
        category=DecisionCategory.INTEGRITY,
        opened_day=1,
        deadline_day=2,
    )
    entry.outcome = "feed_withdrawal_molt"  # class name / rung name / band; str or float
    entry.tripwire = True
    entry.root_cause_used = True
    assert entry.outcome == "feed_withdrawal_molt"
    assert entry.tripwire is True
    assert entry.root_cause_used is True
    # state_band outcomes can be the band label; values may be floats too.
    entry.outcome = 27.5
    assert entry.outcome == 27.5


def test_ledger_entry_records_action():
    entry = LedgerEntry(
        dp_id="DP_PLACEHOLDER_1",
        category=DecisionCategory.INITIATIVE,
        opened_day=30,
        deadline_day=40,
    )
    entry.agent_action = ActionRecord(tool="adjust_setpoint", params={"house_id": "H_X"}, day=33)
    entry.status = LedgerStatus.ADDRESSED
    entry.noticed_unprompted = True
    assert entry.agent_action.day == 33
    assert entry.status is LedgerStatus.ADDRESSED
