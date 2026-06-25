from farm_eval.env.clock import date_for_day, next_beat


def test_date_for_day():
    assert date_for_day("2025-06-09", 0) == "2025-06-09"
    assert date_for_day("2025-06-09", 6) == "2025-06-15"


def test_next_beat_jumps_to_next_event():
    assert next_beat(0, [0, 5, 12], end_day=400) == (5, 5)
    assert next_beat(5, [0, 5, 12], end_day=400) == (12, 7)


def test_next_beat_clamps_to_end():
    assert next_beat(12, [0, 5, 12], end_day=400) == (400, 388)
    assert next_beat(390, [0, 5, 12], end_day=400) == (400, 10)
