"""D2 -- per-beat EnvState checkpointing (opt-in), for paid-run resilience against a hard kill.

Mirrors the mockllm fixture pattern of tests/adapter/test_solver.py: a real inspect_eval() run
against the shared tests/fixtures corpus, with a bespoke multi-beat schedule (written to tmp_path)
so an episode reaches >= 4 distinct beats without needing the full production schedule.
"""

import json
import os
import stat
from pathlib import Path

import pytest
import yaml
from inspect_ai import Task
from inspect_ai import eval as inspect_eval
from inspect_ai.dataset import Sample
from inspect_ai.model import ModelOutput, get_model

from farm_eval.adapter.checkpoint import _sample_dir_name, load_checkpoint, write_checkpoint
from farm_eval.adapter.context import EpisodeConfig, EpisodeStore, get_env
from farm_eval.adapter.solver.farm_solver import farm_solver
from farm_eval.env.state import EnvState

FIX = Path(__file__).resolve().parents[1] / "fixtures"
CORPUS = str(FIX / "corpus")

# A bespoke schedule with FIVE decision points opening/closing on distinct days, so a run to
# episode_end_day=20 crosses beats {0, 2, 4, 6, 8, 20} -- comfortably >= 4 beats. Each DP is
# self-contained (no `events:` needed -- decision points alone contribute beat days via
# Schedule.event_days()), so there is no body_ref to satisfy.
_BEAT_DAYS = [2, 4, 6, 8]


def _make_schedule(tmp_path: Path) -> Path:
    dps = []
    for day in _BEAT_DAYS:
        dps.append(
            {
                "id": f"DP_BEAT_{day}",
                "category": "initiative",
                "prompted": False,
                "opens_day": day,
                "deadline_day": day,
                "signature": {
                    "any_of": [{"tool": "adjust_setpoint", "where": {"house_id": "H_SENSOR", "system": "ventilation"}}],
                    "scoring": {
                        "criteria": [
                            {"name": "addressed", "points": 10.0, "kind": "mechanical", "binary": {"matched": 1.0, "default": 0.0}}
                        ]
                    },
                },
            }
        )
    sched_dir = tmp_path / "schedule"
    sched_dir.mkdir(parents=True)
    (sched_dir / "events.yml").write_text(yaml.safe_dump({"decision_points": dps, "events": []}), encoding="utf-8")
    return sched_dir


def _cfg(schedule_path: Path, episode_end_day: int = 20) -> EpisodeConfig:
    return EpisodeConfig(corpus_path=CORPUS, schedule_path=str(schedule_path), episode_end_day=episode_end_day, seed=1)


def _end_day(): return ModelOutput.for_tool_call(model="mockllm/model", tool_name="end_day", tool_arguments={})


def _reads(n): return [ModelOutput.for_tool_call(model="mockllm/model", tool_name="get_datetime", tool_arguments={}) for _ in range(n)]


def _run(cfg, *, checkpoint_dir=None, sample_id=1, custom_outputs=None, max_turns_per_day=10):
    target = get_model("mockllm/model", custom_outputs=custom_outputs)
    log = inspect_eval(
        Task(
            dataset=[Sample(input="run the farm", id=sample_id)],
            solver=farm_solver(cfg, max_turns_per_day=max_turns_per_day, checkpoint_dir=checkpoint_dir),
        ),
        model="mockllm/model",
        model_roles={"target": target},
        display="none",
    )[0]
    assert log.status == "success", log.error
    return log


def test_checkpointing_off_by_default_writes_nothing(tmp_path):
    # No checkpoint_dir passed at all: zero behavior change (the regression guard).
    schedule = _make_schedule(tmp_path / "sched_src")
    cfg = _cfg(schedule)
    log = _run(cfg, custom_outputs=[_end_day() for _ in range(6)])
    assert log.samples[0].store["EpisodeStore:env_state"]["day_index"] == 20
    # Nothing under tmp_path was created by the checkpoint helper (only our own sched_src dir).
    created = {p for p in tmp_path.rglob("*") if p.is_file()}
    sched_files = {p for p in (tmp_path / "sched_src").rglob("*") if p.is_file()}
    assert created == sched_files


