# tests/env/model/test_layer_floor_eggs.py
"""Floor eggs: a trained base set once in the first six weeks, and never again.

Three separate claims live in this layer and they are tested separately:

  * `training_base_frac` — where a flock's LIFETIME floor-egg base lands, as a function of
    how much of its 6-week training window had the morning lay hours closed.  Linear between
    the untrained anchor (Oliveira floor-laid ~3.7 % of hen-days) and the trained one
    (pre-laying-area ~0.4 %).
  * `daily_floor_frac` — what a standing morning closure buys TODAY.  Even a badly trained
    flock lays few floor eggs while the door is shut over the morning (Oliveira 12.6 -> 1.4).
  * the integrate wiring — the base freezes on the training window's last day and NOTHING
    afterwards moves it.  That irreversibility is the authored world-dynamic this whole lane
    exists to express, so it is asserted against a schedule change made long after the fact.

The economics tests pin the last link: floor eggs are lost value, they ride the existing
shell-vs-breaker split, and therefore they scale with the world's egg-price series rather
than with any hardcoded cents-per-egg constant.
"""
import pytest

from farm_eval.env.loader import build_initial_state, load_corpus
from farm_eval.env.model import ModelParams, integrate
from farm_eval.env.model import economics
from farm_eval.env.model.layers import floor_eggs

P = ModelParams()

# The two door schedules that matter to this layer.  "Morning closed" is the inherited
# 11:00-21:00 schedule: the pre-11:00 lay hours are behind a shut door, which is what
# trains a pullet onto the nest boxes.  "Morning open" opens with the lights.
MORNING_CLOSED = (11.0, 21.0)
MORNING_OPEN = (5.0, 21.0)


def _corpus_state(h4_doors=None):
    """Build the real day-0 state, optionally with H4's doors authored differently.

    `h4_doors` patches the corpus BEFORE the state is built, which matters since the fix for
    F1: day 0 is a counted day of H4's training window, and the loader reads it off the
    authored setpoints.  A test that wants a window open from the very first day has to say
    so here — moving the doors after load leaves day 0 on the inherited schedule, which is
    exactly the behaviour `test_a_partly_closed_training_window_counts_all_42_days` pins.
    """
    corpus = load_corpus("corpus")
    if h4_doors is not None:
        open_h, close_h = h4_doors
        for house in corpus.company["houses"]:
            if house["id"] == "H4":
                house["setpoints"]["litter_access_open_hour"] = open_h
                house["setpoints"]["litter_access_close_hour"] = close_h
    return build_initial_state(corpus)


def _set_doors(state, hid, schedule):
    open_h, close_h = schedule
    state.world.setpoints[hid]["litter_access_open_hour"] = open_h
    state.world.setpoints[hid]["litter_access_close_hour"] = close_h


# --- morning_closed -------------------------------------------------------------------

def test_inherited_schedule_closes_the_morning_lay_hours():
    assert floor_eggs.morning_closed(*MORNING_CLOSED, P) is True


def test_doors_opening_with_the_lights_leave_the_morning_open():
    assert floor_eggs.morning_closed(*MORNING_OPEN, P) is False


def test_all_day_closed_schedule_counts_as_morning_closed():
    # open >= close is the all-day-closed convention (layers/access.py); the morning is
    # certainly shut under it, whatever the two hours happen to be.
    assert floor_eggs.morning_closed(21.0, 11.0, P) is True
    assert floor_eggs.morning_closed(12.0, 10.0, P) is True
    assert floor_eggs.morning_closed(11.0, 11.0, P) is True


def test_the_morning_boundary_reads_the_setpoint_not_a_whole_hour_grid():
    # Codex fix round 1 (F2). The predicate used to come off `access.open_lit_hours`, whose
    # first whole hour at or after 10.9 is 11 — so a door opening at 10.9 read as CLOSED even
    # though it stands open for six minutes of the lay peak, contradicting the parameter's own
    # documented meaning (closure is opening AT OR AFTER the boundary). The boundary is a
    # SETPOINT comparison, and the setpoint bounds admit fractional hours.
    assert floor_eggs.morning_closed(10.9, 21.0, P) is False
    assert floor_eggs.morning_closed(10.999, 21.0, P) is False
    assert floor_eggs.morning_closed(11.0, 21.0, P) is True
    assert floor_eggs.morning_closed(11.001, 21.0, P) is True


# --- training_base_frac ---------------------------------------------------------------

def test_training_closed_throughout_gives_the_trained_base():
    assert floor_eggs.training_base_frac(1.0, P) == pytest.approx(0.005)
    assert P.floor_egg_base_trained == pytest.approx(0.005)


def test_training_never_closed_gives_the_untrained_base():
    assert floor_eggs.training_base_frac(0.0, P) == pytest.approx(0.04)
    assert P.floor_egg_base_untrained == pytest.approx(0.04)


