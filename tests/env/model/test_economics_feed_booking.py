from farm_eval.env.state import FinancialState
from farm_eval.env.model.economics import consume_feed


def test_consume_from_booked_inventory_uses_avg_cost():
    f = FinancialState(feed_inventory_tons=10.0, feed_book_value_usd=2500.0)  # $250/ton booked
    cost = consume_feed(f, 4.0, spot_ration_usd_ton=300.0)
    assert abs(cost - 1000.0) < 1e-6                 # 4 t @ $250 booked, not $300 spot
    assert abs(f.feed_inventory_tons - 6.0) < 1e-6
    assert abs(f.feed_book_value_usd - 1500.0) < 1e-6


def test_shortfall_charged_at_spot():
    f = FinancialState(feed_inventory_tons=2.0, feed_book_value_usd=500.0)  # $250/ton
    cost = consume_feed(f, 5.0, spot_ration_usd_ton=300.0)
    # 2 t @ $250 = 500, plus 3 t shortfall @ $300 = 900 -> 1400
    assert abs(cost - 1400.0) < 1e-6
    assert abs(f.feed_inventory_tons - 0.0) < 1e-6
    assert abs(f.feed_book_value_usd - 0.0) < 1e-6


def test_buying_ahead_of_price_rise_is_cheaper():
    # Buy 10 t at $250, then consume while spot has risen to $300.
    bought = FinancialState(feed_inventory_tons=10.0, feed_book_value_usd=2500.0)
    spot_only = FinancialState()  # no inventory -> pays spot
    c_bought = consume_feed(bought, 5.0, 300.0)
    c_spot = consume_feed(spot_only, 5.0, 300.0)
    assert c_bought < c_spot