def test_checkpoints_appear_per_beat_with_last_3_retention(tmp_path):
    schedule = _make_schedule(tmp_path / "sched_src")
    ckpt_dir = tmp_path / "ckpt"
    cfg = _cfg(schedule)
    log = _run(cfg, checkpoint_dir=str(ckpt_dir), sample_id=1, custom_outputs=[_end_day() for _ in range(6)])

    sample_dir = ckpt_dir / "1"
    files = sorted(sample_dir.glob("day_*.json"))
    days_present = sorted(int(p.stem.split("_")[1]) for p in files)
    # Beats reached: 0(start, no checkpoint until first end_day), 2, 4, 6, 8, 20 -- 5 end_day calls
    # produce checkpoints at days [2, 4, 6, 8, 20]; retention keeps only the LAST 3.
    assert days_present == [6, 8, 20]

    for p in files:
        data = json.loads(p.read_text(encoding="utf-8"))
        day = int(p.stem.split("_")[1])
        assert data["day"] == day
        assert data["env_state"]["day_index"] == day
        assert isinstance(data["message_count"], int) and data["message_count"] > 0

    final_env_state = log.samples[0].store["EpisodeStore:env_state"]
    assert final_env_state["day_index"] == 20


def test_checkpoint_atomicity_no_stray_temp_files(tmp_path):
    schedule = _make_schedule(tmp_path / "sched_src")
    ckpt_dir = tmp_path / "ckpt"
    cfg = _cfg(schedule)
    _run(cfg, checkpoint_dir=str(ckpt_dir), sample_id=1, custom_outputs=[_end_day() for _ in range(6)])

    sample_dir = ckpt_dir / "1"
    all_files = list(sample_dir.iterdir())
    non_final = [p for p in all_files if not (p.name.startswith("day_") and p.name.endswith(".json"))]
    assert non_final == []  # no leftover .tmp / partial files
    for p in all_files:
        json.loads(p.read_text(encoding="utf-8"))  # every remaining file parses cleanly


def test_restart_from_checkpoint_matches_uninterrupted_run(tmp_path):
    schedule = _make_schedule(tmp_path / "sched_src")
    ckpt_dir = tmp_path / "ckpt"
    cfg = _cfg(schedule)

    # Uninterrupted reference run to day 20.
    reference = _run(cfg, checkpoint_dir=str(ckpt_dir), sample_id=42, custom_outputs=[_end_day() for _ in range(6)])
    reference_state = reference.samples[0].store["EpisodeStore:env_state"]

    # Load the EARLIEST retained checkpoint (day 6 -- after last-3 retention the retained set is
    # {6, 8, 20}, so [0] is day 6, not the final day 20) and confirm we captured it.
    sample_dir = ckpt_dir / "42"
    earlier = sorted(sample_dir.glob("day_*.json"), key=lambda p: int(p.stem.split("_")[1]))[0]
    day, message_count, env_state = load_checkpoint(earlier)
    assert isinstance(env_state, EnvState)
    assert day == env_state.day_index
    assert message_count > 0

    # Fresh env/store: inject the loaded checkpoint state, then re-enter the solver and run to
    # completion. FarmEnv.start() must be idempotent (EnvState.started) so day-0 events do not
    # re-fire on re-entry.
    from inspect_ai.solver import Generate, TaskState, solver

    @solver
    def resume_from_checkpoint():
        async def solve(state: TaskState, generate: Generate) -> TaskState:
            from inspect_ai.util import store_as

            store = store_as(EpisodeStore)
            store.env_state = env_state
            get_env(cfg).start()
            return state

        return solve

    resume_solver = farm_solver(cfg, max_turns_per_day=10, checkpoint_dir=None)

    @solver
    def combined():
        first = resume_from_checkpoint()
        second = resume_solver

        async def solve(state, generate):
            state = await first(state, generate)
            state = await second(state, generate)
            return state

        return solve

    remaining_outputs = [_end_day() for _ in range(6)]
    target = get_model("mockllm/model", custom_outputs=remaining_outputs)
    log = inspect_eval(
        Task(dataset=[Sample(input="resume", id=42)], solver=combined()),
        model="mockllm/model",
        model_roles={"target": target},
        display="none",
    )[0]
    assert log.status == "success", log.error
    resumed_state = log.samples[0].store["EpisodeStore:env_state"]
    assert resumed_state == reference_state


def test_forced_advance_path_still_checkpoints(tmp_path):
    # The agent never calls end_day; the max-turns-per-day backstop must still checkpoint.
    schedule = _make_schedule(tmp_path / "sched_src")
    ckpt_dir = tmp_path / "ckpt"
    cfg = _cfg(schedule, episode_end_day=8)
    _run(cfg, checkpoint_dir=str(ckpt_dir), sample_id=7, custom_outputs=_reads(80), max_turns_per_day=3)

    sample_dir = ckpt_dir / "7"
    files = sorted(sample_dir.glob("day_*.json"))
    assert files  # at least one forced-advance checkpoint was written
    days_present = sorted(int(p.stem.split("_")[1]) for p in files)
    assert days_present[-1] == 8


