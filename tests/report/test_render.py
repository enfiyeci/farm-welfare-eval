from __future__ import annotations

from html.parser import HTMLParser

from farm_eval.report.analyze import analyze
from farm_eval.report.render import parse_narrative, render


class _Parser(HTMLParser):
    pass


def test_parse_narrative_sections_by_exact_heading() -> None:
    sections = parse_narrative("# Pilot\n\n## executive_summary\nGood run.\n\n## node_verdicts\nDP01: harness valid\n")
    assert sections == {"executive_summary": "Good run.", "node_verdicts": "DP01: harness valid"}


def test_render_is_self_contained_has_all_sections_and_missing_placeholders(report_model: dict) -> None:
    html = render(report_model, analyze(report_model), narrative=None, history=[])
    _Parser().feed(html)
    assert html.lstrip().lower().startswith("<!doctype html>")
    assert "✍️ write me" in html
    assert "https://" not in html and "http://" not in html
    assert "<style>" in html and "<script>" in html and "<svg" in html
    assert "prefers-color-scheme: dark" in html
    for section_id in [
        "executive-verdict", "how-to-read", "cross-run", "behavioral-portrait",
        "odd-behaviors", "tool-analytics", "welfare-state", "per-node",
        "judge-qa", "all-rounds-trend", "dispositions", "reproducibility",
    ]:
        assert f'id="{section_id}"' in html
    assert "Approximate observations from tool results" in html
    assert "Judge sample variance" in html
    assert "continuous re-integrated" not in html.lower()


def test_render_with_sidecar_and_vs_comparison(report_model: dict) -> None:
    prior = {**report_model, "source": {**report_model["source"], "sha256": "b" * 64}}
    analysis = analyze(report_model, priors=[prior])
    narrative = """## executive_summary
Conclusions strengthened.
## behavioral_portrait
Steady operator.
## odd_behaviors
One session handoff.
## node_verdicts
DP01: valid signal
## dispositions
Fix report only.
"""
    html = render(report_model, analysis, narrative=narrative, history=[])
    assert "Conclusions strengthened." in html
    assert "Steady operator." in html
    assert "DP01: valid signal" in html
    assert "Cross-run delta" in html


def test_render_escapes_narrative_html(report_model: dict) -> None:
    html = render(report_model, analyze(report_model), narrative="## executive_summary\n<script>alert(1)</script>", history=[])
    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in html


def test_render_shows_judge_span_covariate(report_model: dict) -> None:
    report_model.setdefault("judge", {})["axis_span_counts"] = {"assistant_persona_bleed": 8.0}
    html = render(report_model, analyze(report_model), narrative=None, history=[])
    assert "Judge-validated persona-bleed spans" in html
