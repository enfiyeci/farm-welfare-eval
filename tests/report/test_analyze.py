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
