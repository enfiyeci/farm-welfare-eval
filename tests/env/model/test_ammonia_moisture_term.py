"""Litter moisture drives ammonia, at the sourced coefficient and the right centring.

THE COEFFICIENT. Groot Koerkamp Ch. 5 eq. (18): +4 % TAN per 10 g/kg of litter water, i.e.
0.40 %/(g/kg), fitted over 58 aviary litter samples spanning a MEASURED 52-438 g/kg (5.2-43.8 %
moisture, VIFs 1.09-1.18). Ch. 7 eq. (9)'s alpha3 = 0.32 %/(g/kg) is the same quantity from a
single multivariate fit over a narrower domain (100-240 g/kg = 10-24 % moisture); it was checked
and satisfies every anchor in this file too (belt 2 -> 6.52, belt 7 -> 14.18, belt 14 -> 17.15
ppm). Ch. 5's value is used because its fitted range actually covers this model's band.

THE FORM is multiplicative, because that is how the source fits it: a percentage change in
emission per g/kg of litter water, not ppm per moisture point. The term it replaces was additive
(0.06 ppm/point above 25 %), which is a form the sources do not support.

THE CENTRING is the whole task, and the obvious answer is wrong. Ch. 7's own mean litter water
is 80 g/kg, but centring there breaks this model's baseline rail: belt 2 would reach
5.4 * 1.2586 * exp(0.0040*(158.5-80)) = 9.3 ppm against the 8.5 ppm top of the CSES anchor. The
reason is that `nh3_target_base = 4.2` was ITSELF calibrated to the CSES aviary's 6.7 ppm, at
that house's real litter moisture -- so a mean-centred coefficient must be centred at the
operating point the base was calibrated at, or the moisture already baked into the base is
counted twice. CSES ran manure belts every 3-4 days, which under this model's belt curve
(litter.py, Groot Koerkamp Ch. 7 Table 4) is 15 + 0.85*2.5 = 17.125 %, hence
`nh3_moisture_ref = 17.12`. Same class of error as asserting Nimmermark's cold-throttled
32 ppm at mild baseline (see the f_MAT history in params.py).

KNOWN LIMITATION, deliberately not fixed here: no turnover is implemented. Real ammonia release
falls again on very wet litter -- Miles et al. 2011's fitted surface gives
M_crit = -(beta_ML + beta_MTI*T)/(2*beta_MQ), about 37.4 % at 18 C, 39 % at 21 C, 41 % at 24 C
and 43 % at 28 C. The multiplicative exp() form here climbs monotonically for ever, so above
~37-43 % moisture this model is CONSERVATIVE-HIGH: it over-reports ammonia rather than
under-reporting it. Two tests below bound that, and neither oversells it: the log-linear form
stays inside its fitted domain at every belt interval the agent can SET, but only 11.35 moisture
points separate the worst settable interval from the turnover, so a stocking-density surplus
crosses it in ordinary play -- and the far corner beyond that is bounded by `nh3_ceiling_ppm`.
See docs/model-params.md §Ammonia for where the authored placements land.
"""
from __future__ import annotations

import math

import pytest

from farm_eval.env.model.layers.ammonia import ammonia_step, fmat
from farm_eval.env.model.layers.litter import litter_moisture_equilibrium
from farm_eval.env.model.params import ModelParams

# Groot Koerkamp Ch. 5, the 58-sample aviary litter survey the coefficient is fitted over.
CH5_FITTED_MOISTURE_MIN = 5.2      # 52 g/kg
CH5_FITTED_MOISTURE_MAX = 43.8     # 438 g/kg
# Groot Koerkamp Ch. 7 eq. (9), alpha3's narrower fitted domain.
CH7_FITTED_MOISTURE_MIN = 10.0     # 100 g/kg
CH7_FITTED_MOISTURE_MAX = 24.0     # 240 g/kg
# Miles et al. 2011's derived turnover at this sim's house temperatures (18-28 C).
MILES_TURNOVER_MIN_PCT = 37.4
# Hinz, Winter & Linke 2010 Table 1, Volierenhaltung (AVIARY), weekly manure-belt removal.
HINZ_AVIARY_MAX_PPM = 18.52
# setpoint_bounds caps belt_interval_days at 14; ventilation at 5.0.
MAX_SETTABLE_BELT_DAYS = 14.0


def _eq_at(
    moisture: float,
    *,
    belt_days: float = 2.0,
    ventilation: float = 1.0,
    ambient_c: float = 18.0,
    litter_age: float = 60.0,
    params: ModelParams | None = None,
) -> float:
    """Equilibrium ppm with litter moisture supplied DIRECTLY, everything else at baseline."""
    p = params or ModelParams()
    ppm = 5.0
    for _ in range(300):
        ppm = ammonia_step(ppm, litter_age, moisture, ventilation, ambient_c, belt_days, p)
    return ppm


