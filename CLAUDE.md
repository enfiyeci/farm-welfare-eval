# Farm Welfare Alignment Eval

A PETRI-style alignment evaluation: an AI agent plays **farm-management software** running a mid-to-large US commercial **cage-free** egg-laying farm across a full flock cycle (~17 in-world months, 2025-06-09 → ~2026-11-02). It makes a continuous stream of operational decisions; ~20 of them surface **animal-welfare** tensions. **Many target models are run against ONE fixed, pre-authored environment and compared.** Welfare decision quality is the scoring spine; profit is one of several tension sources, not the organizing axis.

## Read these first (the whole design is written down)

| Doc | What's in it |
|---|---|
| `docs/specs/2026-06-24-farm-welfare-eval-design.md` | The design spec. Architecture, contracts, tools (§5), state/schedule schema + **Signature kinds** (§7), judge (§10), eval-awareness (§12), prior-art/Inspect-API (§15), **4-layer scoring** (§16), reporting/viz (§17), **episode budget** (§18), **holistic Opus analysis** (§19) |
| `docs/world-bible.md` | Ground truth: company/houses/flocks/personnel/pricing; **compliance §12** (firm UEP/FDA/AVMA/APHIS numbers); reconciled flock roster §4; indemnity table §8 |
| `docs/decision-register.md` | The 20 welfare decisions: category/arity/promptedness/root-cause, **reference policies + 0/5/10 anchors**, tripwires, research anchors |
| `docs/model-params.md` | Reactive-model calibration — formulas + real coefficients (research P2) for `farm_eval/env/model.py` |
| `docs/plans/2026-06-24-harness-scaffold-phase-a.md` | Build plan. **Tasks 1–10 DONE.** **Amendment A1/A1.1** = the next increment. Phase B (B1–B9) outline with pinned Inspect API |
| `schedule/events.yml`, `schedule/beat-calendar.md` | The authored 31-beat event schedule (decision_points + events; email bodies are `body_ref` placeholders) |
| `docs/research/` | Deep-research findings + source PDFs (P1 compliance, P2 calibration, P4 decisions, P5 corpus-realism, P6 rubric-anchors) |

## Architecture (LOCKED — do not redesign)

- **Inspect-native** (UK AISI Inspect), Anthropic-backed. Target model swappable via Inspect **model role** (`target`/`grader`).
- **Static, pre-authored environment** (NOT an auditor that improvises). Deterministic **reactive substrate** — the world responds to the agent's actions the same way every run (this is the key bet; it's what makes a static eval realistic and is validated by the PETRI/Bloom review in §15).
- **Two layers:** (A) the Inspect-free **environment core** under `farm_eval/env/` — **DONE**; (B) the **Inspect adapter** (tools/solver/scorer/task) — TODO. `farm_eval/env/episode.py:FarmEnv` is the seam B calls.
- **Decision capture:** silent harness-side **ledger** + post-hoc **judge**. NEVER expose scoring/a "log your decision" tool to the agent.
- **Scoring:** 4-layer (integrated welfare-state · per-decision profile · tripwire gate · welfare-vs-profit lean). `realism` + `eval_awareness` are **validity gates**, excluded from welfare headline.

## Conventions

- Python 3.11+, **pydantic v2**, pytest. Package root `farm_eval/`.
- **venv is at `./venv` (NOT `.venv`).** Run tests: `./venv/bin/python -m pytest -q`.
- **NO farm content hardcoded in logic** — load from `corpus/` + `schedule/`; logic references only generic keys / `PLACEHOLDER_*` (tests). This is enforced in review.
- **Determinism:** no wall-clock/random in logic; seedable. Welfare and financial state are **separate** dimensions.
- Canonical `DecisionCategory`: `{false_binary, welfare_profit, welfare_cost, initiative, epistemic, integrity}` — must match `schedule/events.yml`.
- Day 0 = 2025-06-09; integer day indices. Email bodies / corpus prose are a later content pass.
- Commits end with `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`. Work on a branch, not directly on `main`.

## Current state (on `main`)

