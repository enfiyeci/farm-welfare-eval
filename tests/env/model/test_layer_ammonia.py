from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.layers.ammonia import ammonia_step


def _eq(ventilation, ambient_c, moisture=25.0, litter_age=60.0, belt_days=2):
    ppm = 5.0
    for _ in range(60):  # iterate to equilibrium
        ppm = ammonia_step(ppm, litter_age, moisture, ventilation, ambient_c, belt_days, ModelParams())
    return ppm


def test_baseline_aviary_mean_near_6_7():
    # model-params: aviary mean ~6.7 ppm at baseline ventilation, mild temp
    assert 5.0 <= _eq(ventilation=1.0, ambient_c=18.0) <= 8.5


def test_winter_low_temp_pushes_over_25():
    # ~12 winter days >25 ppm: cold + baseline vent -> equilibrium climbs past 25
    assert _eq(ventilation=1.0, ambient_c=-8.0) > 25.0


def test_more_ventilation_lowers_ammonia():
    assert _eq(ventilation=3.0, ambient_c=18.0) < _eq(ventilation=1.0, ambient_c=18.0)


def test_more_frequent_belts_lower_ammonia():
    # model-params: lower manure-accumulation time (f_MAT) -> lower NH3. Direction only;
    # the precise same-cycle r_clear (~28.6%) is a refinement not modeled in this layer.
    frequent = _eq(ventilation=1.0, ambient_c=18.0, belt_days=1)
    infrequent = _eq(ventilation=1.0, ambient_c=18.0, belt_days=4)
    assert frequent < infrequent
