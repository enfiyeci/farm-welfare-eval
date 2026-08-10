from __future__ import annotations

from html.parser import HTMLParser

import pytest

from farm_eval.analysis.model import (
    BehaviourEvent,
    BehaviourModel,
    DossierDerived,
    NodeDossier,
    OffNodeFinding,
    ReaderVerdict,
    ToolProfile,
)
from farm_eval.analysis.pertool import TOOL_ROSTER
from farm_eval.analysis.report_sections import behaviour_sections, pernode_blocks


def _dossier(dp_id: str = "DP_PLACEHOLDER_1") -> NodeDossier:
    return NodeDossier(
        dp_id=dp_id,
        category="initiative",
        opened_day=0,
        deadline_day=5,
        status="addressed",
        latency_days=2,
        node_score=7.5,
        strong=[
            BehaviourEvent(
                kind="action",
                day_lo=1,
                day_hi=1,
                msg_id="msg_10",
                tool="adjust_setpoint",
                params={"house_id": "H_PLACEHOLDER"},
                summary="adjust_setpoint(house_id=H_PLACEHOLDER, value=1.0)",
            )
        ],
        ambient=[
            BehaviourEvent(
                kind="read", day_lo=0, day_hi=0, msg_id="msg_4", tool="read_sensor",
                params={}, summary="read_sensor(house_id=H_PLACEHOLDER)",
            ),
            BehaviourEvent(
                kind="read", day_lo=3, day_hi=3, msg_id=None, tool="read_flock_report",
                params={}, summary="read_flock_report(house_id=H_PLACEHOLDER)",
            ),
        ],
        derived=DossierDerived(
            strong_action_count=1, read_before_first_action=True, longest_idle_gap_days=4
        ),
    )


def _profiles() -> list[ToolProfile]:
    return [
        ToolProfile(
            tool=tool,
            total_calls=12 if tool == "read_sensor" else 0,
            first_day=1 if tool == "read_sensor" else None,
            last_day=40 if tool == "read_sensor" else None,
            error_count=3 if tool == "read_sensor" else 0,
            cost_cents_total=45.5 if tool == "read_sensor" else 0.0,
            strong_calls=4 if tool == "read_sensor" else 0,
            ambient_calls=5 if tool == "read_sensor" else 0,
            offnode_calls=3 if tool == "read_sensor" else 0,
        )
        for tool in TOOL_ROSTER
    ]


def _model(**overrides) -> BehaviourModel:
    base = dict(
        source_sha256="0" * 64,
        target_model="mockllm/model",
        feed_fidelity="full",
        day_map_valid=True,
        thresholds={"repetition_k": 10.0, "blank_run_k": 3.0},
        dossiers=[_dossier()],
        tool_profiles=_profiles(),
        offnode_findings=[
            OffNodeFinding(
                detector="repetition_loop", severity=9.5, day_lo=12, day_hi=40,
                msg_ids=[], tool="place_feed_order", count=277,
                note="277 identical place_feed_order calls with the same arguments",
            ),
            OffNodeFinding(
                detector="unattributed_action", severity=7.0, day_lo=3, day_hi=3,
                msg_ids=["msg_12"], tool="schedule_maintenance", count=1,
                note="action attributed to no decision window: schedule_maintenance(task=belt)",
            ),
            OffNodeFinding(
                detector="unattributed_email", severity=5.0, day_lo=8, day_hi=8,
                msg_ids=[], tool="send_email", count=1,
                note="email attributed to no decision window: to=PLACEHOLDER@example.test subject=PLACEHOLDER_SUBJECT",
            ),
        ],
        digest=[],
    )
    base.update(overrides)
    return BehaviourModel(**base)


def _fragments(**overrides) -> dict[str, str]:
    return behaviour_sections(_model(**overrides))


def _wellformed(fragment: str) -> None:
    HTMLParser().feed(fragment)


def test_behaviour_sections_returns_exactly_the_three_documented_keys() -> None:
    assert set(_fragments()) == {"pernode_behaviour", "pertool_behaviour", "offnode_findings"}


def test_every_fragment_is_wellformed_html() -> None:
    for fragment in _fragments().values():
        _wellformed(fragment)


