import pytest
from farm_eval.study.params import dose_response_pp, DENSITY_CAP, COMPLIANCE_INDEX


def test_constants():
    assert DENSITY_CAP == 2.5
    assert COMPLIANCE_INDEX == 120.0


def test_baseline_multiplier_adds_nothing():
    assert dose_response_pp(1.0) == 0.0
    assert dose_response_pp(0.5) == 0.0  # below baseline never happens; clamps to 0


@pytest.mark.parametrize(
    "mult, pp",
    [
        (1.04, 0.5),
        (1.08, 1.0),
        (1.12, 1.5),
        (1.16, 2.0),
        (1.24, 3.0),
        (1.32, 4.5),
        (1.40, 6.5),
        (1.50, 9.0),
    ],
)
def test_anchor_points_are_exact(mult, pp):
    assert dose_response_pp(mult) == pytest.approx(pp)


def test_linear_interpolation_between_anchors():
    # midway between (1.04, 0.5) and (1.08, 1.0)
    assert dose_response_pp(1.06) == pytest.approx(0.75)


def test_extrapolates_above_top_anchor_at_last_slope():
    # last segment (1.40,6.5)->(1.50,9.0): slope 25 pp per unit multiplier
    assert dose_response_pp(1.50) == pytest.approx(9.0)
    assert dose_response_pp(2.5) == pytest.approx(34.0)  # 9.0 + 25*(2.5-1.5)


def test_strictly_monotonic_on_a_grid():
    xs = [1.0 + i * 0.01 for i in range(0, 160)]
    ys = [dose_response_pp(x) for x in xs]
    assert all(b >= a for a, b in zip(ys, ys[1:]))
