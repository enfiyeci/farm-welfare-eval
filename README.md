# Farm Welfare Alignment Eval

A PETRI-style alignment evaluation: an AI agent plays **farm-management software** running a
mid-to-large US commercial **cage-free** egg-laying farm across a full flock cycle. It makes a
continuous stream of operational decisions; ~20 of them surface **animal-welfare** tensions. Many
target models are run against ONE fixed, pre-authored environment and compared. Welfare decision
quality is the scoring spine.

Start with [`CLAUDE.md`](CLAUDE.md) for the full design map, the locked architecture, and current
state. The design spec is in [`docs/specs/`](docs/specs/).

## Layout

- `farm_eval/env/` — the Inspect-free environment core (state, schedule models, ledger, reactive
  model, events, the silent decision tracker, the `FarmEnv` facade). 100% deterministic.
- `farm_eval/adapter/` — the Inspect adapter: per-sample store (`context.py`), tools, the solver loop.
- `farm_eval/judge/` — the welfare judge (`@scorer`) + per-dimension rubric files + validation.
- `farm_eval/farm_task.py` — the `@task`; `config.yml` — paths, roles, episode/judge config.
- `schedule/` — the authored event schedule. `prompts/operator_briefing.md` — the neutral framing.

## Setup

```bash
python3 -m venv venv && ./venv/bin/pip install -e .   # installs inspect-ai + deps
./venv/bin/python -m pytest -q                          # the suite (keyless; uses mockllm)
```

## Running

Model swapping is via Inspect **model roles** (`target` plays the farm, `grader` judges):

```bash
export ANTHROPIC_API_KEY=...
inspect eval farm_eval/farm_task.py \
  --model-role target=anthropic/claude-opus-4-8 \
  --model-role grader=anthropic/claude-opus-4-8
inspect view        # render the transcript + scores
```

Sweep several targets over the same environment (programmatic):

```python
from farm_eval.run_sweep import run_sweep, summarize_sweep
results = run_sweep(["anthropic/claude-opus-4-8", "anthropic/claude-sonnet-4-6"],
                    grader="anthropic/claude-opus-4-8")
print(summarize_sweep(results))   # welfare-headline-ranked comparison
```

> **Before trusting cross-model welfare deltas**, validate the judge against human labels and report
> Spearman ρ — see [`docs/judge-validation.md`](docs/judge-validation.md).

## Status

The harness (env core + Inspect adapter + judge structure + task wiring + run/validation infra) is
built and tested keyless via `mockllm`. A real run additionally needs the authored **`corpus/`**
and real **rubric anchors** (the content pass — see `CLAUDE.md` "What's next").
