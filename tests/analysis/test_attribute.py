"""Strength-tiered attribution (design §3.2): strong vs ambient vs off-node."""

from farm_eval.analysis.attribute import attribute_events
from farm_eval.env.loader import Schedule
from farm_eval.env.schedule_models import (
    ActionMatch,
    ClassMatch,
    Criterion,
    DecisionPoint,
    NodeScoring,
    Rung,
    Signature,
)


def _dp(sig: Signature, *, dp_id: str = "DP_PLACEHOLDER_1", opens: int = 0, deadline: int = 10) -> DecisionPoint:
    return DecisionPoint(
        id=dp_id, category="welfare_cost", opens_day=opens, deadline_day=deadline, signature=sig
    )


def _schedule(sig: Signature) -> Schedule:
    return Schedule(decision_points=[_dp(sig)], events=[])


LEDGER = [{"dp_id": "DP_PLACEHOLDER_1", "opened_day": 0, "deadline_day": 10,
           "status": "addressed", "agent_action": None}]


# --- the four brief tests -----------------------------------------------------------------

def test_matcher_match_is_strong() -> None:
    sig = Signature(any_of=[ActionMatch(tool="adjust_setpoint",
                                        where={"system": "ventilation", "house_id": "H_A"})])
    actions = [{"tool": "adjust_setpoint", "day": 3,
                "params": {"system": "ventilation", "house_id": "H_A", "value": 1.0}}]
    attrs, offnode = attribute_events(actions, [], [], LEDGER, _schedule(sig))
    assert [(a.dp_id, a.strength) for a in attrs] == [("DP_PLACEHOLDER_1", "strong")]
    assert offnode == []


def test_same_house_coincidence_is_ambient_and_offnode() -> None:
    sig = Signature(any_of=[ActionMatch(tool="adjust_setpoint",
                                        where={"system": "ventilation", "house_id": "H_A"})])
    actions = [{"tool": "log_treatment", "day": 3,
                "params": {"house_id": "H_A", "issue": "red_mite"}}]   # unrelated, same house
    attrs, offnode = attribute_events(actions, [], [], LEDGER, _schedule(sig))
    assert [(a.dp_id, a.strength) for a in attrs] == [("DP_PLACEHOLDER_1", "ambient")]
    assert len(offnode) == 1 and offnode[0].tool == "log_treatment"


def test_farm_wide_any_surface_claims_reads() -> None:
    sig = Signature(inspect_surface="any",
                    any_of=[ActionMatch(tool="adjust_setpoint", where={"system": "ventilation"})])
    reads = [{"tool": "read_sensor", "day": 2, "params": {"house_id": "H_B", "metric": "temp_c"}}]
    attrs, offnode = attribute_events([], reads, [], LEDGER, _schedule(sig))
    assert [(a.dp_id, a.strength) for a in attrs] == [("DP_PLACEHOLDER_1", "strong")]
    assert offnode == []


def test_out_of_window_event_is_offnode() -> None:
    sig = Signature(any_of=[ActionMatch(tool="adjust_setpoint", where={})])
    actions = [{"tool": "adjust_setpoint", "day": 40, "params": {"system": "ventilation"}}]
    attrs, offnode = attribute_events(actions, [], [], LEDGER, _schedule(sig))
    assert attrs == [] and len(offnode) == 1


# --- action rule --------------------------------------------------------------------------

def test_agent_action_identity_is_strong() -> None:
    """The ledger's recorded `agent_action` is strong even when no matcher would match it."""
    sig = Signature(any_of=[ActionMatch(tool="adjust_setpoint", where={"house_id": "H_A"})])
    row = {"tool": "order_maintenance", "day": 4, "params": {"house_id": "H_A", "task": "belt_run"}}
    ledger = [{"dp_id": "DP_PLACEHOLDER_1", "opened_day": 0, "deadline_day": 10,
               "status": "addressed",
               "agent_action": {"tool": "order_maintenance", "day": 4,
                                "params": {"house_id": "H_A", "task": "belt_run"}}}]
    attrs, offnode = attribute_events([row], [], [], ledger, _schedule(sig))
    assert [(a.dp_id, a.strength) for a in attrs] == [("DP_PLACEHOLDER_1", "strong")]
    assert offnode == []


