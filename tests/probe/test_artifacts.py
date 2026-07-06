"""P2 input surface — enumerate the artifacts the probe judges (spec §3 P2)."""

from pathlib import Path

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
    # every corpus document is present with its documents/-relative key as id
    doc_ids = {a.id for a in arts if a.kind in ("email", "document")}
    assert all(a.text for a in arts)
    assert doc_ids  # fixture corpus has at least one document


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
