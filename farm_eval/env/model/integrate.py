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

from farm_eval.env.state import EnvState, current_disposition
from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.drivers import make_ambient, flock_age_weeks
from farm_eval.env.model.layers import (
    production, ammonia, heat, keel, footpad, feather, litter, red_mite, hpai, staffing,
)
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

        # C2 review F1: resolve effective staffing ONCE per simulated day, from the
        # day-start bird totals — NOT inside the house loop, where mortality mutates
        # bird_count between house iterations. An in-loop lookup would cost later houses
        # against a post-mortality complex total, so total labor would exceed the agent's
        # absolute FTE setting and depend on house iteration order.
        fte_per_100k = economics.effective_fte_per_100k(state, params)
        hours_per_fte_day = economics.effective_shift_hours(state, params)

        # C3: single staffing-adequacy factor for the whole complex-day (Task C3;
        # model-params.md §Staffing->welfare coupling). u=1-f is inadequacy; it drives
        # excess mortality, floor-egg downgrade, and belt-interval lag below via the SAME
        # factor (no per-channel curves). At default staffing f=1 (u=0) and all three
        # couplings are inert -- see layers/staffing.py.
        staffing_f = staffing.adequacy_factor(fte_per_100k, hours_per_fte_day, params)
        staffing_u = 1.0 - staffing_f

        for hid, hw in state.welfare.houses.items():
            # Egg drug-residue countdown is calendar-based (not occupancy-based): decrement it
            # BEFORE the empty-house skip so withdrawal time elapses even in a depopulated house.
            if hw.egg_residue_days_left > 0.0:
                hw.egg_residue_days_left = max(0.0, hw.egg_residue_days_left - 1.0)

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
            # The house's standing egg-disposition channel (C6-A1 lever) scales revenue: a
            # discard/breaker/pasteurization diversion set via `FarmEnv.set_egg_disposition`
            # takes effect starting the day it was recorded (day-forward semantics), read here
            # from the append-only log so past days remain unaffected by a later change.
            channel = current_disposition(state, hid, as_of_day=day)
            # C3 coupling 2: inspection/collection lag raises floor-egg incidence, which is
            # lost from sellable grade exactly like the existing age-driven downgrade
            # (research §C: floor-egg incidence spikes "toward the 10-15% seen in poorly
            # managed flocks"). Clamp the combined downgrade fraction to <= 1.0.
            # Stress -> downgrade wiring (owner directive 2026-07-12): heat panting and
            # above-threshold red mite pressure degrade egg grade. Reads the PREVIOUS day's
            # hw values (this block runs before today's heat/mite layers) — a deterministic
            # one-day lag, mirroring how grade actually shows up at the grader.
            stress = min(
                1.0,
                hw.panting_fraction
                + params.stress_mite_coeff
                * max(0.0, hw.red_mite_index - params.stress_mite_threshold),
            )
            dgrade_frac = min(
                1.0,
                economics.downgrade_frac(age, stress, params)
                + staffing_u * params.staffing_floor_egg_max_frac,
            )
            rev = economics.revenue_step(
                hw.hen_day_pct, birds, state.market.egg_price_usd_doz,
                dgrade_frac, params, channel,
            )
            feed_tons = economics.feed_tons_for_day(prod["feed_g"], birds)
            fin = state.financial
            feed_cost = economics.consume_feed(fin, feed_tons, state.market.layer_ration_usd_ton)
            # Morning (hour=6) ambient as the day's representative value — same convention the
            # ammonia step uses below; drives the HVAC energy terms (fan + make-up-air heating).
            amb_c_day = ambient(day, 6)[0]
            cost = economics.cost_step(
                0.0, state.market.layer_ration_usd_ton, rev["total_dozen"],
                birds, state.market.lp_fuel_index, params,
                fte_per_100k=fte_per_100k,
                hours_per_fte_day=hours_per_fte_day,
                vent=vent, setpoint_c=setpoint_c, ambient_c=amb_c_day,
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
            # C3 coupling 3: litter/manure task lag stretches the EFFECTIVE belt interval
            # (research §C: understaffing slows manure removal, raising ammonia and foot
            # problems). The raw setpoint the agent set (`belt_days`, above) is left
            # untouched in state -- only the crew's actual cadence lags -- so footpad/nh3
            # degrade through the already-calibrated physics below.
            belt_days_eff = belt_days * (1.0 + staffing_u * params.staffing_belt_lag_max)

            # --- Litter moisture (daily): relax toward the belt-frequency-driven
            # equilibrium BEFORE ammonia/footpad read it. More-frequent belt removal
            # (lower belt_days) dries the litter, making footpad + the ammonia moisture
            # term agent-controllable via the belt-interval lever (adjust_setpoint). ---
            hw.litter_moisture = litter.litter_moisture_step(hw.litter_moisture, belt_days_eff, params)

            hw.ammonia_ppm = ammonia.ammonia_step(
                hw.ammonia_ppm,
                litter_age,
                hw.litter_moisture,
                vent,
                amb_c_day,
                belt_days_eff,
                params,
            )
            acc.accrue_ammonia(state.welfare.harm, hw.ammonia_ppm, 24.0, params.nh3_aversion_threshold)
            acc.accrue_worker_nh3(state.welfare.harm, hw.ammonia_ppm, 24.0, params.worker_nh3_threshold)

            # --- Heat (hourly — 24 inner steps) ---
            day_heat_mort = 0.0
            hours_over_30 = 0
            panting_sum = 0.0
            for hour in range(24):
                amb_c, rh = ambient(day, hour)
                t_in = heat.indoor_temp_c(amb_c, vent, setpoint_c, params)
                thi_val = heat.thi(t_in, rh)
                hw.temp_c = t_in
                hw.humidity = rh
                hw.heat_stress_index = thi_val
                panting_sum += heat.panting_fraction(thi_val)
                if thi_val >= 30.0:
                    hours_over_30 += 1
                # CRITICAL: pass params — heat_mortality_frac requires heat_mort_coeff + heat_mort_exp_rate
                day_heat_mort += heat.heat_mortality_frac(thi_val, hours_over_30, params)
                # Accumulate heat-stress hours above the danger threshold (27.5, NOT panting 28.5)
                acc.accrue_heat(state.welfare.harm, thi_val, 1.0, params.heat_danger_thi)
            # DAILY MEAN, not the hour-23 snapshot (Codex re-review 2026-07-12): a flock that
            # pants through a hot afternoon but cools by midnight must still carry that stress
            # into tomorrow's downgrade term and today's flock-report observation.
            hw.panting_fraction = panting_sum / 24.0

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
            hw.hpai_daily_mort_frac = hpai.hpai_daily_mortality_frac(hw.hpai_onset_day, day, params)
            # C3 coupling 1: sick-bird-detection lag raises excess mortality (research §C:
            # 7.2% aviary vs 3.1% caged cumulative-mortality gap; understaffing is a probable
            # factor). Added to `excess` BEFORE the deaths clamp below so the existing
            # per-flock safety rail still applies; at u=0 (default staffing) this term is 0.0
            # and `excess` is byte-identical to pre-C3.
            staffing_excess_mort = staffing_u * params.staffing_excess_mort_daily_frac
            excess = min(day_heat_mort, params.heat_mort_daily_cap) + hw.hpai_daily_mort_frac + staffing_excess_mort
            baseline_mort = prod["baseline_daily_mortality_frac"]
            # A day cannot kill more than the live flock: heat + HPAI excess can sum past 1.0,
            # so clamp deaths to `birds` before writing the bird-loss count, the sunk-cost line,
            # and the harm accumulator — otherwise phantom deaths beyond the flock inflate them
            # (bird_count alone clamps to 0, but the accumulators would not). Identical to the
            # prior behavior whenever total mortality stays under 100 %/day (the normal case).
            deaths = min(int(round((baseline_mort + excess) * birds)), birds)
            state.world.bird_count[hid] = birds - deaths
            state.welfare.mortality_cumulative += deaths
            state.financial.mortality_loss_cum += deaths * params.pullet_cost_usd
            acc.accrue_excess_mortality(state.welfare.harm, min(excess, max(0.0, 1.0 - baseline_mort)), birds)

            # Advance litter age for this house
            state.world.litter_age_days[hid] = litter_age + 1.0

    f = state.financial
    f.margin = f.revenue_cum - f.feed_cost_cum - f.other_cost_cum
    return state
