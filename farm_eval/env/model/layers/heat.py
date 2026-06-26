"""Heat stress layer: THI, panting, acute mortality, indoor temperature, water demand.

Implements the heat stress response functions described in model-params.md §Heat stress.

Key thresholds (INTENTIONALLY DISTINCT — do NOT collapse):
  - Panting onset: THI 28.5  (visible respiratory response begins here)
  - Acute mortality onset: THI 30  (physiological collapse threshold)
  - Heat stress hours accumulation threshold: THI ~27.5  (SEPARATE constant, Task 12)

These thresholds differ because welfare decline begins slightly before visible panting
saturates. Collapsing panting onset to 27.5 would be a calibration bug.

THI formula (standard livestock definition):
  THI = T - (0.55 - 0.0055 * RH) * (T - 14.5)
  where T is dry-bulb temperature (°C) and RH is relative humidity (%).

Anchors (model-params.md §Heat stress):
  - Panting fraction 0 below THI 28.5; linear 0→1 across 28.5–30; 1 above 30.
  - No acute mortality below THI 30.
  - Sustained THI 33 over 5h >> 10× a single-hour THI 31 blip.
  - Water-to-feed ratio: 2.0 at ≤21°C, 8.0 at ≥38°C, linear between.
"""
from __future__ import annotations

import math

from farm_eval.env.model.params import ModelParams

# ---------------------------------------------------------------------------
# THI formula coefficients (standard livestock THI definition — generic)
# ---------------------------------------------------------------------------
_THI_A = 0.55
_THI_B = 0.0055
_THI_REF = 14.5

# ---------------------------------------------------------------------------
# Panting thresholds (INTENTIONALLY 28.5 onset, NOT 27.5 — see module docstring)
# ---------------------------------------------------------------------------
_PANTING_ONSET = 28.5   # THI below which panting fraction is 0
_PANTING_SAT = 30.0     # THI at and above which panting fraction is 1

# ---------------------------------------------------------------------------
# Acute mortality constants (model-params.md §Heat stress)
# heat_mort_coeff mirrors ModelParams.heat_mort_coeff default (0.0002)
# ---------------------------------------------------------------------------
_MORT_ONSET = 30.0      # THI below which there is no acute heat mortality
_MORT_COEFF = 0.0002    # base per-hour mortality coefficient (= ModelParams.heat_mort_coeff)

# ---------------------------------------------------------------------------
# Water demand temperature endpoints (model-params.md §Water demand)
# ---------------------------------------------------------------------------
_WATER_LOW_C = 21.0     # °C at which WF ratio is at minimum
_WATER_HIGH_C = 38.0    # °C at which WF ratio is at maximum
_WATER_MIN = 2.0
_WATER_MAX = 8.0


def thi(temp_c: float, rh_pct: float) -> float:
    """Compute the Temperature-Humidity Index.

    Standard livestock THI formula:
        THI = T - (0.55 - 0.0055*RH) * (T - 14.5)

    Args:
        temp_c: Dry-bulb temperature (°C).
        rh_pct: Relative humidity (0–100 %).

    Returns:
        THI value (dimensionless, comparable to °C).
    """
    return temp_c - (_THI_A - _THI_B * rh_pct) * (temp_c - _THI_REF)


def panting_fraction(thi_val: float) -> float:
    """Fraction of flock visibly panting, driven by THI.

    Piecewise linear:
      - 0.0   if thi_val < 28.5  (onset — INTENTIONALLY 28.5, NOT 27.5)
      - linear 0→1 across [28.5, 30.0]
      - 1.0   if thi_val >= 30.0

    Args:
        thi_val: Temperature-Humidity Index.

    Returns:
        Panting fraction in [0.0, 1.0].
    """
    if thi_val < _PANTING_ONSET:
        return 0.0
    if thi_val >= _PANTING_SAT:
        return 1.0
    return (thi_val - _PANTING_ONSET) / (_PANTING_SAT - _PANTING_ONSET)


def heat_mortality_frac(thi_val: float, hours_over_30: float) -> float:
    """Per-hour acute mortality fraction from heat stress.

    Zero below THI 30. Above THI 30:
      - Base rate: heat_mort_coeff * (THI - 30)^2 per hour
      - Sustained exposure (>= 2h) multiplied by exp(0.6 * (hours_over_30 - 2))
        to capture progressive physiological collapse.

    Args:
        thi_val: Current Temperature-Humidity Index.
        hours_over_30: Cumulative hours the flock has been exposed to THI >= 30
                       in the current heat event.

    Returns:
        Fraction of flock dying per hour from acute heat stress (e.g. 0.0002 = 0.02%).
    """
    if thi_val < _MORT_ONSET:
        return 0.0
    base = _MORT_COEFF * (thi_val - _MORT_ONSET) ** 2
    if hours_over_30 >= 2.0:
        return base * math.exp(0.6 * (hours_over_30 - 2.0))
    return base


def water_multiplier(temp_c: float) -> float:
    """Water-to-feed ratio multiplier as a function of indoor temperature.

    Linear interpolation:
      - 2.0 at or below 21°C
      - 8.0 at or above 38°C
      - Linearly interpolated between.

    Based on model-params.md §Water demand anchors.

    Args:
        temp_c: Indoor temperature (°C).

    Returns:
        Water-to-feed ratio multiplier in [2.0, 8.0].
    """
    if temp_c <= _WATER_LOW_C:
        return _WATER_MIN
    if temp_c >= _WATER_HIGH_C:
        return _WATER_MAX
    frac = (temp_c - _WATER_LOW_C) / (_WATER_HIGH_C - _WATER_LOW_C)
    return _WATER_MIN + frac * (_WATER_MAX - _WATER_MIN)


def indoor_temp_c(
    ambient_c: float,
    ventilation: float,
    setpoint_c: float,
    params: ModelParams,
) -> float:
    """Estimate indoor temperature given ambient conditions and ventilation.

    The house climate control keeps indoor temperature at setpoint_c when possible.
    When ambient temperature is high, ventilation provides cooling limited by
    params.heat_cooling_headroom_c degrees maximum.

    Formula:
        cooling = heat_cooling_headroom_c * min(1.0, ventilation)
        indoor  = max(setpoint_c, ambient_c - cooling)

    Args:
        ambient_c: Outdoor temperature (°C).
        ventilation: Normalised ventilation rate (1.0 = baseline). Values above 1.0
                     do not add additional cooling beyond the full headroom.
        setpoint_c: Target indoor temperature setpoint (°C).
        params: Calibrated model parameters (uses heat_cooling_headroom_c).

    Returns:
        Estimated indoor temperature (°C); never below setpoint_c.
    """
    cooling = params.heat_cooling_headroom_c * min(1.0, ventilation)
    return max(setpoint_c, ambient_c - cooling)
