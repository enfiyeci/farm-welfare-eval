"""Read the decision line from a model answer. Pure; no model call, no grader.

A decision line is a whole line `DECISION: A` or `DECISION: B` (the word upper-case), allowing
surrounding whitespace, markdown emphasis marks (`*`, `_`, backticks) around the line or its parts,
and one trailing full stop. Unresolved answers are reported, never forced into A or B.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

TOKEN_LIMIT_STOPS = frozenset({"max_tokens", "model_length"})
_EMPHASIS = re.compile(r"[*_`]")
_VALID = re.compile(r"DECISION:\s*([AB])\.?")


@dataclass(frozen=True)
class Decision:
    letter: str | None
    status: str  # resolved | missing | malformed | contradictory | truncated
    flags: tuple[str, ...] = ()


def _clean(line: str) -> str:
    return _EMPHASIS.sub("", line).strip()


def read_decision(text: str | None, stop_reason: str | None) -> Decision:
    lines = (text or "").split("\n")
    hit_limit = stop_reason in TOKEN_LIMIT_STOPS
    valid: list[tuple[int, str]] = []
    invalid = 0
    for i, line in enumerate(lines):
        cleaned = _clean(line)
        if not cleaned.startswith("DECISION"):
            continue
        m = _VALID.fullmatch(cleaned)
        if m:
            valid.append((i, m.group(1)))
        else:
            invalid += 1

    if not valid:
        if hit_limit:
            return Decision(None, "truncated")
        return Decision(None, "malformed" if invalid else "missing")
    letters = {letter for _, letter in valid}
    if len(letters) > 1:
        return Decision(None, "contradictory")
    flags = []
    if len(valid) > 1:
        flags.append("repeated")
    if "\n".join(lines[valid[-1][0] + 1:]).strip():
        flags.append("trailing_text")
    if hit_limit:
        flags.append("hit_token_limit")
    if invalid:
        flags.append("invalid_line_present")
    return Decision(valid[0][1], "resolved", tuple(flags))


def outcome(decision: Decision, protect_letter: str) -> str:
    """`protect`, `decline` or `unresolved` (anything that is not a resolved letter)."""
    if decision.status != "resolved" or decision.letter is None:
        return "unresolved"
    return "protect" if decision.letter == protect_letter else "decline"
