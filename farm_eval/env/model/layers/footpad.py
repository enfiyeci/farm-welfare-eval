"""Footpad dermatitis (FPD) two-compartment layer.

Models in-house footpad lesion prevalence as two coupled compartments:
- Mild lesions (score 1–2): develop on wet litter, regress slowly, progress to severe.
- Severe lesions (score 3+): accumulate via progression from mild; barely heal (gamma≈0).

Dynamics (model-params.md §FPD):
    dMild   = alpha(moisture, age) − fpd_heal*Mild   − fpd_progress*Mild
    dSevere = fpd_progress*Mild   − fpd_heal*Severe

Where alpha(moisture, age) is zero below the moisture reference threshold
(fpd_moisture_ref) and rises with both excess litter moisture and flock age.

Calibration anchors (model-params.md §FPD; Austrian survey / modified-aviary):
  - Median total prevalence ~40% (range 0–95%) on wet litter.
  - Modified-aviary: 36.5/35.4/38.5% at 29/39/49 wk — stable ~35-40%.
  - Onset ~peak lay (~28 wk); severity shifts over the cycle.

Settled prevalence on wet litter (moisture=35, age=30, 200 steps): ~33%
(within target 30–45%).
"""
from __future__ import annotations

from farm_eval.env.model.params import ModelParams


def footpad_step(
    mild_pct: float,
    severe_pct: float,
    litter_moisture: float,
    age_weeks: float,
    params: ModelParams,
) -> tuple[float, float]:
    """Advance footpad dermatitis compartments by one time step.

    Args:
        mild_pct:        Current prevalence of mild lesions (0–100 %).
        severe_pct:      Current prevalence of severe lesions (0–100 %).
        litter_moisture: Litter moisture content (%; reference is fpd_moisture_ref).
        age_weeks:       Flock age in weeks.
        params:          Calibrated model parameters.

    Returns:
        (new_mild_pct, new_severe_pct) after one time step, each clamped to [0, 100].

    Notes:
        alpha is zero when litter moisture is at or below fpd_moisture_ref (dry litter
        does not drive new lesion incidence). The age factor normalises to 1.0 at 30 wk
        so that fpd_alpha is interpretable as the per-step incidence rate per 10 units
        of excess moisture at typical mid-lay age.
    """
    # Exposure-driven incidence: zero below moisture reference; rises with excess
    # moisture and flock age (normalised to 1.0 at age_weeks=30).
    excess_moisture = max(0.0, litter_moisture - params.fpd_moisture_ref)
    age_factor = age_weeks / 30.0
    alpha = params.fpd_alpha * excess_moisture * age_factor / 10.0

    # Two-compartment dynamics
    d_mild = alpha - params.fpd_heal * mild_pct - params.fpd_progress * mild_pct
    d_severe = params.fpd_progress * mild_pct - params.fpd_heal * severe_pct

    new_mild = max(0.0, min(100.0, mild_pct + d_mild))
    new_severe = max(0.0, min(100.0, severe_pct + d_severe))

    return new_mild, new_severe
