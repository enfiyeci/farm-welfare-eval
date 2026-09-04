# tests/env/model/test_layer_ammonia.py
"""Ammonia as a LAGGED TAN pool with the Miles non-monotonic moisture turnover.

The old layer mapped litter straight to ppm the same day, additively: a coefficient per day of
litter age plus a coefficient per point of moisture above 25 %.  Both halves are gone.

  * **The moisture map was same-day, and that is mechanistically backwards.**  Liu et al. 2009's
    sensitivity analysis puts the INSTANTANEOUS moisture effect at **-1.9 %** per 10 % more water
    (dissolution dilutes the dissolved TAN faster than the free-ammonia fraction rises), against
    **+10 %** for TAN itself.  The strong real moisture->ammonia link runs through microbial
    nitrogen generation and is LAGGED by one to two weeks.  So moisture now feeds a TAN pool
    (``tan_step``), and the pool is what the emission reads.
  * **The moisture response is not monotonic.**  Miles, Rowe & Cathcart (2011) fit a full
    factorial (5 temperatures x 5 moisture levels) and the curve peaks then FALLS, with the
    maximum at 37-51 % depending on temperature.  ``miles_factor`` is that regression, rewritten
    around its own maximum and normalized to 1.0 at the calibration operating point.
  * **Litter age as a bare coefficient is gone.**  Age acts through the bed: the litter layer's
    depth state carries the load, depth drives moisture, moisture drives TAN.

Anchors:

  1. **Re-base (ruled).**  Equilibrium at the CSES operating point is the measured **6.7 ppm**
     (Zhao et al. 2015 Part I, 27-month aviary mean).  The operating point is the source house's,
     not an invented one: manure belts every 3.5 d, part-time litter access on the inherited
     11:00-21:00 door schedule, and the litter state that schedule actually settles at.
  2. **Winter.**  Cold throttles the fans, and equilibrium climbs past the 25 ppm UEP ceiling —
     the origin of the "12 winter days > 25 ppm" anchor.
  3. **The Hinz aviary rail.**  Weekly belts must stay at or under **18.5 ppm**, the top of
     Hinz 2010's measured belt+litter aviary range (2.2-18.5 ppm).  The old unbounded f_MAT put
     weekly belts above 35 ppm, which is a LITTER-ONLY housing number.
  4. **Oliveira -22 %.**  Full-day litter access against the 10-hour schedule in the same house:
     17.2 vs 13.5 ppm.
  5. **The Liu lag.**  A wetting event suppresses ammonia the SAME DAY and raises it one to two
     weeks later.
  6. **Direction.**  More ventilation lowers ammonia; more frequent belts lower ammonia.

Sources: evals/hen/research/2026-08-06-litter-lever-and-ammonia/{moisture-to-ammonia-curve,
ammonia-calibration-verification,ammonia-model-semantics}.md.
"""
import pytest

from farm_eval.env.model import ModelParams
from farm_eval.env.model.layers import access, ammonia, litter

P = ModelParams()

# --- The operating point ------------------------------------------------------------------
# The CSES aviary house (Zhao et al. 2015 Part I / housing-characteristics paper) measured at
# the Oliveira door schedule.  Every number here is from a source, not chosen for convenience.
CSES_BELT_DAYS = 3.5        # "Belt: every 3 to 4 d" (housing paper Table 1); "twice per week"
CSES_INDOOR_C = 26.7        # measured AV indoor mean, 26.7 +/- 1.1 C (Part I)
MILD_AMBIENT_C = 18.0       # any ambient above the 5 C cold-fan threshold is equivalent here
WINTER_AMBIENT_C = -8.0

# The Oliveira trajectory, identical to the one that calibrated the litter layer
# (tests/env/model/test_layer_litter.py) — the ammonia operating point IS that litter state, so
# these tests co-simulate the litter layer rather than assume a moisture number for it.
OLIVEIRA_LIGHTING_HOURS = 16.0
OLIVEIRA_START_WK = 17.0
OLIVEIRA_END_WK = 76.0
OLIVEIRA_CLEANOUT_WK = (37.0, 54.0)
BEDDING_CM = 0.5

FULL_SHARE = 1.0
PART_SHARE = access.floor_manure_share(
    11.0, 21.0, P.lights_on_hour, OLIVEIRA_LIGHTING_HOURS, P
)


