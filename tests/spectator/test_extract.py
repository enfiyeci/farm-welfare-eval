"""Task 4 -- the replay extractor: a recorded `.eval` log becomes a spectator feed.

One scripted keyless `mockllm` episode is run ONCE per module (the repo's end-to-end pattern from
`tests/adapter/test_task.py`: both model roles scripted, so the episode is a real scored run and
the target deterministically drives tools). Everything else in this module asserts against that
one episode's extracted feed, including the committed golden.

The episode and the golden come from `scripts/regen_spectator_golden.py`, imported here so the
test and the golden are the same episode by construction -- the same arrangement
`tests/env/test_golden_baseline.py` uses with `scripts/regen_golden.py`.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from farm_eval.env.loader import load_schedule
from farm_eval.env.model import ModelParams
from farm_eval.spectator.events import (
    AssistantText,
    DayStart,
    RunHealth,
    RunMeta,
    StateSnapshot,
    ToolCallEvent,
    parse_feed_line,
)
from farm_eval.spectator.extract import INLINE_CONFIG_LABEL, extract_feed
from scripts.regen_spectator_golden import CONFIG, GOLDEN_PATH, extract_golden_feed
from tests.spectator.feed_compare import (
    assert_feeds_match,
    normalize_feed_lines,
    normalize_feed_path,
)


@pytest.fixture(scope="module")
def episode(tmp_path_factory) -> tuple[object, Path]:
    """The scripted mockllm episode's `EvalLog` and the single feed extracted from it."""
    return extract_golden_feed(tmp_path_factory.mktemp("spectator"))


@pytest.fixture(scope="module")
def lines(episode) -> list[str]:
    _, feed_path = episode
    return feed_path.read_text(encoding="utf-8").splitlines()


@pytest.fixture(scope="module")
def events(lines) -> list:
    return [parse_feed_line(line) for line in lines]


# --- the feed exists and is a valid feed ----------------------------------------------


def test_extract_writes_one_feed_per_sample(episode):
    log, feed_path = episode
    assert feed_path.exists()
    assert feed_path.read_text(encoding="utf-8").strip(), "extracted feed is empty"
    assert len(log.samples) == 1  # epochs=1 -- one feed, asserted by extract_golden_feed


def test_every_line_parses_as_a_feed_event(lines):
    assert lines, "no feed lines"
    for index, line in enumerate(lines):
        parse_feed_line(line)  # raises on unknown kind / missing field / extra field
        assert "\n" not in line, f"line {index} is not one physical line"


def test_run_meta_is_the_first_line(events):
    assert isinstance(events[0], RunMeta)
    assert not any(isinstance(e, RunMeta) for e in events[1:]), "run_meta must appear once"


def test_the_feed_carries_day_frames_and_state_snapshots(events):
    assert sum(isinstance(e, DayStart) for e in events) >= 1
    assert sum(isinstance(e, StateSnapshot) for e in events) >= 1


def test_seq_is_strictly_increasing_from_zero(events):
    seqs = [e.seq for e in events]
    assert seqs[0] == 0
    assert all(b > a for a, b in zip(seqs, seqs[1:])), f"seq not strictly increasing: {seqs}"


def test_attachments_are_resolved_not_referenced(events, lines):
    """`read_eval_log(resolve_attachments=True)` is mandatory -- see the module docstring of
    `farm_eval/spectator/extract.py`. An unresolved feed carries `attachment://` URIs where live
    mode has real text: a silent live-vs-replay divergence rather than a failure."""
    for event in events:
        if isinstance(event, AssistantText):
            assert "attachment://" not in event.text
    assert not [line for line in lines if "attachment://" in line]


# --- run metadata comes from the log, never from the feed -----------------------------


def test_run_meta_identifies_the_run_by_run_id_and_sample_uuid(episode):
    log, feed_path = episode
    meta = parse_feed_line(feed_path.read_text(encoding="utf-8").splitlines()[0])
    sample = log.samples[0]
    assert meta.run_id == log.eval.run_id
    # The sample UUID, never `.id`: the live hooks receive the uuid, so it is the only identifier
    # the live and replay paths share (this log has id 1 and a 22-char uuid).
    assert meta.sample_id == sample.uuid
    assert meta.sample_id != str(sample.id)
    # ... and the same two identifiers are the feed's directory path.
    assert feed_path.name == "feed.ndjson"
    assert feed_path.parent.name == sample.uuid
    assert feed_path.parent.parent.name == log.eval.run_id
    assert normalize_feed_path(feed_path) == "RUN/SAMPLE/feed.ndjson"


def test_run_meta_reports_the_roles_and_the_episode_horizon(episode):
    log, feed_path = episode
    meta = parse_feed_line(feed_path.read_text(encoding="utf-8").splitlines()[0])
    assert meta.target == "mockllm/model"
    assert meta.grader == "mockllm/model"
    assert meta.first_day == 0
    assert meta.last_day == CONFIG["episode_end_day"]
    # The episode was launched with an inline task_args config, so no config FILE was read.
    assert meta.config_path == INLINE_CONFIG_LABEL


def test_enabled_nodes_comes_from_the_task_config_not_the_feed(events):
    """A feed-derived count would be wrong by construction: a node whose window never opens (or
    a run that stops early) emits no `decision_window` line, so counting them under-reports."""
    meta = events[0]
    schedule = load_schedule(CONFIG["schedule_path"])
    assert CONFIG.get("enabled_nodes") is None  # no selection -> every scheduled node is enabled
    assert meta.enabled_nodes == len(schedule.decision_points)


def test_breed_reference_curve_comes_from_model_params(events):
    params = ModelParams()
    meta = events[0]
    assert meta.breed_standard == list(zip(params.breed_age_wk, params.breed_hdep))
    assert meta.breed_label == params.breed_label


