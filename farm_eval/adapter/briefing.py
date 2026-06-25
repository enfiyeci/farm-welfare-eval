"""Load the neutral operator briefing (world-bible §2) used as the sample input/system message.

The briefing deliberately omits any mention of evaluation, welfare scoring, or ethics — the
neutrality is the instrument. It is authored content (a fixed file), not computed.
"""

from __future__ import annotations

from pathlib import Path


def load_briefing(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8").strip()
