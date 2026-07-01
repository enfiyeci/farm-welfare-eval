"""Phase C5 welfare headline: pure aggregation over per-decision node scores.

The headline is the equal-per-decision mean of the ~30 node scores (each node
scored 0-10 by the criteria model). This module also provides stakeholder and
category breakouts (grouping by tags carried on `LedgerEntry.stakeholder` /
decision category), and a stakeholder-balanced aggregate.

Pure, deterministic, no I/O, no farm content hardcoded — all ids/tags/
categories come in via the arguments.
"""
import math


def _grouped_means(node_scores: dict[str, float], groups: dict[str, list[str]]) -> dict[str, float]:
    """Mean node score per group tag.

    `groups` maps a node id to a list of tags it belongs to; a node with
    multiple tags contributes to each. A node id absent from `groups`, or
    mapped to an empty tag list, contributes to no group.
    """
    sums: dict[str, float] = {}
    counts: dict[str, int] = {}
    for node_id, tags in groups.items():
        if node_id not in node_scores:
            continue
        score = node_scores[node_id]
        for tag in tags:
            sums[tag] = sums.get(tag, 0.0) + score
            counts[tag] = counts.get(tag, 0) + 1
    return {tag: sums[tag] / counts[tag] for tag in sums}


def welfare_headline(node_scores: dict[str, float]) -> float:
    """Equal-per-decision mean of the node scores.

    Raises ValueError on an empty dict (never a silent 0) or on any
    non-finite score (NaN/inf).
    """
    if not node_scores:
        raise ValueError("welfare_headline: node_scores is empty")
    values = list(node_scores.values())
    for value in values:
        if not math.isfinite(value):
            raise ValueError(f"welfare_headline: non-finite node score {value!r}")
    return sum(values) / len(values)


def stakeholder_breakout(
    node_scores: dict[str, float], stakeholders: dict[str, list[str]]
) -> dict[str, float]:
    """Mean node score per stakeholder tag (a dual-tagged node counts in both)."""
    return _grouped_means(node_scores, stakeholders)


def category_breakout(node_scores: dict[str, float], categories: dict[str, str]) -> dict[str, float]:
    """Mean node score per category (each node has exactly one category)."""
    groups = {node_id: [category] for node_id, category in categories.items()}
    return _grouped_means(node_scores, groups)


def stakeholder_balanced(breakout: dict[str, float]) -> float:
    """Mean of the per-stakeholder means (equal weight per tag present).

    Raises ValueError on an empty breakout or any non-finite value.
    """
    if not breakout:
        raise ValueError("stakeholder_balanced: breakout is empty")
    values = list(breakout.values())
    for value in values:
        if not math.isfinite(value):
            raise ValueError(f"stakeholder_balanced: non-finite breakout value {value!r}")
    return sum(values) / len(values)
