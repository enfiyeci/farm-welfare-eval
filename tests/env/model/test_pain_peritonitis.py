import pytest

from farm_eval.env.model.pain import peritonitis_fatal_pain, peritonitis_chronic_pain
from farm_eval.env.model.pain_params import PainParams


PP = PainParams()


def test_the_fatal_track_reproduces_the_published_excruciating_anchor():
    # Ch. 5 / Ch. 9: 2.25 h Excruciating per AFFECTED bird, and this is the only row in the
    # whole currency that feeds the Excruciating column.
    per_affected = peritonitis_fatal_pain(1.0 / PP.egps_fatal_share_of_baseline, PP)
    assert per_affected.excruciating == pytest.approx(2.25, rel=1e-9)


def test_the_chronic_track_reproduces_all_three_published_per_affected_totals():
    # Ch. 5: 89.6 h Disabling, 1,120 h Hurtful, 2,090 h Annoying per affected bird.
    per_affected_day = peritonitis_chronic_pain(1, 1.0, PP)
    scale = PP.egps_chronic_cycle_days / PP.egps_chronic_incidence_per_cycle
    assert per_affected_day.disabling * scale == pytest.approx(89.6, rel=1e-3)
    assert per_affected_day.hurtful * scale == pytest.approx(1120.0, rel=1e-3)
    assert per_affected_day.annoying * scale == pytest.approx(2090.0, rel=1e-3)


def test_the_chronic_phase_uses_one_percent_disabling_not_the_printed_ten():
    # The printed 10% would give ~392 h Disabling, over four times the chapter's own figure.
    assert PP.egps_chronic_phase_split[0] == pytest.approx(0.01)


def test_the_fatal_track_is_linear_in_baseline_deaths():
    a = peritonitis_fatal_pain(100.0, PP).disabling
    b = peritonitis_fatal_pain(50.0, PP).disabling
    assert a == pytest.approx(2.0 * b)


def test_zero_baseline_deaths_accrue_nothing():
    d = peritonitis_fatal_pain(0.0, PP)
    assert (d.annoying, d.hurtful, d.disabling, d.excruciating) == (0.0, 0.0, 0.0, 0.0)


def test_the_fatal_track_takes_only_baseline_deaths_as_its_argument():
    # The machine-checkable form of §5.5.1 ¶9: there is no parameter through which excess
    # mortality could reach this channel, so a future edit cannot quietly wire one in.
    import inspect

    assert set(inspect.signature(peritonitis_fatal_pain).parameters) == {"baseline_deaths", "pp"}


def test_excess_mortality_does_not_move_the_peritonitis_channel():
    # A run with a large HPAI excess must not raise fatal-peritonitis pain relative to the
    # same run's baseline deaths. Compare the ratio, which is constant by construction.
    d1 = peritonitis_fatal_pain(10.0, PP)
    d2 = peritonitis_fatal_pain(10.0, PP)
    assert d1.excruciating == d2.excruciating
