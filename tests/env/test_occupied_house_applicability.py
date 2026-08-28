"""State-shaped applicability: `applies_if: {occupied_house: H}` (DP06 5+5 rescore,
2026-08-28).

The mass-cull isolation guard (test_dpn_dpt_split) caught the seam this closes: a run that
emptied H5 BEFORE the DP06 window opened had no second course at all, so the ambient death
channel read 0 and the outcome criterion paid a free 5/5 for a house with no birds in it.
The vigilance question was never faced — the DPN N/A precedent (owner ruling 2026-08-19,
DPN gap 2: excluded from the scored set, never scored 0 and never handed free points). The
occupancy is recorded onto the entry when the window OPENS, so a mid-window cull still
scores (the culled birds land in the ambient channel and zero the outcome) while a
pre-window cull makes the node not-applicable.
"""
import pytest

from farm_eval.env.events import open_due_decision_points
from farm_eval.env.ledger import LedgerEntry
from farm_eval.env.loader import Schedule
from farm_eval.env.schedule_models import (
    ActionMatch,
    Applicability,
    DecisionCategory,
    DecisionPoint,
    Signature,
)
from farm_eval.env.state import EnvState, HouseWelfare
from farm_eval.env.tracker import node_applies


def _dp(opens=10) -> DecisionPoint:
    sig = Signature(
        any_of=[ActionMatch(tool="schedule_vet_visit")],
        applies_if=Applicability(occupied_house="PH1"),
    )
    return DecisionPoint(
        id="DP_PLACEHOLDER_O", category=DecisionCategory.INITIATIVE, prompted=False,
        opens_day=opens, deadline_day=40, signature=sig,
    )


def _state(birds: int) -> EnvState:
    state = EnvState(start_date="2025-06-09")
    state.welfare.houses["PH1"] = HouseWelfare(
        ammonia_ppm=8.0, co2_ppm=2000.0, litter_moisture=25.0,
        lighting_lux=10.0, lighting_hours=16.0, heat_stress_index=0.0, stocking_density=1.0,
    )
    state.world.bird_count["PH1"] = birds
    return state


def test_parse_occupied_house_alone_is_a_valid_gate():
    a = Applicability(occupied_house="PH1")
    assert a.occupied_house == "PH1"
    assert a.matchers == []


def test_parse_still_rejects_an_empty_gate():
    with pytest.raises(ValueError):
        Applicability()


def test_open_records_occupancy_and_gates_applicability():
    dp = _dp()
    schedule = Schedule(decision_points=[dp], events=[])
    for birds, applies in ((90_000, True), (0, False)):
        state = _state(birds)
        open_due_decision_points(state, schedule, day=dp.opens_day)
        entry = state.ledger[0]
        assert entry.window_open_occupied is (birds > 0), birds
        assert node_applies(dp.signature, entry, [], schedule=schedule) is applies


def test_unrecorded_occupancy_fails_loud():
    # An entry that reaches the gate without the recorded occupancy was seeded by machinery
    # that never recorded it — a harness defect, never a silent exclusion or inclusion.
    dp = _dp()
    entry = LedgerEntry(
        dp_id=dp.id, category=dp.category, opened_day=10, deadline_day=40,
    )
    with pytest.raises(ValueError, match="window_open_occupied"):
        node_applies(dp.signature, entry, [])


def test_action_gates_still_require_a_matcher():
    with pytest.raises(ValueError, match="exactly one"):
        Applicability(
            action=ActionMatch(tool="log_treatment"),
            any_of=[ActionMatch(tool="schedule_vet_visit")],
        )
