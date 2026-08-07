import pathlib

import pytest

from farm_eval.env.loader import build_initial_state, load_corpus
from farm_eval.env.model.integrate import integrate
from farm_eval.env.model.params import ModelParams


ROOT = pathlib.Path(__file__).resolve().parents[3]


def _run(days: int):
    state = build_initial_state(load_corpus(ROOT / "corpus"))
    integrate(state, days, ModelParams())
    return state


def test_one_row_per_occupied_house_per_day():
    state = _run(30)
    occupied = [h for h, n in state.world.bird_count.items() if n > 0]
    assert len(state.welfare.pain_rates) == 30 * len(occupied)


def test_rates_are_per_bird_and_reconstruct_the_house_total():
    state = _run(30)
    for hid, track in state.welfare.pain_by_house.items():
        rebuilt = sum(r.annoying * b for r, b in _rows_with_birds(state, hid))
        assert rebuilt == pytest.approx(track.annoying, rel=1e-6)


def _rows_with_birds(state, hid):
    births = {(d.day, d.house_id): d.birds_start for d in state.deaths}
    return [(r, births[(r.day, hid)]) for r in state.welfare.pain_rates if r.house_id == hid]


def test_rates_are_non_negative():
    state = _run(30)
    for r in state.welfare.pain_rates:
        assert min(r.annoying, r.hurtful, r.disabling, r.excruciating) >= 0.0


def test_the_series_pairs_with_the_death_ledger_day_for_day():
    state = _run(30)
    rate_keys = {(r.day, r.house_id) for r in state.welfare.pain_rates}
    death_keys = {(d.day, d.house_id) for d in state.deaths}
    assert rate_keys == death_keys


def test_the_series_size_stays_in_the_stated_budget():
    state = _run(518)
    assert len(state.welfare.pain_rates) <= 518 * len(state.welfare.houses)


def test_by_channel_omits_quiet_channels():
    state = _run(30)
    for row in state.welfare.pain_rates:
        assert all(any(value != 0.0 for value in rates) for rates in row.by_channel.values())
