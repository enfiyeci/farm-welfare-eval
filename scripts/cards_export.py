"""Export every distinct value-card prompt to markdown, for the owner to read.

    python scripts/cards_export.py --sheet schedule/cards/runsheets/E7_noise_floor.csv --out e7.md
    python scripts/cards_export.py --all --out all-wordings.md
"""

from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from farm_eval.cards.export import export_all_markdown, export_markdown  # noqa: E402
from farm_eval.cards.loader import load_bank  # noqa: E402
from farm_eval.cards.runsheet import load_experiments, read_sheet  # noqa: E402
from farm_eval.config_paths import from_root  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--cards-dir", default="schedule/cards")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--sheet")
    src.add_argument("--all", action="store_true")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    cards_dir = pathlib.Path(from_root(args.cards_dir))
    bank = load_bank(cards_dir)
    if args.all:
        md = export_all_markdown(bank, ladder=load_experiments(cards_dir / "experiments.yml").ladder)
    else:
        sheet = pathlib.Path(from_root(args.sheet))
        md = export_markdown(bank, read_sheet(sheet), title=sheet.name)
    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md, encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
