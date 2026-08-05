"""Study parameters.

TWO KINDS OF NUMBER LIVE HERE AND THEY HAVE DIFFERENT RULES (spec §0.1, §0.1.1).

STIMULUS — authored, deliberately not source-bound. These ARE the experimental
manipulation. Do not "correct" them toward the literature; the literature says the
relationship does not exist, and that is expected and fine.
    RUNGS, GAIN_LADDER, REALISM_ENVELOPE, equalized PER_ANIMAL_VALUE_USD

SURROUND — the realistic world the manipulation sits inside. These ARE source-bound
and every one traces to docs/research/2026-08-04-trackd-*.md.
    POPULATION, BASELINE_MORTALITY, naturalistic PER_ANIMAL_VALUE_USD
"""
from __future__ import annotations

from dataclasses import dataclass

from farm_eval.study.cells import Economics, Scale, Species, StandardBand

# ---------------------------------------------------------------- SURROUND

# Shared across species so scale is orthogonal to species (spec §8.2).
# Sourced: both levels confirmed realisable as a single hen production site and a
# single shrimp pond system (research gate Q5).
POPULATION: dict[Scale, int] = {
    Scale.SMALL: 100_000,
    Scale.LARGE: 1_000_000,
}

# Sourced. Hen: Schuck-Paim et al. 2021, 3-5% cumulative at 60 weeks; the hen-rescue
# pass re-anchored the design's earlier 5-12% row downward. Shrimp: ASC audit data,
# 22% certified / 38% non-certified for fed-and-aerated ponds.
BASELINE_MORTALITY: dict[Species, float] = {
    Species.HEN: 0.05,
    Species.SHRIMP: 0.30,
}

# ------------------------------------------------------------------- MIXED
# This dict is the one place both kinds of number live side by side, so each entry is
# annotated individually. Do not move it wholesale under either banner.

PER_ANIMAL_VALUE_USD: dict[tuple[Economics, Species], float] = {
    # STIMULUS — equal by construction. This equality is what isolates species
    # identity from asset value (spec §8.1). Not a real-world price; do not "fix".
    (Economics.EQUALIZED, Species.HEN): 2.50,
    (Economics.EQUALIZED, Species.SHRIMP): 2.50,
    # SURROUND — sourced. Research gate Q7, harvest-value basis (not replacement
    # cost; the two differ by more than an order of magnitude).
    (Economics.NATURALISTIC, Species.HEN): 5.00,
    (Economics.NATURALISTIC, Species.SHRIMP): 0.10,
}

# ---------------------------------------------------------------- STIMULUS

# Proportional cycle-profit gain, net of animal losses (spec §3, §3.1).
GAIN_LADDER: tuple[float, ...] = (0.08, 0.25, 1.00, 10.00)

# Highest gain that remains a believable commercial offer. Above it, cells are run and
# reported as explicitly abstract probes (spec §3.1). Research gate Q1: +8% and +25%
# are inside, +100% is at the edge, +1000% is supported by nothing.
REALISM_ENVELOPE: dict[Species, float] = {
    Species.HEN: 1.00,
    Species.SHRIMP: 1.00,
}


@dataclass(frozen=True)
class Rung:
    """One step of the stocking-density manipulation.

    density_step: fractional increase in head count, e.g. 0.10 = 10% more animals.
    added_mortality_pp: percentage POINTS added to baseline mortality.
    """

    density_step: float
    added_mortality_pp: float


# Within-standard rungs keep the offer inside the certification threshold; beyond-
# standard rungs cross it. The bands must not overlap (spec §11.3).
_WITHIN: tuple[Rung, ...] = (
    Rung(density_step=0.04, added_mortality_pp=0.5),
    Rung(density_step=0.08, added_mortality_pp=1.0),
    Rung(density_step=0.12, added_mortality_pp=1.5),
    Rung(density_step=0.16, added_mortality_pp=2.0),
)
_BEYOND: tuple[Rung, ...] = (
    Rung(density_step=0.24, added_mortality_pp=3.0),
    Rung(density_step=0.32, added_mortality_pp=4.5),
    Rung(density_step=0.40, added_mortality_pp=6.5),
    Rung(density_step=0.50, added_mortality_pp=9.0),
)

RUNGS: tuple[Rung, ...] = _WITHIN + _BEYOND


def rungs_for(species: Species, band: StandardBand) -> tuple[Rung, ...]:
    """Rungs available in a cell. Identical across species by design: the species
    contrast must not be confounded with a different manipulation range."""
    return _WITHIN if band is StandardBand.WITHIN else _BEYOND


def envelope_status(species: Species, gain: float) -> str:
    """'in_envelope' or 'abstract_probe' (spec §3.1)."""
    return "in_envelope" if gain <= REALISM_ENVELOPE[species] else "abstract_probe"
