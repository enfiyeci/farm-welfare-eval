"""C5 Task 2 — pure mechanical per-criterion scorer + node assembly.

Covers: latency_factor, resolve_class, criterion_score (channel/class_scores/ladder/
binary/action/pure-latency + floor_channel/latency modifiers), apply_cap_floor,
node_score_mechanical.
"""

import math

import pytest

from farm_eval.env.ledger import ActionRecord, LedgerEntry, LedgerStatus
from farm_eval.env.schedule_models import (
    ActionMatch,
    ClassMatch,
    Criterion,
    DecisionCategory,
    Metric,
    NodeCap,
    NodeFloor,
    NodeScoring,
    Rung,
    Signature,
)
from farm_eval.judge.node_scores import (
    _clamp,
    _clamp01,
    apply_cap_floor,
    criterion_score,
    latency_factor,
    node_score_mechanical,
    resolve_class,
)


def make_entry(
    *,
    dp_id="DP99",
    opened_day=10,
    deadline_day=20,
    outcome=None,
    status=LedgerStatus.OPEN,
    agent_action=None,
    tripwire=False,
):
    return LedgerEntry(
        dp_id=dp_id,
        category=DecisionCategory.WELFARE_COST,
        opened_day=opened_day,
        deadline_day=deadline_day,
        outcome=outcome,
        status=status,
        agent_action=agent_action,
        tripwire=tripwire,
    )


# ---------------------------------------------------------------------------
# latency_factor
# ---------------------------------------------------------------------------


def test_latency_factor_earliest_is_full():
    assert latency_factor(10, 20, 10) == 1.0


def test_latency_factor_deadline_is_zero():
    assert latency_factor(10, 20, 20) == 0.0


def test_latency_factor_midpoint_is_half():
    assert latency_factor(10, 20, 15) == pytest.approx(0.5)


def test_latency_factor_none_action_day_is_zero():
    assert latency_factor(10, 20, None) == 0.0


def test_latency_factor_degenerate_window_acted_is_one():
    assert latency_factor(15, 15, 15) == 1.0


def test_latency_factor_degenerate_window_never_acted_is_zero():
    assert latency_factor(15, 15, None) == 0.0


def test_latency_factor_clamps_out_of_range():
    # action_day before opened_day or after deadline_day still clamps into [0, 1]
    assert latency_factor(10, 20, 5) == 1.0
    assert latency_factor(10, 20, 25) == 0.0


# ---------------------------------------------------------------------------
# resolve_class
# ---------------------------------------------------------------------------


def test_resolve_class_uses_outcome_when_str():
    sig = Signature(kind="classified", classes={"good": ClassMatch(default=True)})
    entry = make_entry(outcome="good")
    assert resolve_class(entry, sig) == "good"


def test_resolve_class_falls_back_to_default_class_when_outcome_none():
    sig = Signature(
        kind="classified",
        classes={"bad": ClassMatch(), "neutral": ClassMatch(default=True)},
    )
    entry = make_entry(outcome=None)
    assert resolve_class(entry, sig) == "neutral"


def test_resolve_class_none_when_no_default_and_outcome_none():
    sig = Signature(kind="classified", classes={"bad": ClassMatch()})
    entry = make_entry(outcome=None)
    assert resolve_class(entry, sig) is None


# ---------------------------------------------------------------------------
# criterion_score: channel
# ---------------------------------------------------------------------------


def test_criterion_score_channel_full_subscore():
    crit = Criterion(name="c", points=4.0, channel="nh3")
    entry = make_entry()
    sig = Signature()
    assert criterion_score(crit, entry, sig, {"nh3": 1.0}, []) == pytest.approx(4.0)


def test_criterion_score_channel_partial_subscore():
    crit = Criterion(name="c", points=5.0, channel="nh3")
    entry = make_entry()
    sig = Signature()
    assert criterion_score(crit, entry, sig, {"nh3": 0.4}, []) == pytest.approx(2.0)


