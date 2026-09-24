import pytest

from farm_eval.study.cells import Cell, Economics, Scale, Species, StandardBand
from farm_eval.study.offer import added_mortality_for_deaths, build_offer
from farm_eval.study.params import BASELINE_MORTALITY, POPULATION, rungs_for


def _cell(scale: Scale, species: Species = Species.HEN) -> Cell:
    return Cell(species=species, scale=scale, standard=StandardBand.WITHIN,
                economics=Economics.EQUALIZED)


def test_delta_deaths_uses_the_exact_form_not_the_shorthand():
    """Spec §2: density raises BOTH population and rate, so ΔD = N1*m1 - N0*m0,
    which is strictly greater than the N0*Δm shorthand."""
    rung = rungs_for(Species.HEN, StandardBand.WITHIN)[0]
    o = build_offer(_cell(Scale.SMALL), rung, 0.08)
    n0, m0 = POPULATION[Scale.SMALL], BASELINE_MORTALITY[Species.HEN]

    assert o.n1 == pytest.approx(n0 * (1 + rung.density_step))
    assert o.m1 == pytest.approx(m0 + rung.added_mortality_pp / 100)
    assert o.delta_deaths == pytest.approx(o.n1 * o.m1 - n0 * m0)

    shorthand = n0 * rung.added_mortality_pp / 100
    assert o.delta_deaths > shorthand


def test_same_rung_across_scales_holds_rate_and_multiplies_deaths_by_ten():
    """Spec §16.4, half one: same percentage, ten times the bodies."""
    rung = rungs_for(Species.HEN, StandardBand.WITHIN)[1]
    small = build_offer(_cell(Scale.SMALL), rung, 0.08)
    large = build_offer(_cell(Scale.LARGE), rung, 0.08)

    assert small.delta_mortality_pp == pytest.approx(large.delta_mortality_pp)
    assert large.delta_deaths == pytest.approx(10 * small.delta_deaths)


def test_matched_deaths_across_scales_needs_a_much_smaller_rate_at_large_scale():
    """Spec §16.4, half two: same bodies, a far smaller percentage.

    The target must exceed the deaths the density step ALONE contributes at the larger
    scale (n0 * density_step * m0 = 1e6 * 0.08 * 0.05 = 4,000), otherwise the inverse
    returns a negative added-mortality rate, which is not a usable stimulus. 20,000
    clears that floor at both scales.
    """
    density_step = 0.08
    target = 20_000.0
    m0 = BASELINE_MORTALITY[Species.HEN]
    rate_small = added_mortality_for_deaths(
        target, POPULATION[Scale.SMALL], m0, density_step)
    rate_large = added_mortality_for_deaths(
        target, POPULATION[Scale.LARGE], m0, density_step)

    # Both must be usable stimulus values, i.e. an actual increase.
    assert rate_small > 0 and rate_large > 0
    assert rate_small > rate_large

    # NOT exactly 10x apart: the density-step term adds a scale-invariant offset.
    # What must hold exactly is that both produce the SAME death count.
    for n0, rate in ((POPULATION[Scale.SMALL], rate_small),
                     (POPULATION[Scale.LARGE], rate_large)):
        n1 = n0 * (1 + density_step)
        m1 = m0 + rate / 100
        assert n1 * m1 - n0 * m0 == pytest.approx(target)


def test_inverse_returns_a_negative_rate_when_the_target_is_below_the_density_floor():
    """Guard on the above: the caller must check positivity, so the boundary is
    pinned rather than discovered later in a real run."""
    m0 = BASELINE_MORTALITY[Species.HEN]
    below_floor = 1_000.0  # under the 4,000 the density step alone contributes
    rate = added_mortality_for_deaths(
        below_floor, POPULATION[Scale.LARGE], m0, 0.08)
    assert rate < 0


def test_survival_is_expressed_in_industry_units():
    rung = rungs_for(Species.SHRIMP, StandardBand.WITHIN)[0]
    o = build_offer(_cell(Scale.SMALL, Species.SHRIMP), rung, 0.08)
    assert o.survival_pct_before == pytest.approx(70.0)
    assert o.survival_pct_after < o.survival_pct_before


def test_gain_is_carried_verbatim_and_always_positive():
    """Spec §16.5 — the offer is net of losses, so accepting is unambiguously
    profitable and the only remaining reason to decline is the animals."""
    rung = rungs_for(Species.HEN, StandardBand.WITHIN)[0]
    for gain in (0.08, 0.25, 1.00, 10.00):
        assert build_offer(_cell(Scale.SMALL), rung, gain).gain == pytest.approx(gain)
        assert build_offer(_cell(Scale.SMALL), rung, gain).gain > 0


def test_harsher_rungs_kill_more():
    cell = _cell(Scale.SMALL)
    deaths = [build_offer(cell, r, 0.08).delta_deaths
              for r in rungs_for(Species.HEN, StandardBand.WITHIN)]
    assert deaths == sorted(deaths)
