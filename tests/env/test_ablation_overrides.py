"""P5 (D3) — single-artifact ablation: corpus override map + fail-loud validation.
An override swaps ONE authored artifact for a variant file; used for causal tell
attribution and minimal-contrast pairs. Spec §3 P5/P6, §6.3."""

from pathlib import Path

import pytest

from farm_eval.env.loader import apply_overrides, load_corpus

REPO_ROOT = Path(__file__).resolve().parents[2]
FIX_CORPUS = REPO_ROOT / "tests" / "fixtures" / "corpus"


def _one_doc_id() -> str:
    corpus = load_corpus(FIX_CORPUS)
    assert corpus.documents, "fixture corpus needs at least one document"
    return sorted(corpus.documents)[0]


def test_apply_overrides_swaps_document_text(tmp_path):
    doc_id = _one_doc_id()
    variant = tmp_path / "variant.md"
    variant.write_text("VARIANT BODY", encoding="utf-8")
    corpus = apply_overrides(load_corpus(FIX_CORPUS), {doc_id: str(variant)}, tmp_path)
    assert corpus.documents[doc_id] == "VARIANT BODY"


def test_apply_overrides_unknown_artifact_raises(tmp_path):
    variant = tmp_path / "v.md"
    variant.write_text("x", encoding="utf-8")
    with pytest.raises(ValueError, match="unknown artifact"):
        apply_overrides(load_corpus(FIX_CORPUS), {"emails/ghost.md": str(variant)}, tmp_path)


def test_apply_overrides_missing_variant_raises(tmp_path):
    with pytest.raises(ValueError, match="variant"):
        apply_overrides(load_corpus(FIX_CORPUS), {_one_doc_id(): str(tmp_path / "nope.md")}, tmp_path)
