"""Run self-driven escalation episodes; --dry-run makes no external calls."""

from __future__ import annotations
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from farm_eval.study.agentic import run_escalation_episode, scripted_episode_run
from farm_eval.study.cells import Cell, Economics, Scale, Species, StandardBand
from farm_eval.study.provider import CodexAgenticProvider, FakeAgenticProvider
from farm_eval.study.results import write_episodes_jsonl


def cell(species: Species) -> Cell:
    return Cell(
        species=species,
        scale=Scale.LARGE,
        standard=StandardBand.BEYOND,
        economics=Economics.EQUALIZED,
    )


def dry_provider() -> FakeAgenticProvider:
    values = iter((110.0, 125.0, 140.0))

    def behave(instruction: str, workspace: Path) -> str:
        try:
            return scripted_episode_run("accept", next(values))(instruction, workspace)
        except StopIteration:
            return scripted_episode_run("decline")(instruction, workspace)

    return FakeAgenticProvider(behave=behave)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--arm", choices=["same", "fresh"], required=True)
    p.add_argument("--episodes", type=int, default=3)
    p.add_argument("--max-rounds", type=int, default=8)
    p.add_argument("--species", choices=["hen", "shrimp"], default="hen")
    p.add_argument("--no-compliance", action="store_true")
    p.add_argument("--out", required=True)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--model", default="gpt-5.6-terra")
    p.add_argument("--quiet", action="store_true")
    a = p.parse_args()
    out = Path(a.out)
    if out.exists() and out.stat().st_size:
        raise SystemExit(f"refusing to overwrite non-empty {out}")
    records = []
    for i in range(a.episodes):
        provider = dry_provider() if a.dry_run else CodexAgenticProvider(model=a.model)
        records.append(
            run_escalation_episode(
                provider,
                cell(Species(a.species)),
                a.arm,
                Path(f"{out}.workspaces") / f"ep{i + 1}",
                compliance=not a.no_compliance,
                max_rounds=a.max_rounds,
            )
        )
        write_episodes_jsonl(records, out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
