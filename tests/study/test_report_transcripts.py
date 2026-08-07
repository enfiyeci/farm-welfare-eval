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
