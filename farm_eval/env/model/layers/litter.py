"""Litter as a water balance: moisture, bed depth and caking.

Litter condition is the proximate driver of footpad dermatitis (layers/footpad.py) and a
source term for ammonia (layers/ammonia.py).  It is not an exogenous input: it is a balance
between what dries the bed and what wets it, and BOTH sides are agent-reachable.

    moisture -> belt_equilibrium(belt_days) + floor_moisture_excess(share, age, depth, ...)

The two terms are deliberately very different in size and in speed.

  * ``belt_equilibrium`` — the manure-belt lever (``adjust_setpoint(belt_interval_days=...)``).
    NARROW: 14.5 % at daily belts rising to a 20.5 % cap.  Groot Koerkamp ch. 7 measures the
    whole belt-frequency span of an aviary litter bed inside roughly 14.4-20.6 %, and every
    aviary anchor in the corpus sits in or just above that band.  The layer's previous curve
    reached 45 % at weekly belts, which is a FLOOR-HOUSING number; correcting it is inherited
    calibration correction #1 (evals/hen/research/2026-08-07-litter-prep/).
  * ``floor_moisture_excess`` — the litter-door lever (``litter_access_open_hour`` /
    ``litter_access_close_hour``, via ``layers/access.floor_manure_share``).  This is where
    the LARGE contrasts live: Oliveira et al. 2019 measured 31.3 % moisture under all-day
    access against 20.3 % under a 10-hour schedule in the same house.

That gap is not a direct hours effect and must not be modelled as one.  Oliveira's own
contrast had vanished by the end of the trial (P = 0.57), and the paper attributes the
difference to accumulated bed depth and caking rather than to hours.  So the door schedule
feeds a DEPTH state that accumulates over months, and depth is what gates the moisture source
term.  Strip the bed back to bedding and the two regimens converge within weeks — the model
reproduces the disappearing effect instead of contradicting it.

Age matters more than the doors do.  Groot Koerkamp ch. 8 measured water flow to the litter
peaking near 45 g/hen/day at ~22 weeks and falling to ~7 g/hen/day by 30 weeks: a ~6x
behavioural swing against roughly 2x from full-versus-part access.  ``water_rel`` carries it,
normalized to that 22-week peak, and it scales BOTH the moisture source and bed accretion —
the classic early-lay wet-litter complaint falls out of the same curve.

Depth never decays here.  A bed only gets shallower when someone removes it, which is the
cleanout event, not a daily process.

Calibration anchors, the tuned coefficients and the deterministic trajectory that produced
them are documented in ModelParams (the litter block) and exercised in
tests/env/model/test_layer_litter.py.
"""
from __future__ import annotations

from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.layers.production import _interp


def water_rel(age_wk: float, params: ModelParams) -> float:
    """Return water flow to the litter at ``age_wk``, relative to its 22-week peak.

    1.0 at the peak-deposition age, ~0.16 from 30 weeks onward (GK ch. 8: ~45 vs
    ~7 g water/hen/day).  Clamped flat outside the table by the shared ``_interp``.
    """
    peak = max(params.litter_water_g_day)
    return _interp(age_wk, params.litter_water_age_wk, params.litter_water_g_day) / peak


def belt_equilibrium(belt_days: float, params: ModelParams) -> float:
    """Return the belt-frequency term of the equilibrium moisture (%).

    More-frequent belt removal (lower ``belt_days``) yields a drier bed.  Bounded to
    ``[litter_moisture_belt_floor, litter_moisture_belt_cap]`` — the GK ch. 7 aviary band.
    Sub-daily intervals are meaningless (integrate floors the setpoint at 1 day anyway), so
    they read as the floor rather than extrapolating below it.
    """
    belt_days = max(1.0, belt_days)
    eq = params.litter_moisture_belt_floor + params.litter_moisture_belt_slope * (belt_days - 1.0)
    return min(eq, params.litter_moisture_belt_cap)


def _depth_saturation(depth_cm: float, params: ModelParams) -> float:
    """Bed depth as a fraction of the depth at which it is fully wet-capable, in [0, 1]."""
    return min(max(0.0, depth_cm) / params.litter_depth_deep_ref, 1.0)


