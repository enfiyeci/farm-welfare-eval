import pytest
from pydantic import ValidationError

from farm_eval.env.model.params import ModelParams


def test_modelparams_rejects_mismatched_downgrade_lists():
    # The downgrade age/value anchors are a parallel-list table like breed_/keel_/feather_;
    # a length mismatch must fail fast at construction, not silently survive until _interp.
    with pytest.raises(ValidationError):
        ModelParams(downgrade_age_wk=[30, 80], downgrade_frac_pct=[3.2])


def test_economic_params_present_with_research_anchored_defaults():
    p = ModelParams()
    # Downgrade curve anchors (weak-shell share rises with age): 3.2% @30wk -> 23.8% @80wk
    assert p.downgrade_age_wk[0] == 30 and p.downgrade_age_wk[-1] == 80
    assert p.downgrade_frac_pct[0] == 3.2 and p.downgrade_frac_pct[-1] == 23.8
    # Cost lines (cage-free, $/doz unless noted) — placeholders from research, verify at C7
    assert 0.05 <= p.labor_usd_doz <= 0.10        # ~$0.074/doz cage-free
    assert 0.10 <= p.capital_usd_doz <= 0.20      # ~$0.162/doz aviary
    assert 0.20 <= p.other_var_usd_doz <= 0.35    # misc variable
    assert 0.0 <= p.breaker_price_frac <= 1.0     # breaker price as fraction of shell price
    assert p.pullet_cost_usd >= 4.0               # ~$5/bird point-of-lay
