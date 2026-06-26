"""Market pricing: turn the authored corpus monthly price tables into live, user-visible state.

The corpus carries monthly tables (egg wholesale $/doz, layer ration $/ton, LP fuel index).
`lookup_monthly` resolves the value for an in-world date, carrying forward the latest prior month
for sparse series. `refresh_market` writes the current month's values into EnvState.market as time
advances; scheduled `pricing_shift` events then override it (see events.py). This is the runtime
read path the pricing/financial tools expose, so price/fuel-driven decisions are verifiable through
system data rather than guessable from email prose.
"""

from __future__ import annotations

from farm_eval.env.clock import date_for_day
from farm_eval.env.state import EnvState


def lookup_monthly(table: dict, date_iso: str) -> float | None:
    """Monthly value for ``date_iso`` (YYYY-MM-DD), carrying forward the latest month <= current.

    Returns None if the table is empty or the date precedes its first month.
    """
    if not table:
        return None
    key = date_iso[:7]
    if key in table:
        return float(table[key])
    prior = sorted(k for k in table if k <= key)
    return float(table[prior[-1]]) if prior else None


def refresh_market(state: EnvState, pricing: dict) -> None:
    """Set ``state.market`` from the corpus monthly tables for the state's current in-world date.

    Only overwrites a field when the corresponding table resolves a value, so sparse series
    (e.g. LP fuel index) retain the last known value instead of being zeroed.
    """
    date_iso = date_for_day(state.start_date, state.day_index)
    egg = lookup_monthly(pricing.get("egg_wholesale_usd_doz", {}), date_iso)
    ration = lookup_monthly(pricing.get("layer_ration_usd_ton", {}), date_iso)
    fuel = lookup_monthly(pricing.get("lp_fuel_index", {}), date_iso)
    if egg is not None:
        state.market.egg_price_usd_doz = egg
    if ration is not None:
        state.market.layer_ration_usd_ton = ration
    if fuel is not None:
        state.market.lp_fuel_index = fuel
