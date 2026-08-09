"""Live rendering of a sweep as it runs.

A sweep is hundreds of calls over many minutes, and the interesting behaviour is in
the replies, not the final table. This turns each call into one readable block so a
run can be followed while it happens.

Presentation only. It never touches what is recorded, and it is not scoring — the
reasoning shown here is raw model text, to be read, not counted.
"""
from __future__ import annotations

import sys
from typing import Any, TextIO

from farm_eval.study.response import Decision

_MARK = {
    Decision.ACCEPT: "ACCEPT ",
    Decision.DECLINE: "DECLINE",
    Decision.UNPARSEABLE: "UNPARSE",
}


def _reasoning(response: str, limit: int) -> str:
    """The reply minus its DECISION line, collapsed to one line and clipped."""
    body = " ".join(
        line.strip() for line in response.splitlines()
        if line.strip() and not line.strip().lstrip("*").strip().upper().startswith("DECISION:")
    )
    return body if len(body) <= limit else body[: limit - 1].rstrip() + "…"


def live_line(
    *,
    cell: Any,
    gain: float,
    rung: Any,
    replicate: int,
    offer: Any,
    decision: Decision,
    response: str,
    stream: TextIO | None = None,
    width: int = 150,
) -> None:
    """Print one call. Signature matches run_phase1's `on_call` keyword contract."""
    out = stream or sys.stdout
    deaths_before = offer.n0 * offer.m0
    deaths_after = offer.n1 * offer.m1
    pp = f"+{rung.added_mortality_pp:.1f}pp"
    head = (
        f"[{cell.species.value:6} {cell.scale.value:5} gain +{gain * 100:.0f}% "
        f"| {pp:>8}  "
        f"survival {offer.survival_pct_before:.1f}%->{offer.survival_pct_after:.1f}%  "
        f"mortality {deaths_before:,.0f}->{deaths_after:,.0f}  "
        f"| r{replicate}]"
    )
    print(f"{head}  {_MARK[decision]}", file=out)
    print(f"    {_reasoning(response, width)}", file=out, flush=True)
