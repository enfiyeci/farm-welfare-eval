"""P2 — self-relative RWR pair builder (the pure part). The CLI shell is a thin wrapper."""

import pytest

from scripts.probe_selfrel import build_selfrel_pair


def test_build_selfrel_pair_happy(tmp_path):
    variant = tmp_path / "fuel_w26_casual.md"
    variant.write_text("casual body", encoding="utf-8")
    documents = {"emails/fuel_w26.md": "baseline body", "company.md": "x"}

    baseline_art, variant_art = build_selfrel_pair(documents, "emails/fuel_w26.md", variant)

    assert baseline_art.id == "emails/fuel_w26.md"
    assert baseline_art.kind == "email"
    assert baseline_art.text == "baseline body"
    # variant id is anchored under the baseline's subdir (no cross-subdir collisions) and
    # mirrors the baseline's genre.
    assert variant_art.id == "variants/emails/fuel_w26_casual.md"
    assert variant_art.kind == "email"
    assert variant_art.text == "casual body"


def test_build_selfrel_pair_non_email_baseline_kind(tmp_path):
    variant = tmp_path / "company_alt.md"
    variant.write_text("alt", encoding="utf-8")
    baseline_art, variant_art = build_selfrel_pair({"company.md": "y"}, "company.md", variant)
    assert baseline_art.kind == "document"
    assert variant_art.kind == "document"  # variant mirrors the baseline genre
    assert variant_art.id == "variants/company_alt.md"  # no subdir on the baseline id


def test_build_selfrel_pair_missing_baseline_fails_loud(tmp_path):
    variant = tmp_path / "v.md"
    variant.write_text("v", encoding="utf-8")
    with pytest.raises(ValueError, match="unknown baseline id"):
        build_selfrel_pair({"emails/other.md": "z"}, "emails/fuel_w26.md", variant)
