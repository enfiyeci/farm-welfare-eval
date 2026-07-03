from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.layers.salmonella import _unit_hash, environmental_test


def test_unit_hash_is_half_open_unit_interval():
    # Contract: pseudo-uniform in [0,1). The divisor (2**32) must keep even the maximum 32-bit
    # prefix strictly below 1.0 so a perfect-sensitivity (1.0) test never produces a false negative.
    assert all(0.0 <= _unit_hash(1, "H4", d) < 1.0 for d in range(500))
    assert int("ffffffff", 16) / 0x100000000 < 1.0          # max prefix maps below 1.0


def test_perfect_sensitivity_always_detects_positive_flock():
    # With sensitivity 1.0, every draw (< 1.0 by the [0,1) contract) must detect a positive flock.
    p = ModelParams(se_env_test_sensitivity=1.0)
    assert all(environmental_test(True, 1, "H4", d, p) for d in range(500))


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
