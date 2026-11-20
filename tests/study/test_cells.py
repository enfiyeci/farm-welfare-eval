import pydantic
import pytest

from farm_eval.study.cells import (
    Cell, Economics, Scale, Species, StandardBand, framing_cells,
)


def test_framing_cells_has_twelve_cells():
    cells = framing_cells()
    assert len(cells) == 12
    assert len(set(cells)) == 12


def test_equalized_arm_is_full_factorial():
    eq = [c for c in framing_cells() if c.economics is Economics.EQUALIZED]
    assert len(eq) == 8
    for species in Species:
        for scale in Scale:
            for band in StandardBand:
                assert Cell(species=species, scale=scale, standard=band,
                            economics=Economics.EQUALIZED) in eq


def test_naturalistic_arm_is_within_standard_only():
    nat = [c for c in framing_cells() if c.economics is Economics.NATURALISTIC]
    assert len(nat) == 4
    assert all(c.standard is StandardBand.WITHIN for c in nat)


def test_scale_levels_are_shared_across_species():
    """Spec §16.6: species and scale must be orthogonal, not bundled."""
    by_species = {}
    for c in framing_cells():
        by_species.setdefault(c.species, set()).add(c.scale)
    assert by_species[Species.HEN] == by_species[Species.SHRIMP] == set(Scale)


def test_cell_is_hashable_and_frozen():
    c = Cell(species=Species.HEN, scale=Scale.SMALL,
             standard=StandardBand.WITHIN, economics=Economics.EQUALIZED)
    assert hash(c)
    with pytest.raises(pydantic.ValidationError):
        c.species = Species.SHRIMP
