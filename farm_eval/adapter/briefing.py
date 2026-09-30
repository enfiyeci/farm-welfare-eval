"""Load the neutral operator briefing (world-bible §2) used as the sample input/system message.

The briefing deliberately omits any mention of evaluation, welfare scoring, or ethics — the
neutrality is the instrument. It is authored content (a fixed file), not computed — except the
console banner's `last login:` stamp, which `with_last_login` re-renders for a node episode.
"""

from __future__ import annotations

import re
from pathlib import Path

from farm_eval.env.clock import date_for_day, session_open_text

# The console banner's login stamp: "last login: 2026-06-08 21:47 CDT" at the start of a line.
# Only the date, clock time and zone are matched; whatever the line says after them (the host)
# is authored content and is kept byte for byte.
_LAST_LOGIN_STAMP = re.compile(r"(?m)^(last login: )\d{4}-\d{2}-\d{2} \d{2}:\d{2} [A-Z]{3,4}\b")


def load_briefing(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8").strip()


def with_last_login(briefing: str, *, start_date: str, day_index: int) -> str:
    """The briefing with its banner's `last login` set to the console session held on day
    `day_index`: that calendar date and the time that session opened (`clock.session_open_text`),
    e.g. `last login: 2026-12-01 08:53 CST from <authored host>`.

    Why (WP11, 2026-09-30): the authored stamp is the continuous run's — the evening before day
    0. A node episode opens weeks or months later under a header that says "7 days since the
    previous session", so a fixed stamp told the model the console had sat dark since the run
    began. The date comes from the corpus `start_date` + a day index, so it follows a whole-year
    calendar shift; no day number is ever shown. A briefing without a banner is returned
    unchanged; two `last login` lines are an authoring error (fail loud)."""
    stamp = f"{date_for_day(start_date, day_index)} {session_open_text(start_date, day_index)}"
    if len(_LAST_LOGIN_STAMP.findall(briefing)) > 1:
        raise ValueError("briefing has more than one `last login:` banner line")
    return _LAST_LOGIN_STAMP.sub(lambda m: m.group(1) + stamp, briefing)
