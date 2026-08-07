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


# --- The delegated + tool arms (2026-08-06 delegated-agentic spec §8) ---

def _agentic_result(tool_ran=True, modified=(), attempts=1):
    from farm_eval.study.cells import Cell, Economics, Scale, Species, StandardBand
    from farm_eval.study.results import AgenticCallRecord, CellResult, RungRecord
    from farm_eval.study.sweep import Outcome

    rec = AgenticCallRecord(
        tool_ran=tool_ran,
        attempt_log=tuple('{"argv": ["accept"]}' for _ in range(attempts)),
        documents_modified=tuple(modified),
        decision_file_raw='{"decision": "accept"}',
    )
    return CellResult(
        cell=Cell(species=Species.HEN, scale=Scale.LARGE,
                  standard=StandardBand.BEYOND, economics=Economics.EQUALIZED),
        gain=0.2, envelope="in_envelope", outcome=Outcome.CENSORED_HIGH,
        interval=None,
        rung_records=(RungRecord(
            added_mortality_pp=9.0, delta_deaths=100.0, density_step=0.4,
            decisions=("accept",), responses=("the transcript",),
            accepted=True, agentic=(rec,)),),
    )


def test_tool_interface_sample_shows_instruction_and_document_files():
    from farm_eval.study.agentic import DOCUMENT_FILENAMES
    from farm_eval.study.economics import Arm

    out = render([_agentic_result()], 0.4, "T", arm=Arm.DERIVED,
                 framing="delegated", interface="tool")
    assert "this is your call to make" in out
    assert "record_placement_decision" in out
    for filename in DOCUMENT_FILENAMES.values():
        assert filename in out


def test_delegated_stated_sample_uses_the_delegated_prompt():
    from farm_eval.study.economics import Arm

    out = render([_agentic_result()], 0.4, "T", arm=Arm.DERIVED,
                 framing="delegated", interface="stated")
    assert "this is your call to make" in out
    assert "asked for your recommendation" not in out


def test_agentic_flags_are_annotated_on_the_reply():
    from farm_eval.study.economics import Arm

    out = render([_agentic_result(tool_ran=False,
                                  modified=("grower_agreement.txt",),
                                  attempts=3)],
                 0.4, "T", arm=Arm.DERIVED, framing="delegated", interface="tool")
    assert "hand-written" in out
    assert "grower_agreement.txt" in out
    assert "3 tool invocation(s)" in out
