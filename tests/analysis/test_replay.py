from __future__ import annotations

import pytest
from inspect_ai._util.json import JsonChange
from inspect_ai.event import StoreEvent

from farm_eval.analysis.replay import replay_feed
from farm_eval.spectator.events import EpisodeEnd, RunMeta, StateSnapshot, ToolCallEvent
from scripts.regen_spectator_golden import run_episode


@pytest.fixture(scope="module")
def log(tmp_path_factory):
    return run_episode(tmp_path_factory.mktemp("analysis-replay") / "logs")


def test_full_fidelity_replay(log) -> None:
    result = replay_feed(log, log.samples[0])
    assert result.fidelity == "full" and result.failure_day is None
    assert result.fidelity_reason is None
    kinds = [type(e) for e in result.events]
    assert kinds[0] is RunMeta and kinds[-1] is EpisodeEnd
    assert any(k is StateSnapshot for k in kinds) and any(k is ToolCallEvent for k in kinds)


def test_broken_store_patch_degrades_to_transcript_only(log) -> None:
    sample = log.samples[0].model_copy(deep=True)
    for event in sample.events:
        if isinstance(event, StoreEvent):
            event.changes.append(
                JsonChange(op="replace", path="/EpisodeStore:env_state/nonexistent/9", value=1)
            )
            break
    result = replay_feed(log, sample)
    assert result.fidelity == "transcript_only"
    assert result.failure_day is not None
    assert result.fidelity_reason is None       # the failure day already says what went wrong
    assert any(isinstance(e, ToolCallEvent) for e in result.events)   # transcript stream survives
    assert isinstance(result.events[-1], EpisodeEnd)


def test_a_final_state_mismatch_degrades_with_a_reason_rather_than_raising(log) -> None:
    """Every patch applies, but the replayed state is not the state the run recorded.

    The spectator raises here. This wrapper must not: it exists to stay analysable over logs whose
    store stream no longer replays cleanly. So it degrades to `transcript_only` -- a state series
    that is state-shaped and wrong is worse than an absent one -- and records WHY, so the report
    tells the reader the state disagreed rather than that the feed stopped.
    """
    sample = log.samples[0].model_copy(deep=True)
    recorded = dict(sample.store["EpisodeStore:env_state"])
    recorded["day_index"] = recorded["day_index"] + 7
    sample.store["EpisodeStore:env_state"] = recorded

    result = replay_feed(log, sample)

    assert result.fidelity == "transcript_only"
    assert result.failure_day is None           # nothing failed to apply; the RESULT disagreed
    assert result.fidelity_reason is not None
    assert "does not match" in result.fidelity_reason
    assert any(isinstance(e, ToolCallEvent) for e in result.events)
