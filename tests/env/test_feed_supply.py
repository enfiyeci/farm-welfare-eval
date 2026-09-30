"""Feed on hand under the mill's standing delivery (WP6 / backlog B3, 2026-09-30).

Root cause of the "0 t on hand" digest: `feed_inventory_tons` only ever held tonnage the agent
itself ordered. Every tonne the flock ate beyond that was charged at the day's posted price by
`consume_feed` (the shortfall branch) — the farm was always fed, but nothing ever showed the
feed that fed it, so the digest and `read_financials` both read 0 t on a 450,000-bird complex
and models placed 19-39 "emergency" orders an episode.

The fix is presentational and leaves every dollar where it was: the corpus names a standing
delivery that keeps N days' use in the bins (`company.yml` `feed_supply`), the on-hand figure is
that cover plus any agent-ordered stock, and the tonnage the standing delivery supplied (exactly
the shortfall `consume_feed` already bought at the posted price) is shown per session.
"""
from pathlib import Path
import re

import pytest

from farm_eval.env.digest import build_digest, feed_daily_use_tons, feed_on_hand_tons
from farm_eval.env.episode import FarmEnv
from farm_eval.env.loader import build_initial_state, load_corpus, load_schedule
from farm_eval.env.model import ModelParams
from farm_eval.env.model.economics import consume_feed
from farm_eval.env.node_episodes import expand_episodes, load_node_manifest
from farm_eval.env.snapshot import derive_snapshot
from farm_eval.env.state import EnvState, FinancialState, HouseWelfare

REPO_ROOT = Path(__file__).resolve().parents[2]
FIX = Path(__file__).resolve().parents[1] / "fixtures"
_FEED_LINE = re.compile(r"- feed inventory: (\d+) t on hand")


def _house() -> HouseWelfare:
    return HouseWelfare(
        ammonia_ppm=8.0, co2_ppm=1500.0, litter_moisture=25.0, lighting_lux=10.0,
        lighting_hours=16.0, heat_stress_index=0.0, stocking_density=1.0,
    )


def _state(day: int, *, cover_days: float, booked: float = 0.0, delivered: float = 0.0) -> EnvState:
    s = EnvState(start_date="2025-06-09")
    s.day_index = day
    s.world.bird_count["H_A"] = 100_000
    s.world.bird_count["H_EMPTY"] = 0
    s.welfare.houses["H_A"] = _house()
    s.welfare.houses["H_A"].feed_g = 100.0
    s.welfare.houses["H_EMPTY"] = _house()
    s.welfare.houses["H_EMPTY"].feed_g = 100.0  # an empty house eats nothing, whatever it reads
    s.financial.feed_standing_cover_days = cover_days
    s.financial.feed_inventory_tons = booked
    s.financial.feed_mill_delivered_tons_cum = delivered
    return s


# --- unit: the on-hand figure ----------------------------------------------------------------

def test_daily_use_counts_occupied_houses_only():
    s = _state(5, cover_days=3.0)
    # 100,000 birds x 100 g = 10,000 kg = 11.02 short tons
    assert feed_daily_use_tons(s) == pytest.approx(11.023, abs=1e-3)


def test_on_hand_is_standing_cover_plus_ordered_stock():
    s = _state(5, cover_days=3.0, booked=40.0)
    assert feed_on_hand_tons(s) == pytest.approx(40.0 + 3.0 * feed_daily_use_tons(s))


def test_without_a_standing_delivery_on_hand_is_the_ordered_stock_alone():
    # Legacy / fixture corpora with no `feed_supply` block keep the old figure exactly.
    s = _state(5, cover_days=0.0, booked=42.0)
    assert feed_on_hand_tons(s) == 42.0


def test_digest_shows_cover_days_and_mill_delivery_over_the_gap():
    before = _state(10, cover_days=3.0, delivered=500.0)
    after = _state(14, cover_days=3.0, delivered=544.0)
    text = build_digest(before, after, [])
    m = _FEED_LINE.search(text)
    assert m and int(m.group(1)) == round(feed_on_hand_tons(after))
    assert "about 3.0 days' use" in text
    assert "standing mill delivery 44 t since last session" in text


def test_digest_without_standing_delivery_is_unchanged():
    before, after = _state(0, cover_days=0.0, booked=42.0), _state(14, cover_days=0.0, booked=42.0)
    text = build_digest(before, after, [])
    assert "- feed inventory: 42 t on hand\n" in text + "\n"
    assert "mill delivery" not in text


