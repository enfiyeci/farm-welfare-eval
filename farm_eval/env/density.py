"""Stocking density as a derived identity: usable floor area per live hen.

Density is NOT a setpoint -- it is birds divided into usable area, so it moves whenever
either side moves: mortality raises sq in/hen, a larger placement lowers it, an added tier
raises it. Audit finding N20 was that the field was seeded and never written, so it read
the same at day 518 as at day 0 after ~148,000 deaths.

This module is the single definition that both the daily integrator and the audit snapshot
read, so the gauge the agent sees and the number the auditor writes up cannot disagree.

Imports nothing from `farm_eval.env`: `audit.py` and `model/integrate.py` both depend on
it, and a shared leaf keeps that acyclic.
"""
from __future__ import annotations


def space_sq_in_per_hen(area_sq_in: float, birds: int) -> float:
    """Return usable floor area per live hen (sq in/hen).

    Args:
        area_sq_in: The house's usable floor area (sq in). For a multi-tier aviary this
            properly includes tier area, which is why it is per-house mutable state rather
            than a building constant.
        birds: Live bird count.

    Returns:
        Area per hen, or 0.0 for an empty house -- no flock, so no density, and no
        division by zero.
    """
    if birds <= 0:
        return 0.0
    return area_sq_in / birds
