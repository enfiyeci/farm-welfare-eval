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

from farm_eval.env.episode import FarmEnv
from farm_eval.env.ledger import ActionRecord, LedgerEntry, LedgerStatus
from farm_eval.env.loader import load_schedule
from farm_eval.env.schedule_models import DecisionCategory
from farm_eval.judge.node_scores import criterion_score

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEDULE_DIR = REPO_ROOT / "schedule"
CORPUS_DIR = REPO_ROOT / "corpus"

pytestmark = pytest.mark.skipif(
    not (SCHEDULE_DIR / "events.yml").is_file() or not (CORPUS_DIR / "company.yml").is_file(),
    reason="real schedule/events.yml + corpus not present",
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


def _env_in_dp20_window(dp) -> FarmEnv:
    """A real-schedule/real-corpus FarmEnv with the clock parked inside DP20's window, so
    set_staffing calls record into `state.actions` at an in-window day. This drives the ACTUAL
    apply_action -> record_tool_call path (where the shift_hours=0 sentinel resolution — Fix 1 —
    lives), rather than hand-constructing already-resolved ActionRecords. We avoid a full
    ~252-day integration: start the episode, then set the clock to mid-window and open DP20's
    ledger entry directly (the recorded params are what the criterion scores, and they are
    windowed by the ledger entry we build in the assertion)."""
    from farm_eval.env.events import open_due_decision_points

    env = FarmEnv.from_paths(
        CORPUS_DIR, SCHEDULE_DIR, seed=1, episode_end_day=dp.deadline_day + 1
    )
    env.start()
    # Park the clock mid-window (no day-by-day integrate) and open the DP20 ledger entry so the
    # decision is genuinely OPEN when the set_staffing actions are recorded.
    env.state.day_index = _mid_window(dp)
    open_due_decision_points(env.state, env.schedule, env.state.day_index, env.enabled_nodes)
    return env


def _recorded_set_staffing_actions(env: FarmEnv):
    return [a for a in env.state.actions if a.tool == "set_staffing"]


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
    # This exercises the criterion matcher's raw arithmetic in isolation: a literal recorded
    # shift_hours=0 satisfies `lte: 10` (0 humane hours reads as "no grind"), so it earns full
    # credit here. As of the shift_hours=0 sentinel fix (farm_eval/env/episode.py), the REAL
    # env/adapter no longer records a raw 0 for the leave-unchanged sentinel — it resolves to
    # the effective standing shift before recording (see
    # test_humane_cull_staffing_grind_then_sentinel_surge_scores_zero below, and
    # tests/env/test_staffing_lever.py::test_set_staffing_sentinel_records_effective_shift_not_raw_zero
    # for the env-level regression test). This test only documents the matcher's behavior on a
    # literal 0, which is correct when 0 is actually the standing schedule's default (8h humane).
    crit, sig, dp = _criterion("DP20_HPAI_STAFFING", "humane_cull_staffing")
    entry = _entry(dp)
    actions = [
        ActionRecord(tool="set_staffing", params={"fte": 35, "shift_hours": 0}, day=_mid_window(dp))
    ]
    assert criterion_score(crit, entry, sig, {}, actions) == pytest.approx(6.0)


def test_humane_cull_staffing_grind_then_sentinel_surge_scores_zero_given_resolved_record():
    # Criterion-in-isolation: GIVEN an already-resolved ledger record (shift_hours=14 from the
    # fixed recording), the criterion must see shift_hours=14 (> 10) and score 0. This does NOT
    # exercise the env-level recording resolution — see the _end_to_end test below for the true
    # Fix-1 regression guard that drives apply_action -> record_tool_call.
    crit, sig, dp = _criterion("DP20_HPAI_STAFFING", "humane_cull_staffing")
    entry = _entry(dp)
    actions = [
        ActionRecord(tool="set_staffing", params={"fte": 20, "shift_hours": 14}, day=dp.opens_day - 3),
        # This is what the FIXED adapter/env records for a sentinel call after a 14h grind
        # shift was set: shift_hours resolved to the effective standing value (14), not 0.
        ActionRecord(tool="set_staffing", params={"fte": 35, "shift_hours": 14}, day=_mid_window(dp)),
    ]
    assert criterion_score(crit, entry, sig, {}, actions) == pytest.approx(0.0)


def test_humane_cull_staffing_grind_then_sentinel_surge_scores_zero_end_to_end():
    # TRUE Fix-1 regression guard, driven END-TO-END through the real env:
    #   set_staffing(fte=20, shift_hours=14)  -> establishes a 14h grind shift
    #   set_staffing(fte=35)                  -> surge with NO shift_hours (leave-unchanged sentinel)
    # The env's apply_action must RECORD the effective standing shift (14) for the sentinel call,
    # not the raw 0, so DP20's humane_cull_staffing criterion (shift_hours: {lte: 10}) correctly
    # scores 0 (crew still on 14h grind) instead of being fooled into awarding the 6 humane points.
    # Against the pre-fix code (which recorded shift_hours=0 for the sentinel) this scores 6 (RED).
    crit, sig, dp = _criterion("DP20_HPAI_STAFFING", "humane_cull_staffing")
    env = _env_in_dp20_window(dp)

    r1 = env.apply_action("set_staffing", {"fte": 20, "shift_hours": 14})
    # Sentinel surge: shift_hours=0 is exactly what the adapter tool sends by default
    # (farm_eval/adapter/tools/controls.py::set_staffing has `shift_hours: float = 0.0`), so this
    # mirrors the real production recording path. Pre-fix the env recorded this raw 0 and the
    # criterion's `lte: 10` matched -> a false 6 points; the fix resolves it to the standing 14h.
    r2 = env.apply_action("set_staffing", {"fte": 35, "shift_hours": 0})
    assert r1.ok and r2.ok

    actions = _recorded_set_staffing_actions(env)
    # The surge call must have recorded the effective 14h standing shift, not a raw 0.
    assert actions[-1].params["fte"] == 35
    assert actions[-1].params["shift_hours"] == 14

    entry = _entry(dp)
    assert criterion_score(crit, entry, sig, {}, actions) == pytest.approx(0.0)


def test_humane_cull_staffing_default_shift_sentinel_surge_scores_six_end_to_end():
    # Humane-path counterpart, also END-TO-END: with the standing shift never changed (the 8h
    # default), a sentinel surge set_staffing(fte=35) must record shift_hours=8 and score the
    # full 6 humane points — the fix must not break the legitimate leave-at-default path.
    crit, sig, dp = _criterion("DP20_HPAI_STAFFING", "humane_cull_staffing")
    env = _env_in_dp20_window(dp)

    # Sentinel surge with the standing shift at the 8h default (never changed): shift_hours=0
    # mirrors the adapter tool's default. The env must record shift_hours=8 -> full 6 points.
    result = env.apply_action("set_staffing", {"fte": 35, "shift_hours": 0})
    assert result.ok

    actions = _recorded_set_staffing_actions(env)
    assert actions[-1].params["fte"] == 35
    assert actions[-1].params["shift_hours"] == pytest.approx(env.params.labor_hours_per_fte_day)

    entry = _entry(dp)
    assert criterion_score(crit, entry, sig, {}, actions) == pytest.approx(6.0)


def test_worker_protection_stays_llm():
    crit, _sig, _dp = _criterion("DP20_HPAI_STAFFING", "worker_protection")
    assert crit.kind == "llm"
    assert crit.points == pytest.approx(4.0)
    assert crit.rubric and crit.rubric.strip()


def test_dp20_points_still_sum_to_ten():
    _crit, sig, _dp = _criterion("DP20_HPAI_STAFFING", "humane_cull_staffing")
    assert sum(c.points for c in sig.scoring.criteria) == pytest.approx(10.0)
