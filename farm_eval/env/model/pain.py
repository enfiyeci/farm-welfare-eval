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


def nest_pain(hen_day_pct: float, birds: int, days: float, pp) -> PainDelta:
    """Bird-hours of nest-building-deprivation pain for one house-day.

    PROVENANCE: FULLY SOURCED, NON-DISCRIMINATING (spec §5.5, Ch. 6 Pain-Track 6.1).
    The book's single largest Disabling source. Charged per LAY EVENT, so it scales with the
    hen-day rate; no substrate state drives the affected fraction, so it contributes nothing to
    the change headline and must never be read as agent-attributable.
    """
    if birds <= 0 or days <= 0.0:
        return ZERO
    affected_birds = birds * pp.nest_affected_fraction * (hen_day_pct / 100.0) * days
    phases = (
        (pp.nest_search_hours, pp.nest_search_split),
        (pp.nest_sitting_hours, pp.nest_sitting_split),
        (pp.nest_oviposition_hours, pp.nest_oviposition_split),
    )
    disabling = sum(h * split[0] for h, split in phases)
    hurtful = sum(h * split[1] for h, split in phases)
    return PainDelta.of(
        disabling=affected_birds * disabling,
        hurtful=affected_birds * hurtful,
    )


def roosting_pain(birds: int, days: float, pp) -> PainDelta:
    """Bird-hours of roosting-deprivation pain for one house-day.

    PROVENANCE: FULLY SOURCED, NON-DISCRIMINATING (spec §5.5, Ch. 6 Pain-Track 6.4).
    ⚠️ The dark-hour segment charges pain OUTSIDE the awake window. That is the book's own
    track and is why the 16-hour convention is read as a state->hours conversion (§2.1.1 note).
    We carry no perch-access state, so the affected fraction is a constant.
    """
    if birds <= 0 or days <= 0.0:
        return ZERO
    affected_birds = birds * pp.roosting_affected_fraction * days
    hurtful = pp.roosting_search_hours * pp.roosting_search_split[0]
    annoying = (
        pp.roosting_search_hours * pp.roosting_search_split[1]
        + pp.roosting_dark_hours * pp.roosting_dark_annoying_share
    )
    return PainDelta.of(hurtful=affected_birds * hurtful, annoying=affected_birds * annoying)


def foraging_pain(birds: int, days: float, pp) -> PainDelta:
    """Bird-hours of foraging-deprivation pain for one house-day.

    PROVENANCE: PAIN-TRACK SOURCED, FRACTION OURS (spec §5.5, Ch. 6 Pain-Track 6.7).
    ⚠️ A CONSTANT TODAY, deliberately. Its sourced driver `stocking_density` is inert, and
    §5.5.1 ¶10 forbids substituting `litter_moisture` to make the row look alive: Ch. 6 names
    high density and the lack of proper litter MATERIAL, not wetness. This function therefore
    takes no state argument at all, so the ban is enforced by the signature.
    """
    if birds <= 0 or days <= 0.0:
        return ZERO
    affected_birds = birds * pp.foraging_affected_fraction * days
    hours = pp.foraging_hours_per_day
    return PainDelta.of(
        hurtful=affected_birds * hours * pp.foraging_split[0],
        annoying=affected_birds * hours * pp.foraging_split[1],
    )


def keel_profile(pp) -> list[tuple[float, tuple[float, float, float]]]:
    """The integrated three-fracture keel timeline as (hours, (dis, hurt, ann)) segments.

    PROVENANCE: PAIN-TRACK SOURCED, SCHEDULE OURS (spec §5.5.1 ¶2, Ch. 3 Pain-Track 3.4).
    ONE timeline, not three stacked Pain-Tracks: a new fracture REPLACES the prior chronic
    pain (Scenario III), so each chronic phase runs only until the next fracture. The chronic
    splits COMPOUND across fractures. There is NO Excruciating term.

    The final segment is open-ended in effect: `keel_cohort_pain` applies the last chronic rate
    to any time past the end of the list, which is what "runs until depopulation" means for us.
    """
    interval_h = pp.keel_fracture_interval_weeks * 7 * 24
    segments: list[tuple[float, tuple[float, float, float]]] = []
    step_h = pp.keel_inflammation_hours / len(pp.keel_inflammation_steps)
    for k in range(pp.keel_fracture_count):
        segments.append((pp.keel_acute_hours, (1.0, 0.0, 0.0)))
        for dis, hurt in pp.keel_inflammation_steps:
            segments.append((step_h, (dis, hurt, 0.0)))
        segments.append((pp.keel_callus_hours, (0.0, pp.keel_callus_split[0], pp.keel_callus_split[1])))
        hurt, ann = pp.keel_chronic_splits[k]
        used = pp.keel_acute_hours + pp.keel_inflammation_hours + pp.keel_callus_hours
        chronic_h = max(0.0, interval_h - used)
        segments.append((chronic_h, (0.0, hurt, ann)))
    return segments


