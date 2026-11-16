"""Section 4: the card task. Draft gate in both places, metadata, a mockllm run, scripted solver."""

from __future__ import annotations

import asyncio
from pathlib import Path

import pytest
from inspect_ai import eval as inspect_eval
from inspect_ai.model import ChatMessageSystem, ChatMessageUser, ModelName
from inspect_ai.solver import TaskState

from farm_eval.card_task import card_solver, card_task
from farm_eval.cards.loader import load_bank
from farm_eval.cards.runsheet import build_rows, load_experiments, write_sheet

REPO_ROOT = Path(__file__).resolve().parents[2]
FIX = Path(__file__).resolve().parent / "fixtures" / "bank"
REAL = REPO_ROOT / "schedule" / "cards"
E7 = REAL / "runsheets" / "E7_noise_floor.csv"


def _sheet(tmp_path, exp_id="FX_small") -> Path:
    path = tmp_path / f"{exp_id}.csv"
    write_sheet(build_rows(load_bank(FIX), load_experiments(FIX / "experiments.yml"), exp_id), path)
    return path


def test_draft_gate_at_task_build(tmp_path):
    with pytest.raises(ValueError, match="draft"):
        card_task(sheet=str(_sheet(tmp_path)), cards_dir=str(FIX))
    task = card_task(sheet=str(_sheet(tmp_path)), cards_dir=str(FIX), allow_draft=True)
    assert len(task.dataset) == 32


def test_approved_sheet_builds_without_allow_draft():
    task = card_task(sheet=str(E7))
    assert len(task.dataset) == 80
    s = task.dataset[0]
    assert isinstance(s.input[0], ChatMessageSystem) and isinstance(s.input[1], ChatMessageUser)
    meta = s.metadata
    for col in ("row_id", "experiment", "card_id", "arm_id", "phrasing_id", "order", "price_form",
                "price_per_unit", "framing_id", "repeat", "text_status"):
        assert col in meta
    assert meta["protect_letter"] == "A"
    assert meta["priced_count"] == 124000 and meta["spared_count"] == 121500
    assert "planted_value_per_unit" not in meta
    assert task.config.max_tokens == 2000 and task.config.max_retries == 3
    assert task.config.temperature is None
    assert task.fail_on_error is False


def test_planted_value_and_null_system_in_samples(tmp_path):
    task = card_task(sheet=str(_sheet(tmp_path, "FX_planted")), cards_dir=str(FIX), allow_draft=True)
    values = {s.metadata["planted_value_per_unit"] for s in task.dataset}
    assert values == {"0", "0.40", "2.30"}


def _state(model: str, status: str) -> TaskState:
    return TaskState(model=ModelName(model), sample_id="x", epoch=1, input=[ChatMessageUser(content="hi")],
                     messages=[ChatMessageUser(content="hi")],
                     metadata={"text_status": status, "row_id": "x", "protect_letter": "A",
                               "price_per_unit": "1.50"})


def _run_solver(model: str, status: str, responder=None):
    calls = []

    async def generate(state, *args, **kwargs):
        calls.append(state)
        return state

    solve = card_solver(responder=responder, seed=0)
    result = asyncio.run(solve(_state(model, status), generate))
    return result, calls


def test_draft_gate_in_solver_refuses_a_real_model_before_generation():
    with pytest.raises(RuntimeError, match="draft"):
        _run_solver("anthropic/claude-x", "draft")
    with pytest.raises(RuntimeError, match="draft"):
        _run_solver("anthropic/claude-x", "draft", responder="always_protect")
    # Only the exact value owner_approved passes; a missing or unknown status counts as draft.
    with pytest.raises(RuntimeError, match="draft"):
        _run_solver("anthropic/claude-x", "")


def test_draft_gate_lets_mockllm_and_approved_through():
    _, calls = _run_solver("mockllm/model", "draft")
    assert len(calls) == 1
    _, calls = _run_solver("anthropic/claude-x", "owner_approved")
    assert len(calls) == 1


def test_scripted_responder_writes_the_answer_and_calls_no_model():
    state, calls = _run_solver("mockllm/model", "draft", responder="always_protect")
    assert calls == []
    assert state.output.completion.strip().endswith("DECISION: A")
    assert state.messages[-1].role == "assistant"


def test_mockllm_run_of_the_fixture_sheet_is_all_unresolved_missing(tmp_path):
    log = inspect_eval(card_task(sheet=str(_sheet(tmp_path)), cards_dir=str(FIX), allow_draft=True),
                       model="mockllm/model", display="none", log_dir=str(tmp_path / "logs"))[0]
    assert log.status == "success"
    assert len(log.samples) == 32
    for s in log.samples:
        score = s.scores["card_scorer"]
        assert score.value == "unresolved"
        assert score.metadata["status"] == "missing"


def test_scripted_run_through_inspect_records_the_responder(tmp_path):
    log = inspect_eval(card_task(sheet=str(_sheet(tmp_path)), cards_dir=str(FIX), allow_draft=True,
                                 responder="always_protect"),
                       model="mockllm/model", display="none", log_dir=str(tmp_path / "logs"))[0]
    assert log.status == "success"
    assert {s.scores["card_scorer"].value for s in log.samples} == {"protect"}
    assert {s.metadata["scripted_responder"] for s in log.samples} == {"always_protect"}


def test_task_file_runs_from_a_relative_path(tmp_path, monkeypatch):
    """Inspect chdirs into the task file's folder; data paths are anchored to the repo root."""
    monkeypatch.chdir(REPO_ROOT)
    log = inspect_eval("farm_eval/card_task.py",
                       task_args={"sheet": "schedule/cards/runsheets/E7_noise_floor.csv",
                                  "responder": "never_protect"},
                       model="mockllm/model", display="none", log_dir=str(tmp_path / "logs"))[0]
    assert log.status == "success"
    assert len(log.samples) == 80
    assert {s.scores["card_scorer"].value for s in log.samples} == {"decline"}


def test_unknown_responder_is_refused():
    with pytest.raises(ValueError, match="responder"):
        card_task(sheet=str(E7), responder="nobody")


def test_stale_sheet_status_is_refused(tmp_path):
    rows = build_rows(load_bank(FIX), load_experiments(FIX / "experiments.yml"), "FX_small")
    for r in rows:
        r["text_status"] = "owner_approved"
    path = tmp_path / "stale.csv"
    write_sheet(rows, path)
    with pytest.raises(ValueError, match="rebuild"):
        card_task(sheet=str(path), cards_dir=str(FIX))
