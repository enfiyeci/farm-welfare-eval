"""Flatten an Inspect eval log into the JSON-safe pilot report model."""

from __future__ import annotations

import hashlib
import json
import math
import re
import statistics
from pathlib import Path
from typing import Any

from inspect_ai.log import read_eval_log


def _json(value: Any) -> Any:
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")
    return value


def _message_text(message: Any) -> str:
    content = getattr(message, "content", "")
    if isinstance(content, str):
        return content
    parts: list[str] = []
    for part in content or []:
        if isinstance(part, str):
            parts.append(part)
        elif getattr(part, "text", None):
            parts.append(part.text)
        elif getattr(part, "reasoning", None) and not getattr(part, "redacted", False):
            parts.append(part.reasoning)
    return "\n".join(parts)


def _transcript(messages: list[Any]) -> list[dict[str, Any]]:
    rows = []
    for index, message in enumerate(messages):
        row: dict[str, Any] = {
            "id": f"msg_{index}",
            "role": getattr(message, "role", "unknown"),
            "text": _message_text(message),
        }
        calls = getattr(message, "tool_calls", None)
        if calls:
            row["tool_calls"] = [
                {"id": call.id, "function": call.function, "arguments": _json(call.arguments)}
                for call in calls
            ]
        tool_call_id = getattr(message, "tool_call_id", None)
        if tool_call_id:
            row["tool_call_id"] = tool_call_id
        rows.append(row)
    return rows


def _numeric_metrics(payload: dict[str, Any], source: str) -> dict[str, float]:
    metrics: dict[str, float] = {}
    if source == "sensor":
        metric, value = payload.get("metric"), payload.get("value")
        if isinstance(metric, str) and isinstance(value, (int, float)) and not isinstance(value, bool):
            metrics[metric] = float(value)
        return metrics

    aliases = {
        "birds_alive": ("mortality", "birds_alive"),
        "hen_day_pct": ("production", "hen_day_pct"),
        "feed_g_per_bird": ("intake", "feed_g_per_bird"),
        "water_ml_per_bird": ("intake", "water_ml_per_bird"),
        "footpad_affected_pct": ("welfare_obs", "footpad_affected_pct"),
        "feather_damage_pct": ("welfare_obs", "feather_damage_pct"),
        "panting_fraction": ("welfare_obs", "panting_fraction"),
        "red_mite_signs": ("welfare_obs", "red_mite_signs"),
    }
    for name, (group, field) in aliases.items():
        value = (payload.get(group) or {}).get(field)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            metrics[name] = float(value)
    return metrics


