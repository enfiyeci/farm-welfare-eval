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

## Play the farm (human dashboard)

A local, keyless, deterministic way to play the episode yourself through **exactly the tool surface
the model gets** (spec [`docs/specs/2026-07-06-playable-dashboard-design.md`](docs/specs/2026-07-06-playable-dashboard-design.md)).
Strict info-parity: every panel is a rendering of a tool call you explicitly made — nothing is
fetched implicitly, and blind mode shows nothing the model wouldn't see.

```bash
./venv/bin/python scripts/play.py --session sessions/my-run            # blind (default); opens on :8618
./venv/bin/python scripts/play.py --session sessions/my-run --resume   # continue a saved session later
./venv/bin/python scripts/play.py --session sessions/my-run --debug    # Night Ops debug drawer
                                                                       # (ledger/state/schedule;
                                                                       # permanently stamps the session)
```

Autosaves after every day; `--port` and `--config` override the defaults (8618, `config.yml`).

**Post-game scoring.** When the episode ends, the in-UI **report card** shows your per-decision
outcomes, tripwires, and Layer-1 welfare state (mechanical, offline). For the full judge pass over
your transcript (needs an API key):

```bash
./venv/bin/python scripts/score_session.py sessions/my-run --model anthropic/claude-opus-4-8
```

> Human results are **advisory** and never comparable to model sweep results (you authored the eval).
> Their value is as reference transcripts — e.g. a welfare-first, a profit-first, and a negligent
> run give the judge-validation ρ gate the score spread it needs.

## Status

**Built and content-complete.** The harness (deterministic env core + Inspect adapter + judge
structure + task wiring + run/validation infra) is fully tested keyless via `mockllm` (~1,220
offline tests). The content pass is done: the authored `corpus/` (company docs, pricing, 212
inbound email bodies plus ~281 reply bodies in rotating variant banks from the corpus-realism
pass, so most repeated correspondence draws fresh text rather than one canned line — banks wrap
modulo their length and a few autoresponders are single-body, so it reduces rather than
eliminates repeats), the calibrated welfare model, and the judge rubric — 10 dimension files
(`judge/dimensions/*.md`), including a 3-axis validity split (`eval_awareness`,
`assistant_persona_bleed`, `helplessness_resignation`) with machine-validated multi-span
evidence — are all merged. Real model runs work today with an API key.

**Piloting has begun:** full-model pilots (Gemini 3.1 Pro) ran on 2026-07-12 and a hardened
round-3 re-pilot on 2026-07-15, each with a debrief; the judge went through four rounds of
evidence-pipeline and dimension hardening (see `docs/probes/` pilot notes). **Pending gates
before trusting cross-model results** (deliberate, per spec §15/§16): the multi-model pilot
(`docs/pilot-debrief-protocol.md`) and judge validation — hand-label a transcript sample and
report Spearman ρ vs the judge (`judge/validate.py`) before reading anything into cross-model
deltas. The pilots are also same-family (Gemini judging Gemini); use an out-of-family grader or
measure the bias first. Until those run, outputs are treated as unvalidated.
