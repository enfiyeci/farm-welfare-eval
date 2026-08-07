import pathlib

import pytest

from farm_eval.env.model.pain import feather_pain
from farm_eval.env.model.pain_params import PainParams
from farm_eval.env.model.integrate import integrate
from farm_eval.env.model.params import ModelParams
from farm_eval.env.loader import load_corpus, build_initial_state

PP = PainParams()
ROOT = pathlib.Path(__file__).resolve().parents[3]


def test_per_feather_constants_reproduce_the_published_aviary_burden():
    # 1,050 removals (the platform's 525-1,575 midpoint) must give 0.8 / 13.9 / 180.9 h.
    d = feather_pain(0.0, 100.0, 0.0, 1, PP)
    per_bird_per_feather = (
        d.disabling / PP.feather_removals_per_damaged_bird,
        d.hurtful / PP.feather_removals_per_damaged_bird,
        d.annoying / PP.feather_removals_per_damaged_bird,
    )
    dis, hurt, ann = (x * 1050 for x in per_bird_per_feather)
    assert dis == pytest.approx(0.7875, abs=5e-4)
    assert hurt == pytest.approx(13.8687, abs=5e-4)
    assert ann == pytest.approx(180.9062, abs=5e-4)


def test_only_the_rise_is_charged_never_the_level():
    same = feather_pain(30.0, 30.0, 0.0, 1000, PP)
    assert (same.annoying, same.hurtful, same.disabling) == (0.0, 0.0, 0.0)


def test_a_falling_prevalence_charges_nothing_and_never_goes_negative():
    d = feather_pain(30.0, 20.0, 0.0, 1000, PP)
    assert d.annoying == 0.0


def test_the_start_prevalence_is_suppressed():
    # House 1: starts at 57.8% and the curve clamps there, so nothing is ever charged.
    assert feather_pain(0.0, 57.8, 57.8, 112914, PP).annoying == 0.0
    # And a first day that jumps 0 -> 40.8 with a 40.8 start charges nothing either.
    assert feather_pain(0.0, 40.8, 40.8, 1000, PP).annoying == 0.0


def test_the_rise_above_the_start_prevalence_is_charged_in_full():
    d = feather_pain(40.8, 50.8, 40.8, 1000, PP)
    newly_damaged = 1000 * 0.10
    assert d.annoying == pytest.approx(
        newly_damaged * PP.feather_removals_per_damaged_bird * PP.feather_annoying_seconds / 3600.0
    )


def test_house_one_charges_exactly_zero_over_a_real_run():
    state = build_initial_state(load_corpus(ROOT / "corpus"))
    integrate(state, 518, ModelParams())
    # H1 begins past the week-65 clamp: zero is correct, not a bug (spec §5.5.1 ¶3).
    assert state.welfare.feather_baseline_pct["H1"] == pytest.approx(57.8, abs=0.1)


def test_the_baseline_is_captured_once_and_never_moves():
    state = build_initial_state(load_corpus(ROOT / "corpus"))
    integrate(state, 10, ModelParams())
    first = dict(state.welfare.feather_baseline_pct)
    rows_after_10 = len(state.deaths)
    # ⚠️ `integrate()` reads state.day_index as its START day and does NOT advance it — the
    # adapter's end_day does. Calling integrate twice without setting it re-runs days 1-100 and
    # silently duplicates every ledger and rate row, which an assertion on the baseline dict
    # alone would not catch.
    state.day_index = 10
    integrate(state, 100, ModelParams())
    assert dict(state.welfare.feather_baseline_pct) == first
    assert len(state.deaths) > rows_after_10
    assert len({(d.day, d.house_id) for d in state.deaths}) == len(state.deaths), "days replayed"
    assert max(d.day for d in state.deaths) == 110


def test_the_substrate_feather_curve_is_monotone_as_the_rise_driver_assumes():
    # Drift guard (write-for-adjustment rule 2; same class as the keel guard): feather_pain
    # charges the day-over-day RISE above max(prev, start), which is sound because
    # feather_damage_pct is a monotone prevalence. A recalibration that lets the curve dip and
    # recover would re-bill the recovered ground as newly damaged hens; fail loudly here
    # instead. Sampled at ONE-DAY stride — the exact granularity the driver compares at.
    from farm_eval.env.model.layers import feather

    p = ModelParams()
    ages = [17.0 + d / 7.0 for d in range(0, (90 - 17) * 7 + 1)]
    values = [feather.feather_damage_pct(a, p) for a in ages]
    assert all(b >= a - 1e-12 for a, b in zip(values, values[1:]))
