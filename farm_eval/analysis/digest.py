"""Day-segmented transcript digest (design §3.4): groups transcript rows into one `DigestDay`
per in-world day, so a whole 500+-day episode can be read day by day instead of message by
message -- by a human, by a Claude session asked to walk the whole transcript, and (later) by
the LLM reader's sweep mode as its chunking unit.

Nothing here is farm-specific: rows, ledger entries and snapshots all come from the run's own
recorded artifacts.
"""

from __future__ import annotations

from typing import Any

from farm_eval.analysis.model import DigestDay, DigestEntry
from farm_eval.spectator.events import StateSnapshot

# First N chars of a tool result kept in the digest -- full bodies live in the transcript
# itself; the digest is a reading surface, not a second copy of the log.
_TOOL_TEXT_CHARS = 200


def _tool_call_summary(tool_calls: list[dict[str, Any]]) -> str:
    names = ", ".join(str(call.get("function", "")) for call in tool_calls)
    return f"[tool_call {names}]"


def _entry(row: dict[str, Any]) -> DigestEntry | None:
    """One row -> one digest entry, or `None` for rows that carry no digest content:
    system rows, and blank assistant turns with no tool call either (those are Task 8's
    off-node business, not digest content). An assistant row with tool calls but no text
    still gets an entry naming the calls, so a pure tool-call turn isn't silently dropped."""
    role = row.get("role")
    if role == "assistant":
        text = row.get("text") or ""
        tool_calls = row.get("tool_calls") or []
        if not text and not tool_calls:
            return None
        if not text:
            text = _tool_call_summary(tool_calls)
        return DigestEntry(kind="assistant", msg_id=row.get("id"), text=text)
    if role == "tool":
        text = (row.get("text") or "")[:_TOOL_TEXT_CHARS]
        return DigestEntry(kind="tool", msg_id=row.get("id"), text=text)
    if role == "user":
        return DigestEntry(kind="user", msg_id=row.get("id"), text=row.get("text") or "")
    return None


def _entries(rows: list[dict[str, Any]]) -> list[DigestEntry]:
    return [entry for row in rows if (entry := _entry(row)) is not None]


def _windows_open(ledger: list[dict[str, Any]], day: int) -> list[str]:
    return sorted(
        entry["dp_id"]
        for entry in ledger
        if entry.get("opened_day") is not None
        and entry.get("deadline_day") is not None
        and entry["opened_day"] <= day <= entry["deadline_day"]
    )


def _flatten_numeric(totals: dict[str, Any]) -> dict[str, float]:
    """Numeric keys of `totals`, with one level of nested dicts flattened to dotted keys
    (e.g. `totals["harm"]["excess_mortality"]` -> `"harm.excess_mortality"`). `bool` is
    excluded even though it's a `numbers` subtype of `int` -- a flag toggling isn't a
    quantity to diff."""
    flat: dict[str, float] = {}
    for key, value in totals.items():
        if isinstance(value, bool):
            continue
        if isinstance(value, (int, float)):
            flat[key] = value
        elif isinstance(value, dict):
            for subkey, subvalue in value.items():
                if isinstance(subvalue, bool):
                    continue
                if isinstance(subvalue, (int, float)):
                    flat[f"{key}.{subkey}"] = subvalue
    return flat


def _state_deltas(
    snapshots_by_day: dict[int, StateSnapshot], ordered_days: list[int], day: int
) -> dict[str, float]:
    """Per numeric key, this day's snapshot value minus the PREVIOUS snapshot's (chronological
    order among the snapshots actually present, not necessarily `day - 1`). `{}` when this day
    has no snapshot, or when it's the earliest one on record (no previous to diff against)."""
    if day not in snapshots_by_day:
        return {}
    index = ordered_days.index(day)
    if index == 0:
        return {}
    curr = _flatten_numeric(snapshots_by_day[day].totals)
    prev = _flatten_numeric(snapshots_by_day[ordered_days[index - 1]].totals)
    return {key: curr[key] - prev.get(key, 0) for key in curr}


def build_digest(
    transcript: list[dict[str, Any]],
    day_map: dict[str, int] | None,
    ledger: list[dict[str, Any]],
    snapshots: list[StateSnapshot],
) -> list[DigestDay]:
    """One `DigestDay` per day that has transcript rows, sorted ascending; entries within a
    day keep transcript order. `day_map is None` degrades to a single `day=-1` bucket holding
    every row in order, with `windows_open`/`state_deltas` honestly disabled -- a transcript
    without a reconciled clock cannot support day-dependent output (spec §2.2)."""
    if day_map is None:
        return [DigestDay(day=-1, windows_open=[], state_deltas={}, entries=_entries(transcript))]

    rows_by_day: dict[int, list[dict[str, Any]]] = {}
    for row in transcript:
        day = day_map.get(row.get("id"))
        if day is None:
            continue
        rows_by_day.setdefault(day, []).append(row)

    snapshots_by_day = {s.day: s for s in snapshots if s.day is not None}
    ordered_snapshot_days = sorted(snapshots_by_day)

    return [
        DigestDay(
            day=day,
            windows_open=_windows_open(ledger, day),
            state_deltas=_state_deltas(snapshots_by_day, ordered_snapshot_days, day),
            entries=_entries(rows_by_day[day]),
        )
        for day in sorted(rows_by_day)
    ]
