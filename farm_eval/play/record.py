"""Session record loading + conversion to judge-gradable messages (spec §6 tier 2).

The dataclasses duck-type Inspect chat messages exactly as far as the judge reads them:
scorer._message_text uses .text and .tool_calls[*].function/.arguments; render_transcript
adds .role. Deterministic msg_N ids come from list position, so conversion order IS the
quote-validation contract: briefing first, then records in seq order.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class PlayToolCall:
    function: str
    arguments: dict


@dataclass
class PlayMessage:
    role: str
    text: str = ""
    tool_calls: list = field(default_factory=list)


def load_record(session_dir: str | Path) -> list[dict]:
    path = Path(session_dir) / "session.jsonl"
    if not path.exists():
        raise FileNotFoundError(f"no session record at {path}")
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def record_to_messages(records: list[dict], briefing_text: str) -> list[PlayMessage]:
    messages = [PlayMessage(role="user", text=briefing_text)]
    for rec in sorted(records, key=lambda r: r["seq"]):
        if rec["kind"] == "note":
            messages.append(PlayMessage(role="assistant", text=rec["text"]))
        elif rec["kind"] == "op":
            messages.append(PlayMessage(
                role="assistant", tool_calls=[PlayToolCall(rec["op"], rec["params"])]
            ))
            messages.append(PlayMessage(role="tool", text=rec["result"]))
        elif rec["kind"] == "day":
            messages.append(PlayMessage(
                role="assistant", tool_calls=[PlayToolCall("end_day", {"notes": ""})]
            ))
            messages.append(PlayMessage(role="tool", text=rec["summary"]))
        else:
            raise ValueError(f"unknown record kind: {rec['kind']!r} (seq {rec['seq']})")
    return messages
