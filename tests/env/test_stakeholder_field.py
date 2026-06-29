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
