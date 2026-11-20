"""The study's factorial design (spec §11.2).

Scale is CROSSED with species using shared population levels, never bundled into it
(spec §8.2) — a count-sensitive model would otherwise produce a species difference
from population size alone.
"""
from __future__ import annotations

from enum import Enum
from itertools import product

from pydantic import BaseModel, ConfigDict


class Species(str, Enum):
    HEN = "hen"
    SHRIMP = "shrimp"


class Scale(str, Enum):
    """Population levels are shared across species; see params.POPULATION."""

    SMALL = "small"
    LARGE = "large"


class StandardBand(str, Enum):
    """Whether the offer stays inside the species' certification threshold (spec §11.3)."""

    WITHIN = "within"
    BEYOND = "beyond"


class Economics(str, Enum):
    EQUALIZED = "equalized"
    NATURALISTIC = "naturalistic"


class Cell(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    species: Species
    scale: Scale
    standard: StandardBand
    economics: Economics


def framing_cells() -> list[Cell]:
    """The 12 framing-arm cells: 8 equalized (full factorial) + 4 naturalistic."""
    cells = [
        Cell(species=sp, scale=sc, standard=bd, economics=Economics.EQUALIZED)
        for sp, sc, bd in product(Species, Scale, StandardBand)
    ]
    cells += [
        Cell(species=sp, scale=sc, standard=StandardBand.WITHIN,
             economics=Economics.NATURALISTIC)
        for sp, sc in product(Species, Scale)
    ]
    return cells
