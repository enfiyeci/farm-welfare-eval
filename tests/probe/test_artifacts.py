"""P2 input surface — enumerate the artifacts the probe judges (spec §3 P2)."""

import shutil

import pytest

from pathlib import Path

from farm_eval.env.loader import load_corpus
from farm_eval.probe.artifacts import Artifact, enumerate_corpus_artifacts, rendered_samples

REPO_ROOT = Path(__file__).resolve().parents[2]
FIX = REPO_ROOT / "tests" / "fixtures"
BRIEFING = REPO_ROOT / "prompts" / "operator_briefing.md"


def test_enumerates_fixture_corpus_plus_briefing():
    arts = enumerate_corpus_artifacts(FIX / "corpus", BRIEFING)
    ids = [a.id for a in arts]
    assert ids == sorted(ids[:-1]) + ["briefing"]  # sorted docs, briefing last
    assert ids[-1] == "briefing"
    briefing = arts[-1]
    assert briefing.kind == "briefing" and len(briefing.text) > 100
    # every corpus document is present with its documents/-relative key as id — exact round-trip
    doc_ids = {a.id for a in arts if a.kind in ("email", "document")}
    assert all(a.text for a in arts)
    assert doc_ids == set(load_corpus(FIX / "corpus").documents)


def test_email_kind_from_key_prefix():
    arts = enumerate_corpus_artifacts(FIX / "corpus", BRIEFING)
    for a in arts:
        if a.id.startswith("emails/"):
            assert a.kind == "email"


def test_rendered_samples_are_deterministic():
    a = rendered_samples(FIX / "corpus", FIX / "schedule", days=(3,), house_id="H_SENSOR")
    b = rendered_samples(FIX / "corpus", FIX / "schedule", days=(3,), house_id="H_SENSOR")
    assert [x.id for x in a] == [x.id for x in b]
    assert [x.text for x in a] == [x.text for x in b]
    assert all(x.kind == "rendered" for x in a)
    assert a  # produced at least one rendered artifact


def test_rendered_samples_label_ids_with_the_actual_day_reached():
    # Fixture schedule has beats at days 0 and 5. Requesting day 3 with a horizon of 3 has no
    # scheduled beat before the horizon, so next_beat clamps straight to the horizon: actual == 3.
    arts = rendered_samples(FIX / "corpus", FIX / "schedule", days=(3,), house_id="H_SENSOR")
    ids = [a.id for a in arts]
    assert ids == ["rendered/flock_report/H_SENSOR/day3", "rendered/cop_report/H_SENSOR/day3"]
    flock = arts[0]
    assert '"date": "2025-06-12"' in flock.text  # day 3 = 2025-06-09 + 3 days


def test_rendered_samples_never_loop_forever_past_the_horizon():
    # Requesting an unreachable day (999) against a small horizon (5) must stop at the horizon,
    # not loop forever, and label the artifact with the final reachable day.
    arts = rendered_samples(
        FIX / "corpus", FIX / "schedule", days=(999,), house_id="H_SENSOR", episode_end_day=5
    )
    ids = [a.id for a in arts]
    assert ids == ["rendered/flock_report/H_SENSOR/day5", "rendered/cop_report/H_SENSOR/day5"]


def test_enumerate_rejects_reserved_briefing_id(tmp_path):
    corpus_dir = tmp_path / "corpus"
    shutil.copytree(FIX / "corpus", corpus_dir)
    (corpus_dir / "documents" / "briefing").write_text("collides with the reserved briefing id", encoding="utf-8")
    with pytest.raises(ValueError, match="briefing"):
        enumerate_corpus_artifacts(corpus_dir, BRIEFING)


def test_references_dir_is_never_agent_visible():
    # Spec §6.1: corpus/references/ must never be served. load_corpus walks documents/ only.
    from farm_eval.env.loader import load_corpus

    corpus = load_corpus(REPO_ROOT / "corpus")
    assert not any(k.startswith("references") or "references/" in k for k in corpus.documents)


def test_variants_dir_is_never_agent_visible():
    from farm_eval.env.loader import load_corpus

    corpus = load_corpus(REPO_ROOT / "corpus")
    assert not any("variants/" in k or k.startswith("variants") for k in corpus.documents)
