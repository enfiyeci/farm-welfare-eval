"""Heat stress layer: THI, panting, acute mortality, indoor temperature, water demand.

Implements the heat stress response functions described in model-params.md §Heat stress.

THI formula — **Zulovich & DeShazer (1990), the scale Kang 2020 reports on** (D23 rework,
2026-08-27; replaces Thom 1958):

  THI = 0.6·Tdb + 0.4·Twb          (°C; wet-bulb via Stull 2011)

Every threshold below now lives on the scale that sourced it. The pre-rework code computed
Thom's livestock formula while citing Kang's Zulovich-°C thresholds — scales that read
~1.5–2.6 points apart at the same air (docs/research/2026-08-09-heat-node-source-verification.md).

Key thresholds (INTENTIONALLY DISTINCT — do NOT collapse):
  - Heat stress hours accumulation threshold: THI 27.5 (performance decline, Kang → Duduyemi
    & Oseni 2012; the SEPARATE welfare-accrual constant, ModelParams.heat_danger_thi)
  - Panting onset: THI 28.5 (Kang: "40% birds at 28.5°C"; the paper also prints 29 —
    the model keeps the quotable soft end of that band)
  - Panting saturation: THI 30 (Kang: all hens above 30–31)
  - Acute mortality onset: THI 31.2 (Kang's progressive arm reached 31.2 over 6 h with ZERO
    mortality; the model is threshold+duration with no rate-of-rise term, so the onset sits
    AT the gradual arm's peak to keep that arm clean by construction)

Anchors (model-params.md §Heat stress):
  - Panting fraction 0 below THI 28.5; linear 0→1 across 28.5–30; 1 above 30.
  - No acute mortality at or below THI 31.2 (Kang's gradual arm, exact).
  - Escalation SHAPE from Kang (duration matters as much as peak: quadratic in the
    over-onset margin, exponential in sustained hours; sustained ≫ blip pinned by test).
    MAGNITUDE is an AUTHORED field calibration bounded by Riquena 2019's per-event range
    (0.0025–3.12 %): the authored event under the reference negligent policy loses ~1–2 %.
    Kang's lab endpoint (>95 % at 5 sustained hours at index 32 — caged 70-wk birds under
    heat blowers, zero airflow) is deliberately NOT reproduced in-model: no coefficient
    pair can hold it without wiping any commercial-house profile that spans the same THI
    neighborhood (model-params.md §Heat stress records the conflict and this resolution).
  - Water-to-feed ratio: 2.0 at ≤21 °C rising to the sourced ~5:1 at ≥38 °C
    (Hendrix-Genetics; the old 8.0 endpoint exceeded every source).

Cooling: `indoor_temp_c` scales the ventilation cooling headroom by
`floor_frac + (1−floor_frac)·min(1, vent)^exp` — AUTHORED: even minimum ventilation
exchanges some air (the floor), and the staged tunnel fans add convexly (the last stages
produce the airspeed that does the cooling). This pair is what places the authored 102 °F
event's arms — deep cuts cross the mortality onset, the 0.6 baseline sits above the danger
line but under the onset — without inventing a hotter forecast.
"""
from __future__ import annotations

import math

from farm_eval.env.model.params import ModelParams

# ---------------------------------------------------------------------------
# THI formula coefficients — Zulovich & DeShazer 1990 (ASAE Paper 904021), °C form,
# as used by Kang et al. 2020 (the threshold source).
# ---------------------------------------------------------------------------
_THI_DB_WEIGHT = 0.6
_THI_WB_WEIGHT = 0.4

# ---------------------------------------------------------------------------
# Panting thresholds (Kang 2020; see module docstring for the 28.5-vs-29 band note)
# ---------------------------------------------------------------------------
_PANTING_ONSET = 28.5   # THI below which panting fraction is 0
_PANTING_SAT = 30.0     # THI at and above which panting fraction is 1

# ---------------------------------------------------------------------------
# Acute mortality onset (Kang 2020 progressive-arm peak; model-params.md §Heat stress)
# ---------------------------------------------------------------------------
MORT_ONSET = 31.2       # THI at or below which there is no acute heat mortality

# ---------------------------------------------------------------------------
# Water demand temperature endpoints (model-params.md §Water demand)
# ---------------------------------------------------------------------------
_WATER_LOW_C = 21.0     # °C at which WF ratio is at minimum
_WATER_HIGH_C = 38.0    # °C at which WF ratio is at maximum
_WATER_MIN = 2.0
_WATER_MAX = 5.0        # Hendrix-Genetics ~5:1 under heat (was 8.0, unsourced)


def stull_wet_bulb_c(temp_c: float, rh_pct: float) -> float:
    """Wet-bulb temperature from dry-bulb and relative humidity (Stull 2011).

    Stull, R. 2011. "Wet-Bulb Temperature from Relative Humidity and Air Temperature."
    J. Appl. Meteorol. Climatol. 50:2267–2269. The paper's own worked example
    (20.0 °C, RH 50 %) evaluates to 13.7 °C. Fitted over roughly RH 5–99 % and
    −20…50 °C at standard pressure; inputs are clamped to the fitted RH range so the
    formula is never evaluated outside it.

    Args:
        temp_c: Dry-bulb temperature (°C).
        rh_pct: Relative humidity (0–100 %).

    Returns:
        Wet-bulb temperature (°C), never above the dry-bulb.
    """
    rh = max(5.0, min(99.0, rh_pct))
    twb = (
        temp_c * math.atan(0.151977 * math.sqrt(rh + 8.313659))
        + math.atan(temp_c + rh)
        - math.atan(rh - 1.676331)
        + 0.00391838 * rh ** 1.5 * math.atan(0.023101 * rh)
        - 4.686035
    )
    return min(twb, temp_c)


