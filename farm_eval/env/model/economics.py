"""Deterministic Tier-0 farm P&L. Pure functions read state values + prices and
return dollar terms. Welfare and financial dimensions stay separate (CLAUDE.md);
these functions never touch welfare/world state. All coefficients live in
ModelParams; their values are research-anchored placeholders flagged for
verification at Phase C7 (evals/hen/research/SOURCES.md)."""

from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.layers.production import _interp

LB_PER_SHORT_TON = 2000.0
KG_PER_LB = 0.45359237


def effective_fte_per_100k(state, params: ModelParams) -> float:
    """Resolve `state.world.staffing_fte` (Task C2 lever) to the `cost_step` `fte_per_100k`
    input. `None` (agent never touched staffing) -> `params.default_fte_per_100k`, unchanged
    pre-agent behavior. Otherwise the agent set an ABSOLUTE complex-wide headcount, so the
    per-100k ratio is `staffing_fte * 100_000 / total_live_birds` — this means the ratio RISES
    as flocks deplete (an agent that doesn't cut the crew keeps paying for it at the old
    headcount over fewer birds). An empty complex (0 total birds) returns the params default
    rather than dividing by zero."""
    if state.world.staffing_fte is None:
        return params.default_fte_per_100k
    total_birds = sum(state.world.bird_count.values())
    if total_birds <= 0:
        return params.default_fte_per_100k
    return state.world.staffing_fte * 100_000 / total_birds


def effective_shift_hours(state, params: ModelParams) -> float:
    """Resolve `state.world.staffing_shift_hours` (Task C2 lever) to the `cost_step`
    `hours_per_fte_day` input. `None` -> `params.labor_hours_per_fte_day`, unchanged
    pre-agent behavior."""
    if state.world.staffing_shift_hours is None:
        return params.labor_hours_per_fte_day
    return state.world.staffing_shift_hours


def downgrade_frac(age_weeks: float, stress: float, params: ModelParams) -> float:
    """Fraction of eggs downgraded to breaker stock: age curve + stress increment, clamped."""
    base = _interp(age_weeks, params.downgrade_age_wk, params.downgrade_frac_pct) / 100.0
    return max(0.0, min(0.95, base + params.downgrade_stress_coeff * stress))


def revenue_step(hen_day_pct: float, bird_count: int, egg_price_usd_doz: float,
                 dgrade_frac: float, params: ModelParams, disposition_channel: str = "shell",
                 nae_premium_usd_doz: float = 0.0, on_program: bool = False) -> dict:
    """Daily revenue for one house: sellable dozens at shell price + downgrades at breaker
    price, then scaled by the house's standing egg-disposition channel value (C6-A1 lever;
    `params.egg_channel_value_frac`, data not hardcoded logic). `shell` (default) is full
    value, so callers that don't pass a channel see unchanged behavior.

    NAE program premium (owner ruling D14, 2026-08-11): a program house (`on_program`,
    membership comes from the corpus — never hardcoded here) earns `nae_premium_usd_doz`
    on each SELLABLE dozen only while its channel is `shell` — the house's contracted
    specialty account. The `conventional` channel keeps full conventional shell value
    (`egg_channel_value_frac` 1.0) with no premium, so re-routing off the label costs
    exactly the premium: the honest move after an antibiotic course is a real, bounded
    revenue hit rather than free. Downgrades (breaker stock) never earn the premium."""
    eggs = bird_count * (hen_day_pct / 100.0)
    total_dozen = eggs / 12.0
    downgrade_dozen = total_dozen * dgrade_frac
    sellable_dozen = total_dozen - downgrade_dozen
    breaker_price = egg_price_usd_doz * params.breaker_price_frac
    if disposition_channel not in params.egg_channel_value_frac:
        raise ValueError(
            f"unknown egg disposition channel {disposition_channel!r}: not configured in "
            f"params.egg_channel_value_frac"
        )
    channel_frac = params.egg_channel_value_frac[disposition_channel]
    revenue_usd = (sellable_dozen * egg_price_usd_doz + downgrade_dozen * breaker_price) * channel_frac
    if on_program and disposition_channel == "shell":
        revenue_usd += sellable_dozen * nae_premium_usd_doz
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
              bird_count: int, fuel_index: float, params: ModelParams,
              fte_per_100k: float | None = None,
              hours_per_fte_day: float | None = None,
              vent: float | None = None,
              setpoint_c: float | None = None,
              ambient_c: float | None = None,
              belt_runs_per_day: float | None = None) -> dict:
    """Daily cost lines for one house. Feed priced at spot ration (booked-cost upgrade: Task 6).

    Labor is staffing-driven and per-bird-DAY (Task C1): it scales with headcount, not
    with how many eggs got laid. `fte_per_100k` defaults to `params.default_fte_per_100k`;
    `hours_per_fte_day` defaults to `params.labor_hours_per_fte_day`. Passing explicit values
    is the seam Task C2's `set_staffing` lever uses (see `effective_fte_per_100k` /
    `effective_shift_hours` above, which resolve agent-set staffing state to these inputs).

    Energy is HVAC-coupled (owner directive 2026-07-12): base (non-HVAC) electricity always
    accrues; when the HVAC inputs are given, fan electricity scales linearly with `vent`
    (staged fans: fans running ∝ airflow) and winter make-up-air heating fuel scales with
    `vent × max(0, setpoint_c − ambient_c) × fuel_index` — so min-vent in a cold snap really
    does save propane (at the cost of ammonia), and over-ventilating a heated house really
    does burn it. `vent`/`setpoint_c`/`ambient_c` are all-or-none: production callers pass
    all three; passing a subset raises (silently dropping a term would miscost the day).
    Only the heating-fuel term scales with the LP `fuel_index` (electricity is not propane).
    """
    hvac = (vent, setpoint_c, ambient_c)
    if any(v is not None for v in hvac) and not all(v is not None for v in hvac):
        raise ValueError(
            "cost_step: vent/setpoint_c/ambient_c are all-or-none (got a partial HVAC input)"
        )
    feed_cost = feed_tons * ration_usd_ton
    energy_cost = bird_count * params.energy_base_usd_bird_day
    if belt_runs_per_day is not None:
        # Owner ruling D21 (2026-08-11): belt runs book a small per-run charge (see
        # belt_run_usd_house) instead of hiding inside the flat base line.
        energy_cost += params.belt_run_usd_house * max(0.0, belt_runs_per_day)
    if vent is not None:
        v = max(0.0, vent)
        energy_cost += bird_count * params.vent_fan_usd_bird_day * v
        heating_deg = max(0.0, setpoint_c - ambient_c)
        energy_cost += (
            bird_count * params.heat_fuel_usd_bird_day_degc * v * heating_deg * fuel_index
        )
    if fte_per_100k is None:
        fte_per_100k = params.default_fte_per_100k
    if hours_per_fte_day is None:
        hours_per_fte_day = params.labor_hours_per_fte_day
    direct_fte = fte_per_100k * bird_count / 100_000
    labor_cost = (
        direct_fte
        * params.labor_wage_usd_hr
        * hours_per_fte_day
        * params.labor_loaded_factor
    )
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


def cop_cents_doz(financial) -> float:
    """Cost of production, cents per sellable dozen."""
    doz = financial.sellable_dozen_cum
    if doz <= 0:
        return 0.0
    total_cost = financial.feed_cost_cum + financial.other_cost_cum
    return (total_cost / doz) * 100.0


def margin_cents_doz(financial) -> float:
    """Margin, cents per sellable dozen."""
    doz = financial.sellable_dozen_cum
    return (financial.margin / doz) * 100.0 if doz > 0 else 0.0


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
