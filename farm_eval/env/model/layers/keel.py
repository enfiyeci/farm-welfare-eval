from __future__ import annotations

from farm_eval.env.model.layers.production import _interp
from farm_eval.env.model.params import ModelParams


def keel_prevalence_pct(age_weeks: float, params: ModelParams) -> float:
    """Return estimated keel-bone fracture prevalence (%) at *age_weeks*.

    Interpolated/clamped from the ModelParams anchor tables
    (model-params.md §KBF).  Prevalence is monotone non-decreasing and
    clamped to [0, 100].  Returns 0.0 below the first anchor (~22 wk).
    """
    return _interp(age_weeks, params.keel_age_wk, params.keel_pct)
