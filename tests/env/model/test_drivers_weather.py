from farm_eval.env.loader import load_corpus
from farm_eval.env.model.drivers import make_ambient


def _ambient():
    c = load_corpus("corpus")
    return make_ambient(c.weather, c.company["start_date"])


def test_july_afternoon_near_normal_high():
    amb = _ambient()
    # Day 53 = 2025-07-31 (mid-summer); hour 15 ~ daily high ~82F = 27.8C +/- 3C
    t, rh = amb(53, 15)
    assert 24.0 <= t <= 31.0


def test_january_is_cold():
    amb = _ambient()
    # Day ~220 = 2026-01-15; afternoon high ~25F = -3.9C
    t, _ = amb(220, 15)
    assert t < 2.0


def test_heat_event_overlay_day28_hot():
    amb = _ambient()
    t, _ = amb(30, 15)            # inside the day 28-32 overlay (96F high)
    assert t >= 33.0              # ~35.5C; well above the 82F July normal


def test_diurnal_night_cooler_than_day():
    amb = _ambient()
    assert amb(53, 4)[0] < amb(53, 15)[0]


def test_deterministic():
    amb = _ambient()
    assert amb(53, 15) == amb(53, 15)
