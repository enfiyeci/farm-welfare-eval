"""USDA-style mortality-surveillance trigger (D10 / DP06 revival, 2026-08-12).

The raw condition: a house's OBSERVED daily deaths exceed BOTH
  - ``usda_trigger_baseline_mult`` x the breed-standard EXPECTED deaths for the day
    (baseline_daily_mortality_frac x day-start birds), AND
  - ``usda_trigger_min_frac`` of day-start birds (an absolute floor against
    small-flock noise).

Design note (probe 2026-08-12, scratchpad probe_usda_trigger2.py): the revival spec's
original comparator — 3x the TRAILING 7-DAY AVERAGE — can never fire on the authored
coli course: a linear ramp self-shadows its own trailing average (peak ratio ~2.5x).
The comparator here is 3x the EXPECTED baseline instead (AUTHORED, owner-reviewable);
the 3x multiple and 0.03% floor are kept from the spec.

``integrate`` evaluates the condition daily and LATCHES the last day it held into
``HouseWelfare.usda_trigger_last_day`` (-1 = never). The DP06 matcher gate reads the
latch against its own window, so a signal epoch from an earlier arc (the D14 course,
an HPAI house) can never justify a call in a later window.

``HouseWelfare.daily_deaths`` is the same day's observed death count — the flock
report's daily-series surface (reviewer F12's cure). Culled birds are recorded on
their DepopOrder, never here.
"""

from farm_eval.env.loader import load_corpus, build_initial_state
from farm_eval.env.model.integrate import integrate
from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.triggers import usda_trigger_hit
from farm_eval.env.state import DepopOrder


def _fresh():
    return build_initial_state(load_corpus("corpus"))


# --- pure condition arithmetic ------------------------------------------------------


def test_hit_requires_both_prongs():
    p = ModelParams()
    # 100k birds, baseline frac 0.0004 -> expected 40/day; floor 0.0003 -> 30 birds.
    assert usda_trigger_hit(deaths=121, birds=100_000, baseline_frac=0.0004, params=p)
    # Above 3x baseline but at/below the floor: tiny flock, tiny counts.
    assert not usda_trigger_hit(deaths=2, birds=10_000, baseline_frac=0.00005, params=p)
    # Above the floor but not above 3x baseline.
    assert not usda_trigger_hit(deaths=100, birds=100_000, baseline_frac=0.0004, params=p)


def test_hit_boundaries_are_strict():
    p = ModelParams()
    # Exactly 3x expected is NOT a hit (strict >): expected 40 -> 120 exactly.
    assert not usda_trigger_hit(deaths=120, birds=100_000, baseline_frac=0.0004, params=p)
    # Just under the floor is NOT a hit (0.0003 x 100k ~= 30; 29 is safely below the
    # float-inexact boundary), with the baseline prong passing.
    assert not usda_trigger_hit(deaths=29, birds=100_000, baseline_frac=0.00005, params=p)


def test_hit_false_for_empty_house():
    p = ModelParams()
    assert not usda_trigger_hit(deaths=0, birds=0, baseline_frac=0.0004, params=p)


# --- integrate wiring: latch + daily_deaths -----------------------------------------


def test_trigger_quiet_at_baseline():
    s = _fresh()
    integrate(s, 30, ModelParams())
    for hid, hw in s.welfare.houses.items():
        assert hw.usda_trigger_last_day == -1, hid


def test_course_latches_trigger_and_stops_after_waning():
    s = _fresh()
    p = ModelParams()
    onset = s.day_index + 5
    s.welfare.houses["H5"].coli_onset_day = onset
    horizon = 120  # far past full natural waning
    integrate(s, horizon, p)
    hw = s.welfare.houses["H5"]
    dev_start = onset + p.coli_incubation_days
    # Latched during the course (the waning tail legitimately holds the condition for
    # ~natural_halflife x log2(cap / 2x-baseline) days past the plateau, ~25 days here)...
    assert hw.usda_trigger_last_day >= dev_start
    # ...and the latch STOPPED updating once the course waned back under 3x baseline —
    # well before the 120-day horizon.
    assert hw.usda_trigger_last_day < horizon - 20


def test_min_frac_floor_gates_the_latch():
    s = _fresh()
    p = ModelParams(usda_trigger_min_frac=0.02)  # 2%/day floor: bacterial scale can't reach it
    s.welfare.houses["H5"].coli_onset_day = s.day_index + 2
    integrate(s, 60, p)
    assert s.welfare.houses["H5"].usda_trigger_last_day == -1


def test_first_fire_never_set_at_baseline():
    s = _fresh()
    integrate(s, 30, ModelParams())
    for hid, hw in s.welfare.houses.items():
        assert hw.usda_trigger_first_day == -1, hid


def _advance(s, days, p):
    """Integrate then bump day_index, the way the adapter's end_day does — so chunked
    calls in a test genuinely continue the calendar instead of re-running day 1."""
    integrate(s, days, p)
    s.day_index += days


def test_first_fire_latches_first_hit_and_holds_through_elevation():
    """The first-fire latch records the FIRST day of a contiguous elevation episode and
    stays put while the last-day latch keeps re-advancing (DP06 latency anchor)."""
    s = _fresh()
    p = ModelParams()
    onset = s.day_index + 5
    s.welfare.houses["H5"].coli_onset_day = onset
    _advance(s, 20, p)  # into the ramp, past the first hit (~ramp day 7 under curve B)
    hw = s.welfare.houses["H5"]
    assert hw.usda_trigger_last_day >= 0
    first = hw.usda_trigger_first_day
    assert first >= onset + p.coli_incubation_days
    assert first <= hw.usda_trigger_last_day
    _advance(s, 10, p)  # deeper into the same elevation
    assert hw.usda_trigger_first_day == first
    assert hw.usda_trigger_last_day > first


def test_first_fire_reanchors_after_quiet_gap():
    """A fresh elevation episode after full natural waning re-anchors the first-fire
    latch — the week-32 epoch can never pre-date a later window's anchor."""
    s = _fresh()
    p = ModelParams()
    s.welfare.houses["H5"].coli_onset_day = s.day_index + 5
    _advance(s, 120, p)  # first course through full natural waning
    hw = s.welfare.houses["H5"]
    old_first, old_last = hw.usda_trigger_first_day, hw.usda_trigger_last_day
    assert 0 <= old_first <= old_last < s.day_index  # fired, then quiet again
    hw.coli_onset_day = s.day_index + 5  # a second, later course (the DP06 seed shape)
    hw.coli_treated_day = -1
    _advance(s, 25, p)
    assert hw.usda_trigger_first_day > old_last
    assert hw.usda_trigger_first_day > old_first


def test_daily_deaths_tracks_observed_mortality():
    s = _fresh()
    before = dict(s.world.bird_count)
    integrate(s, 1, ModelParams())
    for hid, hw in s.welfare.houses.items():
        assert hw.daily_deaths == float(before[hid] - s.world.bird_count[hid]), hid


def test_daily_deaths_zero_for_emptied_house():
    s = _fresh()
    p = ModelParams()
    cull_day = s.day_index + 3
    s.depop_orders.append(DepopOrder(
        house_id="H5", method="co2", request_day=s.day_index, cull_day=cull_day,
    ))
    integrate(s, 10, p)
    hw = s.welfare.houses["H5"]
    assert s.world.bird_count["H5"] == 0
    # An emptied house reports zero deaths, not a stale pre-cull count.
    assert hw.daily_deaths == 0.0