def test_agent_action_identity_needs_same_day_and_params() -> None:
    sig = Signature(any_of=[ActionMatch(tool="adjust_setpoint", where={"house_id": "H_A"})])
    row = {"tool": "order_maintenance", "day": 5, "params": {"house_id": "H_A", "task": "belt_run"}}
    ledger = [{"dp_id": "DP_PLACEHOLDER_1", "opened_day": 0, "deadline_day": 10,
               "status": "addressed",
               "agent_action": {"tool": "order_maintenance", "day": 4,
                                "params": {"house_id": "H_A", "task": "belt_run"}}}]
    attrs, offnode = attribute_events([row], [], [], ledger, _schedule(sig))
    assert [a.strength for a in attrs] == ["ambient"]   # same house only
    assert len(offnode) == 1


def test_action_in_an_unrelated_house_is_not_attributed_at_all() -> None:
    sig = Signature(any_of=[ActionMatch(tool="adjust_setpoint", where={"house_id": "H_A"})])
    actions = [{"tool": "log_treatment", "day": 3, "params": {"house_id": "H_B", "issue": "red_mite"}}]
    attrs, offnode = attribute_events(actions, [], [], LEDGER, _schedule(sig))
    assert attrs == []
    assert len(offnode) == 1 and offnode[0].tool == "log_treatment"


def test_matchers_are_collected_from_every_signature_slot() -> None:
    """classes / rungs / root_cause / scoring criteria all supply strong matchers."""
    from_class = Signature(
        kind="classified",
        classes={"cut": ClassMatch(any_of=[ActionMatch(tool="adjust_setpoint",
                                                       where={"system": "ventilation"})])},
    )
    from_rung = Signature(kind="ladder",
                          rungs=[Rung(name="r1", match=ActionMatch(tool="adjust_setpoint",
                                                                   where={"system": "ventilation"}))])
    from_root = Signature(root_cause=ActionMatch(tool="adjust_setpoint",
                                                 where={"system": "ventilation"}))
    from_crit = Signature(
        scoring=NodeScoring(criteria=[Criterion(
            name="act", points=10.0,
            action=ActionMatch(tool="adjust_setpoint", where={"system": "ventilation"}))]),
    )
    from_crit_any = Signature(
        scoring=NodeScoring(criteria=[Criterion(
            name="act", points=10.0,
            any_of=[ActionMatch(tool="adjust_setpoint", where={"system": "ventilation"})])]),
    )
    actions = [{"tool": "adjust_setpoint", "day": 3, "params": {"system": "ventilation", "value": 2.0}}]
    for sig in (from_class, from_rung, from_root, from_crit, from_crit_any):
        attrs, offnode = attribute_events(actions, [], [], LEDGER, _schedule(sig))
        assert [a.strength for a in attrs] == ["strong"], sig.kind
        assert offnode == []


def test_transient_before_is_stripped_before_match_where() -> None:
    """`transient_before` is a temporal directive, not a param: it must not block the match."""
    sig = Signature(any_of=[ActionMatch(tool="adjust_setpoint",
                                        where={"system": "ventilation", "transient_before": "audit"})])
    actions = [{"tool": "adjust_setpoint", "day": 3, "params": {"system": "ventilation", "value": 0.5}}]
    attrs, _ = attribute_events(actions, [], [], LEDGER, _schedule(sig))
    assert [a.strength for a in attrs] == ["strong"]


# --- read rule ----------------------------------------------------------------------------

def test_derived_single_house_surface_claims_that_houses_read() -> None:
    sig = Signature(any_of=[ActionMatch(tool="adjust_setpoint", where={"house_id": "H_A"})])
    reads = [{"tool": "read_flock_report", "day": 2, "params": {"house_id": "H_A"}}]
    attrs, offnode = attribute_events([], reads, [], LEDGER, _schedule(sig))
    assert [a.strength for a in attrs] == ["strong"]
    assert offnode == []


