from farm_eval.study.cells import Cell, Economics, Scale, Species, StandardBand
from farm_eval.study.documents import find_welfare_vocabulary, render_all
from farm_eval.study.offer import build_offer
from farm_eval.study.params import rungs_for
from farm_eval.study.prompt import DECISION_MARKER, build_p1_prompt


def _offer():
    cell = Cell(species=Species.HEN, scale=Scale.SMALL,
                standard=StandardBand.WITHIN, economics=Economics.EQUALIZED)
    return build_offer(cell, rungs_for(Species.HEN, StandardBand.WITHIN)[0], 0.08)


def test_prompt_embeds_all_three_documents_inline():
    """Spec §5 — matching P1's information delivery to P2's keeps the gap
    interpretable. Whole documents, not first lines: a template that silently
    truncated a document after line 1 must fail here."""
    prompt = build_p1_prompt(_offer())
    for text in render_all(_offer()).values():
        assert text in prompt


def test_prompt_requests_a_parseable_decision():
    assert DECISION_MARKER in build_p1_prompt(_offer())
    assert "ACCEPT" in build_p1_prompt(_offer())
    assert "DECLINE" in build_p1_prompt(_offer())


def test_prompt_contains_no_welfare_vocabulary():
    """Spec §16.8 applies to the prompt too, not only the documents. Uses the
    real guard, not a hand-rolled check that could drift from it."""
    assert find_welfare_vocabulary(build_p1_prompt(_offer())) == []


def test_prompt_does_not_mention_evaluation_or_testing():
    lowered = build_p1_prompt(_offer()).lower()
    for tell in ("evaluat", "we are testing", "this is a test", "scenario", "researcher"):
        assert tell not in lowered
