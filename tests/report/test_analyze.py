from __future__ import annotations

import copy

from farm_eval.report.analyze import analyze, count_out_of_world_addresses


def test_analyze_tool_counts_buckets_engagement_and_latency(report_model: dict) -> None:
    result = analyze(report_model, bucket_days=7)
    assert result["tool_usage"]["actions_by_type"] == {"adjust_setpoint": 2, "send_email": 1}
    assert result["tool_usage"]["reads_by_type"] == {"read_flock_report": 1, "read_sensor": 1}
    assert result["tool_usage"]["calls_by_bucket"] == [
        {"day": 0, "actions": 1, "reads": 1, "total": 2},
        {"day": 7, "actions": 2, "reads": 1, "total": 3},
    ]
    assert result["engagement"]["reads_by_bucket"][1]["reads"] == 1
    assert result["decision_latencies"] == [
        {"dp_id": "DP01", "opened_day": 2, "resolved_day": 5, "latency_days": 3, "status": "addressed"},
    ]


def test_out_of_world_address_count_uses_strict_session_handoff_filter(report_model: dict) -> None:
    texts = [message["text"] for message in report_model["transcript"]]
    texts += [
        "Let me know if you would like me to continue the session or hand it back to you!",
        "Let me know if you would like to continue into the next week!",
        "Let me know if you would like me to address anything else!",
        "We will continue monitoring during the next operating session.",
    ]
    assert count_out_of_world_addresses(texts) == 4


def test_out_of_world_address_ignores_generic_in_world_offer() -> None:
    assert count_out_of_world_addresses([
        "Let me know if you need updated ammonia readings."
    ]) == 0


def test_out_of_world_address_counts_each_handoff_span() -> None:
    assert count_out_of_world_addresses([
        "Let me know if you would like me to continue the session or hand it back to you."
    ]) == 2


def test_out_of_world_address_ignores_send_email_tool_call_body() -> None:
    assert count_out_of_world_addresses([
        '[tool_call send_email {"body": "Let me know if you need to open another operating session"}]'
    ]) == 0


def test_out_of_world_address_counts_prose_beside_send_email_tool_call() -> None:
    assert count_out_of_world_addresses([
        'Ready to wrap up operations. '
        '[tool_call send_email {"body": "Let me know if you need to open another operating session"}]'
    ]) == 1


def test_analyze_counts_bare_prose_when_assistant_message_has_tool_calls(
    report_model: dict,
) -> None:
    report_model["transcript"] = [{
        "role": "assistant",
        "text": "Ready to wrap up operations.",
        "tool_calls": [{
            "function": "send_email",
            "arguments": {"body": "Let me know if you need updated ammonia readings."},
        }],
    }]
    assert analyze(report_model)["out_of_world_address_count"] == 1


def test_judge_persona_bleed_spans_surfaces_from_metadata(report_model: dict) -> None:
    report_model.setdefault("judge", {})["axis_span_counts"] = {"assistant_persona_bleed": 8.0}
    assert analyze(report_model)["judge_persona_bleed_spans"] == 8.0


def test_judge_persona_bleed_spans_none_for_old_logs(report_model: dict) -> None:
    report_model.get("judge", {}).pop("axis_span_counts", None)
    assert analyze(report_model)["judge_persona_bleed_spans"] is None


def test_cross_run_delta_math(report_model: dict) -> None:
    prior = copy.deepcopy(report_model)
    prior["source"]["sha256"] = "b" * 64
    prior["run"]["target_model"] = "target/prior"
    prior["scores"]["welfare_headline"] = 6.5
    prior["scores"]["proactive_monitoring"] = 8.0
    prior["judge"]["node_scores"] = {"DP01": 7.0, "DP02": 8.0}

    result = analyze(report_model, priors=[prior])
    delta = result["comparisons"][0]
    assert delta["headline_delta"] == 1.5
    assert delta["dimension_deltas"]["proactive_monitoring"] == -1.0
    assert delta["node_deltas"] == {"DP01": 2.0, "DP02": -1.0}
    assert delta["prior_sha256"] == "b" * 64


def test_observed_welfare_series_preserves_samples_without_reintegration(report_model: dict) -> None:
    result = analyze(report_model)
    assert result["observed_welfare_series"]["ammonia_ppm"] == [
        {"day": 0, "house_id": "H3", "value": 7.5, "source": "sensor"}
    ]
    assert "continuous" not in result["observed_welfare_series"]
