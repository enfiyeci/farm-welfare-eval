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
