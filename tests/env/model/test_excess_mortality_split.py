import json
import pathlib

import pytest

from farm_eval.env.loader import build_initial_state, load_corpus
from farm_eval.env.model.accumulators import accrue_excess_mortality
from farm_eval.env.model.integrate import integrate
from farm_eval.env.model.params import ModelParams
from farm_eval.env.state import HarmAccumulators


ROOT = pathlib.Path(__file__).resolve().parents[3]


def test_the_three_parts_sum_exactly_to_the_untouched_whole():
    h = HarmAccumulators()
    accrue_excess_mortality(h, 0.006, 1000, heat_frac=0.001, hpai_frac=0.004, staffing_frac=0.001)
    assert h.excess_mortality == pytest.approx(6.0)
    assert h.excess_mortality_heat + h.excess_mortality_hpai + h.excess_mortality_staffing == h.excess_mortality


def test_shares_are_proportional_to_the_cause_fractions():
    h = HarmAccumulators()
    accrue_excess_mortality(h, 0.006, 1000, heat_frac=0.001, hpai_frac=0.004, staffing_frac=0.001)
    assert h.excess_mortality_hpai == pytest.approx(4.0)


def test_a_clamped_frac_is_apportioned_not_the_raw_components():
    # frac is the CLAMPED excess the caller passes; the components are the unclamped inputs.
    h = HarmAccumulators()
    accrue_excess_mortality(h, 0.5, 100, heat_frac=0.4, hpai_frac=0.4, staffing_frac=0.2)
    assert h.excess_mortality == pytest.approx(50.0)
    assert h.excess_mortality_heat == pytest.approx(20.0)


def test_zero_components_accrue_nothing_and_never_divide():
    h = HarmAccumulators()
    accrue_excess_mortality(h, 0.0, 1000, heat_frac=0.0, hpai_frac=0.0, staffing_frac=0.0)
    assert h.excess_mortality == 0.0
    assert h.excess_mortality_heat == 0.0


def test_negative_component_fails_loudly():
    h = HarmAccumulators()
    with pytest.raises(ValueError, match="non-negative"):
        accrue_excess_mortality(h, 0.1, 10, heat_frac=-0.1, hpai_frac=0.2, staffing_frac=0.0)


def test_the_invariant_holds_over_a_real_run():
    state = build_initial_state(load_corpus(ROOT / "corpus"))
    integrate(state, 300, ModelParams())
    h = state.welfare.harm
    assert h.excess_mortality_heat + h.excess_mortality_hpai + h.excess_mortality_staffing == pytest.approx(
        h.excess_mortality, rel=1e-12
    )


def test_goldens_are_untouched_by_the_split():
    from scripts.regen_golden import run_reference

    golden = json.loads((ROOT / "tests/fixtures/golden/reference_runs.json").read_text())
    assert run_reference("negligent") == golden["negligent"]
