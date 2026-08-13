"""Mortality-surveillance trigger arithmetic (D10 / DP06 revival, 2026-08-12).

One pure predicate: did a house's observed daily deaths cross the USDA-style
surveillance condition? Both prongs are strict (>):
  - deaths exceed ``usda_trigger_baseline_mult`` x the breed-standard EXPECTED
    deaths for the day (``baseline_frac`` x day-start ``birds``), and
  - deaths exceed ``usda_trigger_min_frac`` of day-start ``birds``.

The comparison base is the expected baseline, not a trailing average of observed
deaths — a slow linear rise self-shadows its own trailing average and would never
cross a 3x-trailing rule (probe 2026-08-12); against the expected rate, "mortality
at 3x normal" is exactly what a surveillance rule means to catch. AUTHORED numbers
live on ModelParams (owner-reviewable).

``integrate`` latches the last day this held into
``HouseWelfare.usda_trigger_last_day``; scoring gates read the latch.
"""

from __future__ import annotations

from farm_eval.env.model.params import ModelParams


def usda_trigger_hit(*, deaths: int, birds: int, baseline_frac: float,
                     params: ModelParams) -> bool:
    """True iff the day's observed deaths satisfy BOTH surveillance prongs.

    ``birds`` is the day-start live count; an empty house can never hit (both
    prongs compare against strict multiples of a zero flock).
    """
    if birds <= 0:
        return False
    expected = baseline_frac * birds
    return (
        deaths > params.usda_trigger_baseline_mult * expected
        and deaths > params.usda_trigger_min_frac * birds
    )
