"""Sparse in-world time advancement: jump to the next scheduled beat, skipping quiet days.

Also the within-beat working-hours clock: each wake-up starts at shift-open and every tool call
costs a small amount of in-world time. The per-call cost is jittered so a fixed policy never sees
a constant per-tool duration (an eval-awareness tell), yet it is fully deterministic — a pure
seeded function of (run seed, day, call index, tool), so a run replays byte-identically. No
wall-clock, no live randomness (project determinism rule).
"""

from __future__ import annotations

import hashlib
from datetime import date, timedelta


def date_for_day(start_date: str, day_index: int) -> str:
    base = date.fromisoformat(start_date)
    return (base + timedelta(days=day_index)).isoformat()


def next_beat(current_day: int, event_days: list[int], end_day: int) -> tuple[int, int]:
    future = [d for d in event_days if d > current_day and d <= end_day]
    new_day = min(future) if future else end_day
    return new_day, new_day - current_day


def _unit_interval(seed: int, day_index: int, call_index: int, tool: str) -> float:
    """A deterministic pseudo-random value in [0, 1) from the timing key. Uses hashlib (NOT the
    salted built-in hash()) so the value is stable across processes and replays."""
    key = f"{seed}|{day_index}|{call_index}|{tool}".encode()
    digest = hashlib.sha256(key).digest()[:8]
    return int.from_bytes(digest, "big") / 2**64


def tool_duration_minutes(
    seed: int, day_index: int, call_index: int, tool: str, base_minutes: float, jitter_frac: float
) -> float:
    """In-world minutes a single tool call costs: `base_minutes` scaled by a seeded jitter factor
    in [1 - jitter_frac, 1 + jitter_frac). A zero base stays zero (free tools). Deterministic:
    same inputs -> same value; distinct (call_index / seed / day / tool) reshuffle it, so the
    per-tool duration is never a constant a model could clock."""
    if base_minutes <= 0.0:
        return 0.0
    unit = _unit_interval(seed, day_index, call_index, tool)
    factor = 1.0 + jitter_frac * (2.0 * unit - 1.0)
    return base_minutes * factor


def format_time_of_day(minutes_into_day: float, shift_start_min: float) -> str:
    """Wall-clock time-of-day "HH:MM" for `minutes_into_day` minutes past shift-open. Wraps at
    24 h (a runaway day never prints an hour > 23)."""
    total = int(round(shift_start_min + minutes_into_day))
    return f"{(total // 60) % 24:02d}:{total % 60:02d}"