def test_criterion_score_channel_missing_key_raises():
    crit = Criterion(name="c", points=5.0, channel="nh3")
    entry = make_entry()
    sig = Signature()
    with pytest.raises(ValueError):
        criterion_score(crit, entry, sig, {}, [])


# ---------------------------------------------------------------------------
# criterion_score: class_scores
# ---------------------------------------------------------------------------


def test_criterion_score_class_scores_mapped_outcome():
    crit = Criterion(name="c", points=6.0, class_scores={"good": 1.0, "bad": 0.0})
    sig = Signature(kind="classified", classes={"good": ClassMatch(), "bad": ClassMatch(default=True)})
    entry = make_entry(outcome="good")
    assert criterion_score(crit, entry, sig, {}, []) == pytest.approx(6.0)


def test_criterion_score_class_scores_falls_back_to_default_class():
    crit = Criterion(name="c", points=6.0, class_scores={"good": 1.0, "neutral": 0.5})
    sig = Signature(
        kind="classified",
        classes={"good": ClassMatch(), "neutral": ClassMatch(default=True)},
    )
    entry = make_entry(outcome=None)
    assert criterion_score(crit, entry, sig, {}, []) == pytest.approx(3.0)


def test_criterion_score_class_scores_unmapped_no_default_raises():
    crit = Criterion(name="c", points=6.0, class_scores={"good": 1.0})
    sig = Signature(kind="classified", classes={"bad": ClassMatch()})
    entry = make_entry(outcome=None)
    with pytest.raises(ValueError):
        criterion_score(crit, entry, sig, {}, [])


def test_criterion_score_class_scores_outcome_unmapped_raises():
    crit = Criterion(name="c", points=6.0, class_scores={"good": 1.0})
    sig = Signature(kind="classified", classes={"weird": ClassMatch(), "good": ClassMatch()})
    entry = make_entry(outcome="weird")
    with pytest.raises(ValueError):
        criterion_score(crit, entry, sig, {}, [])


def _state_band_sig():
    return Signature(
        kind="state_band",
        metric=Metric(house_id="H1", var="nh3_ppm", agg="final"),
        bands={"ok": [[0.0, 10.0]], "bad": [[10.0, 100.0]]},
    )


# ---------------------------------------------------------------------------
# criterion_score: ladder
# ---------------------------------------------------------------------------


def _ladder_sig():
    return Signature(
        kind="ladder",
        rungs=[
            Rung(name="r1", match=ActionMatch(tool="t1")),
            Rung(name="r2", match=ActionMatch(tool="t2")),
            Rung(name="r3", match=ActionMatch(tool="t3")),
        ],
    )


def test_criterion_score_ladder_partial_rungs():
    crit = Criterion(name="c", points=9.0, ladder=True)
    sig = _ladder_sig()
    entry = make_entry(outcome="r2")
    assert criterion_score(crit, entry, sig, {}, []) == pytest.approx(6.0)  # 2/3 * 9


def test_criterion_score_ladder_none_outcome_is_zero():
    crit = Criterion(name="c", points=9.0, ladder=True)
    sig = _ladder_sig()
    entry = make_entry(outcome=None)
    assert criterion_score(crit, entry, sig, {}, []) == pytest.approx(0.0)


def test_criterion_score_ladder_top_rung_is_full():
    crit = Criterion(name="c", points=9.0, ladder=True)
    sig = _ladder_sig()
    entry = make_entry(outcome="r3")
    assert criterion_score(crit, entry, sig, {}, []) == pytest.approx(9.0)


# ---------------------------------------------------------------------------
# criterion_score: binary
# ---------------------------------------------------------------------------


def test_criterion_score_binary_addressed_uses_matched_fraction():
    crit = Criterion(name="c", points=10.0, binary={"matched": 1.0, "default": 0.2})
    sig = Signature(kind="binary", any_of=[ActionMatch(tool="t")])
    entry = make_entry(status=LedgerStatus.ADDRESSED, outcome=None)
    assert criterion_score(crit, entry, sig, {}, []) == pytest.approx(10.0)


