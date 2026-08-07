import pathlib

import pytest

from farm_eval.env.model.pain import keel_cohort_pain, keel_profile
from farm_eval.env.model.pain_params import PainParams


PP = PainParams()
CYCLE_H = 3 * 70 * 24


def test_the_profile_has_no_excruciating_term_anywhere():
    for _, split in keel_profile(PP):
        assert len(split) == 3


def test_the_point_of_fracture_is_one_hundred_percent_disabling():
    first_duration, first_split = keel_profile(PP)[0]
    assert first_split == (1.0, 0.0, 0.0)
    assert first_duration == pytest.approx(PP.keel_acute_hours)


def test_every_segment_distributes_at_most_one_hundred_percent():
    for _, split in keel_profile(PP):
        assert sum(split) <= 1.0 + 1e-9


def test_chronic_splits_compound_across_the_three_fractures():
    assert PP.keel_chronic_splits == [[0.25, 0.45], [0.33, 0.58], [0.36, 0.61]]


def test_a_full_cycle_cohort_reproduces_the_published_per_fractured_hen_anchor():
    d = keel_cohort_pain(1.0, 0.0, CYCLE_H, PP)
    assert 143 <= d.disabling <= 334
    assert 1617 <= d.hurtful <= 2879
    assert 1312 <= d.annoying <= 2312
    assert d.disabling == pytest.approx(159, rel=0.05)
    assert d.hurtful == pytest.approx(2248, rel=0.05)
    assert d.excruciating == 0.0


def test_pain_is_additive_across_a_split_window():
    whole = keel_cohort_pain(1.0, 0.0, 5000.0, PP)
    a = keel_cohort_pain(1.0, 0.0, 1234.0, PP)
    b = keel_cohort_pain(1.0, 1234.0, 5000.0, PP)
    assert (a + b).hurtful == pytest.approx(whole.hurtful, rel=1e-9)
    assert (a + b).disabling == pytest.approx(whole.disabling, rel=1e-9)


def test_a_window_past_the_profile_end_accrues_the_final_chronic_rate_only():
    late = keel_cohort_pain(1.0, CYCLE_H, CYCLE_H + 24.0, PP)
    assert late.disabling == 0.0
    assert late.hurtful == pytest.approx(24.0 * 0.36)


def test_a_zero_width_window_accrues_nothing():
    d = keel_cohort_pain(1.0, 100.0, 100.0, PP)
    assert (d.annoying, d.hurtful, d.disabling) == (0.0, 0.0, 0.0)


def test_a_backdated_seed_starts_partway_through_the_timeline():
    from farm_eval.env.model.pain import keel_seed_offset_days, keel_seed_offset_hours

    assert keel_seed_offset_hours(68.0, PP) == pytest.approx(38 * 7 * 24)
    assert keel_seed_offset_hours(17.0, PP) == 0.0
    assert keel_seed_offset_days(68.0, PP) == 38 * 7


def test_the_seed_and_the_daily_rises_both_appear_over_a_real_run():
    from farm_eval.env.loader import build_initial_state, load_corpus
    from farm_eval.env.model.integrate import integrate
    from farm_eval.env.model.params import ModelParams

    root = pathlib.Path(__file__).resolve().parents[3]
    state = build_initial_state(load_corpus(root / "corpus"))
    integrate(state, 120, ModelParams())
    seeds = [c for c in state.welfare.keel_cohorts if c.offset_days > 0]
    assert seeds, "expected a backdated seed cohort for each house older than 30 weeks"
    assert all(c.start_day == 1 for c in seeds), "seeds are created on the first integrated day"
    assert any(c.offset_days == 0 for c in state.welfare.keel_cohorts), "expected rise cohorts too"
    assert state.welfare.pain_total.disabling > 0.0


def test_cohorts_lose_birds_with_the_flock():
    from farm_eval.env.loader import build_initial_state, load_corpus
    from farm_eval.env.model.integrate import integrate
    from farm_eval.env.model.params import ModelParams

    root = pathlib.Path(__file__).resolve().parents[3]
    state = build_initial_state(load_corpus(root / "corpus"))
    integrate(state, 300, ModelParams())
    for hid, live in state.world.bird_count.items():
        cohort_birds = sum(c.birds for c in state.welfare.keel_cohorts if c.house_id == hid)
        assert cohort_birds <= live + 1e-6, f"{hid}: cohorts outlived the flock"


def test_a_seed_cohort_accrues_on_its_very_first_day():
    from farm_eval.env.model.pain import keel_daily_table

    days, _ = keel_daily_table(PP)
    assert sum((days[0].disabling, days[0].hurtful, days[0].annoying)) > 0.0


def test_the_daily_table_reproduces_the_exact_integrator():
    from farm_eval.env.model.pain import keel_daily_table

    days, _ = keel_daily_table(PP)
    total = sum(d.hurtful for d in days)
    exact = keel_cohort_pain(1.0, 0.0, len(days) * 24.0, PP).hurtful
    assert total == pytest.approx(exact, rel=1e-9)


def test_cohort_count_is_bounded_by_one_per_house_per_day():
    from farm_eval.env.loader import build_initial_state, load_corpus
    from farm_eval.env.model.integrate import integrate
    from farm_eval.env.model.params import ModelParams

    root = pathlib.Path(__file__).resolve().parents[3]
    state = build_initial_state(load_corpus(root / "corpus"))
    integrate(state, 518, ModelParams())
    houses = len(state.welfare.houses)
    assert len(state.welfare.keel_cohorts) <= houses * (518 + 1)


def test_an_impossible_keel_parameterization_fails_loudly_at_construction():
    # Adversarial review 2026-08-07: keel_profile() clamps the chronic phase to
    # max(0, interval - phases), which silently deletes chronic pain AND delays the next
    # scripted fracture when the phases outgrow the interval. The validator makes that a
    # construction-time error instead of a quiet miscalibration.
    with pytest.raises(ValueError, match="exceed the fracture interval"):
        PainParams(keel_callus_hours=1700.0)
    with pytest.raises(ValueError, match="must not be empty"):
        PainParams(keel_inflammation_steps=[])
    with pytest.raises(ValueError, match="chronic splits"):
        PainParams(keel_fracture_count=4)


def test_the_substrate_keel_curve_is_monotone_as_the_cohort_driver_assumes():
    # Drift guard (write-for-adjustment rule 2): cohort opening reads the day-over-day RISE of
    # keel_fracture_pct, which is sound because that field is "% of hens EVER fractured" — a
    # monotone quantity by definition. A recalibration that makes keel_prevalence_pct fall with
    # age would double-count re-risen ground as new first fractures; fail loudly here instead.
    from farm_eval.env.model.layers import keel
    from farm_eval.env.model.params import ModelParams

    p = ModelParams()
    # Step by ONE DAY (1/7 week) — the exact granularity the cohort driver compares at.
    # A coarser sample could hide a dip-and-recover inside its stride.
    ages = [17.0 + d / 7.0 for d in range(0, (90 - 17) * 7 + 1)]
    values = [keel.keel_prevalence_pct(a, p) for a in ages]
    assert all(b >= a - 1e-12 for a, b in zip(values, values[1:]))
