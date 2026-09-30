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
* `session_open_minutes` — the console's own opening time for a calendar day. It varies day to
  day (never :00 or :30) so a session never looks like a cron job.
* `timestamp_for` — deterministic arrival times for inbox mail, to the second (US Central,
  DST-aware). Mail is scattered across the whole span since the previous session, so most of it
  arrived the evening before rather than in a tidy pre-session block — but only inside its
  SENDER's working hours (`send_windows_for`, data in `corpus/personas.yml`), and never before
  the day of the event it describes (`not_before_day`).

The parsers read ONLY this format. Archived pre-2026-09-17 logs no longer parse; that is accepted,
they were smoke tests only.
"""

from __future__ import annotations

import hashlib
import re
from datetime import date, timedelta

# The console's opening time wanders inside a late-morning band, and never lands on a :00 or a
# :30 — a farm manager sits down when the barn work lets him, not when a scheduler says so.
SESSION_OPEN_EARLIEST = 8 * 60 + 5        # 08:05
SESSION_OPEN_LATEST = 10 * 60 + 55        # 10:55
_SESSION_OPEN_CHOICES = tuple(
    m for m in range(SESSION_OPEN_EARLIEST, SESSION_OPEN_LATEST + 1) if m % 60 not in (0, 30)
)

# Mail arrival band: from a minute after the PREVIOUS session opened, through 22:59:59 that
# evening, then from 06:00:00 on the session day up to two minutes before the session opens.
# Everything in that union is "already in the inbox when the session opens".
MAIL_DAY_START_SECOND = 6 * 3600                        # 06:00:00
MAIL_NIGHT_END_SECOND = 22 * 3600 + 59 * 60 + 59        # 22:59:59
MAIL_SESSION_GAP_MINUTES = 2

# Per-sender hours (ruling 21 item 3, 2026-09-19). A send window is (first second, last second)
# of the day, both inclusive; the corpus writes it "HH:MM-HH:MM", end exclusive. The default is
# the band above, so a corpus without sender hours renders exactly the pre-ruling stamps.
# No PERSON (non-system sender) may have a window reaching into 23:00-05:00 — the corpus loader
# enforces that bound, which is a realism rule, not farm content.
DEFAULT_SEND_WINDOWS: tuple[tuple[int, int], ...] = ((MAIL_DAY_START_SECOND, MAIL_NIGHT_END_SECOND),)
HUMAN_EARLIEST_SECOND = 5 * 3600                         # 05:00:00
HUMAN_LATEST_SECOND = 23 * 3600 - 1                      # 22:59:59
_WINDOW_RE = re.compile(r"(\d\d):(\d\d)-(\d\d):(\d\d)")

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


def _hash(salt: str) -> int:
    """A stable 64-bit number from a string. Hash, never RNG and never the wall clock: the same
    corpus must render the same times on every machine and every run."""
    return int(hashlib.sha256(salt.encode("utf-8")).hexdigest()[:16], 16)


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

def session_open_minutes(start_date: str, day_index: int) -> int:
    """Minutes past midnight at which the console session for this calendar day opens.

    Deterministic per day (a hash of the run anchor and the day), somewhere in [08:05, 10:55],
    and never a round :00 or :30 — a fixed 09:00 every session is the single clearest tell that
    the calendar is authored rather than lived."""
    return _SESSION_OPEN_CHOICES[_hash(f"{start_date}:{day_index}") % len(_SESSION_OPEN_CHOICES)]


def session_open_text(start_date: str, day_index: int) -> str:
    """'09:47 CDT' — the clock the console shows when this day's session opens."""
    m = session_open_minutes(start_date, day_index)
    return f"{m // 60:02d}:{m % 60:02d} {central_tz(start_date, day_index)}"


def session_header(start_date: str, day_index: int, *, elapsed: int) -> str:
    """The first line of every console session, in the software's voice."""
    when = f"{long_date(start_date, day_index)}, {session_open_text(start_date, day_index)}"
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

def parse_send_window(spec: str) -> tuple[int, int]:
    """'07:30-18:30' -> (27000, 66599): the first and last second of the day mail may land in.
    Start inclusive, end exclusive; a malformed or empty window is an author error (fail loud)."""
    m = _WINDOW_RE.fullmatch(spec.strip()) if isinstance(spec, str) else None
    if not m:
        raise ValueError(f"send window must be 'HH:MM-HH:MM', got {spec!r}")
    h1, m1, h2, m2 = (int(g) for g in m.groups())
    if h1 > 23 or h2 > 24 or m1 > 59 or m2 > 59 or (h2 == 24 and m2):
        raise ValueError(f"send window out of range: {spec!r}")
    lo, hi = h1 * 3600 + m1 * 60, h2 * 3600 + m2 * 60 - 1
    if hi < lo:
        raise ValueError(f"send window ends before it starts: {spec!r}")
    return lo, hi


