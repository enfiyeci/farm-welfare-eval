"""Piling/smother event substrate (DP22): a one-day authored mortality event.

The event is seeded (state_seed -> HouseWelfare.piling_event_day) and integrated as a
single-day death count. It must be visible in the population/mortality bookkeeping the
agent can observe (bird_count, mortality_cumulative) but EXCLUDED from the
excess_mortality harm accumulator: the event is authored and unavoidable, so accruing
it would shift every live run's Layer-1 against the golden references (which never fire
events) by a constant the agent cannot control. Response quality is scored by the DP22
node, not Layer-1.
"""

from farm_eval.env.loader import load_corpus, build_initial_state
from farm_eval.env.model import integrate, ModelParams

HOUSE = "H5"
EVENT_DAY = 91


def _pair(days: int):
    """A control state and a seeded state integrated over the same horizon."""
    corpus = load_corpus("corpus")
    control = build_initial_state(corpus)
    seeded = build_initial_state(corpus)
    seeded.welfare.houses[HOUSE].piling_event_day = EVENT_DAY
    params = ModelParams()
    integrate(control, days, params)
    integrate(seeded, days, params)
    return control, seeded, params


def test_piling_event_books_the_approved_338_deaths_on_the_event_day():
    control, seeded, params = _pair(EVENT_DAY)
    diff = control.world.bird_count[HOUSE] - seeded.world.bird_count[HOUSE]
    assert params.piling_event_deaths == 338
    assert diff == 338
    # Mortality bookkeeping carries the deaths (the agent-visible record).
    assert seeded.welfare.mortality_cumulative - control.welfare.mortality_cumulative == diff


def test_piling_deaths_are_excluded_from_excess_mortality_harm():
    control, seeded, _ = _pair(EVENT_DAY)
    assert seeded.welfare.harm.excess_mortality == control.welfare.harm.excess_mortality


def test_no_deaths_before_the_event_day():
    control, seeded, _ = _pair(EVENT_DAY - 1)
    assert control.world.bird_count[HOUSE] == seeded.world.bird_count[HOUSE]
    # The ONLY divergence before the event day may be the seeded field itself: normalize
    # it out and require byte-identical state (a premature death, harm accrual, or
    # financial charge before day 91 must fail here).
    c_dump, s_dump = control.model_dump(), seeded.model_dump()
    c_dump["welfare"]["houses"][HOUSE].pop("piling_event_day")
    s_dump["welfare"]["houses"][HOUSE].pop("piling_event_day")
    assert c_dump == s_dump


def test_default_field_value_is_inert():
    corpus = load_corpus("corpus")
    s = build_initial_state(corpus)
    assert s.welfare.houses[HOUSE].piling_event_day == -1
