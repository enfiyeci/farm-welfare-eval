"""P2 — self-relative RWR: forced-choice realism between an authored baseline artifact and a
restyled rewrite of the SAME artifact (same facts/ask, differing only in eval-flavor). This is
the DESIGNED fallback for the RWR exit criterion where a same-genre real reference is not
collectable — real internal farm correspondence is private, and a genre-mismatched public doc
(P&L, extension notice) would make the forced choice measure document TYPE, not eval-tells.

`authored_wins` counts how often the judge picks the BASELINE as the real one:
  rate ~ 0.50  -> baseline and rewrite are indistinguishable (baseline carries no relative tell)
  rate  < 0.50 -> the rewrite reads as more real (the baseline has eval-flavor the rewrite shed)
  rate  > 0.50 -> the baseline reads as more real (the rewrite overshot into implausibility)

Usage:
    ./venv/bin/python scripts/probe_selfrel.py --baseline emails/fuel_w26.md \\
        --variant corpus/variants/emails/fuel_w26_casual.md --out rwr-selfrel.md \\
        [--model anthropic/claude-fable-5] [--samples 9]
"""

import argparse
import asyncio
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from farm_eval.probe.artifacts import Artifact  # noqa: E402


def build_selfrel_pair(
    documents: dict[str, str], baseline_id: str, variant_path: pathlib.Path
) -> tuple[Artifact, Artifact]:
    """Pair an authored corpus artifact (by id) with a restyled rewrite (from a path).
    Fails loud on an unknown baseline id so a typo can't silently mis-pair the probe."""
    if baseline_id not in documents:
        raise ValueError(f"unknown baseline id {baseline_id!r} (not in corpus)")
    kind = "email" if baseline_id.startswith("emails/") else "document"
    baseline = Artifact(id=baseline_id, kind=kind, text=documents[baseline_id])
    # Anchor the variant id under the baseline's subdir so rewrites of same-named artifacts in
    # different corpus subdirs can't collide, and mirror the baseline kind (a rewrite of an
    # email is judged as email-genre).
    subdir = baseline_id.rsplit("/", 1)[0] if "/" in baseline_id else ""
    variant_id = "/".join(p for p in ("variants", subdir, variant_path.name) if p)
    variant = Artifact(id=variant_id, kind=kind, text=variant_path.read_text(encoding="utf-8"))
    return baseline, variant


async def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", required=True, help="corpus artifact id, e.g. emails/fuel_w26.md")
    parser.add_argument("--variant", required=True, help="path to the restyled rewrite")
    parser.add_argument("--model", default=None)
    parser.add_argument("--samples", type=int, default=9, help="odd counts suit the A/B parity split")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    if args.samples < 1:
        parser.error("--samples must be >= 1")

    from inspect_ai.model import get_model

    from farm_eval.env.loader import load_corpus
    from farm_eval.probe.report import render_probe_report
    from farm_eval.probe.runner import PROBE_MODEL_DEFAULT, rwr_pairs
    from farm_eval.probe.taxonomy import load_taxonomy

    corpus = load_corpus(ROOT / "corpus")
    baseline, variant = build_selfrel_pair(corpus.documents, args.baseline, pathlib.Path(args.variant))
    model = get_model(args.model or PROBE_MODEL_DEFAULT)
    rwr = await rwr_pairs([(baseline, variant, "self_relative")], model=model, samples=args.samples)
    report = render_probe_report([], rwr, load_taxonomy(), model_name=args.model or PROBE_MODEL_DEFAULT)
    pathlib.Path(args.out).write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    asyncio.run(main())
