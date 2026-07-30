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


def test_the_weekly_belt_anchor_holds_only_at_the_calibrated_litter_age():
    """KNOWN RESIDUAL — pinned deliberately, NOT fixed by the N2 bound.

    The 32-38 ppm aviary band is calibrated at litter_age=60 d. But `litter_age_days`
    only ever increments: it is seeded from corpus and advanced +1/day in integrate.py,
    and NO action in the codebase resets it (only a flock placement would). So by day 518
    a house carries ~578-day litter and the same weekly-belt equilibrium reaches ~90 ppm,
    far outside the cited measurement.

    The driver is `nh3_litter_coeff * litter_age_days` — a SEPARATE unbounded
    extrapolation, of exactly the same species as the f_MAT defect this task fixed: a
    coefficient calibrated over a short horizon and then evaluated far outside it. N2's
    ceiling catches the extreme, but between ~47 and 100 ppm the layer is likely
    overstating late-cycle ammonia.

    Bounding it is a distinct change with its own golden movement and needs a sourced
    long-horizon coefficient, so it is recorded rather than fixed here. This test pins the
    behaviour so it cannot drift silently, and fails loudly if someone bounds the litter
    term without updating docs/model-params.md.
    """
    params = ModelParams()
    late = _eq_belt(7, litter_age=578.0)
    assert 85.0 <= late <= 95.0, "late-cycle weekly-belt equilibrium moved; update the record"
    assert late <= params.nh3_ceiling_ppm
    # The default 2-day interval stays physical even at end-of-episode litter age, which
    # is why this is a residual rather than a blocker for the density wave.
    assert _eq_belt(2, litter_age=578.0) < 25.0


def test_ammonia_never_exceeds_physical_ceiling_in_worst_reachable_state():
    # Worst reachable config: max belt interval, episode-long litter age, throttled winter
    # ventilation. Measured 35,736 ppm before this bound.
    params = ModelParams()
    ppm = 5.0
    for _ in range(400):
        ppm = ammonia_step(ppm, 518.0, params.litter_moisture_max, 0.4, -8.0, 14.0, params)
    assert ppm <= params.nh3_ceiling_ppm


def test_belt_lever_stays_strictly_monotone_across_every_reachable_interval():
    # STRICTLY increasing, not merely non-decreasing: an implementation that rises to d=7
    # and is flat thereafter would satisfy `== sorted(...)` while the lever had stopped
    # discriminating. Fractional values are included because integrate.py passes
    # belt_days_eff = belt_days * (1 + staffing_u * staffing_belt_lag_max), so the setpoint
    # bound of 14 becomes an effective 56 under fully collapsed staffing.
    days = [1, 2, 3, 4, 5, 6, 7, 10, 14, 17.5, 28.0, 42.0, 56.0]
    values = [_eq_belt(d) for d in days]
    for lo, hi in zip(values, values[1:]):
        assert hi > lo, f"belt lever flat or inverted between {lo:.4f} and {hi:.4f}"
    assert values[-1] > values[0] * 5


def test_ventilation_stays_a_live_lever_even_in_the_worst_reachable_house():
    # Regression for the first version of this bound, which clamped only the finished
    # concentration: at belt_days_eff=56, litter age 518 and winter, EVERY ventilation
    # setting from 0 to ~2.29 returned an identical 100 ppm, so raising ventilation bought
    # the agent nothing. Bounding the emission term instead keeps dilution monotone above
    # baseline ventilation. Below baseline the house sits at the physical maximum and
    # cutting ventilation further cannot make the reading worse -- that plateau is intended.
    params = ModelParams()
    at = {
        v: _eq_belt(56.0, litter_age=518.0, ventilation=v, ambient_c=-8.0)
        for v in (2.0, 3.0, 4.0, 5.0)
    }
    assert at[5.0] < at[4.0] < at[3.0] < at[2.0] <= params.nh3_ceiling_ppm


def test_a_legacy_over_ceiling_concentration_is_pulled_under_the_rail_immediately():
    # An EnvState saved under the unbounded model (a checkpoint, or a pinned pilot replay
    # artifact) can carry a concentration far above the rail. Clamping only `target` left
    # it ~9 days above the ceiling, accruing unphysical harm the whole way.
    params = ModelParams()
    out = ammonia_step(1000.0, 60.0, 20.0, 1.0, 18.0, 2, params)
    assert out <= params.nh3_ceiling_ppm


def test_calibrated_domain_is_byte_identical():
    # d <= 4 is the Wageningen-validated domain; the bound must not touch it. This is what
    # limits how far the golden anchors can move.
    params = ModelParams()
    for d in (1, 2, 3, 4):
        expected = math.exp(
            params.nh3_fmat_linear * (d - 1) + params.nh3_fmat_quad * (d - 1) ** 2
        )
        assert fmat(float(d), params) == expected
