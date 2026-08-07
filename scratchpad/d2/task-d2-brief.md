# Task D2 — Per-beat EnvState checkpointing, opt-in (TDD)

Deterministic egg-farm operations simulator. Work only in the worktree
`/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers` — verify your cwd before
every git command; never touch `/Users/ardaenfiyeci/Desktop/farm-eval` itself. Tests:
`./venv/bin/python -m pytest -q`. Strict TDD. Baseline suite count comes in your dispatch message.

## Why
Pilot-hardening: a hard kill (SIGKILL/power) mid-paid-episode currently loses the run. With a
per-beat checkpoint, the latest `EnvState` + D1's `replay_env` recover the run for partial scoring.

## Design
**Config:** `EpisodeConfig` (`farm_eval/adapter/context.py`) gains `checkpoint_dir: str | None = None`.
`None` (default) = checkpointing OFF — zero behavior change (regression guard). Thread it from
`config.yml`/task args the same way existing config fields flow (mirror B1's `enabled_nodes`
threading; key-absent = off).

**Write path:** in `farm_eval/adapter/solver/farm_solver.py`, after each ACTUAL day advancement —
BOTH sites: the natural advance (`current_day() > day_before`) and the forced advance (the
max-turns-per-day backstop) — call a small helper that, when `checkpoint_dir` is set:
- Serializes `{"day": <new day>, "message_count": len(state.messages), "env_state": <EnvState
  model_dump(mode="json")>}` to `<checkpoint_dir>/<sample_id>/day_<n>.json`.
- `sample_id` comes from the Inspect `TaskState` (`state.sample_id`; coerce to a filesystem-safe
  string). Create directories as needed.
- **Atomic write-replace:** write to a temp file in the SAME directory, then `os.replace` onto the
  final name — a kill mid-write must never leave a truncated `day_<n>.json`.
- **Retention:** keep only the last **3** `day_*.json` per sample (delete older by day number,
  parsed from the filename — not mtime; determinism).
- **IO failure policy:** a checkpoint write failure must NEVER crash the episode (that would be the
  resilience feature killing a healthy paid run). Catch OS/serialization errors, emit a
  `logging.getLogger(...).warning(...)` naming the path and error, continue. Document this in the
  helper docstring. (Run-health surfacing of such warnings is E7's job, not yours.)

**Load helper:** `load_checkpoint(path) -> tuple[int, int, EnvState]` (day, message_count,
validated EnvState via `EnvState.model_validate`) in the same module or `farm_eval/adapter/
checkpoint.py` (your call; keep it importable without running a solver). Used by tests + future
salvage tooling.

## TDD — tests FIRST (under `tests/adapter/`, using the keyless mockllm pattern of the existing
solver tests — read them first and mirror their fixtures)
1. Off by default: run a short mockllm episode with `checkpoint_dir=None` → no files written, no
   behavior change (suite regression is the broader guard).
2. Checkpoints appear per beat: with `checkpoint_dir` set (tmp_path), after an episode reaching ≥4
   beats, exactly the LAST 3 `day_*.json` exist under `<dir>/<sample_id>/`, filenames match the
   beat days, JSON parses, `env_state.day_index == day`, `message_count` is a plausible positive int.
3. Atomicity: no stray temp files left after a normal run (glob the dir); the final file parses
   (structural stand-in for the kill-mid-write property — the os.replace pattern itself is the
   guarantee, assert it is used by checking no partial artifacts).
4. Restart equivalence: run an uninterrupted mockllm episode to day X, capturing the checkpoint at
   some earlier beat B; then build a FRESH env/store, load checkpoint B into it (set the store's
   env_state), re-enter the solver, run to day X; final `EnvState.model_dump()` equal to the
   uninterrupted run's. (`FarmEnv.start()` is idempotent via `EnvState.started`, so re-entry must
   not re-fire day-0 events — this test also guards that.)
5. Forced-advance path: a mockllm that never calls end_day (the backstop fires) still produces
   checkpoints on forced advances.
6. IO failure: point `checkpoint_dir` at an unwritable location (e.g. chmod 0 dir or a path under a
   FILE) → episode completes normally, a warning is logged (caplog), no exception.

Then RUN THE FULL SUITE. Zero existing-test changes expected.

## Constraints
- The env core stays Inspect-free: ALL of this lives in the adapter layer. Do not touch
  `farm_eval/env/` (D1's replay is a separate, already-merged consumer).
- Silent ledger: checkpoints are harness-side files; nothing about them is surfaced to the agent
  (no new tools, no message content besides the existing forced-advance note).
- Determinism: filenames/retention keyed on day numbers, not wall-clock/mtime.
- Commit: `feat(adapter): per-beat EnvState checkpointing (opt-in) for paid-run resilience` with
  the exact trailer `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`. Targeted `git add`.

## Done when
Opt-in checkpoints appear atomically per beat with last-3 retention; restart-from-checkpoint equals
uninterrupted; IO failures warn and never kill the episode; off-by-default is a no-op; full suite
green. Report: files changed, config threading, new test names, suite counts.
