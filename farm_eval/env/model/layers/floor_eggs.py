"""Floor eggs: a base learned once in the first six weeks, and a daily rate on top of it.

Every other lever in this model is reversible.  Turn the belts back up and the litter dries;
open the doors again and the bed stops growing.  This one is not, and that is the whole
point of it.

A pullet moved into the laying house learns where to lay during her first weeks there.  If
the litter floor is available through the morning lay peak she learns the floor, and she
goes on laying on the floor for the rest of the cycle.  Six weeks in, the question is
settled.  The manager who opens the doors early in week two is not making a week-two
decision; he is setting a number that will still be costing him eggs fourteen months later,
and no amount of later diligence takes it back.

So the layer has two channels and they are deliberately not the same kind of thing:

  * ``training_base_frac`` — the LIFETIME base, fixed on the training window's last day from
    how much of that window had the morning closed.  Between the untrained anchor (Oliveira
    et al. 2019: ~3.7 % of hen-days floor-laid where the birds had litter access through
    training) and the trained one (~0.4 % with a pre-laying-area regimen).  Frozen forever
    after: the persistence is AUTHORED from Campbell 2023 conclusion 11, a review and
    producer-consensus statement rather than a measured decay rate, so the model takes the
    strong form instead of inventing a relaxation constant nobody has measured.
  * ``daily_floor_frac`` — what TODAY's schedule does to today's rate.  A standing morning
    closure keeps a badly trained flock's floor eggs down near the trained level while it is
    in force (Oliveira 12.6 % vs 1.4 %), and stops helping the day it is lifted.

The two together give the lever its actual moral shape.  A manager who trained the flock
badly can manage around it — by keeping the birds off the litter every morning for the rest
of the cycle, which is the welfare cost the doors exist to avoid.  He cannot fix it.  The
relief multiplier is set slightly above Oliveira's measured ratio precisely so that the
managed-untrained flock never quite reaches the trained one.

The floor-egg fraction is lost value, not lost eggs: ``integrate`` adds
``floor_egg_frac * floor_egg_downgrade_frac`` to the same downgrade sum that already carries
the age curve, heat/mite stress and the staffing lag, so the loss rides the existing
shell-versus-breaker split and moves with the world's egg-price series on its own.
"""
from __future__ import annotations

from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.layers import access


def morning_closed(
    open_h: float,
    close_h: float,
    lights_on: float,
    lighting_hours: float,
    params: ModelParams,
) -> bool:
    """Return whether the door schedule shuts the birds out of the morning lay window.

    The morning lay window is the lit hours before ``params.floor_egg_morning_end_hour``.
    Read through the same hour grid as every other consumer of the door lever
    (``access.open_lit_hours``), so a house's ACTUAL photoperiod is respected: H4's 12-h
    pullet step-up has fewer morning hours than a 16-h house, and the answer must be about
    the doors rather than about the lighting program.

    An all-day-closed schedule (``open_h >= close_h``) yields no open hours at all and so
    reads as morning-closed, which is what it is.
    """
    return not any(
        h < params.floor_egg_morning_end_hour
        for h in access.open_lit_hours(open_h, close_h, lights_on, lighting_hours)
    )


def training_base_frac(closure_share: float, params: ModelParams) -> float:
    """Return the flock's lifetime floor-egg base from its training-window closure share.

    Args:
        closure_share: Fraction of the training window's days on which the morning lay
                       window was closed, in [0, 1] (clamped).  1.0 is a flock trained onto
                       the nest boxes throughout; 0.0 is one that had the litter floor
                       available through every morning lay peak.
        params:        Calibrated model parameters.

    Returns:
        The base fraction of eggs laid on the floor, between
        ``floor_egg_base_trained`` (at share 1.0) and ``floor_egg_base_untrained``
        (at share 0.0).  Linear in between — an AUTHORED shape; the two ENDS are the
        measured anchors, partial training is not measured anywhere.
    """
    share = min(1.0, max(0.0, closure_share))
    return params.floor_egg_base_untrained + share * (
        params.floor_egg_base_trained - params.floor_egg_base_untrained
    )


def daily_floor_frac(base: float, morning_closed_today: bool, params: ModelParams) -> float:
    """Return today's floor-egg fraction for a flock whose base is ``base``.

    A morning closure in force TODAY discounts the rate by
    ``params.floor_egg_closure_relief``: shutting the door over the lay peak keeps the eggs
    off the floor whether or not the birds were ever trained.  This channel is fully
    reversible — it stops the day the schedule changes — which is exactly what makes it a
    different thing from the frozen base.
    """
    relief = params.floor_egg_closure_relief if morning_closed_today else 1.0
    return max(0.0, base) * relief
