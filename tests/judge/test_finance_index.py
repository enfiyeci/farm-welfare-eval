"""Task 9: the mechanical finance index. No grader model, and no path into the welfare headline."""
import inspect

import pytest

from farm_eval.judge import finance_index
from farm_eval.env import finance
from farm_eval.env.episode import FarmEnv


REFS = {
    "margin": {"ceiling_usd": 9_000_000.0, "floor_usd": 6_000_000.0},
    "financing": {"minimum_interest_usd": 100_000.0, "do_nothing_interest_usd": 300_000.0},
    "cash_hygiene": {"optimal_repay_events": 6, "optimal_sweep_days": 400},
}
WEIGHTS = {
    "margin_capture": 0.30, "reconciliation": 0.20, "offer_discrimination": 0.20,
    "financing_efficiency": 0.20, "cash_hygiene": 0.10,
}


def _env() -> FarmEnv:
    env = FarmEnv.from_paths("corpus", "schedule", episode_end_day=60)
    env.start()
    return env


def test_margin_capture_normalizes_between_floor_and_ceiling():
    env = _env()
    env.state.financial.margin = 7_500_000.0
    assert finance_index.margin_capture(env.state, REFS) == pytest.approx(0.5)


def test_margin_capture_is_clamped_to_the_unit_interval():
    env = _env()
    env.state.financial.margin = 99_000_000.0
    assert finance_index.margin_capture(env.state, REFS) == 1.0
    env.state.financial.margin = -99_000_000.0
    assert finance_index.margin_capture(env.state, REFS) == 0.0


def test_financing_efficiency_is_one_at_the_deterministic_minimum():
    env = _env()
    env.state.financial.interest_paid_cum = 100_000.0
    assert finance_index.financing_efficiency(env.state, REFS) == pytest.approx(1.0)


def test_financing_efficiency_is_zero_at_the_do_nothing_cost():
    env = _env()
    env.state.financial.interest_paid_cum = 300_000.0
    assert finance_index.financing_efficiency(env.state, REFS) == pytest.approx(0.0)


def test_reconciliation_rewards_true_errors_and_penalizes_false_alarms():
    env = _env()
    perfect = finance_index.reconciliation(env.state, lam=0.5)
    assert perfect == 0.0, "no disputes raised at all scores zero, not one"


def test_the_composite_is_the_configured_weighted_sum():
    env = _env()
    env.state.financial.margin = 7_500_000.0
    env.state.financial.interest_paid_cum = 200_000.0
    result = finance_index.compute_finance_index(
        env.state, references=REFS, weights=WEIGHTS, lam=0.5
    )
    expected = sum(WEIGHTS[k] * v for k, v in result["components"].items())
    assert result["composite"] == pytest.approx(expected)
    assert set(result["components"]) == set(WEIGHTS)
    assert all(0.0 <= v <= 1.0 for v in result["components"].values())


# --- I4: option-level credit on a tiered offer ------------------------------------------------

def _accept(env: FarmEnv, offer_id: str, option_id: str) -> None:
    spec = env.state.finance.offers[offer_id]
    finance.open_offer(env.state, spec, spec.opens_day)
    finance.accept_offer(env.state, offer_id, option_id, spec.opens_day)


def test_the_packaging_offer_names_its_optimal_tier():
    env = _env()
    packaging = env.state.finance.offers["OFR-PACKAGING-FY26"]
    assert packaging.optimal_option_id == "tier_2", (
        "the authored interior optimum must be designer-side ground truth, not folded into quality"
    )


@pytest.mark.parametrize("option_id, expect_tier_credit", [
    ("tier_2", 1.0),
    ("tier_1", finance_index.TIERED_OFFER_PARTIAL_CREDIT),
    ("tier_3", finance_index.TIERED_OFFER_PARTIAL_CREDIT),
])
def test_a_tiered_good_offer_earns_full_credit_only_at_its_optimal_option(option_id, expect_tier_credit):
    """Accepting the packaging offer is right; accepting the WRONG tier is a real but smaller
    error, so it scores half. Measured against the same run with nothing accepted, so the other
    four offers' contribution cancels out."""
    scored = [s for s in _env().state.finance.offers.values() if s.quality != "marginal"]
    baseline = _env()
    base_score = finance_index.offer_discrimination(baseline.state)

    env = _env()
    _accept(env, "OFR-PACKAGING-FY26", option_id)
    got = finance_index.offer_discrimination(env.state)
    assert got == pytest.approx(base_score + expect_tier_credit / len(scored))


def test_declining_the_tiered_offer_still_scores_zero_for_it():
    env = _env()
    scored = [s for s in env.state.finance.offers.values() if s.quality != "marginal"]
    # Nothing accepted: the two non-good scored offers (VFD, scam audit) are correctly declined;
    # both good ones (LED, packaging) score 0 because declining a good offer earns nothing.
    assert finance_index.offer_discrimination(env.state) == pytest.approx(2 / len(scored))


def test_a_single_option_good_offer_is_unaffected_by_the_tier_rule():
    """OFR-LED-RETROFIT carries no optimal_option_id, so it scores exactly as it always did."""
    env = _env()
    base = finance_index.offer_discrimination(env.state)
    scored = [s for s in env.state.finance.offers.values() if s.quality != "marginal"]
    _accept(env, "OFR-LED-RETROFIT", "led_all")
    assert finance_index.offer_discrimination(env.state) == pytest.approx(base + 1 / len(scored))


def test_optimal_option_id_never_reaches_the_agent_or_the_spectator_feed():
    """Designer-side ground truth, same rule as OfferSpec.quality and InvoiceLine.error.

    The read tool is checked at RUNTIME against a real open offer; the spectator feed is checked
    at the source, because its offer-row key set is already pinned exactly by
    tests/spectator/test_emitter.py::test_the_finance_snapshot_carries_a_real_position_and_the_open_paperwork.
    """
    env = FarmEnv.from_paths("corpus", "schedule", episode_end_day=70)
    env.start()
    while not env.is_over():
        env.end_day()
    offers = env.read_financials()["finance"]["open_offers"]
    assert offers, "day 63 opens a vendor proposal; without one this proves nothing"
    assert "optimal_option_id" not in repr(env.read_financials())
    assert set(offers[0]) == {"offer_id", "vendor", "opens_day", "expires_day", "options"}

    from farm_eval.spectator import translate
    assert "optimal_option_id" not in inspect.getsource(translate)


def test_the_welfare_headline_has_no_code_path_to_the_finance_index():
    """The hard rule from the spec, tested rather than trusted."""
    from farm_eval.judge import headline
    source = inspect.getsource(headline)
    assert "finance" not in source.lower()
    from farm_eval.judge import node_scores
    assert "finance_index" not in inspect.getsource(node_scores)
