"""Density -> litter loading. Pure functions, no state, no corpus.

Stocking density reaches the welfare channels through the LITTER, not directly. The physical
quantity that matters is hens per m2 of litter: droppings that land on the litter floor load
it with water, and litter moisture is what footpad dermatitis (layers/footpad.py) and the
ammonia moisture term (layers/ammonia.py) actually read.

Why the litter and not the belt (Groot Koerkamp, aviary thesis; see
docs/research/2026-07-30-density-coefficients.md §S28): in an aviary the litter produces about
77 % of the house's ammonia -- 62.5 g/h against 18.8 g/h from the belts -- while receiving only
22.5 % of the droppings. The litter is the dominant source, and density is what loads it.

Both farm-content figures this module needs (`litter_area_frac`, and the reference density used
by callers) arrive in ModelParams from corpus via loader.params_for. They default to 0.0, so a
bare ModelParams() makes every function here return 0.0 rather than inventing a loading.
"""
from __future__ import annotations

from farm_eval.env.model.params import ModelParams

# Unit conversion only -- not farm content, not calibration.
SQ_IN_PER_M2 = 1550.0031


def litter_area_m2(area_sq_in: float, params: ModelParams) -> float:
    """Litter (scratch) floor area in m2, from usable area and the authored litter share.

    Returns 0.0 when either input is absent, which switches the pathway off rather than
    dividing by zero downstream.
    """
    if area_sq_in <= 0.0 or params.litter_area_frac <= 0.0:
        return 0.0
    return area_sq_in * params.litter_area_frac / SQ_IN_PER_M2


def birds_per_m2_litter(area_sq_in: float, birds: float, params: ModelParams) -> float:
    """Hens per m2 of LITTER -- the loading the water balance is driven by.

    For scale: the two measured multi-tier aviaries run at 19.2 hens/m2 (Coalition for
    Sustainable Egg Supply, US commercial) and 21.4 (Groot Koerkamp's 6,480-hen house -- NOT
    the Ch. 7 house at 23.0 that the water-input reference above is taken from; the thesis
    reports both, and conflating them is the defect that reference was corrected for). Our
    houses at the UEP floor of 144 sq in/hen run at 26.3, about 37 % more loaded than CSES --
    a consequence of the authored stocking density, since the litter share itself is the
    measured commercial figure.
    """
    litter_m2 = litter_area_m2(area_sq_in, params)
    if litter_m2 <= 0.0 or birds <= 0:
        return 0.0
    return birds / litter_m2


def litter_water_in_g_per_kg(loading_hens_per_m2: float, params: ModelParams) -> float:
    """Water reaching the litter, g per kg of litter per day, linear in loading.

    Anchored to Groot Koerkamp's measured +126.8 g/kg litter/day (s.e. 19.4) in his CHAPTER 7
    house, whose litter loading was 23.0 hens/m2 (~972 hens over 42.2 m2, the whole floor
    littered), and scaled linearly from there: droppings production is per hen, so the water
    arriving per kg of litter is proportional to hens per m2 of litter.

    The reference used to read 21.4, which is a different house in the same thesis (6,480 hens
    over 303 m2 of litter) -- the input and the loading it is divided by must come from the
    same barn. See params.py:litter_loading_ref_hens_m2.
    """
    if loading_hens_per_m2 <= 0.0 or params.litter_loading_ref_hens_m2 <= 0.0:
        return 0.0
    return (
        params.litter_water_in_ref_g_kg
        * loading_hens_per_m2
        / params.litter_loading_ref_hens_m2
    )


def excess_water_g_per_kg(area_sq_in: float, birds: float, params: ModelParams) -> float:
    """Water input MINUS evaporative capacity, floored at zero.

    This one-sided term is where the knee comes from, and it is why no knee is authored.
    Evaporation from litter is bounded: water activity saturates near 0.86 (Groot Koerkamp),
    so above the sorption plateau the litter cannot shed water any faster no matter how wet it
    gets. Below capacity the belt-driven equilibrium governs entirely and density does nothing
    -- which is exactly Kang's flat 23.67 / 23.57 / 22.93 % across a 31 % density rise. Above
    capacity the surplus has nowhere to go and moisture runs away -- Kang's 40.93 % after the
    next 11.8 %.
    """
    loading = birds_per_m2_litter(area_sq_in, birds, params)
    if loading <= 0.0:
        return 0.0
    water_in = litter_water_in_g_per_kg(loading, params)
    return max(0.0, water_in - params.litter_evap_capacity_g_kg)
