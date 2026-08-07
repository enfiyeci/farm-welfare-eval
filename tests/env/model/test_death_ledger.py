import json, pathlib
import pytest
from farm_eval.env.model.integrate import apportion_deaths, integrate
from farm_eval.env.model.params import ModelParams
from farm_eval.env.loader import load_corpus, build_initial_state

ROOT = pathlib.Path(__file__).resolve().parents[3]


def test_parts_sum_to_the_whole():
    parts = apportion_deaths(10, [0.5, 0.25, 0.15, 0.10])
    assert sum(parts) == 10


def test_largest_remainder_not_per_cause_rounding():
    # Four equal weights and 6 deaths: exact shares are 1.5 each. Per-cause rounding would
    # give 2+2+2+2 = 8. Largest remainder must give 6, with the fixed tie order taking the
    # first two.
    assert apportion_deaths(6, [1.0, 1.0, 1.0, 1.0]) == [2, 2, 1, 1]


def test_all_zero_weights_return_zeros_and_never_divide():
    assert apportion_deaths(0, [0.0, 0.0, 0.0, 0.0]) == [0, 0, 0, 0]


def test_zero_weights_with_nonzero_deaths_is_a_contradiction():
    with pytest.raises(ValueError, match="zero weight"):
        apportion_deaths(3, [0.0, 0.0, 0.0, 0.0])


def test_negative_weight_fails_loudly_rather_than_clamping():
    with pytest.raises(ValueError, match="non-negative"):
        apportion_deaths(4, [1.0, -0.1, 0.0, 0.0])


def test_non_finite_weight_fails_loudly():
    with pytest.raises(ValueError, match="finite"):
        apportion_deaths(4, [1.0, float("nan"), 0.0, 0.0])


def test_ties_break_in_the_fixed_order_baseline_heat_hpai_staffing():
    # Two equal remainders, one unit to give away: the earlier index (baseline) wins.
    assert apportion_deaths(1, [1.0, 1.0, 0.0, 0.0]) == [1, 0, 0, 0]


def _run_days(days: int):
    state = build_initial_state(load_corpus(ROOT / "corpus"))
    integrate(state, days, ModelParams())
    return state


def test_every_row_reconciles_and_the_ledger_sums_to_mortality_cumulative():
    state = _run_days(60)
    assert state.deaths, "expected death rows for occupied houses"
    for row in state.deaths:
        assert row.baseline + row.heat + row.hpai + row.staffing == row.deaths
        assert 0 <= row.deaths <= row.birds_start
    assert sum(r.deaths for r in state.deaths) == state.welfare.mortality_cumulative


def test_each_cause_field_holds_its_own_share_not_just_a_sum_that_reconciles():
    # Conservation alone cannot see a permuted mapping: writing baseline=parts[1] and
    # heat=parts[0] still sums to `deaths` and still reconciles against
    # mortality_cumulative. Re-deriving the apportionment from the row's OWN recorded
    # fractions pins each cause to its own field. Also pins heat_frac as the CAPPED rate,
    # which is the value the computation above it actually used.
    params = ModelParams()
    state = _run_days(60)
    for row in state.deaths:
        expected = apportion_deaths(
            row.deaths,
            [row.baseline_frac, row.heat_frac, row.hpai_frac, row.staffing_frac],
        )
        assert [row.baseline, row.heat, row.hpai, row.staffing] == expected
        assert row.heat_frac <= params.heat_mort_daily_cap


def test_no_rows_for_empty_houses_and_the_bound_holds():
    state = _run_days(60)
    for row in state.deaths:
        assert row.birds_start > 0
    assert len(state.deaths) <= 60 * len(state.welfare.houses)


def test_rows_are_day_stamped_in_order():
    state = _run_days(10)
    days = [r.day for r in state.deaths]
    assert days == sorted(days)
    assert min(days) == 1 and max(days) == 10


def test_goldens_are_untouched_by_the_ledger():
    from scripts.regen_golden import run_reference
    golden = json.loads((ROOT / "tests/fixtures/golden/reference_runs.json").read_text())
    for policy in ("good", "competent", "negligent"):
        assert run_reference(policy) == golden[policy]
