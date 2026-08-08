# tests/env/model/test_layer_litter.py
"""Litter as a WATER BALANCE: bounded belt equilibrium + a floor-manure source term,
mediated by accumulated bed depth, with caking as a depth x wetness product.

The old layer relaxed litter moisture toward a belt-frequency curve that reached ~45 % at
weekly belts.  That curve is gone (inherited calibration correction #1): Groot Koerkamp's
ch.-7 aviary band puts the belt-regime span at roughly 14.4-20.6 % moisture, and the large
moisture contrasts Oliveira measured come from the ACCESS lever through accumulated depth,
not from the belts.  See
evals/hen/research/2026-08-07-litter-prep/ and
evals/hen/research/2026-08-06-litter-lever-and-ammonia/litter-access-dose-response.md.

Anchors (all evaluated at the Oliveira 16-h photoperiod, belt interval 3.5 d, at 76 weeks
of age, on a trajectory that reproduces the whole-house litter removals at 37/38 and
54/55 WOA):

    quantity            full access (share 1.0)   part access (11:00-21:00, share 0.505)
    litter moisture     31.3 +/- 1.5 %            20.3 +/- 1.5 %
    bed depth            3.77 +/- 0.5 cm           1.64 +/- 0.4 cm
    caked share         33 +/- 8 %                 0 %

Source: Oliveira et al. 2019, Poult. Sci. 98:1664-1677 (same house, 32 interleaved
sections, 14 months).
"""
import pytest

from farm_eval.env.model import ModelParams
from farm_eval.env.model.layers import access, litter

P = ModelParams()

# --- The Oliveira measurement condition -------------------------------------------------
OLIVEIRA_LIGHTING_HOURS = 16.0   # lights 05:00-21:00
OLIVEIRA_BELT_DAYS = 3.5         # CSES-cadence manure-belt interval
OLIVEIRA_START_WK = 17.0         # hens transferred at 17 wk, litter given ~then
OLIVEIRA_END_WK = 76.0           # final sampling age
OLIVEIRA_CLEANOUT_WK = (37.0, 54.0)   # whole-house litter removals; BOTH arms reset
BEDDING_CM = 0.5                 # fresh bedding depth after a cleanout

FULL_SHARE = 1.0
PART_SHARE = access.floor_manure_share(
    11.0, 21.0, P.lights_on_hour, OLIVEIRA_LIGHTING_HOURS, P
)


def _trajectory(
    floor_share: float,
    params: ModelParams = P,
    *,
    start_wk: float = OLIVEIRA_START_WK,
    end_wk: float = OLIVEIRA_END_WK,
    cleanouts: tuple[float, ...] = OLIVEIRA_CLEANOUT_WK,
    moisture0: float = 15.0,
    depth0: float = BEDDING_CM,
    belt_days: float = OLIVEIRA_BELT_DAYS,
) -> tuple[float, float, float]:
    """Run the deterministic Oliveira calibration trajectory; return (moisture, depth, caked).

    One step per day.  A cleanout resets the bed to fresh bedding at the START of its day —
    the measured depth pair is depth accumulated SINCE the ~54-WOA removal, which is why the
    trajectory has to model the resets rather than run bedding-to-76-WOA uncut.
    """
    moisture, depth = moisture0, depth0
    cleanout_days = {int(round((wk - start_wk) * 7)) for wk in cleanouts}
    for d in range(int(round((end_wk - start_wk) * 7))):
        if d in cleanout_days:
            depth = depth0
        age_wk = start_wk + d / 7.0
        moisture = litter.litter_moisture_step(
            moisture, belt_days, floor_share, age_wk, depth, 1.0, params
        )
        depth = litter.litter_depth_step(depth, floor_share, age_wk, params)
    return moisture, depth, litter.caked_pct(moisture, depth, params)


# ---------------------------------------------------------------------------------------
# The measurement condition itself
# ---------------------------------------------------------------------------------------
def test_part_access_share_is_the_oliveira_deposition_anchor():
    # The part-access arm is the inherited 11:00-21:00 door schedule read through the Task-2
    # access layer at Oliveira's 16-h photoperiod — not a hardcoded number.
    assert PART_SHARE == pytest.approx(0.505, abs=0.01)


