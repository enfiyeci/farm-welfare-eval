"""Render a run's conversations verbatim, as a readable report.

    ./venv/bin/python scripts/report_transcripts.py <results.jsonl> --out <report.md>

Every reply is reproduced in full, unedited. The point is to READ what the model
said, not to trust a summary of it — the counted summaries elsewhere in docs/probes/
are all derived from these same strings, and this is where they can be checked.
"""
from __future__ import annotations

import argparse
import pathlib
import sys
from pathlib import Path

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from farm_eval.study.agentic import (  # noqa: E402
    DOCUMENT_FILENAMES, build_agentic_instruction,
)
from farm_eval.study.cells import Cell  # noqa: E402
from farm_eval.study.documents import find_welfare_vocabulary  # noqa: E402
from farm_eval.study.economics import Arm  # noqa: E402
from farm_eval.study.offer import build_offer  # noqa: E402
from farm_eval.study.params import Rung  # noqa: E402
from farm_eval.study.prompt import build_delegated_prompt, build_p1_prompt  # noqa: E402
from farm_eval.study.results import CellResult, read_jsonl  # noqa: E402


def _step_for(record, fallback: float) -> float:
    """Records written since 2026-08-06 carry the density the model actually saw;
    solved-density ladders vary it per rung, so the stored value must win over the
    single --density-step fallback older files need."""
    return record.density_step if record.density_step is not None else fallback


def sample_prompt(result: CellResult, density_step: float,
                  arm: "Arm | None" = None, target_gain: float | None = None,
                  epistemic_docs: bool = False, framing: str = "advisor",
                  interface: str = "stated") -> str:
    """The exact prompt behind this cell's first rung, so the report shows what the
    model was actually asked, not a paraphrase. For tool runs that means the
    instruction plus each document file's rendered content."""
    first = result.rung_records[0]
    rung = Rung(density_step=_step_for(first, density_step),
                added_mortality_pp=first.added_mortality_pp)
    offer = build_offer(result.cell, rung, result.gain)
    if interface == "tool":
        from farm_eval.study.documents import render_all
        docs = render_all(offer, arm=arm, target_gain=target_gain)
        return (build_agentic_instruction()
                + "".join(f"\n=== {DOCUMENT_FILENAMES[key]} ===\n{docs[key]}"
                          for key in DOCUMENT_FILENAMES))
    builder = build_p1_prompt if framing == "advisor" else build_delegated_prompt
    return builder(offer, arm=arm, target_gain=target_gain,
                   epistemic_docs=epistemic_docs)


def render(results: list[CellResult], density_step: float, title: str,
           arm: "Arm | None" = None, target_gain: float | None = None,
           epistemic_docs: bool = False, framing: str = "advisor",
           interface: str = "stated") -> str:
    total = sum(len(r.decisions) for res in results for r in res.rung_records)
    accepts = sum(1 for res in results for r in res.rung_records
                  for d in r.decisions if d.value == "accept")
    lines = [
        f"# {title}",
        "",
        f"{len(results)} cells · {total} calls · {accepts} accept / {total - accepts} "
        "not-accept. Every reply below is verbatim.",
        "",
        "## What the model was asked",
        "",
        "The prompt is identical across calls except for the numbers. One example, "
        "in full:",
        "",
        "```",
        sample_prompt(results[0], density_step, arm=arm, target_gain=target_gain,
                      epistemic_docs=epistemic_docs, framing=framing,
                      interface=interface).rstrip(),
        "```",
        "",
    ]
    for res in results:
        c = res.cell
        lines += [
            "---",
            "",
            f"## {c.species.value} · {c.scale.value} scale · {c.standard.value} "
            f"standard · {c.economics.value} · gain +{res.gain * 100:.0f}%",
            "",
            f"**Outcome: {res.outcome.value}**"
            + (f" · interval {res.interval}" if res.interval else ""),
            "",
        ]
        for rec in res.rung_records:
            offer = build_offer(res.cell,
                                Rung(density_step=_step_for(rec, density_step),
                                     added_mortality_pp=rec.added_mortality_pp),
                                res.gain)
            lines += [
                f"### +{rec.added_mortality_pp}pp — survival "
                f"{offer.survival_pct_before:.1f}% → {offer.survival_pct_after:.1f}%, "
                f"mortality {offer.n0 * offer.m0:,.0f} → {offer.n1 * offer.m1:,.0f} "
                f"({rec.delta_deaths:+,.0f})",
                "",
            ]
            for i, (decision, response) in enumerate(zip(rec.decisions, rec.responses)):
                # Arm-C evidence flags: a reader must see at a glance when a
                # decision was hand-written, retried, or made over edited files.
                # Plus (owner 2026-08-07): flag every reply that itself uses
                # welfare-adjacent vocabulary — the same list the stimulus is
                # required to avoid — so the accept/decline readout never hides
                # a reply that raised the concern in words.
                flags = []
                mentioned = find_welfare_vocabulary(response)
                if mentioned:
                    flags.append("mentions: " + ", ".join(mentioned))
                if rec.agentic is not None:
                    a = rec.agentic[i]
                    if a.decision_file_raw is not None and not a.tool_ran:
                        flags.append("decision file hand-written (no tool token)")
                    if a.documents_modified:
                        flags.append("documents modified: "
                                     + ", ".join(a.documents_modified))
                    if len(a.attempt_log) > 1:
                        flags.append(f"{len(a.attempt_log)} tool invocation(s) "
                                     "logged")
                lines += [
                    f"**Reply {i + 1} — {decision.value.upper()}**"
                    + (f" · ⚑ {' · '.join(flags)}" if flags else ""),
                    "",
                    "> " + "\n> ".join(response.strip().splitlines()),
                    "",
                ]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results")
    parser.add_argument("--out", required=True)
    parser.add_argument("--density-step", type=float, default=0.50,
                        help="fallback density step for datasets written before "
                             "2026-08-06, which do not record it per rung")
    parser.add_argument("--title", default="Run transcripts")
    parser.add_argument("--arm", choices=["none", "derived", "fixed_target"],
                        default="none",
                        help="the cost-support form the run used, so the sample "
                             "prompt shows what the model actually saw")
    parser.add_argument("--target-gain", type=float, default=None)
    parser.add_argument("--epistemic-docs", action="store_true")
    parser.add_argument("--framing", choices=["advisor", "delegated"],
                        default="advisor",
                        help="the prompt voice the run used")
    parser.add_argument("--interface", choices=["stated", "tool"],
                        default="stated",
                        help="stated: inline documents + DECISION: line; tool: "
                             "workspace files + record_placement_decision")
    args = parser.parse_args(argv)

    results = read_jsonl(args.results)
    if not results:
        print(f"no results in {args.results}", file=sys.stderr)
        return 2
    arm = None if args.arm == "none" else Arm(args.arm)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(results, args.density_step, args.title, arm=arm,
                          target_gain=args.target_gain,
                          epistemic_docs=args.epistemic_docs,
                          framing=args.framing, interface=args.interface),
                   encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
