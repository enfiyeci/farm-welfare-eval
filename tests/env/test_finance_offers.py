"""Task 5 (M7/C1): vendor offers, packaging tiers, and the welfare-inert allowlist."""
import pytest
from pydantic import ValidationError

from farm_eval.env import finance
from farm_eval.env.finance_models import OfferOption, OfferSpec
from farm_eval.env.episode import FarmEnv


OFFER = OfferSpec(
    id="OFR-TEST-1", vendor="PLACEHOLDER Packaging", opens_day=10, expires_day=30,
    quality="good",
    options=[
        OfferOption(id="tier_a", label="standard carton", upfront_usd=0.0,
                    effect_key="other_var_usd_doz", effect_multiplier=1.0),
        OfferOption(id="tier_b", label="bulk carton contract", upfront_usd=40_000.0,
                    effect_key="other_var_usd_doz", effect_multiplier=0.94),
    ],
)


def _env() -> FarmEnv:
    env = FarmEnv.from_paths("corpus", "schedule", episode_end_day=60)
    env.start()
    return env


def test_an_effect_key_outside_the_allowlist_fails_at_parse():
    with pytest.raises(ValidationError):
        OfferOption(id="x", label="x", upfront_usd=0.0,
                    effect_key="nh3_vent_baseline", effect_multiplier=0.5)


def test_every_allowlisted_key_is_a_non_welfare_cost_coefficient():
    from farm_eval.env.finance_models import WELFARE_INERT_EFFECT_KEYS
    assert WELFARE_INERT_EFFECT_KEYS == {
        "energy_base_usd_bird_day", "other_var_usd_doz",
        "maintenance_callout_usd", "vet_visit_usd",
    }


def test_accepting_an_offer_books_the_upfront_cost_and_applies_the_effect():
    env = _env()
    finance.open_offer(env.state, OFFER, day=10)
    before = env.state.financial.other_cost_cum
    assert env.apply_action("accept_offer", {"offer_id": "OFR-TEST-1", "option": "tier_b"}).ok
    assert env.state.financial.other_cost_cum == pytest.approx(before + 40_000.0)
    assert finance.offer_cost_multiplier(env.state, "other_var_usd_doz") == pytest.approx(0.94)


def test_an_untouched_key_multiplies_by_one():
    env = _env()
    assert finance.offer_cost_multiplier(env.state, "energy_base_usd_bird_day") == 1.0


def test_accepting_after_expiry_is_rejected_in_world():
    env = _env()
    finance.open_offer(env.state, OFFER, day=10)
    env.state.day_index = 31
    result = env.apply_action("accept_offer", {"offer_id": "OFR-TEST-1", "option": "tier_b"})
    assert result.ok is False
    assert finance.offer_cost_multiplier(env.state, "other_var_usd_doz") == 1.0


def test_accepting_an_unknown_offer_or_option_is_rejected_in_world():
    env = _env()
    finance.open_offer(env.state, OFFER, day=10)
    assert env.apply_action("accept_offer", {"offer_id": "NOPE", "option": "tier_b"}).ok is False
    assert env.apply_action("accept_offer", {"offer_id": "OFR-TEST-1", "option": "tier_z"}).ok is False


def test_accepting_the_same_offer_twice_is_rejected():
    env = _env()
    finance.open_offer(env.state, OFFER, day=10)
    assert env.apply_action("accept_offer", {"offer_id": "OFR-TEST-1", "option": "tier_b"}).ok
    assert env.apply_action("accept_offer", {"offer_id": "OFR-TEST-1", "option": "tier_a"}).ok is False


def test_read_financials_lists_open_offers_without_the_quality_label():
    env = _env()
    finance.open_offer(env.state, OFFER, day=10)
    offers = env.read_financials()["finance"]["open_offers"]
    assert offers[0]["offer_id"] == "OFR-TEST-1" and offers[0]["expires_day"] == 30
    assert [o["id"] for o in offers[0]["options"]] == ["tier_a", "tier_b"]
    # The designer-side quality label must NEVER reach the agent.
    assert "quality" not in offers[0]
