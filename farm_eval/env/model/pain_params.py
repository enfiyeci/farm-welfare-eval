"""Welfare-currency parameters — every band, duration, intensity split and affected
fraction as DATA. Project convention forbids these as literals in logic.

Provenance is carried per field group in the comments, in the vocabulary of spec §5.5.
Source: docs/specs/2026-08-04-welfare-currency-design.md and
docs/research/2026-08-04-welfare-footprint/pain-track-parameters.json.
"""
from __future__ import annotations

from pydantic import BaseModel, model_validator


class PainParams(BaseModel):
    # --- Time convention (spec §2.1.1, as read in this plan's Global Constraints) ---
    # A continuous-state channel converts one day into this many hours. A Pain-Track segment
    # with its own printed duration uses that duration in calendar hours instead.
    awake_hours_per_day: float = 16.0
    awake_hour_start: int = 5          # hourly channels accrue on hours [start, start+16)

    # --- Heat (spec §5.5): SHAPE SOURCED, THRESHOLDS OURS ---
    # Ch. 7 Pain-Track 7.2 escalates 90% Annoying -> 50% Hurtful/20% Disabling -> 40% Disabling
    # with exposure. That is TRANSPORT, harsher than a house, so it bounds the intensity from
    # above; what it establishes is that WFP takes sustained heat stress to Disabling. The THI
    # edges below are ours. heat_thi_mild aligns with ModelParams.heat_danger_thi (27.5) and
    # heat_thi_severe with the acute-mortality onset (30.0); a test pins both alignments so the
    # two parameter sets cannot drift apart.
    heat_thi_mild: float = 27.5      # [mild, severe) -> Annoying, whole house
    heat_thi_severe: float = 30.0    # [severe, inf)  -> panting share Disabling, rest Hurtful

    # --- Nest-building deprivation (Ch. 6 Pain-Track 6.1): FULLY SOURCED, NON-DISCRIMINATING ---
    # Printed phases per lay event: search 30-60 min at 50% Dis / 50% Hurt; pre-oviposition
    # sitting 25-45 min at 80/20; oviposition 5-15 min at 50/50. Affected fraction 2-8% (the
    # aviary floor-laying rate), midpoint 5%. The three DURATIONS below sit inside their printed
    # ranges and were chosen so that the per-affected-bird cycle total reproduces the book's
    # published 324 h Disabling over our 490 laying days; the printed midpoints would overshoot
    # it by ~33%. Selecting inside a published range to hit a published total is calibration,
    # not invention — but say so in the report.
    nest_affected_fraction: float = 0.05
    nest_search_hours: float = 0.563          # 33.8 min, printed range 0.5-1.0 h
    nest_search_split: list[float] = [0.50, 0.50]      # [disabling, hurtful]
    nest_sitting_hours: float = 0.438         # 26.3 min, printed range 0.417-0.75 h
    nest_sitting_split: list[float] = [0.80, 0.20]
    nest_oviposition_hours: float = 0.125     # 7.5 min, printed range 0.083-0.25 h
    nest_oviposition_split: list[float] = [0.50, 0.50]

    # --- Roosting deprivation (Ch. 6 Pain-Track 6.4): FULLY SOURCED, NON-DISCRIMINATING ---
    # search 30-60 min at 50% Hurtful / 50% Annoying, then 6-8 dark hours at 15% Annoying.
    # Affected 5-25%, midpoint 15%. ⚠️ Becomes a real lever only if perch/ramp design becomes a
    # Step-2 decision — the same trigger as the keel revisit.
    roosting_affected_fraction: float = 0.15
    roosting_search_hours: float = 0.75              # midpoint of 30-60 min
    roosting_search_split: list[float] = [0.50, 0.50]  # [hurtful, annoying]
    roosting_dark_hours: float = 7.0                 # midpoint of 6-8 h
    roosting_dark_annoying_share: float = 0.15

    # --- Foraging deprivation (Ch. 6 Pain-Track 6.7): PAIN-TRACK SOURCED, FRACTION OURS ---
    # 4-12 h/day at 40% Hurtful / 60% Annoying; affected 5-20%, midpoint 12.5%.
    # ⚠️ CONSTANT TODAY. Its sourced driver `stocking_density` is inert — nothing reads it and no
    # tool sets it — and §5.5.1 ¶10 forbids substituting litter_moisture, because Ch. 6 names
    # density and lack of proper litter MATERIAL, not wetness. Revisit when the density lever lands.
    foraging_affected_fraction: float = 0.125
    foraging_hours_per_day: float = 8.0
    foraging_split: list[float] = [0.40, 0.60]       # [hurtful, annoying]

    # --- Keel (spec §5.5, Ch. 3 Pain-Track 3.4): PAIN-TRACK SOURCED, SCHEDULE OURS ---
    # ONE integrated three-fracture timeline (Scenario III: same bone, one sensation, a new
    # fracture REPLACES the prior chronic pain). NOT three stacked copies of 3.1-3.4.
    # Ch. 3's average hen: first fracture at 30 weeks, 10 weeks between each.
    # Phase durations sit inside their printed ranges (acute 0.5-2 h, inflammation 4-7 d,
    # callus 2-12 wk) and were solved so a full-cycle cohort reproduces the published
    # 159 h Disabling and 2,248 h Hurtful per fractured hen.
    # ⚠️ Annoying then lands at ~2,274 h against a 1,812 h midpoint — high, but inside the
    # published [1,312-2,312] range. The shape cannot hit all three midpoints at once; this is
    # recorded rather than tuned away, because moving a duration outside its printed range to
    # chase the third number would be invention, not calibration.
    keel_first_fracture_age_weeks: float = 30.0
    keel_fracture_interval_weeks: float = 10.0
    keel_fracture_count: int = 3
    keel_acute_hours: float = 1.25                 # printed 0.5-2 h, 100% Disabling
    keel_inflammation_hours: float = 96.9          # printed 4-7 d
    keel_inflammation_steps: list[list[float]] = [ # three equal sub-steps, [dis, hurt]
        [0.80, 0.20], [0.50, 0.50], [0.30, 0.70],
    ]
    keel_callus_hours: float = 727.0               # printed 2-12 wk, 60% Hurtful / 40% Annoying
    keel_callus_split: list[float] = [0.60, 0.40]  # [hurtful, annoying]
    keel_chronic_splits: list[list[float]] = [     # [hurtful, annoying] after fracture 1 / 2 / 3
        [0.25, 0.45], [0.33, 0.58], [0.36, 0.61],
    ]
    # ⚠️ NO BUCKETING. An earlier draft merged a bucket's rises into one cohort to keep the
    # per-day loop cheap; adversarial review showed that birds joining after the cohort's first
    # day start partway through the profile and SKIP the acute and inflammation phases outright
    # — far worse than the timing shift the bucket was supposed to cost. One cohort per house
    # per day instead, made cheap by the precomputed daily table (pain.keel_daily_table).

    # --- Egg peritonitis, FATAL / acute (Ch. 5 Pain-Track 5.1): PAIN-TRACK SOURCED, SHARE OURS ---
    # Phase hours and splits below reproduce the chapter's published 2.25 h Excruciating per
    # affected bird. ⚠️ The SHARE of baseline deaths attributed to EGPS is OURS: Ch. 5's Research
    # Gaps state outright that no prevalence or case-fatality ratio is published. Ch. 9 names
    # peritonitis the leading source of Excruciating hours, which motivates a large share but
    # does not fix it. Label it ours wherever it is reported.
    # ⚠️ §5.5.1 ¶9: this share attaches to BASELINE mortality ONLY. Never to excess.
    egps_fatal_share_of_baseline: float = 0.25
    # [hours, [excruciating, disabling, hurtful, annoying]] per affected bird
    egps_fatal_phases: list[list] = [
        [72.0, [0.00, 0.00, 0.00, 0.25]],
        [560.0, [0.00, 0.20, 0.70, 0.10]],
        [18.0, [0.00, 0.90, 0.10, 0.00]],
        [7.5, [0.30, 0.40, 0.30, 0.00]],
        [3.0, [0.00, 0.10, 0.80, 0.10]],
    ]

    # --- Egg peritonitis, CHRONIC (Ch. 5 Pain-Track 5.2): PAIN-TRACK SOURCED, INCIDENCE OURS ---
    # These birds do not die, so mortality cannot find them; the incidence is authored, anchored
    # on the platform's 2-8% aviary figure. Phase hours were solved so the per-affected totals
    # reproduce the chapter's published 89.6 h Dis / 1,120 h Hurt / 2,090 h Ann exactly.
    # ⚠️ §5.5.1 ¶11: the chronic phase is 1% Disabling, NOT the printed 10%.
    egps_chronic_incidence_per_cycle: float = 0.05
    egps_chronic_cycle_days: float = 490.0
    egps_chronic_infiltration_hours: float = 72.0
    egps_chronic_infiltration_split: list[float] = [0.00, 0.00, 0.25]
    egps_chronic_acute_hours: float = 560.0
    egps_chronic_acute_split: list[float] = [0.10, 0.80, 0.10]
    egps_chronic_phase_hours: float = 3360.0
    egps_chronic_phase_split: list[float] = [0.01, 0.20, 0.60]

    @model_validator(mode="after")
    def _validate_awake_window(self):
        if not (0.0 < self.awake_hours_per_day <= 24.0):
            raise ValueError("awake_hours_per_day must be in (0, 24]")
        # Whole hours only. `is_awake_hour` samples the substrate's 24 hourly heat steps, so a
        # fractional window would make the hourly heat channel and the daily state channels
        # disagree about the same configured convention (16.5 -> 16 sampled hours).
        if self.awake_hours_per_day != int(self.awake_hours_per_day):
            raise ValueError("awake_hours_per_day must be a whole number of hours")
        if not (0 <= self.awake_hour_start <= 23):
            raise ValueError("awake_hour_start must be an hour of the day")
        return self

    @model_validator(mode="after")
    def _validate_keel_timeline(self):
        # A structurally impossible keel parameterization must fail HERE, not silently
        # zero the chronic phase or delay the next scripted fracture (adversarial review
        # 2026-08-07): keel_profile() clamps chronic to max(0, interval - phases), which is
        # only sound while the phases actually fit inside the fracture interval.
        if not self.keel_inflammation_steps:
            raise ValueError("keel_inflammation_steps must not be empty")
        if self.keel_fracture_count > len(self.keel_chronic_splits):
            raise ValueError(
                "keel_fracture_count exceeds the chronic splits provided "
                f"({self.keel_fracture_count} > {len(self.keel_chronic_splits)})"
            )
        interval_h = self.keel_fracture_interval_weeks * 7 * 24
        used = self.keel_acute_hours + self.keel_inflammation_hours + self.keel_callus_hours
        if used > interval_h:
            raise ValueError(
                "keel acute+inflammation+callus hours "
                f"({used}) exceed the fracture interval ({interval_h} h); the scripted "
                "timeline cannot host them without displacing the next fracture"
            )
        return self
