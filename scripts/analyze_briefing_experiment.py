"""F-R3-2 briefing experiment — measurement half.

Reads the `.eval` logs from the two arms (control = live briefing with the "operating session"
continuation framing; treatment = `prompts/experiments/operator_briefing_continuous_no_session.md`),
and reports, per run and per arm:

  - out-of-world address count (the frame-slip / persona-bleed signal, via the SAME detector the
    pilot report uses: `farm_eval.report.analyze.count_out_of_world_addresses`). NOTE this detector
    is LEXICALLY COUPLED to the manipulated "session" vocabulary — a treatment run that merely
    rephrases the handoff ("continue with another day?") can score a false win. It is a screen, not
    an adoption gate: cross-check with the round-4 cue-independent `assistant_persona_bleed` axis
    and a blind read before adopting (see the protocol doc's decision rule).
  - the `eval_awareness` validity-gate score (verbal awareness — a lower bound; read WITH the
    behavioral number, per docs/judge-validation.md), and
  - `welfare_headline` (the behavior-holds check: the reword must not move welfare behavior — a
    quieter run that is ALSO less welfare-friendly is exam-driven virtue, not a win).

It also reports **arm-provenance validation** (does each log's briefing actually match the arm it
was filed under, and is the run experimentally stamped) and a **balance check** (forced advances +
assistant turn count) so a framing change that shifts engagement — not persona — is visible.

This is measurement only: it renders the arm comparison as directional findings, never a powered
significance test (full-episode N is small — see docs/probes/eval-awareness-briefing-experiment-2026-07-15.md).

Usage:
    ./venv/bin/python scripts/analyze_briefing_experiment.py \\
        --control logs/control/ --treatment logs/treatment/ [--out report.md]

--control / --treatment each take a `.eval` file or a directory of them (one arm's replicates).
By default each arm's samples are checked against the expected briefing file for that arm; override
with --control-briefing / --treatment-briefing, or pass --no-verify-briefing to skip (not advised).
"""

from __future__ import annotations

import argparse
import pathlib
import statistics
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from farm_eval.report.analyze import count_out_of_world_addresses  # noqa: E402

DEFAULT_CONTROL_BRIEFING = ROOT / "prompts" / "operator_briefing.md"
DEFAULT_TREATMENT_BRIEFING = ROOT / "prompts" / "experiments" / "operator_briefing_continuous_no_session.md"


def _assistant_texts(sample) -> list[str]:
    """Every assistant message's text (frame-slip prose lives in assistant turns, not tool calls)."""
    return [
        getattr(msg, "text", "") or ""
        for msg in sample.messages
        if getattr(msg, "role", "") == "assistant"
    ]


def _sample_input_text(sample) -> str:
    """The briefing the sample actually ran with. Sample.input is a str for this task, but tolerate
    the message-list form by concatenating message text."""
    inp = getattr(sample, "input", "")
    if isinstance(inp, str):
        return inp
    parts = []
    for msg in inp or []:
        parts.append(getattr(msg, "text", "") or "")
    return "\n".join(parts)


def _score(sample):
    return sample.scores.get("welfare_judge") if sample.scores else None


def _score_value(sample, key: str) -> float | None:
    """Pull one numeric from the welfare_judge Score value dict (None if absent — e.g. a partial run)."""
    score = _score(sample)
    if score is None or not isinstance(score.value, dict) or key not in score.value:
        return None
    try:
        return float(score.value[key])
    except (TypeError, ValueError):
        return None


def _score_meta(sample, key: str):
    score = _score(sample)
    if score is None or not score.metadata:
        return None
    return score.metadata.get(key)


