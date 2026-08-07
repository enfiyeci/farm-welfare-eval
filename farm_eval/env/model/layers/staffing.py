"""Staffing adequacy layer: one monotone factor coupling the C2 staffing lever into welfare.

HEURISTIC (model-params.md §Staffing->welfare coupling). Research
evals/hen/research/2026-07-01-daily-labor-staffing.md §C proposes a heuristic model in the
absence of any published dose-response curve for staffing-vs-welfare, so this is a
defensible interpolation between the anchors that DO exist, not a calibrated model.
`adequacy_factor` is the SINGLE factor `integrate()` couples into excess mortality,
floor-egg downgrade, and belt-interval lag (via `u = 1 - f`) -- see integrate.py.

Basis (research §A): daily labor-hours per 100k hens, not raw FTE headcount, because a
crew working longer shifts covers proportionally more ground (a crew of 2 on 16h surge
days covers what 4 cover on 8h shifts -- this is also the seam Task C4's cull-surge
mechanics builds on). `fte_eq` normalises `fte_per_100k * shift_hours` against the
standard `labor_hours_per_fte_day` shift, so `fte_eq` is directly comparable to a plain
FTE/100k count at the standard shift length.

Curve: smoothstep between `staffing_adequacy_zero_fte` (f=0 at/below) and
`staffing_adequacy_full_fte` (f=1 at/above, research §A's ~40k hens/FTE aviary
standard). Values above full PLATEAU at 1.0 (research §C: staff beyond ~2-3 FTE/100k
yield diminishing returns, so no adequacy bonus above full). Monotone non-decreasing,
bounded [0, 1].
"""
from __future__ import annotations

from farm_eval.env.model.params import ModelParams


def adequacy_factor(fte_per_100k: float, shift_hours: float, params: ModelParams) -> float:
    """Return the staffing-adequacy factor f in [0, 1].

    Args:
        fte_per_100k: Effective FTE headcount per 100k hens (economics.effective_fte_per_100k).
        shift_hours:  Effective scheduled hours per FTE-day (economics.effective_shift_hours).
        params:       Calibrated model parameters.

    Returns:
        f = 0 at/below `staffing_adequacy_zero_fte` FTE-equivalent, f = 1 at/above
        `staffing_adequacy_full_fte`, smoothstep interpolated between (plateau above full,
        no diminishing-returns bonus).
    """
    fte_eq = fte_per_100k * shift_hours / params.labor_hours_per_fte_day
    zero = params.staffing_adequacy_zero_fte
    full = params.staffing_adequacy_full_fte
    t = max(0.0, min(1.0, (fte_eq - zero) / (full - zero)))
    return t * t * (3.0 - 2.0 * t)
