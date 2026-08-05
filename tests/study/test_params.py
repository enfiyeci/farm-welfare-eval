import pytest

from farm_eval.study.cells import Economics, Scale, Species, StandardBand
from farm_eval.study.params import (
    BASELINE_MORTALITY, GAIN_LADDER, PER_ANIMAL_VALUE_USD, POPULATION,
    REALISM_ENVELOPE, envelope_status, rungs_for,
)


def test_population_levels_are_shared_and_decade_apart():
    assert POPULATION[Scale.SMALL] == 100_000
    assert POPULATION[Scale.LARGE] == 1_000_000
    assert POPULATION[Scale.LARGE] == 10 * POPULATION[Scale.SMALL]


def test_equalized_arm_prices_species_identically():
    """Spec §16.6 — equal per-animal value is what isolates species identity."""
    hen = PER_ANIMAL_VALUE_USD[(Economics.EQUALIZED, Species.HEN)]
    shrimp = PER_ANIMAL_VALUE_USD[(Economics.EQUALIZED, Species.SHRIMP)]
    assert hen == shrimp


def test_naturalistic_arm_prices_species_differently():
    hen = PER_ANIMAL_VALUE_USD[(Economics.NATURALISTIC, Species.HEN)]
    shrimp = PER_ANIMAL_VALUE_USD[(Economics.NATURALISTIC, Species.SHRIMP)]
    assert hen > 10 * shrimp


def test_gain_ladder_is_ascending_and_all_positive():
    """Spec §16.5 — declining must never be the financially superior choice."""
    assert all(g > 0 for g in GAIN_LADDER)
    assert list(GAIN_LADDER) == sorted(GAIN_LADDER)


def test_envelope_marks_top_rung_abstract_for_both_species():
    """Spec §3.1 — +1000% is supported by nothing and is an abstract probe."""
    for species in Species:
        assert envelope_status(species, 0.08) == "in_envelope"
        assert envelope_status(species, 10.00) == "abstract_probe"


def test_rungs_are_ascending_in_both_dimensions():
    """Both dimensions, as the name says: a harsher rung must mean both more crowding
    and more mortality, or the manipulation is not monotone in the thing it varies."""
    for species in Species:
        for band in StandardBand:
            rungs = rungs_for(species, band)
            assert len(rungs) >= 4
            assert [r.added_mortality_pp for r in rungs] == sorted(
                r.added_mortality_pp for r in rungs)
            assert [r.density_step for r in rungs] == sorted(
                r.density_step for r in rungs)
            assert all(r.density_step > 0 for r in rungs)


def test_beyond_band_rungs_are_strictly_harsher_than_within_band():
    """Spec §11.3 — the bands must not overlap, or the contrast means nothing."""
    for species in Species:
        within = rungs_for(species, StandardBand.WITHIN)
        beyond = rungs_for(species, StandardBand.BEYOND)
        assert min(r.added_mortality_pp for r in beyond) > max(
            r.added_mortality_pp for r in within)


def test_baseline_mortality_matches_researched_surround():
    """Surround values ARE source-bound (§0.1.1). Hen re-anchored per the hen-rescue
    pass; shrimp from ASC audit data for fed-and-aerated ponds."""
    assert BASELINE_MORTALITY[Species.HEN] == pytest.approx(0.05)
    assert BASELINE_MORTALITY[Species.SHRIMP] == pytest.approx(0.30)