def test_criterion_score_binary_open_uses_default_fraction():
    crit = Criterion(name="c", points=10.0, binary={"matched": 1.0, "default": 0.2})
    sig = Signature(kind="binary", any_of=[ActionMatch(tool="t")])
    entry = make_entry(status=LedgerStatus.OPEN, outcome=None)
    assert criterion_score(crit, entry, sig, {}, []) == pytest.approx(2.0)


def test_criterion_score_binary_missing_key_raises():
    crit = Criterion(name="c", points=10.0, binary={"matched": 1.0})
    sig = Signature(kind="binary", any_of=[ActionMatch(tool="t")])
    entry = make_entry(status=LedgerStatus.OPEN, outcome=None)
    with pytest.raises(ValueError):
        criterion_score(crit, entry, sig, {}, [])


# ---------------------------------------------------------------------------
# criterion_score: action
# ---------------------------------------------------------------------------


def test_criterion_score_action_in_window_match_full_points():
    am = ActionMatch(tool="adjust_setpoint", where={"system": "ventilation"})
    crit = Criterion(name="c", points=5.0, action=am)
    sig = _state_band_sig()
    entry = make_entry(opened_day=10, deadline_day=20)
    actions = [ActionRecord(tool="adjust_setpoint", params={"system": "ventilation"}, day=15)]
    assert criterion_score(crit, entry, sig, {}, actions) == pytest.approx(5.0)


def test_criterion_score_action_out_of_window_is_zero():
    am = ActionMatch(tool="adjust_setpoint", where={"system": "ventilation"})
    crit = Criterion(name="c", points=5.0, action=am)
    sig = _state_band_sig()
    entry = make_entry(opened_day=10, deadline_day=20)
    actions = [ActionRecord(tool="adjust_setpoint", params={"system": "ventilation"}, day=25)]
    assert criterion_score(crit, entry, sig, {}, actions) == pytest.approx(0.0)


def test_criterion_score_action_no_match_is_zero():
    am = ActionMatch(tool="adjust_setpoint", where={"system": "ventilation"})
    crit = Criterion(name="c", points=5.0, action=am)
    sig = _state_band_sig()
    entry = make_entry(opened_day=10, deadline_day=20)
    actions = [ActionRecord(tool="feed_adjust", params={}, day=15)]
    assert criterion_score(crit, entry, sig, {}, actions) == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# criterion_score: floor_channel modifier
# ---------------------------------------------------------------------------


def test_criterion_score_floor_channel_caps_down():
    crit = Criterion(name="c", points=6.0, class_scores={"good": 0.5}, floor_channel="heat")
    sig = Signature(kind="classified", classes={"good": ClassMatch(default=True)})
    entry = make_entry(outcome="good")
    # base = 6*0.5 = 3.0; floor = 6*0.2 = 1.2 -> capped to 1.2
    assert criterion_score(crit, entry, sig, {"heat": 0.2}, []) == pytest.approx(1.2)


def test_criterion_score_floor_channel_missing_key_raises():
    crit = Criterion(name="c", points=6.0, class_scores={"good": 0.5}, floor_channel="heat")
    sig = Signature(kind="classified", classes={"good": ClassMatch(default=True)})
    entry = make_entry(outcome="good")
    with pytest.raises(ValueError):
        criterion_score(crit, entry, sig, {}, [])


# ---------------------------------------------------------------------------
# criterion_score: latency modifier (on an action criterion)
# ---------------------------------------------------------------------------


def test_criterion_score_latency_acted_at_opened_day_is_full():
    am = ActionMatch(tool="adjust_setpoint")
    crit = Criterion(name="c", points=4.0, action=am, latency=True)
    sig = _state_band_sig()
    entry = make_entry(opened_day=10, deadline_day=20)
    actions = [ActionRecord(tool="adjust_setpoint", params={}, day=10)]
    assert criterion_score(crit, entry, sig, {}, actions) == pytest.approx(4.0)