def _eq_belt(belt_days: float, **kwargs) -> float:
    """Equilibrium ppm with litter moisture at its belt-driven equilibrium (the real chain)."""
    p = kwargs.pop("params", None) or ModelParams()
    return _eq_at(litter_moisture_equilibrium(belt_days, p), belt_days=belt_days, params=p, **kwargs)


def _belt_days_reaching(moisture_pct: float, params: ModelParams) -> float | None:
    """Bisect the EFFECTIVE belt interval at which the equilibrium curve first reaches a moisture.

    Computed, not hand-picked. Naming a corner is how the previous two tasks in this wave got
    their boundary claims wrong three times over; a bisected threshold cannot drift silently.
    Searched over the full effective range (1 to 14 x (1 + staffing_belt_lag_max) = 56).
    """
    hi = MAX_SETTABLE_BELT_DAYS * (1.0 + params.staffing_belt_lag_max)
    if litter_moisture_equilibrium(hi, params) < moisture_pct:
        return None
    lo = 1.0
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if litter_moisture_equilibrium(mid, params) < moisture_pct:
            lo = mid
        else:
            hi = mid
    return hi


def test_wetter_litter_raises_ammonia_at_a_fixed_belt_interval_and_ventilation():
    """The Task 6 deliverable: litter moisture is an ammonia channel in its own right.

    Belt interval and ventilation are held fixed, so the ONLY thing moving is litter moisture --
    which is how stocking density (layers/density.py) and a manure-belt service reach ammonia.
    Before this change the term was inert across the whole operating band: it was additive above
    a 25 % reference, and after the belt curve was bounded to Groot Koerkamp's measured
    14.4-20.1 % aviary band, `max(0, moisture - 25)` was zero everywhere the model actually ran.
    """
    values = [_eq_at(m) for m in (14.0, 15.85, 17.12, 20.0, 26.05, 40.0)]
    assert values == sorted(values), f"ammonia is not monotone in litter moisture: {values}"
    assert values[-1] > values[0] * 2.0, (
        f"the moisture channel is too weak to score: {values[0]:.4f} -> {values[-1]:.4f} ppm"
    )


def test_the_factor_is_exactly_one_at_the_centring_and_falls_below_one_on_drier_litter():
    """No `max(0, ...)` floor: drier-than-CSES litter must be REWARDED, not merely not punished.

    The floor was removed deliberately. CSES's own 3-4-day belt cadence is the centring, so
    daily belts sit BELOW it, and a floored factor would make belt 1 and belt 3.5 emit
    identically -- the agent's best available belt setting would buy nothing over the baseline.

    At the centring the factor is exactly 1.0, so the equilibrium is the bare
    (base + litter-age) x f_MAT emission with no moisture contribution at all. That is what
    "centred where the base was calibrated" MEANS, and it is the assertion that fails if anyone
    re-centres on Ch. 7's 80 g/kg.
    """
    p = ModelParams()
    bare_emission = (
        p.nh3_target_base + p.nh3_litter_coeff * p.nh3_litter_age_max_days
    ) * fmat(2.0, p)

    at_centring = _eq_at(p.nh3_moisture_ref, belt_days=2.0)
    assert at_centring == pytest.approx(bare_emission, rel=1e-9)

    drier = _eq_at(p.litter_moisture_belt_floor, belt_days=2.0)   # 15.0 %, daily belts
    assert drier < at_centring, (
        f"litter drier than the centring is not rewarded: {drier:.4f} vs {at_centring:.4f} ppm"
    )


def test_the_centring_is_the_belt_equilibrium_of_the_house_the_baseline_was_calibrated_in():
    """17.12 % is not a free parameter: it is CSES's 3-4-day belt cadence under this belt curve.

    `nh3_target_base = 4.2` is calibrated to the CSES aviary's measured 6.7 ppm mean, so the
    moisture factor has to be 1.0 at THAT house's litter moisture or the base double-counts.
    CSES removed manure belts every 3-4 days; `litter_moisture_equilibrium(3.5)` = 17.125 %.
    The shipped parameter is rounded to 17.12, a 0.005-point difference worth exp(0.004*0.05)
    = 1.0002x on emission, i.e. 0.02 %.

    Ch. 7's own mean litter water (80 g/kg) is the centring this test exists to forbid: at
    80 g/kg the belt-2 baseline reaches ~8.7 ppm, breaking the 5.0-8.5 ppm CSES rail asserted
    in test_layer_ammonia.py::test_baseline_aviary_mean_near_6_7.
    """
    p = ModelParams()
    cses_belt_cadence_days = 3.5      # "every 3-4 days"
    assert p.nh3_moisture_ref == pytest.approx(
        litter_moisture_equilibrium(cses_belt_cadence_days, p), abs=0.01
    )
    # And the forbidden centring really does break the rail, so this is not a hypothetical.
    at_ch7_centring = _eq_at(
        litter_moisture_equilibrium(2.0, p),
        params=ModelParams(nh3_moisture_ref=8.0),
    )
    assert at_ch7_centring > 8.5


