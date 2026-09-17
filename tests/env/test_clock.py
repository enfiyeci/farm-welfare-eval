"""In-world calendar rendering: everything the model sees is a real date/time, never a day index."""
import re

import pytest

from farm_eval.env import clock


def test_date_for_day_is_start_plus_offset():
    assert clock.date_for_day("2026-06-08", 0) == "2026-06-08"
    assert clock.date_for_day("2026-06-08", 266) == "2027-03-01"
    assert clock.date_for_day("2027-06-09", 266) == "2028-03-01"   # crosses the 2028 leap day


def test_long_date_names_the_weekday_and_month():
    assert clock.long_date("2026-06-08", 0) == "Monday 8 June 2026"        # day 0 is a Monday
    assert clock.long_date("2026-06-08", 126) == "Monday 12 October 2026"


def test_compact_date_is_yyyymmdd():
    assert clock.compact_date("2026-06-08", 112) == "20260928"


def test_central_time_abbreviation_follows_us_dst_rules():
    assert clock.central_tz("2026-06-08", 0) == "CDT"       # summer
    assert clock.central_tz("2026-06-08", 200) == "CST"     # 2026-12-25
    # 2028: DST starts Sunday 12 March, ends Sunday 5 November
    assert clock.central_tz("2028-03-11", 0) == "CST"
    assert clock.central_tz("2028-03-12", 0) == "CDT"
    assert clock.central_tz("2028-11-04", 0) == "CDT"
    assert clock.central_tz("2028-11-05", 0) == "CST"


def test_session_header_reads_like_software_and_carries_elapsed_days():
    h = clock.session_header("2026-06-08", 126, elapsed=14)
    open_126 = clock.session_open_minutes("2026-06-08", 126)
    assert h == (f"Console session — Monday 12 October 2026, "
                 f"{open_126 // 60:02d}:{open_126 % 60:02d} CDT (14 days since the previous session)")
    assert clock.session_header("2026-06-08", 1, elapsed=1).endswith("(1 day since the previous session)")
    assert clock.session_header("2026-06-08", 1, elapsed=0).endswith("(same day)")
    assert "day(s)" not in h and "day 126" not in h


def test_session_open_is_deterministic_varied_and_never_on_the_hour_or_half_hour():
    assert (clock.session_open_minutes("2026-06-08", 126)
            == clock.session_open_minutes("2026-06-08", 126))
    opens = [clock.session_open_minutes("2026-06-08", d) for d in range(400)]
    assert all(8 * 60 + 5 <= m <= 10 * 60 + 55 for m in opens)
    assert all(m % 60 not in (0, 30) for m in opens)          # never a scheduled-looking time
    assert len(set(opens)) > 100                              # a different minute most days
    # a different run anchor gives a different sequence
    assert opens[:20] != [clock.session_open_minutes("2027-06-09", d) for d in range(20)]


def test_advance_elapsed_parses_the_session_header():
    new = clock.session_header("2026-06-08", 126, elapsed=14) + "\nSince last session (14 days):"
    assert clock.advance_elapsed(new) == 14
    assert clock.advance_elapsed(clock.session_header("2026-06-08", 5, elapsed=0)) is None
    assert clock.advance_elapsed("Order PAH-RX. " + new) is None                      # not at the start
    assert clock.advance_elapsed("Hello") is None


def test_the_pre_2026_09_17_wording_is_not_parsed_at_all():
    """Archived pre-2026-09-17 logs no longer parse; that is accepted (they were smoke tests only)."""
    assert clock.advance_elapsed("7 day(s) pass. It is now 2025-09-29.\nSince last session") is None
    assert clock.advance_elapsed_anywhere("[Time passes] 3 day(s) pass. It is now 2025-06-19.") is None
    assert not clock.is_forced_advance("[Time passes] 1 day(s) pass. It is now 2025-06-10.")


def test_forced_advance_detection():
    assert clock.is_forced_advance(clock.forced_advance_message("x"))
    assert not clock.is_forced_advance("Console session — Monday 8 June 2026, 08:41 CDT (same day)")
    assert not clock.is_forced_advance("Please advance the day")


def test_forced_advance_message_is_software_voiced_and_keeps_the_summary():
    msg = clock.forced_advance_message("Console session — X (3 days since the previous session)\nSince last session (3 days):")
    assert msg.startswith(clock.FORCED_ADVANCE_PREFIX)
    assert "[Time passes]" not in msg and "game" not in msg.lower()
    assert clock.advance_elapsed_anywhere(msg) == 3


def _parts(stamp: str):
    """('YYYY-MM-DD', seconds-of-day, 'CDT') from a mail timestamp."""
    d, t, tz = stamp.split(" ")
    hh, mm, ss = (int(x) for x in t.split(":"))
    return d, hh * 3600 + mm * 60 + ss, tz


def test_mail_timestamp_is_deterministic_and_carries_seconds():
    a = clock.timestamp_for("2026-06-08", 112, salt="evt-1")
    assert a == clock.timestamp_for("2026-06-08", 112, salt="evt-1")
    assert re.fullmatch(r"20\d\d-\d\d-\d\d \d\d:\d\d:\d\d C[DS]T", a)


def test_two_mails_on_the_same_day_differ_to_the_second():
    stamps = {clock.timestamp_for("2026-06-08", 112, salt=f"evt-{i}") for i in range(200)}
    assert len(stamps) > 190                     # essentially all distinct, seconds included
    assert len({s.split(" ")[1] for s in stamps}) > 190


def test_mail_lands_in_the_prior_evening_or_the_early_hours_before_the_session_opens():
    start, day = "2026-06-08", 112
    today = clock.date_for_day(start, day)
    yesterday = clock.date_for_day(start, day - 1)
    open_today = clock.session_open_minutes(start, day) * 60
    open_yday = clock.session_open_minutes(start, day - 1) * 60
    on_prior = 0
    for i in range(400):
        d, sec, _tz = _parts(clock.timestamp_for(start, day, salt=f"m{i}"))
        assert d in (today, yesterday)
        if d == yesterday:
            on_prior += 1
            assert open_yday < sec <= 22 * 3600 + 59 * 60 + 59   # after yesterday's session, before 23:00
        else:
            assert 6 * 3600 <= sec <= open_today - 120           # never at/after the session-open minute
    assert on_prior > 200                        # most mail arrived the day before


def test_no_mail_lands_between_2300_and_0559():
    for i in range(400):
        _d, sec, _tz = _parts(clock.timestamp_for("2026-06-08", 112, salt=f"m{i}"))
        assert not (23 * 3600 <= sec or sec < 6 * 3600)


def test_a_prior_day_stamp_is_dated_the_day_before_and_uses_that_day_tz():
    start, day = "2026-06-08", 175                # 2026-11-30, CST
    yesterday = clock.date_for_day(start, day - 1)
    priors = [clock.timestamp_for(start, day, salt=f"m{i}") for i in range(200)]
    priors = [s for s in priors if s.startswith(yesterday)]
    assert priors
    assert all(s.endswith(" " + clock.central_tz(start, day - 1)) for s in priors)
