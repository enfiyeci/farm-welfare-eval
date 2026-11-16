"""Dry run of the value-card pipeline on made-up answers. No network call, no paid model.

Builds one dry-run sheet from the fixture experiments (tests/cards/fixtures/bank: FX_curves and
FX_planted; `planted_follower` gets the FX_planted rows only, since it needs a planted value),
runs it through `inspect_ai.eval` once per scripted responder and once on `mockllm/model` into a
temp log dir, runs the report, and prints the label per responder.

    python scripts/cards_dry_run.py [--out <dir to keep results.json / results.md>]
"""

from __future__ import annotations

import argparse
import pathlib
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from inspect_ai import eval as inspect_eval  # noqa: E402

from farm_eval.card_task import card_task  # noqa: E402
from farm_eval.cards.loader import load_bank  # noqa: E402
from farm_eval.cards.report import build_report, write_report  # noqa: E402
from farm_eval.cards.runsheet import build_rows, load_experiments, write_sheet  # noqa: E402
from farm_eval.config_paths import from_root  # noqa: E402

FIXTURE = "tests/cards/fixtures/bank"
EXPERIMENTS = ("FX_curves", "FX_planted")
RESPONDERS = ("always_protect", "never_protect", "flat_60", "threshold_2.30", "noisy_threshold_2.30",
              "malformed_mix", "planted_follower")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=None)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args(argv)
    cards_dir = pathlib.Path(from_root(FIXTURE))
    bank = load_bank(cards_dir)
    exps = load_experiments(cards_dir / "experiments.yml")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        sheet = tmp / "dry_run.csv"
        write_sheet([row for e in EXPERIMENTS for row in build_rows(bank, exps, e)], sheet)
        # planted_follower needs a planted value on every row, so it runs on the planted rows only.
        planted_sheet = tmp / "dry_run_planted.csv"
        write_sheet(build_rows(bank, exps, "FX_planted"), planted_sheet)
        logs = tmp / "logs"
        for responder in RESPONDERS + (None,):
            use = planted_sheet if responder == "planted_follower" else sheet
            task = card_task(sheet=str(use), cards_dir=str(cards_dir), allow_draft=True,
                             responder=responder, seed=args.seed)
            log = inspect_eval(task, model="mockllm/model", log_dir=str(logs), display="none")[0]
            if log.status != "success":
                print(f"run failed: {responder or 'mockllm/model'}: {log.status}")
                return 1
        rep = build_report(logs, cards_dir / "rules.yml", from_root("scripts/model_prices.yml"))
        out = pathlib.Path(args.out) if args.out else tmp / "report"
        write_report(rep, out)
    print(rep["notice"])
    for exp, e in rep["experiments"].items():
        for c in e["curves"]:
            if exp == "FX_curves":
                print(f"label {c['model']}: {c['label']}; fitted midpoint: {c['midpoint_text']}")
        for p in e["planted"]:
            print(f"planted {p['model']} v={p['planted_value_per_unit']}: "
                  f"{'pass' if p['passed'] else 'fail'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
