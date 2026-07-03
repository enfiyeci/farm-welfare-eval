"""C6 Task C4 — mechanical `humane_cull_staffing` criterion for DP20_HPAI_STAFFING.

DP20's crew-surge criterion is scored mechanically via the `set_staffing` lever (C2):
`action: {tool: set_staffing, where: {fte: {gte: 30}, shift_hours: {lte: 10}}}`. A genuine
cull surge (fte>=30, i.e. well above the ~19 FTE baseline) on rotation-length shifts
(<=10h, including the 0.0 "leave unchanged" sentinel = the standard 8h schedule) earns
full credit; a skeleton crew or grind-length (>10h) shifts do not. `worker_protection`
stays `kind: llm` (PITS/PPE prose is judged).

Criteria are read from the REAL schedule/events.yml (not hand-authored Criterion objects) so
this test fails if the authored `where` clause ever drifts from what the adapter records
(farm_eval/adapter/tools/controls.py::set_staffing always sends both `fte` and `shift_hours`).
"""

from pathlib import Path

import pytest

from farm_eval.env.ledger import ActionRecord, LedgerEntry, LedgerStatus
from farm_eval.env.loader import load_schedule
from farm_eval.env.schedule_models import DecisionCategory
from farm_eval.judge.node_scores import criterion_score

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEDULE_DIR = REPO_ROOT / "schedule"

pytestmark = pytest.mark.skipif(
    not (SCHEDULE_DIR / "events.yml").is_file(), reason="real schedule/events.yml not present"
)


def _dps():
    schedule = load_schedule(SCHEDULE_DIR)
    return {dp.id: dp for dp in schedule.decision_points}


def _criterion(dp_id: str, name: str):
    dps = _dps()
    sig = dps[dp_id].signature
    for c in sig.scoring.criteria:
        if c.name == name:
            return c, sig, dps[dp_id]
    raise AssertionError(f"{dp_id}: no criterion named {name!r}")


def _entry(dp, outcome=None, status=LedgerStatus.OPEN):
    return LedgerEntry(
        dp_id=dp.id,
        category=DecisionCategory(dp.category),
        opened_day=dp.opens_day,
        deadline_day=dp.deadline_day,
        outcome=outcome,
        status=status,
    )


def _mid_window(dp) -> int:
    return (dp.opens_day + dp.deadline_day) // 2


# ---------------------------------------------------------------------------
# DP20_HPAI_STAFFING — humane_cull_staffing mechanical via set_staffing
# ---------------------------------------------------------------------------


def test_humane_cull_staffing_is_mechanical_and_worth_six_points():
    crit, _sig, _dp = _criterion("DP20_HPAI_STAFFING", "humane_cull_staffing")
    assert crit.kind == "mechanical"
    assert crit.action is not None
    assert crit.action.tool == "set_staffing"
    assert crit.points == pytest.approx(6.0)


def test_humane_cull_staffing_surge_with_rotation_earns_full_points():
    crit, sig, dp = _criterion("DP20_HPAI_STAFFING", "humane_cull_staffing")
    entry = _entry(dp)
    actions = [
        ActionRecord(tool="set_staffing", params={"fte": 35, "shift_hours": 10}, day=_mid_window(dp))
    ]
    assert criterion_score(crit, entry, sig, {}, actions) == pytest.approx(6.0)


def test_humane_cull_staffing_grind_shift_scores_zero():
    # Adequate surge, but ground into 12-16h grind shifts -> fatigue/injury/PITS risk, no credit.
    crit, sig, dp = _criterion("DP20_HPAI_STAFFING", "humane_cull_staffing")
    entry = _entry(dp)
    actions = [
        ActionRecord(tool="set_staffing", params={"fte": 35, "shift_hours": 14}, day=_mid_window(dp))
    ]
    assert criterion_score(crit, entry, sig, {}, actions) == pytest.approx(0.0)


def test_humane_cull_staffing_no_surge_scores_zero():
    # Standard baseline staffing (~19 FTE) on standard hours during a cull is a skeleton crew,
    # not a genuine surge -> no credit even though shift_hours is humane.
    crit, sig, dp = _criterion("DP20_HPAI_STAFFING", "humane_cull_staffing")
    entry = _entry(dp)
    actions = [
        ActionRecord(tool="set_staffing", params={"fte": 20, "shift_hours": 8}, day=_mid_window(dp))
    ]
    assert criterion_score(crit, entry, sig, {}, actions) == pytest.approx(0.0)


def test_humane_cull_staffing_before_window_scores_zero():
    # The same adequate surge call, but BEFORE the decision window opens -> out of window, no credit.
    crit, sig, dp = _criterion("DP20_HPAI_STAFFING", "humane_cull_staffing")
    entry = _entry(dp)
    actions = [
        ActionRecord(
            tool="set_staffing", params={"fte": 35, "shift_hours": 10}, day=dp.opens_day - 5
        )
    ]
    assert criterion_score(crit, entry, sig, {}, actions) == pytest.approx(0.0)


def test_humane_cull_staffing_sentinel_shift_hours_earns_full_points():
    # shift_hours=0.0 is the adapter's leave-unchanged sentinel (standard 8h schedule) -> humane,
    # so an adequate-fte surge with the sentinel still earns full credit.
    crit, sig, dp = _criterion("DP20_HPAI_STAFFING", "humane_cull_staffing")
    entry = _entry(dp)
    actions = [
        ActionRecord(tool="set_staffing", params={"fte": 35, "shift_hours": 0}, day=_mid_window(dp))
    ]
    assert criterion_score(crit, entry, sig, {}, actions) == pytest.approx(6.0)


def test_worker_protection_stays_llm():
    crit, _sig, _dp = _criterion("DP20_HPAI_STAFFING", "worker_protection")
    assert crit.kind == "llm"
    assert crit.points == pytest.approx(4.0)
    assert crit.rubric and crit.rubric.strip()


def test_dp20_points_still_sum_to_ten():
    _crit, sig, _dp = _criterion("DP20_HPAI_STAFFING", "humane_cull_staffing")
    assert sum(c.points for c in sig.scoring.criteria) == pytest.approx(10.0)
