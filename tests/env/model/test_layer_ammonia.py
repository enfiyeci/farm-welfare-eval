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


def test_weekly_belt_removal_matches_measured_AVIARY_band():
    """Two aviaries measured at weekly manure-belt removal, at mild conditions.

    Groot Koerkamp thesis Ch. 7 period 2B (weekly belts, litter drying OFF, litter loading
    23.0 hens/m2 of litter): exhaust NH3 6.4 ppm at 19.3 % litter moisture.
    Hinz, Winter & Linke 2010 Table 1, Volierenhaltung (AVIARY) with weekly manure-belt
    removal: median 11.40 ppm, min 2.24, max 18.52 (one-hour spot measurements).

    The band is [6.0, 19.0] -- from Groot Koerkamp's mean to Hinz's aviary maximum.

    NOT calibrated to Nimmermark et al. 2009's 32-38 ppm. That house is a MULTILEVEL house
    measured at 1.48 m3/h per hen with NO supplemental heat, where the authors recorded
    litter caking that the farmer attributed to wheat in the feed, and whose 32.3 ppm / 21-42
    range came from 28 March-7 April at a mean OUTDOOR temperature of +2.1 C. The paper states
    that "the highest ammonia levels occurred on very cold days when the ventilation rate was
    decreased to keep the indoor temperature on the setpoint value" -- so that figure belongs
    to the cold, throttled-ventilation operating point, which this model reaches through
    ``nh3_cold_vent_penalty`` (see test_winter_low_temp_pushes_over_25), NOT to mild baseline.
    Asserting it at mild baseline counted the winter condition twice.
    """
    assert 6.0 <= _eq_belt(7) <= 19.0


def test_belt_multiplier_holds_its_last_validated_value_past_the_domain_edge():
    """f_MAT is a Wageningen fit over belt_days 1-4. Past 4 it HOLDS, it does not grow.

    The previous ceiling for this test (9.2-47.4 ppm, "litter with NO removal for two years")
    was Hinz 2010's *Bodenhaltung* (FLOOR-HOUSING) row, min 9.19 and max 47.42, applied to an
    aviary. Hinz's actual aviary row is 2.24-18.52 ppm. There is no aviary measurement at a
    14-day belt interval, so rather than extrapolate to an invented rail, the multiplier holds
    the last value its fit validates. Any further rise at long belt intervals must come from a
    channel that IS measured -- litter moisture or litter age -- not from f_MAT.

    Asserted on ``fmat`` itself, not on ``_eq_belt``: ``_eq_belt`` also carries the
    litter-moisture channel (``litter_moisture_equilibrium`` keeps rising with belt interval),
    so equal end-to-end ppm past the domain edge is NOT what this fix claims, and would
    contradict the sentence above.
    """
    params = ModelParams()
    edge = fmat(float(params.nh3_fmat_domain_max), params)
    for belt_days in (5, 7, 10, 14, 28, 56):
        assert fmat(float(belt_days), params) == edge, (
            f"f_MAT grew past its domain at {belt_days} d"
        )


def test_the_litter_age_input_is_capped_at_its_calibrated_range():
    """Regression for the litter-age extrapolation (owner ruling 2026-07-30).

    `nh3_litter_coeff` is a linear ppm-per-day rate and `litter_age_days` only ever
    increments -- seeded from corpus at 0-60 d, advanced +1/day at integrate.py:275, with
    no reset path anywhere in the codebase. Evaluated at 578 d it added +11.6 ppm on a base
    of 4.2, drove emission to the ceiling in ORDINARY play (belt=10, adequate staffing,
    late episode, winter) and flattened the ventilation lever there. Same category error as
    the f_MAT extrapolation: a short-horizon coefficient applied far outside its range.

    This replaces a characterisation test that pinned the defect. That test carried an
    instruction to delete it once the two-year analogue came under 47.4; it did (47.27), so
    it was deleted.
    """
    params = ModelParams()

    # Ages beyond the cap contribute nothing further.
    assert _eq_belt(7, litter_age=90.0) == _eq_belt(7, litter_age=730.0)
    assert params.nh3_litter_age_max_days == 60.0

    # Inside the calibrated range the term still does its job.
    assert _eq_belt(7, litter_age=0.0) < _eq_belt(7, litter_age=60.0)

    # The ventilation lever is live again in the state that used to pin at the ceiling.
    lo = _eq_belt(10, litter_age=518.0, ventilation=1.0, ambient_c=-8.0)
    hi = _eq_belt(10, litter_age=518.0, ventilation=2.0, ambient_c=-8.0)
    assert hi < lo, "doubling ventilation must lower ammonia in an ordinary late-episode house"


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
    # Dense sampling INCLUDING fractional low intervals: staffing inadequacy is continuous,
    # so belt_days_eff takes fractional values everywhere, not just at the sampled integers.
    days = [1 + 0.1 * i for i in range(0, 131)] + [14.5, 17.5, 21.0, 28.0, 42.0, 56.0]
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
    # ...and the agent's ventilation must still matter on that first day. Clamping AFTER
    # relaxation collapsed every legacy step to exactly the ceiling, so vent=0 and vent=5
    # were indistinguishable.
    calm = ammonia_step(1000.0, 60.0, 20.0, 0.0, 18.0, 2, params)
    airy = ammonia_step(1000.0, 60.0, 20.0, 5.0, 18.0, 2, params)
    assert airy < calm


def test_calibrated_domain_is_byte_identical():
    # d <= 4 is the Wageningen-validated domain; the bound must not touch it. This is what
    # limits how far the golden anchors can move.
    params = ModelParams()
    for d in (1, 2, 3, 4):
        expected = math.exp(
            params.nh3_fmat_linear * (d - 1) + params.nh3_fmat_quad * (d - 1) ** 2
        )
        assert fmat(float(d), params) == expected
