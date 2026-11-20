"""Run the two cost-support arms over the preregistered ladder.

    ./venv/bin/python scripts/run_cost_support_arms.py --arm derived --out <a.jsonl>
    ./venv/bin/python scripts/run_cost_support_arms.py --arm fixed_target --out <b.jsonl>

Arm DERIVED       — the profit gain is computed from the P&L and varies by rung.
Arm FIXED_TARGET  — the gain is held at --target-gain by solving one cost line.

Both render a profit-and-loss the reader can check (economics.py). The comparison is
the point: if the arms behave alike, the fixed-target form is safe to use and keeps
mortality as the only varying quantity. If FIXED_TARGET draws suspicion DERIVED does
not, the model is detecting a number that always lands neatly — itself a finding.

The PREREGISTERED ladder is used, not the extended one. Under a real cost model every
preregistered rung is profitable (+6% to +34%), while the extended ladder's high rungs
are loss-making, where profit and welfare both say decline and there is no trade to
observe.
"""
from __future__ import annotations

import argparse
import pathlib
import sys
from pathlib import Path

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from farm_eval.study.cells import (  # noqa: E402
    Cell, Economics, Scale, Species, StandardBand,
)
from farm_eval.study.economics import Arm, gain_for, viable_rung  # noqa: E402
from farm_eval.study.offer import build_offer  # noqa: E402
from farm_eval.study.params import rungs_for  # noqa: E402
from farm_eval.study.phase1 import run_phase1  # noqa: E402
from farm_eval.study.prompt import build_p1_prompt  # noqa: E402
from farm_eval.study.provider import CodexProvider, FakeProvider  # noqa: E402
from farm_eval.study.results import dump_jsonl_line  # noqa: E402
from farm_eval.study.sweep import SweepRules  # noqa: E402
from farm_eval.study.watch import live_line  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--arm", required=True, choices=[a.value for a in Arm])
    parser.add_argument("--out", required=True)
    parser.add_argument("--target-gain", type=float, default=0.08)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--model", default="gpt-5.6-terra")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)

    arm = Arm(args.arm)
    if not 0.0 < args.target_gain:
        print("--target-gain must be positive", file=sys.stderr)
        return 2
    out = Path(args.out)
    if out.is_dir():
        print(f"--out must be a file path, not a directory: {out}", file=sys.stderr)
        return 2

    cells = [Cell(species=sp, scale=Scale.LARGE, standard=band,
                  economics=Economics.EQUALIZED)
             for sp in Species for band in StandardBand]

    print(f"arm: {arm.value}"
          + (f"  target gain +{args.target_gain * 100:.0f}%"
             if arm is Arm.FIXED_TARGET else "  (gain derived per rung)"))
    for cell in cells:
        gains = [gain_for(build_offer(cell, r, args.target_gain))
                 for r in rungs_for(cell.species, cell.standard)]
        viable = all(viable_rung(build_offer(cell, r, args.target_gain))
                     for r in rungs_for(cell.species, cell.standard))
        print(f"  {cell.species.value:7} {cell.standard.value:7} "
              f"derived gains {[f'{g * 100:+.0f}%' for g in gains]}"
              f"{'' if viable else '   <-- CONTAINS A LOSS-MAKING RUNG'}")

    provider = (FakeProvider(lambda p: "DECISION: ACCEPT") if args.dry_run
                else CodexProvider(model=args.model))

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
            gains=[args.target_gain],
            rules=SweepRules(),
            on_result=persist,
            on_call=None if args.quiet else live_line,
            prompt_builder=lambda offer: build_p1_prompt(
                offer, arm=arm, target_gain=args.target_gain),
        )
    print(f"wrote {count} cell results to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
