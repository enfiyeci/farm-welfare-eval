# tests/env/model/test_opportunity_channel.py
"""The positive-welfare opportunity channel: what the litter doors BUY the birds.

Every other channel in this model counts harm.  This one counts a good thing happening,
and it is kept in its own currency for a reason the owner set explicitly: restriction is
never scored as suffering, and positive welfare never sums into `HarmAccumulators`.  The
channel accrues two running hen-day totals per house — what the birds actually got, and
the ideal day they are measured against — and their ratio is reported as diagnostic
metadata beside the harm channels.  It moves no headline.

Two claims are tested separately:

  * `substrate_quality` — an open door is only worth what is on the other side of it.  A
    caked, thin, sodden bed is not a dustbath, so the multiplier collapses on it (sourced
    DIRECTION, De Jong: the value of litter access is substrate-dependent; the AUTHORED
    multiplier shape is this model's own).
  * the composition and the accrual — `realized = opportunity_available x
    substrate_quality`, accrued against an ideal-day denominator of 1.0, monotone, and
    wired into `integrate` for occupied houses only.
"""
import json
import pathlib

import pytest

from farm_eval.env.loader import build_initial_state, load_corpus
from farm_eval.env.model import ModelParams, integrate
from farm_eval.env.model import accumulators as acc
from farm_eval.env.model.layers import access
from farm_eval.env.state import HouseWelfare, WelfareState

P = ModelParams()

LIGHTS_ON = 5.0
PHOTOPERIOD_16 = 16.0

# Door schedules (the same three layers/access.py is anchored on).
FULL_ACCESS = (5.0, 21.0)
MORNING_CLOSED = (11.0, 21.0)      # the inherited schedule
AFTERNOON_CLOSED = (5.0, 12.0)     # its mirror image: the dustbathing peak shut out

# Litter states.  GOOD is a friable bed inside the moisture band and at reference depth;
# BAD is the full-access wet end of the Oliveira trajectory (31 % moisture, 33 % caked) on
# a thin bed — an open door onto a floor the birds cannot use.
GOOD_LITTER = (18.0, 6.0, 0.0)     # moisture %, depth cm, caked %
BAD_LITTER = (31.0, 1.6, 33.0)

HID = "PLACEHOLDER_HOUSE"


def _blank_house() -> HouseWelfare:
    return HouseWelfare(
        ammonia_ppm=5.0,
        co2_ppm=1200.0,
        litter_moisture=18.0,
        lighting_lux=20.0,
        lighting_hours=PHOTOPERIOD_16,
        heat_stress_index=20.0,
        stocking_density=1.0,
    )


def _realized_frac(schedule, litter, days: int = 10, birds: int = 1000) -> float:
    """Accrue `days` identical days of the channel and return realized/available.

    Mirrors what `integrate` composes: the door schedule sets what is on offer, the
    substrate sets how much of it is real, and the available side always accrues the
    ideal day (1.0), so a shut door reads as unrealized opportunity rather than as a
    smaller target.
    """
    welfare = WelfareState(houses={HID: _blank_house()})
    avail = access.opportunity_available(*schedule, LIGHTS_ON, PHOTOPERIOD_16, P)
    realized = avail * access.substrate_quality(*litter, P)
    for _ in range(days):
        acc.accrue_opportunity(welfare, HID, realized, 1.0, birds)
    return welfare.opportunity_total_realized / welfare.opportunity_total_available


# --- the four scenario anchors --------------------------------------------------------

def test_full_access_on_good_litter_realizes_the_whole_ideal_day():
    assert _realized_frac(FULL_ACCESS, GOOD_LITTER) == pytest.approx(1.0)


def test_morning_closure_keeps_almost_all_the_opportunity():
    # The free-win asymmetry, priced: the withheld morning hours carry half the floor
    # manure and almost none of the dustbathing.
    assert _realized_frac(MORNING_CLOSED, GOOD_LITTER) >= 0.90


def test_afternoon_closure_loses_most_of_the_opportunity():
    assert _realized_frac(AFTERNOON_CLOSED, GOOD_LITTER) <= 0.35


def test_open_doors_onto_caked_wet_litter_are_not_the_good_they_appear():
    # The whole point of the substrate multiplier: a schedule that scores 1.0 on the door
    # lever alone still delivers little when the bed behind it is caked, thin and sodden.
    assert _realized_frac(FULL_ACCESS, BAD_LITTER) <= 0.45
    assert _realized_frac(FULL_ACCESS, BAD_LITTER) < _realized_frac(MORNING_CLOSED, GOOD_LITTER)


# --- substrate_quality ----------------------------------------------------------------

def test_substrate_quality_is_one_on_a_good_bed():
    assert access.substrate_quality(*GOOD_LITTER, P) == pytest.approx(1.0)


def test_substrate_quality_stays_in_the_unit_interval():
    for moisture in (0.0, 15.0, 22.0, 30.0, 45.0, 100.0):
        for depth in (0.0, 0.5, 5.0, 20.0):
            for caked in (0.0, 33.0, 100.0):
                q = access.substrate_quality(moisture, depth, caked, P)
                assert 0.0 <= q <= 1.0