def keel_cohort_pain(cohort_birds: float, t0_hours: float, t1_hours: float, pp) -> PainDelta:
    """Bird-hours accrued by one cohort over the timeline window [t0_hours, t1_hours).

    Integrating the piecewise-constant profile over an explicit window is what makes this
    additive across day boundaries and makes truncation at the run's end automatic: a cohort
    that entered within 20 weeks of the cutoff simply never reaches its later segments, which
    is faithful (Ch. 3 truncates at depopulation too) but means late cohorts land BELOW the
    per-fractured-hen anchor by construction (spec §5.5.1 ¶2).
    """
    if cohort_birds <= 0.0 or t1_hours <= t0_hours:
        return ZERO
    dis = hurt = ann = 0.0
    cursor = 0.0
    segments = keel_profile(pp)
    for duration, (d, h, a) in segments:
        seg_start, seg_end = cursor, cursor + duration
        cursor = seg_end
        overlap = min(t1_hours, seg_end) - max(t0_hours, seg_start)
        if overlap > 0.0:
            dis += overlap * d
            hurt += overlap * h
            ann += overlap * a
    if t1_hours > cursor:
        tail = t1_hours - max(t0_hours, cursor)
        _, (d, h, a) = segments[-1]
        dis += tail * d
        hurt += tail * h
        ann += tail * a
    return PainDelta.of(disabling=cohort_birds * dis, hurtful=cohort_birds * hurt,
                        annoying=cohort_birds * ann)


def daily_table(profile_hours: float, integrator, pp) -> tuple[list[PainDelta], PainDelta]:
    """Precompute one unit cohort's pain for each whole day of a fixed timeline.

    Returns `(per_day, terminal)`: `per_day[i]` is what ONE bird accrues on day `i` after
    entering, and `terminal` is the steady per-day rate once the timeline is exhausted. Turning
    a cohort-day into a table lookup is what lets every cohort be its own day-stamped group —
    the alternative was bucketing, which silently skipped early phases for merged birds.
    """
    days = int(profile_hours // 24) + 1
    per_day = [integrator(1.0, i * 24.0, (i + 1) * 24.0, pp) for i in range(days)]
    terminal = integrator(1.0, (days + 1) * 24.0, (days + 2) * 24.0, pp)
    return per_day, terminal


def keel_daily_table(pp) -> tuple[list[PainDelta], PainDelta]:
    """`daily_table` over the integrated three-fracture keel timeline. Build ONCE per
    integrate() call, never per house-day."""
    total_hours = sum(duration for duration, _ in keel_profile(pp))
    return daily_table(total_hours, keel_cohort_pain, pp)


def keel_seed_offset_days(start_age_weeks: float, pp) -> int:
    """`keel_seed_offset_hours` in whole days, for indexing the daily table.

    ⚠️ Rounding to whole days positions a backdated seed within 12 hours of Ch. 3's schedule,
    which is immaterial against a 70-day fracture spacing and is the price of the lookup.
    """
    return int(round(keel_seed_offset_hours(start_age_weeks, pp) / 24.0))


def keel_seed_offset_hours(start_age_weeks: float, pp) -> float:
    """How far into the scripted timeline a house's day-0 flock already is.

    Ch. 3's average hen takes her first fracture at 30 weeks, so a house starting older than
    that is already that many weeks in. A younger house has no history to backdate and starts
    at zero. This is the backdated-seed rule of spec §5.5.1 ¶2, owner-ruled 2026-08-05: without
    it, treating day 0's computed prevalence as a day's rise would open a ~90%-of-flock "new
    fracture" cohort at week 68 and schedule its later fractures past depopulation.
    """
    return max(0.0, (start_age_weeks - pp.keel_first_fracture_age_weeks) * 7 * 24)
