"""Deterministic reactive substrate.

The agent's interventions (setpoints, orders) move these variables; the world evolves the
same way every run given the same actions. Formulas are intentionally simple PLACEHOLDER
calibration — TODO: fit constants to world-bible Hy-Line curve (§6) and price timeline (§8).
"""

from __future__ import annotations

from pydantic import BaseModel

from farm_eval.env.state import EnvState


class ModelParams(BaseModel):
    ammonia_base: float = 5.0
    ammonia_per_litter_day: float = 0.05
    ammonia_vent_coeff: float = 8.0
    vent_baseline: float = 1.0
    ammonia_relax: float = 0.25
    feed_lb_per_bird_day: float = 0.247
    ammonia_mortality_threshold: float = 25.0
    mortality_excess_per_day: float = 0.0003


# TODO(calibration): FinancialState.revenue / feed_cost / margin / eggs_sold / cull_value and
# WelfareState.mortality_rate_weekly are NOT updated by integrate() — they are deferred to
# Phase B model-params calibration. This is intentional for Phase A.
def integrate(state: EnvState, elapsed_days: int, params: ModelParams) -> EnvState:
    if elapsed_days <= 0:
        return state

    mortality_excess = 0.0
    for hid, hw in state.welfare.houses.items():
        litter_age = state.world.litter_age_days.get(hid, 0.0)
        ventilation = state.world.setpoints.get(hid, {}).get("ventilation", params.vent_baseline)

        target = (
            params.ammonia_base
            + params.ammonia_per_litter_day * litter_age
            - params.ammonia_vent_coeff * (ventilation - params.vent_baseline)
        )
        target = max(0.0, target)
        step = min(1.0, params.ammonia_relax * elapsed_days)
        hw.ammonia_ppm = max(0.0, hw.ammonia_ppm + (target - hw.ammonia_ppm) * step)

        state.world.litter_age_days[hid] = litter_age + elapsed_days
        over = max(0.0, hw.ammonia_ppm - params.ammonia_mortality_threshold)
        mortality_excess += over * params.mortality_excess_per_day * elapsed_days

    total_birds = sum(state.world.bird_count.values())
    feed_used_tons = total_birds * params.feed_lb_per_bird_day * elapsed_days / 2000.0
    state.financial.feed_inventory_tons = max(0.0, state.financial.feed_inventory_tons - feed_used_tons)
    state.welfare.mortality_cumulative += mortality_excess
    return state
