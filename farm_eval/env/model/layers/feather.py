from __future__ import annotations

from farm_eval.env.model.layers.production import _interp
from farm_eval.env.model.params import ModelParams


def feather_damage_pct(age_weeks: float, params: ModelParams) -> float:
    """Return estimated feather-damage prevalence (%) at *age_weeks*.

    Interpolated/clamped from the ModelParams anchor tables
    (model-params.md §Feather).  Returns 0.0 below the first anchor (~30 wk);
    monotone non-decreasing and clamped to [0, 100].

    Anchor points (from model-params.md §Feather):
      wk 30 → 0 %
      wk 31 → 3.2 %
      wk 46 → 32.9 %
      wk 65 → 57.8 %
    """
    return _interp(age_weeks, params.feather_age_wk, params.feather_pct)