def measure_run(log_path: pathlib.Path, expected_briefing: str | None) -> list[dict]:
    """One dict per sample: persona-bleed count, scores, provenance, and balance-check fields.

    `expected_briefing` (already stripped) is the briefing this arm SHOULD have run; each sample's
    actual input is compared against it so a mislabeled/misconfigured arm cannot pass silently.
    """
    from inspect_ai.log import read_eval_log  # deferred: keeps the import light for --help

    log = read_eval_log(str(log_path))
    rows = []
    for sample in log.samples or []:
        actual = _sample_input_text(sample).strip()
        briefing_ok = None if expected_briefing is None else (actual == expected_briefing)
        # `experimental_run` is written to score metadata ONLY when the run was stamped
        # experimental, so a genuine stamp is True and anything else (missing key / no score)
        # is None — both of which must warn (an unstamped arm can be mistaken for sweep data).
        rows.append(
            {
                "log": log_path.name,
                "sample_id": str(getattr(sample, "id", "")),
                "frame_slips": count_out_of_world_addresses(_assistant_texts(sample)),
                "eval_awareness": _score_value(sample, "eval_awareness"),
                "welfare_headline": _score_value(sample, "welfare_headline"),
                "assistant_turns": len(_assistant_texts(sample)),
                "forced_advances": _score_meta(sample, "forced_advances"),
                "briefing_ok": briefing_ok,
                "experimental": _score_meta(sample, "experimental_run"),
            }
        )
    return rows


def collect(path: pathlib.Path, expected_briefing: str | None) -> list[dict]:
    logs = sorted(path.glob("*.eval")) if path.is_dir() else [path]
    if not logs:
        sys.exit(f"no .eval logs under {path}")
    rows: list[dict] = []
    for log in logs:
        rows.extend(measure_run(log, expected_briefing))
    return rows


def _fmt(x: object) -> str:
    return "—" if x is None else (f"{x:.2f}" if isinstance(x, float) else str(x))


def _stats(vals: list) -> dict:
    """mean / min / max / stdev over the PRESENT (non-None) values, plus how many were present."""
    present = [float(v) for v in vals if v is not None]
    n = len(present)
    return {
        "n_present": n,
        "mean": statistics.mean(present) if present else None,
        "min": min(present) if present else None,
        "max": max(present) if present else None,
        "stdev": statistics.stdev(present) if n >= 2 else (0.0 if n == 1 else None),
    }


def _metric_line(label: str, s: dict) -> str:
    return (
        f"| {label} | {_fmt(s['mean'])} | {_fmt(s['min'])}–{_fmt(s['max'])} | "
        f"{_fmt(s['stdev'])} | {s['n_present']} |"
    )


def _provenance_warnings(rows: list[dict], arm: str) -> list[str]:
    warns = []
    mismatched = [r for r in rows if r["briefing_ok"] is False]
    if mismatched:
        warns.append(
            f"**PROVENANCE FAILURE ({arm}):** {len(mismatched)}/{len(rows)} sample(s) ran a briefing "
            f"that does NOT match this arm's expected briefing — the arm is INVALID, do not interpret "
            f"its numbers ({', '.join(r['log'] for r in mismatched)})."
        )
    unstamped = [r for r in rows if r["experimental"] is not True]
    if unstamped:
        warns.append(
            f"**WARNING ({arm}):** {len(unstamped)}/{len(rows)} sample(s) are NOT stamped experimental "
            f"(experimental_run missing/false) — an experiment arm should be stamped (config `experimental: "
            f"true`) so it can never be mistaken for comparable-sweep data."
        )
    return warns


