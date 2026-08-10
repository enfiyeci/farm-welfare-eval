import pytest
from pydantic import ValidationError

from farm_eval.analysis.model import BehaviourEvent, BehaviourModel, DossierDerived, NodeDossier


def test_behaviour_model_round_trips_through_json() -> None:
    model = BehaviourModel(
        source_sha256="a" * 64, target_model="mockllm/model", feed_fidelity="full",
        day_map_valid=True, thresholds={"repetition_k": 5.0}, dossiers=[], tool_profiles=[],
        offnode_findings=[], digest=[],
    )
    assert BehaviourModel.model_validate_json(model.model_dump_json()) == model


def test_extra_fields_are_rejected() -> None:
    with pytest.raises(ValidationError):
        BehaviourEvent(kind="action", day_lo=1, day_hi=1, surprise=True)


def test_dossier_requires_derived() -> None:
    with pytest.raises(ValidationError):
        NodeDossier(dp_id="DP_PLACEHOLDER_1", category="welfare_cost", opened_day=0,
                    deadline_day=5, status="open")