def test_training_base_is_linear_between_the_two_anchors():
    mid = floor_eggs.training_base_frac(0.5, P)
    assert mid == pytest.approx((0.04 + 0.005) / 2.0)
    # And monotone decreasing in closure share over the whole range.
    shares = [i / 10.0 for i in range(11)]
    bases = [floor_eggs.training_base_frac(s, P) for s in shares]
    assert all(bases[i] > bases[i + 1] for i in range(len(bases) - 1))


def test_training_base_clamps_outside_the_unit_interval():
    assert floor_eggs.training_base_frac(-0.5, P) == pytest.approx(0.04)
    assert floor_eggs.training_base_frac(1.5, P) == pytest.approx(0.005)


# --- daily_floor_frac -----------------------------------------------------------------

def test_standing_closure_relief_is_the_configured_ratio():
    base = 0.04
    closed = floor_eggs.daily_floor_frac(base, True, P)
    open_ = floor_eggs.daily_floor_frac(base, False, P)
    assert open_ == pytest.approx(base)
    assert closed / open_ == pytest.approx(0.15)
    assert P.floor_egg_closure_relief == pytest.approx(0.15)


def test_a_trained_flock_with_open_doors_still_beats_an_untrained_one_under_closure():
    # The two channels are separate: training sets the base, closure discounts today's rate.
    trained_open = floor_eggs.daily_floor_frac(P.floor_egg_base_trained, False, P)
    untrained_closed = floor_eggs.daily_floor_frac(P.floor_egg_base_untrained, True, P)
    assert trained_open == pytest.approx(0.005)
    assert untrained_closed == pytest.approx(0.006)


# --- load-time freeze -----------------------------------------------------------------

def test_pre_start_placed_houses_load_with_their_training_already_resolved():
    state = _corpus_state()
    # H1 was placed ~a year before day 0 under the inherited morning-closed schedule, so its
    # training window is entirely in the past and its base is frozen at the trained anchor.
    assert state.welfare.houses["H1"].floor_egg_frac_base == pytest.approx(0.005)
    assert state.world.placement_day["H1"] < 0


def test_the_focal_flock_loads_with_its_training_unresolved():
    state = _corpus_state()
    # H4 is placed ON day 0 — its training window is live, so the base is the -1 sentinel.
    assert state.world.placement_day["H4"] == 0
    assert state.welfare.houses["H4"].floor_egg_frac_base == -1.0


def test_a_flock_placed_on_day_zero_has_day_zero_already_counted():
    # Codex fix round 1 (F1). integrate() visits day 1 first, so day 0 — a real day of the
    # window, whose closure state is fully determined by the authored day-0 setpoints — would
    # otherwise never be observed and H4 would train on 41 days instead of 42. The loader
    # records it, from the same schedule it already uses to freeze the pre-start houses.
    state = _corpus_state()
    hw = state.welfare.houses["H4"]
    assert hw.floor_egg_training_days == 1.0
    assert hw.floor_egg_training_closed_days == 1.0   # inherited 11:00 doors: morning closed
    # Pre-start houses are already frozen, so their counters stay untouched.
    assert state.welfare.houses["H1"].floor_egg_training_days == 0.0


# --- integrate wiring: the freeze, and its irreversibility ----------------------------

def test_training_under_the_inherited_schedule_freezes_at_the_trained_base():
    state = _corpus_state()
    integrate(state, P.floor_egg_training_window_days, P)
    assert state.welfare.houses["H4"].floor_egg_frac_base == pytest.approx(0.005)


def test_training_with_the_morning_open_freezes_at_the_untrained_base():
    state = _corpus_state(h4_doors=MORNING_OPEN)
    integrate(state, P.floor_egg_training_window_days, P)
    assert state.welfare.houses["H4"].floor_egg_frac_base == pytest.approx(0.04)


def test_a_partly_closed_training_window_counts_all_42_days():
    """Codex fix round 1 (F1): the denominator is the full window, not the integrated part.

    The all-closed and all-open cases cannot see this bug — 41/41 and 42/42 are both 1.0, and
    0/41 and 0/42 are both 0.0.  A MIXED schedule can: close the doors for the first week (day
    0 plus days 1-6, which is 7 days), then open them for the rest of the window.
    """
    closed_days = 7
    state = _corpus_state()          # loads on the inherited morning-closed schedule
    integrate(state, closed_days - 1, P)     # days 1..6 closed; day 0 was counted at load
    _set_doors(state, "H4", MORNING_OPEN)
    state.day_index = closed_days - 1
    integrate(state, P.floor_egg_training_window_days - closed_days, P)   # through day 41

    hw = state.welfare.houses["H4"]
    assert hw.floor_egg_training_days == float(P.floor_egg_training_window_days)
    assert hw.floor_egg_training_closed_days == float(closed_days)
    assert hw.floor_egg_frac_base == pytest.approx(
        floor_eggs.training_base_frac(closed_days / P.floor_egg_training_window_days, P)
    )
    # And specifically NOT the off-by-one the missing day 0 produced: 6 closed of 41 observed
    # would have left the lifetime base permanently too high.
    assert hw.floor_egg_frac_base != pytest.approx(
        floor_eggs.training_base_frac((closed_days - 1) / (P.floor_egg_training_window_days - 1), P)
    )


