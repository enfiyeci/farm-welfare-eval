"""A2 frequency-weighted aggregation: span validation/dedupe, the log-count formula,
median-of-samples, and the axis_span_counts metadata the report generator reads (F-R3-6)."""

import json
import math

from farm_eval.judge.dimensions import JudgeDimension
from farm_eval.judge.scorer import (
    SPAN_WEIGHT_K,
    aggregate_multi_span,
    average_samples,
    axis_span_counts,
    collect_cue_localization,
    parse_grader_response,
    sanitize_dimension_sample,
)

MULTI = JudgeDimension(
    id="assistant_persona_bleed", group="validity", weight=0.0, scale=(0, 10),
    multi_span=True, extra_fields=("trigger_type", "artifact"),
)
SINGLE = JudgeDimension(id="realism", group="validity", weight=0.0, scale=(0, 10))
DIMS = [MULTI, SINGLE]

INDEX = {
    "msg_1": "Let me know if you need to open another operating session!",
    "msg_2": "I will convene another operating session!",
    "msg_3": "email sent to someone@example.com",
    "msg_4": "Let me know if you need to open another operating session!",
    "msg_5": "Please open another operating session tomorrow before noon.",
    "msg_A": (
        '[tool_call send_email {"to": "ops@example.com", "subject": "Heat plan", '
        '"body": "Increase ventilation"}]'
    ),
    "msg_B": (
        '[tool_call log_treatment {"house_id": "H1", "issue": "red mites", '
        '"route": "oral"}]'
    ),
    "msg_C": (
        "I handled both follow-ups.\n"
        '[tool_call send_email {"to": "ops@example.com", "subject": "Heat plan", '
        '"body": "Increase ventilation"}]\n'
        '[tool_call log_treatment {"house_id": "H1", "issue": "red mites", '
        '"route": "oral"}]'
    ),
}


def _entry(score, spans, **extra):
    base = {"score": score, "quote": spans[0]["quote"] if spans else "",
            "message_id": spans[0]["message_id"] if spans else "", "spans": spans,
            "trigger_type": "meta_language", "artifact": "unknown"}
    base.update(extra)
    return base


def _sample(multi_entry):
    return {
        "assistant_persona_bleed": multi_entry,
        "realism": {"score": 8.0, "quote": "email sent to someone@example.com", "message_id": "msg_3"},
    }


def _parsed_multi(raw_entry):
    response = {
        "assistant_persona_bleed": raw_entry,
        "realism": {"score": 8.0, "quote": "email sent to someone@example.com", "message_id": "msg_3"},
    }
    return parse_grader_response(json.dumps(response), DIMS)


def test_sanitize_validates_dedupes_and_notes_span_drops():
    spans = [
        {"quote": "open another operating session", "message_id": "msg_1"},
        {"quote": "open another operating session", "message_id": "msg_1"},  # dupe
        {"quote": "this span is fabricated entirely and appears nowhere at all", "message_id": "msg_2"},
    ]
    notes: list[dict] = []
    out = sanitize_dimension_sample(_sample(_entry(5.0, spans)), DIMS, INDEX, notes, 0)
    entry = out["assistant_persona_bleed"]
    assert entry["spans"] == [{"quote": "open another operating session", "message_id": "msg_1"}]
    span_notes = [n for n in notes if n.get("span")]
    assert len(span_notes) == 1 and span_notes[0]["dimension"] == "assistant_persona_bleed"


def test_sanitize_coalesces_contained_quotes_in_same_message_before_aggregation():
    spans = [
        {"quote": "Let me know if you need to open another operating session!", "message_id": "msg_1"},
        {"quote": "open another operating session", "message_id": "msg_1"},
    ]
    notes: list[dict] = []
    out = sanitize_dimension_sample(_sample(_entry(5.0, spans)), DIMS, INDEX, notes, 0)
    entry = aggregate_multi_span(out["assistant_persona_bleed"], MULTI)

    assert entry["spans"] == [spans[0]]
    assert entry["span_count"] == 1
    assert notes == []


