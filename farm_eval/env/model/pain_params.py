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
