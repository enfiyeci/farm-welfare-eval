"""Pure diurnal calculations for internal litter-access doors.

Resolution is WHOLE CLOCK HOURS. `lighting_hours`, `litter_access_open_hour` and
`litter_access_close_hour` are all float setpoints the agent may set fractionally, but the
diurnal weight tables are hourly, so an hour counts as open only if it starts at or after
`open_h` and before `close_h`: a door set to open at 11.5 first counts hour 12. Both weighted
shares are ratios over the same hour set, so the quantization cancels for a fully-open door
and only ever costs the partial hour at each edge.
"""
from __future__ import annotations

from farm_eval.env.model.params import ModelParams


def open_lit_hours(
    open_h: float, close_h: float, lights_on: float, lighting_hours: float
) -> list[int]:
    """Return absolute clock hours that are both lit and open to litter."""
    if open_h >= close_h:
        return []
    return [
        hour
        for hour in range(int(lights_on), int(lights_on + lighting_hours))
        if 0 <= hour < 24 and open_h <= hour < close_h
    ]


def _lit_hours(lights_on: float, lighting_hours: float) -> list[int]:
    return [
        hour
        for hour in range(int(lights_on), int(lights_on + lighting_hours))
        if 0 <= hour < 24
    ]


def _lit_weight(hours: list[int], lights_on: float, weights: list[float]) -> float:
    # The tables hold 16 entries — the standard layer photoperiod — but `lighting_hours` is a
    # (0, 24) setpoint, so a longer photoperiod runs off the end of the table. Hold the final
    # entry rather than dropping those hours: dropping them made an open door read as zero
    # share AND zero opportunity while `access_hours` still counted it open, which is a
    # contradiction, not a conservative default. Both tables are flat/decaying in their tail
    # (deposition .0505, opportunity .05), so holding the last value extends the measured
    # shape instead of inventing a new one.
    return sum(weights[min(hour - int(lights_on), len(weights) - 1)] for hour in hours
               if hour - int(lights_on) >= 0)


def floor_manure_share(
    open_h: float,
    close_h: float,
    lights_on: float,
    lighting_hours: float,
    params: ModelParams,
) -> float:
    """Return the deposition-weighted share of daily manure landing on litter."""
    lit_hours = _lit_hours(lights_on, lighting_hours)
    denominator = _lit_weight(lit_hours, lights_on, params.w_dep_hourly)
    if open_h >= close_h or denominator == 0.0:
        return 0.0
    numerator = _lit_weight(
        open_lit_hours(open_h, close_h, lights_on, lighting_hours),
        lights_on,
        params.w_dep_hourly,
    )
    return max(0.0, min(1.0, numerator / denominator))


def opportunity_available(
    open_h: float,
    close_h: float,
    lights_on: float,
    lighting_hours: float,
    params: ModelParams,
) -> float:
    """Return the lit-window-normalized dust-bathing opportunity available."""
    lit_hours = _lit_hours(lights_on, lighting_hours)
    denominator = _lit_weight(lit_hours, lights_on, params.w_opp_hourly)
    if open_h >= close_h or denominator == 0.0:
        return 0.0
    numerator = _lit_weight(
        open_lit_hours(open_h, close_h, lights_on, lighting_hours),
        lights_on,
        params.w_opp_hourly,
    )
    return max(0.0, min(1.0, numerator / denominator))


def access_hours(open_h: float, close_h: float, lights_on: float, lighting_hours: float) -> float:
    """Return the number of lit hours during which internal doors are open."""
    return float(len(open_lit_hours(open_h, close_h, lights_on, lighting_hours)))
