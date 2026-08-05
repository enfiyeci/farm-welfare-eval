# Scope: unit-derived plausibility guards for authored numbers

**Status:** scoped, not started. Spawned from the non-finite-guard work (branch
`fix/model-params-finiteness`; review record in
`docs/plans/2026-08-03-litter-ammonia-footpad-recalibration.md`), where it was ruled out of
scope twice with the note that finite-but-nonsense values are a different task.

## Problem

Every finiteness guard in the repo now fails loudly on `inf`/`nan` — but a **finite** nonsense
value passes them all and is laundered by the same clamps: every comparison against NaN is
false, and every clamp accepts any finite input. Measured during the non-finite work: a NaN
ventilation setpoint drove house NH3 to ~5e-26 and *raised* the welfare score and margin. A
finite `ammonia_ppm: -50` seed, `ventilation: 900` setpoint, or `litter_moisture: 300` behaves
identically — no error anywhere, a plausible-looking run whose scores are silently wrong. For
an eval, silent distortion is a validity threat; these runs are only caught today if someone
notices the numbers look odd.

## What is already guarded (do not rebuild)

- **Finiteness, everywhere external data enters:** `load_corpus`/`load_schedule` sweep all
  authored YAML numbers at load; `ModelParams` and `EnvState` validate at construction /
  `model_validate` (config block, play resume, checkpoints, `.eval` logs).
- **Agent actions:** `FarmEnv.apply_action` rails (E5) — `setpoint_bounds`, feed-order ceiling,
  staffing bounds — already reject nonsense *from the agent*, including non-finites (range
  comparisons are NaN-rejecting).
- **Schedule shape:** `state_seed`/`sensor_anomaly` field names are whitelisted to declared
  `HouseWelfare` fields (`farm_eval/env/events.py`); `_validate_audit_thresholds` fails at load
  when required corpus keys are missing.
- **Corpus prose:** `scripts/lint_corpus.py` + `scripts/check_corpus_consistency.py`
  (deterministic, content-driven, wired into pytest) own style/consistency — they do not check
  numeric plausibility and should not grow that job (they lint prose artifacts; numbers need to
  fire for fixtures and ablation variants too, which only the loader sees).

## The gap, by entry route

| Route | Writes | Example nonsense that passes today |
|---|---|---|
| `company.yml` house `welfare:` seeds | true state at day 0 | `ammonia_ppm: -50`, `litter_moisture: 300` |
| `company.yml` house `setpoints:` | world setpoints, bypasses the E5 agent rails | `ventilation: 900` (agent could never set this) |
| `company.yml` `bird_count`/areas/`litter_age_days` | world state | negative area, `bird_count: -1` |
| `pricing.yml` monthly tables | `state.market` via `refresh_market` | negative egg price |
| `weather.yml` normals | ambient driver | `humidity: 400` |
| schedule `state_seed` payload `value` | true state mid-episode via raw `setattr` | `keel_fracture_pct: 250` |
| schedule `pricing_shift` payload | `state.market` mid-episode | negative ration price |
| `history.yml` archives | archive READS only (display) | low stakes — exclude |

`sensor_anomaly` is **deliberately excluded**: it writes the gauge overlay, not the world, and
an implausible reading is legitimate authoring (a glitched gauge is the point of the event).

## Design constraint: unit-derived bounds only

The same trap was declined twice for the ~80 `ModelParams` calibration constants: inventing
per-field ranges asserts precision the model does not have. The line that avoids it: enforce
only bounds that are **objective facts of the unit**, never judgment calls about plausibility.

- Percentages (`*_pct`, `litter_moisture`, `humidity`): 0–100.
- Fractions (`panting_fraction`, vent as normalized unit ≤ the E5 ceiling): 0–1 (or the E5 rail).
- Hours-of-day (`lighting_hours`): 0–24.
- Non-negative physical quantities: ppm, lux, counts, areas, prices, tons, days, indices.
- Setpoints: validate against the **existing** `params.setpoint_bounds` table — the agent rail
  reused verbatim, so authored setpoints and agent-set setpoints obey one source of truth.

"Is 45 ppm a plausible ammonia *seed*?" is a judgment call and stays OUT. If wanted later, it
belongs in a lint `--report` warning tier, never a hard error.

## Recommended shape

One bounds table keyed by `HouseWelfare`/market/weather field name, next to the finiteness
walker's call sites (unit facts are physics, not farm content, so code is the right home —
the no-farm-content rule is not violated). Enforced at exactly two places:

1. **Load time** (`farm_eval/env/loader.py`, riding `_reject_non_finite`'s walk or a sibling
   sweep): covers company/pricing/weather seeds and both schedule payload routes before an
   episode starts, naming the authored key. Zero per-day cost, same fail-at-load posture.
2. **`state_seed` fire time** (`farm_eval/env/events.py`): the payload `value` is checked
   against the same table before `setattr`. One comparison per seed event (~a handful per
   episode). Technically redundant with (1) for YAML-loaded schedules but keeps the raw
   `setattr` route safe for any schedule assembled in memory.

Explicitly **not**: pydantic `Field(ge=, le=)` constraints on `HouseWelfare`. The substrate
writes those fields ~100k times per episode; constraints fire at construction only (so they
add nothing over (1)) and would tempt a future `validate_assignment` that costs seconds per
episode. Also **not**: guarding internal model writes — a full clean 518-day episode provably
stays finite and in-band; the anchor/invariant tests own model behavior.

## Order of work

1. **Measure first, enforce second:** run the proposed table read-only against the real corpus,
   the fixture corpora, and both schedules. Any shipped value outside a unit bound is either a
   bound error or a live content bug — both findings we want *before* enforcement flips on.
2. TDD the table + the two enforcement points (load-time; state_seed).
3. Full suite vs the 6-failure baseline; Codex pair per standing review discipline.

## Acceptance criteria

- An authored `ammonia_ppm: -50` (company seed or `state_seed` payload) fails at load naming
  the key; same for a >100 percentage, a >24 photoperiod, a negative price, and a setpoint
  outside `setpoint_bounds`.
- The real corpus, fixture corpora, both schedules, and all golden/replay fixtures still load
  (or every failure is adjudicated as a real content bug and fixed in the same wave).
- `sensor_anomaly` payloads remain unconstrained; `history.yml` untouched.
- No new per-day cost (suite runtime within noise of the baseline).

**Estimated size:** ~half a day including the measurement pass, TDD, and the review pair.
One risk to watch: fixture corpora use stylized values (e.g. `stocking_density: 1.0` as a
normalized unit vs the real corpus's hens-basis numbers) — the measurement pass decides
whether any bound needs to key on unit convention rather than field name alone.