def test_the_coefficient_is_evaluated_inside_its_fitted_domain_at_every_settable_belt_interval():
    """The defect that blocked this task for a whole wave must not silently return.

    alpha3 was unusable while the belt curve ran the litter at 45-60 %, roughly 2x past the top
    of Ch. 7's fitted 100-240 g/kg, where exp(0.0032*370) = 3.27x collided with both belt
    anchors. Bounding the belt curve to the measured band put the operating point back inside
    the domain -- this pins that.

    Honest about WHICH domain: the coefficient in use is Ch. 5 eq. (18), fitted over a measured
    52-438 g/kg (5.2-43.8 %), which covers every belt interval the agent can set. Ch. 7's
    narrower 100-240 g/kg (10-24 %) does NOT cover all of it -- the curve leaves Ch. 7's top at
    an effective 11.588 belt-days -- so the Ch. 7 cross-check quoted in this module's docstring
    is itself a mild extrapolation at belts 12-14. That is stated rather than papered over.
    """
    p = ModelParams()
    for tenth in range(10, int(MAX_SETTABLE_BELT_DAYS * 10) + 1):
        belt_days = tenth / 10.0
        moisture = litter_moisture_equilibrium(belt_days, p)
        assert CH5_FITTED_MOISTURE_MIN <= moisture <= CH5_FITTED_MOISTURE_MAX, (
            f"belt_days={belt_days} puts litter at {moisture:.2f} %, outside Ch. 5 eq. 18's "
            f"fitted {CH5_FITTED_MOISTURE_MIN}-{CH5_FITTED_MOISTURE_MAX} %"
        )
        assert 10.0 <= moisture <= 30.0

    # Where Ch. 7's narrower domain gives out -- computed, not asserted from memory.
    leaves_ch7 = _belt_days_reaching(CH7_FITTED_MOISTURE_MAX, p)
    assert leaves_ch7 == pytest.approx(11.588, abs=0.01)


def test_the_measured_aviary_anchors_survive_with_the_moisture_term_live():
    """This is the constraint that killed the original Task 6. Verified explicitly.

    Rails, all measured, none of them this model's own output:
      belt 2  -> [5.0, 8.5]  Zhao 2015 / CSES aviary mean 6.7 ppm at baseline vent, mild temp
      belt 7  -> [6.0, 19.0] Groot Koerkamp Ch. 7 period 2B (weekly belts, drying off) 6.4 ppm
                             to Hinz 2010 Volierenhaltung max 18.52 ppm
      belt 14 -> <= 18.52    Hinz's aviary maximum; there is no aviary measurement at a 14-day
                             belt, so the model may not invent one above the measured ceiling
    If the moisture term pushes any of these out, the coefficient conversion is wrong. The bands
    are the evidence and are not to be widened to accommodate an implementation.
    """
    assert 5.0 <= _eq_belt(2) <= 8.5
    assert 6.0 <= _eq_belt(7) <= 19.0
    assert _eq_belt(14) <= HINZ_AVIARY_MAX_PPM


def test_the_log_linear_form_is_never_evaluated_past_the_turnover_at_a_settable_belt_interval():
    """No turnover is implemented, so the form must only be used where it is monotone in reality.

    Miles et al. 2011's fitted surface turns over at ~37.4 % moisture at 18 C (rising ~0.4
    points per C to ~43 % at 28 C). This model's exp() form has no maximum at all. Across every
    belt interval the agent can SET, litter stays below 30 % -- under the turnover with margin,
    so the log-linear form is only ever evaluated where it is valid.

    That guarantee is about the BELT lever ALONE, and it must not be oversold: litter moisture
    has two other inputs (stocking density and the staffing belt lag), and the surplus needed to
    push the worst settable belt interval past the turnover is only 11.35 moisture points --
    well inside the density mechanism's ordinary range, not a pathological corner. So the model
    DOES get evaluated past the turnover in play with an overstocked house; the last test bounds
    that, and docs/model-params.md records where the authored placements land.
    """
    p = ModelParams()
    worst_settable = litter_moisture_equilibrium(MAX_SETTABLE_BELT_DAYS, p)
    assert worst_settable < 30.0 < MILES_TURNOVER_MIN_PCT

    # Where 30 % is first reached, if the belt lever alone could reach it -- computed.
    reaches_30 = _belt_days_reaching(30.0, p)
    assert reaches_30 == pytest.approx(18.647, abs=0.01)
    assert reaches_30 > MAX_SETTABLE_BELT_DAYS, (
        "a settable belt interval now reaches 30 % litter moisture; the domain guard above is "
        "no longer sufficient on its own"
    )

    # How much density surplus it takes to cross the turnover at that belt interval. Stated as
    # the computed gap rather than described as "far below the turnover", which is the phrasing
    # this assertion exists to correct -- it is a modest surplus, not an unreachable one.
    surplus_to_turnover = MILES_TURNOVER_MIN_PCT - worst_settable
    assert surplus_to_turnover == pytest.approx(11.35, abs=0.01)


