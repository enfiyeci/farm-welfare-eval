from __future__ import annotations

from pydantic import BaseModel


class ModelParams(BaseModel):
    ammonia_base: float = 5.0
    ammonia_per_litter_day: float = 0.05
    ammonia_vent_coeff: float = 8.0
    vent_baseline: float = 1.0
    ammonia_relax: float = 0.25
    feed_lb_per_bird_day: float = 0.247
    ammonia_mortality_threshold: float = 25.0
    mortality_excess_per_day: float = 0.0003
