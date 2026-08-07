"""Guards for the extended-ladder probe's own arithmetic.

The probe's whole interpretive value rests on the survivor-flip point being right:
below it a decline is animal-regarding, above it a decline is explained by the
contract paying per survivor. A wrong flip point would mislabel the finding.
"""
from farm_eval.study.cells import Species
from farm_eval.study.offer import build_offer
from farm_eval.study.params import BASELINE_MORTALITY, Rung
from scripts.probe_extended_ladder import (
    DENSITY_STEP, ceiling_pp, rungs_for_species, survivor_flip_pp,
)


def _survivors(species: Species, pp: float) -> tuple[float, float]:
    from farm_eval.study.cells import Cell, Economics, Scale, StandardBand
    cell = Cell(species=species, scale=Scale.LARGE, standard=StandardBand.BEYOND,
                economics=Economics.EQUALIZED)
    o = build_offer(cell, Rung(density_step=DENSITY_STEP, added_mortality_pp=pp), 0.08)
    return o.n0 * (1.0 - o.m0), o.n1 * (1.0 - o.m1)


def test_survivor_flip_point_is_where_survivors_actually_stop_rising():
    for species in Species:
        flip = survivor_flip_pp(species)
        before_0, before_1 = _survivors(species, flip - 0.5)
        assert before_1 > before_0, f"{species}: below the flip, survivors must rise"
        after_0, after_1 = _survivors(species, flip + 0.5)
        assert after_1 < after_0, f"{species}: above the flip, survivors must fall"


def test_the_ladder_never_proposes_an_offer_where_nothing_survives():
    for species in Species:
        limit = ceiling_pp(species)
        assert limit == (1.0 - BASELINE_MORTALITY[species]) * 100.0
        for rung in rungs_for_species(species):
            assert rung.added_mortality_pp < limit
            _, survivors_after = _survivors(species, rung.added_mortality_pp)
            assert survivors_after > 0


def test_shrimp_ladder_is_shorter_than_hen_because_its_baseline_is_higher():
    """Shrimp start at 30% mortality, so they hit 100% sooner. The species run
    different ladder lengths and that must not be silently equalised."""
    hen = [r.added_mortality_pp for r in rungs_for_species(Species.HEN)]
    shrimp = [r.added_mortality_pp for r in rungs_for_species(Species.SHRIMP)]
    assert shrimp == [pp for pp in hen if pp < 70.0]
    assert max(hen) > max(shrimp)
