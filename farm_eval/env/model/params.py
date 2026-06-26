from __future__ import annotations

from pydantic import BaseModel


class ModelParams(BaseModel):
    ammonia_base: float = 5.0
    ammonia_per_litter_day: float = 0.05
    ammonia_vent_coeff: float = 8.0
    vent_baseline: float = 1.0
    ammonia_relax: float = 0.25
    feed_lb_per_bird_day: float = 0.247
    ammonia_mortality_threshold: float = 25.0
    mortality_excess_per_day: float = 0.0003

    # Ammonia two-source layer constants (model-params.md §Ammonia)
    # Calibrated to: aviary mean ~6.7 ppm at baseline vent + mild temp;
    # winter low-temp (ambient_c=-8) equilibrium >25 ppm; direction tests pass.
    nh3_target_base: float = 4.2        # baseline floor ppm (belt_days=2, no litter age/moisture effect)
    nh3_litter_coeff: float = 0.02      # ppm per litter-age day (litter TAN generation)
    nh3_moisture_coeff: float = 0.06    # ppm per g/kg above reference moisture (25 g/kg)
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
