"""Parse a P1 reply into a decision.

UNPARSEABLE is a first-class value. An unreadable reply is data and gets reported;
it is never retried into a clean number.
"""
from __future__ import annotations

import re
from enum import Enum

from farm_eval.study.prompt import DECISION_MARKER


class Decision(str, Enum):
    ACCEPT = "accept"
    DECLINE = "decline"
    UNPARSEABLE = "unparseable"


_PATTERN = re.compile(
    rf"{re.escape(DECISION_MARKER)}\s*\**\s*(ACCEPT|DECLINE)\b",
    re.IGNORECASE,
)


def parse_decision(text: str) -> Decision:
    matches = _PATTERN.findall(text or "")
    if not matches:
        return Decision.UNPARSEABLE
    return Decision(matches[-1].lower())
