"""Judge dimensions: one markdown file per dimension (YAML frontmatter + body), so a dimension
is added without touching scorer code (à la PETRI). Frontmatter is the machine-readable rubric
(id/group/weight/scale/anchors/tripwire); the body is the grader instructions for that dimension.
"""

from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, Field


class JudgeDimension(BaseModel):
    # extra="forbid": a stray frontmatter key is a rubric-authoring error, not silently ignored.
    model_config = ConfigDict(extra="forbid")

    id: str
    group: str = "welfare"  # welfare | integrity | validity | tripwire (organizes the score view)
    weight: float = 1.0  # 0 for non-pointed dims (tripwires, validity gates)
    scale: tuple[int, int] = (0, 10)
    tripwire: bool = False  # binary hard-fail dimension, not weighted points
    anchors: dict[int, str] = Field(default_factory=dict)
    instructions: str = ""  # the markdown body — the per-dimension grader prompt
    # P4 cue-localization: extra string fields this dimension asks the grader to emit
    # alongside score/quote/message_id (e.g. trigger_type/artifact for eval_awareness).
    # Diagnostic pass-through only — never validated against a vocabulary here (the
    # vocabulary is authored in the dimension body), never in the headline.
    extra_fields: tuple[str, ...] = ()

    @classmethod
    def from_markdown(cls, text: str) -> "JudgeDimension":
        front, body = _split_frontmatter(text)
        data = yaml.safe_load(front) or {}
        data["instructions"] = body.strip()
        return cls.model_validate(data)


def _split_frontmatter(text: str) -> tuple[str, str]:
    stripped = text.lstrip()
    if not stripped.startswith("---"):
        raise ValueError("dimension file must start with a '---' YAML frontmatter block")
    # split on the frontmatter fences: --- <yaml> --- <body>
    rest = stripped[3:]
    end = rest.find("\n---")
    if end == -1:
        raise ValueError("dimension frontmatter is not closed with '---'")
    front = rest[:end]
    body = rest[end + 4 :]
    return front, body


def load_dimensions(directory: str | Path) -> list[JudgeDimension]:
    base = Path(directory)
    dims = [JudgeDimension.from_markdown(f.read_text(encoding="utf-8")) for f in sorted(base.glob("*.md"))]
    if not dims:
        # An empty/bad dimensions dir must fail loudly — never reach the scorer as an empty rubric
        # that would collapse to a plausible zero headline.
        raise ValueError(f"no judge dimension files (*.md) found in {base}")
    ids = [d.id for d in dims]
    if len(ids) != len(set(ids)):
        raise ValueError(f"duplicate judge dimension ids: {ids}")
    return dims
