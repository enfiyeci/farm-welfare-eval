import math

from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.layers.ammonia import ammonia_step, fmat
from farm_eval.env.model.layers.litter import litter_moisture_equilibrium


def _eq(ventilation, ambient_c, moisture=25.0, litter_age=60.0, belt_days=2):
    ppm = 5.0
    for _ in range(60):  # iterate to equilibrium
        ppm = ammonia_step(ppm, litter_age, moisture, ventilation, ambient_c, belt_days, ModelParams())
    return ppm


def test_baseline_aviary_mean_near_6_7():
    # model-params: aviary mean ~6.7 ppm at baseline ventilation, mild temp
    assert 5.0 <= _eq(ventilation=1.0, ambient_c=18.0) <= 8.5


def test_winter_low_temp_pushes_over_25():
    # ~12 winter days >25 ppm: cold + baseline vent -> equilibrium climbs past 25
    assert _eq(ventilation=1.0, ambient_c=-8.0) > 25.0


def test_more_ventilation_lowers_ammonia():
    assert _eq(ventilation=3.0, ambient_c=18.0) < _eq(ventilation=1.0, ambient_c=18.0)


def test_more_frequent_belts_lower_ammonia():
    # model-params: lower manure-accumulation time (f_MAT) -> lower NH3. Direction only;
    # the precise same-cycle r_clear (~28.6%) is a refinement not modeled in this layer.
    frequent = _eq(ventilation=1.0, ambient_c=18.0, belt_days=1)
    infrequent = _eq(ventilation=1.0, ambient_c=18.0, belt_days=4)
    assert frequent < infrequent


# --- N2: the layer must stay physical outside f_MAT's calibrated domain ---------------
# The exponential-quadratic f_MAT is a Wageningen fit over belt_days 1-4. Extrapolated to
# 14 it returns a multiplier of ~2143 and the layer reaches ~35,700 ppm. Measured reality:
# aviary weekly belts 32-38 ppm; litter unremoved for two years 9.2-47.4 ppm; worst case in
# ANY system ~85-100 ppm (deep litter with indoor manure storage).
# Probe: docs/probes/node-layer-audit-2026-07-29.md (N2).
# Research: docs/research/2026-07-29-stocking-density.md.


def _eq_belt(belt_days, litter_age=60.0, ventilation=1.0, ambient_c=18.0):
    """Equilibrium ppm at the aviary reference condition, with litter moisture at its
    belt-driven equilibrium (the real coupling) rather than a flat 25 %."""
    params = ModelParams()
    moisture = litter_moisture_equilibrium(belt_days, params)
    ppm = 5.0
    for _ in range(200):
        ppm = ammonia_step(ppm, litter_age, moisture, ventilation, ambient_c, belt_days, params)
    return ppm


def test_weekly_belt_removal_matches_measured_aviary_band():
    # research 2026-07-29: aviary with weekly belt removal measures 32-38 ppm
    assert 32.0 <= _eq_belt(7) <= 38.0


def test_two_week_interval_stays_within_measured_no_removal_ceiling():
    # research: litter with NO removal for two years reaches only 9.2-47.4 ppm
    assert _eq_belt(14) <= 47.4


def test_ammonia_never_exceeds_physical_ceiling_in_worst_reachable_state():
    # Worst reachable config: max belt interval, episode-long litter age, throttled winter
    # ventilation. Measured 35,736 ppm before this bound.
    params = ModelParams()
    ppm = 5.0
    for _ in range(400):
        ppm = ammonia_step(ppm, 518.0, params.litter_moisture_max, 0.4, -8.0, 14.0, params)
    assert ppm <= params.nh3_ceiling_ppm


def test_belt_lever_stays_monotone_across_the_full_setpoint_range():
    # The saturating branch must not flatten so hard that the lever stops discriminating.
    # belt_interval_days is bounded (1.0, 14.0) in ModelParams.setpoint_bounds.
    values = [_eq_belt(d) for d in (1, 2, 3, 4, 5, 6, 7, 10, 14)]
    assert values == sorted(values)
    assert values[-1] > values[0] * 5


def test_calibrated_domain_is_byte_identical():
    # d <= 4 is the Wageningen-validated domain; the bound must not touch it. This is what
    # limits how far the golden anchors can move.
    params = ModelParams()
    for d in (1, 2, 3, 4):
        expected = math.exp(
            params.nh3_fmat_linear * (d - 1) + params.nh3_fmat_quad * (d - 1) ** 2
        )
        assert fmat(float(d), params) == expected
