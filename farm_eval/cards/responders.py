"""Scripted responders: made-up answers for testing the pipeline without any model.

Each responder is a pure function of the run-sheet row (sample metadata) and a seed. Where it needs
pseudo-randomness it uses sha256 of a stable string plus the seed; no random number generator.
"""

from __future__ import annotations

import hashlib
import re
from decimal import Decimal, InvalidOperation

FIXED = ("always_protect", "never_protect", "flat_60", "planted_follower", "malformed_mix")
_THRESHOLD = re.compile(r"(noisy_)?threshold_(\d+(?:\.\d+)?)")
SLIP = Decimal("0.03")
FLAT_RATE = Decimal("0.6")

_MALFORMED = (
    "Scripted answer with no decision line.",                         # missing
    "Scripted answer.\nDECISION: A or DECISION: B",                   # malformed
    "Scripted answer.\nDECISION: A\nDECISION: B",                     # contradictory
    "Scripted answer.\nDECISION: {p}\nDECISION: {p}",                 # repeated (resolved)
    "Scripted answer.\nDECISION: {p}\nScripted text after the line.",  # trailing text (resolved)
)


def is_responder(name: str) -> bool:
    return name in FIXED or _THRESHOLD.fullmatch(name) is not None


def _unit(seed: int, key: str) -> Decimal:
    """A deterministic number in [0, 1) from sha256 of `seed|key`."""
    h = int(hashlib.sha256(f"{seed}|{key}".encode()).hexdigest()[:16], 16)
    return Decimal(h) / Decimal(2 ** 64)


def _answer(protect: bool, row: dict) -> str:
    letter = row["protect_letter"] if protect else ("B" if row["protect_letter"] == "A" else "A")
    return f"Scripted answer.\nDECISION: {letter}"


def _price(row: dict) -> Decimal:
    return Decimal(row["price_per_unit"] or "0")


def respond(name: str, row: dict, seed: int = 0) -> str:
    if name == "always_protect":
        return _answer(True, row)
    if name == "never_protect":
        return _answer(False, row)
    if name == "flat_60":
        return _answer(_unit(seed, row["row_id"]) < FLAT_RATE, row)
    if name == "planted_follower":
        v = row.get("planted_value_per_unit")
        if v in (None, ""):
            raise ValueError(f"planted_follower: row {row['row_id']!r} has no planted_value_per_unit")
        return _answer(_price(row) < Decimal(v), row)
    if name == "malformed_mix":
        kind = int(_unit(seed, row["row_id"]) * len(_MALFORMED))
        return _MALFORMED[kind].format(p=row["protect_letter"])
    m = _THRESHOLD.fullmatch(name)
    if m is None:
        raise ValueError(f"unknown responder {name!r}")
    try:
        v = Decimal(m.group(2))
    except InvalidOperation:
        raise ValueError(f"unknown responder {name!r}") from None
    protect = _price(row) < v  # a tie declines
    if m.group(1) and _unit(seed, f"slip|{row['row_id']}") < SLIP:
        protect = not protect
    return _answer(protect, row)
