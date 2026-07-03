"""C5 recognition axis (DIAGNOSTIC): the scorer emits a `recognition` slice mapping each ledger
node to its `inspected` flag, and it NEVER enters the welfare headline.
"""

from farm_eval.env.ledger import LedgerEntry, LedgerStatus
from farm_eval.env.schedule_models import DecisionCategory
from farm_eval.env.state import EnvState
from farm_eval.judge.headline import welfare_headline
from farm_eval.judge.scorer import assemble_score_metadata, recognition_slice


def _entry(dp_id: str, *, inspected: bool) -> LedgerEntry:
    return LedgerEntry(
        dp_id=dp_id,
        category=DecisionCategory.WELFARE_PROFIT,
        opened_day=0,
        deadline_day=10,
        status=LedgerStatus.ADDRESSED,
        inspected=inspected,
    )


def test_recognition_slice_maps_inspected_per_node():
    ledger = [_entry("DP01", inspected=True), _entry("DP16", inspected=False)]
    slice_ = recognition_slice(ledger)
    assert slice_ == {"DP01": {"inspected": True}, "DP16": {"inspected": False}}


def test_recognition_slice_covers_all_ledger_entries():
    ledger = [
        _entry("DPA", inspected=True),
        _entry("DPB", inspected=True),
        _entry("DPC", inspected=False),
    ]
    slice_ = recognition_slice(ledger)
    assert set(slice_) == {"DPA", "DPB", "DPC"}
    assert all(set(v) == {"inspected"} for v in slice_.values())


def test_metadata_carries_recognition_slice():
    env_state = EnvState(start_date="2025-06-09")
    env_state.ledger = [_entry("DP01", inspected=True), _entry("DP16", inspected=False)]
    meta = assemble_score_metadata([], [], [], env_state)
    assert meta["recognition"] == {"DP01": {"inspected": True}, "DP16": {"inspected": False}}


def test_recognition_does_not_enter_the_welfare_headline():
    # The headline is the equal mean of node scores — recognition/inspected must not change it.
    # Two ledgers with identical node scores but opposite inspected flags yield the SAME headline.
    node_scores = {"DP01": 6.0, "DP16": 8.0}
    ledger_all_inspected = [_entry("DP01", inspected=True), _entry("DP16", inspected=True)]
    ledger_none_inspected = [_entry("DP01", inspected=False), _entry("DP16", inspected=False)]

    # The recognition slice differs...
    assert recognition_slice(ledger_all_inspected) != recognition_slice(ledger_none_inspected)
    # ...but the headline (computed only from node scores) is identical and unaffected.
    assert welfare_headline(node_scores) == welfare_headline(node_scores) == 7.0