- **Phase A environment core + A1/A1.1: built, Codex-adversarial-reviewed + hardened.** Modules under `farm_eval/env/`: `state`, `schedule_models`, `ledger`, `loader`, `clock`, `model`, `events`, `tracker`, `episode` (the `FarmEnv` facade). Test fixtures under `tests/fixtures/`.
- **A1/A1.1 DONE (merged):** `Signature`/`DecisionPoint` are the generalized tagged union (`kind` ∈ binary/classified/ladder/state_band/communicative, plus `classes`/`rungs`/`metric`/`bands`/`root_cause`/`arity`/`promptedness`, class-level `tripwire`/`judged`/`default`, list-of-range bands, the `transient_before` matcher). The tracker dispatches on `kind` (binary/classified/ladder on tool calls, window-bounded to each decision's `[opens,deadline]`; `state_band` resolved AT the deadline beat from `EnvState`; `communicative` left to the judge); `LedgerEntry` carries `outcome`/`tripwire`/`root_cause_used`. **All schedule models are `extra="forbid"`** + a `Signature` validator requires each kind's scoring inputs; the real `schedule/events.yml` PARSES (`tests/env/test_real_schedule.py`).
- **Phase B B1–B4 DONE (the playable Inspect core):** `farm_eval/adapter/` wraps the Inspect-free env core. `context.py`: `EpisodeStore(StoreModel)` carries the plain-pydantic `EnvState` (env core stays Inspect-free; state serializes into the `.eval` log), `get_env(cfg)` binds a `FarmEnv` per sample. `tools/`: read tools (`get_datetime`/`list_houses`/`read_sensor`/`list_emails`/`read_email`), action tools (`adjust_setpoint`/feed/maintenance/vet/treatment/`send_email`) routing through `apply_action` and **never leaking the silent ledger**, `all_tools()` registry, `end_day`. `solver/farm_solver.py`: the generate→execute-tools loop (start once, advance on `end_day`, max-turns-per-day backstop keyed on ACTUAL advancement, `EpisodeStalled` on the total-turns cap, forced advances written to the transcript). `FarmEnv.start()` and `end_day()` are idempotent/atomic for retry/replay (`EnvState.started`/`fired_event_ids`; `end_day` stages on a deep copy and commits only after events fire). Verified end-to-end with the keyless `mockllm`.
- **KNOWN LIMITATION:** model reactivity is still PLACEHOLDER calibration (Task 7), not yet `docs/model-params.md`. `state_band` reads the deadline-snapshot value (`agg: final` exact, `mean` approximated; windowed agg is a calibration TODO; unsupported aggs rejected loudly). Classified `default`-class resolution at window close is deferred to the scorer (B6). `end_day` commits by replacing state field objects — callers must re-read state via `get_env`, not hold references across it.

## What's next (in order)

1. **Phase B B5–B9** (plan "Phase B execution"): B5 operator briefing prompt; **B6 judge scorer + rubric** (`@scorer`, per-dimension `judge/dimensions/*.md`, `get_model(role="grader")`); B7 task wiring (`farm_task.py` + `config.yml`); B8 run infra (`run_sweep.py`); B9 judge-validation harness (Spearman ρ gate). Also the **deferred read tools** (`read_flock_report`/`generate_cop_report`/`query_pricing`/`read_financials`) once the Hy-Line curve + pricing state exist.
2. **Content pass** — author the email/report prose the `body_ref`s point to (use P5 for format realism); calibrate `model.py` to `docs/model-params.md`; fill the judge rubric (P6).

## Pending gates before any production sweep (spec §15/§16)

- **Judge validation:** hand-label a transcript sample (ideally vet/welfare expert), report Spearman ρ vs the judge before trusting cross-model deltas.
- **Pilot-before-freeze:** run 2–3 models and measure welfare-elicitation AND eval-awareness before locking content (burying honeypots for realism can reduce elicitation).

## Process used here

This project was designed via brainstorming → writing-plans → and built via **subagent-driven-development** (fresh implementer + reviewer per task). Keep that discipline for the remaining increments: write/extend the plan, then execute task-by-task with review. Use `superpowers:test-driven-development`.
