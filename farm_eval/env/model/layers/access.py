"""Diurnal litter/scratch-area access layer: door schedule -> hourly access quantities.

The litter doors are an agent-reachable lever: ``adjust_setpoint`` writes
``litter_access_open_hour`` / ``litter_access_close_hour`` per house.  This layer is the
pure machinery every consumer of that lever calls.  It answers three separate questions
about one schedule, and they are deliberately different currencies:

  * ``floor_manure_share``    — how much of the day's manure lands on the litter floor
    instead of the belts (the COST of open doors: wetter litter, more footpad/ammonia).
  * ``opportunity_available`` — how much of the birds' dustbathing/foraging opportunity
    the schedule actually delivers (the WELFARE the doors exist to provide).
  * ``access_hours``          — the plain count of usable hours, for reporting and for
    the UEP daily-litter-access requirement.

The asymmetry between the first two is the point.  Hen floor deposition is morning-heavy
while dustbathing/foraging initiation is near-zero before ~11:00 and peaks early
afternoon, so the inherited "doors open at 11:00" schedule buys roughly half the floor
manure load for well under a tenth of the behavioural opportunity — and the mirror-image
schedule (open at lights-on, shut at noon) is the expensive one.  A caller comparing the
two numbers is comparing a real trade-off, not a single monotone "more access is better".

Photoperiod handling (round-2 F2).  Both shares are denominated against the CURRENT lit
window, not against an absolute 16-h day:

    floor_manure_share    = sum w_dep(open & lit) / sum w_dep(lit)
    opportunity_available = sum w_opp(open & lit) / sum w_opp(lit)

so a fully open door reads 1.0 at any photoperiod.  This isolates the DOOR lever's own
contribution: the live H4 runs a correct 12-h pullet step-up, and charging the litter
node for that lighting program would make the diligent target unreachable.  Whether a
short photoperiod is itself a welfare cost is a separate question that belongs to the
welfare-currency lane (P9), not here.

Hours are whole clock hours.  An hour ``h`` counts as open when ``open_h <= h < close_h``
and as lit when it falls in ``[lights_on, lights_on + lighting_hours)``.  By convention
``open_h >= close_h`` means the doors stay shut all day (a degenerate but valid schedule,
matching the setpoint bounds in ModelParams), and every function returns 0/empty for it.
"""
from __future__ import annotations

from farm_eval.env.model.params import ModelParams

HOURS_PER_DAY = 24


def open_lit_hours(
    open_h: float,
    close_h: float,
    lights_on: float,
    lighting_hours: float,
) -> list[int]:
    """Return the absolute clock hours that are BOTH lit and door-open.

    Args:
        open_h:         Door open hour (clock hour, 0-24).
        close_h:        Door close hour (clock hour, 0-24).  ``open_h >= close_h`` means
                        the doors stay closed all day.
        lights_on:      Lights-on clock hour for the house.
        lighting_hours: The house's photoperiod in hours (its ACTUAL setpoint, never a
                        hardcoded 16).

    Returns:
        Ascending list of whole clock hours in [0, 24).  A lit window running past
        midnight is truncated at 24:00 rather than wrapped — no lighting program in this
        world does that, and wrapping would make the open/close comparison ambiguous.
    """
    if open_h >= close_h:
        return []
    start = int(lights_on)
    end = start + int(lighting_hours)
    return [
        h
        for h in range(start, end)
        if 0 <= h < HOURS_PER_DAY and open_h <= h < close_h
    ]


def _lit_hours(lights_on: float, lighting_hours: float) -> list[int]:
    """Return every lit clock hour, ignoring the doors (the denominator's window)."""
    start = int(lights_on)
    end = start + int(lighting_hours)
    return [h for h in range(start, end) if 0 <= h < HOURS_PER_DAY]


def _weighted(hours: list[int], lights_on: float, table: list[float]) -> float:
    """Sum an hourly weight table over ``hours``.

    Entry ``i`` of the table is the clock hour ``lights_on + i``.  Hours outside the
    table (a photoperiod longer than the reference 16 h) carry zero weight, which keeps
    a renormalized share well-defined instead of raising on an unusual setpoint.
    """
    start = int(lights_on)
    return sum(table[h - start] for h in hours if 0 <= h - start < len(table))


def _renormalized_share(
    open_h: float,
    close_h: float,
    lights_on: float,
    lighting_hours: float,
    table: list[float],
) -> float:
    """Share of ``table``'s lit-window weight that the door schedule actually delivers."""
    denominator = _weighted(_lit_hours(lights_on, lighting_hours), lights_on, table)
    if denominator <= 0.0:
        return 0.0
    numerator = _weighted(
        open_lit_hours(open_h, close_h, lights_on, lighting_hours), lights_on, table
    )
    return min(1.0, numerator / denominator)


def floor_manure_share(
    open_h: float,
    close_h: float,
    lights_on: float,
    lighting_hours: float,
    params: ModelParams,
) -> float:
    """Return the deposition-weighted share of daily manure landing on the litter floor.

    In [0, 1]: 1.0 when the doors are open for the whole lit window (at ANY photoperiod),
    0.0 when they never open.  Weighted by ``params.w_dep_hourly``, whose morning-heavy
    shape is what makes the inherited 11:00 opening halve the floor load.
    """
    return _renormalized_share(
        open_h, close_h, lights_on, lighting_hours, params.w_dep_hourly
    )


def opportunity_available(
    open_h: float,
    close_h: float,
    lights_on: float,
    lighting_hours: float,
    params: ModelParams,
) -> float:
    """Return the opportunity-weighted access the schedule delivers, in [0, 1].

    Denominated against the CURRENT lit window, so full-open is 1.0 at any photoperiod —
    this is the DOOR lever's own contribution, not a judgement on the lighting program.
    Weighted by ``params.w_opp_hourly`` (dustbathing/foraging initiation), so withholding
    early-morning hours costs little while shutting the early afternoon costs a lot.
    """
    return _renormalized_share(
        open_h, close_h, lights_on, lighting_hours, params.w_opp_hourly
    )


def access_hours(
    open_h: float,
    close_h: float,
    lights_on: float,
    lighting_hours: float,
) -> float:
    """Return how many whole clock hours are both door-open and lit.

    The same discretization as ``open_lit_hours`` (and therefore as the two shares), so a
    caller can compare hours against weighted shares without a grid mismatch.
    """
    return float(len(open_lit_hours(open_h, close_h, lights_on, lighting_hours)))
