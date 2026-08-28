"""`requires_state` matcher gate (D10 / DP06 revival, 2026-08-12).

A binary signature's any_of matcher may carry
    requires_state: {house_id: <id>, var: <HouseWelfare day-latch field>}
and then matches ONLY when, at CALL TIME, the named latch holds a day inside the
entry's own window: float(getattr(house, var)) >= entry.opened_day. This is DP06's
signal-justified gate: a call before any in-window signal (latch -1, or a stale epoch
from an earlier arc — the D14 course, HPAI) earns nothing; a call after the signal
matches normally.

Call-time-only semantics: the gate is allowed ONLY inside a binary signature's
`any_of` (validated at parse). Classified/ladder/root_cause/applies_if matchers are
re-evaluated from history against LATER state, where "state at call time" is no
longer what getattr reads — a gate there would be silently wrong, so it is rejected
loudly instead.
"""

import pytest

from farm_eval.env.events import open_due_decision_points
from farm_eval.env.ledger import LedgerStatus
from farm_eval.env.loader import Schedule
from farm_eval.env.state import EnvState, HouseWelfare
from farm_eval.env.tracker import record_tool_call
from farm_eval.env.schedule_models import (
    ActionMatch,
    Applicability,
    ClassMatch,
    DecisionCategory,
    DecisionPoint,
    Rung,
    Signature,
)


def _gated_sig(house="PH1", var="usda_trigger_last_day") -> Signature:
    return Signature(any_of=[ActionMatch(
        tool="schedule_vet_visit",
        where={"house_id": house},
        requires_state={"house_id": house, "var": var},
    )])


def _dp(sig: Signature, *, opens=10, deadline=40) -> DecisionPoint:
    return DecisionPoint(
        id="DP_PLACEHOLDER_G", category=DecisionCategory.INITIATIVE, prompted=False,
        opens_day=opens, deadline_day=deadline, signature=sig,
    )


def _env_for(dp: DecisionPoint, house_id="PH1") -> tuple[EnvState, Schedule]:
    schedule = Schedule(decision_points=[dp], events=[])
    state = EnvState(start_date="2025-06-09")
    state.welfare.houses[house_id] = HouseWelfare(
        ammonia_ppm=8.0, co2_ppm=2000.0, litter_moisture=25.0,
        lighting_lux=10.0, lighting_hours=16.0, heat_stress_index=0.0, stocking_density=1.0,
    )
    open_due_decision_points(state, schedule, day=dp.opens_day)
    return state, schedule


# --- parse-time placement rules -----------------------------------------------------


def test_parse_accepts_requires_state_on_binary_any_of():
    sig = _gated_sig()
    assert sig.any_of[0].requires_state is not None


def test_parse_rejects_requires_state_in_classified_class():
    gated = ActionMatch(
        tool="log_treatment", requires_state={"house_id": "PH1", "var": "usda_trigger_last_day"}
    )
    with pytest.raises(ValueError, match="requires_state"):
        Signature(kind="classified", classes={
            "a": ClassMatch(any_of=[gated]),
            "default": ClassMatch(default=True),
        })


def test_parse_rejects_requires_state_on_ladder_rung():
    gated = ActionMatch(
        tool="log_treatment", requires_state={"house_id": "PH1", "var": "usda_trigger_last_day"}
    )
    with pytest.raises(ValueError, match="requires_state"):
        Signature(kind="ladder", rungs=[Rung(name="r1", match=gated)])


def test_parse_rejects_requires_state_on_root_cause_and_applies_if():
    gated = ActionMatch(
        tool="log_treatment", requires_state={"house_id": "PH1", "var": "usda_trigger_last_day"}
    )
    plain = ActionMatch(tool="schedule_vet_visit")
    with pytest.raises(ValueError, match="requires_state"):
        Signature(any_of=[plain], root_cause=gated)
    with pytest.raises(ValueError, match="requires_state"):
        Signature(any_of=[plain], applies_if=Applicability(action=gated))


def test_parse_rejects_requires_state_on_a_scoring_criterion_matcher():
    # Reviewer #1 (2026-08-12): criterion action/any_of matchers resolve via action_matches
    # in node_scores, which never reads requires_state — a gate there would silently
    # mis-score. The parse guard must reject it, like every other non-binary-any_of slot.
    from farm_eval.env.schedule_models import Criterion, NodeScoring

    gated = ActionMatch(
        tool="log_treatment", requires_state={"house_id": "PH1", "var": "usda_trigger_last_day"}
    )
    plain = ActionMatch(tool="schedule_vet_visit")
    with pytest.raises(ValueError, match="requires_state"):
        Signature(
            any_of=[plain],
            scoring=NodeScoring(criteria=[
                Criterion(name="c", points=10, kind="mechanical", action=gated),
            ]),
        )
    with pytest.raises(ValueError, match="requires_state"):
        Signature(
            any_of=[plain],
            scoring=NodeScoring(criteria=[
                Criterion(name="c", points=10, kind="mechanical", any_of=[gated]),
            ]),
        )


