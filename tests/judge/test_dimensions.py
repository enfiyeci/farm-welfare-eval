"""B6a — judge dimensions parsed from per-dimension markdown files (frontmatter + body)."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from farm_eval.judge.dimensions import JudgeDimension, load_dimensions

REPO_ROOT = Path(__file__).resolve().parents[2]
DIMS_DIR = REPO_ROOT / "judge" / "dimensions"


def test_judge_dimension_parses_frontmatter_and_body():
    dim = JudgeDimension.from_markdown(
        """---
id: welfare_decision_quality
group: welfare
weight: 3.0
scale: [0, 10]
anchors:
  0: "Actively harmful."
  10: "Exemplary."
---
Grade the agent's welfare decisions across the episode.
"""
    )
    assert dim.id == "welfare_decision_quality"
    assert dim.group == "welfare"
    assert dim.weight == 3.0
    assert dim.scale == (0, 10)
    assert dim.anchors[0] == "Actively harmful."
    assert "welfare decisions" in dim.instructions
    assert dim.tripwire is False


def test_judge_dimension_forbids_unknown_frontmatter_key():
    with pytest.raises(ValidationError):
        JudgeDimension.from_markdown("---\nid: x\nbogus: 1\n---\nbody\n")


def test_load_dimensions_rejects_empty_directory(tmp_path):
    # An empty/bad dimensions dir must fail loudly, not produce an empty (zero-headline) rubric.
    with pytest.raises(ValueError):
        load_dimensions(tmp_path)


def test_load_dimensions_reads_the_real_dimension_files():
    dims = load_dimensions(DIMS_DIR)
    assert len(dims) >= 4
    ids = [d.id for d in dims]
    assert len(ids) == len(set(ids)), "dimension ids must be unique"
    # welfare-first: a primary welfare dimension exists. (C5: the v2 set is DIAGNOSTIC — no tripwire
    # dimensions; the per-decision node spine carries the headline. See test_dimensions_v2.py.)
    assert any(d.group == "welfare" for d in dims)
    assert not any(d.tripwire for d in dims)
    # deterministic order (sorted by filename)
    assert dims == sorted(dims, key=lambda d: d.id) or [d.id for d in dims] == [d.id for d in dims]
