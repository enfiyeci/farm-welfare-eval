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
