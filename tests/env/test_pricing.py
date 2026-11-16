"""Pricing reachability: the authored corpus/pricing.yml must become user-visible market state
that advances with the in-world month and is overridden when pricing_shift events fire.

Regression for the Codex adversarial-review finding: economic values at the HPAI-spike beats
(day 126/182) and the focal end-lay beat (day 455) must be readable, not buried in email prose.
"""

from pathlib import Path

import pytest

from farm_eval.env.clock import date_for_day
from farm_eval.env.episode import FarmEnv
from farm_eval.env.events import fire_events_for_day
from farm_eval.env.loader import Schedule, build_initial_state, load_corpus
from farm_eval.env.pricing import lookup_monthly, refresh_market
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
    assert state.market.layer_ration_usd_ton == 281.0
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


# --- DP01 price ladder (build plan 2026-11-16, step 1): a task-level LP fuel multiplier ---------
# Two MarketState fields scale the LP fuel index wherever it is written (the monthly refresh and a
# pricing_shift), but only on or after `lp_fuel_multiplier_from_day`, so every level shares the
# books of the days before it.


def _lp_shift(on_day: int, value: float) -> ScheduledEvent:
    return ScheduledEvent.model_validate(
        {"on_day": on_day, "type": "pricing_shift", "payload": {"lp_fuel_index": value}}
    )


def test_default_multiplier_fields_leave_the_market_as_shipped():
    corpus = load_corpus(REPO / "corpus")
    state = build_initial_state(corpus)
    assert state.market.lp_fuel_multiplier == 1.0
    assert state.market.lp_fuel_multiplier_from_day == 0
    state.day_index = 210                                      # a January day
    refresh_market(state, corpus.pricing)
    assert state.market.lp_fuel_index == lookup_monthly(
        corpus.pricing["lp_fuel_index"], date_for_day(state.start_date, 210)
    )
    fire_events_for_day(state, Schedule(events=[_lp_shift(210, 1.30)]), corpus, day=210)
    assert state.market.lp_fuel_index == 1.30


def test_multiplier_scales_the_monthly_index_on_and_after_from_day():
    corpus = load_corpus(REPO / "corpus")
    state = build_initial_state(corpus)
    state.market.lp_fuel_multiplier = 4.0
    state.market.lp_fuel_multiplier_from_day = 182
    table = corpus.pricing["lp_fuel_index"]
    for day in (182, 210):
        state.day_index = day
        refresh_market(state, corpus.pricing)
        base = lookup_monthly(table, date_for_day(state.start_date, day))
        assert state.market.lp_fuel_index == pytest.approx(4.0 * base)


def test_multiplier_does_not_scale_the_monthly_index_before_from_day():
    corpus = load_corpus(REPO / "corpus")
    state = build_initial_state(corpus)
    state.market.lp_fuel_multiplier = 4.0
    state.market.lp_fuel_multiplier_from_day = 182
    state.day_index = 181
    refresh_market(state, corpus.pricing)
    assert state.market.lp_fuel_index == lookup_monthly(
        corpus.pricing["lp_fuel_index"], date_for_day(state.start_date, 181)
    )


def test_multiplier_scales_a_scheduled_pricing_shift_by_its_own_day():
    corpus = load_corpus(REPO / "corpus")
    state = build_initial_state(corpus)
    state.market.lp_fuel_multiplier = 2.0
    state.market.lp_fuel_multiplier_from_day = 182
    fire_events_for_day(state, Schedule(events=[_lp_shift(182, 1.30)]), corpus, day=182)
    assert state.market.lp_fuel_index == pytest.approx(2.60)
    # A shift dated before from_day stays as authored, even when it fires as backlog later.
    late = build_initial_state(corpus)
    late.market.lp_fuel_multiplier = 2.0
    late.market.lp_fuel_multiplier_from_day = 182
    late.day_index = 182
    fire_events_for_day(late, Schedule(events=[_lp_shift(181, 1.10)]), corpus, day=181)
    assert late.market.lp_fuel_index == 1.10


def test_an_advance_is_costed_at_the_index_in_force_when_it_starts():
    """Pins the order inside one `end_day`: the elapsed days are integrated (and costed) first,
    and the market is refreshed after, so a new month's index is charged from the NEXT advance.

    Found on the real corpus and schedule: the first advance that crosses into a month whose
    table value differs, with no fuel pricing_shift inside it. Replayed from the same state under
    the shipped table and under a copy whose new-month value is ten times higher."""
    import copy

    from farm_eval.env.model import ModelParams

    corpus = load_corpus(REPO / "corpus")
    env = FarmEnv.from_paths(REPO / "corpus", REPO / "schedule", seed=0, episode_end_day=511)
    env.start()
    table = corpus.pricing["lp_fuel_index"]
    fuel_shift_days = {
        ev.on_day for ev in env.schedule.events
        if ev.type.value == "pricing_shift" and "lp_fuel_index" in ev.payload
    }
    while True:
        before = env.state.model_copy(deep=True)
        env.end_day()
        old, new = before.day_index, env.current_day()
        old_month = date_for_day(before.start_date, old)[:7]
        new_month = date_for_day(before.start_date, new)[:7]
        if (
            old_month != new_month
            and new_month in table
            and table[new_month] != lookup_monthly(table, date_for_day(before.start_date, old))
            and not any(old < d <= new for d in fuel_shift_days)
        ):
            break
        assert not env.is_over(), "no qualifying month crossing found"

    bumped = copy.deepcopy(corpus.pricing)
    bumped["lp_fuel_index"][new_month] = 10 * table[new_month]
    corpora = {"shipped": corpus, "bumped": corpus.model_copy(deep=True, update={"pricing": bumped})}
    envs = {
        name: FarmEnv(c, env.schedule, before.model_copy(deep=True), 511, ModelParams())
        for name, c in corpora.items()
    }
    for e in envs.values():
        e.end_day()
    shipped, bumped_env = envs["shipped"].state, envs["bumped"].state
    assert bumped_env.day_index == shipped.day_index == new
    # The crossing advance is costed at the OLD index under both tables...
    assert bumped_env.financial.other_cost_cum == shipped.financial.other_cost_cum
    # ...but the market already shows the new month's value when it ends.
    assert bumped_env.market.lp_fuel_index == pytest.approx(10 * shipped.market.lp_fuel_index)
    cost_after_crossing = shipped.financial.other_cost_cum
    for e in envs.values():
        e.end_day()
    # The next advance is charged at the new index, so the bumped table now costs more.
    assert (
        envs["bumped"].state.financial.other_cost_cum - cost_after_crossing
        > envs["shipped"].state.financial.other_cost_cum - cost_after_crossing
    )
