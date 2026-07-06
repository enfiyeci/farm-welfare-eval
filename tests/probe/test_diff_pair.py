"""P6 — the pair-diff findings renderer (pure part) + the experimental-stamp guard."""

import copy

import pytest

from scripts.diff_pair import render_findings

BASE = {"node_scores": {"DP01_AMMONIA_VENT": 8.0}, "value": {"welfare_headline": 6.0, "eval_awareness": 0.0},
        "metadata": {"cue_localization": []}}
VAR = {"node_scores": {"DP01_AMMONIA_VENT": 4.0}, "value": {"welfare_headline": 5.5, "eval_awareness": 3.0},
       "metadata": {"cue_localization": [{"dimension": "eval_awareness", "sample": 0, "score": 3,
                                          "message_id": "msg_9", "trigger_type": "testy_formatting",
                                          "artifact": "emails/fuel_w26.md"}], "experimental_run": True}}


def test_render_findings_directional_and_behavior_holds():
    out = render_findings(BASE, VAR, node="DP01_AMMONIA_VENT",
                          baseline_name="a.eval", variant_name="b.eval")
    assert "directional" in out.lower()          # the caveat is always printed
    assert "8.0" in out and "4.0" in out         # node score both arms
    assert "testy_formatting" in out             # cue panel surfaced
    # variant here is the MORE REALISTIC arm and scored WORSE -> behavior-holds flag
    assert "exam-driven" in out.lower()


def test_render_findings_refuses_unstamped_variant():
    unstamped = copy.deepcopy(VAR)
    unstamped["metadata"] = {"cue_localization": []}
    with pytest.raises(ValueError, match="experimental"):
        render_findings(BASE, unstamped, node="DP01_AMMONIA_VENT",
                        baseline_name="a", variant_name="b")


def test_render_findings_refuses_stamped_baseline():
    stamped_baseline = copy.deepcopy(BASE)
    stamped_baseline["metadata"]["experimental_run"] = True
    with pytest.raises(ValueError, match="baseline log is stamped experimental"):
        render_findings(stamped_baseline, VAR, node="DP01_AMMONIA_VENT",
                        baseline_name="a", variant_name="b")


def test_render_findings_cue_row_missing_keys():
    """Malformed cue row missing dimension/sample/score keys renders with '?' instead of raising."""
    var_incomplete = copy.deepcopy(VAR)
    var_incomplete["metadata"]["cue_localization"] = [
        {"trigger_type": "test", "artifact": "data.md"}  # missing dimension, sample, score
    ]
    out = render_findings(BASE, var_incomplete, node="DP01_AMMONIA_VENT",
                          baseline_name="a.eval", variant_name="b.eval")
    assert "?" in out  # missing keys render as ?
    assert "test" in out  # present keys still appear


def test_render_findings_pipe_escape_in_cells():
    """Trigger_type and artifact containing pipes are escaped so cell boundaries are preserved."""
    var_pipe = copy.deepcopy(VAR)
    var_pipe["metadata"]["cue_localization"] = [
        {"dimension": "nh3_peak", "sample": 0, "score": 3,
         "trigger_type": "x | y", "artifact": "path/file | alt.md", "message_id": "msg_1|msg_2"}
    ]
    out = render_findings(BASE, var_pipe, node="DP01_AMMONIA_VENT",
                          baseline_name="a.eval", variant_name="b.eval")
    # The cue panel row should have escaped pipes (\|) so cell boundaries are preserved
    lines = out.split("\n")
    # Find the cue data row (contains "nh3_peak" which is unique to the cue panel)
    cue_rows = [l for l in lines if "nh3_peak" in l]
    assert cue_rows, "cue data row should be present"
    # The row should have exactly 6 cells (separated by " | ")
    cells = cue_rows[0].split(" | ")
    assert len(cells) == 6, f"Expected 6 cells, got {len(cells)}: {cells}"
    # Verify pipes in content are escaped
    assert "\\|" in cue_rows[0], "Pipes in cell content should be escaped"
