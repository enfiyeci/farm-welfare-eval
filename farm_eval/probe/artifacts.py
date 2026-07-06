"""Probe input surface: corpus documents, the operator briefing, and deterministic
rendered read-tool samples (spec §3 P2). Read-only — never mutates corpus or schedule."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict

from farm_eval.env.episode import FarmEnv
from farm_eval.env.loader import load_corpus


class Artifact(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    kind: Literal["email", "document", "briefing", "rendered"]
    text: str


def enumerate_corpus_artifacts(corpus_path: str | Path, briefing_path: str | Path) -> list[Artifact]:
    """Every authored corpus document plus the briefing, in deterministic order.

    Fails loud if a corpus document key collides with a reserved id namespace (`briefing`,
    `rendered/*`) or duplicates another artifact's id — later tasks pair probe results back
    by artifact id, so a silent collision would mis-pair results.
    """
    corpus = load_corpus(corpus_path)
    arts = [
        Artifact(
            id=key,
            kind="email" if key.startswith("emails/") else "document",
            text=text,
        )
        for key, text in sorted(corpus.documents.items())
    ]
    briefing_text = Path(briefing_path).read_text(encoding="utf-8")
    arts.append(Artifact(id="briefing", kind="briefing", text=briefing_text))

    seen: set[str] = set()
    for art in arts:
        if art.kind != "briefing" and (art.id == "briefing" or art.id.startswith("rendered/")):
            raise ValueError(f"corpus document id {art.id!r} collides with a reserved id namespace (briefing/rendered/*)")
        if art.id in seen:
            raise ValueError(f"duplicate artifact id {art.id!r}")
        seen.add(art.id)
    return arts


def rendered_samples(
    corpus_path: str | Path,
    schedule_path: str | Path,
    *,
    days: tuple[int, ...] = (30, 120),
    house_id: str = "H4",
    episode_end_day: int | None = None,
) -> list[Artifact]:
    """Deterministic read-tool outputs at fixed days under the default (no-action) policy.
    The env core is deterministic, so two calls yield byte-identical artifacts.

    `FarmEnv.end_day()` jumps to the next SCHEDULED BEAT, not the next calendar day (see
    farm_eval/env/clock.py:next_beat), so requested `days` are lower bounds, not exact labels:
    each artifact id carries the ACTUAL day the env reached at-or-past the request (a beat jump
    can overshoot). If two requested days land on the same actual beat, they collapse to one
    pair of artifacts. A no-progress guard stops once the episode horizon is reached, so an
    unreachable target never loops forever — its artifacts are labeled with the final day.

    Rendered the way the tool layer renders them (json.dumps of the returned dict — see
    farm_eval/adapter/tools/controller.py:read_flock_report and finance.py:generate_cop_report),
    so the probe judges the same text the agent would have seen.
    """
    horizon = episode_end_day if episode_end_day is not None else max(days)
    env = FarmEnv.from_paths(corpus_path, schedule_path, episode_end_day=horizon, seed=0)
    env.start()
    out: list[Artifact] = []
    seen_actual_days: set[int] = set()
    targets = sorted(set(days))
    for target in targets:
        while env.current_day() < target:
            result = env.end_day()
            if result.elapsed_days == 0:
                break  # horizon reached — no further beats to advance to
        actual_day = env.current_day()
        if actual_day in seen_actual_days:
            continue  # dedupe: an earlier target already landed on this same actual beat
        seen_actual_days.add(actual_day)
        flock = env.read_flock_report(house_id)
        cop = env.generate_cop_report(house_id)
        out.append(
            Artifact(
                id=f"rendered/flock_report/{house_id}/day{actual_day}", kind="rendered", text=json.dumps(flock)
            )
        )
        out.append(
            Artifact(id=f"rendered/cop_report/{house_id}/day{actual_day}", kind="rendered", text=json.dumps(cop))
        )
    return out
