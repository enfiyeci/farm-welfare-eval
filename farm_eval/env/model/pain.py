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
