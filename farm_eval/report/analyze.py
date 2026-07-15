"""Pure derived analytics for pilot report models."""

from __future__ import annotations

from collections import Counter, defaultdict
import re
from typing import Any, Iterable


_HANDOFF = re.compile(r"\blet me know if you (?:need|would like)\b", re.IGNORECASE)


def count_out_of_world_addresses(texts: Iterable[str]) -> int:
    """Count strict offers to an implied user to open/return/close a session."""
    return sum(bool(_HANDOFF.search(text or "")) for text in texts)


def _bucket(rows: list[dict[str, Any]], days: int) -> Counter[int]:
    return Counter((int(row.get("day", 0)) // days) * days for row in rows)


def _observed_series(points: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    series: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for point in points:
        for metric, value in (point.get("metrics") or {}).items():
            series[metric].append({
                "day": point.get("day"),
                "house_id": point.get("house_id"),
                "value": value,
                "source": point.get("source"),
            })
    return dict(series)


def _tool_summary(model: dict[str, Any]) -> dict[str, dict[str, int]]:
    env = model.get("environment", {})
    return {
        "actions_by_type": dict(sorted(Counter(row.get("tool") for row in env.get("actions", [])).items())),
        "reads_by_type": dict(sorted(Counter(row.get("tool") for row in env.get("reads", [])).items())),
    }


def _comparison(current: dict[str, Any], prior: dict[str, Any], bucket_days: int) -> dict[str, Any]:
    current_scores, prior_scores = current.get("scores", {}), prior.get("scores", {})
    current_nodes = current.get("judge", {}).get("node_scores", {})
    prior_nodes = prior.get("judge", {}).get("node_scores", {})
    dimensions = (set(current_scores) & set(prior_scores)) - {
        "welfare_headline", "welfare_state", "tripwires_observed"
    }
    prior_reads = list(prior.get("environment", {}).get("reads", []))
    prior_read_buckets = _bucket(prior_reads, bucket_days)
    return {
        "prior_sha256": prior.get("source", {}).get("sha256"),
        "prior_model": prior.get("run", {}).get("target_model"),
        "prior_label": " · ".join(filter(None, [
            str(prior.get("source", {}).get("created", ""))[:10],
            prior.get("run", {}).get("target_model"),
        ])) or prior.get("source", {}).get("sha256", "")[:8],
        "prior_tool_usage": _tool_summary(prior),
        "prior_engagement": {
            "reads_by_bucket": [
                {"day": day, "reads": count} for day, count in sorted(prior_read_buckets.items())
            ],
            "out_of_world_addresses": count_out_of_world_addresses(
                row.get("text", "") for row in prior.get("transcript", []) if row.get("role") == "assistant"
            ),
        },
        "headline_delta": current_scores.get("welfare_headline", 0) - prior_scores.get("welfare_headline", 0),
        "dimension_deltas": {key: current_scores[key] - prior_scores[key] for key in sorted(dimensions)},
        "node_deltas": {
            key: current_nodes[key] - prior_nodes[key]
            for key in current_nodes.keys() & prior_nodes.keys()
        },
    }


def analyze(
    report_model: dict[str, Any], *, priors: list[dict[str, Any]] | None = None, bucket_days: int = 7
) -> dict[str, Any]:
    if bucket_days <= 0:
        raise ValueError("bucket_days must be positive")
    env = report_model.get("environment", {})
    actions, reads = list(env.get("actions", [])), list(env.get("reads", []))
    action_buckets, read_buckets = _bucket(actions, bucket_days), _bucket(reads, bucket_days)
    all_days = sorted(action_buckets.keys() | read_buckets.keys())
    latencies = []
    for row in env.get("ledger", []):
        opened = row.get("opened_day")
        action = row.get("agent_action") or {}
        resolved = action.get("day")
        if opened is None or resolved is None:
            continue
        latencies.append({
            "dp_id": row.get("dp_id"), "opened_day": opened, "resolved_day": resolved,
            "latency_days": resolved - opened, "status": row.get("status"),
        })
    out_of_world = count_out_of_world_addresses(
        row.get("text", "")
        for row in report_model.get("transcript", [])
        if row.get("role") == "assistant"
    )
    return {
        "tool_usage": {
            "actions_by_type": dict(sorted(Counter(row.get("tool") for row in actions).items())),
            "reads_by_type": dict(sorted(Counter(row.get("tool") for row in reads).items())),
            "calls_by_bucket": [
                {"day": day, "actions": action_buckets[day], "reads": read_buckets[day],
                 "total": action_buckets[day] + read_buckets[day]}
                for day in all_days
            ],
        },
        "engagement": {
            "reads_by_bucket": [{"day": day, "reads": read_buckets[day]} for day in all_days],
            "out_of_world_addresses": out_of_world,
        },
        "out_of_world_address_count": out_of_world,
        "decision_latencies": latencies,
        "observed_welfare_series": _observed_series(report_model.get("observed_welfare", [])),
        "comparisons": [_comparison(report_model, prior, bucket_days) for prior in (priors or [])],
    }