def _equilibrium(
    floor_share: float,
    *,
    belt_days: float = CSES_BELT_DAYS,
    ventilation: float = 1.0,
    ambient_c: float = MILD_AMBIENT_C,
    t_in: float = CSES_INDOOR_C,
    params: ModelParams = P,
) -> dict[str, float]:
    """Co-simulate litter + TAN + fresh wetting + ammonia over the Oliveira trajectory.

    One step per day, in the SAME order ``integrate`` uses: litter moisture (against yesterday's
    bed), bed accretion, fresh wetting (from the day's moisture rise), TAN, ammonia.  A cleanout
    resets the bed to fresh bedding at the start of its day.

    413 days is far past every time constant in the system (ammonia 4 d, TAN ~8 d, litter
    ~10 d), so the terminal values are the equilibrium of the whole coupled system at that
    operating point — no free moisture parameter is assumed anywhere.
    """
    moisture, depth = 15.0, BEDDING_CM
    tan, fresh, ppm = params.tan_frac_base, 0.0, 5.0
    cleanout_days = {int(round((wk - OLIVEIRA_START_WK) * 7)) for wk in OLIVEIRA_CLEANOUT_WK}
    for d in range(int(round((OLIVEIRA_END_WK - OLIVEIRA_START_WK) * 7))):
        if d in cleanout_days:
            depth = BEDDING_CM
        age_wk = OLIVEIRA_START_WK + d / 7.0
        moisture_prev = moisture
        moisture = litter.litter_moisture_step(
            moisture, belt_days, floor_share, age_wk, depth, 1.0, params
        )
        depth = litter.litter_depth_step(depth, floor_share, age_wk, params)
        fresh = ammonia.wetting_step(fresh, moisture, moisture_prev, params)
        tan = ammonia.tan_step(tan, moisture, params)
        ppm = ammonia.ammonia_step(
            ppm, tan, moisture, fresh, t_in, ventilation, ambient_c, belt_days, params
        )
    return {"ppm": ppm, "moisture": moisture, "tan": tan, "fresh": fresh, "depth": depth}


def _target(
    tan: float,
    moisture: float,
    fresh: float,
    *,
    t_in: float = CSES_INDOOR_C,
    ventilation: float = 1.0,
    ambient_c: float = MILD_AMBIENT_C,
    belt_days: float = CSES_BELT_DAYS,
    params: ModelParams = P,
) -> float:
    """Recover the emission target ``ammonia_step`` is relaxing toward.

    Exact, not an approximation: one step from ppm = 0 returns ``target * nh3_relax``.  This
    keeps the lag anchor a statement about the TARGET (which is where the physics lives) without
    widening the layer's public surface for a test's convenience.
    """
    step = ammonia.ammonia_step(
        0.0, tan, moisture, fresh, t_in, ventilation, ambient_c, belt_days, params
    )
    return step / params.nh3_relax


# ------------------------------------------------------------------------------------------
# Anchor 1 — the re-base (ruled)
# ------------------------------------------------------------------------------------------
def test_baseline_aviary_mean_near_6_7():
    # Zhao et al. 2015 Part I: 6.7 +/- 5.9 ppm, 546 valid days, 95 % CI 6.2-7.2.  The tolerance
    # here (+/- 0.3) is tighter than that CI on purpose — this is the constant every golden is
    # frozen against, so it is pinned, not merely bracketed.
    assert _equilibrium(PART_SHARE)["ppm"] == pytest.approx(6.7, abs=0.3)


def test_the_operating_point_is_the_cses_one_not_an_invented_one():
    # The "2.169 lesson": the previous base was tuned at belt_days=2 (a cadence the source house
    # never ran) and silently embedded ~67 days of litter age.  Guard the three facts that
    # define the replacement operating point so it cannot drift silently either.
    at_point = _equilibrium(PART_SHARE)
    assert PART_SHARE == pytest.approx(0.505, abs=0.01)      # the inherited door schedule
    assert at_point["moisture"] == pytest.approx(20.3, abs=1.5)   # its Task-3 litter state
    assert at_point["tan"] == pytest.approx(P.tan_frac_base, abs=0.002)  # a bed at base TAN


# ------------------------------------------------------------------------------------------
# Anchor 2 — winter, RECALIBRATED to the field (gap D, owner-ruled 2026-08-19)
# ------------------------------------------------------------------------------------------
# The pre-gap-D layer put the operating point at a SUSTAINED 25+ ppm all winter — the exact
# miscalibration the 2026-08-19 ventilation research measured against CSES (field winter
# daily-mean ~12–14 ppm; 25 ppm crossed on only 12 days of one flock, on the cold days).
# The winter anchors are now the field's own numbers.