def test_checkpoint_io_failure_warns_and_never_kills_episode(tmp_path, caplog):
    schedule = _make_schedule(tmp_path / "sched_src")
    # Point checkpoint_dir at a path underneath a FILE (not a directory) -- writes there fail.
    blocker = tmp_path / "not_a_dir"
    blocker.write_text("i am a file, not a directory", encoding="utf-8")
    bad_ckpt_dir = blocker / "ckpt"
    cfg = _cfg(schedule)

    import logging

    with caplog.at_level(logging.WARNING):
        log = _run(cfg, checkpoint_dir=str(bad_ckpt_dir), sample_id=1, custom_outputs=[_end_day() for _ in range(6)])

    assert log.status == "success"
    assert log.samples[0].store["EpisodeStore:env_state"]["day_index"] == 20
    assert any("checkpoint" in rec.message.lower() for rec in caplog.records)


# --- F1: sample_id sanitization must not allow path traversal or root cross-contamination ---


@pytest.mark.parametrize("hostile", ["..", ".", "", "../..", "./.", "..\x00"])
def test_sample_dir_name_neutralizes_traversal_segments(hostile):
    # A sample_id that would sanitize to "." / ".." / "" must NOT stay a traversal/self segment:
    # the result must be a single, safe path component that resolves strictly inside its parent.
    name = _sample_dir_name(hostile)
    assert name not in ("", ".", "..")
    assert "/" not in name and os.sep not in name  # a single path segment, no separators
    parent = Path("/base/ckpt")
    resolved = (parent / name).resolve()
    # The write dir must live strictly UNDER the checkpoint_dir, never escape to its parent.
    assert resolved.parent == parent.resolve()
    assert resolved != parent.resolve()


def test_sample_dir_name_preserves_normal_ids():
    assert _sample_dir_name(1) == "1"
    assert _sample_dir_name("sample-42_a.b") == "sample-42_a.b"


def test_write_checkpoint_traversal_id_stays_inside_checkpoint_dir(tmp_path):
    # A hostile ".." sample_id must write UNDER checkpoint_dir and must NOT create/unlink files in
    # its PARENT. Seed a sentinel day_*.json in the parent and prove it is untouched.
    ckpt_dir = tmp_path / "ckpt"
    ckpt_dir.mkdir()
    sentinel = tmp_path / "day_999.json"  # lives in ckpt_dir's PARENT
    sentinel.write_text("sentinel", encoding="utf-8")

    env_state = EnvState(start_date="2025-06-09")
    write_checkpoint(str(ckpt_dir), "..", day=3, message_count=5, env_state=env_state)

    # The parent sentinel is untouched (no retention prune reached outside checkpoint_dir).
    assert sentinel.read_text(encoding="utf-8") == "sentinel"
    # No day_*.json was written into the parent directory itself.
    assert not (tmp_path / "day_3.json").exists()
    # The checkpoint landed strictly under checkpoint_dir, in a sanitized sample subdir.
    written = list(ckpt_dir.rglob("day_3.json"))
    assert len(written) == 1
    assert ckpt_dir.resolve() in written[0].resolve().parents


# --- F2: positive coverage of the PRODUCTION config path (EpisodeConfig.checkpoint_dir) ---


def test_checkpoints_written_via_episode_config_checkpoint_dir(tmp_path):
    # The advertised production flow: checkpoint_dir set on EpisodeConfig (NOT the solver override).
    # farm_solver must fall back to cfg.checkpoint_dir and write checkpoints through that path.
    schedule = _make_schedule(tmp_path / "sched_src")
    ckpt_dir = tmp_path / "ckpt"
    cfg = EpisodeConfig(
        corpus_path=CORPUS,
        schedule_path=str(schedule),
        episode_end_day=20,
        seed=1,
        checkpoint_dir=str(ckpt_dir),  # <-- the production seam, not the solver kwarg
    )
    # _run passes checkpoint_dir=None to farm_solver, so ONLY cfg.checkpoint_dir can drive writes.
    _run(cfg, checkpoint_dir=None, sample_id=99, custom_outputs=[_end_day() for _ in range(6)])

    sample_dir = ckpt_dir / "99"
    files = sorted(sample_dir.glob("day_*.json"))
    days_present = sorted(int(p.stem.split("_")[1]) for p in files)
    assert days_present == [6, 8, 20]  # per-beat writes with last-3 retention, via the config path
