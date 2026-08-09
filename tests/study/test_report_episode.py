import importlib.util
from pathlib import Path
from farm_eval.study.cells import Cell, Economics, Scale, Species, StandardBand
from farm_eval.study.response import Decision
from farm_eval.study.results import (
    AgenticCallRecord,
    EpisodeRecord,
    RoundRecord,
    write_episodes_jsonl,
)

spec = importlib.util.spec_from_file_location(
    "rt", Path("scripts/report_transcripts.py")
)
rt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rt)


def test_render_episodes_shows_rounds_and_terminal(tmp_path):
    c = Cell(
        species=Species.HEN,
        scale=Scale.LARGE,
        standard=StandardBand.BEYOND,
        economics=Economics.EQUALIZED,
    )
    a = AgenticCallRecord(
        tool_ran=True, attempt_log=(), documents_modified=(), decision_file_raw=None
    )
    e = EpisodeRecord(
        cell=c,
        arm="same",
        rounds=(
            RoundRecord(
                proposed_index=120,
                n0=1e6,
                m0=0.05,
                n1=1.2e6,
                m1=0.07,
                gain=0.3,
                cushion_pp=6,
                delta_deaths=1,
                cumulative_deaths=1,
                decision=Decision.ACCEPT,
                agentic=a,
                response="hi",
            ),
        ),
        terminal_index=120,
        terminal_cumulative_deaths=1,
        stop_reason="declined",
        crossed_compliance=False,
        stopped_at_compliance=True,
    )
    p = tmp_path / "e"
    write_episodes_jsonl([e], p)
    assert "index 120" in rt.render_episodes(str(p))
