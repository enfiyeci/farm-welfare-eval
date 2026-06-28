from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.layers.salmonella import environmental_test


def test_negative_flock_never_tests_positive():
    p = ModelParams()
    assert all(
        environmental_test(False, seed=1, house_id="H4", day=d, params=p) is False
        for d in range(300)
    )


def test_positive_flock_detection_is_sensitivity_limited_but_deterministic():
    p = ModelParams(se_env_test_sensitivity=0.6)
    results = [environmental_test(True, seed=1, house_id="H4", day=d, params=p) for d in range(300)]
    frac = sum(results) / len(results)
    assert 0.45 <= frac <= 0.75                 # ~sensitivity (imperfect environmental swab)
    # deterministic: same inputs -> same output
    assert environmental_test(True, 1, "H4", 40, p) == environmental_test(True, 1, "H4", 40, p)