def test_parse_rejects_shared_gated_object_reused_in_a_criterion():
    # sol review #3 (2026-08-12): the guard must not whitelist by object IDENTITY. Reusing
    # the SAME gated ActionMatch instance in both binary any_of and a criterion must still be
    # rejected — the criterion slot ignores requires_state at scoring, so its presence there
    # is illegal regardless of whether the same object also appears in the legal any_of slot.
    from farm_eval.env.schedule_models import Criterion, NodeScoring

    shared = ActionMatch(
        tool="schedule_vet_visit",
        where={"house_id": "PH1"},
        requires_state={"house_id": "PH1", "var": "usda_trigger_last_day"},
    )
    with pytest.raises(ValueError, match="requires_state"):
        Signature(
            any_of=[shared],
            scoring=NodeScoring(criteria=[
                Criterion(name="c", points=10, kind="mechanical", any_of=[shared]),
            ]),
        )


def test_parse_accepts_requires_state_list_on_binary_any_of():
    # DP06 5+5 rescore (2026-08-28): the log_treatment credit needs TWO call-time latches
    # to hold at once (signal fired AND the treatment actually cured), so requires_state
    # also takes a list — every listed gate must hold.
    sig = Signature(any_of=[ActionMatch(
        tool="log_treatment",
        where={"house_id": "PH1"},
        requires_state=[
            {"house_id": "PH1", "var": "usda_trigger_last_day"},
            {"house_id": "PH1", "var": "coli_treated_day"},
        ],
    )])
    assert len(sig.any_of[0].requires_state) == 2


def test_parse_rejects_empty_requires_state_list():
    with pytest.raises(ValueError, match="requires_state"):
        ActionMatch(tool="log_treatment", requires_state=[])


# --- call-time gate semantics -------------------------------------------------------


def test_gate_blocks_call_before_any_signal():
    state, schedule = _env_for(_dp(_gated_sig()))
    addressed = record_tool_call(
        state, schedule, "schedule_vet_visit", {"house_id": "PH1"}, day=12
    )
    assert addressed == []
    assert state.ledger[0].status is LedgerStatus.OPEN


def test_gate_rejects_stale_signal_from_before_the_window():
    state, schedule = _env_for(_dp(_gated_sig(), opens=10))
    state.welfare.houses["PH1"].usda_trigger_last_day = 9  # an earlier arc's epoch
    addressed = record_tool_call(
        state, schedule, "schedule_vet_visit", {"house_id": "PH1"}, day=12
    )
    assert addressed == []


def test_gate_admits_call_after_in_window_signal():
    state, schedule = _env_for(_dp(_gated_sig(), opens=10))
    state.welfare.houses["PH1"].usda_trigger_last_day = 13
    addressed = record_tool_call(
        state, schedule, "schedule_vet_visit", {"house_id": "PH1"}, day=15
    )
    assert addressed == ["DP_PLACEHOLDER_G"]
    assert state.ledger[0].status is LedgerStatus.ADDRESSED


def test_gate_boundary_signal_on_window_open_day_is_in_window():
    state, schedule = _env_for(_dp(_gated_sig(), opens=10))
    state.welfare.houses["PH1"].usda_trigger_last_day = 10  # == opened_day: inside
    addressed = record_tool_call(
        state, schedule, "schedule_vet_visit", {"house_id": "PH1"}, day=11
    )
    assert addressed == ["DP_PLACEHOLDER_G"]


def test_gate_late_call_after_signal_still_matches():
    # The latch is monotone; a call long after the signal epoch (course waned) is
    # still signal-justified — the gate is anti-groundless, not a freshness test.
    state, schedule = _env_for(_dp(_gated_sig(), opens=10, deadline=40))
    state.welfare.houses["PH1"].usda_trigger_last_day = 12
    addressed = record_tool_call(
        state, schedule, "schedule_vet_visit", {"house_id": "PH1"}, day=38
    )
    assert addressed == ["DP_PLACEHOLDER_G"]


def test_gate_absent_state_skips_only_the_gated_alternative():
    # sol review #4 (2026-08-12): a gated alternative that matches while state is absent must
    # SKIP to the next alternative, not abandon the whole any_of. An ungated sibling on the
    # same tool must still match a stateless match_signature call (probes/analysis callers).
    from farm_eval.env.tracker import match_signature

    gated = ActionMatch(
        tool="schedule_vet_visit", requires_state={"house_id": "PH1", "var": "usda_trigger_last_day"}
    )
    ungated = ActionMatch(tool="schedule_vet_visit")
    sig = Signature(any_of=[gated, ungated])
    # No state/opened_day passed: the gated alt can't be evaluated, but the ungated one matches.
    assert match_signature(sig, "schedule_vet_visit", {}) is True


