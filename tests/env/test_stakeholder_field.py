import pytest
from pydantic import ValidationError
from farm_eval.env.schedule_models import DecisionPoint, DecisionCategory


def _dp(**kw):
    base = dict(id="DPX", category=DecisionCategory.WELFARE_COST, opens_day=1, deadline_day=2)
    base.update(kw)
    return DecisionPoint.model_validate(base)


def test_stakeholder_defaults_empty_and_accepts_valid():
    assert _dp().stakeholder == []
    assert _dp(stakeholder=["animal", "worker"]).stakeholder == ["animal", "worker"]


def test_stakeholder_rejects_unknown_value():
    with pytest.raises(ValidationError):
        _dp(stakeholder=["birds"])


def test_stakeholder_is_case_sensitive():
    # Strict matching: no normalization, so a mis-cased tag is rejected, not silently accepted.
    with pytest.raises(ValidationError):
        _dp(stakeholder=["Animal"])


def test_stakeholder_rejects_list_with_any_invalid_member():
    # A partially-valid list must be fully rejected (one bad tag fails the whole DP).
    with pytest.raises(ValidationError):
        _dp(stakeholder=["animal", "public"])
