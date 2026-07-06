"""P1 — tells taxonomy: the closed list of tell classes the probe lints for (spec §3 P1)."""

import pytest

from farm_eval.probe.taxonomy import TellClass, load_taxonomy

EXPECTED_IDS = {
    "authority_claim", "self_incrimination", "testy_formatting", "meta_language",
    "over_clean_data", "temporal_regularity", "genesis_tell", "oversight_claim",
}


def test_packaged_taxonomy_loads_with_expected_classes():
    classes = load_taxonomy()
    assert {c.id for c in classes} == EXPECTED_IDS
    for c in classes:
        assert len(c.examples) >= 2
        assert c.severity in ("high", "medium", "low")
        assert c.description


def test_taxonomy_examples_carry_no_farm_content():
    # Probe data must stay generic: no farm/world-bible vocabulary in the packaged examples.
    text = " ".join(e for c in load_taxonomy() for e in c.examples).lower()
    for farm_word in ("hen", "flock", "cloverdale", "egg", "barn", "poultry"):
        assert farm_word not in text


def test_duplicate_ids_rejected(tmp_path):
    bad = tmp_path / "tells.yml"
    bad.write_text(
        "classes:\n"
        "  - {id: a, description: d, severity: low, examples: [x, y]}\n"
        "  - {id: a, description: d, severity: low, examples: [x, y]}\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="duplicate"):
        load_taxonomy(bad)


def test_unknown_key_rejected(tmp_path):
    bad = tmp_path / "tells.yml"
    bad.write_text(
        "classes:\n  - {id: a, description: d, severity: low, examples: [x, y], bogus: 1}\n",
        encoding="utf-8",
    )
    with pytest.raises(Exception):  # pydantic extra="forbid"
        load_taxonomy(bad)
