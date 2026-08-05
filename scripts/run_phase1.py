"""Run the phase-1 stated-preference sweep.

    ./venv/bin/python scripts/run_phase1.py --out docs/probes/phase1-surface.jsonl

--dry-run uses a deterministic fake model and makes no network or CLI calls.
"""
from __future__ import annotations

import argparse
import math
import sys
import pathlib
from pathlib import Path

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from farm_eval.study.cells import framing_cells  # noqa: E402
from farm_eval.study.documents import parse_survival_projections  # noqa: E402
from farm_eval.study.params import GAIN_LADDER  # noqa: E402
from farm_eval.study.phase1 import run_phase1  # noqa: E402
from farm_eval.study.provider import CodexProvider, FakeProvider  # noqa: E402
from farm_eval.study.results import dump_jsonl_line  # noqa: E402
from farm_eval.study.sweep import SweepRules  # noqa: E402


def _fake_responder(prompt: str) -> str:
    before, after = parse_survival_projections(prompt)
    return "DECISION: ACCEPT" if (before - after) <= 1.2 else "DECISION: DECLINE"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Track D phase-1 sweep")
    parser.add_argument("--out", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--model", default="gpt-5.6-terra")
    parser.add_argument("--limit-cells", type=int, default=None)
    parser.add_argument("--gains", nargs="*", type=float, default=None)
    args = parser.parse_args(argv)

    out = Path(args.out)
    if out.is_dir():
        print(f"--out must be a file path, not a directory: {out}")
        return 2
    if args.limit_cells is not None and args.limit_cells < 1:
        print(f"--limit-cells must be >= 1, got {args.limit_cells}", file=sys.stderr)
        return 2

    provider = (FakeProvider(_fake_responder) if args.dry_run
                else CodexProvider(model=args.model))
    cells = framing_cells()[: args.limit_cells] if args.limit_cells is not None else None
    if args.gains is not None and not args.gains:
        # A shell-expanded empty variable must not silently become the full
        # ladder and launch a live sweep nobody asked for.
        print("--gains was given with no values; omit the flag to run the "
              f"preregistered ladder {list(GAIN_LADDER)}", file=sys.stderr)
        return 2
    gains = args.gains if args.gains is not None else list(GAIN_LADDER)
    if any(not math.isfinite(g) or g <= 0 for g in gains):
        # A non-positive gain renders "improve unit cycle profit by -50.0%":
        # declining becomes financially superior and the instrument inverts.
        # nan/inf slip past a bare `g <= 0` and render a meaningless offer.
        print(f"--gains must be positive and finite, got {gains}", file=sys.stderr)
        return 2
    if args.gains and not all(g in GAIN_LADDER for g in args.gains):
        print(
            f"warning: --gains {args.gains} deviates from the preregistered "
            f"GAIN_LADDER {list(GAIN_LADDER)}",
            file=sys.stderr,
        )

    # Write each cell result as it completes: a provider failure late in the
    # sweep must not cost the results already gathered.
    out.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with out.open("w", encoding="utf-8") as fh:
        def persist(result) -> None:
            nonlocal count
            fh.write(dump_jsonl_line(result))
            fh.flush()
            count += 1

        run_phase1(
            provider,
            cells=cells,
            gains=gains,
            rules=SweepRules(),
            on_result=persist,
        )
    print(f"wrote {count} cell results to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
