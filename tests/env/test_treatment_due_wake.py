"""`treatment_due_day` (Task 2 of the DP05 red-mite full-course plan): the farm-wide wake
signal `FarmEnv.end_day` reads to know whether a mite treatment step is due tomorrow.

Unlike `active_hpai_wake` and its siblings in `harm_window.py`, this predicate takes no
`decision_points`/`enabled_nodes` — it reads farm state only (`state.mite_orders`), so it
behaves identically in every episode regardless of which nodes are enabled. It aggregates
`mite_control.next_due_day` (Task 1, pure per-order arithmetic) over every order that
`mite_control.systemic_order_is_active` still counts as workable, and reports the earliest
STRICTLY-FUTURE due day — or None when nothing is due.

Built directly on `MiteControlOrder` and `EnvState`, the way
`tests/env/test_dp05_mite_scoring.py`'s `next_due_day` unit tests and
`tests/env/test_harm_window.py`'s `_state` helper do: no episode fixture needed, since
`treatment_due_day` only reads `state.day_index` and `state.mite_orders`.
"""

from farm_eval.env.harm_window import treatment_due_day
from farm_eval.env.model.params import ModelParams
from farm_eval.env.state import EnvState, MiteControlOrder

PARAMS = ModelParams()


def _state(day_index: int, orders: list[MiteControlOrder]) -> EnvState:
    return EnvState(start_date="2025-06-09", day_index=day_index, mite_orders=orders)


def _order(**overrides) -> MiteControlOrder:
    fields = dict(
        order_id="RX-H2-112",
        house_id="H2",
        issue="red_mite",
        route="systemic",
        request_day=112,
    )
    fields.update(overrides)
    return MiteControlOrder(**fields)


def test_no_orders_is_none():
    assert treatment_due_day(_state(100, []), PARAMS) is None


def test_pending_order_due_on_its_approval_day():
    # request_day 112 + approval_lag_days 2 = approved_day 114 (mirrors request_vet_treatment).
    order = _order(approved_day=114)
    st = _state(100, [order])  # day_index 100 is strictly before 114
    assert treatment_due_day(st, PARAMS) == 114


def test_part_dosed_course_due_at_last_dose_plus_interval():
    order = _order(approved_day=114, days=[119])
    st = _state(120, [order])  # strictly before 119 + interval
    expected = 119 + PARAMS.mite_systemic_dose_interval_days
    assert treatment_due_day(st, PARAMS) == expected


def test_failed_course_is_none():
    # Window closes at days[-1] + interval + tol; one day past that, systemic_order_is_active
    # goes False and the course can never complete, so there is nothing left to wake for.
    order = _order(approved_day=114, days=[119])
    window_closes = 119 + PARAMS.mite_systemic_dose_interval_days + PARAMS.mite_systemic_dose_interval_tol
    st = _state(window_closes + 1, [order])
    assert treatment_due_day(st, PARAMS) is None


def test_approved_undosed_due_day_already_passed_is_none():
    # Strictly-after rule: an approved-but-undosed order stays "active" indefinitely with a due
    # day that can fall in the past. Without the strict filter the clock would try to jump
    # backwards (or wake daily forever) chasing a day that has already happened.
    order = _order(approved_day=114)
    st = _state(114, [order])  # due day == day_index, not strictly after
    assert treatment_due_day(st, PARAMS) is None
    st_past = _state(120, [order])  # due day well before day_index
    assert treatment_due_day(st_past, PARAMS) is None


def test_two_active_orders_earlier_due_day_wins():
    earlier = _order(order_id="RX-H2-112", house_id="H2", approved_day=130)
    later = _order(order_id="RX-H3-100", house_id="H3", request_day=100, approved_day=200)
    st = _state(50, [later, earlier])  # order added out of due-day order on purpose
    assert treatment_due_day(st, PARAMS) == 130
