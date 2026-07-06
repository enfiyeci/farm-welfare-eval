"""P1 — tells taxonomy loader (spec §3 P1). Data, not logic: the classes live in
data/tells.yml; this module only validates and exposes them."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, field_validator

_PACKAGED = Path(__file__).parent / "data" / "tells.yml"


class TellClass(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    description: str
    severity: Literal["high", "medium", "low"]
    examples: list[str]

    @field_validator("examples")
    @classmethod
    def _at_least_two(cls, v: list[str]) -> list[str]:
        if len(v) < 2:
            raise ValueError("each tell class needs >=2 generic examples")
        return v


def load_taxonomy(path: str | Path | None = None) -> list[TellClass]:
    """The packaged taxonomy (path=None) or a caller-supplied tells.yml. Fails loud on
    duplicate ids or unknown keys — a taxonomy typo must never silently weaken the probe."""
    raw = yaml.safe_load(Path(path or _PACKAGED).read_text(encoding="utf-8")) or {}
    classes = [TellClass.model_validate(c) for c in raw.get("classes", [])]
    if not classes:
        raise ValueError("tells.yml has no classes")
    ids = [c.id for c in classes]
    if len(ids) != len(set(ids)):
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        raise ValueError(f"tells.yml has duplicate class ids: {dupes}")
    return classes
