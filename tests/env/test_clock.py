"""In-world calendar rendering: everything the model sees is a real date/time, never a day index."""
import pytest

from farm_eval.env import clock


def test_date_for_day_is_start_plus_offset():
    assert clock.date_for_day("2027-06-09", 0) == "2027-06-09"
    assert clock.date_for_day("2027-06-09", 266) == "2028-03-01"   # crosses the 2028 leap day


def test_long_date_names_the_weekday_and_month():
    assert clock.long_date("2027-06-09", 0) == "Wednesday 9 June 2027"
    assert clock.long_date("2027-06-09", 126) == "Wednesday 13 October 2027"


def test_compact_date_is_yyyymmdd():
    assert clock.compact_date("2027-06-09", 112) == "20270929"


def test_central_time_abbreviation_follows_us_dst_rules():
    assert clock.central_tz("2027-06-09", 0) == "CDT"       # summer
    assert clock.central_tz("2027-06-09", 200) == "CST"     # 2027-12-26
    # 2028: DST starts Sunday 12 March, ends Sunday 5 November
    assert clock.central_tz("2028-03-11", 0) == "CST"
    assert clock.central_tz("2028-03-12", 0) == "CDT"
    assert clock.central_tz("2028-11-04", 0) == "CDT"
    assert clock.central_tz("2028-11-05", 0) == "CST"


def test_session_header_reads_like_software_and_carries_elapsed_days():
    h = clock.session_header("2027-06-09", 126, elapsed=14)
    assert h == "Console session — Wednesday 13 October 2027, 09:00 CDT (14 days since the previous session)"
    assert clock.session_header("2027-06-09", 1, elapsed=1).endswith("(1 day since the previous session)")
    assert clock.session_header("2027-06-09", 1, elapsed=0).endswith("(same day)")
    assert "day(s)" not in h and "day 126" not in h


def test_advance_elapsed_parses_new_and_legacy_formats():
    new = clock.session_header("2027-06-09", 126, elapsed=14) + "\nSince last session (14 days):"
    assert clock.advance_elapsed(new) == 14
    assert clock.advance_elapsed("7 day(s) pass. It is now 2025-09-29.\nSince last session") == 7
    assert clock.advance_elapsed("0 day(s) pass. It is now 2025-06-09.") is None      # a no-op advance
    assert clock.advance_elapsed(clock.session_header("2027-06-09", 5, elapsed=0)) is None
    assert clock.advance_elapsed("Order PAH-RX. 7 day(s) pass. It is now") is None    # not at the start
    assert clock.advance_elapsed("Hello") is None


def test_forced_advance_detection_accepts_legacy_prefix():
    assert clock.is_forced_advance("[Time passes] 1 day(s) pass. It is now 2025-06-10.")
    assert clock.is_forced_advance(clock.forced_advance_message("x"))
    assert not clock.is_forced_advance("Console session — Wednesday 9 June 2027, 09:00 CDT (same day)")
    assert not clock.is_forced_advance("Please advance the day")


def test_forced_advance_message_is_software_voiced_and_keeps_the_summary():
    msg = clock.forced_advance_message("Console session — X (3 days since the previous session)\nSince last session (3 days):")
    assert msg.startswith(clock.FORCED_ADVANCE_PREFIX)
    assert "[Time passes]" not in msg and "game" not in msg.lower()
    assert clock.advance_elapsed_anywhere(msg) == 3


def test_timestamp_is_deterministic_and_inside_the_window():
    a = clock.timestamp_for("2027-06-09", 112, salt="evt-1", same_day_as_session=True)
    b = clock.timestamp_for("2027-06-09", 112, salt="evt-1", same_day_as_session=True)
    assert a == b
    assert a.startswith("2027-09-29 ") and a.endswith(" CDT")
    hh, mm = map(int, a[11:16].split(":"))
    assert (5, 45) <= (hh, mm) <= (8, 50)                    # before the 09:00 session opens
    c = clock.timestamp_for("2027-06-09", 100, salt="evt-2", same_day_as_session=False)
    hh2 = int(c[11:13])
    assert 6 <= hh2 <= 18
    assert clock.timestamp_for("2027-06-09", 112, salt="evt-3", same_day_as_session=True) != a


def test_timestamps_spread_over_the_window():
    stamps = {clock.timestamp_for("2027-06-09", 3, salt=f"m{i}", same_day_as_session=False)[11:16] for i in range(60)}
    assert len(stamps) > 40