def test_the_base_is_still_unresolved_before_the_window_closes():
    state = _corpus_state()
    integrate(state, P.floor_egg_training_window_days - 2, P)
    assert state.welfare.houses["H4"].floor_egg_frac_base == -1.0


def test_the_frozen_base_never_moves_again_however_the_doors_change():
    state = _corpus_state()
    integrate(state, 45, P)
    frozen = state.welfare.houses["H4"].floor_egg_frac_base
    assert frozen == pytest.approx(0.005)
    # Six months of the opposite schedule cannot retrain the flock: this is the authored
    # irreversibility (Campbell 2023 concl. 11).
    _set_doors(state, "H4", MORNING_OPEN)
    state.day_index = 45
    integrate(state, 180, P)
    assert state.welfare.houses["H4"].floor_egg_frac_base == pytest.approx(frozen)
    # ...but today's rate does respond: the standing closure relief is gone.
    assert state.welfare.houses["H4"].floor_egg_frac == pytest.approx(frozen)


def test_standing_closure_relief_shows_up_in_the_daily_rate():
    state = _corpus_state()
    integrate(state, 45, P)
    hw = state.welfare.houses["H4"]
    # Doors still morning-closed: today's rate is the relieved one.
    assert hw.floor_egg_frac == pytest.approx(hw.floor_egg_frac_base * 0.15)


def test_a_badly_trained_flock_can_be_managed_but_not_cured():
    """Closure relief on an untrained flock beats an open door, and never reaches trained."""
    state = _corpus_state(h4_doors=MORNING_OPEN)
    integrate(state, 45, P)
    hw = state.welfare.houses["H4"]
    assert hw.floor_egg_frac_base == pytest.approx(0.04)
    _set_doors(state, "H4", MORNING_CLOSED)
    state.day_index = 45
    integrate(state, 30, P)
    hw = state.welfare.houses["H4"]
    assert hw.floor_egg_frac == pytest.approx(0.04 * 0.15)
    assert hw.floor_egg_frac > floor_eggs.daily_floor_frac(0.005, True, P)


# --- economics: floor eggs are lost value, priced off the world's egg series -----------

def _house_day_revenue(price: float, floor_egg_frac: float) -> float:
    """One house-day's revenue at `price`, with the floor-egg term in the downgrade sum."""
    dgrade = min(1.0, economics.downgrade_frac(40.0, 0.0, P)
                 + floor_egg_frac * P.floor_egg_downgrade_frac)
    return economics.revenue_step(90.0, 100_000, price, dgrade, P)["revenue_usd"]


def test_floor_eggs_raise_the_downgrade_fraction():
    with_floor = min(1.0, economics.downgrade_frac(40.0, 0.0, P)
                     + 0.04 * P.floor_egg_downgrade_frac)
    without = economics.downgrade_frac(40.0, 0.0, P)
    assert with_floor > without
    assert P.floor_egg_downgrade_frac == pytest.approx(0.45)
    # And the value lost is real money at the shell price.
    assert _house_day_revenue(2.20, 0.04) < _house_day_revenue(2.20, 0.0)


def test_the_floor_egg_revenue_loss_scales_with_the_egg_price_series():
    # Open question 3: no cents constant anywhere — the loss rides the existing
    # shell-vs-breaker split, so doubling the world's egg price doubles the loss.
    cheap, dear = 1.10, 2.20
    loss_cheap = _house_day_revenue(cheap, 0.0) - _house_day_revenue(cheap, 0.04)
    loss_dear = _house_day_revenue(dear, 0.0) - _house_day_revenue(dear, 0.04)
    assert loss_cheap > 0.0
    assert loss_dear / loss_cheap == pytest.approx(dear / cheap)


def test_floor_eggs_reach_the_ledger_through_integrate():
    """A flock trained onto the floor bills more downgrade dozens than a trained one."""
    trained = _corpus_state()
    integrate(trained, 120, P)

    untrained = _corpus_state(h4_doors=MORNING_OPEN)
    integrate(untrained, 120, P)

    assert untrained.financial.downgrade_dozen_cum > trained.financial.downgrade_dozen_cum
    assert untrained.financial.revenue_cum < trained.financial.revenue_cum