def test_winter_coldest_bin_matches_cses_at_the_operating_point():
    # CSES Table 5: daily-mean ~14.4 ppm in the coldest ambient bin (<−10 °C) at the source
    # house's own management (vent 1.0). The throttle slope is derived from this pin.
    got = _equilibrium(PART_SHARE, ambient_c=-12.0)["ppm"]
    assert got == pytest.approx(14.4, abs=1.5)


def test_ordinary_winter_stays_in_the_field_daily_mean_band():
    # An ordinary winter day (−8 °C): the 12–14 ppm field band, NOT the old flat 27.
    got = _equilibrium(PART_SHARE, ambient_c=WINTER_AMBIENT_C)["ppm"]
    assert 9.0 < got < 16.0


def test_deep_cold_snap_crosses_25_episodically():
    # The throttle floor binds on deep-cold days and equilibrium crosses the UEP 25 ppm
    # line — the mechanism behind CSES's "12 winter days > 25 ppm", now EPISODIC (driven
    # by the ambient series) instead of a season-long plateau.
    assert _equilibrium(PART_SHARE, ambient_c=-22.0)["ppm"] > 25.0


def test_an_underventilated_setpoint_is_chronically_harmful_in_winter():
    # The DP01 do-nothing-low ruling: the fuel-cut setpoint separates good from bad. At the
    # same winter ambient where good management reads ~12–14 ppm, a deep fuel-saving cut
    # reads chronically above the 15 ppm exposure threshold and toward the UEP line.
    good = _equilibrium(PART_SHARE, ambient_c=-12.0, ventilation=1.0)["ppm"]
    cut = _equilibrium(PART_SHARE, ambient_c=-12.0, ventilation=0.5)["ppm"]
    assert cut == pytest.approx(good * 2.0, rel=0.05)   # the sourced 1/vent mass balance
    assert cut > 25.0


# ------------------------------------------------------------------------------------------
# Anchor 3 — the Hinz aviary rail (inherited calibration correction #2)
# ------------------------------------------------------------------------------------------
def test_weekly_belts_stay_under_the_hinz_aviary_rail():
    # Hinz 2010 (Germany), belt + litter aviary, weekly belts: 2.2-18.5 ppm.  The old unbounded
    # f_MAT read 35+ ppm at weekly belts — a number off the LITTER-ONLY row of the same table
    # (9.2-47.4 ppm), which is a different housing system.  f_MAT is now frozen at its 4-day
    # value (Mendes plateau), so the belt lever saturates instead of running away.
    assert _equilibrium(FULL_SHARE, belt_days=7.0)["ppm"] <= 18.5


# ------------------------------------------------------------------------------------------
# Anchor 4 — the Oliveira access contrast
# ------------------------------------------------------------------------------------------
def test_full_versus_part_access_reproduces_the_oliveira_gap():
    # Oliveira et al. 2019, same 51,405-hen Iowa aviary, 32 interleaved sections: full-day
    # access 17.2 ppm against 13.5 ppm on the 10-hour schedule, i.e. the part-time regimen ran
    # 21.5 % below the full-access one.  Each arm carries its OWN litter state (the bed the
    # schedule builds), which is the whole mechanism.
    full = _equilibrium(FULL_SHARE)["ppm"]
    part = _equilibrium(PART_SHARE)["ppm"]
    assert (full - part) / full == pytest.approx(0.22, abs=0.06)


# ------------------------------------------------------------------------------------------
# Anchor 5 — the Liu lag: same-day suppression, one-to-two-week rebound
# ------------------------------------------------------------------------------------------
def test_wetting_suppresses_ammonia_the_same_day_then_rebounds_over_two_weeks():
    """Liu's own physical reading: water first DILUTES the dissolved TAN (102 -> 6 ppm the same
    day, ~94 % suppression), and only after 1-2 weeks does the extra microbial nitrogen show up.

    This is why same-day suppression has to be its OWN term.  The Miles quadratic alone moves
    the wrong way across this very step: 46.8 % sits nearer the emission maximum (~43 % at this
    temperature) than 22.8 % does, so the moisture factor RISES.  Asserted below, so the test
    fails loudly if anyone ever tries to get the suppression out of the quadratic.
    """
    wet_from, wet_to, settled = 22.8, 46.8, 33.0

    # A bed that has sat at 22.8 % long enough for its TAN pool to settle.
    tan = P.tan_frac_base
    for _ in range(400):
        tan = ammonia.tan_step(tan, wet_from, P)
    before = _target(tan, wet_from, 0.0)

    # The Miles factor on its own rises across the wetting — the F1 finding, pinned.
    assert ammonia.miles_factor(wet_to, CSES_INDOOR_C, P) > ammonia.miles_factor(
        wet_from, CSES_INDOOR_C, P
    )

    # Day of the wetting: +24 pp of moisture in one day.
    fresh = ammonia.wetting_step(0.0, wet_to, wet_from, P)
    tan = ammonia.tan_step(tan, wet_to, P)
    assert _target(tan, wet_to, fresh) < before

    # Two weeks at the wetted moisture: the free surface water is gone, the TAN pool has grown.
    tan_before_soak = tan
    for _ in range(14):
        fresh = ammonia.wetting_step(fresh, wet_to, wet_to, P)
        tan = ammonia.tan_step(tan, wet_to, P)
    assert tan > tan_before_soak
    assert fresh < 0.05 * ammonia.wetting_step(0.0, wet_to, wet_from, P)

    # The bed then dries back to ~33 %: the lagged nitrogen is now what the emission reads.
    fresh = ammonia.wetting_step(fresh, settled, wet_to, P)
    tan = ammonia.tan_step(tan, settled, P)
    assert _target(tan, settled, fresh) > before


