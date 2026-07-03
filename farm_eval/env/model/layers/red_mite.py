"""Red-mite (Dermanyssus gallinae) burden: deterministic logistic growth. Treatment knockdown
is applied as an ACTION in FarmEnv.apply_action (log_treatment), not here. Index is a relative
burden in [0, carrying]; ~1.0 is the IPM action threshold."""

from farm_eval.env.model.params import ModelParams


def red_mite_step(index: float, params: ModelParams) -> float:
    """Advance mite burden one day: logistic growth toward carrying capacity."""
    growth = params.red_mite_growth * index * (1.0 - index / params.red_mite_carrying)
    return max(0.0, min(params.red_mite_carrying, index + growth))
