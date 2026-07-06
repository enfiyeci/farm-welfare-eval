"""P2 — run the artifact probe over the real corpus (motivation-guessing; optionally RWR
against corpus/references/). QA-side: output steers authoring, never enters scoring.

Usage:
    ./venv/bin/python scripts/probe_corpus.py --out probe-report.md \\
        [--model anthropic/claude-fable-5] [--samples 5] [--references corpus/references]
"""

import argparse
import asyncio
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from farm_eval.probe.artifacts import Artifact, enumerate_corpus_artifacts, rendered_samples  # noqa: E402
from farm_eval.probe.report import render_probe_report  # noqa: E402
from farm_eval.probe.runner import PROBE_MODEL_DEFAULT, probe_artifacts, rwr_pairs  # noqa: E402
from farm_eval.probe.taxonomy import load_taxonomy  # noqa: E402


def _reference_pairs(artifacts, ref_dir: pathlib.Path):
    """Pair each email artifact with a same-kind reference (real_reference mode) when
    corpus/references/ has any; classes with no reference are simply not RWR'd here
    (self_relative mode is exercised by comparing pre/post rewrite files explicitly)."""
    refs = sorted(ref_dir.rglob("*.md")) if ref_dir.is_dir() else []
    # Exclude README.md (case-insensitive) — provenance marker, not a real reference document
    refs = [r for r in refs if r.name.lower() != "readme.md"]
    if not refs:
        return []
    pairs = []
    for i, art in enumerate(a for a in artifacts if a.kind == "email"):
        ref_path = refs[i % len(refs)]
        ref = Artifact(id=f"references/{ref_path.name}", kind="document",
                       text=ref_path.read_text(encoding="utf-8"))
        pairs.append((art, ref, "real_reference"))
    return pairs


async def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default=PROBE_MODEL_DEFAULT)
    parser.add_argument("--samples", type=int, default=5)
    parser.add_argument("--rwr-samples", type=int, default=9, help="odd counts suit majority reads")
    parser.add_argument("--references", default=str(ROOT / "corpus" / "references"))
    parser.add_argument("--rendered", action=argparse.BooleanOptionalAction, default=True,
                        help="also probe rendered read-tool outputs (default: on)")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    if args.samples < 1:
        parser.error("--samples must be >= 1")
    if args.rwr_samples < 1:
        parser.error("--rwr-samples must be >= 1")

    from inspect_ai.model import get_model

    model = get_model(args.model)
    taxonomy = load_taxonomy()
    artifacts = enumerate_corpus_artifacts(ROOT / "corpus", ROOT / "prompts" / "operator_briefing.md")
    motivation_artifacts = artifacts
    if args.rendered:
        motivation_artifacts = artifacts + rendered_samples(ROOT / "corpus", ROOT / "schedule")
    motivation = await probe_artifacts(motivation_artifacts, taxonomy, model=model, samples=args.samples)
    rwr = await rwr_pairs(_reference_pairs(artifacts, pathlib.Path(args.references)), model=model, samples=args.rwr_samples)
    report = render_probe_report(motivation, rwr, taxonomy, model_name=args.model)
    pathlib.Path(args.out).write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    asyncio.run(main())
