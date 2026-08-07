"""Per-node behaviour dossiers (design §3.3): one row per ledger entry, joining the node's
judge score with its strong/ambient attributed events and a handful of derived timing facts."""

from __future__ import annotations

from farm_eval.analysis.model import Attribution, DossierDerived, NodeDossier


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


def build_dossiers(
    ledger: list[dict], node_scores: dict[str, float], attributions: list[Attribution]
) -> list[NodeDossier]:
    """One `NodeDossier` per ledger row, sorted by `opened_day` then `dp_id`."""
    dossiers = []
    for entry in sorted(ledger, key=lambda e: (e.get("opened_day", 0), e.get("dp_id", ""))):
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
    return dossiers