def floor_moisture_excess(
    floor_share: float,
    age_wk: float,
    depth_cm: float,
    density_factor: float,
    params: ModelParams,
) -> float:
    """Return the percentage points of moisture the floor-manure load adds at equilibrium.

    Args:
        floor_share:    Share of the day's manure landing on the litter floor
                        (``access.floor_manure_share``), in [0, 1].
        age_wk:         Flock age in weeks — carries the water-flow curve.
        depth_cm:       Current bed depth; a shallow bed contributes little even under a
                        heavy load, and the term saturates at ``litter_depth_deep_ref``.
        density_factor: Hens per m2 of litter relative to the reference (Task 7 wires the
                        real lever; 1.0 until then).  A clean multiplier by construction —
                        water load per m2 is (hens/m2) x (g water/hen/day) reaching the floor.
        params:         Calibrated model parameters.
    """
    return (
        params.litter_floor_moist_coeff
        * max(0.0, floor_share)
        * water_rel(age_wk, params)
        * _depth_saturation(depth_cm, params) ** params.litter_depth_exp
        * density_factor
    )


def litter_moisture_step(
    moisture: float,
    belt_days: float,
    floor_share: float,
    age_wk: float,
    depth_cm: float,
    density_factor: float,
    params: ModelParams,
) -> float:
    """Advance litter moisture one day toward its belt + floor-load equilibrium.

    First-order relaxation at ``litter_moisture_relax`` (~10-day time constant), so a change
    to either lever shows up over days rather than instantly, and a single step never
    overshoots the equilibrium.  Bounded to ``[0, litter_moisture_max]``.
    """
    eq = belt_equilibrium(belt_days, params) + floor_moisture_excess(
        floor_share, age_wk, depth_cm, density_factor, params
    )
    new = moisture + (eq - moisture) * params.litter_moisture_relax
    return max(0.0, min(params.litter_moisture_max, new))


def litter_depth_step(
    depth_cm: float,
    floor_share: float,
    age_wk: float,
    params: ModelParams,
) -> float:
    """Advance bed depth one day (cm).  Monotone non-decreasing.

    Accretion is the floor-manure load again, but with an AUTHORED convexity on the share
    term (``litter_depth_share_exp``): a part-time schedule builds a bed disproportionately
    more slowly than its share of the day's manure suggests, which is what Oliveira's
    measured depth pair requires (1.64/3.77 = 0.435 at share 0.505).

    There is no decay term.  A bed gets shallower only when litter is physically removed,
    which is a cleanout event, not a daily process.
    """
    return depth_cm + (
        params.litter_depth_accretion_cm_day
        * max(0.0, floor_share) ** params.litter_depth_share_exp
        * water_rel(age_wk, params)
    )


def caked_pct(moisture: float, depth_cm: float, params: ModelParams) -> float:
    """Return the caked share of the litter surface (%), in [0, litter_cake_max_pct].

    A product of excess wetness and bed saturation, zero on either factor alone: dry litter
    does not cake however deep it is, and a thin bed has nothing to cake.  Oliveira
    attributes caking to depth — "the thicker litter being more difficult to be dried by the
    ventilation air" — and measured 33.1 % caked at 31.3 % moisture / 3.77 cm against 0 % at
    20.3 % / 1.64 cm.

    The ceiling applies to the WETNESS term, BEFORE bed saturation scales it.  Capping the
    product instead made caking a step rather than a curve: through the 18-26-week high-water
    window litter moisture sits on its own ``litter_moisture_max`` rail for every floor share
    above ~0.46, so a cap on the product pinned all of those schedules to the same number and
    erased the door lever's entire upper range — exactly where the opportunity channel later
    reads ``1 - caked/100``.  Capping the wetness term leaves depth, which does still separate
    those schedules, in charge of the answer: the ceiling is how caked a FULLY DEEP bed gets
    at maximum wetness, and a shallower bed cakes proportionally less.  That is also the
    paper's own reading of the mechanism — caking follows the bed.
    """
    wetness = min(
        params.litter_cake_coeff * max(0.0, moisture - params.litter_cake_moisture_ref),
        params.litter_cake_max_pct,
    )
    return max(0.0, wetness * _depth_saturation(depth_cm, params))