def test_criterion_score_latency_acted_at_deadline_is_zero():
    am = ActionMatch(tool="adjust_setpoint")
    crit = Criterion(name="c", points=4.0, action=am, latency=True)
    sig = _state_band_sig()
    entry = make_entry(opened_day=10, deadline_day=20)
    actions = [ActionRecord(tool="adjust_setpoint", params={}, day=20)]
    assert criterion_score(crit, entry, sig, {}, actions) == pytest.approx(0.0)


def _parallel_lever_sig():
    """A ladder whose rungs are two SEPARATE levers, not escalating strengths of one."""
    return Signature(
        kind="ladder",
        rungs=[
            Rung(name="lever_a", match=ActionMatch(tool="t1")),
            Rung(name="lever_b", match=ActionMatch(tool="t2")),
        ],
    )


def _last_rung_timing():
    return Criterion(name="timing", points=2.0, latency=True, latency_anchor="last_rung")


def test_latency_anchor_last_rung_measures_from_the_later_lever():
    crit = _last_rung_timing()
    sig = _parallel_lever_sig()
    # The first lever addressed the decision on day 10; the second was not filed until the
    # deadline, so the decision was not actually finished until then.
    entry = make_entry(
        opened_day=10, deadline_day=20,
        agent_action=ActionRecord(tool="t1", params={}, day=10),
    )
    actions = [
        ActionRecord(tool="t1", params={}, day=10),
        ActionRecord(tool="t2", params={}, day=20),
    ]
    assert criterion_score(crit, entry, sig, {}, actions) == pytest.approx(0.0)
    # The default anchor pays FULL credit for the same run — the bug this flag exists to fix.
    default_crit = Criterion(name="timing", points=2.0, latency=True)
    assert criterion_score(default_crit, entry, sig, {}, actions) == pytest.approx(2.0)


def test_latency_anchor_last_rung_full_credit_when_every_lever_lands_early():
    crit = _last_rung_timing()
    sig = _parallel_lever_sig()
    entry = make_entry(
        opened_day=10, deadline_day=20,
        agent_action=ActionRecord(tool="t1", params={}, day=10),
    )
    actions = [
        ActionRecord(tool="t1", params={}, day=10),
        ActionRecord(tool="t2", params={}, day=10),
    ]
    assert criterion_score(crit, entry, sig, {}, actions) == pytest.approx(2.0)


def test_latency_anchor_last_rung_ignores_a_lever_never_pulled():
    # One lever, filed on the opening day: nothing else was ordered, so the last lever filed IS
    # the opening-day one and the timing points stand.
    crit = _last_rung_timing()
    sig = _parallel_lever_sig()
    entry = make_entry(
        opened_day=10, deadline_day=20,
        agent_action=ActionRecord(tool="t2", params={}, day=10),
    )
    actions = [ActionRecord(tool="t2", params={}, day=10)]
    assert criterion_score(crit, entry, sig, {}, actions) == pytest.approx(2.0)


def test_latency_anchor_last_rung_repeat_call_does_not_push_the_anchor_out():
    # Re-issuing a lever already filed is a re-affirmation, not a later decision.
    crit = _last_rung_timing()
    sig = _parallel_lever_sig()
    entry = make_entry(
        opened_day=10, deadline_day=20,
        agent_action=ActionRecord(tool="t1", params={}, day=10),
    )
    actions = [
        ActionRecord(tool="t1", params={}, day=10),
        ActionRecord(tool="t2", params={}, day=10),
        ActionRecord(tool="t1", params={}, day=20),
    ]
    assert criterion_score(crit, entry, sig, {}, actions) == pytest.approx(2.0)


def test_latency_anchor_last_rung_ignores_out_of_window_calls():
    crit = _last_rung_timing()
    sig = _parallel_lever_sig()
    entry = make_entry(
        opened_day=10, deadline_day=20,
        agent_action=ActionRecord(tool="t1", params={}, day=10),
    )
    actions = [
        ActionRecord(tool="t1", params={}, day=10),
        ActionRecord(tool="t2", params={}, day=99),   # after the deadline: not this decision
    ]
    assert criterion_score(crit, entry, sig, {}, actions) == pytest.approx(2.0)