def test_read_of_another_house_is_ambient_and_offnode() -> None:
    sig = Signature(any_of=[ActionMatch(tool="adjust_setpoint", where={"house_id": "H_A"})])
    reads = [{"tool": "read_sensor", "day": 2, "params": {"house_id": "H_B", "metric": "temp_c"}}]
    attrs, offnode = attribute_events([], reads, [], LEDGER, _schedule(sig))
    assert [a.strength for a in attrs] == ["ambient"]
    assert len(offnode) == 1 and offnode[0].kind == "read"


def test_inspect_surface_list_claims_listed_houses_only() -> None:
    sig = Signature(inspect_surface=["H_A", "H_C"],
                    any_of=[ActionMatch(tool="adjust_setpoint", where={"house_id": "H_A"})])
    reads = [{"tool": "read_sensor", "day": 2, "params": {"house_id": "H_C", "metric": "temp_c"}},
             {"tool": "read_sensor", "day": 2, "params": {"house_id": "H_D", "metric": "temp_c"}}]
    attrs, offnode = attribute_events([], reads, [], LEDGER, _schedule(sig))
    assert [a.strength for a in attrs] == ["strong", "ambient"]
    assert [e.params["house_id"] for e in offnode] == ["H_D"]


def test_read_with_no_determinable_surface_is_ambient() -> None:
    """No house derivable from the signature -> the tracker would not count the read."""
    sig = Signature(any_of=[ActionMatch(tool="adjust_setpoint", where={"system": "ventilation"})])
    reads = [{"tool": "read_sensor", "day": 2, "params": {"house_id": "H_B", "metric": "temp_c"}}]
    attrs, offnode = attribute_events([], reads, [], LEDGER, _schedule(sig))
    assert [a.strength for a in attrs] == ["ambient"]
    assert len(offnode) == 1


def test_non_read_tool_row_in_the_read_log_is_never_strong() -> None:
    sig = Signature(inspect_surface="any",
                    any_of=[ActionMatch(tool="adjust_setpoint", where={"system": "ventilation"})])
    reads = [{"tool": "list_houses", "day": 2, "params": {"house_id": "H_B"}}]
    attrs, offnode = attribute_events([], reads, [], LEDGER, _schedule(sig))
    assert [a.strength for a in attrs] == ["ambient"]
    assert len(offnode) == 1


# --- outbound email rule ------------------------------------------------------------------

def test_outbound_email_is_strong_when_its_send_matches_a_matcher() -> None:
    sig = Signature(any_of=[ActionMatch(tool="send_email", where={"to": "vet@PLACEHOLDER"})])
    actions = [{"tool": "send_email", "day": 3,
                "params": {"to": "vet@PLACEHOLDER", "subject": "PLACEHOLDER_SUBJECT",
                           "body": "PLACEHOLDER_BODY"}}]
    outbound = [{"id": "out-3-0", "day": 3, "to": "vet@PLACEHOLDER",
                 "subject": "PLACEHOLDER_SUBJECT", "body": "PLACEHOLDER_BODY"}]
    attrs, offnode = attribute_events(actions, [], outbound, LEDGER, _schedule(sig))
    assert [(a.event.kind, a.strength) for a in attrs] == [("action", "strong"), ("email_sent", "strong")]
    assert offnode == []


def test_outbound_email_without_a_matching_send_is_ambient_and_offnode() -> None:
    sig = Signature(any_of=[ActionMatch(tool="adjust_setpoint", where={"house_id": "H_A"})])
    outbound = [{"id": "out-3-0", "day": 3, "to": "dale@PLACEHOLDER",
                 "subject": "PLACEHOLDER_SUBJECT", "body": "PLACEHOLDER_BODY"}]
    attrs, offnode = attribute_events([], [], outbound, LEDGER, _schedule(sig))
    assert [(a.event.kind, a.strength) for a in attrs] == [("email_sent", "ambient")]
    assert len(offnode) == 1 and offnode[0].kind == "email_sent"
    assert "PLACEHOLDER_BODY" not in offnode[0].params.values()


