"""Stocking density -> litter water loading.

Density reaches the litter/ammonia/footpad channels through ONE physical quantity: hens per
m2 of LITTER floor, not hens per m2 of house. Droppings landing on the litter floor load it
with water, and it is that load -- not the raw stocking-density setpoint -- that
``litter.floor_moisture_excess`` actually reads, through the ``density_factor`` this module
produces.

The response is a KNEE, not a straight line, because evaporation off the bed is bounded.
Below the litter's evaporative capacity the belt-driven equilibrium governs and the density
term is a clean multiplier that sits at 1.0 at the reference loading (23.0 hens/m2); above
capacity the surplus water has nowhere to go, so the factor climbs super-linearly on top of
that. That is what a one-sided water balance does on its own -- the knee is not authored,
only its two anchors are. See ModelParams (the litter_density_* block) and
evals/hen/research/2026-08-03-stocking-density-archive/2026-08-03-nh3-moisture-decomposition.md
§3, which also documents the corrected 23.0 hens/m2 reference (the previously shipped 21.4
was a provenance error -- a different house in the same Groot Koerkamp thesis).
"""
from __future__ import annotations

from farm_eval.env.model.params import ModelParams


def hens_per_m2_litter(bird_count: int, litter_area_m2: float) -> float:
    """Return hens per m2 of litter floor -- the loading the water balance is driven by.

    0.0 for an empty house or a house with no litter floor at all, rather than dividing by
    zero downstream.
    """
    if bird_count <= 0 or litter_area_m2 <= 0.0:
        return 0.0
    return bird_count / litter_area_m2


def density_factor(hens_m2: float, params: ModelParams) -> float:
    """Return the multiplier ``litter.floor_moisture_excess`` applies for this loading.

    ``base`` is the loading relative to the sourced reference
    (``litter_density_ref_hens_m2``, 23.0 -- Groot Koerkamp ch. 7). ``input`` is the water
    reaching the litter that ``base`` implies, scaled linearly from the sourced anchor
    (``litter_water_input_ref_g_kg_day``, 126.8 g/kg/day at 23.0). Below the litter's
    evaporative capacity (``litter_evap_capacity_g_kg_day``, 150.0 -- AUTHORED-DERIVED, see
    ModelParams) the factor IS ``base``: a clean multiplier that reproduces the reference
    calibration exactly at 1.0. Above capacity the surplus (``input - capacity``) has nowhere
    to evaporate, so a second, steeper term (``litter_density_knee_gain``) adds on top -- the
    knee, continuous at the boundary since the surplus term is exactly 0 there.  That second
    term is ``density_knee_excess`` below, split out so DP25's accrued-harm channel can
    integrate the threshold part on its own without re-deriving it.

    Returns 0.0 at ``hens_m2 <= 0`` (an empty house adds no floor load); otherwise strictly
    increasing in ``hens_m2``.
    """
    if hens_m2 <= 0.0:
        return 0.0
    return hens_m2 / params.litter_density_ref_hens_m2 + density_knee_excess(hens_m2, params)


def density_knee_excess(hens_m2: float, params: ModelParams) -> float:
    """Return the KNEE half of ``density_factor`` -- the part that is a threshold, not a slope.

    ``density_factor`` is a linear base plus this term.  Below the litter's evaporative
    capacity the water balance clears everything the birds put down, so this is EXACTLY 0.0;
    above it the surplus has nowhere to go and the term climbs super-linearly.  Splitting it
    out gives the density->welfare accrual a quantity with the shape the evidence actually
    supports, without authoring a second curve on top of the calibrated one.

    Why the threshold shape is the finding rather than a simplification: Kang et al. 2018
    (aviary Hy-Line Browns) measures a knee at ~19 hens/m2 of pen footprint where litter
    moisture, ammonia, production and stress markers all move together, and the 2026-08-20
    dose-response sweep found NO clean continuous dose-response BELOW that knee -- the field
    studies are null (Decina 2019, Volkmann 2024), non-monotonic (Nicol 2006) or U-shaped
    (von Eugen 2019).  A smooth sub-knee penalty would be invented, so there is none here.
    Evidence grade, stated plainly: the sweep is ABSTRACT-level throughout (it read none of its
    13 sources end to end -- paywalls), so the sub-knee null rests on the CONVERGENCE of those
    abstracts plus the one in-repo full read, Kang 2018.  The magnitude comes from neither: it
    comes from Groot Koerkamp's measured water-input coefficient, already wired above.
    See evals/hen/research/2026-08-03-stocking-density-archive/ (the 2026-07-31 decision
    research and the 2026-08-20 dose-response sweep).
    """
    if hens_m2 <= 0.0:
        return 0.0
    base = hens_m2 / params.litter_density_ref_hens_m2
    water_input = base * params.litter_water_input_ref_g_kg_day
    surplus = max(0.0, water_input - params.litter_evap_capacity_g_kg_day)
    return params.litter_density_knee_gain * surplus / params.litter_evap_capacity_g_kg_day
