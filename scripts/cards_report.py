"""Value-card report from finished Inspect logs: results.json and results.md.

    python scripts/cards_report.py --logs <log dir> --out <out dir>
"""

from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from farm_eval.cards.report import build_report, write_report  # noqa: E402
from farm_eval.config_paths import from_root  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--logs", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--rules", default="schedule/cards/rules.yml")
    ap.add_argument("--prices", default="scripts/model_prices.yml")
    args = ap.parse_args(argv)
    rep = build_report(args.logs, from_root(args.rules), from_root(args.prices))
    write_report(rep, args.out)
    if rep["notice"]:
        print(rep["notice"])
    print(f"wrote {pathlib.Path(args.out) / 'results.json'} and results.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
