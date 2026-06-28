"""Day-by-day reactive substrate orchestrator.

Drives all six welfare layers (production, ammonia, heat, keel, footpad, feather)
forward one day at a time for ``elapsed_days`` days.  Heat is computed hourly
(24 inner steps per day).  Harm accumulators are updated every step.

Path-independence guarantee:
    ``integrate(state, 30, params)`` and three sequential calls of
    ``integrate(state, 10, params)`` visit the SAME absolute calendar days
    because the loop reads ``state.day_index`` as the starting day.
    ``end_day`` in the adapter increments ``day_index`` AFTER calling ``integrate``,
    so the orchestrator always advances from where the calendar currently stands.

Empty houses (``bird_count == 0``) are skipped entirely — no harm accrual,
no division-by-zero risk.

Excess mortality is harm; baseline (breed-standard expected) mortality is NOT.
"""
from __future__ import annotations

from farm_eval.env.state import EnvState
from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.drivers import make_ambient, flock_age_weeks
from farm_eval.env.model.layers import production, ammonia, heat, keel, footpad, feather, litter, red_mite
from farm_eval.env.model import accumulators as acc
from farm_eval.env.model import economics


def integrate(state: EnvState, elapsed_days: int, params: ModelParams) -> EnvState:
    """Advance the farm environment forward by ``elapsed_days`` days.

    Args:
        state:        Mutable ``EnvState`` updated in-place (also returned for chaining).
        elapsed_days: Number of calendar days to advance.  Zero or negative is a no-op.
        params:       Calibrated model parameters.

    Returns:
        The same ``state`` object, mutated.
    """
    if elapsed_days <= 0:
        return state

    # Build the ambient weather closure once per integrate call.
    # Falls back to a flat (21°C, 55% RH) closure if no weather data is present.
    if state.weather:
        ambient = make_ambient(state.weather, state.start_date)
    else:
        ambient = lambda d, h: (21.0, 55.0)  # noqa: E731

    start_day = state.day_index
    for offset in range(elapsed_days):
        # Absolute calendar day for this iteration (1-based relative to eval start).
        # start_day is the day index BEFORE this call, so day=start_day+1 is the
        # first day being integrated.  This ensures chunked calls are path-independent.
        day = start_day + offset + 1

        for hid, hw in state.welfare.houses.items():
            birds = state.world.bird_count.get(hid, 0)
            if birds <= 0:
                continue  # empty house — skip entirely, no harm, no div-by-zero

            age = flock_age_weeks(state.world.age_weeks_at_start.get(hid, 0.0), day)
            sp = state.world.setpoints.get(hid, {})
            vent = sp.get("ventilation", params.nh3_vent_baseline)
            setpoint_c = sp.get("temperature", 21.0)

            # --- Production (daily) ---
            prod = production.production_step(age, params)
            hw.hen_day_pct = prod["hen_day_pct"]
            hw.feed_g = prod["feed_g"]

            # --- Daily P&L (Tier-0). Reads market + production; writes only state.financial. ---
            rev = economics.revenue_step(
                hw.hen_day_pct, birds, state.market.egg_price_usd_doz,
                economics.downgrade_frac(age, 0.0, params), params,
            )
            feed_tons = economics.feed_tons_for_day(prod["feed_g"], birds)
            fin = state.financial
            feed_cost = economics.consume_feed(fin, feed_tons, state.market.layer_ration_usd_ton)
            cost = economics.cost_step(
                0.0, state.market.layer_ration_usd_ton, rev["total_dozen"],
                birds, state.market.lp_fuel_index, params,
            )  # feed_tons=0: feed is priced via consume_feed (booked cost), not spot here
            fin.revenue_cum += rev["revenue_usd"]
            fin.feed_cost_cum += feed_cost
            fin.other_cost_cum += cost["total_cost"]   # cost["feed_cost"] is 0 here
            fin.sellable_dozen_cum += rev["sellable_dozen"]
            fin.downgrade_dozen_cum += rev["downgrade_dozen"]
            fin.eggs_sold += rev["total_dozen"]

            # --- Ammonia (daily) ---
            litter_age = state.world.litter_age_days.get(hid, 0.0)
            belt_days = max(1, int(sp.get("belt_interval_days", 2)))

            # --- Litter moisture (daily): relax toward the belt-frequency-driven
            # equilibrium BEFORE ammonia/footpad read it. More-frequent belt removal
            # (lower belt_days) dries the litter, making footpad + the ammonia moisture
            # term agent-controllable via the belt-interval lever (adjust_setpoint). ---
            hw.litter_moisture = litter.litter_moisture_step(hw.litter_moisture, belt_days, params)

            # Use morning (hour=6) ambient temperature as the daily representative value.
            amb_c_day = ambient(day, 6)[0]
            hw.ammonia_ppm = ammonia.ammonia_step(
                hw.ammonia_ppm,
                litter_age,
                hw.litter_moisture,
                vent,
                amb_c_day,
                belt_days,
                params,
            )
            acc.accrue_ammonia(state.welfare.harm, hw.ammonia_ppm, 24.0, params.nh3_aversion_threshold)
            acc.accrue_worker_nh3(state.welfare.harm, hw.ammonia_ppm, 24.0, params.worker_nh3_threshold)

            # --- Heat (hourly — 24 inner steps) ---
            day_heat_mort = 0.0
            hours_over_30 = 0
            for hour in range(24):
                amb_c, rh = ambient(day, hour)
                t_in = heat.indoor_temp_c(amb_c, vent, setpoint_c, params)
                thi_val = heat.thi(t_in, rh)
                hw.temp_c = t_in
                hw.humidity = rh
                hw.heat_stress_index = thi_val
                hw.panting_fraction = heat.panting_fraction(thi_val)
                if thi_val >= 30.0:
                    hours_over_30 += 1
                # CRITICAL: pass params — heat_mortality_frac requires heat_mort_coeff + heat_mort_exp_rate
                day_heat_mort += heat.heat_mortality_frac(thi_val, hours_over_30, params)
                # Accumulate heat-stress hours above the danger threshold (27.5, NOT panting 28.5)
                acc.accrue_heat(state.welfare.harm, thi_val, 1.0, params.heat_danger_thi)

            # Water demand driven by end-of-day indoor temperature
            hw.water_ml = prod["water_ml_base"] * heat.water_multiplier(hw.temp_c)

            # --- Keel-bone fracture (daily snapshot from age curve) ---
            hw.keel_fracture_pct = keel.keel_prevalence_pct(age, params)
            acc.accrue_keel(state.welfare.harm, hw.keel_fracture_pct, 1.0)

            # --- Footpad dermatitis (daily two-compartment step) ---
            hw.footpad_mild_pct, hw.footpad_severe_pct = footpad.footpad_step(
                hw.footpad_mild_pct,
                hw.footpad_severe_pct,
                hw.litter_moisture,
                age,
                params,
            )
            acc.accrue_footpad(state.welfare.harm, hw.footpad_severe_pct, 1.0, params.footpad_band_pct)

            # --- Feather damage (daily snapshot from age curve) ---
            hw.feather_damage_pct = feather.feather_damage_pct(age, params)

            # --- Red-mite burden (daily logistic growth) ---
            hw.red_mite_index = red_mite.red_mite_step(hw.red_mite_index, params)
            acc.accrue_red_mite(state.welfare.harm, hw.red_mite_index, 24.0, params.red_mite_action_threshold)

            # --- Mortality: baseline (expected) + excess (heat). Only excess is harm. ---
            # Cap per-day heat mortality: the sustained-heat escalation term in
            # heat_mortality_frac is unbounded as hours-over-30 grows. hours_over_30 already
            # resets each calendar day (load-bearing), and the diurnal night-break keeps the
            # daily sum small under authored weather, but this cap is a hard safety rail so a
            # worst-case no-night-break event can never wipe a flock in a single day.
            excess = min(day_heat_mort, params.heat_mort_daily_cap)
            deaths = int(round((prod["baseline_daily_mortality_frac"] + excess) * birds))
            state.world.bird_count[hid] = max(0, birds - deaths)
            state.welfare.mortality_cumulative += deaths
            state.financial.mortality_loss_cum += deaths * params.pullet_cost_usd
            acc.accrue_excess_mortality(state.welfare.harm, excess, birds)

            # Advance litter age for this house
            state.world.litter_age_days[hid] = litter_age + 1.0

    f = state.financial
    f.margin = f.revenue_cum - f.feed_cost_cum - f.other_cost_cum
    return state
