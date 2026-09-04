"""Deterministic ambient weather driver.

``make_ambient(weather, start_date)`` returns a closure ``ambient(day, hour)``
that produces ``(temp_c, rh_pct)`` for any integer (day, hour) pair.

No wall-clock, no random.  The only datetime use is
``date.fromisoformat(start_date)`` to derive the day-0 day-of-year from the
fixed corpus string — deterministic by definition.
"""

from __future__ import annotations

import datetime
import math
from typing import Callable

_PEAK_DOY = 205          # late July warmest
_HOUR_PEAK = 15          # afternoon high
_RH_CEILING_PCT = 90.0   # generic ambient-RH band ceiling
_RH_FLOOR_PCT = 35.0     # generic ambient-RH band floor
_RH_SLOPE_PER_F = 1.2    # RH drop per °F above the daily low (generic heuristic)


def _f_to_c(f: float) -> float:
    return (f - 32.0) * 5.0 / 9.0


def flock_age_weeks(age_weeks_at_start: float, day: int) -> float:
    """Return flock age in weeks at *day* (integer day index from eval start).

    Parameters
    ----------
    age_weeks_at_start:
        Age of the flock in weeks on day 0 (from WorldState.age_weeks_at_start).
    day:
        Integer day index (0-based from eval start).
    """
    return age_weeks_at_start + day / 7.0


def make_ambient(weather: dict, start_date: str) -> Callable[[int, int], tuple[float, float]]:
    """Build a deterministic ambient(day, hour) closure from corpus weather data.

    Parameters
    ----------
    weather:
        The ``Corpus.weather`` dict (keys: ``monthly_normals_f``,
        ``diurnal_swing_f``, optional ``heat_events``, optional ``cold_events``).
    start_date:
        ISO date string from ``Corpus.company["start_date"]`` (e.g. "2025-06-09").
        Used to derive day-0 day-of-year — parsing a fixed corpus string is
        not wall-clock use.

    Returns
    -------
    ambient : Callable[[int, int], tuple[float, float]]
        ``ambient(day, hour) -> (temp_c, rh_pct)``
    """
    # Day-0 day-of-year derived from corpus start_date (parsing a fixed string is not wall-clock).
    day0_doy = datetime.date.fromisoformat(start_date).timetuple().tm_yday
    normals = weather["monthly_normals_f"]
    swing_f = float(weather.get("diurnal_swing_f", 20.0))
    # Annual mean and amplitude from the warmest (Jul) and coldest (Jan) monthly means.
    jul_mean = (normals[7]["high"] + normals[7]["low"]) / 2.0
    jan_mean = (normals[1]["high"] + normals[1]["low"]) / 2.0
    annual_mean_f = (jul_mean + jan_mean) / 2.0
    annual_amp_f = (jul_mean - jan_mean) / 2.0
    # Dated overlays override the day's high/low. Heat and cold events share one mechanism;
    # the two keys are corpus semantics (heat events reconcile with the heat-warning email,
    # cold events with the winter fuel emails and the DP12 audit window — D23/gap-D build).
    events = list(weather.get("heat_events", [])) + list(weather.get("cold_events", []))

    def ambient(day: int, hour: int) -> tuple[float, float]:
        doy = (day0_doy + day) % 365
        seasonal_f = annual_mean_f + annual_amp_f * math.cos(2 * math.pi * (doy - _PEAK_DOY) / 365.0)
        daily_high_f = seasonal_f + swing_f / 2.0
        daily_low_f = seasonal_f - swing_f / 2.0
        for ev in events:
            if ev["from_day"] <= day <= ev["to_day"]:
                daily_high_f, daily_low_f = ev["high_f"], ev["low_f"]
                break
        mean_f = (daily_high_f + daily_low_f) / 2.0
        amp_f = (daily_high_f - daily_low_f) / 2.0
        temp_f = mean_f + amp_f * math.cos(2 * math.pi * (hour - _HOUR_PEAK) / 24.0)
        # RH inversely tracks temperature within a plausible barn-ambient band.
        rh = max(_RH_FLOOR_PCT, min(_RH_CEILING_PCT, _RH_CEILING_PCT - (temp_f - daily_low_f) * _RH_SLOPE_PER_F))
        return _f_to_c(temp_f), rh

    return ambient