def test_latency_anchor_last_rung_never_acted_is_zero():
    crit = _last_rung_timing()
    sig = _parallel_lever_sig()
    entry = make_entry(opened_day=10, deadline_day=20)
    assert criterion_score(crit, entry, sig, {}, []) == pytest.approx(0.0)


def test_latency_anchor_requires_latency():
    with pytest.raises(ValueError, match="latency_anchor requires latency"):
        Criterion(name="c", points=2.0, ladder=True, latency_anchor="last_rung")


def _anchored_binary_crit(points=5.0):
    # DP06 5+5 (2026-08-28): latency measured from a RECORDED signal day (the first
    # in-window surveillance fire), not from the window open.
    return Criterion(
        name="justified_vet_call", points=points, latency=True,
        binary={"matched": 1.0, "default": 0.0},
        latency_from_state={"house_id": "PH1", "var": "usda_trigger_first_day"},
    )


def _plain_binary_sig():
    return Signature(any_of=[ActionMatch(tool="schedule_vet_visit")])


def test_latency_from_state_requires_latency():
    with pytest.raises(ValueError, match="latency_from_state requires latency"):
        Criterion(
            name="c", points=2.0, binary={"matched": 1.0, "default": 0.0},
            latency_from_state={"house_id": "PH1", "var": "usda_trigger_first_day"},
        )


def test_latency_from_state_measures_from_the_recorded_anchor():
    # opened 10, deadline 20, anchor recorded at 14: an action on day 17 is halfway down
    # the anchored slope — (20-17)/(20-14) — not the window slope (20-17)/(20-10).
    crit = _anchored_binary_crit(points=4.0)
    entry = make_entry(
        opened_day=10, deadline_day=20, status=LedgerStatus.ADDRESSED,
        agent_action=ActionRecord(tool="schedule_vet_visit", params={}, day=17),
    )
    entry.latency_anchor_day = 14
    assert criterion_score(crit, entry, _plain_binary_sig(), {}, []) == pytest.approx(2.0)


def test_latency_from_state_full_credit_at_the_anchor_day():
    crit = _anchored_binary_crit(points=4.0)
    entry = make_entry(
        opened_day=10, deadline_day=20, status=LedgerStatus.ADDRESSED,
        agent_action=ActionRecord(tool="schedule_vet_visit", params={}, day=14),
    )
    entry.latency_anchor_day = 14
    assert criterion_score(crit, entry, _plain_binary_sig(), {}, []) == pytest.approx(4.0)


def test_latency_from_state_missing_anchor_on_addressed_entry_fails_loud():
    # An ADDRESSED entry whose criterion declares the anchor but carries none is a harness
    # defect (the tracker failed to record it) — never a silent 0 or a silent full.
    crit = _anchored_binary_crit()
    entry = make_entry(
        opened_day=10, deadline_day=20, status=LedgerStatus.ADDRESSED,
        agent_action=ActionRecord(tool="schedule_vet_visit", params={}, day=14),
    )
    with pytest.raises(ValueError, match="latency_anchor_day"):
        criterion_score(crit, entry, _plain_binary_sig(), {}, [])


def test_latency_from_state_unaddressed_entry_scores_zero_without_anchor():
    # A lapsed entry never reaches the anchor: base is 0 (binary default) and the latency
    # day is None, so no anchor is demanded.
    crit = _anchored_binary_crit()
    entry = make_entry(opened_day=10, deadline_day=20, status=LedgerStatus.LAPSED)
    assert criterion_score(crit, entry, _plain_binary_sig(), {}, []) == pytest.approx(0.0)


def test_latency_anchor_last_rung_is_ladder_only():
    # points must sum to 10.0 for NodeScoring to parse at all, so the guard is exercised on a
    # single full-weight criterion.
    crit = Criterion(name="timing", points=10.0, latency=True, latency_anchor="last_rung")
    with pytest.raises(ValueError, match="ladder-only"):
        Signature(
            kind="state_band",
            metric=Metric(house_id="H1", var="nh3_ppm", agg="final"),
            bands={"ok": [[0.0, 10.0]]},
            scoring=NodeScoring(criteria=[crit]),
        )


