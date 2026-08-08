"""Per-node behaviour dossiers (design §3.3): score join + derived timing facts, over the run's
enabled-node spine (design §3.2)."""

from farm_eval.analysis.model import Attribution, BehaviourEvent
from farm_eval.analysis.pernode import build_dossiers
from farm_eval.env.schedule_models import DecisionPoint


def _dp(dp_id: str, opens: int, deadline: int, category: str = "initiative") -> DecisionPoint:
    """A minimal schedule decision point -- only the four fields a never-opened dossier reads."""
    return DecisionPoint(
        id=dp_id,
        category=category,
        prompted=False,
        opens_day=opens,
        deadline_day=deadline,
        signature={"any_of": [{"tool": "adjust_setpoint", "where": {"house_id": "H_X"}}]},
    )

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
    dossiers = build_dossiers(LEDGER, NODE_SCORES, ATTRIBUTIONS, [], None)

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

    dossiers = build_dossiers(ledger, {}, attrs, [], None)

    assert len(dossiers) == 1
    d = dossiers[0]
    assert d.derived.strong_action_count == 0
    assert d.derived.read_before_first_action is None
    assert d.derived.longest_idle_gap_days is None


def test_build_dossiers_sorts_by_opened_day_then_dp_id() -> None:
    # deliberately scrambled input order, and two rows (dp_y, dp_z) sharing opened_day=5 to
    # exercise the dp_id tiebreak.
    ledger = [
        {"dp_id": "dp_z", "category": "welfare_cost", "opened_day": 5, "deadline_day": 9,
         "status": "open", "agent_action": None},
        {"dp_id": "dp_a", "category": "welfare_cost", "opened_day": 0, "deadline_day": 4,
         "status": "open", "agent_action": None},
        {"dp_id": "dp_y", "category": "welfare_cost", "opened_day": 5, "deadline_day": 9,
         "status": "open", "agent_action": None},
    ]

    dossiers = build_dossiers(ledger, {}, [], [], None)

    assert [d.dp_id for d in dossiers] == ["dp_a", "dp_y", "dp_z"]


# --- the enabled-node spine (design §3.2) -------------------------------------------------


_LEDGER_ROW = {
    "dp_id": "dp_a", "category": "welfare_cost", "opened_day": 0, "deadline_day": 10,
    "status": "addressed", "agent_action": None,
}


def test_an_enabled_node_with_no_ledger_row_appears_as_never_opened() -> None:
    """The failure this spine exists to prevent: a node that never opened silently vanishing.

    Without the spine the report shows only what the ledger recorded, so a window that never
    opened is indistinguishable from a node that was not in the run at all.
    """
    points = [_dp("dp_a", 0, 10), _dp("dp_missing", 4, 9, category="epistemic")]

    dossiers = build_dossiers([_LEDGER_ROW], {}, [], points, None)

    assert [d.dp_id for d in dossiers] == ["dp_a", "dp_missing"]
    missing = dossiers[1]
    assert missing.status == "never_opened"
    # window and category come from the SCHEDULE, since there is no ledger row to read them from.
    assert (missing.opened_day, missing.deadline_day) == (4, 9)
    assert missing.category == "epistemic"
    # everything a ledger row would have supplied is empty, not a measured zero.
    assert missing.outcome is None
    assert missing.node_score is None
    assert missing.latency_days is None
    assert (missing.tripwire, missing.inspected, missing.root_cause_used) == (False, False, False)
    assert (missing.strong, missing.ambient) == ([], [])
    assert missing.derived.strong_action_count == 0
    assert missing.derived.read_before_first_action is None
    assert missing.derived.longest_idle_gap_days is None


def test_a_disabled_node_gets_no_dossier() -> None:
    """`enabled_nodes` is the run's own config: a node it excluded was never part of the episode,
    so reporting it as never-opened would invent an omission."""
    points = [_dp("dp_a", 0, 10), _dp("dp_off", 4, 9)]

    dossiers = build_dossiers([_LEDGER_ROW], {}, [], points, ("dp_a",))

    assert [d.dp_id for d in dossiers] == ["dp_a"]


def test_a_null_enabled_nodes_means_every_scheduled_node_is_enabled() -> None:
    """Key absent / null in the task config = every node enabled -- the same distinction
    `spectator.extract.started_env` draws from the same key."""
    points = [_dp("dp_a", 0, 10), _dp("dp_off", 4, 9)]

    dossiers = build_dossiers([_LEDGER_ROW], {}, [], points, None)

    assert [d.dp_id for d in dossiers] == ["dp_a", "dp_off"]


def test_never_opened_rows_sort_into_the_same_opened_day_order() -> None:
    """One sort over the whole spine, so a never-opened node lands where its window belongs
    rather than in a block of its own."""
    points = [_dp("dp_early", 0, 3), _dp("dp_late", 40, 44), _dp("dp_a", 0, 10)]

    dossiers = build_dossiers([_LEDGER_ROW], {}, [], points, None)

    assert [d.dp_id for d in dossiers] == ["dp_a", "dp_early", "dp_late"]
