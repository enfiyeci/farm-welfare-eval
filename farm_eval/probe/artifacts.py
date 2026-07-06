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
    """Every authored corpus document plus the briefing, in deterministic order."""
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
    return arts


def rendered_samples(
    corpus_path: str | Path,
    schedule_path: str | Path,
    *,
    days: tuple[int, ...] = (30, 120),
    house_id: str = "H4",
) -> list[Artifact]:
    """Deterministic read-tool outputs at fixed days under the default (no-action) policy.
    The env core is deterministic, so two calls yield byte-identical artifacts.

    Rendered the way the tool layer renders them (json.dumps of the returned dict — see
    farm_eval/adapter/tools/controller.py:read_flock_report and finance.py:generate_cop_report),
    so the probe judges the same text the agent would have seen.
    """
    horizon = max(days)
    env = FarmEnv.from_paths(corpus_path, schedule_path, episode_end_day=horizon, seed=0)
    env.start()
    out: list[Artifact] = []
    day = 0
    targets = sorted(set(days))
    for target in targets:
        while day < target:
            env.end_day()
            day += 1
        flock = env.read_flock_report(house_id)
        cop = env.generate_cop_report(house_id)
        out.append(
            Artifact(id=f"rendered/flock_report/{house_id}/day{target}", kind="rendered", text=json.dumps(flock))
        )
        out.append(
            Artifact(id=f"rendered/cop_report/{house_id}/day{target}", kind="rendered", text=json.dumps(cop))
        )
    return out
