"""Per-node behaviour dossiers (design §3.3): one row per ENABLED node, joining the node's judge
score with its strong/ambient attributed events and a handful of derived timing facts.

The row set is the run's **enabled-node spine**, not the ledger (design §3.2). A node whose window
never opened leaves no ledger entry, so a ledger-driven list would let it vanish from the report
without a word — the reader could not tell "the agent had nothing to answer here" from "this node
was never in the run". Every enabled node therefore gets a dossier; the ones with no ledger row get
`status="never_opened"` and nothing else, which is exactly what is known about them.
"""

from __future__ import annotations

from farm_eval.analysis.model import Attribution, DossierDerived, NodeDossier
from farm_eval.env.schedule_models import DecisionPoint


def _derived(opened_day: int, deadline_day: int, attrs: list[Attribution]) -> DossierDerived:
    strong = [a for a in attrs if a.strength == "strong"]
    strong_action_count = sum(1 for a in strong if a.event.kind == "action")

    read_days = [a.event.day_lo for a in strong if a.event.kind == "read" and a.event.day_lo is not None]
    action_days = [a.event.day_lo for a in strong if a.event.kind == "action" and a.event.day_lo is not None]
    read_before_first_action = (
        min(read_days) <= min(action_days) if read_days and action_days else None
    )

    strong_days = [a.event.day_lo for a in strong if a.event.day_lo is not None]
    if not strong_days:
        longest_idle_gap_days = None
    else:
        points = sorted({opened_day, deadline_day, *strong_days})
        longest_idle_gap_days = max(hi - lo for lo, hi in zip(points, points[1:]))

    return DossierDerived(
        strong_action_count=strong_action_count,
        read_before_first_action=read_before_first_action,
        longest_idle_gap_days=longest_idle_gap_days,
    )


def _never_opened(dp: DecisionPoint) -> NodeDossier:
    """A dossier for an enabled node whose window never opened in this run.

    Everything but the schedule's own facts is empty, because nothing else happened: no ledger
    row, no attributions, no judge score. `opened_day`/`deadline_day` are the SCHEDULE's authored
    days -- the window that was supposed to open -- which is what a reader needs to see where in
    the episode the gap sits.
    """
    return NodeDossier(
        dp_id=dp.id,
        category=dp.category,
        opened_day=dp.opens_day,
        deadline_day=dp.deadline_day,
        status="never_opened",
        derived=DossierDerived(
            strong_action_count=0,
            read_before_first_action=None,
            longest_idle_gap_days=None,
        ),
    )


def build_dossiers(
    ledger: list[dict],
    node_scores: dict[str, float],
    attributions: list[Attribution],
    decision_points: list[DecisionPoint],
    enabled_nodes: tuple[str, ...] | None,
) -> list[NodeDossier]:
    """One `NodeDossier` per enabled node, sorted by `opened_day` then `dp_id`.

    `enabled_nodes` is the run's recorded task-config value, and `None` means every node in the
    schedule is enabled -- the same distinction `spectator.extract.started_env` draws from the same
    config key. A node the run DISABLED gets no dossier: it was not part of this episode, so
    reporting it as never-opened would invent an omission.
    """
    ledger_ids = {entry.get("dp_id") for entry in ledger}
    enabled = set(enabled_nodes) if enabled_nodes is not None else None
    dossiers = [
        _never_opened(dp)
        for dp in decision_points
        if dp.id not in ledger_ids and (enabled is None or dp.id in enabled)
    ]
    for entry in ledger:
        dp_id = entry.get("dp_id")
        opened_day, deadline_day = entry.get("opened_day"), entry.get("deadline_day")
        agent_action = entry.get("agent_action")
        latency_days = agent_action.get("day") - opened_day if agent_action else None
        attrs = [a for a in attributions if a.dp_id == dp_id]
        dossiers.append(
            NodeDossier(
                dp_id=dp_id,
                category=entry.get("category", ""),
                opened_day=opened_day,
                deadline_day=deadline_day,
                status=entry.get("status", ""),
                outcome=entry.get("outcome"),
                tripwire=entry.get("tripwire", False),
                inspected=entry.get("inspected", False),
                root_cause_used=entry.get("root_cause_used", False),
                latency_days=latency_days,
                node_score=node_scores.get(dp_id),
                strong=[a.event for a in attrs if a.strength == "strong"],
                ambient=[a.event for a in attrs if a.strength == "ambient"],
                derived=_derived(opened_day, deadline_day, attrs),
            )
        )
    dossiers.sort(key=lambda d: (d.opened_day, d.dp_id))
    return dossiers
