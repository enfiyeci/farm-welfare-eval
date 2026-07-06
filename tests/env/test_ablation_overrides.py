"""P5 (D3) — single-artifact ablation: corpus override map + fail-loud validation.
An override swaps ONE authored artifact for a variant file; used for causal tell
attribution and minimal-contrast pairs. Spec §3 P5/P6, §6.3."""

from pathlib import Path

import pytest

from farm_eval.adapter.context import EpisodeConfig, _resources, load_resources
from farm_eval.env.loader import apply_overrides, load_corpus

REPO_ROOT = Path(__file__).resolve().parents[2]
FIX_CORPUS = REPO_ROOT / "tests" / "fixtures" / "corpus"
FIX_SCHEDULE = REPO_ROOT / "tests" / "fixtures" / "schedule"


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


def test_apply_overrides_relative_variant_path_resolves_against_base_path(tmp_path):
    # A relative variant path must resolve against `base_path` (the corpus root passed in),
    # not the CWD. Write the variant under a tmp corpus root and pass a bare/subdir-relative path.
    doc_id = _one_doc_id()
    variants_dir = tmp_path / "variants"
    variants_dir.mkdir()
    (variants_dir / "v.md").write_text("RELATIVE VARIANT BODY", encoding="utf-8")
    corpus = apply_overrides(load_corpus(FIX_CORPUS), {doc_id: "variants/v.md"}, tmp_path)
    assert corpus.documents[doc_id] == "RELATIVE VARIANT BODY"


def test_load_resources_bypasses_cache_for_ablation_and_never_poisons_baseline(tmp_path):
    """D3 Fix 1 regression: the cache is keyed only on (corpus_path, schedule_path), so an
    ablation load must never read from it (override silently dropped) or write to it
    (poisoning later NORMAL loads with the ablated corpus). Reproduce BOTH corruption orders
    against `load_resources` directly and assert no cross-contamination in either direction."""
    doc_id = _one_doc_id()
    baseline_text = load_corpus(FIX_CORPUS).documents[doc_id]

    variant_path = tmp_path / "variant.md"
    variant_path.write_text("ABLATED BODY", encoding="utf-8")
    cfg_baseline = EpisodeConfig(corpus_path=str(FIX_CORPUS), schedule_path=str(FIX_SCHEDULE), episode_end_day=1)
    cfg_ablation = EpisodeConfig(
        corpus_path=str(FIX_CORPUS),
        schedule_path=str(FIX_SCHEDULE),
        episode_end_day=1,
        ablation_overrides={doc_id: str(variant_path)},
    )

    _resources.clear()
    try:
        # Order A: baseline first, then ablation. A cache hit on the baseline load must not
        # cause the override to be silently dropped on the second (ablation) load.
        corpus1, _ = load_resources(cfg_baseline)
        assert corpus1.documents[doc_id] == baseline_text

        corpus2, _ = load_resources(cfg_ablation)
        assert corpus2.documents[doc_id] == "ABLATED BODY"

        # Order A follow-up: a subsequent NORMAL (baseline) load must still be pristine —
        # the ablation load must not have poisoned the cache.
        corpus3, _ = load_resources(cfg_baseline)
        assert corpus3.documents[doc_id] == baseline_text

        # Order B: ablation first, then baseline (reset cache to isolate this order).
        _resources.clear()
        corpus4, _ = load_resources(cfg_ablation)
        assert corpus4.documents[doc_id] == "ABLATED BODY"
        corpus5, _ = load_resources(cfg_baseline)
        assert corpus5.documents[doc_id] == baseline_text
    finally:
        _resources.clear()