def test_sanitize_coalesces_partially_overlapping_quotes_in_same_message():
    spans = [
        {"quote": "open another operating session", "message_id": "msg_5"},
        {"quote": "operating session tomorrow", "message_id": "msg_5"},
    ]
    notes: list[dict] = []
    out = sanitize_dimension_sample(_sample(_entry(5.0, spans)), DIMS, INDEX, notes, 0)
    entry = aggregate_multi_span(out["assistant_persona_bleed"], MULTI)

    assert entry["spans"] == [spans[0]]
    assert entry["span_count"] == 1
    assert notes == []


def test_sanitize_coalesces_all_unlocatable_quotes_in_same_message():
    spans = [
        {
            "quote": (
                '[tool_call send_email {"subject": "Heat plan", "body": "Increase ventilation", '
                '"to": "ops@example.com"}]'
            ),
            "message_id": "msg_A",
        },
        {
            "quote": (
                '[tool_call send_email {"body": "Increase ventilation", "to": "ops@example.com", '
                '"subject": "Heat plan"}]'
            ),
            "message_id": "msg_A",
        },
    ]
    notes: list[dict] = []
    out = sanitize_dimension_sample(_sample(_entry(5.0, spans)), DIMS, INDEX, notes, 0)
    entry = aggregate_multi_span(out["assistant_persona_bleed"], MULTI)

    assert entry["spans"] == [spans[0]]
    assert entry["span_count"] == 1
    assert notes == []


def test_sanitize_keeps_unlocatable_quotes_from_different_tool_call_segments():
    spans = [
        {
            "quote": (
                '[tool_call send_email {"subject": "Heat plan", "body": "Increase ventilation", '
                '"to": "ops@example.com"}]'
            ),
            "message_id": "msg_C",
        },
        {
            "quote": (
                '[tool_call log_treatment {"issue": "red mites", "route": "oral", '
                '"house_id": "H1"}]'
            ),
            "message_id": "msg_C",
        },
    ]
    notes: list[dict] = []
    out = sanitize_dimension_sample(_sample(_entry(5.0, spans)), DIMS, INDEX, notes, 0)
    entry = aggregate_multi_span(out["assistant_persona_bleed"], MULTI)

    assert entry["spans"] == spans
    assert entry["span_count"] == 2
    assert notes == []


def test_sanitize_coalesces_reorderings_of_same_tool_call_segment():
    spans = [
        {
            "quote": (
                '[tool_call send_email {"subject": "Heat plan", "body": "Increase ventilation", '
                '"to": "ops@example.com"}]'
            ),
            "message_id": "msg_C",
        },
        {
            "quote": (
                '[tool_call send_email {"body": "Increase ventilation", "to": "ops@example.com", '
                '"subject": "Heat plan"}]'
            ),
            "message_id": "msg_C",
        },
    ]
    notes: list[dict] = []
    out = sanitize_dimension_sample(_sample(_entry(5.0, spans)), DIMS, INDEX, notes, 0)
    entry = aggregate_multi_span(out["assistant_persona_bleed"], MULTI)

    assert entry["spans"] == [spans[0]]
    assert entry["span_count"] == 1
    assert notes == []


def test_sanitize_keeps_unlocatable_quotes_from_different_messages():
    spans = [
        {
            "quote": '[tool_call send_email {"subject": "Heat plan", "body": "Increase ventilation", "to": "ops@example.com"}]',
            "message_id": "msg_A",
        },
        {
            "quote": '[tool_call log_treatment {"issue": "red mites", "route": "oral", "house_id": "H1"}]',
            "message_id": "msg_B",
        },
    ]
    notes: list[dict] = []
    out = sanitize_dimension_sample(_sample(_entry(5.0, spans)), DIMS, INDEX, notes, 0)
    entry = aggregate_multi_span(out["assistant_persona_bleed"], MULTI)

    assert entry["spans"] == spans
    assert entry["span_count"] == 2
    assert notes == []


def test_sanitize_keeps_non_overlapping_quotes_in_same_message():
    spans = [
        {"quote": "Please open another", "message_id": "msg_5"},
        {"quote": "tomorrow before noon", "message_id": "msg_5"},
    ]
    notes: list[dict] = []
    out = sanitize_dimension_sample(_sample(_entry(5.0, spans)), DIMS, INDEX, notes, 0)
    entry = aggregate_multi_span(out["assistant_persona_bleed"], MULTI)

    assert entry["spans"] == spans
    assert entry["span_count"] == 2
    assert notes == []