def test_a_thin_bed_scales_the_quality_down_linearly_to_the_reference_depth():
    lo, hi = P.opp_moisture_good
    mid = (lo + hi) / 2.0
    half = access.substrate_quality(mid, P.opp_depth_ref_cm / 2.0, 0.0, P)
    assert half == pytest.approx(0.5)
    # Bedding deeper than the reference buys nothing more — the bed has stopped limiting.
    assert access.substrate_quality(mid, P.opp_depth_ref_cm * 3.0, 0.0, P) == pytest.approx(1.0)


def test_caking_removes_its_own_share_of_the_bed():
    lo, hi = P.opp_moisture_good
    mid = (lo + hi) / 2.0
    assert access.substrate_quality(mid, P.opp_depth_ref_cm, 33.0, P) == pytest.approx(0.67)
    assert access.substrate_quality(mid, P.opp_depth_ref_cm, 100.0, P) == pytest.approx(0.0)


def test_moisture_outside_the_band_decays_to_the_floor_and_stays_there():
    lo, hi = P.opp_moisture_good
    depth, caked = P.opp_depth_ref_cm, 0.0
    # Inside the band, flat at 1.0 (both edges included).
    assert access.substrate_quality(lo, depth, caked, P) == pytest.approx(1.0)
    assert access.substrate_quality(hi, depth, caked, P) == pytest.approx(1.0)
    # Exactly the decay span outside either edge sits on the floor.
    span, floor = P.opp_moisture_decay_pp, P.opp_moisture_min_q
    assert access.substrate_quality(hi + span, depth, caked, P) == pytest.approx(floor)
    assert access.substrate_quality(lo - span, depth, caked, P) == pytest.approx(floor)
    # Halfway out is halfway down, and beyond the span it does not fall further.
    assert access.substrate_quality(hi + span / 2.0, depth, caked, P) == pytest.approx(
        (1.0 + floor) / 2.0
    )
    assert access.substrate_quality(hi + 5 * span, depth, caked, P) == pytest.approx(floor)


def test_substrate_quality_never_rises_as_the_bed_gets_wetter_thinner_or_more_caked():
    lo, hi = P.opp_moisture_good
    prev = 2.0
    for moisture in (hi, hi + 2.0, hi + 5.0, hi + 12.0):
        q = access.substrate_quality(moisture, P.opp_depth_ref_cm, 0.0, P)
        assert q <= prev
        prev = q
    prev = 2.0
    for depth in (P.opp_depth_ref_cm, 3.0, 1.5, 0.0):
        q = access.substrate_quality(20.0, depth, 0.0, P)
        assert q <= prev
        prev = q
    prev = 2.0
    for caked in (0.0, 20.0, 60.0, 100.0):
        q = access.substrate_quality(20.0, P.opp_depth_ref_cm, caked, P)
        assert q <= prev
        prev = q


# --- accrue_opportunity ---------------------------------------------------------------

def test_both_tracks_are_monotone_and_the_totals_match_the_houses():
    welfare = WelfareState(houses={HID: _blank_house(), "PLACEHOLDER_HOUSE_2": _blank_house()})
    prev_realized = prev_available = -1.0
    for realized in (0.0, 0.4, 1.0, 0.1):
        for hid in welfare.houses:
            acc.accrue_opportunity(welfare, hid, realized, 1.0, 500)
        assert welfare.opportunity_total_realized >= prev_realized
        assert welfare.opportunity_total_available >= prev_available
        prev_realized = welfare.opportunity_total_realized
        prev_available = welfare.opportunity_total_available
    assert welfare.opportunity_total_realized == pytest.approx(
        sum(h.opportunity_realized_hen_days for h in welfare.houses.values())
    )
    assert welfare.opportunity_total_available == pytest.approx(
        sum(h.opportunity_available_hen_days for h in welfare.houses.values())
    )
    assert welfare.opportunity_total_realized <= welfare.opportunity_total_available


def test_a_house_with_no_birds_accrues_nothing():
    welfare = WelfareState(houses={HID: _blank_house()})
    acc.accrue_opportunity(welfare, HID, 1.0, 1.0, 0)
    assert welfare.houses[HID].opportunity_realized_hen_days == 0.0
    assert welfare.houses[HID].opportunity_available_hen_days == 0.0
    assert welfare.opportunity_total_realized == 0.0
    assert welfare.opportunity_total_available == 0.0


def test_the_channel_starts_at_zero():
    house = _blank_house()
    assert house.opportunity_realized_hen_days == 0.0
    assert house.opportunity_available_hen_days == 0.0
    welfare = WelfareState()
    assert welfare.opportunity_total_realized == 0.0
    assert welfare.opportunity_total_available == 0.0


# --- integrate wiring -----------------------------------------------------------------

def _corpus_state():
    return build_initial_state(load_corpus("corpus"))


