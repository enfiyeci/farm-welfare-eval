"""Build value-card run sheets: schedule/cards/runsheets/<experiment>.csv, one row per model call.

    python scripts/cards_build_sheets.py                    # every experiment
    python scripts/cards_build_sheets.py --experiment E7_noise_floor
"""

from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from farm_eval.cards.loader import load_bank  # noqa: E402
from farm_eval.cards.runsheet import build_rows, load_experiments, write_sheet  # noqa: E402
from farm_eval.config_paths import from_root  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--cards-dir", default="schedule/cards")
    ap.add_argument("--out-dir", default=None, help="default: <cards-dir>/runsheets")
    ap.add_argument("--experiment", default=None)
    args = ap.parse_args(argv)
    cards_dir = pathlib.Path(from_root(args.cards_dir))
    out_dir = pathlib.Path(from_root(args.out_dir)) if args.out_dir else cards_dir / "runsheets"
    bank = load_bank(cards_dir)
    experiments = load_experiments(cards_dir / "experiments.yml")
    ids = [args.experiment] if args.experiment else [e.id for e in experiments.experiments]
    for exp_id in ids:
        rows = build_rows(bank, experiments, exp_id)
        path = out_dir / f"{exp_id}.csv"
        write_sheet(rows, path)
        statuses = sorted({r["text_status"] for r in rows})
        print(f"{path}: {len(rows)} rows, text status {', '.join(statuses)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
