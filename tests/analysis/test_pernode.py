"""Per-node behaviour dossiers (design §3.3): score join + derived timing facts."""

from farm_eval.analysis.model import Attribution, BehaviourEvent
from farm_eval.analysis.pernode import build_dossiers

# dp_a: opened 0, deadline 10 — the brief's worked example (strong events on days 2 and 7).
# dp_b: opened 3, deadline 8 — a strong action but no strong read, and no node score.
LEDGER = [
    {
        "dp_id": "dp_a", "category": "welfare_cost", "opened_day": 0, "deadline_day": 10,
        "status": "addressed", "outcome": "x", "tripwire": False, "root_cause_used": True,
        "inspected": True, "agent_action": {"tool": "foo", "params": {}, "day": 7},
    },
    {
        "dp_id": "dp_b", "category": "welfare_profit", "opened_day": 3, "deadline_day": 8,
        "status": "lapsed", "agent_action": None,
    },
]

NODE_SCORES = {"dp_a": 7.5}  # dp_b deliberately absent -> node_score None

ATTRIBUTIONS = [
    # dp_a: strong read on day 2, strong action on day 7 (input order preserved), plus one
    # ambient action on day 1 that must NOT count toward strong_action_count or the gap calc.
    Attribution(
        event=BehaviourEvent(kind="read", day_lo=2, day_hi=2, tool="read_sensor", summary="read x"),
        dp_id="dp_a", strength="strong",
    ),
    Attribution(
        event=BehaviourEvent(kind="action", day_lo=7, day_hi=7, tool="foo", summary="foo()"),
        dp_id="dp_a", strength="strong",
    ),
    Attribution(
        event=BehaviourEvent(kind="action", day_lo=1, day_hi=1, tool="bar", summary="bar()"),
        dp_id="dp_a", strength="ambient",
    ),
    # dp_b: one strong action, no strong read -> read_before_first_action must be None.
    Attribution(
        event=BehaviourEvent(kind="action", day_lo=5, day_hi=5, tool="foo", summary="foo()"),
        dp_id="dp_b", strength="strong",
    ),
    Attribution(
        event=BehaviourEvent(kind="email_sent", day_lo=4, day_hi=4, summary="email"),
        dp_id="dp_b", strength="ambient",
    ),
]


def test_build_dossiers_joins_scores_orders_and_derives() -> None:
    dossiers = build_dossiers(LEDGER, NODE_SCORES, ATTRIBUTIONS)

    # ordering: sorted by opened_day (dp_a=0 before dp_b=3), regardless of ledger input order.
    assert [d.dp_id for d in dossiers] == ["dp_a", "dp_b"]

    a, b = dossiers

    # score join by dp_id.
    assert a.node_score == 7.5
    assert b.node_score is None

    # ledger fields carried through.
    assert a.category == "welfare_cost"
    assert a.status == "addressed"
    assert a.outcome == "x"
    assert a.root_cause_used is True
    assert a.inspected is True
    assert b.tripwire is False

    # latency_days mirrors report/analyze.py: agent_action.day - opened_day, else None.
    assert a.latency_days == 7
    assert b.latency_days is None

    # strong/ambient lists: this node's attributions, in their input (transcript) order.
    assert [e.day_lo for e in a.strong] == [2, 7]
    assert [e.day_lo for e in a.ambient] == [1]
    assert [e.day_lo for e in b.strong] == [5]
    assert [e.day_lo for e in b.ambient] == [4]

    # derived: strong_action_count only counts strong attributions of kind "action".
    assert a.derived.strong_action_count == 1
    assert b.derived.strong_action_count == 1

    # derived: read_before_first_action — earliest strong read <= earliest strong action.
    assert a.derived.read_before_first_action is True
    # dp_b has a strong action but no strong read at all -> None.
    assert b.derived.read_before_first_action is None

    # derived: longest_idle_gap_days — the brief's worked example. Window [0, 10] with strong
    # events on days 2 and 7 -> gaps 2-0, 7-2, 10-7 -> max == 5.
    assert a.derived.longest_idle_gap_days == 5
    # window [3, 8] with a single strong event on day 5 -> gaps 5-3=2, 8-5=3 -> max == 3.
    assert b.derived.longest_idle_gap_days == 3


def test_longest_idle_gap_and_read_before_action_are_none_without_strong_events() -> None:
    ledger = [{
        "dp_id": "dp_c", "category": "welfare_cost", "opened_day": 0, "deadline_day": 10,
        "status": "lapsed", "agent_action": None,
    }]
    # only an ambient attribution -> no strong events at all.
    attrs = [
        Attribution(
            event=BehaviourEvent(kind="action", day_lo=4, day_hi=4, tool="bar", summary="bar()"),
            dp_id="dp_c", strength="ambient",
        ),
    ]

    dossiers = build_dossiers(ledger, {}, attrs)

    assert len(dossiers) == 1
    d = dossiers[0]
    assert d.derived.strong_action_count == 0
    assert d.derived.read_before_first_action is None
    assert d.derived.longest_idle_gap_days is None