def test_consume_feed_counts_the_shortfall_as_mill_delivery_without_changing_its_cost():
    # The standing delivery IS the shortfall branch: same tonnage, same posted price, same $.
    fin = FinancialState(feed_inventory_tons=10.0, feed_book_value_usd=2800.0)
    cost = consume_feed(fin, 25.0, 300.0)
    assert cost == pytest.approx(10.0 * 280.0 + 15.0 * 300.0)
    assert fin.feed_inventory_tons == 0.0
    assert fin.feed_mill_delivered_tons_cum == pytest.approx(15.0)
    fin2 = FinancialState(feed_inventory_tons=30.0, feed_book_value_usd=8400.0)
    consume_feed(fin2, 25.0, 300.0)
    assert fin2.feed_mill_delivered_tons_cum == 0.0  # ordered stock covered the day


def test_cover_days_are_seeded_from_the_corpus_and_default_to_zero():
    fixture = load_corpus(FIX / "corpus")
    assert build_initial_state(fixture).financial.feed_standing_cover_days == 0.0
    fixture.company["feed_supply"] = {"standing_cover_days": 2.5}
    assert build_initial_state(fixture).financial.feed_standing_cover_days == 2.5


def test_read_financials_reports_the_same_on_hand_figure_and_its_parts():
    corpus = load_corpus(FIX / "corpus")
    corpus.company["feed_supply"] = {"standing_cover_days": 3.0, "note": "PLACEHOLDER_TERMS"}
    schedule = load_schedule(FIX / "schedule")
    env = FarmEnv(corpus, schedule, build_initial_state(corpus), 30, ModelParams())
    env.start()
    env.end_day()
    fin = env.read_financials()
    assert fin["feed_inventory_tons"] == round(feed_on_hand_tons(env.state), 2)
    assert fin["feed_inventory_tons"] > 0.0
    assert fin["feed_ordered_stock_tons"] == 0.0
    assert fin["feed_supply_terms"] == "PLACEHOLDER_TERMS"


# --- acceptance: the real bird-flu depopulation episode, do-nothing arm ----------------------

def _dp14_env():
    corpus, schedule = load_corpus(REPO_ROOT / "corpus"), load_schedule(REPO_ROOT / "schedule")
    params = ModelParams()
    eps = expand_episodes(load_node_manifest(REPO_ROOT / "schedule"), schedule)
    ep = next(e for e in eps if e.dp_id == "DP14_HPAI_DEPOP_METHOD")
    state, summary = derive_snapshot(corpus, schedule, params, ep, seed=0)
    env = FarmEnv(corpus, schedule, state, ep.end_day, params, enabled_nodes=None, beat_days=ep.sessions)
    return env, summary


def _digest_tons(summary: str) -> int:
    m = _FEED_LINE.search(summary)
    assert m, summary
    return int(m.group(1))


def test_do_nothing_digest_never_reads_zero_and_matches_read_financials_at_every_open():
    env, summary = _dp14_env()
    opens = [(summary, env.read_financials()["feed_inventory_tons"], env)]
    checked = 0
    while True:
        text, fin_tons, _ = opens[-1]
        birds = sum(env.state.world.bird_count.values())
        if birds > 0:
            assert _digest_tons(text) > 0, text
            assert _digest_tons(text) == round(fin_tons), (text, fin_tons)
            checked += 1
        if env.is_over():
            break
        res = env.end_day()
        opens.append((res.summary, env.read_financials()["feed_inventory_tons"], env))
    assert checked >= 5


def test_an_order_raises_on_hand_by_its_tonnage_and_is_drawn_first():
    env, _ = _dp14_env()
    before = env.read_financials()
    res = env.apply_action("place_feed_order", {"ration": "LP2", "quantity_tons": 24})
    assert res.ok
    after = env.read_financials()
    assert after["feed_inventory_tons"] == pytest.approx(before["feed_inventory_tons"] + 24.0, abs=0.01)
    assert after["feed_ordered_stock_tons"] == pytest.approx(24.0)
    res = env.end_day()
    nxt = env.read_financials()
    assert _digest_tons(res.summary) == round(nxt["feed_inventory_tons"])
    # 24 t is under a day's use on this complex, so the order is gone by the next session.
    assert nxt["feed_ordered_stock_tons"] == 0.0