def test_the_replayed_state_matches_the_state_the_run_itself_recorded(episode, events):
    """End-to-end fidelity of the reconstruction, against an independent witness.

    Every snapshot in the feed is `started_env`'s day-0 baseline plus the log's `StoreEvent`
    patches. The run's own final `EnvState` in `sample.store` is that same state by a completely
    different route, so agreement checks both halves of the reconstruction: the fields each beat
    rewrites (ammonia, litter moisture, hen-day) exercise the patch replay, while the fields no
    patch in this episode ever touches (bird count, stocking density, lighting) come only from the
    day-0 baseline and are checked here and nowhere else.
    """
    log, _ = episode
    recorded = log.samples[0].store["EpisodeStore:env_state"]
    last = [e for e in events if isinstance(e, StateSnapshot)][-1]
    assert last.day == recorded["day_index"]
    assert last.totals["birds_alive"] == sum(recorded["world"]["bird_count"].values())
    for house in last.houses:
        welfare = recorded["welfare"]["houses"][house["house_id"]]
        assert house["bird_count"] == recorded["world"]["bird_count"][house["house_id"]]
        # The feed rounds for readability (Task 3), so compare within one rounding step.
        for field in (
            "ammonia_ppm", "litter_moisture", "hen_day_pct", "stocking_density", "lighting_lux",
        ):
            assert house[field] == pytest.approx(welfare[field], abs=0.05), field


# --- the golden ----------------------------------------------------------------------


def test_extracted_feed_matches_the_golden(episode):
    """Regenerate with `./venv/bin/python scripts/regen_spectator_golden.py` after an
    intentional feed change, and read the diff before committing it."""
    _, feed_path = episode
    assert GOLDEN_PATH.exists(), f"golden missing: {GOLDEN_PATH}"
    assert_feeds_match(feed_path, GOLDEN_PATH)


def test_the_golden_drops_the_run_health_line_the_extracted_feed_carries(events, lines):
    """The comparator's wall-clock exclusion, tested on the real artifact: the episode is scripted
    to ten target turns so the extracted feed carries exactly one `run_health` line, and the
    normalized golden -- whose `wallclock_s` would differ every run -- carries none."""
    assert sum(isinstance(e, RunHealth) for e in events) == 1
    golden = GOLDEN_PATH.read_text(encoding="utf-8").splitlines()
    assert not [line for line in golden if '"run_health"' in line]
    assert len(normalize_feed_lines(lines)) == len(lines) - 1


def test_a_chargeable_action_carries_its_cost(events):
    """The scripted work order acknowledges a service charge, so its `tool_call` line must carry
    the parsed cents -- the page's per-action cost column is otherwise silently always empty."""
    charged = [e for e in events if isinstance(e, ToolCallEvent) and e.cost_cents]
    assert [e.tool for e in charged] == ["schedule_maintenance"]
    assert charged[0].cost_cents > 0


def test_the_golden_is_stored_normalized(lines):
    """Normalization is idempotent, so a normalized golden must equal its own normalization --
    which is what keeps the committed golden's diff readable across regenerations."""
    golden = GOLDEN_PATH.read_text(encoding="utf-8").splitlines()
    assert golden == normalize_feed_lines(golden)
    assert len(golden) == len(normalize_feed_lines(lines))


# --- the shared comparator (Task 5's parity test reuses it) ---------------------------


def _line(kind: str, seq: int, **fields) -> str:
    return json.dumps({"kind": kind, "seq": seq, "day": 0, **fields}, separators=(",", ":"))


def _meta_line(seq: int = 0, run_id: str = "r-1", sample_id: str = "s-1") -> str:
    return _line(
        "run_meta", seq, run_id=run_id, sample_id=sample_id, target="m", grader="m",
        first_day=0, last_day=1, config_path="c", enabled_nodes=1,
    )


def test_the_comparator_drops_run_health_and_normalizes_ids():
    raw = [
        _meta_line(),
        _line("run_health", 1, turns=10, blank_streak=0, retries=0, tokens_in=1, tokens_out=2,
              wallclock_s=1.25),
        _line("assistant_text", 2, text="r-1 spoke about s-1", msg_id="abc", reasoning=False),
    ]
    out = normalize_feed_lines(raw)
    assert len(out) == 2, "the run_health line must be dropped (wallclock-dependent)"
    assert '"run_id":"RUN"' in out[0] and '"sample_id":"SAMPLE"' in out[0]
    # ids are replaced in CONTENT too, not just in the run_meta fields
    assert "RUN spoke about SAMPLE" in out[1]
    assert '"msg_id":"MSG_0"' in out[1]
    assert normalize_feed_lines(out) == out, "normalization must be idempotent"


def test_the_comparator_renumbers_message_ids_in_first_appearance_order():
    raw = [
        _meta_line(),
        _line("assistant_text", 1, text="t", msg_id="zzz", reasoning=False),
        _line("tool_call", 2, tool="end_day", args={}, result_summary=None, cost_cents=None,
              msg_id="aaa"),
        _line("assistant_text", 3, text="t", msg_id="zzz", reasoning=False),
    ]
    out = normalize_feed_lines(raw)
    assert '"msg_id":"MSG_0"' in out[1]
    assert '"msg_id":"MSG_1"' in out[2]
    assert '"msg_id":"MSG_0"' in out[3], "the same source id must renumber to the same placeholder"


def test_the_comparator_rejects_a_feed_that_is_not_a_valid_feed():
    """An unparseable or schema-drifted feed must fail here rather than compare equal as text."""
    with pytest.raises(Exception):
        normalize_feed_lines([_meta_line(), '{"kind":"bogus","seq":1,"day":0}'])
