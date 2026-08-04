"""Footpad dermatitis (FPD) two-compartment layer.

Models in-house footpad lesion prevalence as two coupled compartments:
- Mild lesions (score 1–2): develop on wet litter, regress slowly, progress to severe.
- Severe lesions (score 3+): accumulate via progression from mild; heal on dry litter,
  and whenever prevalence sits above the plateau the current litter supports.

Dynamics (model-params.md §FPD):
    excess_moisture = max(0, litter_moisture − fpd_moisture_ref)
    age_factor      = min(age_weeks / fpd_age_ref, fpd_age_factor_max)
    plateau         = piecewise_linear(litter_moisture; fpd_plateau_anchors)
    driver          = max(excess_moisture, fpd_dry_incidence_floor)
                      if litter_moisture >= fpd_moisture_ref else 0
    alpha           = fpd_alpha * driver * age_factor / fpd_moisture_scale
                      * (1 − (mild + severe) / plateau)   # saturating: stops AT the plateau
    may_heal        = excess_moisture == 0 or (mild + severe) > plateau
    dMild   = alpha − (fpd_heal + fpd_progress) * Mild
    dSevere = fpd_progress * Mild − fpd_heal * Severe * [may_heal]

Key design properties:
  1. A real steady state: the saturation target is the moisture-determined `plateau`,
     not a flat 100%. Before that, severe never healed on wet litter, so prevalence
     ratcheted monotonically toward the 100% clamp — 19.6% at day 100 rising to 67.4%
     at day 518 on identical litter — and the reported number said more about episode
     length than about litter condition. The sum is still hard-clamped after each step
     so floating-point drift cannot push mild+severe above 100.
  2. Reversible: healing also opens when prevalence exceeds the plateau, so improving
     the litter reduces prevalence instead of freezing it (Taira et al. 2014 measured
     lesions regressing when birds moved to drier litter). Below the plateau on wet
     litter severe still only rises, so wet litter is never self-correcting.
  3. Bounded age factor: capped at fpd_age_factor_max (default 3.0) so old flocks
     (73 wk) do not get runaway incidence.
  4. Named normalisation constants: fpd_moisture_scale (was /10.0) and fpd_age_ref
     (was /30.0) live in ModelParams for full calibration visibility.

Calibration anchors — the PLATEAU is the calibrated quantity (see fpd_plateau_anchors):
  - Wang, Ekstrand & Svedberg 1998 (White Leghorn LAYERS, 2x2 dry/wet litter x perches):
    foot-pad lesion prevalence 17/13% on dry litter and 49/48% on wet. Dry-litter
    footpad is NOT zero. ⚠️ Read from the PubMed abstract only (paywalled full text),
    which does not state the litter moisture % of its "dry" and "wet" arms — so it fixes
    the prevalence endpoints, not the moistures they occur at.
  - Austrian survey: median total prevalence ~40% (range 0–95%).
  - Modified-aviary: 36.5/35.4/38.5% at 29/39/49 wk — roughly FLAT across the cycle,
    which is the property the plateau reproduces.
  - Groot Koerkamp Ch. 7 Table 4 / Ch. 5: aviary litter is 14.4–20.1% across five belt
    regimes, mean 22.7% over 58 samples, max 43.8% — the moisture axis this maps onto.

Measured over a full 518-day cycle at age 30 wk, starting from an unaffected flock
(total prevalence at day 518, with the plateau it is approaching in brackets):
15% litter → 17.7 (19.7); 20% → 31.4 (31.6); 22.7% → 37.9 (38.0); 40% → 48.0 (48.0).
Approach is slower at the dry end because alpha scales with excess moisture, so the
driest corner is still ~2 points below its plateau at the end of the cycle.

Essentially all of the settled prevalence sits in the SEVERE compartment: mild is a
flow-through, drained at (fpd_heal + fpd_progress) per day. At the default belt-2
litter equilibrium (15.85%) day 518 is mild 0.15 / severe 20.46.
"""
from __future__ import annotations

from farm_eval.env.model.params import ModelParams


def _plateau(litter_moisture: float, params: ModelParams) -> float:
    """Prevalence plateau for this litter moisture: piecewise-linear through measured anchors.

    Held flat below the first anchor and above the last, so the plateau is always defined and
    never extrapolated past a measurement.
    """
    anchors = params.fpd_plateau_anchors
    if litter_moisture <= anchors[0][0]:
        return anchors[0][1]
    for (m0, p0), (m1, p1) in zip(anchors, anchors[1:]):
        if litter_moisture <= m1:
            return p0 + (p1 - p0) * (litter_moisture - m0) / (m1 - m0)
    return anchors[-1][1]


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
        Alpha is zero only BELOW fpd_moisture_ref (13%, drier than any litter measured
        in a working aviary).  At or above it the driver is floored at
        fpd_dry_incidence_floor, because Wang et al. 1998 measured 13–17% prevalence on
        dry litter — footpad incidence on dry litter is small, not zero.  The age factor
        is normalised to 1.0 at fpd_age_ref weeks and capped at fpd_age_factor_max so
        that very old flocks (>60–70 wk) do not produce unbounded incidence.

        Incidence is multiplied by the susceptible fraction (1 − total/plateau), so
        prevalence settles AT the moisture-determined plateau rather than climbing to
        the 100% clamp.

        Severe healing is gated to two cases: dry litter (excess_moisture == 0), and
        prevalence above the plateau this litter supports.  Below the plateau on wet
        litter severe never decreases, so wet litter is never self-correcting; above
        it, drying the litter lets prevalence come back down.
    """
    # --- incidence driver ---
    excess_moisture = max(0.0, litter_moisture - params.fpd_moisture_ref)
    age_factor = min(age_weeks / params.fpd_age_ref, params.fpd_age_factor_max)

    # The saturation target the flock approaches, replacing a flat 100 %. A flat target made the
    # layer ratchet to full prevalence on any wet litter, so the reported value depended on how
    # long the episode ran rather than on how wet the litter was.
    plateau = _plateau(litter_moisture, params)

    total = mild_pct + severe_pct
    susceptible = max(0.0, 1.0 - total / plateau) if plateau > 0.0 else 0.0
    # Dry-litter incidence is positive but small (Wang's dry arms: 13-17 % prevalence), so the
    # driver has a floor -- but ONLY at or above the threshold. Applying it below the threshold
    # would generate lesions on bone-dry litter and contradict the dry-litter tests.
    driver = (
        max(excess_moisture, params.fpd_dry_incidence_floor)
        if litter_moisture >= params.fpd_moisture_ref
        else 0.0
    )
    alpha = params.fpd_alpha * driver * age_factor / params.fpd_moisture_scale * susceptible

    # --- two-compartment dynamics ---
    d_mild = alpha - (params.fpd_heal + params.fpd_progress) * mild_pct
    # Severe heals on dry litter, AND whenever prevalence exceeds what this litter supports --
    # otherwise improving the litter can never reduce prevalence. Verified: without the second
    # clause, a flock held 300 d at 40 % moisture (47.96 % prevalence) then moved to 20 % litter
    # (plateau 31.6 %) stayed frozen at 47.96 % for the remaining 218 days. That would make DP16
    # irreversible and path-dependent, and it contradicts Taira et al. 2014, which measured
    # lesions regressing when birds were moved to drier litter.
    may_heal = excess_moisture <= 0.0 or total > plateau
    heal_severe = params.fpd_heal * severe_pct if may_heal else 0.0
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