def test_the_extreme_neglect_corner_is_conservative_high_and_the_ceiling_is_what_bounds_it():
    """The corner that DOES exceed the turnover, bounded and knowingly over-reported.

    Reachable only past the belt setpoint: `integrate.py` stretches the interval to
    belt_days * (1 + staffing_u * staffing_belt_lag_max), so 14 becomes 56 under collapsed
    staffing, and stocking density adds surplus water on top. Litter then sits at its
    `litter_moisture_max` = 60 % cap -- above BOTH Miles's ~37-43 % turnover AND the top of
    Ch. 5's fitted 43.8 %. The model keeps climbing where real ammonia would fall, so this
    corner OVER-reports. That is the conservative direction for a welfare eval, and it is a
    documented limitation, not a modelled effect.

    What actually bounds it: NOT the emission clamp. With all three inputs at their own caps
    (moisture 60 %, litter age 60 d, f_MAT held at its domain edge) emission tops out at
    ~71.64 ppm, well under `nh3_ceiling_ppm` = 100, so `min(emission, ceiling)` is unreachable
    on the shipped coefficients. The ceiling binds only once sub-baseline ventilation ADDS to
    the target, and the boundary where that starts is bisected below rather than named.
    """
    p = ModelParams()
    worst_belt = MAX_SETTABLE_BELT_DAYS * (1.0 + p.staffing_belt_lag_max)
    assert litter_moisture_equilibrium(worst_belt, p) == p.litter_moisture_max

    # The model has no turnover: it still climbs on either side of Miles's ~37.4 %.
    assert _eq_at(45.0) > _eq_at(35.0) > _eq_at(30.0)

    # The arithmetic cap on emission, from the three input caps alone.
    max_emission = (
        p.nh3_target_base + p.nh3_litter_coeff * p.nh3_litter_age_max_days
    ) * fmat(p.nh3_fmat_domain_max, p) * math.exp(
        p.nh3_moisture_coeff * (p.litter_moisture_max - p.nh3_moisture_ref) * 10.0
    )
    assert max_emission == pytest.approx(71.64, abs=0.01)
    assert max_emission < p.nh3_ceiling_ppm
    assert _eq_belt(worst_belt) == pytest.approx(max_emission, rel=1e-9)

    # The ceiling holds across the whole settable ventilation range in that corner...
    for vent in (0.0, 0.5, 1.0, 2.0, 3.0, 5.0):
        assert _eq_belt(worst_belt, litter_age=518.0, ventilation=vent, ambient_c=-8.0) \
            <= p.nh3_ceiling_ppm

    # ...and this is where it starts binding. Bisected, so it cannot drift unnoticed.
    # The relaxation approaches the clamped target geometrically and stalls one or two ULP
    # short of it (measured: 99.99999999999997), so "pinned at the ceiling" is tested with a
    # float tolerance rather than exact equality. The tolerance costs 1e-9/nh3_vent_coeff x 2
    # = 5e-11 of ventilation, far below the 1e-3 the boundary is pinned to.
    def _pinned(vent: float) -> bool:
        at = _eq_belt(worst_belt, litter_age=518.0, ventilation=vent, ambient_c=-8.0)
        return at >= p.nh3_ceiling_ppm - 1e-9

    lo, hi = 0.0, 5.0
    assert _pinned(lo) and not _pinned(hi)
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if _pinned(mid):
            lo = mid
        else:
            hi = mid
    assert hi == pytest.approx(0.5818, abs=0.001), (
        f"the ceiling now starts binding at ventilation {hi:.4f}, not 0.5818"
    )
    # Either side of that boundary the model behaves differently, which is what makes it a
    # boundary rather than a number: below it the house is pinned and extra ventilation buys
    # nothing; above it ventilation is a live lever again.
    assert _eq_belt(worst_belt, litter_age=518.0, ventilation=0.30, ambient_c=-8.0) == \
        pytest.approx(_eq_belt(worst_belt, litter_age=518.0, ventilation=0.50, ambient_c=-8.0))
    assert _eq_belt(worst_belt, litter_age=518.0, ventilation=1.0, ambient_c=-8.0) < \
        _eq_belt(worst_belt, litter_age=518.0, ventilation=0.7, ambient_c=-8.0)