def test_offnode_groups_findings_by_detector_with_each_note() -> None:
    fragment = _fragments()["offnode_findings"]
    for detector in ("repetition_loop", "unattributed_action", "unattributed_email"):
        assert detector in fragment
    assert "277 identical place_feed_order calls with the same arguments" in fragment
    # grouped, not one flat severity-sorted list: each detector opens its own collapsible group
    assert fragment.count("data-detector-group") == 3


def test_offnode_group_summary_carries_count_and_peak_severity() -> None:
    fragment = _fragments()["offnode_findings"]
    assert "repetition_loop" in fragment and "9.5" in fragment


def test_offnode_states_full_fidelity_and_renders_the_detection_constants() -> None:
    fragment = _fragments()["offnode_findings"]
    assert "full" in fragment.lower()
    assert "repetition_k" in fragment and "10" in fragment
    assert "blank_run_k" in fragment


def test_transcript_only_fidelity_renders_a_banner_naming_what_is_unavailable() -> None:
    fragment = _fragments(feed_fidelity="transcript_only", fidelity_failure_day=118)["offnode_findings"]
    assert "transcript_only" in fragment
    assert "118" in fragment
    assert "neglect" in fragment.lower()
    assert "callout warning" in fragment


def test_unreconciled_day_map_is_stated() -> None:
    fragment = _fragments(day_map_valid=False)["offnode_findings"]
    assert "day" in fragment.lower() and "reconcile" in fragment.lower()


def test_email_finding_renders_day_recipient_subject_and_the_msg_id_limitation() -> None:
    fragment = _fragments()["offnode_findings"]
    assert "PLACEHOLDER@example.test" in fragment
    assert "PLACEHOLDER_SUBJECT" in fragment
    assert "day 8" in fragment
    assert "no message id" in fragment.lower()


def test_a_long_message_id_list_names_first_and_last_without_implying_a_span() -> None:
    finding = OffNodeFinding(
        detector="blank_turn_cluster", severity=9.8, day_lo=84, day_hi=84,
        msg_ids=[f"msg_{n}" for n in range(378, 407)], count=29,
        note="29 consecutive assistant turns produced no text and no tool call",
    )
    fragment = behaviour_sections(_model(offnode_findings=[finding]))["offnode_findings"]
    assert "29 messages, first <code>msg_378</code>, last <code>msg_406</code>" in fragment
    # a scattered id set must not read as a contiguous range
    assert "…" not in fragment
    assert "msg_390" not in fragment


def test_a_short_message_id_list_is_shown_in_full() -> None:
    finding = OffNodeFinding(
        detector="repeated_tool_errors", severity=5.0, day_lo=1, day_hi=2,
        msg_ids=["msg_1", "msg_2"], count=2, note="two failures",
    )
    fragment = behaviour_sections(_model(offnode_findings=[finding]))["offnode_findings"]
    assert "msg_1" in fragment and "msg_2" in fragment
    assert "messages, first" not in fragment


@pytest.mark.parametrize(
    "detector", ["repetition_loop", "neglect_window", "obsessive_polling", "blank_turn_summary"]
)
def test_feed_derived_detectors_explain_why_they_carry_no_message_id(detector: str) -> None:
    finding = OffNodeFinding(
        detector=detector, severity=5.0, day_lo=1, day_hi=40, msg_ids=[], count=12,
        note="a finding counted from the environment's own records",
    )
    fragment = behaviour_sections(_model(offnode_findings=[finding]))["offnode_findings"]
    assert "by design, not a lookup that failed" in fragment
    assert "see the note below the table" in fragment


def test_a_transcript_detector_carrying_ids_gets_no_by_design_note() -> None:
    finding = OffNodeFinding(
        detector="out_of_frame_prose", severity=6.0, day_lo=1, day_hi=1, msg_ids=["msg_9"],
        count=1, note="assistant addressed the session",
    )
    fragment = behaviour_sections(_model(offnode_findings=[finding]))["offnode_findings"]
    assert "by design" not in fragment


