"""Manifest models, loader, schedule validation and expansion (D6 defaults, D11 no content in logic)."""
from pathlib import Path

import pytest

from farm_eval.env.loader import load_schedule
from farm_eval.env.node_episodes import (
    NodeEpisodeManifest,
    expand_episodes,
    load_node_manifest,
    resolve_sessions,
    validate_manifest,
)

FIX = Path(__file__).resolve().parents[1] / "fixtures" / "node_schedule"


def _loaded():
    schedule = load_schedule(FIX)
    manifest = load_node_manifest(FIX)
    validate_manifest(manifest, schedule)
    return schedule, manifest


def test_fixture_manifest_loads_and_validates():
    schedule, manifest = _loaded()
    assert [e.id for e in manifest.episodes] == ["DP_PLACEHOLDER_2", "QUIET_D15"]
    assert manifest.meta.default_arm == "neutral"


def test_defaults_follow_the_schedule_window():
    schedule, manifest = _loaded()
    ep = manifest.episodes[0]
    resolved = expand_episodes(manifest, schedule)
    neutral = next(r for r in resolved if r.episode_id == "DP_PLACEHOLDER_2" and r.arm_id == "neutral")
    assert (neutral.start_day, neutral.end_day) == (10, 21)          # opens_day, deadline_day + 1
    assert neutral.sessions == [15, 20, 21]                            # beats in (10, 21) plus end_day
    assert neutral.enabled_nodes == ("DP_PLACEHOLDER_2",)
    assert neutral.scored is True
    assert neutral.welfare_pass_min == 7.0
    assert neutral.digest_note is None


def test_expansion_yields_one_resolved_episode_per_arm_plus_quiet():
    schedule, manifest = _loaded()
    resolved = expand_episodes(manifest, schedule)
    keys = [(r.episode_id, r.arm_id) for r in resolved]
    assert keys == [("DP_PLACEHOLDER_2", "neutral"), ("DP_PLACEHOLDER_2", "history_bad"), ("QUIET_D15", "neutral")]
    bad = resolved[1]
    assert bad.digest_note.startswith("prior-session note")
    quiet = resolved[2]
    assert quiet.scored is False and quiet.dp_id is None and quiet.enabled_nodes == ()
    assert (quiet.start_day, quiet.end_day, quiet.sessions) == (15, 20, [20])


def test_resolve_sessions_uses_explicit_list_when_given():
    schedule, manifest = _loaded()
    ep = manifest.episodes[0].model_copy(update={"sessions": [20, 21]})
    assert resolve_sessions(ep, schedule, start_day=10, end_day=21) == [20, 21]


@pytest.mark.parametrize(
    "patch, message",
    [
        ({"dp_id": "NOPE"}, "unknown decision point"),
        ({"start_day": 11}, "start_day 11 is after opens_day 10"),
        ({"start_day": 7}, "start_day 7 is not a schedule beat"),
        ({"end_day": 20}, "end_day 20 must be after deadline_day 20"),
        ({"sessions": [15, 21]}, "sessions must contain deadline_day 20"),
        ({"sessions": [15, 20]}, "last session must equal end_day 21"),
        ({"prelude_actions": [{"day": 7, "tool": "end_day", "params": {}}]}, "prelude action day 7 is not a schedule beat"),
        ({"prelude_actions": [{"day": 10, "tool": "end_day", "params": {}}]}, "prelude action day 10 must be before start_day 10"),
        ({"arms": [{"id": "x"}]}, "no arm named the default arm 'neutral'"),
        ({"arms": [{"id": "neutral"}, {"id": "neutral"}]}, "duplicate arm id"),
        ({"sessions": []}, "sessions must not be empty"),
    ],
)
def test_validation_fails_loud(patch, message):
    schedule = load_schedule(FIX)
    manifest = load_node_manifest(FIX)
    episodes = list(manifest.episodes)
    episodes[0] = episodes[0].model_copy(update=patch)
    broken = manifest.model_copy(update={"episodes": episodes})
    with pytest.raises(ValueError, match=message):
        validate_manifest(broken, schedule)


def test_quiet_episode_must_not_name_a_node_and_node_episode_must():
    schedule = load_schedule(FIX)
    with pytest.raises(ValueError, match="quiet episode QUIET_D15 must not set dp_id"):
        NodeEpisodeManifest.model_validate({
            "meta": {}, "episodes": [{"id": "QUIET_D15", "kind": "quiet", "dp_id": "DP_PLACEHOLDER_2",
                                      "start_day": 15, "end_day": 20}]})
    with pytest.raises(ValueError, match="node episode X requires dp_id"):
        NodeEpisodeManifest.model_validate({"meta": {}, "episodes": [{"id": "X"}]})


def test_duplicate_episode_ids_rejected():
    schedule = load_schedule(FIX)
    manifest = load_node_manifest(FIX)
    doubled = manifest.model_copy(update={"episodes": [manifest.episodes[0], manifest.episodes[0]]})
    with pytest.raises(ValueError, match="duplicate episode id"):
        validate_manifest(doubled, schedule)


def test_store_dict_round_trips_the_fields_the_adapter_needs():
    schedule, manifest = _loaded()
    r = expand_episodes(manifest, schedule)[1]
    d = r.to_store_dict(opening_digest="Console session — ... (14 days since the previous session)")
    assert d == {
        "episode_id": "DP_PLACEHOLDER_2", "arm_id": "history_bad", "dp_id": "DP_PLACEHOLDER_2",
        "start_day": 10, "end_day": 21, "sessions": [15, 20, 21], "enabled_nodes": ["DP_PLACEHOLDER_2"],
        "scored": True, "welfare_pass_min": 7.0, "ablation_overrides": None,
        "opening_digest": "Console session — ... (14 days since the previous session)",
    }
