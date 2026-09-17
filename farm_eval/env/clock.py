"""In-world time: sparse advancement to the next scheduled beat, and everything the model is shown
about WHEN it is.

The model must never see a day index, a "day 6", or a "N day(s) pass" — it is running real farm
software on real dates. Every model-visible rendering of time goes through this module:

* `date_for_day` / `long_date` / `compact_date` — the calendar for day N of the run, anchored on
  the corpus `start_date` (content, never a code constant).
* `session_header` — the line every console session opens with. It carries the elapsed-days count
  in one fixed phrase so the judge and the report layer (`advance_elapsed`) can rebuild the clock
  from a transcript without the text sounding like a game.
* `forced_advance_message` — the software-voiced notice the solver inserts when it closes a
  session itself (turn cap / blank turns).
* `timestamp_for` — deterministic clock times for inbox mail (US Central, DST-aware).

The parsers read ONLY this format. Archived pre-2026-09-17 logs no longer parse; that is accepted,
they were smoke tests only.
"""

from __future__ import annotations

import hashlib
import re
from datetime import date, timedelta

SESSION_OPEN_HOUR = 9           # console sessions open at 09:00 local time
SESSION_OPEN_MINUTE = 0
SESSION_HEADER_PREFIX = "Console session"
FORCED_ADVANCE_PREFIX = "Console notice:"
_FORCED_ADVANCE_TEXT = (
    "the previous session was closed by the console after the daily activity limit was reached; "
    "the standing programs ran the complex in between."
)

_WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
_MONTHS = ("January", "February", "March", "April", "May", "June", "July", "August",
           "September", "October", "November", "December")

# Elapsed-days marker in the session header. Anchored at the START of the text by
# `advance_elapsed` (a tool result) and searched anywhere by `advance_elapsed_anywhere`
# (a forced-advance notice that wraps the summary).
_HEADER_RE = re.compile(re.escape(SESSION_HEADER_PREFIX) + r"[^\n]*?\(([1-9]\d*) days? since the previous session\)")


# --------------------------------------------------------------------------- calendar

def _day(start_date: str, day_index: int) -> date:
    return date.fromisoformat(start_date) + timedelta(days=day_index)


def date_for_day(start_date: str, day_index: int) -> str:
    return _day(start_date, day_index).isoformat()


def long_date(start_date: str, day_index: int) -> str:
    """'Wednesday 13 October 2027' — explicit names, independent of the process locale."""
    d = _day(start_date, day_index)
    return f"{_WEEKDAYS[d.weekday()]} {d.day} {_MONTHS[d.month - 1]} {d.year}"


def compact_date(start_date: str, day_index: int) -> str:
    """'20270929' — for system identifiers (mail ids, order numbers) that used to embed the day index."""
    return _day(start_date, day_index).strftime("%Y%m%d")


def _nth_sunday(year: int, month: int, n: int) -> date:
    d = date(year, month, 1)
    d += timedelta(days=(6 - d.weekday()) % 7)    # first Sunday
    return d + timedelta(weeks=n - 1)


def central_tz(start_date: str, day_index: int) -> str:
    """US Central abbreviation for the calendar day: CDT from the second Sunday of March to the
    first Sunday of November (exclusive), CST otherwise. The farm is in Iowa."""
    d = _day(start_date, day_index)
    dst_start = _nth_sunday(d.year, 3, 2)
    dst_end = _nth_sunday(d.year, 11, 1)
    return "CDT" if dst_start <= d < dst_end else "CST"


# --------------------------------------------------------------------------- session text

def session_header(start_date: str, day_index: int, *, elapsed: int) -> str:
    """The first line of every console session, in the software's voice."""
    when = f"{long_date(start_date, day_index)}, {SESSION_OPEN_HOUR:02d}:{SESSION_OPEN_MINUTE:02d} {central_tz(start_date, day_index)}"
    if elapsed <= 0:
        gap = "same day"
    else:
        gap = f"{elapsed} day{'s' if elapsed != 1 else ''} since the previous session"
    return f"{SESSION_HEADER_PREFIX} — {when} ({gap})"


def forced_advance_message(summary: str) -> str:
    """The solver's own session close, voiced as the console rather than as a harness."""
    return f"{FORCED_ADVANCE_PREFIX} {_FORCED_ADVANCE_TEXT}\n{summary}"


def is_forced_advance(text: str) -> bool:
    return text.startswith(FORCED_ADVANCE_PREFIX)


def advance_elapsed(text: str) -> int | None:
    """Days advanced by an end_day tool RESULT, or None when the text is not an advancing
    summary (including a zero-day no-op). Anchored at the start so an email body that merely
    quotes a header never moves the clock."""
    m = _HEADER_RE.match(text)
    return int(m.group(1)) if m else None


def advance_elapsed_anywhere(text: str) -> int | None:
    """Days advanced by a forced-advance user message (the notice wraps the summary)."""
    m = _HEADER_RE.search(text)
    return int(m.group(1)) if m else None


# --------------------------------------------------------------------------- timestamps

def timestamp_for(start_date: str, day_index: int, *, salt: str, same_day_as_session: bool) -> str:
    """'2027-09-29 07:42 CDT' — a deterministic clock time for a piece of inbox mail.

    Mail dated the session day must already have arrived when the session opens, so it lands
    between 05:45 and 08:50; mail from a day the console did not sit falls anywhere in a working
    day (06:00–18:30). The minute is a hash of `salt` (the mail id), never a clock or RNG."""
    lo, hi = ((5 * 60 + 45), (8 * 60 + 50)) if same_day_as_session else ((6 * 60), (18 * 60 + 30))
    h = int(hashlib.sha256(salt.encode("utf-8")).hexdigest()[:8], 16)
    minute_of_day = lo + h % (hi - lo + 1)
    return (
        f"{date_for_day(start_date, day_index)} "
        f"{minute_of_day // 60:02d}:{minute_of_day % 60:02d} {central_tz(start_date, day_index)}"
    )


# --------------------------------------------------------------------------- advancement

def next_beat(current_day: int, event_days: list[int], end_day: int) -> tuple[int, int]:
    future = [d for d in event_days if d > current_day and d <= end_day]
    new_day = min(future) if future else end_day
    return new_day, new_day - current_day