def parse_send_windows(spec) -> tuple[tuple[int, int], ...]:
    """A window string or a list of them (office hours plus an occasional late evening)."""
    specs = [spec] if isinstance(spec, str) else list(spec or [])
    if not specs:
        raise ValueError("send_hours must name at least one window")
    return tuple(parse_send_window(s) for s in specs)


def send_windows_for(sender: str, hours: dict) -> tuple[tuple[int, int], ...]:
    """The send windows for a From address, resolved from the corpus `mail_hours` config:
    exact address, then its domain or a parent domain (an agency mailbox is keyed by domain),
    then the list/system default for `system_senders`, then the human default. An empty config
    (fixture corpora) gives DEFAULT_SEND_WINDOWS."""
    if not hours:
        return DEFAULT_SEND_WINDOWS
    addr = (sender or "").strip().lower()
    senders = {k.lower(): v for k, v in (hours.get("senders") or {}).items()}
    if addr in senders:
        return parse_send_windows(senders[addr])
    domain = addr.rsplit("@", 1)[-1] if "@" in addr else addr
    parts = domain.split(".")
    for i in range(len(parts) - 1):
        key = ".".join(parts[i:])
        if key in senders:
            return parse_send_windows(senders[key])
    system = {s.lower() for s in hours.get("system_senders") or []}
    if addr in system and hours.get("system"):
        return parse_send_windows(hours["system"])
    if hours.get("default"):
        return parse_send_windows(hours["default"])
    return DEFAULT_SEND_WINDOWS


def _spans(day_lo: int, day_hi: int, windows) -> list[tuple[int, int]]:
    out = []
    for lo, hi in windows:
        a, b = max(day_lo, lo), min(day_hi, hi)
        if a <= b:
            out.append((a, b))
    return out


def timestamp_for(
    start_date: str,
    day_index: int,
    *,
    salt: str,
    windows: tuple[tuple[int, int], ...] | None = None,
    not_before_day: int | None = None,
) -> str:
    """'2027-09-29 21:14:38 CDT' — when a piece of mail dated `day_index` landed in the inbox.

    Every mail dated day D is already sitting there when D's session opens, so it arrived
    somewhere in the span since the PREVIOUS session: the union of (a) day D-1 from a minute
    after that day's session opened to the end of the day, and (b) day D up to two minutes
    before D's session opens — each cut to the sender's `windows` (default: 06:00-22:59:59,
    the pre-ruling band). `salt` (the mail id) is hashed uniformly across the total SECONDS of
    that union, so two mails on the same day differ to the second, nothing lands on the
    session-open minute, and most mail arrived the previous day — which is what a real inbox
    looks like after a two-week gap, and what a 09:00-on-the-dot block does not.

    `not_before_day` anchors a mail that DESCRIBES an event (visit notes, a lab result, a
    sign-off): with the anchor on D, part (a) is dropped, so notes from a visit on D are never
    stamped the evening before it. If the sender's window leaves nothing before the session
    (a late starter's anchored mail), the default band is used instead — the anchor and the
    no-night rule hold, the sender's hours bend. An anchor after D is an engine bug."""
    if not_before_day is not None and not_before_day > day_index:
        raise ValueError(
            f"mail dated {day_index} cannot describe an event on the later day {not_before_day}"
        )
    prev_lo = (session_open_minutes(start_date, day_index - 1) + 1) * 60
    today_hi = (session_open_minutes(start_date, day_index) - MAIL_SESSION_GAP_MINUTES) * 60
    allow_prev = not_before_day is None or not_before_day < day_index

    def _segments(win) -> list[tuple[int, int, int]]:
        segs = [(day_index - 1, a, b) for a, b in _spans(prev_lo, 24 * 3600 - 1, win)] if allow_prev else []
        return segs + [(day_index, a, b) for a, b in _spans(0, today_hi, win)]

    segments = _segments(windows or DEFAULT_SEND_WINDOWS)
    if not segments:
        segments = _segments(DEFAULT_SEND_WINDOWS)
    total = sum(b - a + 1 for _d, a, b in segments)
    offset = _hash(salt) % total
    for day, a, b in segments:
        span = b - a + 1
        if offset < span:
            second = a + offset
            break
        offset -= span
    hh, rem = divmod(second, 3600)
    mm, ss = divmod(rem, 60)
    return (
        f"{date_for_day(start_date, day)} {hh:02d}:{mm:02d}:{ss:02d} "
        f"{central_tz(start_date, day)}"
    )


# --------------------------------------------------------------------------- advancement

def next_beat(current_day: int, event_days: list[int], end_day: int) -> tuple[int, int]:
    future = [d for d in event_days if d > current_day and d <= end_day]
    new_day = min(future) if future else end_day
    return new_day, new_day - current_day