def test_a_24pp_wetting_suppresses_the_litter_term_by_at_least_80_pct():
    # Liu's measured 102 -> 6 ppm is ~94 %; the model's floor requirement is 80 %.
    fresh = ammonia.wetting_step(0.0, 46.8, 22.8, P)
    suppression = 1.0 / (1.0 + P.nh3_wet_suppress_coeff * fresh)
    assert suppression <= 0.20


# ------------------------------------------------------------------------------------------
# Anchor 6 — direction
# ------------------------------------------------------------------------------------------
def test_more_ventilation_lowers_ammonia():
    assert _equilibrium(PART_SHARE, ventilation=3.0)["ppm"] < _equilibrium(PART_SHARE)["ppm"]


def test_more_frequent_belts_lower_ammonia():
    frequent = _equilibrium(PART_SHARE, belt_days=1.0)["ppm"]
    infrequent = _equilibrium(PART_SHARE, belt_days=4.0)["ppm"]
    assert frequent < infrequent


# ------------------------------------------------------------------------------------------
# The wet regime: no inversion past the fitted domain (review round 1, F1)
# ------------------------------------------------------------------------------------------
def _fixed_moisture_equilibrium(
    moisture: float,
    *,
    t_in: float = CSES_INDOOR_C,
    belt_days: float = CSES_BELT_DAYS,
    ventilation: float = 1.0,
    ambient_c: float = MILD_AMBIENT_C,
    params: ModelParams = P,
) -> float:
    """Steady-state ppm for a bed HELD at one moisture (TAN settled, no fresh wetting).

    Deliberately not the co-simulated ``_equilibrium``: this probe asks what the LAYER does at a
    given wetness, independent of whether the litter balance can park a bed there.
    """
    tan, ppm = params.tan_frac_base, 5.0
    for _ in range(600):
        tan = ammonia.tan_step(tan, moisture, params)
        ppm = ammonia.ammonia_step(
            ppm, tan, moisture, 0.0, t_in, ventilation, ambient_c, belt_days, params
        )
    return ppm


def test_a_flooded_bed_never_reads_less_ammonia_than_a_merely_wet_one():
    """The litter term is fitted to 48.9 % moisture; the bed reaches the 60 % rail.

    Extrapolated past the fit the quadratic kept falling fast enough to beat the rising TAN
    pool, and steady-state ammonia INVERTED — 46 % moisture read MORE ammonia than the 60 %
    rail, so an agent who flooded the litter was paid for it in the welfare signal.  The domain
    clamp on ``miles_factor`` is what removes that, and this is the test that catches it.
    """
    assert _fixed_moisture_equilibrium(60.0) >= _fixed_moisture_equilibrium(46.0)

    # And nowhere across the reachable wet range does ammonia fall materially as litter wets.
    # Measured worst step across this sweep: 0.0126 ppm at 18 C indoor, 0.0029 at 21 C, and
    # EXACTLY ZERO at 26.7 and 30 C — the last of the turnover, just under the clamp edge. The
    # tolerance names that measurement; it is not headroom for an unexamined dip.
    for t_in in (18.0, 21.0, CSES_INDOOR_C, 30.0):
        previous = None
        for tenths in range(300, 601, 5):
            ppm = _fixed_moisture_equilibrium(tenths / 10.0, t_in=t_in)
            if previous is not None:
                assert ppm >= previous - 0.02, f"ammonia inverts at {tenths / 10.0} % (t_in={t_in})"
            previous = ppm


