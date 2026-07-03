"""Pilot driver — run the farm-welfare eval over one or more target models with a FIXED grader.

Unlike the original ephemeral scratchpad driver (which hardcoded a specific worktree), this resolves
the repo root RELATIVE TO ITSELF, so it always runs the code it is committed alongside — no stale
checkout, and it survives session/scratchpad cleanup. Relative config paths (corpus/schedule/
prompts/dimensions) resolve because we chdir to the repo root first.

The grader (judge) role is held FIXED across the sweep — only the target may vary, or welfare
headlines are not comparable (see farm_eval/run_sweep.py).

Usage:
    ./venv/bin/python scripts/run_pilot.py <config.yml> <grader> <target1> [target2 ...]

Prefer the wrapper `scripts/run_pilot.sh`, which also wires up Vertex/ADC auth. Example:
    ./venv/bin/python scripts/run_pilot.py config.yml \\
        google/gemini-2.5-pro google/gemini-2.5-pro
"""
import os
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

from farm_eval.run_sweep import run_sweep, summarize_sweep  # noqa: E402

if len(sys.argv) < 4:
    sys.exit("usage: run_pilot.py <config.yml> <grader> <target1> [target2 ...]")

config_path, grader, targets = sys.argv[1], sys.argv[2], sys.argv[3:]

print(f"[pilot] repo root:     {ROOT}")
print(f"[pilot] farm_eval from: {__import__('farm_eval').__file__}")
print(f"[pilot] config={config_path}  grader={grader}  targets={targets}")

results = run_sweep(targets, grader=grader, config_path=config_path)

print("\n=== SWEEP RESULTS ===")
for r in results:
    print(
        f"  model={r.model!r} status={r.status} "
        f"welfare_headline={r.welfare_headline} tripwires={r.tripwires_tripped}"
    )
print("\n=== SUMMARY (ranked) ===")
print(summarize_sweep(results))
