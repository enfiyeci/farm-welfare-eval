"""P3 — the probe's own validity gate. Two modes:

1. sheets:  generate blind kappa label sheets for ~15 artifacts (user fills true/false per class)
2. report:  probe the same artifacts, pair with filled sheets, print kappa + gate;
            --format-control additionally re-probes format-normalized copies and reports
            the per-class flag flip-rate (advisory).

Usage:
    ./venv/bin/python scripts/probe_kappa.py sheets --ids emails/a.md emails/b.md ... --out labels/
    ./venv/bin/python scripts/probe_kappa.py report --labels labels/ [--model ...] [--samples 5] [--format-control]
"""

import argparse
import asyncio
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from farm_eval.probe.artifacts import Artifact, enumerate_corpus_artifacts  # noqa: E402
from farm_eval.probe.kappa import kappa_report, make_kappa_sheets, normalize_format  # noqa: E402
from farm_eval.probe.runner import PROBE_MODEL_DEFAULT, probe_artifacts  # noqa: E402
from farm_eval.probe.taxonomy import load_taxonomy  # noqa: E402


def _artifacts(ids: list[str] | None) -> list[Artifact]:
    arts = enumerate_corpus_artifacts(ROOT / "corpus", ROOT / "prompts" / "operator_briefing.md")
    if ids:
        by_id = {a.id: a for a in arts}
        missing = [i for i in ids if i not in by_id]
        if missing:
            sys.exit(f"unknown artifact id(s): {missing}")
        return [by_id[i] for i in ids]
    return arts


async def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="mode", required=True)
    sheets_cmd = sub.add_parser("sheets")
    sheets_cmd.add_argument("--ids", nargs="*", default=None)
    sheets_cmd.add_argument("--out", required=True)
    report_cmd = sub.add_parser("report")
    report_cmd.add_argument("--labels", required=True)
    report_cmd.add_argument("--model", default=PROBE_MODEL_DEFAULT)
    report_cmd.add_argument("--samples", type=int, default=5)
    report_cmd.add_argument("--format-control", action="store_true")
    args = parser.parse_args()

    taxonomy = load_taxonomy()
    if args.mode == "sheets":
        for p in make_kappa_sheets(_artifacts(args.ids), taxonomy, args.out):
            print(p)
        return

    from inspect_ai.model import get_model

    import yaml as _yaml

    label_paths = sorted(pathlib.Path(args.labels).glob("*.kappa.yml"))
    if not label_paths:
        sys.exit(f"no *.kappa.yml sheets under {args.labels}")
    ids = [_yaml.safe_load(p.read_text(encoding="utf-8"))["artifact_id"] for p in label_paths]
    artifacts = _artifacts(ids)
    model = get_model(args.model)
    results = await probe_artifacts(artifacts, taxonomy, model=model, samples=args.samples)
    out = kappa_report(results, label_paths, taxonomy, samples=args.samples)
    print(f"kappa={out['kappa']:.3f}  n_pairs={out['n_pairs']}  gate={out['gate']} (>= 0.6)")
    for cls, c in sorted(out["per_class_counts"].items()):
        print(f"  {cls}: agree={c['agree']} disagree={c['disagree']}")
    if args.format_control:
        normalized = [
            Artifact(id=a.id, kind=a.kind, text=normalize_format(a.text)) for a in artifacts
        ]
        renorm = await probe_artifacts(normalized, taxonomy, model=model, samples=args.samples)
        base_by_id = {r["artifact_id"]: r for r in results}
        flips = 0
        checks = 0
        for r in renorm:
            base = base_by_id[r["artifact_id"]]
            for cls in (c.id for c in taxonomy):
                before = base["flag_counts"].get(cls, 0) * 2 > args.samples
                after = r["flag_counts"].get(cls, 0) * 2 > args.samples
                checks += 1
                flips += before != after
        print(f"format-control flip-rate: {flips}/{checks} = {flips / checks:.2f} (advisory; high => tighten rubric)")


if __name__ == "__main__":
    asyncio.run(main())