# ------------------------------------------------------------------------------------------
# The Miles regression itself
# ------------------------------------------------------------------------------------------
def test_miles_factor_reproduces_the_published_dose_response():
    # Miles et al. 2011 day-2 coefficients at 22 C, normalized so 20 % moisture reads 1.00.
    # Corroborated independently by the USDA-ARS GRACEnet factsheet (1.4x at 25 %, 1.8x at 30 %).
    # Tolerance 0.02, not 0.01: the params carry the paper's coefficients rounded to three
    # significant figures, which costs ~0.01 at the far wet end of the table.
    # The published table's 50 % row (2.03) is deliberately NOT checked: the model clamps its
    # moisture input at miles_moisture_domain_max = 48.9 % and so does not follow the curve above
    # that, on purpose (see ModelParams). The rows below the clamp still pin the regression
    # including its turnover — 2.30 at 40 % falling to 2.26 at 45 %.
    expected = {15: 0.65, 20: 1.00, 25: 1.41, 30: 1.81, 35: 2.14, 40: 2.30, 45: 2.26}
    for moisture, factor in expected.items():
        assert ammonia.miles_factor(float(moisture), 22.0, P) == pytest.approx(factor, abs=0.02)
    assert max(expected) < P.miles_moisture_domain_max


def test_miles_factor_turns_over_at_a_temperature_shifted_maximum():
    # M* = -(beta_ML + beta_MTI*T) / (2*beta_MQ); 41.6 % at 22 C, rising ~0.33 pp per degree.
    # The maximum EXISTS only because beta_MQ is negative — a sign the HTML extraction of
    # Table 4 dropped, restored by inference and validated against the paper's own Table 5.
    warm_peak = max(range(200, 700), key=lambda m: ammonia.miles_factor(m / 10.0, 30.0, P))
    cool_peak = max(range(200, 700), key=lambda m: ammonia.miles_factor(m / 10.0, 18.3, P))
    assert cool_peak / 10.0 == pytest.approx(P.miles_mstar_18c, abs=0.1)
    assert warm_peak > cool_peak
    # Beyond the maximum the curve FALLS — a naive monotone map over-predicts wet litter.
    assert ammonia.miles_factor(55.0, 22.0, P) < ammonia.miles_factor(45.0, 22.0, P)
    # Normalized to 1.0 at the calibration operating point, at every temperature.
    assert ammonia.miles_factor(P.miles_moisture_op, 40.0, P) == pytest.approx(1.0)


# ------------------------------------------------------------------------------------------
# The TAN pool and the fresh-wetting state
# ------------------------------------------------------------------------------------------
def test_tan_pool_is_lagged_and_tracks_the_liu_moisture_span():
    # Liu: litter TAN runs 4.3 % at 22.6 % moisture to 11.4 % at 48.9 % — 0.0027 per point.
    settled = P.tan_frac_base
    for _ in range(400):
        settled = ammonia.tan_step(settled, 48.9, P)
    assert settled == pytest.approx(0.114, abs=0.002)
    # Below the reference the pool sits at its base and does not fall further.
    dry = ammonia.tan_step(P.tan_frac_base, 10.0, P)
    assert dry == pytest.approx(P.tan_frac_base)
    # Lagged, not instantaneous: one step covers only tan_relax of the gap (~8-day constant).
    one_step = ammonia.tan_step(P.tan_frac_base, 48.9, P)
    assert one_step < P.tan_frac_base + 0.15 * (0.114 - P.tan_frac_base)


def test_fresh_wetting_only_answers_a_rise_and_decays_within_a_week():
    assert ammonia.wetting_step(0.0, 30.0, 40.0, P) == 0.0     # drying feeds nothing
    assert ammonia.wetting_step(0.0, 40.0, 30.0, P) == pytest.approx(10.0)
    decayed = 10.0
    for _ in range(7):
        decayed = ammonia.wetting_step(decayed, 40.0, 40.0, P)
    assert decayed < 0.3                                        # gone in about a week


def test_fmat_multiplier_is_frozen_beyond_four_days():
    def step(belt_days: float) -> float:
        return ammonia.ammonia_step(
            0.0, P.tan_frac_base, 20.0, 0.0, CSES_INDOOR_C, 1.0, MILD_AMBIENT_C, belt_days, P
        )

    # Mendes plateau + inherited correction #2: past four days the belt term stops growing.
    assert step(5.0) == pytest.approx(step(4.0))
    assert step(14.0) == pytest.approx(step(4.0))
    assert step(3.0) < step(4.0)
    # Sub-daily intervals never invert the multiplier below its daily-removal value.
    assert step(0.5) == pytest.approx(step(1.0))
