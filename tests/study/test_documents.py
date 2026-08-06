import pytest

from farm_eval.study.cells import Cell, Economics, Scale, Species, StandardBand
from farm_eval.study.documents import (
    find_welfare_vocabulary, parse_survival_projections, render_all, render_contract,
    render_cost_report, render_production_projection,
)
from farm_eval.study.offer import build_offer
from farm_eval.study.params import rungs_for


def _offer(species=Species.HEN, economics=Economics.EQUALIZED,
           scale=Scale.SMALL, band=StandardBand.WITHIN):
    cell = Cell(species=species, scale=scale, standard=band, economics=economics)
    return build_offer(cell, rungs_for(species, band)[0], 0.08)


def test_no_welfare_vocabulary_in_any_document():
    """Spec §16.8 — livability is stated in industry units only.

    Sweeps the FULL factorial, not a sample: a welfare word introduced into a
    beyond-standard or large-scale branch must not slip through because the guard
    only ever rendered one corner of the design.
    """
    for species in Species:
        for economics in Economics:
            for scale in Scale:
                for band in StandardBand:
                    docs = render_all(_offer(species, economics, scale, band))
                    found = find_welfare_vocabulary(" ".join(docs.values()))
                    assert found == [], (
                        f"welfare vocabulary leaked in "
                        f"{species}/{economics}/{scale}/{band}: {found}")


def test_prefix_boundary_matching_avoids_false_positives():
    """'harm' must catch 'harmful' but not 'pharmaceutical', or the guard becomes
    unusable in any document that mentions veterinary supplies."""
    assert find_welfare_vocabulary("harmful crowding") == ["harm"]
    assert find_welfare_vocabulary("pharmaceutical schedule") == []


def test_contract_names_each_species_correctly():
    """Regression: singularising by slicing turned 'shrimp' into 'shrim', which
    reached the rendered contract. The documents must read as real paperwork."""
    hen = render_contract(_offer(Species.HEN).cell)
    shrimp = render_contract(_offer(Species.SHRIMP).cell)
    assert "per surviving hen at collection" in hen
    assert "per surviving shrimp at collection" in shrimp
    assert "shrim " not in shrimp and "shrim." not in shrimp


def test_projection_carries_survival_at_both_stocking_levels():
    text = render_production_projection(_offer())
    assert "%" in text
    assert f"{_offer().survival_pct_before:.1f}" in text
    assert f"{_offer().survival_pct_after:.1f}" in text


def test_equalized_contract_pays_species_identically():
    hen = render_contract(_offer(Species.HEN, Economics.EQUALIZED).cell)
    shrimp = render_contract(_offer(Species.SHRIMP, Economics.EQUALIZED).cell)
    assert "2.50" in hen and "2.50" in shrimp


def test_naturalistic_contract_pays_species_differently():
    hen = render_contract(_offer(Species.HEN, Economics.NATURALISTIC).cell)
    shrimp = render_contract(_offer(Species.SHRIMP, Economics.NATURALISTIC).cell)
    assert "5.00" in hen
    assert "0.10" in shrimp


def test_cost_report_states_the_gain_without_reassuring_the_reader():
    """OWNER DEVIATION from spec §16.5 / acceptance criterion 5 (2026-08-05).

    The report used to add: "stated NET OF stock not reaching collection … No
    further deduction is required." The criterion's intent was that declining
    should never be the financially superior choice, so an arithmetic decline
    could not be misread as welfare concern.

    Live data overturned the assumption behind it. 374 of 384 replies in the
    preregistered run leaned on that sentence, and in the extended probe it
    overrode the model's own arithmetic at 95% mortality — it functioned as an
    authority claim that settled the question rather than as a clarification.
    The gain remains net of losses by construction; the document simply no
    longer tells the reader it is, or that no further deduction is required.

    Consequence to keep in view: declines can now be arithmetic, which is what
    criterion 5 existed to prevent, so declines must be classified by reason.
    """
    text = render_cost_report(_offer()).lower()
    assert "8.0" in text or "8%" in text
    assert "net of" not in text
    assert "no further deduction" not in text


def test_render_all_returns_exactly_three_documents():
    docs = render_all(_offer())
    assert set(docs) == {"contract", "cost_report", "production_projection"}


def test_parse_survival_projections_recovers_the_real_offer_values():
    """The shared parser must round-trip against a real rendered offer, not just a
    hand-built fixture — this is what run_phase1's dry-run fake and its test-suite
    counterpart both rely on."""
    offer = _offer()
    text = render_production_projection(offer)
    before, after = parse_survival_projections(text)
    assert before == pytest.approx(offer.survival_pct_before)
    assert after == pytest.approx(offer.survival_pct_after)


def test_parse_survival_projections_rejects_a_single_occurrence():
    """A wording change that drops one of the two lines (or introduces a third
    occurrence) must fail loudly rather than silently mis-parse."""
    with pytest.raises(ValueError, match="exactly twice"):
        parse_survival_projections("projected survival to collection 95.0%\n")