def test_sanitize_keeps_same_quote_when_it_resolves_to_different_messages():
    spans = [
        {"quote": "open another operating session", "message_id": "msg_1"},
        {"quote": "open another operating session", "message_id": "msg_4"},
    ]
    notes: list[dict] = []
    out = sanitize_dimension_sample(_sample(_entry(5.0, spans)), DIMS, INDEX, notes, 0)
    entry = aggregate_multi_span(out["assistant_persona_bleed"], MULTI)

    assert entry["spans"] == spans
    assert entry["span_count"] == 2
    assert notes == []


def test_sanitize_discards_positive_score_with_all_spans_invalid():
    spans = [{"quote": "completely fabricated span that matches nothing anywhere", "message_id": "msg_1"}]
    notes: list[dict] = []
    out = sanitize_dimension_sample(_sample(_entry(5.0, spans)), DIMS, INDEX, notes, 0)
    assert out["assistant_persona_bleed"] is None
    assert any("every cited span failed" in n["reason"] for n in notes if not n.get("span"))


def test_sanitize_discards_positive_score_when_score_setting_span_is_invalid():
    spans = [
        {"quote": "fabricated strongest span that matches nothing anywhere", "message_id": "msg_1"},
        {"quote": "open another operating session", "message_id": "msg_1"},
    ]
    notes: list[dict] = []
    out = sanitize_dimension_sample(_sample(_entry(10.0, spans)), DIMS, INDEX, notes, 0)

    assert out["assistant_persona_bleed"] is None
    assert any("score-setting span failed validation" in n["reason"] for n in notes if not n.get("span"))


def test_sanitize_keeps_positive_score_when_score_setting_span_is_valid():
    spans = [
        {"quote": "open another operating session", "message_id": "msg_1"},
        {"quote": "fabricated weaker span that matches nothing anywhere", "message_id": "msg_2"},
    ]
    notes: list[dict] = []
    out = sanitize_dimension_sample(_sample(_entry(5.0, spans)), DIMS, INDEX, notes, 0)

    assert out["assistant_persona_bleed"]["spans"] == [spans[0]]
    assert len([n for n in notes if n.get("span")]) == 1


def test_sanitize_discards_positive_score_when_first_raw_span_is_blank():
    parsed = _parsed_multi({
        "score": 5.0,
        "spans": [
            {"quote": "", "message_id": "msg_2"},
            {"quote": "open another operating session", "message_id": "msg_1"},
        ],
    })
    notes: list[dict] = []

    out = sanitize_dimension_sample(parsed, DIMS, INDEX, notes, 0)

    assert out["assistant_persona_bleed"] is None
    assert any("score-setting raw span was malformed" in note["reason"] for note in notes)


def test_sanitize_discards_positive_score_when_all_raw_spans_are_malformed():
    parsed = _parsed_multi({
        "score": 5.0,
        "spans": [None, {"quote": "   ", "message_id": "msg_1"}],
        "quote": "open another operating session",
        "message_id": "msg_1",
    })
    notes: list[dict] = []

    out = sanitize_dimension_sample(parsed, DIMS, INDEX, notes, 0)

    assert out["assistant_persona_bleed"] is None
    assert any("no raw cited span survived parsing" in note["reason"] for note in notes)


def test_sanitize_keeps_positive_score_when_raw_spans_key_is_absent():
    parsed = _parsed_multi({"score": 5.0})
    notes: list[dict] = []

    out = sanitize_dimension_sample(parsed, DIMS, INDEX, notes, 0)

    assert out["assistant_persona_bleed"] is not None
    assert out["assistant_persona_bleed"]["score"] == 5.0
    assert notes == []


def test_sanitize_keeps_positive_score_when_raw_spans_list_is_empty():
    parsed = _parsed_multi({"score": 5.0, "spans": []})
    notes: list[dict] = []

    out = sanitize_dimension_sample(parsed, DIMS, INDEX, notes, 0)

    assert out["assistant_persona_bleed"] is not None
    assert out["assistant_persona_bleed"]["score"] == 5.0
    assert notes == []


