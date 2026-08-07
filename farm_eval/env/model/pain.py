"""Welfare currency — cumulative time in pain, in bird-hours, by intensity category.

One pure function per condition. Each reads house state and returns a PainDelta; NONE of
them mutates welfare state, adds a compartment or changes a rate (spec §5.3). Every
function's docstring carries its provenance label in the vocabulary of spec §5.5.
"""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict

# Canonical channel order. Sorted, so the rate series and every report iterate deterministically.
PAIN_CHANNELS: tuple[str, ...] = (
    "ammonia",
    "dustbathing",
    "feather",
    "footpad",
    "foraging",
    "heat",
    "keel",
    "mortality_baseline",
    "mortality_heat",
    "mortality_hpai",
    "mortality_staffing",
    "nest",
    "peritonitis_chronic",
    "peritonitis_fatal",
    "red_mite",
    "roosting",
)


class PainDelta(BaseModel):
    """Bird-hours (or worker-hours) accrued by ONE channel in ONE step. Immutable."""

    model_config = ConfigDict(frozen=True)

    annoying: float = 0.0
    hurtful: float = 0.0
    disabling: float = 0.0
    excruciating: float = 0.0

    @classmethod
    def of(cls, *, annoying: float = 0.0, hurtful: float = 0.0,
           disabling: float = 0.0, excruciating: float = 0.0) -> "PainDelta":
        return cls(annoying=annoying, hurtful=hurtful,
                   disabling=disabling, excruciating=excruciating)

    def __add__(self, other: "PainDelta") -> "PainDelta":
        return PainDelta(
            annoying=self.annoying + other.annoying,
            hurtful=self.hurtful + other.hurtful,
            disabling=self.disabling + other.disabling,
            excruciating=self.excruciating + other.excruciating,
        )

    def scaled(self, factor: float) -> "PainDelta":
        return PainDelta(
            annoying=self.annoying * factor,
            hurtful=self.hurtful * factor,
            disabling=self.disabling * factor,
            excruciating=self.excruciating * factor,
        )


ZERO = PainDelta()


def is_awake_hour(hour: int, pp) -> bool:
    """True if `hour` lies in the awake window [awake_hour_start, +awake_hours_per_day).

    Wraps past midnight, so a window that starts late in the day still yields a contiguous
    16 hours. Hourly channels accrue only inside it (spec §2.1.1 convention 1).
    """
    span = int(round(pp.awake_hours_per_day))
    return any((pp.awake_hour_start + k) % 24 == hour for k in range(span))


def heat_pain(thi: float, panting_fraction: float, birds: int, hours: float, pp) -> PainDelta:
    """Bird-hours of heat pain for one hourly house-step.

    PROVENANCE: SHAPE SOURCED, THRESHOLDS OURS (spec §5.5).

    Bands are MUTUALLY EXCLUSIVE and the population split at the severe band sums to exactly
    100% (spec §5.5.1 ¶6): below `heat_thi_mild` nothing; in the mild band the whole house is
    Annoying and panting is ignored; at or above `heat_thi_severe` the panting share is
    Disabling and the remainder Hurtful. No bird is ever counted in two categories.
    """
    if not (0.0 <= panting_fraction <= 1.0):
        raise ValueError(f"panting_fraction must be in [0, 1], got {panting_fraction}")
    bird_hours = birds * hours
    if bird_hours <= 0.0 or thi < pp.heat_thi_mild:
        return ZERO
    if thi < pp.heat_thi_severe:
        return PainDelta.of(annoying=bird_hours)
    return PainDelta.of(
        disabling=bird_hours * panting_fraction,
        hurtful=bird_hours * (1.0 - panting_fraction),
    )