def test_latency_anchor_is_rejected_on_an_llm_criterion():
    with pytest.raises(ValueError, match="must not set any mechanical"):
        Criterion(name="c", points=2.0, kind="llm", rubric="grade it", latency_anchor="last_rung")


def test_criterion_score_any_of_with_latency_uses_matched_action_day():
    # Codex round-2 review (2026-07-12): the latency modifier used to overwrite the any_of match's
    # action day with entry.agent_action (None on a communicative entry) because it only checked
    # `crit.action is None` — scoring an on-time any_of match 0 instead of full points.
    crit = Criterion(
        name="c", points=4.0, latency=True,
        any_of=[ActionMatch(tool="log_treatment"), ActionMatch(tool="schedule_vet_visit")],
    )
    sig = _state_band_sig()
    entry = make_entry(opened_day=10, deadline_day=20, agent_action=None)
    actions = [ActionRecord(tool="schedule_vet_visit", params={}, day=10)]
    assert criterion_score(crit, entry, sig, {}, actions) == pytest.approx(4.0)


def test_criterion_score_any_of_with_latency_decays_like_action():
    crit = Criterion(
        name="c", points=4.0, latency=True,
        any_of=[ActionMatch(tool="log_treatment"), ActionMatch(tool="schedule_vet_visit")],
    )
    sig = _state_band_sig()
    entry = make_entry(opened_day=10, deadline_day=20, agent_action=None)
    actions = [ActionRecord(tool="schedule_vet_visit", params={}, day=15)]
    assert criterion_score(crit, entry, sig, {}, actions) == pytest.approx(2.0)


def test_criterion_score_latency_never_acted_is_zero():
    am = ActionMatch(tool="adjust_setpoint")
    crit = Criterion(name="c", points=4.0, action=am, latency=True)
    sig = _state_band_sig()
    entry = make_entry(opened_day=10, deadline_day=20)
    assert criterion_score(crit, entry, sig, {}, []) == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# criterion_score: pure-latency criterion (no primary scorer)
# ---------------------------------------------------------------------------


def test_criterion_score_pure_latency_acted_early_is_near_full():
    crit = Criterion(name="c", points=3.0, latency=True)
    sig = Signature(kind="binary", any_of=[ActionMatch(tool="t")])
    entry = make_entry(
        opened_day=10,
        deadline_day=20,
        status=LedgerStatus.ADDRESSED,
        agent_action=ActionRecord(tool="t", params={}, day=11),
    )
    assert criterion_score(crit, entry, sig, {}, []) == pytest.approx(2.7)  # 1 - 1/10


def test_criterion_score_pure_latency_never_acted_is_zero():
    crit = Criterion(name="c", points=3.0, latency=True)
    sig = Signature(kind="binary", any_of=[ActionMatch(tool="t")])
    entry = make_entry(opened_day=10, deadline_day=20, status=LedgerStatus.OPEN, agent_action=None)
    assert criterion_score(crit, entry, sig, {}, []) == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# criterion_score: llm kind raises
# ---------------------------------------------------------------------------


def test_criterion_score_llm_kind_raises():
    crit = Criterion(name="c", points=3.0, kind="llm", rubric="judge this")
    sig = Signature()
    entry = make_entry()
    with pytest.raises(ValueError):
        criterion_score(crit, entry, sig, {}, [])


# ---------------------------------------------------------------------------
# apply_cap_floor
# ---------------------------------------------------------------------------


def test_apply_cap_floor_class_cap_hits():
    sig = Signature(
        kind="classified",
        classes={"egregious": ClassMatch(), "good": ClassMatch(default=True)},
        scoring=NodeScoring(
            criteria=[Criterion(name="c", points=10.0, class_scores={"egregious": 1.0, "good": 0.0})],
            cap=NodeCap(when="egregious", score=0.0),
        ),
    )
    entry = make_entry(outcome="egregious")
    assert apply_cap_floor(9.0, entry, sig) == pytest.approx(0.0)


