from farm_eval.study.cells import framing_cells
from farm_eval.study.phase1 import run_phase1
from farm_eval.study.provider import FakeProvider
from farm_eval.study.sweep import SweepRules
from scripts.report_transcripts import render


def _results(reply: str):
    return run_phase1(FakeProvider(lambda p: reply), cells=framing_cells()[:1],
                      gains=(0.08,), rules=SweepRules(replicates=2))


def test_every_reply_appears_verbatim_and_uncut():
    reply = ("Line one of the reasoning.\nLine two, which must survive intact.\n"
             "DECISION: ACCEPT")
    out = render(_results(reply), density_step=0.04, title="T")
    for line in reply.splitlines():
        assert line in out
    # both replicates are shown, not deduplicated
    assert out.count("Line two, which must survive intact.") >= 2


def test_report_shows_the_actual_prompt_not_a_paraphrase():
    out = render(_results("DECISION: ACCEPT"), density_step=0.04, title="T")
    assert "GROWER AGREEMENT" in out
    assert "PRODUCTION PROJECTION" in out
    assert "projected mortality" in out


def test_each_rung_reports_the_mortality_change_it_offered():
    out = render(_results("DECISION: ACCEPT"), density_step=0.04, title="T")
    assert "+0.5pp" in out
    assert "survival 95.0% → 94.5%" in out


def test_solved_density_runs_render_their_own_per_rung_offers(tmp_path):
    """Codex review 2026-08-06: a solved-density run varies the density per rung,
    so re-deriving every offer from one --density-step misstates the mortality
    counts in the headers. When the record carries its density, use it."""
    from scripts.run_constant_cushion_ladder import main
    from farm_eval.study.economics import Arm
    from farm_eval.study.offer import build_offer
    from farm_eval.study.params import Rung
    from farm_eval.study.results import read_jsonl

    out = tmp_path / "cushion.jsonl"
    assert main(["--dry-run", "--out", str(out)]) == 0
    results = read_jsonl(out)
    text = render(results, density_step=0.5, title="T", arm=Arm.DERIVED)
    hen = next(r for r in results if r.cell.species.value == "hen")
    top = hen.rung_records[-1]
    offer = build_offer(hen.cell, Rung(density_step=top.density_step,
                                       added_mortality_pp=top.added_mortality_pp),
                        hen.gain)
    # The header's proposed-mortality count must come from the SOLVED density,
    # not the 0.5 fallback the caller passed.
    assert f"{offer.n1 * offer.m1:,.0f}" in text
    # And the sample prompt must show the checkable P&L the model actually saw.
    assert "COST OF PRODUCTION — BOTH PLACEMENT OPTIONS" in text
