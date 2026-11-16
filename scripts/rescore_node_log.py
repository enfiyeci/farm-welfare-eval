"""Re-score a node-episode log with a different grader (Inspect 0.3.241's `inspect score` has no
grader-role option). Every grader call is LIVE; arguments mirror `node_welfare_judge`.

  ./venv/bin/python scripts/rescore_node_log.py <log.eval> <grader model> [effort] [out.json]
  e.g. ./venv/bin/python scripts/rescore_node_log.py logs/node-20261116T060224Z/<file>.eval \
           claude-code/claude-opus-5-5 high

Prints the new score beside the logged one and writes a JSON record when an output path is given.
"""
import asyncio
import json
import pathlib
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import yaml
from inspect_ai.log import read_eval_log
from inspect_ai.model import GenerateConfig, get_model

from farm_eval.env.loader import load_schedule
from farm_eval.env.state import EnvState
from farm_eval.judge.dimensions import load_dimensions
from farm_eval.judge.scorer import grade_episode, load_node_reference, load_signatures


async def rescore(log_path: str, grader_name: str, effort: str | None) -> list[dict]:
    cfg = yaml.safe_load((ROOT / "config-nodes.yml").read_text())
    dims = load_dimensions(ROOT / cfg["dimensions_dir"])
    schedule_dir = ROOT / cfg.get("schedule_path", "schedule")
    signatures, schedule = load_signatures(schedule_dir), load_schedule(schedule_dir)
    grader = get_model(grader_name, config=GenerateConfig(effort=effort))
    calls: list[dict] = []

    async def generate(prompt: str) -> str:
        kind = "criterion" if prompt.startswith("You are grading ONE criterion") else "dimensions"
        start = time.monotonic()
        out = await grader.generate(prompt)
        calls.append({"kind": kind, "prompt_chars": len(prompt), "seconds": round(time.monotonic() - start, 1),
                      "usage": out.usage.model_dump() if out.usage else None})
        print(f"  {kind} call: {len(prompt):,} chars, {calls[-1]['seconds']}s", flush=True)
        return out.completion

    results = []
    for sample in read_eval_log(log_path).samples:
        store = sample.store
        spec = store["EpisodeStore:episode_spec"]
        refs = None
        if spec["scored"] and cfg.get("node_reference_path"):
            refs = load_node_reference(ROOT / cfg["node_reference_path"])[spec["episode_id"]]
        print(f"{sample.id}: grading with {grader_name} (effort {effort})", flush=True)
        score = await grade_episode(
            sample.messages, EnvState.model_validate(store["EpisodeStore:env_state"]),
            dimensions=dims, signatures=signatures, schedule=schedule, generate=generate,
            samples=int(cfg.get("judge_samples", 1)), episode_end_day=int(spec["end_day"]),
            forced_advances=store.get("EpisodeStore:forced_advances", 0),
            text_only_turns=store.get("EpisodeStore:text_only_turns", 0), welfare_references=refs,
            start_day=int(spec["start_day"]), dimension_mode=cfg.get("dimension_mode", "validity_only"),
            allow_empty_spine=not spec["scored"],
            scored_nodes=frozenset({spec["dp_id"]}) if spec["dp_id"] else frozenset(),
        )
        logged = next(iter(sample.scores.values()))
        results.append({
            "sample": sample.id, "grader": grader_name, "effort": effort,
            "logged_grader": store.get("EpisodeStore:grader_model"),
            "new_value": score.value, "logged_value": logged.value,
            "new_explanation": score.explanation, "logged_explanation": logged.explanation,
            "new_criterion_notes": score.metadata.get("criterion_notes"),
            "new_dimension_notes": score.metadata.get("dimension_notes"),
            "new_highlights": score.metadata.get("highlights"),
            "new_node_criteria": score.metadata.get("node_criteria"),
            "calls": calls,
        })
    return results


if __name__ == "__main__":
    log_path, grader_name = sys.argv[1], sys.argv[2]
    effort = sys.argv[3] if len(sys.argv) > 3 else None
    results = asyncio.run(rescore(log_path, grader_name, effort))
    for r in results:
        print(f"\n=== {r['sample']} ===")
        for key in sorted(set(r["new_value"]) | set(r["logged_value"])):
            print(f"{key:28s} new={r['new_value'].get(key)!s:24} logged={r['logged_value'].get(key)}")
        print("\nnew explanation:\n" + r["new_explanation"])
        print("\nlogged explanation:\n" + str(r["logged_explanation"]))
    if len(sys.argv) > 4:
        pathlib.Path(sys.argv[4]).write_text(json.dumps(results, indent=2, default=str))
        print(f"\nwrote {sys.argv[4]}")
