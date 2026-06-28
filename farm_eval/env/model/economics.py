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
