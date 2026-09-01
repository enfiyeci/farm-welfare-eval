from farm_eval.env.clock import (
    date_for_day,
    format_time_of_day,
    next_beat,
    tool_duration_minutes,
)


def test_date_for_day():
    assert date_for_day("2025-06-09", 0) == "2025-06-09"
    assert date_for_day("2025-06-09", 6) == "2025-06-15"


def test_next_beat_jumps_to_next_event():
    assert next_beat(0, [0, 5, 12], end_day=400) == (5, 5)
    assert next_beat(5, [0, 5, 12], end_day=400) == (12, 7)


def test_next_beat_clamps_to_end():
    assert next_beat(12, [0, 5, 12], end_day=400) == (400, 388)
    assert next_beat(390, [0, 5, 12], end_day=400) == (400, 10)


# --- within-beat tool-time clock (seeded, jittered per-tool durations) ---


def test_tool_duration_is_deterministic_for_same_inputs():
    a = tool_duration_minutes(seed=1, day_index=5, call_index=0, tool="read_sensor",
                              base_minutes=4.0, jitter_frac=0.35)
    b = tool_duration_minutes(seed=1, day_index=5, call_index=0, tool="read_sensor",
                              base_minutes=4.0, jitter_frac=0.35)
    assert a == b


def test_tool_duration_varies_across_call_index():
    # Not a constant per tool: two consecutive identical calls must differ (the anti-eval-
    # awareness point). Distinct call indices, same tool -> a spread of values.
    vals = {tool_duration_minutes(1, 5, i, "read_sensor", 4.0, 0.35) for i in range(8)}
    assert len(vals) > 1


def test_tool_duration_varies_across_seed_and_day():
    # A different run seed (or a different beat) reshuffles the durations, so a fixed policy
    # never sees a byte-identical timing fingerprint across runs.
    base = tool_duration_minutes(1, 5, 0, "read_sensor", 4.0, 0.35)
    assert tool_duration_minutes(2, 5, 0, "read_sensor", 4.0, 0.35) != base
    assert tool_duration_minutes(1, 6, 0, "read_sensor", 4.0, 0.35) != base


def test_tool_duration_within_jitter_band():
    for i in range(64):
        d = tool_duration_minutes(1, 5, i, "read_sensor", 4.0, 0.35)
        assert 4.0 * 0.65 <= d <= 4.0 * 1.35


def test_tool_duration_zero_base_is_zero():
    # A free tool (end_day, glancing at the clock) costs nothing regardless of jitter.
    assert tool_duration_minutes(1, 5, 0, "end_day", 0.0, 0.35) == 0.0


def test_format_time_of_day():
    assert format_time_of_day(0.0, 8 * 60) == "08:00"
    assert format_time_of_day(90.0, 8 * 60) == "09:30"
    assert format_time_of_day(59.4, 8 * 60) == "08:59"  # rounds to the minute
    assert format_time_of_day(600.0, 8 * 60) == "18:00"
