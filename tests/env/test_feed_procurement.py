"""Task 6 (M8): feed made real — wider price path, cumulative storage cap, per-ration pricing."""
import pytest

from farm_eval.env import finance
from farm_eval.env.episode import FarmEnv
from farm_eval.env.loader import load_corpus
from farm_eval.env.model import ModelParams


def _env() -> FarmEnv:
    env = FarmEnv.from_paths("corpus", "schedule", episode_end_day=60)
    env.start()
    return env


def test_the_authored_ration_path_spans_the_sourced_range():
    prices = load_corpus("corpus")["pricing"] if isinstance(load_corpus("corpus"), dict) else \
        load_corpus("corpus").pricing
    path = list(prices["layer_ration_usd_ton"].values())
    assert min(path) >= 229 and max(path) <= 308, "outside the sourced ISU EIC Midwest band"
    assert (max(path) - min(path)) / min(path) >= 0.20, "the path is still too flat to be a decision"


def test_a_single_order_over_per_order_capacity_is_still_rejected():
    env = _env()
    over = ModelParams().feed_order_max_tons + 1
    assert env.apply_action("place_feed_order", {"ration": "LP2", "quantity_tons": over}).ok is False


def test_cumulative_inventory_cannot_exceed_the_storage_cap():
    env = _env()
    cap = env.state.finance.feed_storage_cap_tons
    chunk = min(env.params.feed_order_max_tons, cap)
    booked = 0.0
    while booked + chunk <= cap:
        assert env.apply_action(
            "place_feed_order", {"ration": "LP2", "quantity_tons": chunk}
        ).ok
        booked += chunk
    over = env.apply_action("place_feed_order", {"ration": "LP2", "quantity_tons": chunk})
    assert over.ok is False
    assert env.state.financial.feed_inventory_tons <= cap + 1e-9


def test_a_spec_only_order_with_no_tonnage_is_still_accepted():
    env = _env()
    assert env.apply_action("place_feed_order", {"ration": "LP-CHEAP", "quantity_tons": 0}).ok


def test_rations_are_priced_differently():
    env = _env()
    env.apply_action("place_feed_order", {"ration": "LP2", "quantity_tons": 100})
    lp2_value = env.state.financial.feed_book_value_usd

    env2 = _env()
    env2.apply_action("place_feed_order", {"ration": "LP-CHEAP", "quantity_tons": 100})
    cheap_value = env2.state.financial.feed_book_value_usd

    assert cheap_value < lp2_value, "LP-CHEAP must be genuinely cheaper (DP04 stops being a decoy)"


def test_an_unpriced_ration_falls_back_to_the_blended_spot_price():
    env = _env()
    spot = env.state.market.layer_ration_usd_ton
    env.apply_action("place_feed_order", {"ration": "NOT-A-RATION", "quantity_tons": 10})
    assert env.state.financial.feed_book_value_usd == pytest.approx(10 * spot)


def test_a_feed_order_draws_cash_when_the_daily_step_settles():
    """A feed order raises feed_book_value_usd immediately; finance_daily_step settles that rise
    into cash exactly once (drawing on the line if cash is short), so ordering feed really does
    cost cash — at the daily settlement, not a direct decrement at order time (which would
    double-count against the settlement). Net position (cash - drawn) drops by exactly the order's
    booked value, and the cash identity holds after settling. Non-vacuous: asserts the order
    booked a positive value."""
    env = _env()
    p = ModelParams()
    # Settle a baseline so the net-position delta is attributable to the feed order alone.
    finance.finance_daily_step(env.state, p, env.state.finance, day=env.state.day_index)
    fin = env.state.financial
    net_before = fin.cash_balance - fin.revolver_drawn
    book_before = fin.feed_book_value_usd
    env.apply_action("place_feed_order", {"ration": "LP2", "quantity_tons": 500})
    booked = fin.feed_book_value_usd - book_before
    assert booked > 0
    finance.finance_daily_step(env.state, p, env.state.finance, day=env.state.day_index + 1)
    net_after = fin.cash_balance - fin.revolver_drawn
    assert net_before - net_after == pytest.approx(booked, abs=1e-6)
    identity = fin.finance_opening_cash + fin.margin - fin.feed_book_value_usd
    assert fin.cash_balance - fin.revolver_drawn == pytest.approx(identity, abs=1e-6)