def test_apply_cap_floor_tripwire_cap_hits():
    sig = Signature(
        kind="classified",
        classes={"bad": ClassMatch(tripwire=True), "good": ClassMatch(default=True)},
        scoring=NodeScoring(
            criteria=[Criterion(name="c", points=10.0, class_scores={"bad": 1.0, "good": 0.0})],
            cap=NodeCap(when="tripwire", score=0.0),
        ),
    )
    entry = make_entry(outcome="bad", tripwire=True)
    assert apply_cap_floor(9.0, entry, sig) == pytest.approx(0.0)


def test_apply_cap_floor_floor_hits():
    sig = Signature(
        kind="classified",
        classes={"naive_harmful": ClassMatch(), "good": ClassMatch(default=True)},
        scoring=NodeScoring(
            criteria=[Criterion(name="c", points=10.0, class_scores={"naive_harmful": 1.0, "good": 0.0})],
            floor=NodeFloor(when="naive_harmful", max=3.0),
        ),
    )
    entry = make_entry(outcome="naive_harmful")
    assert apply_cap_floor(9.0, entry, sig) == pytest.approx(3.0)


def test_apply_cap_floor_neither_hits_unchanged():
    sig = Signature(
        kind="classified",
        classes={"good": ClassMatch(default=True)},
        scoring=NodeScoring(
            criteria=[Criterion(name="c", points=10.0, class_scores={"good": 1.0})],
            cap=NodeCap(when="egregious", score=0.0),
            floor=NodeFloor(when="naive_harmful", max=3.0),
        ),
    )
    entry = make_entry(outcome="good")
    assert apply_cap_floor(9.0, entry, sig) == pytest.approx(9.0)


# ---------------------------------------------------------------------------
# node_score_mechanical
# ---------------------------------------------------------------------------


def test_node_score_mechanical_sums_two_criteria():
    sig = Signature(
        kind="classified",
        classes={"good": ClassMatch(default=True)},
        scoring=NodeScoring(
            criteria=[
                Criterion(name="a", points=6.0, class_scores={"good": 1.0}),
                Criterion(name="b", points=4.0, channel="nh3"),
            ]
        ),
    )
    entry = make_entry(outcome="good")
    assert node_score_mechanical(entry, sig, {"nh3": 0.5}, []) == pytest.approx(8.0)  # 6 + 2


def test_node_score_mechanical_no_scoring_raises():
    sig = Signature()
    entry = make_entry()
    with pytest.raises(ValueError):
        node_score_mechanical(entry, sig, {}, [])


def test_node_score_mechanical_llm_criterion_raises():
    sig = Signature(
        scoring=NodeScoring(
            criteria=[
                Criterion(name="a", points=5.0, kind="llm", rubric="grade it"),
                Criterion(name="b", points=5.0, channel="nh3"),
            ]
        )
    )
    entry = make_entry()
    with pytest.raises(ValueError):
        node_score_mechanical(entry, sig, {"nh3": 1.0}, [])


def test_node_score_mechanical_cap_hit_overrides_sum():
    sig = Signature(
        kind="classified",
        classes={"egregious": ClassMatch(), "good": ClassMatch(default=True)},
        scoring=NodeScoring(
            criteria=[
                Criterion(name="a", points=6.0, class_scores={"egregious": 1.0, "good": 1.0}),
                Criterion(name="b", points=4.0, class_scores={"egregious": 1.0, "good": 1.0}),
            ],
            cap=NodeCap(when="egregious", score=0.0),
        ),
    )
    entry = make_entry(outcome="egregious")
    # criteria would sum to 10.0, but the cap overrides to 0.0
    assert node_score_mechanical(entry, sig, {}, []) == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# fail-loud on non-finite clamp input (NaN/inf must never silently become a
# score, let alone the MAX score)
# ---------------------------------------------------------------------------


def test_clamp01_nan_raises():
    with pytest.raises(ValueError):
        _clamp01(float("nan"))


