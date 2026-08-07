"""The delegation arms: the manager hands the call over — stated, or executed.

    ./venv/bin/python scripts/run_delegated_ladder.py --interface stated --out b.jsonl
    ./venv/bin/python scripts/run_delegated_ladder.py --interface tool   --out c.jsonl

Same constant-cushion ladder as experiment 9 (the comparison target), same offers,
same outcome rules. What changes is who owns the decision and how it is delivered
(2026-08-06 delegated-agentic spec §2):

  stated — the delegation framing, decision still written as a DECISION: line.
  tool   — the delegation framing, documents as files in a scratch workspace, and
           the decision EXECUTED via ./record_placement_decision, read back from
           decision.json. Stated-vs-revealed preference, one interface change.
"""
from __future__ import annotations

import argparse
import math
import pathlib
import sys
import tempfile
from pathlib import Path

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.run_constant_cushion_ladder import rungs_for_cell  # noqa: E402
from farm_eval.study.agentic import (  # noqa: E402
    run_agentic_ladder, scripted_tool_run,
)
from farm_eval.study.cells import (  # noqa: E402
    Cell, Economics, Scale, Species, StandardBand,
)
from farm_eval.study.economics import Arm, gain_for  # noqa: E402
from farm_eval.study.offer import build_offer  # noqa: E402
from farm_eval.study.phase1 import run_phase1  # noqa: E402
from farm_eval.study.prompt import build_delegated_prompt  # noqa: E402
from farm_eval.study.provider import (  # noqa: E402
    CodexAgenticProvider, CodexProvider, FakeAgenticProvider, FakeProvider,
)
from farm_eval.study.results import dump_jsonl_line  # noqa: E402
from farm_eval.study.sweep import SweepRules  # noqa: E402
from farm_eval.study.watch import live_line  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--interface", required=True, choices=["stated", "tool"],
                        help="stated: delegation framing, DECISION: line (arm B). "
                             "tool: delegation framing, documents as files, "
                             "decision executed via record_placement_decision "
                             "(arm C)")
    parser.add_argument("--out", required=True)
    parser.add_argument("--target-cushion", type=float, default=6.0,
                        help="survival cushion in percentage points, held at "
                             "every rung (6.0 = the experiment-9 value; the "
                             "comparison target)")
    parser.add_argument("--replicates", type=int, default=3)
    parser.add_argument("--min-accepts", type=int, default=2)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--model", default="gpt-5.6-terra")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)

    # isfinite first: "nan <= 0" is False, so NaN would otherwise sail through
    # (same guard as run_constant_cushion_ladder).
    if not math.isfinite(args.target_cushion) or args.target_cushion <= 0:
        print("--target-cushion must be a positive finite number", file=sys.stderr)
        return 2
    out = Path(args.out)
    if out.is_dir():
        print(f"--out must be a file path, not a directory: {out}", file=sys.stderr)
        return 2
    # Refuse to truncate completed work (Codex review 2026-08-07 F6): after a
    # partial failure the jsonl holds the cells already paid for; a rerun with
    # the same --out must not silently delete them.
    if out.exists() and out.stat().st_size > 0:
        print(f"--out already exists and is not empty; refusing to overwrite: "
              f"{out} (move it, or pass a new path)", file=sys.stderr)
        return 2

    cells = [Cell(species=sp, scale=Scale.LARGE, standard=StandardBand.BEYOND,
                  economics=Economics.EQUALIZED) for sp in Species]
    rung_map = {cell.species: rungs_for_cell(cell, args.target_cushion)
                for cell in cells}
    live_cells = [cell for cell in cells if rung_map[cell.species]]
    for cell in cells:
        if not rung_map[cell.species]:
            print(f"{cell.species.value}: no rung can reach a "
                  f"{args.target_cushion:.1f}pp cushion within the density cap — "
                  f"skipping this species", file=sys.stderr)
    if not live_cells:
        print("no species has a feasible rung at this cushion", file=sys.stderr)
        return 2
    # Each cell's own ladder-max gain, exactly as in run_constant_cushion_ladder:
    # an honest per-cell upper bound for the record and the envelope label.
    cell_max_gain = {
        cell.species: max(gain_for(build_offer(cell, rung, 0.0))
                          for rung in rung_map[cell.species])
        for cell in live_cells
    }

    on_call = None if args.quiet else live_line
    rules = SweepRules(replicates=args.replicates, min_accepts=args.min_accepts)
    out.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with out.open("w", encoding="utf-8") as fh:
        def persist(result) -> None:
            nonlocal count
            fh.write(dump_jsonl_line(result))
            fh.flush()
            count += 1

        if args.interface == "stated":
            provider = (FakeProvider(lambda p: "DECISION: ACCEPT") if args.dry_run
                        else CodexProvider(model=args.model))
            for cell in live_cells:
                run_phase1(
                    provider,
                    cells=[cell],
                    gains=[cell_max_gain[cell.species]],
                    rules=rules,
                    on_result=persist,
                    on_call=on_call,
                    rungs_provider=lambda c: rung_map[c.species],
                    prompt_builder=lambda offer: build_delegated_prompt(
                        offer, arm=Arm.DERIVED),
                )
        else:
            provider = (FakeAgenticProvider(scripted_tool_run("accept"))
                        if args.dry_run else CodexAgenticProvider(model=args.model))
            # Workspaces are left in place after the run so the raw decision
            # files and logs can be inspected; the jsonl carries everything the
            # analysis needs regardless.
            workspace_root = Path(tempfile.mkdtemp(prefix="delegated-tool-"))
            print(f"workspaces under {workspace_root}\n")
            for cell in live_cells:
                persist(run_agentic_ladder(
                    provider,
                    cell,
                    rung_map[cell.species],
                    gain_label=cell_max_gain[cell.species],
                    rules=rules,
                    workspace_root=workspace_root,
                    on_call=on_call,
                ))
    print(f"wrote {count} cell results to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
