"""Deterministic Tier-0 farm P&L. Pure functions read state values + prices and
return dollar terms. Welfare and financial dimensions stay separate (CLAUDE.md);
these functions never touch welfare/world state. All coefficients live in
ModelParams; their values are research-anchored placeholders flagged for
verification at Phase C7 (docs/research/SOURCES.md)."""

from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.layers.production import _interp

LB_PER_SHORT_TON = 2000.0
KG_PER_LB = 0.45359237


def downgrade_frac(age_weeks: float, stress: float, params: ModelParams) -> float:
    """Fraction of eggs downgraded to breaker stock: age curve + stress increment, clamped."""
    base = _interp(age_weeks, params.downgrade_age_wk, params.downgrade_frac_pct) / 100.0
    return max(0.0, min(0.95, base + params.downgrade_stress_coeff * stress))


def revenue_step(hen_day_pct: float, bird_count: int, egg_price_usd_doz: float,
                 dgrade_frac: float, params: ModelParams) -> dict:
    """Daily revenue for one house: sellable dozens at shell price + downgrades at breaker price."""
    eggs = bird_count * (hen_day_pct / 100.0)
    total_dozen = eggs / 12.0
    downgrade_dozen = total_dozen * dgrade_frac
    sellable_dozen = total_dozen - downgrade_dozen
    breaker_price = egg_price_usd_doz * params.breaker_price_frac
    revenue_usd = sellable_dozen * egg_price_usd_doz + downgrade_dozen * breaker_price
    return {
        "total_dozen": total_dozen,
        "sellable_dozen": sellable_dozen,
        "downgrade_dozen": downgrade_dozen,
        "revenue_usd": revenue_usd,
    }


def feed_tons_for_day(feed_g: float, bird_count: int) -> float:
    """Convert per-bird grams/day to US short tons/day for the house."""
    feed_kg = feed_g * bird_count / 1000.0
    feed_lb = feed_kg / KG_PER_LB
    return feed_lb / LB_PER_SHORT_TON


def cost_step(feed_tons: float, ration_usd_ton: float, total_dozen: float,
              bird_count: int, fuel_index: float, params: ModelParams) -> dict:
    """Daily cost lines for one house. Feed priced at spot ration (booked-cost upgrade: Task 6)."""
    feed_cost = feed_tons * ration_usd_ton
    energy_cost = bird_count * params.energy_usd_bird_day * fuel_index
    labor_cost = total_dozen * params.labor_usd_doz
    capital_cost = total_dozen * params.capital_usd_doz
    pullet_amort = bird_count * params.pullet_amort_usd_bird_day
    other_var = total_dozen * params.other_var_usd_doz
    total_cost = feed_cost + energy_cost + labor_cost + capital_cost + pullet_amort + other_var
    return {
        "feed_cost": feed_cost,
        "energy_cost": energy_cost,
        "labor_cost": labor_cost,
        "capital_cost": capital_cost,
        "pullet_amort": pullet_amort,
        "other_var": other_var,
        "total_cost": total_cost,
    }


def consume_feed(financial, feed_tons: float, spot_ration_usd_ton: float) -> float:
    """Draw feed_tons from booked inventory at weighted-average cost; charge any shortfall at
    spot. Mutates financial.{feed_inventory_tons, feed_book_value_usd}. Returns the $ cost.
    This is what makes procurement timing a real lever: feed bought cheap is consumed cheap."""
    on_hand = financial.feed_inventory_tons
    from_inventory = min(feed_tons, on_hand)
    avg_cost = (financial.feed_book_value_usd / on_hand) if on_hand > 0 else 0.0
    inv_cost = from_inventory * avg_cost
    financial.feed_inventory_tons = on_hand - from_inventory
    financial.feed_book_value_usd = max(0.0, financial.feed_book_value_usd - inv_cost)
    shortfall = feed_tons - from_inventory
    spot_cost = shortfall * spot_ration_usd_ton
    return inv_cost + spot_cost