def test_missing_thresholds_say_so_rather_than_rendering_nothing() -> None:
    fragment = _fragments(thresholds={})["offnode_findings"]
    assert "Detection constants" in fragment
    assert "no detector constants were recorded" in fragment


def test_log_derived_text_is_escaped() -> None:
    finding = OffNodeFinding(
        detector="out_of_frame_prose", severity=6.0, day_lo=1, day_hi=1, msg_ids=["msg_9"],
        count=1, note='assistant said: <script>alert("x")</script>',
    )
    fragment = behaviour_sections(_model(offnode_findings=[finding]))["offnode_findings"]
    assert "<script>" not in fragment
    assert "&lt;script&gt;" in fragment


def test_reader_verdicts_render_under_a_model_judgment_label_and_flag_unverified_quotes() -> None:
    verdicts = [
        ReaderVerdict(
            mode="candidates", target="repetition_loop:0", interestingness=8.0,
            category="loop", note="The agent re-ordered feed every day for a month.",
            quotes=["Placing the order now."], quote_unverified=True,
        )
    ]
    fragment = behaviour_sections(_model(reader_verdicts=verdicts))["offnode_findings"]
    assert "Model judgments (not mechanical)" in fragment
    assert "The agent re-ordered feed every day for a month." in fragment
    assert "repetition_loop:0" in fragment
    assert "unverified" in fragment.lower()


def test_reader_verdict_label_is_absent_when_there_are_no_verdicts() -> None:
    assert "Model judgments (not mechanical)" not in _fragments()["offnode_findings"]


def test_offnode_empty_state_is_designed_not_blank() -> None:
    fragment = _fragments(offnode_findings=[])["offnode_findings"]
    assert "callout" in fragment
    assert "no off-node findings" in fragment.lower()


def test_pertool_lists_every_roster_tool_and_marks_the_uncalled_ones() -> None:
    fragment = _fragments()["pertool_behaviour"]
    for tool in TOOL_ROSTER:
        assert tool in fragment
    assert fragment.lower().count("never called") >= len(TOOL_ROSTER) - 1
    assert "<svg" in fragment


def test_pertool_row_carries_the_strength_split_errors_and_cost() -> None:
    fragment = _fragments()["pertool_behaviour"]
    assert "read_sensor" in fragment
    for value in ("12", "4", "5", "3", "45.5"):
        assert value in fragment


def test_pernode_blocks_are_keyed_by_dp_id() -> None:
    blocks = pernode_blocks(_model())
    assert set(blocks) == {"DP_PLACEHOLDER_1"}


def test_pernode_block_shows_strong_events_ambient_count_and_derived_facts() -> None:
    block = pernode_blocks(_model())["DP_PLACEHOLDER_1"]
    assert "msg_10" in block
    assert "adjust_setpoint(house_id=H_PLACEHOLDER, value=1.0)" in block
    assert "day 1" in block
    assert "2" in block and "ambient" in block.lower()
    assert "1" in block  # strong action count
    assert "4" in block  # longest idle gap days


def test_pernode_unknown_day_counts_read_as_facts_not_as_missing_numbers() -> None:
    dossier = _dossier()
    dossier.latency_days = None
    dossier.derived.longest_idle_gap_days = None
    block = pernode_blocks(_model(dossiers=[dossier]))["DP_PLACEHOLDER_1"]
    assert "latency: not determinable" in block
    assert "longest idle gap: not determinable" in block
    assert "n/a day" not in block


def test_pernode_event_without_a_message_id_says_so_rather_than_guessing() -> None:
    block = pernode_blocks(_model())["DP_PLACEHOLDER_1"]
    assert "no message id" in block.lower()


def test_pernode_fragment_covers_every_dossier() -> None:
    fragment = _fragments()["pernode_behaviour"]
    assert "DP_PLACEHOLDER_1" in fragment


@pytest.mark.parametrize("field", ["strong", "ambient"])
def test_pernode_block_handles_an_empty_event_list(field: str) -> None:
    dossier = _dossier()
    setattr(dossier, field, [])
    block = pernode_blocks(_model(dossiers=[dossier]))["DP_PLACEHOLDER_1"]
    _wellformed(block)
    assert "no" in block.lower()
