from __future__ import annotations

from html.parser import HTMLParser

from farm_eval.analysis.model import (
    BehaviourEvent,
    BehaviourModel,
    DossierDerived,
    NodeDossier,
    OffNodeFinding,
    ToolProfile,
)
from farm_eval.analysis.pertool import TOOL_ROSTER
from farm_eval.report.analyze import analyze
from farm_eval.report.render import parse_narrative, render


class _Parser(HTMLParser):
    pass


_BEHAVIOUR_SECTION_IDS = ("offnode-findings", "pertool-behaviour")


def _behaviour_model() -> BehaviourModel:
    """A behaviour model for the `report_model` fixture's run (nodes DP01/DP02)."""
    return BehaviourModel(
        source_sha256="a" * 64,
        target_model="target/current",
        feed_fidelity="full",
        day_map_valid=True,
        thresholds={"repetition_k": 10.0},
        dossiers=[
            NodeDossier(
                dp_id="DP01", category="welfare_cost", opened_day=2, deadline_day=10,
                status="addressed", latency_days=3, node_score=9.0,
                strong=[
                    BehaviourEvent(
                        kind="action", day_lo=5, day_hi=5, msg_id="msg_2",
                        tool="adjust_setpoint", params={},
                        summary="adjust_setpoint(house_id=PLACEHOLDER_HOUSE)",
                    )
                ],
                derived=DossierDerived(
                    strong_action_count=1, read_before_first_action=True,
                    longest_idle_gap_days=5,
                ),
            )
        ],
        tool_profiles=[ToolProfile(tool=tool, total_calls=0) for tool in TOOL_ROSTER],
        offnode_findings=[
            OffNodeFinding(
                detector="unattributed_action", severity=7.0, day_lo=8, day_hi=8,
                msg_ids=["msg_1"], tool="schedule_maintenance", count=1,
                note="PLANTED_OFFNODE_NOTE for the render test",
            )
        ],
        digest=[],
    )


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
    assert "Judge-validated persona-bleed spans (median/sample): <strong>8</strong>" in html


def test_render_shows_fractional_judge_span_covariate(report_model: dict) -> None:
    report_model.setdefault("judge", {})["axis_span_counts"] = {"assistant_persona_bleed": 8.5}
    html = render(report_model, analyze(report_model), narrative=None, history=[])
    assert "Judge-validated persona-bleed spans (median/sample): <strong>8.5</strong>" in html


def test_render_without_behaviour_is_byte_identical_and_adds_no_sections(report_model: dict) -> None:
    analysis = analyze(report_model)
    default = render(report_model, analysis, narrative=None, history=[])
    explicit_none = render(report_model, analysis, narrative=None, history=[], behaviour=None)
    assert default == explicit_none
    for section_id in _BEHAVIOUR_SECTION_IDS:
        assert f'id="{section_id}"' not in default
    assert "data-behaviour-node" not in default


def test_render_with_behaviour_adds_the_offnode_and_per_tool_sections(report_model: dict) -> None:
    html = render(
        report_model, analyze(report_model), narrative=None, history=[],
        behaviour=_behaviour_model(),
    )
    _Parser().feed(html)
    for section_id in _BEHAVIOUR_SECTION_IDS:
        assert f'id="{section_id}"' in html
    assert "PLANTED_OFFNODE_NOTE for the render test" in html
    assert "https://" not in html and "http://" not in html


def test_render_with_behaviour_augments_the_matching_node_card(report_model: dict) -> None:
    html = render(
        report_model, analyze(report_model), narrative=None, history=[],
        behaviour=_behaviour_model(),
    )
    assert 'data-behaviour-node="DP01"' in html
    assert "adjust_setpoint(house_id=PLACEHOLDER_HOUSE)" in html
    # DP02 has a card but no dossier: its card must stay intact rather than gain an empty block
    assert 'data-behaviour-node="DP02"' not in html


def test_render_with_behaviour_keeps_the_sidecar_oddities_section_above_the_auto_section(
    report_model: dict,
) -> None:
    html = render(
        report_model, analyze(report_model), narrative="## odd_behaviors\nOne session handoff.",
        history=[], behaviour=_behaviour_model(),
    )
    assert "One session handoff." in html
    assert html.index('id="odd-behaviors"') < html.index('id="offnode-findings"')
