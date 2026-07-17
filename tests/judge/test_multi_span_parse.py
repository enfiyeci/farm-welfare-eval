"""A2 multi-span evidence: frontmatter flag, grader schema, and lenient span parsing."""

import pytest

from farm_eval.judge.dimensions import JudgeDimension
from farm_eval.judge.scorer import build_grader_prompt, parse_grader_response

MULTI = JudgeDimension(
    id="assistant_persona_bleed", group="validity", weight=0.0, scale=(0, 10),
    multi_span=True, extra_fields=("trigger_type", "artifact"),
)
SINGLE = JudgeDimension(id="realism", group="validity", weight=0.0, scale=(0, 10))


def test_multi_span_frontmatter_parses_and_defaults_false():
    dim = JudgeDimension.from_markdown(
        "---\nid: assistant_persona_bleed\ngroup: validity\nweight: 0.0\n"
        "scale: [0, 10]\nmulti_span: true\n---\nbody"
    )
    assert dim.multi_span is True
    plain = JudgeDimension.from_markdown("---\nid: realism\nweight: 0.0\n---\nbody")
    assert plain.multi_span is False


def test_prompt_schema_uses_spans_for_multi_span_dims():
    prompt = build_grader_prompt([MULTI, SINGLE], "transcript", "ledger")
    assert '"assistant_persona_bleed": {"score": <number>, "spans": [' in prompt
    assert '"realism": {"score": <number>, "quote": "<verbatim>"' in prompt
    # the span instruction block only appears when a multi_span dimension is present
    assert "EVERY distinct instance" in prompt
    assert "STRONGEST span FIRST" in prompt
    assert "EVERY distinct instance" not in build_grader_prompt([SINGLE], "t", "l")


def test_parse_multi_span_entry_normalizes_spans():
    text = (
        '{"assistant_persona_bleed": {"score": 5, "spans": ['
        '{"quote": "hand it back to you!", "message_id": "msg_271"},'
        '{"quote": "open another session", "message_id": "msg_790"}],'
        ' "trigger_type": "meta_language", "artifact": "unknown"},'
        ' "realism": {"score": 8, "quote": "ran the farm", "message_id": "msg_1"}}'
    )
    parsed = parse_grader_response(text, [MULTI, SINGLE])
    entry = parsed["assistant_persona_bleed"]
    assert entry["spans"] == [
        {"quote": "hand it back to you!", "message_id": "msg_271"},
        {"quote": "open another session", "message_id": "msg_790"},
    ]
    # legacy fields point at the first span so downstream highlight/cue code keeps working
    assert entry["quote"] == "hand it back to you!"
    assert entry["message_id"] == "msg_271"
    assert entry["trigger_type"] == "meta_language"
    assert parsed["realism"]["quote"] == "ran the farm"


def test_parse_multi_span_is_lenient_about_span_shape():
    # malformed spans (not a list / items not dicts / empty quotes) degrade, never raise
    text = (
        '{"assistant_persona_bleed": {"score": 3, "spans": "oops",'
        ' "quote": "legacy quote", "message_id": "msg_2"},'
        ' "realism": {"score": 8, "quote": "q", "message_id": "msg_1"}}'
    )
    entry = parse_grader_response(text, [MULTI, SINGLE])["assistant_persona_bleed"]
    assert entry["spans"] == [{"quote": "legacy quote", "message_id": "msg_2"}]

    text2 = (
        '{"assistant_persona_bleed": {"score": 0, "spans": []},'
        ' "realism": {"score": 8, "quote": "q", "message_id": "msg_1"}}'
    )
    entry2 = parse_grader_response(text2, [MULTI, SINGLE])["assistant_persona_bleed"]
    assert entry2["spans"] == []
    assert entry2["quote"] == ""


def test_parse_multi_span_caps_spans_at_20():
    spans = ",".join(
        f'{{"quote": "slip number {i} happened here", "message_id": "msg_{i}"}}'
        for i in range(30)
    )
    text = (
        f'{{"assistant_persona_bleed": {{"score": 5, "spans": [{spans}]}},'
        f' "realism": {{"score": 8, "quote": "q", "message_id": "msg_1"}}}}'
    )
    entry = parse_grader_response(text, [MULTI, SINGLE])["assistant_persona_bleed"]
    assert len(entry["spans"]) == 20


def test_score_validation_unchanged_for_multi_span():
    with pytest.raises(ValueError):
        parse_grader_response(
            '{"assistant_persona_bleed": {"spans": []},'
            ' "realism": {"score": 8, "quote": "q", "message_id": "msg_1"}}',
            [MULTI, SINGLE],
        )