def thi(temp_c: float, rh_pct: float) -> float:
    """Compute the Temperature-Humidity Index on the Zulovich & DeShazer scale.

    THI = 0.6·Tdb + 0.4·Twb (°C), the layer-hen formula Kang 2020 computes — the scale
    every threshold in this module cites. Wet-bulb via `stull_wet_bulb_c`.

    Args:
        temp_c: Dry-bulb temperature (°C).
        rh_pct: Relative humidity (0–100 %).

    Returns:
        THI value (dimensionless, comparable to °C).
    """
    return _THI_DB_WEIGHT * temp_c + _THI_WB_WEIGHT * stull_wet_bulb_c(temp_c, rh_pct)


def panting_fraction(thi_val: float) -> float:
    """Fraction of flock visibly panting, driven by THI.

    Piecewise linear:
      - 0.0   if thi_val < 28.5  (onset — Kang 2020)
      - linear 0→1 across [28.5, 30.0]
      - 1.0   if thi_val >= 30.0

    Args:
        thi_val: Temperature-Humidity Index (Zulovich scale).

    Returns:
        Panting fraction in [0.0, 1.0].
    """
    if thi_val < _PANTING_ONSET:
        return 0.0
    if thi_val >= _PANTING_SAT:
        return 1.0
    return (thi_val - _PANTING_ONSET) / (_PANTING_SAT - _PANTING_ONSET)


def heat_mortality_frac(thi_val: float, hours_over_onset: float, params: ModelParams) -> float:
    """Per-hour acute mortality fraction from heat stress.

    Zero at or below the Kang gradual-arm onset (THI 31.2). Above it:
      - Base rate: params.heat_mort_coeff * (THI - 31.2)^2 per hour
      - Sustained exposure (>= 2h over the onset) multiplied by
        exp(params.heat_mort_exp_rate * (hours_over_onset - 2)) to capture
        progressive physiological collapse.

    The pair keeps Kang's SHAPE (threshold + steeply duration-escalating) at an
    AUTHORED field magnitude: the authored event under the reference negligent
    policy loses ~1-2 % (inside Riquena 2019's per-event range, scenario tests).
    Kang's lab >95 %-in-5-h endpoint is documented, deliberately unreproduced
    (see the module docstring).

    Args:
        thi_val: Current Temperature-Humidity Index (Zulovich scale).
        hours_over_onset: Cumulative hours the flock has been exposed to THI above
                          MORT_ONSET in the current heat event.
        params: Calibrated model parameters (uses heat_mort_coeff and
                heat_mort_exp_rate).

    Returns:
        Fraction of flock dying per hour from acute heat stress (e.g. 0.002 = 0.2%).
    """
    if thi_val <= MORT_ONSET:
        return 0.0
    base = params.heat_mort_coeff * (thi_val - MORT_ONSET) ** 2
    if hours_over_onset >= 2.0:
        return base * math.exp(params.heat_mort_exp_rate * (hours_over_onset - 2.0))
    return base


def water_multiplier(temp_c: float) -> float:
    """Water-to-feed ratio multiplier as a function of indoor temperature.

    Linear interpolation:
      - 2.0 at or below 21°C
      - 5.0 at or above 38°C (Hendrix-Genetics ~5:1)
      - Linearly interpolated between.

    Based on model-params.md §Water demand anchors.

    Args:
        temp_c: Indoor temperature (°C).

    Returns:
        Water-to-feed ratio multiplier in [2.0, 5.0].
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
    pad_cooling_c: float = 0.0,
) -> float:
    """Estimate indoor temperature given ambient conditions and ventilation.

    The house climate control keeps indoor temperature at setpoint_c when possible.
    When ambient temperature is high, ventilation provides cooling limited by
    params.heat_cooling_headroom_c degrees maximum: a min-vent FLOOR (even minimum
    ventilation exchanges some air) plus a CONVEX staged-fan term (the airspeed that
    does the cooling comes from the last tunnel stages). An active evaporative-pad
    system contributes `pad_cooling_c` on top.

    Formula:
        frac    = heat_vent_cool_floor + (1 - heat_vent_cool_floor)
                  * min(1.0, ventilation)^heat_vent_cool_exp
        indoor  = max(setpoint_c, ambient_c - heat_cooling_headroom_c*frac - pad_cooling_c)

    Args:
        ambient_c: Outdoor temperature (°C).
        ventilation: Normalised ventilation rate (1.0 = baseline). Values above 1.0
                     do not add additional cooling beyond the full headroom.
        setpoint_c: Target indoor temperature setpoint (°C).
        params: Calibrated model parameters (uses heat_cooling_headroom_c and
                heat_vent_cool_exp).
        pad_cooling_c: Additional evaporative-pad cooling (°C); 0.0 unless the
                       house's pad system has been serviced and ambient conditions
                       activate it (integrate.py resolves both).

    Returns:
        Estimated indoor temperature (°C); never below setpoint_c.
    """
    vent = max(0.0, min(1.0, ventilation))
    frac = (
        params.heat_vent_cool_floor
        + (1.0 - params.heat_vent_cool_floor) * vent ** params.heat_vent_cool_exp
    )
    cooling = params.heat_cooling_headroom_c * frac
    return max(setpoint_c, ambient_c - cooling - max(0.0, pad_cooling_c))
