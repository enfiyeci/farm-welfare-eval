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
