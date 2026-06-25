"""Sparse in-world time advancement: jump to the next scheduled beat, skipping quiet days."""

from __future__ import annotations

from datetime import date, timedelta


def date_for_day(start_date: str, day_index: int) -> str:
    base = date.fromisoformat(start_date)
    return (base + timedelta(days=day_index)).isoformat()


def next_beat(current_day: int, event_days: list[int], end_day: int) -> tuple[int, int]:
    future = [d for d in event_days if d > current_day and d <= end_day]
    new_day = min(future) if future else end_day
    return new_day, new_day - current_day
