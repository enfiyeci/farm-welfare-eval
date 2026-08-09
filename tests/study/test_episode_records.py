import pytest
from farm_eval.study.cells import Cell, Economics, Scale, Species, StandardBand
from farm_eval.study.response import Decision
from farm_eval.study.results import (
    AgenticCallRecord,
    EpisodeRecord,
    RoundRecord,
    read_episodes_jsonl,
    write_episodes_jsonl,
)

CELL = Cell(
    species=Species.HEN,
    scale=Scale.LARGE,
    standard=StandardBand.BEYOND,
    economics=Economics.EQUALIZED,
)
REC = AgenticCallRecord(
    tool_ran=True,
    attempt_log=("x",),
    documents_modified=(),
    decision_file_raw='{"decision":"accept"}',
)


def _round(idx):
    return RoundRecord(
        proposed_index=idx,
        n0=1e6,
        m0=0.05,
        n1=1.1e6,
        m1=0.06,
        gain=0.2,
        cushion_pp=6.0,
        delta_deaths=16000.0,
        cumulative_deaths=16000.0,
        decision=Decision.ACCEPT,
        agentic=REC,
        response="reasoning",
    )


def test_episode_roundtrips_through_jsonl(tmp_path):
    ep = EpisodeRecord(
        cell=CELL,
        arm="same",
        rounds=(_round(110.0), _round(125.0)),
        terminal_index=125.0,
        terminal_cumulative_deaths=32000.0,
        stop_reason="declined",
        crossed_compliance=True,
        stopped_at_compliance=False,
    )
    path = tmp_path / "ep.jsonl"
    write_episodes_jsonl([ep], path)
    assert read_episodes_jsonl(path) == [ep]


def test_extra_fields_rejected():
    with pytest.raises(Exception):
        RoundRecord(
            proposed_index=1,
            n0=1,
            m0=0,
            n1=1,
            m1=0,
            gain=0,
            cushion_pp=0,
            delta_deaths=0,
            cumulative_deaths=0,
            decision=Decision.DECLINE,
            agentic=REC,
            response="",
            surprise=1,
        )
