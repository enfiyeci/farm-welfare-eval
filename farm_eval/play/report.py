"""Tier-1 mechanical report card for a play session (spec §6): pure computation over the
final EnvState — ledger outcomes, mechanical tripwires, Layer-1 welfare-state position.

Human results are ADVISORY, never sweep-comparable (spec §6 hard rule): the banner is part of
the contract, not decoration. The judge (tier 2) merges into this via scripts/score_session.py.
"""

from __future__ import annotations


def build_report(env_state, *, actor: str = "human") -> str:
    # Lazy imports: farm_eval/judge/scorer.py imports inspect_ai at module level; the play
    # package stays import-light so PlaySession works without Inspect installed-but-broken envs.
    from farm_eval.judge.scorer import compute_welfare_state, ledger_tripwires

    lines = [
        "# Play-session report card",
        "",
        f"> **actor: {actor} — advisory; never comparable to model sweep results.**",
        "",
        "## Decision outcomes (mechanical ledger)",
        "",
        "| decision | status | outcome | tripwire |",
        "|---|---|---|---|",
    ]
    for entry in env_state.ledger:
        lines.append(
            f"| {entry.dp_id} | {entry.status.value} | {entry.outcome!r} | {entry.tripwire} |"
        )
    if not env_state.ledger:
        lines.append("| (no decisions opened) | | | |")

    trips = ledger_tripwires(env_state)
    lines += ["", "## Mechanical tripwires", ""]
    lines += [f"- {t}" for t in trips] or ["- none"]

    ws = compute_welfare_state(env_state)
    lines += [
        "", "## Layer-1 welfare state (position between neglect floor 0 and gold ceiling 1)", "",
        f"- overall: **{ws['score']:.3f}**",
    ]
    for channel, sub in sorted(ws["channels"].items()):
        lines.append(f"- {channel}: {sub:.3f}")
    lines += [
        "",
        "_Judged dimensions and per-decision rubric scores require the tier-2 judge pass:_",
        "_`./venv/bin/python scripts/score_session.py <session-dir> --model <grader>`_",
    ]
    return "\n".join(lines) + "\n"
