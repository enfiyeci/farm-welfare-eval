"""The node-episode manifest: which decision windows are played as their own Inspect sample.

Content-free by construction — every id, day, house and action comes from
`<schedule_path>/node_episodes.yml`; this module knows only the schema and the rules that tie
an episode to its decision point's window in `events.yml` (design plan
evals/hen/design/2026-09-15-node-episodes-build.md, decisions D1–D6).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, model_validator

from farm_eval.env.loader import Schedule

_FORBID = ConfigDict(extra="forbid")

MANIFEST_FILENAME = "node_episodes.yml"


class PreludeAction(BaseModel):
    """One scripted action applied during the routine-only prelude replay (D2)."""

    model_config = _FORBID
    day: int
    tool: str
    params: dict[str, Any] = Field(default_factory=dict)


class EpisodeArm(BaseModel):
    model_config = _FORBID
    id: str
    digest_note: str | None = None
    ablation_overrides: dict[str, str] | None = None
    prelude_actions: list[PreludeAction] = Field(default_factory=list)


class ManifestMeta(BaseModel):
    model_config = _FORBID
    default_arm: str = "neutral"
    welfare_pass_min: float = 7.0
    shared_prelude_actions: list[PreludeAction] = Field(default_factory=list)


class NodeEpisodeSpec(BaseModel):
    model_config = _FORBID
    id: str
    kind: Literal["node", "quiet"] = "node"
    dp_id: str | None = None
    start_day: int | None = None
    end_day: int | None = None
    sessions: list[int] | None = None
    welfare_pass_min: float | None = None
    prelude_actions: list[PreludeAction] = Field(default_factory=list)
    expected_degenerate_channels: list[str] = Field(default_factory=list)
    # Decision points, BESIDES the scored one, whose latent-signal daily wakes may cap this
    # episode's clock (`FarmEnv(wake_nodes=...)`; wake audit 2026-09-30). Empty by default: an
    # episode is woken only by its own node's signal.
    wake_nodes: list[str] = Field(default_factory=list)
    arms: list[EpisodeArm] | None = None

    @model_validator(mode="after")
    def _kind_vs_dp(self) -> "NodeEpisodeSpec":
        if self.kind == "quiet":
            if self.dp_id is not None:
                raise ValueError(f"quiet episode {self.id} must not set dp_id")
            if self.start_day is None or self.end_day is None:
                raise ValueError(f"quiet episode {self.id} requires explicit start_day and end_day")
        elif self.dp_id is None:
            raise ValueError(f"node episode {self.id} requires dp_id")
        return self


class NodeEpisodeManifest(BaseModel):
    model_config = _FORBID
    meta: ManifestMeta = Field(default_factory=ManifestMeta)
    episodes: list[NodeEpisodeSpec] = Field(default_factory=list)


def load_node_manifest(schedule_path: str | Path) -> NodeEpisodeManifest:
    path = Path(schedule_path) / MANIFEST_FILENAME
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    return NodeEpisodeManifest.model_validate(data)


def _dp_index(schedule: Schedule) -> dict:
    return {dp.id: dp for dp in schedule.decision_points}


def _window(spec: NodeEpisodeSpec, schedule: Schedule) -> tuple[int, int]:
    """(start_day, end_day) with the D6 defaults applied."""
    if spec.kind == "quiet":
        return int(spec.start_day), int(spec.end_day)  # both required by the model validator
    dp = _dp_index(schedule)[spec.dp_id]
    start = dp.opens_day if spec.start_day is None else spec.start_day
    end = dp.deadline_day + 1 if spec.end_day is None else spec.end_day
    return start, end


def resolve_sessions(spec: NodeEpisodeSpec, schedule: Schedule, *, start_day: int, end_day: int) -> list[int]:
    """The days the clock stops at after start_day: the explicit list, or every schedule beat
    strictly inside (start_day, end_day) plus end_day (D6)."""
    if spec.sessions is not None:
        return list(spec.sessions)
    inside = [d for d in schedule.event_days() if start_day < d < end_day]
    return inside + [end_day]


def _as_prelude_action(entry: Any) -> PreludeAction:
    """Normalise a prelude-action entry that may arrive as a plain dict.

    `model_copy(update=...)` (used by the test suite to build broken manifests) does not
    re-run validators or coerce nested dicts into models, so a patched `prelude_actions` list
    can hold plain dicts instead of `PreludeAction` instances by the time `validate_manifest`
    sees it. Accept either shape rather than assuming the loader's own validated path.
    """
    if isinstance(entry, PreludeAction):
        return entry
    return PreludeAction.model_validate(entry)


def _as_episode_arm(entry: Any) -> EpisodeArm:
    """Normalise an arm entry that may arrive as a plain dict — same `model_copy` caveat as
    `_as_prelude_action` above, for a patched `arms` list."""
    if isinstance(entry, EpisodeArm):
        return entry
    return EpisodeArm.model_validate(entry)


def validate_manifest(manifest: NodeEpisodeManifest, schedule: Schedule) -> None:
    """Fail loud on any manifest that cannot be played faithfully against this schedule."""
    dps = _dp_index(schedule)
    beats = set(schedule.event_days())
    seen: set[str] = set()
    for spec in manifest.episodes:
        if spec.id in seen:
            raise ValueError(f"duplicate episode id {spec.id!r}")
        seen.add(spec.id)
        if spec.kind == "node" and spec.dp_id not in dps:
            raise ValueError(f"episode {spec.id}: unknown decision point {spec.dp_id!r}")
        unknown = [w for w in spec.wake_nodes if w not in dps]
        if unknown:
            raise ValueError(f"episode {spec.id}: unknown decision point(s) in wake_nodes {unknown}")
        start, end = _window(spec, schedule)
        if start < 1:
            raise ValueError(f"episode {spec.id}: start_day {start} must be >= 1 (day 0 is placement)")
        dp = dps[spec.dp_id] if spec.kind == "node" else None
        # Decision-point-specific bounds are checked BEFORE the generic "is a schedule beat"
        # check: a start_day that both misses opens_day and isn't a beat should read as the
        # more specific, more informative complaint (D-day-11 is neither a beat nor <= opens_day
        # 10; the contract is the opens_day message, not the beat one).
        if dp is not None and start > dp.opens_day:
            raise ValueError(f"episode {spec.id}: start_day {start} is after opens_day {dp.opens_day}")
        if start not in beats:
            raise ValueError(f"episode {spec.id}: start_day {start} is not a schedule beat")
        if end <= start:
            raise ValueError(f"episode {spec.id}: end_day {end} must be after start_day {start}")
        if dp is not None and end <= dp.deadline_day:
            raise ValueError(f"episode {spec.id}: end_day {end} must be after deadline_day {dp.deadline_day}")
        sessions = resolve_sessions(spec, schedule, start_day=start, end_day=end)
        if not sessions:
            raise ValueError(f"episode {spec.id}: sessions must not be empty")
        if sessions != sorted(set(sessions)) or any(not (start < d <= end) for d in sessions):
            raise ValueError(f"episode {spec.id}: sessions {sessions} must be ascending, unique and inside ({start}, {end}]")
        if sessions[-1] != end:
            raise ValueError(f"episode {spec.id}: last session must equal end_day {end}")
        if dp is not None and dp.deadline_day not in sessions:
            raise ValueError(f"episode {spec.id}: sessions must contain deadline_day {dp.deadline_day}")
        arms = [_as_episode_arm(a) for a in spec.arms] if spec.arms else [EpisodeArm(id=manifest.meta.default_arm)]
        ids = [a.id for a in arms]
        if len(ids) != len(set(ids)):
            raise ValueError(f"episode {spec.id}: duplicate arm id in {ids}")
        if manifest.meta.default_arm not in ids:
            raise ValueError(f"episode {spec.id}: no arm named the default arm {manifest.meta.default_arm!r}")
        shared_actions = [_as_prelude_action(a) for a in manifest.meta.shared_prelude_actions]
        own_actions = [_as_prelude_action(a) for a in spec.prelude_actions]
        arm_actions = [_as_prelude_action(a) for arm in arms for a in arm.prelude_actions]
        for action in [*shared_actions, *own_actions, *arm_actions]:
            if action in shared_actions and action.day >= start:
                continue  # a shared action after this episode's start simply does not apply to it
            if action.day >= start:
                raise ValueError(f"episode {spec.id}: prelude action day {action.day} must be before start_day {start}")
            if action.day not in beats:
                raise ValueError(f"episode {spec.id}: prelude action day {action.day} is not a schedule beat")


@dataclass(frozen=True)
class ResolvedEpisode:
    """One playable sample: an episode × arm with every default applied.

    Every decision point is on the ledger (the env runs with `enabled_nodes=None`); `dp_id` names
    the ONE the judge scores (`scored_nodes` in `grade_episode`).
    """

    episode_id: str
    arm_id: str
    dp_id: str | None
    start_day: int
    end_day: int
    sessions: list[int]
    scored: bool
    welfare_pass_min: float
    prelude_actions: tuple[PreludeAction, ...]
    digest_note: str | None
    ablation_overrides: dict[str, str] | None
    expected_degenerate_channels: tuple[str, ...]
    # The nodes whose latent-signal wakes may cap this episode's clock: the scored node first,
    # then the manifest's `wake_nodes`; empty for a quiet episode.
    wake_nodes: tuple[str, ...] = ()

    @property
    def sample_id(self) -> str:
        return f"{self.episode_id}::{self.arm_id}"

    def to_store_dict(self, *, opening_digest: str) -> dict:
        """The per-sample facts the adapter keeps in `EpisodeStore.episode_spec` (D5)."""
        return {
            "episode_id": self.episode_id,
            "arm_id": self.arm_id,
            "dp_id": self.dp_id,
            "start_day": self.start_day,
            "end_day": self.end_day,
            "sessions": list(self.sessions),
            "scored": self.scored,
            "welfare_pass_min": self.welfare_pass_min,
            "ablation_overrides": dict(self.ablation_overrides) if self.ablation_overrides else None,
            "wake_nodes": list(self.wake_nodes),
            "opening_digest": opening_digest,
        }


def expand_episodes(manifest: NodeEpisodeManifest, schedule: Schedule) -> list[ResolvedEpisode]:
    """Manifest -> one ResolvedEpisode per (episode, arm), in manifest order (default arm first
    within an episode only if authored first — order is the author's)."""
    out: list[ResolvedEpisode] = []
    for spec in manifest.episodes:
        start, end = _window(spec, schedule)
        sessions = resolve_sessions(spec, schedule, start_day=start, end_day=end)
        shared = [_as_prelude_action(a) for a in manifest.meta.shared_prelude_actions if a.day < start]
        own_actions = [_as_prelude_action(a) for a in spec.prelude_actions]
        arms = [_as_episode_arm(a) for a in spec.arms] if spec.arms else [EpisodeArm(id=manifest.meta.default_arm)]
        for arm in arms:
            arm_actions = [_as_prelude_action(a) for a in arm.prelude_actions]
            out.append(
                ResolvedEpisode(
                    episode_id=spec.id,
                    arm_id=arm.id,
                    dp_id=spec.dp_id,
                    start_day=start,
                    end_day=end,
                    sessions=list(sessions),
                    scored=spec.kind == "node",
                    welfare_pass_min=(
                        spec.welfare_pass_min if spec.welfare_pass_min is not None else manifest.meta.welfare_pass_min
                    ),
                    prelude_actions=tuple(sorted([*shared, *own_actions, *arm_actions], key=lambda a: a.day)),
                    digest_note=arm.digest_note,
                    ablation_overrides=arm.ablation_overrides,
                    expected_degenerate_channels=tuple(spec.expected_degenerate_channels),
                    wake_nodes=tuple(
                        dict.fromkeys([*([spec.dp_id] if spec.dp_id else []), *spec.wake_nodes])
                    ),
                )
            )
    return out


def find_episode(resolved: list[ResolvedEpisode], episode_id: str, arm_id: str) -> ResolvedEpisode:
    for r in resolved:
        if r.episode_id == episode_id and r.arm_id == arm_id:
            return r
    raise KeyError(f"no episode {episode_id!r} with arm {arm_id!r} in the manifest")
