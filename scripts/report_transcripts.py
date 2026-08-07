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

from farm_eval.study.cells import Cell  # noqa: E402
from farm_eval.study.offer import build_offer  # noqa: E402
from farm_eval.study.params import Rung  # noqa: E402
from farm_eval.study.prompt import build_p1_prompt  # noqa: E402
from farm_eval.study.results import CellResult, read_jsonl  # noqa: E402


def sample_prompt(result: CellResult, density_step: float) -> str:
    """The exact prompt behind this cell's first rung, so the report shows what the
    model was actually asked, not a paraphrase."""
    rung = Rung(density_step=density_step,
                added_mortality_pp=result.rung_records[0].added_mortality_pp)
    return build_p1_prompt(build_offer(result.cell, rung, result.gain))


def render(results: list[CellResult], density_step: float, title: str) -> str:
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
        sample_prompt(results[0], density_step).rstrip(),
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
                                Rung(density_step=density_step,
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
                lines += [
                    f"**Reply {i + 1} — {decision.value.upper()}**",
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
                        help="the density step the run used (for re-deriving offers)")
    parser.add_argument("--title", default="Run transcripts")
    args = parser.parse_args(argv)

    results = read_jsonl(args.results)
    if not results:
        print(f"no results in {args.results}", file=sys.stderr)
        return 2
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(results, args.density_step, args.title), encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
