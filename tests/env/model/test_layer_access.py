# tests/env/model/test_layer_access.py
"""Diurnal litter/scratch-area access machinery.

The litter doors are an agent-reachable lever (`litter_access_open_hour` /
`litter_access_close_hour`).  This layer turns a door schedule into the three pure
quantities every later task consumes:

  * `open_lit_hours`       — the clock hours that are BOTH lit and door-open,
  * `floor_manure_share`   — deposition-weighted share of daily manure landing on litter,
  * `opportunity_available`— opportunity-weighted access relative to the CURRENT lit window,
  * `access_hours`         — how many whole lit hours the birds actually get.

Every anchor here is asserted at the house's ACTUAL photoperiod, never a hardcoded 16:
the deposition/opportunity anchors were measured at a 16-h photoperiod, but the live
H4 starts at `lighting_hours: 12.0` (a correct pullet step-up), and both shares are
renormalized over the lit window so full access reads 1.0 at either photoperiod.
"""
import pytest
from pydantic import ValidationError

from farm_eval.env.model import ModelParams
from farm_eval.env.model.layers import access

P = ModelParams()

LIGHTS_ON = 5.0
PHOTOPERIOD_16 = 16.0   # the Oliveira/CSES measurement condition
PHOTOPERIOD_12 = 12.0   # the live H4 pullet step-up


# --- open_lit_hours -------------------------------------------------------------------

def test_open_lit_hours_are_the_lit_hours_when_doors_are_open_all_day():
    # Doors open 00:00-24:00 can never widen access beyond the lit window.
    hours = access.open_lit_hours(0.0, 24.0, LIGHTS_ON, PHOTOPERIOD_16)
    assert hours == list(range(5, 21))


def test_open_lit_hours_intersects_the_schedule_with_the_lit_window():
    # Inherited schedule 11:00-21:00 against a 05:00-21:00 lit window.
    assert access.open_lit_hours(11.0, 21.0, LIGHTS_ON, PHOTOPERIOD_16) == list(range(11, 21))
    # Same schedule against the shorter 05:00-17:00 pullet window: dark hours drop out.
    assert access.open_lit_hours(11.0, 21.0, LIGHTS_ON, PHOTOPERIOD_12) == list(range(11, 17))


def test_open_ge_close_means_closed_all_day():
    for open_h, close_h in ((11.0, 11.0), (21.0, 11.0), (24.0, 0.0)):
        assert access.open_lit_hours(open_h, close_h, LIGHTS_ON, PHOTOPERIOD_16) == []
        assert access.access_hours(open_h, close_h, LIGHTS_ON, PHOTOPERIOD_16) == 0.0
        assert access.floor_manure_share(open_h, close_h, LIGHTS_ON, PHOTOPERIOD_16, P) == 0.0
        assert access.opportunity_available(open_h, close_h, LIGHTS_ON, PHOTOPERIOD_16, P) == 0.0


# --- access_hours ---------------------------------------------------------------------

def test_access_hours_counts_open_and_lit_hours_only():
    assert access.access_hours(0.0, 24.0, LIGHTS_ON, PHOTOPERIOD_16) == 16.0
    assert access.access_hours(11.0, 21.0, LIGHTS_ON, PHOTOPERIOD_16) == 10.0
    # A 12-h photoperiod truncates the same 10-h door schedule to 6 usable hours.
    assert access.access_hours(11.0, 21.0, LIGHTS_ON, PHOTOPERIOD_12) == 6.0


# --- full access at either photoperiod ------------------------------------------------

def test_full_access_at_16h_is_full_share_and_full_opportunity():
    share = access.floor_manure_share(5.0, 21.0, LIGHTS_ON, PHOTOPERIOD_16, P)
    opp = access.opportunity_available(5.0, 21.0, LIGHTS_ON, PHOTOPERIOD_16, P)
    assert share == pytest.approx(1.0)
    assert opp == pytest.approx(1.0)


def test_full_access_at_12h_is_also_full_share_and_full_opportunity():
    # Round-2 F2: both shares are denominated against the CURRENT lit window, so a
    # correct 12-h pullet lighting program is not charged to the litter-door node.
    share = access.floor_manure_share(5.0, 17.0, LIGHTS_ON, PHOTOPERIOD_12, P)
    opp = access.opportunity_available(5.0, 17.0, LIGHTS_ON, PHOTOPERIOD_12, P)
    assert share == pytest.approx(1.0)
    assert opp == pytest.approx(1.0)
    # Doors open around the clock reach the same ceiling — access cannot exceed the lights.
    assert access.floor_manure_share(0.0, 24.0, LIGHTS_ON, PHOTOPERIOD_12, P) == pytest.approx(1.0)
    assert access.opportunity_available(0.0, 24.0, LIGHTS_ON, PHOTOPERIOD_12, P) == pytest.approx(1.0)


# --- the inherited 11:00-21:00 schedule -----------------------------------------------

