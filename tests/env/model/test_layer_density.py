# tests/env/model/test_layer_density.py
"""Stocking density -> litter water loading -> the litter water balance.

Density does not touch any welfare channel directly; it loads the litter with water, and
``density.density_factor`` is the multiplier ``layers/litter.py``'s ``floor_moisture_excess``
applies to its floor-deposition term (Task 3 stubbed that multiplier at 1.0; this module wires
the real one).

The response is a KNEE: a water balance is one-sided (evaporation off a bed is bounded by its
evaporative capacity), so below capacity the factor is a clean linear multiplier and above it
a second, steeper term takes over. See ModelParams (the litter_density_* block) and
evals/hen/research/2026-08-03-stocking-density-archive/2026-08-03-nh3-moisture-decomposition.md
§3 for the corrected 23.0 hens/m2 reference and the AUTHORED-DERIVED 150.0 capacity that
replaces it.
"""
import pytest

from farm_eval.env.model import ModelParams
from farm_eval.env.model.layers import density, litter

P = ModelParams()

# Knee location: capacity/input_ref * ref = 150.0/126.8 * 23.0 ~= 27.2 hens/m2.
KNEE_HENS_M2 = (
    P.litter_evap_capacity_g_kg_day / P.litter_water_input_ref_g_kg_day
) * P.litter_density_ref_hens_m2


# ---------------------------------------------------------------------------------------
# hens_per_m2_litter -- the loading identity
# ---------------------------------------------------------------------------------------
def test_hens_per_m2_litter_is_the_plain_ratio():
    assert density.hens_per_m2_litter(125_000, 6500.0) == pytest.approx(125_000 / 6500.0)


def test_hens_per_m2_litter_is_zero_for_an_empty_or_arealess_house():
    assert density.hens_per_m2_litter(0, 6500.0) == 0.0
    assert density.hens_per_m2_litter(125_000, 0.0) == 0.0
    assert density.hens_per_m2_litter(-1, 6500.0) == 0.0
    assert density.hens_per_m2_litter(125_000, -1.0) == 0.0


# ---------------------------------------------------------------------------------------
# density_factor -- the reference point
# ---------------------------------------------------------------------------------------
def test_factor_is_1_0_exactly_at_the_reference_density():
    # This is the calibration invariant: at 23.0 hens/m2 the litter-lever anchors (Oliveira,
    # calibrated at density_factor=1.0 throughout test_layer_litter.py) must be untouched.
    assert density.density_factor(P.litter_density_ref_hens_m2, P) == pytest.approx(1.0)


def test_knee_sits_near_27_2_hens_m2():
    assert KNEE_HENS_M2 == pytest.approx(27.2, abs=0.05)


def test_factor_is_zero_for_an_empty_house():
    assert density.density_factor(0.0, P) == 0.0
    assert density.density_factor(-5.0, P) == 0.0


# ---------------------------------------------------------------------------------------
# density_factor -- monotone below the knee, super-linear above it
# ---------------------------------------------------------------------------------------
def test_factor_is_monotone_across_the_whole_range():
    hens_m2s = [5, 10, 15, 20, 23, 25, 27, 27.2, 30, 35, 40, 50]
    factors = [density.density_factor(h, P) for h in hens_m2s]
    assert factors == sorted(factors)
    assert len(set(factors)) == len(factors)  # strictly increasing, no flat spots


def test_factor_is_linear_below_the_knee():
    # Below capacity the factor IS `base` -- a clean multiplier, slope exactly 1/ref.
    lo, hi = 10.0, 20.0
    slope = (density.density_factor(hi, P) - density.density_factor(lo, P)) / (hi - lo)
    assert slope == pytest.approx(1.0 / P.litter_density_ref_hens_m2)


def test_factor_is_strictly_super_linear_past_the_knee():
    # Finite-difference slope above the knee must exceed the slope below it -- the defining
    # property of the §3 knee (a bounded evaporative capacity crossed by a linear input).
    below = (density.density_factor(25.0, P) - density.density_factor(20.0, P)) / 5.0
    above = (density.density_factor(35.0, P) - density.density_factor(30.0, P)) / 5.0
    assert above > below
    assert below == pytest.approx(1.0 / P.litter_density_ref_hens_m2)


def test_factor_is_continuous_at_the_knee():
    just_below = density.density_factor(KNEE_HENS_M2 - 1e-6, P)
    just_above = density.density_factor(KNEE_HENS_M2 + 1e-6, P)
    assert just_below == pytest.approx(just_above, abs=1e-4)


# ---------------------------------------------------------------------------------------
# The mechanism-is-alive test (the §3 defect this task fixes): two H4-like loadings must
# actually separate the litter water balance, not just the bare factor.
# ---------------------------------------------------------------------------------------
def _moisture_equilibrium(hens_m2: float, floor_share: float, age_wk: float, depth_cm: float) -> float:
    """Relax litter_moisture_step to its fixed point at a constant loading/schedule/age/depth."""
    factor = density.density_factor(hens_m2, P)
    moisture = 15.0
    for _ in range(500):
        moisture = litter.litter_moisture_step(
            moisture, 2.0, floor_share, age_wk, depth_cm, factor, P
        )
    return moisture


def test_the_mechanism_is_alive_19_vs_29_hens_m2_separate_moisture():
    # H4's own nameplate (125k birds / 6500 m2 = 19.2 hens/m2) against a plausible overstocked
    # equivalent (29): the whole point of Task 7 landing on the CORRECTED 23.0 reference is
    # that this comparison must still separate, unlike the dead-mechanism regression §3 found
    # at the previous (wrong) 21.4/160.0 pairing.
    light = _moisture_equilibrium(19.0, floor_share=1.0, age_wk=22.0, depth_cm=1.0)
    heavy = _moisture_equilibrium(29.0, floor_share=1.0, age_wk=22.0, depth_cm=1.0)
    assert heavy - light >= 2.0, f"mechanism is dead: {light:.2f} -> {heavy:.2f}"


def test_higher_density_never_produces_drier_litter():
    for hens_m2 in (5, 15, 19, 23, 27, 29, 40):
        lo = _moisture_equilibrium(hens_m2, floor_share=0.505, age_wk=40.0, depth_cm=2.0)
        hi = _moisture_equilibrium(hens_m2 + 5, floor_share=0.505, age_wk=40.0, depth_cm=2.0)
        assert hi >= lo


# ---------------------------------------------------------------------------------------
# density_factor is inert without a real loading, matching the layer's other guards.
# ---------------------------------------------------------------------------------------
def test_the_layer_is_inert_for_a_bare_house_with_no_birds_or_no_litter():
    assert density.density_factor(density.hens_per_m2_litter(0, 6500.0), P) == 0.0
    assert density.density_factor(density.hens_per_m2_litter(125_000, 0.0), P) == 0.0
