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
