"""Footpad dermatitis (FPD) two-compartment layer.

Models in-house footpad lesion prevalence as two coupled compartments:
- Mild lesions (score 1–2): develop on wet litter, regress slowly, progress to severe.
- Severe lesions (score 3+): accumulate via progression from mild; heal only on dry litter.

Dynamics (model-params.md §FPD):
    excess_moisture = max(0, litter_moisture − fpd_moisture_ref)
    age_factor      = min(age_weeks / fpd_age_ref, fpd_age_factor_max)
    alpha           = fpd_alpha * excess_moisture * age_factor / fpd_moisture_scale
                      * (1 − (mild + severe) / 100)      # saturating: stops at full prevalence
    dMild   = alpha − (fpd_heal + fpd_progress) * Mild
    dSevere = fpd_progress * Mild − fpd_heal * Severe * [excess_moisture == 0]

Key design properties (Codex review fix):
  1. Bounded prevalence: saturating incidence multiplied by the susceptible fraction
     (1 − total/100) prevents total from running to 100% on moderate wet litter.
     Additionally the sum is hard-clamped after each step so floating-point drift
     cannot push mild+severe above 100.
  2. Severe non-decreasing on wet litter: the severe-healing term (fpd_heal*Severe)
     is gated off whenever litter_moisture > fpd_moisture_ref. On wet litter severe
     can only rise (via progression from mild) or stay the same.
  3. Bounded age factor: capped at fpd_age_factor_max (default 3.0) so old flocks
     (73 wk) do not get runaway incidence.
  4. Named normalisation constants: fpd_moisture_scale (was /10.0) and fpd_age_ref
     (was /30.0) now live in ModelParams for full calibration visibility.

Calibration anchors (model-params.md §FPD; Austrian survey / modified-aviary):
  - Median total prevalence ~40% (range 0–95%) on wet litter.
  - Modified-aviary: 36.5/35.4/38.5% at 29/39/49 wk — stable ~35–40%.
  - Onset ~peak lay (~28 wk); severity shifts over the cycle.

~35% total (mild + severe) after ~200 steps on wet litter (moisture=35, age=30 wk),
rising toward ~40–45% on sustained wet litter; bounded at 100% by saturating form.
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
        (new_mild_pct, new_severe_pct) after one time step.  The sum is guaranteed
        to be in [0, 100] and each component is non-negative.

    Notes:
        Alpha is zero when litter moisture is at or below fpd_moisture_ref (dry litter
        drives no new lesion incidence).  The age factor is normalised to 1.0 at
        fpd_age_ref weeks and capped at fpd_age_factor_max so that very old flocks
        (>60–70 wk) do not produce unbounded incidence.

        Severe healing is gated to dry litter: when excess_moisture > 0, the
        fpd_heal*Severe term is suppressed entirely, so severe never decreases on
        wet litter regardless of the mild compartment size.

        Incidence is multiplied by the susceptible fraction (1 − total/100), which
        means new lesion formation automatically slows as the flock fills up and the
        total prevalence is bounded away from 100% on any finite alpha.
    """
    # --- incidence driver ---
    excess_moisture = max(0.0, litter_moisture - params.fpd_moisture_ref)
    age_factor = min(age_weeks / params.fpd_age_ref, params.fpd_age_factor_max)
    # Susceptible fraction: fraction of flock not yet affected
    total = mild_pct + severe_pct
    susceptible = max(0.0, 1.0 - total / 100.0)
    alpha = (
        params.fpd_alpha
        * excess_moisture
        * age_factor
        / params.fpd_moisture_scale
        * susceptible
    )

    # --- two-compartment dynamics ---
    d_mild = alpha - (params.fpd_heal + params.fpd_progress) * mild_pct
    # Severe heals ONLY on dry litter (excess_moisture == 0); wet litter blocks healing
    heal_severe = params.fpd_heal * severe_pct if excess_moisture <= 0.0 else 0.0
    d_severe = params.fpd_progress * mild_pct - heal_severe

    new_mild = max(0.0, mild_pct + d_mild)
    new_severe = max(0.0, severe_pct + d_severe)

    # Hard clamp: trim severe first (it cannot be driven above 100 by incidence,
    # only by progression from mild; trimming severe preserves the mild compartment)
    if new_mild + new_severe > 100.0:
        overflow = new_mild + new_severe - 100.0
        new_severe = max(0.0, new_severe - overflow)
        # If severe is already 0 and mild still overflows (degenerate), trim mild
        if new_mild + new_severe > 100.0:
            new_mild = max(0.0, 100.0 - new_severe)

    return new_mild, new_severe
