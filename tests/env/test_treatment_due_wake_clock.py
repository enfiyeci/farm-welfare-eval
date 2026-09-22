"""The clock convenes a session on the day a red-mite treatment step falls due (Task 3 of the
DP05 red-mite full-course plan), in a NODE EPISODE.

A node episode's sessions are an authored list (`beat_days`), and for the red-mite node they are
[126, 154, 168, 211] — 28 days apart at the front, where a lawful systemic course is two doses 7
days apart. Without the due-day rule the agent can never finish the course it just asked the vet
for. `FarmEnv.end_day` therefore jumps to `harm_window.treatment_due_day` when that day falls
before the next authored session; the sessions themselves are never mutated.

The continuous-calendar half of the same behaviour lives in `tests/env/test_event_window.py`.
"""

import copy
from pathlib import Path

import pytest

from farm_eval.env.episode import FarmEnv
from farm_eval.env.loader import load_corpus, load_schedule
from farm_eval.env.model.params import ModelParams
from farm_eval.env.node_episodes import expand_episodes, load_node_manifest
from farm_eval.env.snapshot import derive_snapshot

REPO = Path(__file__).resolve().parents[2]
EPISODE = "DP05_RED_MITE"
HOUSE = "H2"
ORDER = "PAH-RX-H2-112"
REQUEST = ("request_vet_treatment", {"house_id": HOUSE, "issue": "red_mite"})
DOSE = ("administer_vet_order", {"order_id": ORDER})

pytestmark = pytest.mark.skipif(
    not (REPO / "schedule" / "node_episodes.yml").is_file(), reason="real manifest not present"
)


@pytest.fixture(scope="module")
def snapshot():
    """The real n_RED_MITE episode's opening world, derived once (the replay to day 112 is the
    expensive part; each test plays its own deep copy)."""
    corpus, schedule = load_corpus(REPO / "corpus"), load_schedule(REPO / "schedule")
    manifest = load_node_manifest(REPO / "schedule")
    ep = next(r for r in expand_episodes(manifest, schedule) if r.episode_id == EPISODE)
    state, _ = derive_snapshot(corpus, schedule, ModelParams(), ep, seed=0)
    return corpus, schedule, ep, state


def _env(snapshot) -> FarmEnv:
    corpus, schedule, ep, state = snapshot
    env = FarmEnv(
        corpus, schedule, copy.deepcopy(state), ep.end_day, ModelParams(),
        enabled_nodes=tuple(ep.enabled_nodes), beat_days=ep.sessions,
    )
    env.start()
    return env


def _act(env: FarmEnv, call: tuple[str, dict]) -> None:
    tool, params = call
    res = env.apply_action(tool, dict(params))
    assert res.ok, f"day {env.current_day()} {tool} rejected: {res.detail}"


def test_the_episode_sessions_are_the_authored_ones(snapshot):
    _, _, ep, state = snapshot
    assert ep.start_day == 112 and ep.end_day == 211
    assert ep.sessions == [126, 154, 168, 211]
    assert state.day_index == 112


def test_a_full_course_pulls_two_sessions_in_front_of_the_authored_ones(snapshot):
    env = _env(snapshot)
    _act(env, REQUEST)                       # approval lag 2 -> approved_day 114
    assert env.end_day().new_day == 114       # not the authored session 126
    _act(env, DOSE)                           # dose 1; the second is due 7 days later
    assert env.end_day().new_day == 121       # not 126 either
    _act(env, DOSE)                           # dose 2 completes the course
    assert env.end_day().new_day == 126        # nothing due -> the authored sessions resume
    assert env.end_day().new_day == 154
    assert env._beat_days == [126, 154, 168, 211]  # the session list was never mutated


def test_an_approved_order_never_dosed_wakes_once_and_no_more(snapshot):
    env = _env(snapshot)
    _act(env, REQUEST)
    assert env.end_day().new_day == 114        # the approval day
    # Day 114 arrived and the agent did nothing: the due day is no longer in the future, so it
    # is not a fresh wake. The order waits for the next authored session.
    assert env.end_day().new_day == 126


def test_no_order_leaves_the_authored_sessions_alone(snapshot):
    env = _env(snapshot)
    assert env.end_day().new_day == 126
    assert env.end_day().new_day == 154


def test_the_one_day_harm_cap_keeps_priority_over_a_due_day(snapshot):
    env = _env(snapshot)
    _act(env, REQUEST)                         # due day 114
    env.state.welfare.houses[HOUSE].egg_residue_days_left = 4.0  # arms active_harm_day
    assert env.end_day().new_day == 113         # old_day + 1, ahead of the due day