# ---------------------------------------------------------------------------------------
# Anchor pair 1 — litter moisture
# ---------------------------------------------------------------------------------------
def test_full_access_moisture_matches_the_31_3_anchor():
    moisture, _, _ = _trajectory(FULL_SHARE)
    assert moisture == pytest.approx(31.3, abs=1.5)


def test_part_access_moisture_matches_the_20_3_anchor():
    moisture, _, _ = _trajectory(PART_SHARE)
    assert moisture == pytest.approx(20.3, abs=1.5)


# ---------------------------------------------------------------------------------------
# Anchor pair 2 — bed depth (reachable only with the share exponent; Codex plan-review F7)
# ---------------------------------------------------------------------------------------
def test_full_access_depth_matches_the_3_77_anchor():
    _, depth, _ = _trajectory(FULL_SHARE)
    assert depth == pytest.approx(3.77, abs=0.5)


def test_part_access_depth_matches_the_1_64_anchor():
    # A LINEAR share term cannot reach this: share 0.505 would force a depth ratio of 0.505
    # (~2.15 cm) against the measured 1.64/3.77 = 0.435.  The exponent is what lands it.
    _, depth, _ = _trajectory(PART_SHARE)
    assert depth == pytest.approx(1.64, abs=0.4)
    assert P.litter_depth_share_exp > 1.0


# ---------------------------------------------------------------------------------------
# Anchor pair 3 — caking
# ---------------------------------------------------------------------------------------
def test_full_access_caking_matches_the_33_pct_anchor():
    _, _, caked = _trajectory(FULL_SHARE)
    assert caked == pytest.approx(33.0, abs=8.0)


def test_part_access_litter_does_not_cake():
    _, _, caked = _trajectory(PART_SHARE)
    assert caked == 0.0


# ---------------------------------------------------------------------------------------
# The convergence property (Oliveira end-of-trial P = 0.57)
# ---------------------------------------------------------------------------------------
def test_moisture_gap_collapses_after_a_cleanout_at_equal_access():
    # Oliveira's two regimens were statistically indistinguishable at the final sampling.
    # The mechanism is depth: strip both beds back to bedding, run them at the SAME access,
    # and the 11-pp gap has to disappear — it lived in the bed, not in the hours.
    m_full, _, _ = _trajectory(FULL_SHARE)
    m_part, _, _ = _trajectory(PART_SHARE)
    assert m_full - m_part > 8.0          # the gap really is there before the cleanout

    depth_a = depth_b = BEDDING_CM
    for _ in range(30):
        m_full = litter.litter_moisture_step(
            m_full, OLIVEIRA_BELT_DAYS, FULL_SHARE, OLIVEIRA_END_WK, depth_a, 1.0, P
        )
        m_part = litter.litter_moisture_step(
            m_part, OLIVEIRA_BELT_DAYS, FULL_SHARE, OLIVEIRA_END_WK, depth_b, 1.0, P
        )
        depth_a = litter.litter_depth_step(depth_a, FULL_SHARE, OLIVEIRA_END_WK, P)
        depth_b = litter.litter_depth_step(depth_b, FULL_SHARE, OLIVEIRA_END_WK, P)
    assert abs(m_full - m_part) < 2.0


# ---------------------------------------------------------------------------------------
# The belt-regime rail (inherited calibration correction #1)
# ---------------------------------------------------------------------------------------
def _belt_only_equilibrium(belt_days: float) -> float:
    """Fixed point of the moisture step with NO floor-manure source term."""
    m = 25.0
    for _ in range(1000):
        m = litter.litter_moisture_step(m, belt_days, 0.0, 40.0, 0.0, 1.0, P)
    return m


def test_belt_regime_stays_inside_the_groot_koerkamp_band():
    # GK ch. 7: the whole belt-frequency span of an aviary litter bed lives in ~14.4-20.6 %.
    # The old curve put weekly belts at 45 %, which is a FLOOR-HOUSING number — the error
    # this rewrite corrects (evals/hen/research/2026-08-07-litter-prep/).
    for belt_days in (1, 2, 3, 4, 5, 7, 10, 14):
        eq = _belt_only_equilibrium(belt_days)
        assert 14.4 <= eq <= 20.6, f"belt_days={belt_days} equilibrium {eq:.2f} outside band"


