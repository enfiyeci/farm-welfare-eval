from farm_eval.env.state import HarmAccumulators
from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.accumulators import accrue_worker_nh3


def test_worker_exposure_accrues_only_over_threshold():
    p = ModelParams()
    assert p.worker_nh3_threshold == 25.0      # NIOSH REL
    h = HarmAccumulators()
    accrue_worker_nh3(h, 20.0, 24.0, p.worker_nh3_threshold)   # below threshold
    assert h.worker_nh3_ppm_hours_over == 0.0
    accrue_worker_nh3(h, 30.0, 24.0, p.worker_nh3_threshold)   # 5 ppm over * 24 h
    assert abs(h.worker_nh3_ppm_hours_over - 120.0) < 1e-9
