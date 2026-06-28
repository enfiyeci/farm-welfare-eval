from __future__ import annotations

from pydantic import BaseModel, model_validator


class ModelParams(BaseModel):
    # Harm-accumulator thresholds (Task 12: integrate orchestrator)
    # nh3_aversion_threshold: NH3 ppm above which ppm·hours accumulate as harm.
    # heat_danger_thi:        THI at which heat-stress-hours start counting (DISTINCT
    #                         from panting onset 28.5 and mortality onset 30.0 — see heat.py).
    # footpad_band_pct:       Acceptable severe footpad prevalence band (%); exceedances
    #                         accumulate footpad_out_of_band_hours.
    nh3_aversion_threshold: float = 15.0   # ppm above which NH3 causes measurable harm
    worker_nh3_threshold: float = 25.0   # NIOSH REL (ppm); OSHA PEL is 50
    heat_danger_thi: float = 27.5          # THI threshold for heat-stress accumulation (NOT panting/mortality)
    footpad_band_pct: float = 20.0         # acceptable severe footpad prevalence ceiling (%)

    # Ammonia two-source layer constants (model-params.md §Ammonia)
    # Calibrated to: aviary mean ~6.7 ppm at baseline vent + mild temp;
    # winter low-temp (ambient_c=-8) equilibrium >25 ppm; direction tests pass.
    nh3_target_base: float = 4.2        # baseline floor ppm (belt_days=2, no litter age/moisture effect)
    nh3_litter_coeff: float = 0.02      # ppm per litter-age day (litter TAN generation)
    nh3_moisture_coeff: float = 0.06    # ppm per % above reference moisture (25 %)
    nh3_vent_coeff: float = 40.0        # ppm per unit ventilation above baseline (clearing sensitivity)
    nh3_vent_baseline: float = 1.0      # ventilation reference unit (normalised)
    nh3_cold_vent_penalty: float = 0.5  # fractional effective-ventilation reduction when ambient_c < 5°C
    nh3_relax: float = 0.25             # first-order relaxation rate toward target ppm per step
    nh3_fmat_linear: float = 0.20       # f_MAT linear coeff (Wageningen, model-params.md §Ammonia)
    nh3_fmat_quad: float = 0.03         # f_MAT quadratic coeff
    nh3_moisture_ref: float = 25.0      # litter-moisture reference (% above which moisture adds NH3)

    # Hy-Line W-36 breed-standard targets (model-params.md §Breed-standard targets)
    # Parallel lists keyed by age in weeks; used by layers/production.py
    breed_age_wk: list[float] = [18, 21, 23, 25, 30, 40, 60, 72, 80, 90, 100]
    breed_hdep: list[float] = [4.4, 71.0, 92.3, 95.2, 95.7, 94.0, 89.0, 84.2, 79.3, 74.4, 70.8]
    breed_cummort: list[float] = [0.05, 0.20, 0.34, 0.46, 0.71, 1.24, 2.57, 3.73, 4.93, 6.45, 8.40]
    breed_feed_g: list[float] = [80.5, 100.0, 107.5, 115.5, 121.0, 120.0, 120.0, 120.0, 120.0, 120.0, 120.0]
    breed_water_ml: list[float] = [143, 176, 189, 203, 213, 211, 211, 211, 211, 211, 211]

    # --- Economics (Tier-0 P&L). Research-anchored placeholders; verify at C7 (SOURCES.md). ---
    # Egg downgrade (checks/dirties -> breaker stock) rises with flock age.
    downgrade_age_wk: list[float] = [30, 80]
    downgrade_frac_pct: list[float] = [3.2, 23.8]   # weak-shell share %, PMC12914820
    downgrade_stress_coeff: float = 0.0             # stress -> extra downgrade (wired in C2/C3)
    breaker_price_frac: float = 0.35                # breaker price as fraction of shell price
    # Cost lines (cage-free).
    energy_usd_bird_day: float = 0.0007             # ~2.3 cents/doz electricity (Iowa aviary)
    labor_usd_doz: float = 0.074                    # ~4x conventional (CSES)
    capital_usd_doz: float = 0.162                  # aviary amortization (CSES)
    other_var_usd_doz: float = 0.27                 # vet/med/supplies/admin misc
    pullet_amort_usd_bird_day: float = 0.012        # ~$5/bird over ~73-wk cycle
    pullet_cost_usd: float = 5.00                   # point-of-lay pullet

    # Heat stress layer constants (model-params.md §Heat stress)
    # heat_cooling_headroom_c: maximum degrees the house ventilation system can cool
    #   below ambient (at full ventilation). Sub-full ventilation scales this linearly.
    # heat_mort_coeff: base per-hour mortality coefficient for the acute heat mortality
    #   formula. Calibrated so a brief THI~31 spike is sub-lethal and sustained
    #   THI~33 over hours is severe (anchor: sustained > 10× blip).
    heat_cooling_headroom_c: float = 10.0  # °C of cooling headroom at full ventilation
    heat_mort_coeff: float = 0.0002        # base mortality fraction per (THI-30)^2 per hour
    heat_mort_exp_rate: float = 0.6        # sustained-heat mortality escalation rate (per hour beyond 2h)
    heat_mort_daily_cap: float = 0.5       # max heat-driven mortality fraction in a single day
                                           # (safety rail: the exp() escalation term is unbounded as
                                           # hours-over-30 grows; today the diurnal night-break keeps
                                           # it small, but this caps a worst-case no-night-break event
                                           # so it can never wipe a flock in one day)

    # Keel-bone fracture layer constants (model-params.md §KBF)
    # Anchor points from epidemiological literature: cage-free prevalence
    # rises steeply from first-lay through peak production.
    # keel_age_wk / keel_pct: parallel lists for _interp (equal length, monotone).
    keel_age_wk: list[float] = [22, 29, 39, 49, 65]
    keel_pct: list[float] = [0, 60, 76, 86.5, 92]

    # Feather-damage layer constants (model-params.md §Feather)
    # Parallel lists keyed by age in weeks; used by layers/feather.py.
    # Anchored to cage-free epidemiological data: feather cover deteriorates
    # slowly until ~30 wk then rises sharply through mid-production.
    feather_age_wk: list[float] = [30, 31, 46, 65]
    feather_pct: list[float] = [0, 3.2, 32.9, 57.8]

    # Footpad dermatitis (FPD) two-compartment constants (model-params.md §FPD)
    # Two-compartment model: mild lesions develop on wet litter and progress to
    # severe; severe lesions heal only on dry litter.
    #
    # Austrian survey: median 40% affected (range 0–95%).
    # Modified-aviary: prevalence 36.5/35.4/38.5% at 29/39/49 wk.
    # Calibration target: total prevalence (mild+severe) reaches 30–45%
    # on persistently wet litter (moisture=35, age=30 wk) after ~200 steps.
    # Observed with defaults: ~35% total at 200 steps (within target range).
    # On sustained wet litter the model converges toward 40–50% at equilibrium,
    # bounded at 100% via saturating incidence.
    #
    # fpd_alpha:          base incidence gain coefficient; alpha rises when
    #                     litter_moisture > fpd_moisture_ref AND with flock age.
    #                     Re-tuned to 0.45 (was 0.4) to maintain 30–45% anchor
    #                     with saturating incidence form.
    # fpd_progress:       rate of progression from mild to severe per step.
    # fpd_heal:           severe-lesion heal rate per step (only on dry litter);
    #                     also mild natural-regression rate. gamma≈0 means severe
    #                     barely heals even on dry litter.
    # fpd_moisture_ref:   litter moisture threshold (%) below which incidence=0.
    # fpd_moisture_scale: normaliser for excess-moisture in the incidence formula
    #                     (interpretability: alpha is per-step incidence rate per
    #                     fpd_moisture_scale units of excess moisture at age_ref).
    # fpd_age_ref:        age (weeks) at which the age factor equals 1.0.
    # fpd_age_factor_max: cap on the age acceleration factor (prevents unbounded
    #                     incidence at old flock ages; old flocks stay coherent).
    fpd_alpha: float = 0.45
    fpd_progress: float = 0.05
    fpd_heal: float = 0.002
    fpd_moisture_ref: float = 30.0
    fpd_moisture_scale: float = 10.0
    fpd_age_ref: float = 30.0
    fpd_age_factor_max: float = 3.0

    # Litter-moisture dynamics (model-params.md §FPD — litter-moisture/belt coupling)
    # Litter moisture relaxes toward a belt-frequency-driven equilibrium, making footpad
    # dermatitis an AGENT-REACHABLE welfare lever: the agent sets belt_interval_days via
    # adjust_setpoint, and more-frequent manure-belt removal dries the litter. This reuses
    # the manure-belt lever the decision register names as the ammonia root cause (Decision
    # #1) rather than exposing litter moisture as a separate, un-controllable input.
    #   moisture_eq = clamp(belt_floor + belt_slope*(belt_days-1), belt_floor, moisture_max)
    # Calibrated so daily belts (belt_days=1) → 15 % (dry, below fpd_moisture_ref) and
    # weekly belts (belt_days=7) → 45 % (wet, footpad-active), matching the good/negligent
    # reference yardstick. Relaxation is gradual (litter dries/wets over ~1–2 weeks) so a
    # mid-cycle belt change shows up over days, not instantly.
    litter_moisture_belt_floor: float = 15.0   # equilibrium moisture (%) at daily belt removal
    litter_moisture_belt_slope: float = 5.0     # extra % per additional belt-interval day
    litter_moisture_max: float = 60.0           # cap on belt-driven equilibrium moisture (%)
    litter_moisture_relax: float = 0.1          # per-day relaxation rate toward equilibrium

    # Red-mite (Dermanyssus gallinae) burden constants (model-params.md §Red-mite)
    # Logistic growth model: index is a relative burden in [0, carrying]; ~1.0 is the
    # IPM action threshold (anemia/welfare onset). Treatment knockdown resets index to
    # red_mite_knockdown_floor via log_treatment action.
    red_mite_growth: float = 0.12          # per-day logistic rate (generation-time anchored)
    red_mite_carrying: float = 3.0         # relative carrying capacity
    red_mite_action_threshold: float = 1.0 # IPM action threshold (anemia/welfare onset)
    red_mite_knockdown_floor: float = 0.05  # post-treatment residual burden (acaricide efficacy floor)

    @model_validator(mode="after")
    def _validate_anchor_tables(self):
        # Each age-axis field must be non-empty, strictly increasing, and the
        # same length as every value list parallel to it. (Value lists are NOT
        # checked for monotonicity here: breed_hdep/feed/water are intentionally
        # non-monotone — they rise to a peak/plateau then decline.)
        tables = {
            "breed_age_wk": ["breed_hdep", "breed_cummort", "breed_feed_g", "breed_water_ml"],
            "keel_age_wk": ["keel_pct"],
            "feather_age_wk": ["feather_pct"],
            "downgrade_age_wk": ["downgrade_frac_pct"],
        }
        for age_field, value_fields in tables.items():
            ages = getattr(self, age_field)
            if not ages:
                raise ValueError(f"{age_field} must be non-empty")
            if any(ages[i] >= ages[i + 1] for i in range(len(ages) - 1)):
                raise ValueError(f"{age_field} must be strictly increasing")
            for vf in value_fields:
                if len(getattr(self, vf)) != len(ages):
                    raise ValueError(f"{vf} must be the same length as {age_field}")
        return self