def test_belt_equilibrium_is_capped_and_monotone():
    eqs = [litter.belt_equilibrium(b, P) for b in (1, 2, 3, 4, 5, 6, 7, 10, 14)]
    assert eqs == sorted(eqs)
    assert eqs[0] == pytest.approx(P.litter_moisture_belt_floor)
    assert max(eqs) <= P.litter_moisture_belt_cap + 1e-9
    # Sub-daily belt intervals are meaningless; the floor is the driest the belts can get.
    assert litter.belt_equilibrium(0.1, P) == pytest.approx(P.litter_moisture_belt_floor)


# ---------------------------------------------------------------------------------------
# The age (water-flow) curve — GK ch. 8
# ---------------------------------------------------------------------------------------
def test_water_rel_peaks_at_22_weeks_and_collapses_by_30():
    assert litter.water_rel(22.0, P) == pytest.approx(1.0)
    # ~45 g/hen/day at 20-22 wk falling to ~7 g/hen/day by 30 wk: a ~6x behavioural swing,
    # bigger than the access-hours effect (GK ch. 8).
    assert litter.water_rel(30.0, P) == pytest.approx(7.0 / 45.0, abs=1e-6)
    assert litter.water_rel(76.0, P) == pytest.approx(litter.water_rel(30.0, P))
    assert litter.water_rel(17.0, P) < 1.0     # pre-lay, below the peak
    assert litter.water_rel(26.0, P) < 1.0     # post-peak decline


# ---------------------------------------------------------------------------------------
# Direction, bounds and monotonicity
# ---------------------------------------------------------------------------------------
def test_more_floor_access_means_wetter_litter_and_a_deeper_bed():
    m_full, d_full, c_full = _trajectory(FULL_SHARE)
    m_part, d_part, c_part = _trajectory(PART_SHARE)
    assert m_full > m_part
    assert d_full > d_part
    assert c_full > c_part


def test_step_moves_toward_equilibrium_from_both_sides():
    # A wet bed under full access keeps wetting; the same bed with the doors shut dries out.
    up = litter.litter_moisture_step(20.0, 7, FULL_SHARE, 76.0, 3.77, 1.0, P)
    assert up > 20.0
    down = litter.litter_moisture_step(40.0, 1, 0.0, 76.0, 3.77, 1.0, P)
    assert down < 40.0


def test_step_does_not_leave_bounds():
    for belt_days in (1, 2, 4, 7):
        for share in (0.0, PART_SHARE, 1.0):
            m = litter.litter_moisture_step(0.0, belt_days, share, 22.0, 10.0, 1.0, P)
            assert 0.0 <= m <= P.litter_moisture_max
            m = litter.litter_moisture_step(100.0, belt_days, share, 22.0, 10.0, 1.0, P)
            assert 0.0 <= m <= P.litter_moisture_max


def test_depth_never_decreases_and_shut_doors_stop_accretion():
    assert litter.litter_depth_step(2.0, 0.0, 22.0, P) == pytest.approx(2.0)
    assert litter.litter_depth_step(2.0, 1.0, 22.0, P) > 2.0
    # Accretion is fastest at the 22-wk water-flow peak, slowest in late lay.
    young = litter.litter_depth_step(2.0, 1.0, 22.0, P) - 2.0
    old = litter.litter_depth_step(2.0, 1.0, 76.0, P) - 2.0
    assert young > old > 0.0


def test_caking_needs_both_wetness_and_depth_and_is_clamped():
    assert litter.caked_pct(24.0, 3.77, P) == 0.0            # dry litter never cakes
    assert litter.caked_pct(40.0, 0.0, P) == 0.0             # a bare floor has nothing to cake
    assert litter.caked_pct(60.0, 10.0, P) <= P.litter_cake_max_pct
    assert litter.caked_pct(35.0, 3.77, P) > litter.caked_pct(30.0, 3.77, P)
    assert litter.caked_pct(35.0, 3.77, P) > litter.caked_pct(35.0, 1.5, P)


def test_density_factor_scales_the_floor_source_term():
    # Task 7 wires real density here; until then integrate passes 1.0.  The term must be a
    # clean multiplier so that lever lands without touching this layer's calibration.
    base = litter.floor_moisture_excess(1.0, 76.0, 3.77, 1.0, P)
    assert litter.floor_moisture_excess(1.0, 76.0, 3.77, 2.0, P) == pytest.approx(2.0 * base)
    assert litter.floor_moisture_excess(1.0, 76.0, 3.77, 0.0, P) == 0.0
