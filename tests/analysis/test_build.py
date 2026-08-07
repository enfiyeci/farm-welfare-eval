"""Task 9 -- the behaviour-model orchestrator, and its scripted-episode golden.

The integration half runs ONE scripted keyless `mockllm` episode per module (the repo's
end-to-end pattern) through `build_behaviour_model` and asserts the result against the committed
golden. The episode and the golden come from `scripts/regen_behaviour_golden.py`, imported here so
the test and the golden are the same episode by construction -- the same arrangement
`tests/spectator/test_extract.py` uses with `scripts/regen_spectator_golden.py`.

The unit half pins the two joins the orchestrator owns and no earlier task could test: the
`msg_N` link onto action/read events (spec §2.1) and the two-clock cross-check (spec §2.2).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from farm_eval.analysis import build as build_module
from farm_eval.analysis.build import (
    _errors_by_tool,
    _link_msg_ids,
    build_behaviour_model,
)
from farm_eval.analysis.model import BehaviourEvent
from farm_eval.analysis.offnode import THRESHOLDS
from scripts.regen_behaviour_golden import (
    GOLDEN_PATH,
    PLACEHOLDER_SHA256,
    build_golden_model,
    normalize_model,
)

_FIXTURE_DP = "DP_PLACEHOLDER_1"


@pytest.fixture(scope="module")
def episode(tmp_path_factory) -> tuple[str, object]:
    """The scripted episode's log location and the behaviour model built from it."""
    return build_golden_model(tmp_path_factory.mktemp("behaviour"))


@pytest.fixture(scope="module")
def model(episode):
    return episode[1]


# --- the run header -------------------------------------------------------------------


def test_the_scripted_episode_replays_at_full_fidelity(model) -> None:
    assert model.feed_fidelity == "full"
    assert model.fidelity_failure_day is None


def test_the_recorded_clock_reconciles(model) -> None:
    assert model.day_map_valid is True


def test_the_header_carries_the_run_identity_and_every_threshold(model) -> None:
    assert len(model.source_sha256) == 64
    assert model.target_model == "mockllm/model"
    assert model.thresholds == dict(THRESHOLDS)
    assert model.schema_version == 1
    assert model.reader_verdicts == []


# --- the stages are actually wired ----------------------------------------------------


def test_the_fixture_decision_point_has_a_strong_behavioural_record(model) -> None:
    dossier = next(d for d in model.dossiers if d.dp_id == _FIXTURE_DP)
    assert dossier.strong, "the scripted adjust_setpoint must attribute strongly to the node"
    assert any(e.tool == "adjust_setpoint" for e in dossier.strong)


def test_the_scripted_calls_appear_in_the_tool_profiles(model) -> None:
    profiles = {p.tool: p for p in model.tool_profiles}
    assert profiles["send_email"].total_calls == 1
    assert profiles["schedule_maintenance"].total_calls == 1
    assert profiles["end_day"].total_calls >= 1


def test_the_digest_is_day_segmented_and_carries_entries(model) -> None:
    assert model.digest, "a full-fidelity episode must produce digest days"
    assert [d.day for d in model.digest] == sorted(d.day for d in model.digest)
    assert any(day.entries for day in model.digest)


def test_action_events_carry_their_msg_n_link(model) -> None:
    dossier = next(d for d in model.dossiers if d.dp_id == _FIXTURE_DP)
    setpoint = next(e for e in dossier.strong if e.tool == "adjust_setpoint")
    assert setpoint.msg_id is not None and setpoint.msg_id.startswith("msg_")


# --- the golden -----------------------------------------------------------------------


def test_the_built_model_matches_the_committed_golden(model) -> None:
    golden = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
    assert normalize_model(model) == golden, (
        "behaviour model drifted from the golden; regenerate with "
        "./venv/bin/python scripts/regen_behaviour_golden.py and review the diff"
    )


def test_normalization_replaces_the_per_run_source_hash(model) -> None:
    assert normalize_model(model)["source_sha256"] == PLACEHOLDER_SHA256


# --- the msg_N link (spec §2.1) -------------------------------------------------------


def _assistant(msg_id: str, function: str, arguments: dict) -> dict:
    return {
        "id": msg_id,
        "role": "assistant",
        "text": "",
        "tool_calls": [{"id": f"{function}_x", "function": function, "arguments": arguments}],
    }


def _event(tool: str, params: dict, day: int) -> BehaviourEvent:
    return BehaviourEvent(kind="action", day_lo=day, day_hi=day, tool=tool, params=params)


def test_two_identical_calls_on_one_day_claim_two_distinct_messages_in_order() -> None:
    args = {"house_id": "H_A", "system": "ventilation", "value": 1.0}
    transcript = [_assistant("msg_1", "adjust_setpoint", args), _assistant("msg_3", "adjust_setpoint", args)]
    day_map = {"msg_1": 4, "msg_3": 4}
    first, second = _event("adjust_setpoint", args, 4), _event("adjust_setpoint", args, 4)

    _link_msg_ids([first, second], transcript, day_map)

    assert (first.msg_id, second.msg_id) == ("msg_1", "msg_3")


def test_an_unmatched_event_keeps_no_msg_id() -> None:
    transcript = [_assistant("msg_1", "adjust_setpoint", {"house_id": "H_A"})]
    event = _event("place_feed_order", {"ration": "LP2"}, 4)

    _link_msg_ids([event], transcript, {"msg_1": 4})

    assert event.msg_id is None


def test_a_call_on_a_different_day_is_not_claimed_when_the_clock_is_trusted() -> None:
    args = {"house_id": "H_A"}
    transcript = [_assistant("msg_1", "adjust_setpoint", args)]
    event = _event("adjust_setpoint", args, 9)

    _link_msg_ids([event], transcript, {"msg_1": 4})

    assert event.msg_id is None


def test_without_a_trusted_clock_the_day_is_not_required_to_agree() -> None:
    args = {"house_id": "H_A"}
    transcript = [_assistant("msg_1", "adjust_setpoint", args)]
    event = _event("adjust_setpoint", args, 9)

    _link_msg_ids([event], transcript, None)

    assert event.msg_id == "msg_1"


# --- the two-clock cross-check (spec §2.2) --------------------------------------------


def test_a_day_map_that_disagrees_with_the_feed_clock_fails_loudly(episode, monkeypatch) -> None:
    log_location, _ = episode
    real_extract = build_module.extract

    def doctored(path):
        report_model = real_extract(path)
        report_model["day_map"] = {mid: day + 100 for mid, day in report_model["day_map"].items()}
        return report_model

    monkeypatch.setattr(build_module, "extract", doctored)
    with pytest.raises(ValueError, match="clock"):
        build_behaviour_model(log_location)


# --- error classification -------------------------------------------------------------


def test_errors_by_tool_counts_harness_errors_and_in_band_json_errors() -> None:
    transcript = [
        {"id": "msg_1", "role": "tool", "function": "read_sensor", "text": "", "error": "boom"},
        {"id": "msg_2", "role": "tool", "function": "read_sensor",
         "text": json.dumps({"error": "no sensor"}), "error": None},
        {"id": "msg_3", "role": "tool", "function": "read_sensor",
         "text": json.dumps({"value": 4.2}), "error": None},
        {"id": "msg_4", "role": "assistant", "text": json.dumps({"error": "not a tool row"})},
    ]

    assert _errors_by_tool(transcript) == {"read_sensor": 2}


def test_a_clean_transcript_has_no_tool_errors() -> None:
    assert _errors_by_tool([{"id": "msg_1", "role": "tool", "function": "read_sensor",
                             "text": "ok", "error": None}]) == {}