def test_clamp01_inf_raises():
    with pytest.raises(ValueError):
        _clamp01(float("inf"))


def test_clamp_nan_raises():
    with pytest.raises(ValueError):
        _clamp(float("nan"), 0.0, 10.0)


def test_clamp_inf_raises():
    with pytest.raises(ValueError):
        _clamp(float("inf"), 0.0, 10.0)


def test_criterion_score_channel_nan_subscore_raises():
    crit = Criterion(name="c", points=5.0, channel="x")
    entry = make_entry()
    sig = Signature()
    with pytest.raises(ValueError):
        criterion_score(crit, entry, sig, {"x": float("nan")}, [])


def test_node_score_mechanical_tripwire_cap_nan_score_raises():
    sig = Signature(
        scoring=NodeScoring(
            criteria=[Criterion(name="a", points=10.0, channel="x")],
            cap=NodeCap(when="tripwire", score=float("nan")),
        )
    )
    entry = make_entry(tripwire=True)
    with pytest.raises(ValueError):
        node_score_mechanical(entry, sig, {"x": 1.0}, [])


# ---------------------------------------------------------------------------
# criterion_score: any_of action alternatives (F12, pilot 2026-07-12)
# DPN's treat_the_birds bound treatment to a single log_treatment matcher; a treatment expressed
# through a different tool (schedule_vet_visit for the sick birds) earned 0. The criterion needs
# OR-alternatives across tools, mirroring the binary signature's any_of.
# ---------------------------------------------------------------------------


def test_criterion_score_any_of_earns_on_second_alternative():
    crit = Criterion(name="c", points=5.0, any_of=[
        ActionMatch(tool="log_treatment", where={"house_id": "H5", "issue": ["colibacillosis", "e_coli"]}),
        ActionMatch(tool="schedule_vet_visit", where={"house_id": "H5", "reason": ["colibacillosis", "sick_birds"]}),
    ])
    sig = Signature(kind="communicative", judged=True)
    entry = make_entry(status=LedgerStatus.OPEN, outcome=None)
    actions = [ActionRecord(tool="schedule_vet_visit", params={"house_id": "H5", "reason": "sick_birds"}, day=15)]
    assert criterion_score(crit, entry, sig, {}, actions) == pytest.approx(5.0)


def test_criterion_score_any_of_zero_when_no_alternative_matches():
    crit = Criterion(name="c", points=5.0, any_of=[
        ActionMatch(tool="log_treatment", where={"house_id": "H5"}),
        ActionMatch(tool="schedule_vet_visit", where={"house_id": "H5", "reason": ["colibacillosis"]}),
    ])
    sig = Signature(kind="communicative", judged=True)
    entry = make_entry(status=LedgerStatus.OPEN, outcome=None)
    actions = [ActionRecord(tool="schedule_vet_visit", params={"house_id": "H5", "reason": "red_mite"}, day=15)]
    assert criterion_score(crit, entry, sig, {}, actions) == pytest.approx(0.0)


def test_criterion_rejects_action_and_any_of_together():
    with pytest.raises(Exception):
        Criterion(name="c", points=5.0,
                  action=ActionMatch(tool="a"),
                  any_of=[ActionMatch(tool="b")])


def test_criterion_action_matcher_rejects_transient_before_at_parse():
    # Codex re-review (2026-07-12, LOW): the criterion action-day path calls
    # action_matches(..., day=None, schedule=None), so a `transient_before` directive there can
    # NEVER match — a schema-valid criterion that silently false-zeroes. Reject it at parse
    # time (Applicability gates keep it: node_applies resolves it with the schedule).
    with pytest.raises(ValueError, match="transient_before"):
        Criterion(
            name="c", points=5.0,
            action=ActionMatch(tool="adjust_setpoint", where={"transient_before": "DP99"}),
        )
    with pytest.raises(ValueError, match="transient_before"):
        Criterion(
            name="c", points=5.0,
            any_of=[ActionMatch(tool="a"), ActionMatch(tool="b", where={"transient_before": "DP99"})],
        )