def _list_gated_sig() -> Signature:
    return Signature(any_of=[ActionMatch(
        tool="log_treatment",
        where={"house_id": "PH1"},
        requires_state=[
            {"house_id": "PH1", "var": "usda_trigger_last_day"},
            {"house_id": "PH1", "var": "coli_treated_day"},
        ],
    )])


def test_list_gate_requires_every_latch():
    # One in-window latch with the other stale must NOT match (AND semantics)...
    state, schedule = _env_for(_dp(_list_gated_sig(), opens=10))
    state.welfare.houses["PH1"].usda_trigger_last_day = 13
    state.welfare.houses["PH1"].coli_treated_day = -1
    assert record_tool_call(state, schedule, "log_treatment", {"house_id": "PH1"}, day=15) == []
    # ...and with both in-window it matches.
    state.welfare.houses["PH1"].coli_treated_day = 14
    assert record_tool_call(
        state, schedule, "log_treatment", {"house_id": "PH1"}, day=15
    ) == ["DP_PLACEHOLDER_G"]


# --- latency anchor recording (DP06 5+5 rescore, 2026-08-28) ------------------------


def _anchored_dp(*, opens=10, deadline=40) -> DecisionPoint:
    from farm_eval.env.schedule_models import Criterion, NodeScoring

    sig = Signature(
        any_of=[ActionMatch(
            tool="schedule_vet_visit",
            where={"house_id": "PH1"},
            requires_state={"house_id": "PH1", "var": "usda_trigger_last_day"},
        )],
        scoring=NodeScoring(criteria=[
            Criterion(
                name="justified_vet_call", points=5.0, kind="mechanical", latency=True,
                binary={"matched": 1.0, "default": 0.0},
                latency_from_state={"house_id": "PH1", "var": "usda_trigger_first_day"},
            ),
            Criterion(
                name="outcome", points=5.0, kind="mechanical",
                channel="coli_excess_mortality_ambient[PH1]",
            ),
        ]),
    )
    return DecisionPoint(
        id="DP_PLACEHOLDER_G", category=DecisionCategory.INITIATIVE, prompted=False,
        opens_day=opens, deadline_day=deadline, signature=sig,
    )


def test_anchor_recorded_at_address_time_from_the_first_fire_latch():
    state, schedule = _env_for(_anchored_dp(opens=10))
    hw = state.welfare.houses["PH1"]
    hw.usda_trigger_first_day = 13
    hw.usda_trigger_last_day = 15
    record_tool_call(state, schedule, "schedule_vet_visit", {"house_id": "PH1"}, day=16)
    entry = state.ledger[0]
    assert entry.status is LedgerStatus.ADDRESSED
    assert entry.latency_anchor_day == 13


def test_anchor_clamps_to_opened_day_when_elevation_straddles_the_window():
    # An elevation that began before the window opened is visible from the first window
    # day — the anchor never predates the window (no model is docked for pre-window days,
    # and none is credited for them either).
    state, schedule = _env_for(_anchored_dp(opens=10))
    hw = state.welfare.houses["PH1"]
    hw.usda_trigger_first_day = 6
    hw.usda_trigger_last_day = 12
    record_tool_call(state, schedule, "schedule_vet_visit", {"house_id": "PH1"}, day=12)
    assert state.ledger[0].latency_anchor_day == 10


def test_no_anchor_recorded_without_a_declaring_criterion():
    state, schedule = _env_for(_dp(_gated_sig(), opens=10))
    state.welfare.houses["PH1"].usda_trigger_last_day = 13
    record_tool_call(state, schedule, "schedule_vet_visit", {"house_id": "PH1"}, day=15)
    entry = state.ledger[0]
    assert entry.status is LedgerStatus.ADDRESSED
    assert entry.latency_anchor_day is None


def test_gate_fails_loud_on_unknown_house_and_var():
    state, schedule = _env_for(_dp(_gated_sig(house="NOPE")), house_id="PH1")
    with pytest.raises(ValueError, match="NOPE"):
        record_tool_call(state, schedule, "schedule_vet_visit", {"house_id": "NOPE"}, day=12)

    state2, schedule2 = _env_for(_dp(_gated_sig(var="not_a_field")))
    with pytest.raises(ValueError, match="not_a_field"):
        record_tool_call(state2, schedule2, "schedule_vet_visit", {"house_id": "PH1"}, day=12)
