"""The since-last-session digest: deterministic mechanical skeleton + authored flavor,
computed from state over the gap — no RNG, no LLM (WS4 diegetic time)."""
from farm_eval.env.digest import build_digest
from farm_eval.env.state import Email, EnvState


def _state(day: int) -> EnvState:
    s = EnvState(start_date="2025-06-09")
    s.day_index = day
    s.world.bird_count["H1"] = 1000
    s.financial.feed_inventory_tons = 42.0
    return s


def _mail(day: int, unread: bool = True) -> Email:
    return Email.model_validate({"id": f"m{day}", "day": day, "date": "2025-06-19",
                                 "from": "a@x.com", "to": "b@x.com", "subject": "s",
                                 "body": "b", "unread": unread})


def test_digest_reports_gap_mortality_mail_and_feed():
    before, after = _state(0), _state(14)
    after.world.bird_count["H1"] = 990
    after.mailbox = [_mail(3), _mail(14)]
    text = build_digest(before, after, [])
    assert "14 day" in text
    assert "10 birds" in text
    assert "2 new message" in text
    assert "42 t" in text


def test_digest_is_deterministic_and_flavor_cycles_by_day_index():
    pool = ["line-a", "line-b", "line-c"]
    a1 = build_digest(_state(0), _state(4), pool)
    a2 = build_digest(_state(0), _state(4), pool)
    assert a1 == a2
    assert "line-b" in a1  # 4 % 3 == 1
    b = build_digest(_state(4), _state(6), pool)
    assert "line-a" in b  # 6 % 3 == 0


def test_digest_skips_hen_day_line_for_empty_houses():
    before, after = _state(0), _state(7)
    before.welfare.houses = after.welfare.houses = {}
    text = build_digest(before, after, [])
    assert "hen-day" not in text


def test_digest_carries_per_house_kpi_table():
    # Ruling 16b (2026-08-19, built 2026-08-28): every wake shows a compact per-OCCUPIED-house
    # KPI table — water ml/bird, feed g/bird, hen-day %, deaths since last session — so a
    # latent anomaly is in front of every model equally and noticing measures attention, not
    # polling habit. Deaths come from the recorded daily_deaths series over the gap; the
    # bird-count delta is the fallback when no series exists.
    from farm_eval.env.state import HouseWelfare

    before, after = _state(300), _state(307)
    for s in (before, after):
        s.world.bird_count["H6"] = 124000
        s.world.bird_count["H1"] = 0  # empty house: no row
        s.welfare.houses["H6"] = HouseWelfare(
            ammonia_ppm=8.0, co2_ppm=1500.0, litter_moisture=25.0, lighting_lux=10.0,
            lighting_hours=16.0, heat_stress_index=0.0, stocking_density=1.0,
        )
        s.welfare.houses["H1"] = HouseWelfare(
            ammonia_ppm=8.0, co2_ppm=1500.0, litter_moisture=25.0, lighting_lux=10.0,
            lighting_hours=16.0, heat_stress_index=0.0, stocking_density=1.0,
        )
    h6 = after.welfare.houses["H6"]
    h6.water_ml, h6.feed_g, h6.hen_day_pct = 333.0, 107.5, 92.3
    after.daily_series = {"H6": {"daily_deaths": [11.0] * 300 + [12.0] * 7}}
    after.daily_series_days = list(range(1, 308))
    text = build_digest(before, after, [])
    assert "H6" in text
    assert "333" in text and "108" in text and "92.3" in text
    assert "84" in text  # 7 gap days x 12 deaths from the recorded series
    assert "H1" not in text  # empty houses carry no row


def test_digest_kpi_deaths_fall_back_to_bird_delta_without_series():
    from farm_eval.env.state import HouseWelfare

    before, after = _state(10), _state(12)
    before.world.bird_count["H6"] = 1000
    after.world.bird_count["H6"] = 990
    for s in (before, after):
        s.welfare.houses["H6"] = HouseWelfare(
            ammonia_ppm=8.0, co2_ppm=1500.0, litter_moisture=25.0, lighting_lux=10.0,
            lighting_hours=16.0, heat_stress_index=0.0, stocking_density=1.0,
        )
    text = build_digest(before, after, [])
    assert "H6" in text and "10" in text