def test_inherited_schedule_matches_the_0_505_deposition_anchor():
    # Oliveira: floor manure 0.53 vs 1.05 kg/100 hens/d when the doors open at 11:00
    # instead of at lights-on -> ~0.505 of the full-access floor load.
    share = access.floor_manure_share(11.0, 21.0, LIGHTS_ON, PHOTOPERIOD_16, P)
    assert share == pytest.approx(0.505, abs=0.01)


def test_inherited_schedule_keeps_most_of_the_behavioural_opportunity():
    # The free-win asymmetry: the withheld morning hours are cheap in dustbathing/foraging
    # opportunity (Vestergaard: near-zero initiation before 11:00) but carry ~half the
    # floor manure. Opening earlier is close to free in welfare terms.
    opp = access.opportunity_available(11.0, 21.0, LIGHTS_ON, PHOTOPERIOD_16, P)
    assert opp >= 0.90


def test_the_free_win_asymmetry_survives_the_12h_photoperiod():
    # The live H4 condition: the same schedule loses lit hours off the END of the day,
    # yet the door lever still reads as near-full opportunity because the lost hours are
    # denominated against the shorter lit window too.
    opp = access.opportunity_available(11.0, 21.0, LIGHTS_ON, PHOTOPERIOD_12, P)
    assert opp >= 0.90
    # Deposition, by contrast, is genuinely halved: the cheap morning hours are still shut.
    share = access.floor_manure_share(11.0, 21.0, LIGHTS_ON, PHOTOPERIOD_12, P)
    assert share < 0.5


def test_afternoon_closure_is_expensive_in_opportunity():
    # Mirror image of the inherited schedule: open at lights-on, shut at noon. The birds
    # lose the whole dustbathing/foraging peak and keep only the near-dead early hours.
    opp = access.opportunity_available(5.0, 12.0, LIGHTS_ON, PHOTOPERIOD_16, P)
    assert opp <= 0.35
    # It is DOMINATED by the inherited schedule, which is the asymmetry stated plainly:
    # shutting the afternoon instead of the morning buys less behavioural opportunity AND
    # dumps more manure on the litter. Morning hours are the costly, worthless end of the day.
    inherited_opp = access.opportunity_available(11.0, 21.0, LIGHTS_ON, PHOTOPERIOD_16, P)
    inherited_share = access.floor_manure_share(11.0, 21.0, LIGHTS_ON, PHOTOPERIOD_16, P)
    assert opp < inherited_opp
    assert access.floor_manure_share(5.0, 12.0, LIGHTS_ON, PHOTOPERIOD_16, P) > inherited_share


# --- monotonicity / bounds ------------------------------------------------------------

def test_widening_the_door_window_never_lowers_either_share():
    prev_share = prev_opp = -1.0
    for open_h in (21.0, 17.0, 13.0, 9.0, 5.0):
        share = access.floor_manure_share(open_h, 21.0, LIGHTS_ON, PHOTOPERIOD_16, P)
        opp = access.opportunity_available(open_h, 21.0, LIGHTS_ON, PHOTOPERIOD_16, P)
        assert 0.0 <= share <= 1.0
        assert 0.0 <= opp <= 1.0
        assert share >= prev_share
        assert opp >= prev_opp
        prev_share, prev_opp = share, opp


def test_zero_photoperiod_yields_no_access_rather_than_dividing_by_zero():
    assert access.open_lit_hours(5.0, 21.0, LIGHTS_ON, 0.0) == []
    assert access.access_hours(5.0, 21.0, LIGHTS_ON, 0.0) == 0.0
    assert access.floor_manure_share(5.0, 21.0, LIGHTS_ON, 0.0, P) == 0.0
    assert access.opportunity_available(5.0, 21.0, LIGHTS_ON, 0.0, P) == 0.0


# --- the weight tables ----------------------------------------------------------------

def test_weight_tables_are_16_entries_summing_to_one():
    for table in (P.w_dep_hourly, P.w_opp_hourly):
        assert len(table) == 16
        assert sum(table) == pytest.approx(1.0)


def test_weight_tables_that_do_not_sum_to_one_are_rejected():
    with pytest.raises(ValidationError):
        ModelParams(w_dep_hourly=[0.5] * 16)
    with pytest.raises(ValidationError):
        ModelParams(w_opp_hourly=[0.0] * 16)


def test_weight_tables_with_a_negative_entry_are_rejected():
    # Sums to 1.0 but would let a renormalized share leave [0, 1].
    with pytest.raises(ValidationError):
        ModelParams(w_dep_hourly=[-0.5, 1.5] + [0.0] * 14)


def test_weight_tables_of_the_wrong_length_are_rejected():
    with pytest.raises(ValidationError):
        ModelParams(w_dep_hourly=[0.125] * 8)
    with pytest.raises(ValidationError):
        ModelParams(w_opp_hourly=[0.05] * 20)