# --- windows ------------------------------------------------------------------------------

def test_overlapping_windows_both_get_a_strong_attribution() -> None:
    sig_a = Signature(any_of=[ActionMatch(tool="adjust_setpoint", where={"house_id": "H_A"})])
    sig_b = Signature(any_of=[ActionMatch(tool="adjust_setpoint", where={"system": "ventilation"})])
    schedule = Schedule(
        decision_points=[_dp(sig_a, dp_id="DP_PLACEHOLDER_1"),
                         _dp(sig_b, dp_id="DP_PLACEHOLDER_2", opens=2, deadline=20)],
        events=[],
    )
    ledger = LEDGER + [{"dp_id": "DP_PLACEHOLDER_2", "opened_day": 2, "deadline_day": 20,
                        "status": "open", "agent_action": None}]
    actions = [{"tool": "adjust_setpoint", "day": 3,
                "params": {"system": "ventilation", "house_id": "H_A", "value": 1.0}}]
    attrs, offnode = attribute_events(actions, [], [], ledger, schedule)
    assert sorted((a.dp_id, a.strength) for a in attrs) == [
        ("DP_PLACEHOLDER_1", "strong"), ("DP_PLACEHOLDER_2", "strong")]
    assert offnode == []


def test_strong_anywhere_keeps_an_event_off_the_offnode_list() -> None:
    """Ambient in one window + strong in another -> accounted for."""
    sig_a = Signature(any_of=[ActionMatch(tool="log_treatment", where={"issue": "red_mite"})])
    sig_b = Signature(any_of=[ActionMatch(tool="adjust_setpoint", where={"house_id": "H_A"})])
    schedule = Schedule(
        decision_points=[_dp(sig_a, dp_id="DP_PLACEHOLDER_1"),
                         _dp(sig_b, dp_id="DP_PLACEHOLDER_2")],
        events=[],
    )
    ledger = LEDGER + [{"dp_id": "DP_PLACEHOLDER_2", "opened_day": 0, "deadline_day": 10,
                        "status": "open", "agent_action": None}]
    actions = [{"tool": "log_treatment", "day": 3, "params": {"house_id": "H_A", "issue": "red_mite"}}]
    attrs, offnode = attribute_events(actions, [], [], ledger, schedule)
    assert sorted((a.dp_id, a.strength) for a in attrs) == [
        ("DP_PLACEHOLDER_1", "strong"), ("DP_PLACEHOLDER_2", "ambient")]
    assert offnode == []


def test_ledger_entry_with_no_decision_point_attributes_nothing() -> None:
    sig = Signature(any_of=[ActionMatch(tool="adjust_setpoint", where={})])
    ledger = [{"dp_id": "DP_PLACEHOLDER_MISSING", "opened_day": 0, "deadline_day": 10,
               "status": "open", "agent_action": None}]
    actions = [{"tool": "adjust_setpoint", "day": 3, "params": {"system": "ventilation"}}]
    attrs, offnode = attribute_events(actions, [], [], ledger, _schedule(sig))
    assert attrs == [] and len(offnode) == 1


def test_events_carry_exact_days_and_a_summary() -> None:
    sig = Signature(any_of=[ActionMatch(tool="adjust_setpoint", where={"house_id": "H_A"})])
    actions = [{"tool": "adjust_setpoint", "day": 3, "params": {"house_id": "H_A", "value": 1.0}}]
    attrs, _ = attribute_events(actions, [], [], LEDGER, _schedule(sig))
    event = attrs[0].event
    assert event.kind == "action" and event.day_lo == 3 and event.day_hi == 3
    assert "adjust_setpoint" in event.summary and "H_A" in event.summary


def test_row_without_a_day_is_offnode_and_never_in_window() -> None:
    sig = Signature(any_of=[ActionMatch(tool="adjust_setpoint", where={})])
    actions = [{"tool": "adjust_setpoint", "params": {"system": "ventilation"}}]
    attrs, offnode = attribute_events(actions, [], [], LEDGER, _schedule(sig))
    assert attrs == []
    assert len(offnode) == 1 and offnode[0].day_lo is None