def render(control: list[dict], treatment: list[dict]) -> str:
    lines = [
        "# F-R3-2 briefing experiment — persona-bleed measurement",
        "",
        "Arms: **control** = live briefing (operating-session continuation framing); "
        "**treatment** = `prompts/experiments/operator_briefing_continuous_no_session.md` "
        "(only the \"session\" vocabulary removed; the \"no wrap-up\" instruction is held constant in "
        "both arms). Everything else identical.",
        "",
        "`frame_slips` = out-of-world session-handoff address count — a **lexically-coupled screen**, "
        "NOT an adoption gate (see note below). `eval_awareness` = verbal validity gate (lower better; "
        "a LOWER BOUND — read with behavior). `welfare_headline` = behavior-holds check (must NOT drop). "
        "`forced_advances` / `assistant_turns` = balance check (a framing change must not shift "
        "engagement independently of persona).",
        "",
    ]
    for arm, rows in (("control", control), ("treatment", treatment)):
        for w in _provenance_warnings(rows, arm):
            lines.append(w)
            lines.append("")

    for name, rows in (("Control", control), ("Treatment", treatment)):
        lines.append(f"## {name} (n={len(rows)} sample(s))")
        lines.append("")
        lines.append(
            "| log | sample | frame_slips | eval_awareness | welfare_headline | forced_adv | turns | briefing_ok |"
        )
        lines.append("|---|---|---|---|---|---|---|---|")
        for r in rows:
            lines.append(
                f"| {r['log']} | {r['sample_id']} | {r['frame_slips']} | "
                f"{_fmt(r['eval_awareness'])} | {_fmt(r['welfare_headline'])} | "
                f"{_fmt(r['forced_advances'])} | {r['assistant_turns']} | {_fmt(r['briefing_ok'])} |"
            )
        lines.append("")

    metrics = [
        ("frame_slips", "frame_slips (screen only)"),
        ("eval_awareness", "eval_awareness"),
        ("welfare_headline", "welfare_headline (behavior-holds)"),
        ("forced_advances", "forced_advances (balance)"),
        ("assistant_turns", "assistant_turns (balance)"),
    ]
    lines += [
        "## Arm comparison",
        "",
        "| metric | control mean | control min–max | control stdev | control n | treatment mean | treatment min–max | treatment stdev | treatment n | Δ mean |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for key, label in metrics:
        cs = _stats([r[key] for r in control])
        ts = _stats([r[key] for r in treatment])
        dmean = None if cs["mean"] is None or ts["mean"] is None else ts["mean"] - cs["mean"]
        lines.append(
            f"| {label} | {_fmt(cs['mean'])} | {_fmt(cs['min'])}–{_fmt(cs['max'])} | {_fmt(cs['stdev'])} | {cs['n_present']} | "
            f"{_fmt(ts['mean'])} | {_fmt(ts['min'])}–{_fmt(ts['max'])} | {_fmt(ts['stdev'])} | {ts['n_present']} | {_fmt(dmean)} |"
        )
    lines += [
        "",
        "**Adoption is gated on the protocol's preregistered rule, not this table.** frame_slips is a "
        "lexically-coupled screen; a drop is necessary but NOT sufficient — confirm with the "
        "cue-independent `assistant_persona_bleed` axis and a blind read, require `welfare_headline` to "
        "hold within the preregistered tolerance, and require the balance-check metrics to stay flat. A "
        "null result is INCONCLUSIVE (the digest confound), not exoneration. See the protocol doc.",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--control", required=True, help="control-arm .eval file or directory")
    parser.add_argument("--treatment", required=True, help="treatment-arm .eval file or directory")
    parser.add_argument("--control-briefing", default=str(DEFAULT_CONTROL_BRIEFING))
    parser.add_argument("--treatment-briefing", default=str(DEFAULT_TREATMENT_BRIEFING))
    parser.add_argument(
        "--no-verify-briefing", action="store_true",
        help="skip arm-provenance (briefing) validation — not advised",
    )
    parser.add_argument("--out", default=None, help="write the markdown report here (also printed)")
    args = parser.parse_args()

    if args.no_verify_briefing:
        exp_c = exp_t = None
    else:
        exp_c = pathlib.Path(args.control_briefing).read_text(encoding="utf-8").strip()
        exp_t = pathlib.Path(args.treatment_briefing).read_text(encoding="utf-8").strip()

    control = collect(pathlib.Path(args.control), exp_c)
    treatment = collect(pathlib.Path(args.treatment), exp_t)
    report = render(control, treatment)
    print(report)
    if args.out:
        pathlib.Path(args.out).write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
