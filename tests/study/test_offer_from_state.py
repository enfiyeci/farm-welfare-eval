import pytest
from farm_eval.study.cells import Cell, Economics, Scale, Species, StandardBand
from farm_eval.study.offer import build_offer, build_offer_from_state
from farm_eval.study.params import BASELINE_MORTALITY, POPULATION, Rung

CELL = Cell(
    species=Species.HEN,
    scale=Scale.LARGE,
    standard=StandardBand.BEYOND,
    economics=Economics.EQUALIZED,
)


def test_matches_build_offer_at_the_original_baseline():
    # proposed index 150 == build_offer's density_step 0.50 (a rung anchor), so the
    # dose curve and the rung table agree and the two builders must coincide.
    n0 = float(POPULATION[Scale.LARGE])
    m0 = BASELINE_MORTALITY[Species.HEN]
    a = build_offer(CELL, Rung(density_step=0.50, added_mortality_pp=9.0), gain=0.0)
    b = build_offer_from_state(
        CELL, n0=n0, m0=m0, current_index=100.0, proposed_index=150.0
    )
    assert b.n1 == pytest.approx(a.n1)
    assert b.m1 == pytest.approx(a.m1)
    assert b.delta_deaths == pytest.approx(a.delta_deaths)


def test_compounds_from_an_accumulated_state():
    # A unit already at index 130 (m0 must equal baseline + dose(1.30)) going to 145.
    from farm_eval.study.params import dose_response_pp

    n0 = float(POPULATION[Scale.LARGE]) * 1.30
    m0 = BASELINE_MORTALITY[Species.HEN] + dose_response_pp(1.30) / 100.0
    o = build_offer_from_state(
        CELL, n0=n0, m0=m0, current_index=130.0, proposed_index=145.0
    )
    assert o.n1 == pytest.approx(float(POPULATION[Scale.LARGE]) * 1.45)
    assert o.m1 == pytest.approx(
        BASELINE_MORTALITY[Species.HEN] + dose_response_pp(1.45) / 100.0
    )
    assert o.delta_deaths == pytest.approx(o.n1 * o.m1 - n0 * m0)
    assert o.gain != 0.0  # gain computed from the P&L, not left at the placeholder


def test_gain_is_the_derived_gain():
    from farm_eval.study.economics import gain_for

    n0 = float(POPULATION[Scale.LARGE])
    m0 = BASELINE_MORTALITY[Species.HEN]
    o = build_offer_from_state(
        CELL, n0=n0, m0=m0, current_index=100.0, proposed_index=140.0
    )
    assert o.gain == pytest.approx(gain_for(o))
