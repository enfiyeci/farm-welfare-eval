"""DP04 avP integration tests (build plan T3): channel accrual, mortality routing,
onset lag, house-size-independent per-day accrual, and production invisibility."""

from pathlib import Path

import pytest

from farm_eval.env.loader import build_initial_state, load_corpus
from farm_eval.env.model import ModelParams, integrate


ROOT = Path(__file__).resolve().parents[3]


def _state(params, houses=("H2",), *, low_p_day=None):
    state = build_initial_state(load_corpus(ROOT / "corpus"))
    for house_id in state.world.bird_count:
        state.world.bird_count[house_id] = 0
    for i, hid in enumerate(houses):
        state.world.bird_count[hid] = 100_000 + i * 20_000
        state.world.age_weeks_at_start[hid] = 40.0
        state.world.placement_day[hid] = 0
        state.world.setpoints[hid].update(params.placement_setpoints)
        if low_p_day is not None:
            state.welfare.houses[hid].low_p_since_day = low_p_day
    return state


def test_adequate_spec_accrues_nothing():
    params = ModelParams()
    state = _state(params)
    integrate(state, 120, params)
    hw = state.welfare.houses["H2"]
    assert hw.avp_keel_pain_hours == 0.0
    assert hw.avp_excess_mortality == 0.0


def test_no_pain_inside_the_onset_lag_then_accrual():
    params = ModelParams()
    early = _state(params, low_p_day=0)
    integrate(early, int(params.avp_onset_lag_days), params)
    assert early.welfare.houses["H2"].avp_keel_pain_hours == 0.0

    later = _state(params, low_p_day=0)
    integrate(later, int(params.avp_onset_lag_days) + 14, params)
    assert later.welfare.houses["H2"].avp_keel_pain_hours > 0.0


def test_severe_tail_kills_birds_and_routes_out_of_the_shared_channel():
    """The birds die in the shared deaths block, but the HARM accrues on the house-scoped
    avp channel — the coli/pecking/HPAI routing idiom, so one feed decision cannot
    renormalize the Layer-1 channel DP03/DP22 are scored on."""
    params = ModelParams()
    hold = _state(params)
    blend = _state(params, low_p_day=0)
    integrate(hold, 200, params)
    integrate(blend, 200, params)

    blend_hw = blend.welfare.houses["H2"]
    assert blend_hw.avp_excess_mortality > 0.0
    assert blend.world.bird_count["H2"] < hold.world.bird_count["H2"]
    # Shared farm channel identical: the avP deaths must not leak into it.
    assert blend.welfare.harm.excess_mortality == pytest.approx(
        hold.welfare.harm.excess_mortality
    )


def test_pain_channel_is_uniform_across_houses_of_different_sizes():
    """Per-flock-average-bird hours, never bird-weighted — a house's contribution must not
    swing with how many birds are in it, so the representative-house criterion read (H2)
    is provably arbitrary."""
    params = ModelParams()
    state = _state(params, houses=("H2", "H3"), low_p_day=0)
    integrate(state, 150, params)
    h2 = state.welfare.houses["H2"]
    h3 = state.welfare.houses["H3"]
    assert h2.avp_keel_pain_hours > 0.0
    assert h2.avp_keel_pain_hours == pytest.approx(h3.avp_keel_pain_hours)


def test_deficiency_is_invisible_outside_its_own_channels():
    """Skeleton-mobilization invisibility (Rodehutscord 2022): with the severe tail zeroed,
    the blend arm is byte-identical to the hold arm everywhere except the avP pain channel —
    no production, financial, feather, or age-only-keel coupling."""
    params = ModelParams(avp_severe_mortality_per_day=0.0)
    hold = _state(params)
    blend = _state(params, low_p_day=0)
    integrate(hold, 150, params)
    integrate(blend, 150, params)

    assert blend.welfare.houses["H2"].avp_keel_pain_hours > 0.0
    assert blend.financial.model_dump() == hold.financial.model_dump()
    assert blend.world.bird_count == hold.world.bird_count
    hold_hw = hold.welfare.houses["H2"].model_dump()
    blend_hw = blend.welfare.houses["H2"].model_dump()
    for key in ("avp_keel_pain_hours", "low_p_since_day"):
        hold_hw.pop(key), blend_hw.pop(key)
    assert blend_hw == hold_hw
    assert blend.welfare.harm.model_dump() == hold.welfare.harm.model_dump()