def _observed_welfare(messages: list[Any], reads: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Scrape only successful model-visible read tool results, never terminal state."""
    relevant = [row for row in reads if row.get("tool") in {"read_flock_report", "read_sensor"}]
    cursor = 0
    points: list[dict[str, Any]] = []
    for message in messages:
        if getattr(message, "role", None) != "tool":
            continue
        function = getattr(message, "function", None)
        call_id = str(getattr(message, "tool_call_id", "") or "")
        tool = function if function in {"read_flock_report", "read_sensor"} else next(
            (name for name in ("read_flock_report", "read_sensor") if call_id.startswith(name)), None
        )
        if tool is None:
            continue
        while cursor < len(relevant) and relevant[cursor].get("tool") != tool:
            cursor += 1
        if cursor >= len(relevant):
            break
        read = relevant[cursor]
        cursor += 1
        try:
            payload = json.loads(_message_text(message))
        except (TypeError, json.JSONDecodeError):
            continue
        if not isinstance(payload, dict) or payload.get("error"):
            continue
        source = "flock_report" if tool == "read_flock_report" else "sensor"
        metrics = _numeric_metrics(payload, source)
        if not metrics:
            continue
        points.append({
            "day": int(read["day"]),
            "house_id": payload.get("house_id") or (read.get("params") or {}).get("house_id"),
            "source": source,
            "metrics": metrics,
        })
    return points


def _usage_map(usage: dict[str, Any] | None) -> dict[str, Any]:
    return {name: _json(value) for name, value in (usage or {}).items()}


def _criterion_evidence(sample: Any, criterion_notes: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Recover recorded node-criterion rubrics and citations from grader events."""
    attachments = sample.attachments or {}

    def resolve(text: str | None) -> str:
        value = text or ""
        if value.startswith("attachment://"):
            return str(attachments.get(value.removeprefix("attachment://"), value))
        return value

    raw_samples: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for event in sample.events or []:
        inputs = getattr(event, "input", None) or []
        output = getattr(event, "output", None)
        if not inputs or output is None:
            continue
        prompt = resolve(getattr(inputs[0], "text", ""))
        if "grading ONE criterion" not in prompt:
            continue
        dp_match = re.search(r"faced:\s*(\S+?)\.", prompt)
        criterion_match = re.search(r"Criterion:\s*'([^']+)'", prompt)
        rubric_match = re.search(r"=== RUBRIC for this criterion ===\s*(.*?)\s*=== TRANSCRIPT", prompt, re.DOTALL)
        if not dp_match or not criterion_match:
            continue
        dp_id, criterion = dp_match.group(1), criterion_match.group(1)
        record: dict[str, Any] = {
            "rubric": rubric_match.group(1).strip() if rubric_match else "",
            "score": None,
            "quote": "",
            "message_id": "",
        }
        completion = resolve(getattr(output, "completion", ""))
        start = completion.find("{")
        if start >= 0:
            try:
                graded, _ = json.JSONDecoder().raw_decode(completion[start:])
            except (TypeError, json.JSONDecodeError):
                graded = None
            if isinstance(graded, dict):
                record.update({
                    "score": graded.get("score"),
                    "quote": str(graded.get("quote", "")),
                    "message_id": str(graded.get("message_id", "")),
                })
        raw_samples.setdefault((dp_id, criterion), []).append(record)
    by_node: dict[str, list[dict[str, Any]]] = {}
    for (dp_id, criterion), samples in raw_samples.items():
        scored_samples = []
        for sample_index, record in enumerate(samples):
            note = next((
                item for item in criterion_notes
                if item.get("dp_id") == dp_id and item.get("criterion") == criterion
                and item.get("sample_index", 0) == sample_index
            ), None)
            raw_score = record.get("score")
            numeric = isinstance(raw_score, (int, float)) and not isinstance(raw_score, bool) and math.isfinite(raw_score)
            accepted = note is None and numeric
            scored_samples.append({
                **record,
                "score": float(raw_score) if numeric else None,
                "sample_index": sample_index,
                "accepted": accepted,
                "scored": float(raw_score) if accepted else 0.0,
                "discard_reason": str(note.get("reason", "")) if note else "",
            })
        by_node.setdefault(dp_id, []).append({
            "criterion": criterion,
            "rubric": samples[0].get("rubric", "") if samples else "",
            "score": statistics.median(item["scored"] for item in scored_samples),
            "samples": scored_samples,
        })
    return by_node


def extract(path: str | Path) -> dict[str, Any]:
    """Read one `.eval` and return a plain, JSON-serializable report-model dict."""
    source_path = Path(path).expanduser().resolve()
    log = read_eval_log(str(source_path))
    if not log.samples:
        raise ValueError(f"eval log contains no samples: {source_path}")
    sample = log.samples[0]
    state = dict(sample.store.get("EpisodeStore:env_state") or {})
    score = sample.scores.get("welfare_judge")
    if score is None:
        raise ValueError("eval sample has no welfare_judge score")
    scores = dict(score.value) if isinstance(score.value, dict) else {"welfare_headline": score.value}
    metadata = dict(score.metadata or {})
    messages = list(sample.messages or [])
    reads = list(state.get("reads") or [])
    roles = getattr(log.eval, "model_roles", None) or {}
    grader = roles.get("grader")
    grader_model = getattr(grader, "model", None) or ""
    transcript = _transcript(messages)
    ledger = list(state.get("ledger") or [])
    node_scores = dict(metadata.get("node_scores") or {})
    node_set = list(node_scores) or [row.get("dp_id") for row in ledger if row.get("dp_id")]
    welfare = state.get("welfare") or {}
    revision = _json(getattr(log.eval, "revision", None)) or {}
    eval_data = log.eval.model_dump(mode="json")

    model: dict[str, Any] = {
        "schema_version": 1,
        "source": {
            "path": str(source_path),
            "sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
            "status": log.status,
            "created": log.eval.created,
        },
        "run": {
            "target_model": log.eval.model,
            "grader_model": grader_model,
            "task": log.eval.task,
            "branch": revision.get("branch"),
            "commit": revision.get("commit"),
            "dirty": revision.get("dirty"),
            "started_at": log.stats.started_at,
            "completed_at": log.stats.completed_at,
            "runtime_seconds": sample.total_time,
            "usage": _usage_map(sample.role_usage),
            "day_index": state.get("day_index"),
            "forced_advances": metadata.get("forced_advances", 0),
            "sample_id": sample.id,
            "epoch": sample.epoch,
            "node_set": node_set,
            "task_args": eval_data.get("task_args") or {},
            "scorers": eval_data.get("scorers") or [],
            "eval_config": eval_data.get("config") or {},
        },
        "scores": scores,
        "judge": {
            "explanation": score.explanation,
            "tripwires": metadata.get("tripwires_observed", []),
            "node_scores": node_scores,
            "node_evidence": _criterion_evidence(sample, list(metadata.get("criterion_notes", []))),
            "node_variance": metadata.get("node_variance", {}),
            "highlights": metadata.get("highlights", []),
            "dimension_samples": metadata.get("samples", []),
            "dimension_notes": metadata.get("dimension_notes", []),
            "criterion_notes": metadata.get("criterion_notes", []),
            "discarded_evidence": metadata.get("discarded_evidence", {}),
            "cue_localization": metadata.get("cue_localization", []),
            "axis_span_counts": metadata.get("axis_span_counts", {}),
            "stakeholder_breakout": metadata.get("stakeholder_breakout", {}),
            "category_breakout": metadata.get("category_breakout", {}),
            "stakeholder_balanced": metadata.get("stakeholder_balanced"),
            "recognition": metadata.get("recognition", {}),
            "welfare_state_channels": metadata.get("welfare_state_channels", {}),
        },
        "environment": {
            "actions": list(state.get("actions") or []),
            "reads": reads,
            "event_log": list(state.get("event_log") or []),
            "outbound": list(state.get("outbound") or []),
            "mailbox": list(state.get("mailbox") or []),
            "ledger": ledger,
            "welfare_endpoint_harm": dict(welfare.get("harm") or {}),
            "final_houses": dict(welfare.get("houses") or {}),
            "financial_endpoint": dict(state.get("financial") or {}),
        },
        "transcript": transcript,
        "observed_welfare": _observed_welfare(messages, reads),
    }
    return json.loads(json.dumps(model, allow_nan=False))