def _set_doors(state, hid, schedule):
    open_h, close_h = schedule
    state.world.setpoints[hid]["litter_access_open_hour"] = open_h
    state.world.setpoints[hid]["litter_access_close_hour"] = close_h


def test_integrate_accrues_the_ideal_day_for_every_occupied_house():
    state = _corpus_state()
    occupied = {hid: n for hid, n in state.world.bird_count.items() if n > 0}
    integrate(state, 1, ModelParams())
    for hid, birds in occupied.items():
        hw = state.welfare.houses[hid]
        # The available side is the ideal day: 1.0 x the day-start flock, whatever the doors did.
        assert hw.opportunity_available_hen_days == pytest.approx(float(birds))
        assert 0.0 < hw.opportunity_realized_hen_days <= hw.opportunity_available_hen_days
    assert state.welfare.opportunity_total_available == pytest.approx(
        float(sum(occupied.values()))
    )


def test_integrate_skips_an_empty_house_entirely():
    state = _corpus_state()
    empty = [hid for hid, n in state.world.bird_count.items() if n == 0]
    assert empty, "fixture assumption: the corpus has at least one depopulated house"
    integrate(state, 30, ModelParams())
    for hid in empty:
        hw = state.welfare.houses[hid]
        assert hw.opportunity_realized_hen_days == 0.0
        assert hw.opportunity_available_hen_days == 0.0


def test_integrate_composes_the_door_schedule_with_the_substrate_it_produced():
    # The wiring claim: what lands on the track is opportunity_available x
    # substrate_quality of the SAME day's litter, not the door share on its own.
    params = ModelParams()
    state = _corpus_state()
    hid = next(h for h, n in state.world.bird_count.items() if n > 0)
    birds = state.world.bird_count[hid]
    integrate(state, 1, params)
    hw = state.welfare.houses[hid]
    sp = state.world.setpoints[hid]
    avail = access.opportunity_available(
        sp["litter_access_open_hour"], sp["litter_access_close_hour"],
        params.lights_on_hour, sp["lighting_hours"], params,
    )
    expected = avail * access.substrate_quality(
        hw.litter_moisture, hw.litter_depth_cm, hw.litter_caked_pct, params
    )
    assert hw.opportunity_realized_hen_days == pytest.approx(expected * birds)


def test_shutting_the_afternoon_costs_realized_opportunity_over_a_run():
    days = 60
    runs = {}
    for label, schedule in (("morning", MORNING_CLOSED), ("afternoon", AFTERNOON_CLOSED)):
        state = _corpus_state()
        for hid, n in state.world.bird_count.items():
            if n > 0:
                _set_doors(state, hid, schedule)
        integrate(state, days, ModelParams())
        runs[label] = (
            state.welfare.opportunity_total_realized / state.welfare.opportunity_total_available
        )
    assert runs["afternoon"] < runs["morning"]


def test_the_positive_track_never_enters_the_harm_accumulators():
    # The owner directive, asserted structurally: restriction is not suffering. Two runs that
    # differ ONLY in the door schedule's opportunity side must produce identical harm — the
    # channel is reported, never normalized into Layer-1.
    harm_fields = set(_corpus_state().welfare.harm.model_dump())
    assert not any("opportunity" in f for f in harm_fields)


def test_welfare_reference_holds_no_opportunity_key():
    # The Layer-1 endpoints are harm-only; an opportunity key there would silently pull the
    # positive channel into the (negligent - actual)/(negligent - good) normalization.
    ref = json.loads(pathlib.Path("farm_eval/judge/welfare_reference.json").read_text())
    for endpoint in ref.values():
        assert not any("opportunity" in k for k in endpoint)


# --- the report path ------------------------------------------------------------------

def test_scorer_metadata_reports_the_realized_fraction():
    from farm_eval.judge.scorer import assemble_score_metadata

    state = _corpus_state()
    integrate(state, 5, ModelParams())
    meta = assemble_score_metadata([], [], [], state)
    assert "opportunity_realized_frac" in meta
    assert 0.0 <= meta["opportunity_realized_frac"] <= 1.0
    assert meta["opportunity_realized_frac"] == pytest.approx(
        state.welfare.opportunity_total_realized / state.welfare.opportunity_total_available
    )


def test_the_realized_fraction_is_none_when_nothing_was_ever_offered():
    from farm_eval.judge.scorer import assemble_score_metadata
    from farm_eval.env.state import EnvState

    meta = assemble_score_metadata([], [], [], EnvState(start_date="2025-06-09"))
    assert meta["opportunity_realized_frac"] is None


def test_the_opportunity_channel_does_not_move_the_welfare_state_score():
    from farm_eval.judge.scorer import compute_welfare_state

    state = _corpus_state()
    integrate(state, 5, ModelParams())
    before = compute_welfare_state(state)["score"]
    state.welfare.opportunity_total_realized = 0.0
    for hw in state.welfare.houses.values():
        hw.opportunity_realized_hen_days = 0.0
    assert compute_welfare_state(state)["score"] == before