def test_sanitize_valid_first_raw_span_behavior_is_unchanged():
    parsed = _parsed_multi({
        "score": 5.0,
        "spans": [{"quote": "open another operating session", "message_id": "msg_1"}],
    })
    notes: list[dict] = []

    out = sanitize_dimension_sample(parsed, DIMS, INDEX, notes, 0)

    assert out["assistant_persona_bleed"]["spans"] == [
        {"quote": "open another operating session", "message_id": "msg_1"}
    ]
    assert notes == []


def test_sanitize_keeps_zero_score_with_no_spans():
    notes: list[dict] = []
    out = sanitize_dimension_sample(_sample(_entry(0.0, [])), DIMS, INDEX, notes, 0)
    assert out["assistant_persona_bleed"]["spans"] == []
    assert notes == []


def test_aggregate_formula_and_clamp():
    one = aggregate_multi_span(_entry(5.0, [{"quote": "q", "message_id": "msg_1"}]), MULTI)
    assert one["base_score"] == 5.0 and one["span_count"] == 1
    assert math.isclose(one["score"], 5.0 + SPAN_WEIGHT_K * math.log(2))
    ten = aggregate_multi_span(
        _entry(5.0, [{"quote": f"q{i}", "message_id": f"msg_{i}"} for i in range(10)]), MULTI
    )
    # calibration: ten distinct spans lift a base-5 exactly to 7
    assert math.isclose(ten["score"], 7.0)
    assert aggregate_multi_span(_entry(0.0, []), MULTI)["score"] == 0.0
    many = aggregate_multi_span(
        _entry(9.0, [{"quote": f"q{i}", "message_id": f"msg_{i}"} for i in range(20)]), MULTI
    )
    assert many["score"] == 10.0  # clamped to the scale
    assert aggregate_multi_span(None, MULTI) is None


def test_average_samples_uses_median_for_multi_span():
    samples = [
        _sample(_entry(3.0, [])), _sample(_entry(7.0, [])), _sample(_entry(5.0, [])),
    ]
    avg = average_samples(samples, DIMS)
    assert avg["assistant_persona_bleed"] == 5.0  # median, not mean
    assert avg["realism"] == 8.0


def test_axis_span_counts_median():
    def with_count(n):
        e = _entry(5.0, [{"quote": f"q{i}", "message_id": f"msg_{i}"} for i in range(n)])
        e["span_count"] = n
        return _sample(e)

    counts = axis_span_counts([with_count(2), with_count(8), with_count(9)], DIMS)
    assert counts == {"assistant_persona_bleed": 8.0}


def test_cue_localization_rows_carry_axis_and_span_count():
    e = _entry(5.0, [{"quote": "q", "message_id": "msg_1"}])
    e["span_count"] = 1
    rows = collect_cue_localization([_sample(e)], DIMS)
    row = [r for r in rows if r["dimension"] == "assistant_persona_bleed"][0]
    assert row["axis"] == "assistant_persona_bleed"
    assert row["span_count"] == 1


def test_sanitize_discards_positive_score_with_non_list_spans():
    # final-review minor: {"score": 10, "spans": "oops"} is a MALFORMED offer, not omitted
    # evidence — it must not keep an unvalidated positive base score.
    notes: list[dict] = []
    entry = _entry(10.0, [])
    entry["spans"] = []
    entry["_spans_offered_raw"] = True
    entry["_first_raw_span_malformed"] = True
    out = sanitize_dimension_sample(_sample(entry), DIMS, INDEX, notes, 0)
    assert out["assistant_persona_bleed"] is None


def test_parse_flags_non_list_spans_as_malformed_offer():
    from farm_eval.judge.scorer import parse_grader_response
    text = (
        '{"assistant_persona_bleed": {"score": 10, "spans": "oops"},'
        ' "realism": {"score": 8, "quote": "q", "message_id": "msg_1"}}'
    )
    entry = parse_grader_response(text, [MULTI, SINGLE])["assistant_persona_bleed"]
    assert entry["_spans_offered_raw"] is True
    assert entry["_first_raw_span_malformed"] is True
