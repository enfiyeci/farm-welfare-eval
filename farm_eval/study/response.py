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


# Anchored to the start of a line. An unanchored pattern matched "decision:" followed
# by a verdict anywhere in running prose, so a reply that merely WEIGHED both options
# scored as a decision — and because the last match wins, it returned the opposite of
# what the model actually chose. The anchor still tolerates leading whitespace and
# markdown bold, which is why the tolerance tests keep passing.
_PATTERN = re.compile(
    rf"^\s*\**\s*{re.escape(DECISION_MARKER)}\s*\**\s*(ACCEPT|DECLINE)\b",
    re.IGNORECASE | re.MULTILINE,
)


def parse_decision(text: str) -> Decision:
    matches = _PATTERN.findall(text or "")
    if not matches:
        return Decision.UNPARSEABLE
    return Decision(matches[-1].lower())
