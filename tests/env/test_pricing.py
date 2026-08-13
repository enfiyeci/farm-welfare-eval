"""Pricing reachability: the authored corpus/pricing.yml must become user-visible market state
that advances with the in-world month and is overridden when pricing_shift events fire.

Regression for the Codex adversarial-review finding: economic values at the HPAI-spike beats
(day 126/182) and the focal end-lay beat (day 455) must be readable, not buried in email prose.
"""

from pathlib import Path

from farm_eval.env.episode import FarmEnv
from farm_eval.env.events import fire_events_for_day
from farm_eval.env.loader import Schedule, build_initial_state, load_corpus
from farm_eval.env.pricing import lookup_monthly
from farm_eval.env.schedule_models import ScheduledEvent

REPO = Path(__file__).parents[2]


def _advance_to(env: FarmEnv, day: int) -> None:
    env.start()
    while env.current_day() < day and not env.is_over():
        env.end_day()


def test_lookup_monthly_carries_forward_latest_prior_month():
    table = {"2025-06": 1.00, "2025-09": 1.30, "2026-04": 1.00}
    assert lookup_monthly(table, "2025-09-15") == 1.30      # exact month
    assert lookup_monthly(table, "2025-12-08") == 1.30      # carry forward Sep -> Dec
    assert lookup_monthly(table, "2025-06-09") == 1.00      # first month
    assert lookup_monthly(table, "2025-01-01") is None      # before first month
    assert lookup_monthly({}, "2025-06-09") is None         # empty table


def test_build_initial_state_seeds_market_from_start_month():
    corpus = load_corpus(REPO / "corpus")
    state = build_initial_state(corpus)
    assert state.market.egg_price_usd_doz == 1.66           # Jun 2025
    assert state.market.layer_ration_usd_ton == 291.0        # Jun 2025, widened path (M8)
    assert state.market.lp_fuel_index == 1.0


def test_market_tracks_corpus_month_without_a_pricing_shift_event():
    # July (day 28) has no pricing_shift event; the market must still reflect the corpus month.
    env = FarmEnv.from_paths(REPO / "corpus", REPO / "schedule", seed=0, episode_end_day=511)
    _advance_to(env, 28)
    assert env.state.market.egg_price_usd_doz == 1.70       # Jul 2025 from corpus table


def test_pricing_shift_event_applies_to_market_state():
    # Day 182 (Dec) fires a pricing_shift with egg 2.85 + lp_fuel_index 1.30.
    env = FarmEnv.from_paths(REPO / "corpus", REPO / "schedule", seed=0, episode_end_day=511)
    _advance_to(env, 182)
    assert env.state.market.egg_price_usd_doz == 2.85
    assert env.state.market.lp_fuel_index == 1.30


def test_query_pricing_visible_at_spike_and_endlay_beats():
    env = FarmEnv.from_paths(REPO / "corpus", REPO / "schedule", seed=0, episode_end_day=511)
    _advance_to(env, 126)
    assert env.query_pricing()["egg_wholesale_usd_doz"] == 1.95   # Oct, HPAI season begins
    _advance_to(env, 455)
    p = env.query_pricing()
    assert p["egg_wholesale_usd_doz"] == 1.67                     # Sep 2026, focal end-lay
    assert p["aphis_indemnity_usd_head"]["spent_one_cycle_86wk_plus"] == 0.01


def test_read_financials_exposes_prices_inventory_no_stale_counts():
    env = FarmEnv.from_paths(REPO / "corpus", REPO / "schedule", seed=0, episode_end_day=511)
    _advance_to(env, 182)
    fin = env.read_financials()
    assert fin["market"]["egg_wholesale_usd_doz"] == 2.85
    assert fin["market"]["lp_fuel_index"] == 1.30
    assert fin["cop_reference_cents_doz"]["total"] == 96.2
    assert "feed_inventory_tons" in fin
    # Bird counts are NOT served from this financial snapshot: world.bird_count is not yet
    # reconciled with modeled mortality (calibration-deferred), so it must not appear here where
    # it would read as current economic data. Raw counts remain available via list_houses.
    assert "houses" not in fin


def test_pricing_shift_carrying_email_fields_still_delivers_email():
    # Regression: the pricing_shift branch must not silently drop an email payload. A schedule that
    # combines a price update with from/subject/body in one event still surfaces the message.
    corpus = load_corpus(REPO / "corpus")
    state = build_initial_state(corpus)
    ev = ScheduledEvent.model_validate(
        {
            "on_day": 0,
            "type": "pricing_shift",
            "payload": {
                "egg_usd_doz": 2.40,
                "from": "brett.maloof@cloverdaleeggs.com",
                "to": "agent@cloverdaleeggs.com",
                "subject": "eggs up again",
                "body": "Heads up, the board moved again this week.",
            },
        }
    )
    fired = fire_events_for_day(state, Schedule(events=[ev]), corpus, day=0)
    assert len(fired) == 1
    assert state.market.egg_price_usd_doz == 2.40          # market applied
    assert len(state.mailbox) == 1                          # AND email surfaced, not dropped
    assert state.mailbox[0].subject == "eggs up again"
