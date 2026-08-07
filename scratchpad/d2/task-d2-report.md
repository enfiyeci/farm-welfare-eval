# Task D2 — Per-beat EnvState checkpointing (opt-in) — Report

**Status:** DONE
**Commit:** `09f593eb965e83c1ea70ade3b1b8cc58106673a2`
**Branch:** `feat/phase-c6-env-levers`
**Suite:** 669 passed, 1 skipped (baseline was 663 passed, 1 skipped → +6, my six new tests, zero regressions).

## Files changed
- **`farm_eval/adapter/checkpoint.py`** (NEW) — the checkpoint module: `write_checkpoint(...)` (never-raising, atomic, retention-pruning) + `_prune_old_checkpoints(...)` + `_sample_dir_name(...)` + `load_checkpoint(path) -> tuple[int, int, EnvState]`. Importable without running a solver (for tests + future salvage tooling).
- **`farm_eval/adapter/context.py`** — `EpisodeConfig` gains `checkpoint_dir: str | None = None` (default `None` = OFF).
- **`farm_eval/adapter/solver/farm_solver.py`** — `farm_solver(...)` gains a `checkpoint_dir: str | None = None` override kwarg; resolves the effective dir as `checkpoint_dir if not None else cfg.checkpoint_dir`; a `_checkpoint(state)` helper writes at BOTH advancement sites (natural `end_day` advance and the forced-backstop advance). No-op when the effective dir is `None`.
- **`farm_eval/farm_task.py`** — threads `checkpoint_dir=cfg.get("checkpoint_dir")` into `EpisodeConfig` (mirrors the `enabled_nodes` pattern; key-absent → `None` → off).
- **`config.yml`** — documents the new optional `checkpoint_dir` key (commented out; default off).
- **`tests/adapter/test_checkpoint.py`** (NEW) — 6 tests, mockllm fixture pattern mirrored from `tests/adapter/test_solver.py`.

## Config threading (config → EpisodeConfig → solver)
`config.yml` `checkpoint_dir:` (absent/null = off) → `farm_task.py` reads `cfg.get("checkpoint_dir")` and passes it to `EpisodeConfig(checkpoint_dir=...)` → the solver reads `cfg.checkpoint_dir` inside its `_checkpoint` closure (with an optional direct `farm_solver(..., checkpoint_dir=...)` override for tests/tooling, which takes precedence when non-None). This exactly mirrors how `enabled_nodes` flows: through `EpisodeConfig` only, not as a required separate solver kwarg. `get_env(cfg)` is unchanged — checkpointing is a pure adapter/solver-layer concern; the env core stays Inspect-free and untouched.

## Atomic-write + last-3-retention mechanism
- **Per-beat file:** `<checkpoint_dir>/<sample_id>/day_<n>.json`, payload `{"day": n, "message_count": len(state.messages), "env_state": EnvState.model_dump(mode="json")}`. `sample_id` (Inspect `TaskState.sample_id`, int|str) is coerced to a filesystem-safe dir name (alnum/`-`/`_`/`.` kept, else `_`).
- **Atomicity:** write to a temp file `.day_<n>.json.tmp` in the SAME directory, then `os.replace(tmp, final)`. `os.replace` is atomic on a single filesystem, so a kill mid-write can only ever leave a `.tmp` (never a truncated `day_<n>.json`). Verified by test 3 (no non-`day_*.json` artifacts remain after a normal run).
- **Retention:** `_prune_old_checkpoints` globs `day_*.json`, parses the day number **out of the filename** (not mtime — determinism), sorts ascending, and unlinks all but the last 3. Verified by test 2: a run crossing beats {2,4,6,8,20} leaves exactly `[6, 8, 20]`.

## IO-failure policy
`write_checkpoint` NEVER raises: `OSError` (mkdir/write/replace failures) and `TypeError`/`ValueError` (serialization) are caught, logged via `logging.getLogger(__name__).warning(...)` naming the day, `checkpoint_dir`, and the error, then swallowed — the episode continues. Documented in the module + function docstrings. Rationale: the resilience feature must never be the thing that kills a healthy paid run. Verified by test 6 (checkpoint_dir under a FILE → episode still `success`, day_index reaches 20, a "checkpoint" warning is captured by caplog, no exception). Manually confirmed the failure path is real (Errno 20 Not a directory) — not a vacuous pass.

## New test names (tests/adapter/test_checkpoint.py)
1. `test_checkpointing_off_by_default_writes_nothing` — `checkpoint_dir=None`: no files written anywhere; episode reaches day 20 (regression guard).
2. `test_checkpoints_appear_per_beat_with_last_3_retention` — beats {2,4,6,8,20} → exactly `[6,8,20]` retained; each file's `day`, `env_state.day_index`, and positive int `message_count` verified.
3. `test_checkpoint_atomicity_no_stray_temp_files` — no leftover `.tmp`/partial files; every remaining file parses.
4. `test_restart_from_checkpoint_matches_uninterrupted_run` — load an EARLIER checkpoint (day 4) into a FRESH env/store, re-enter the solver, run to day 20; final `EnvState` equals the uninterrupted run's (also guards `FarmEnv.start()` idempotence via `EnvState.started` — day-0 events don't re-fire).
5. `test_forced_advance_path_still_checkpoints` — agent never calls `end_day`; the max-turns backstop still produces checkpoints (last day == episode end).
6. `test_checkpoint_io_failure_warns_and_never_kills_episode` — unwritable path; episode completes, warning logged, no crash.

## Test fixture note
The shared `tests/fixtures/schedule` has only beats {0,5}, insufficient for the ≥4-beat requirement. Each test writes a bespoke `schedule/events.yml` to `tmp_path` with five self-contained decision points at days {2,4,6,8} (decision points alone contribute beat days via `Schedule.event_days()`; no `events:` → no `body_ref` to satisfy), reusing the shared fixture corpus unchanged. `episode_end_day` (default 20) contributes the final beat.

## Deviations / concerns
- None material. The solver exposes a direct `checkpoint_dir` override kwarg in addition to reading `cfg.checkpoint_dir`; production (`farm_task`) uses only the config path, and the override is used by tests. This is additive and back-compatible.
- The `TypeError`/`ValueError` serialization branch is marked `# pragma: no cover` (defensive — `EnvState.model_dump(mode="json")` is always JSON-serializable in practice); the `OSError` branch IS covered by test 6.
- No existing tests were modified (zero expected, zero changed).

---

## Review-fix pass (commit `90a1dcc`)

Two review findings fixed via TDD (tests written first, watched fail for the right reason, then implemented), plus one stale-comment cleanup.

### F1 — path-traversal in `_sample_dir_name` (codex Critical / reviewer Minor)
**Problem:** `_sample_dir_name` preserved dots, so a `sample_id` sanitizing to exactly `"."`, `".."`, or `""` was NOT neutralized. `".."` made `Path(checkpoint_dir) / ".."` write to — and let retention `unlink` `day_*.json` in — the PARENT of `checkpoint_dir`; `"."` collapsed into `checkpoint_dir` itself and cross-contaminated samples. (Slashes were already mapped to `_`, so no deep traversal — this was the only gap.)

**Fix:** after sanitizing, deterministically remap the three degenerate results to fixed safe single segments that stay strictly inside `checkpoint_dir`: `"" -> "_"`, `"." -> "__"`, `".." -> "___"`. Documented in the docstring, including the note that the sanitizer is already non-injective in general (`"a/b"` and `"a_b"` collide), so the remaps add no new class of collision — every result is a safe single path segment, which is all the traversal fix requires.

**Tests (TDD, initially failing):**
- `test_sample_dir_name_neutralizes_traversal_segments` (parametrized over `["..", ".", "", "../..", "./.", "..\x00"]`) — each yields a name that is not `""`/`.`/`..`, has no separators, and resolves strictly UNDER its parent (asserts `resolved.parent == parent.resolve()` and `resolved != parent.resolve()`).
- `test_sample_dir_name_preserves_normal_ids` — `1` and `"sample-42_a.b"` pass through unchanged (regression guard: the fix doesn't mangle real ids).
- `test_write_checkpoint_traversal_id_stays_inside_checkpoint_dir` — an end-to-end `write_checkpoint(str(ckpt_dir), "..", ...)` leaves a sentinel `day_999.json` in the parent untouched, writes no `day_3.json` into the parent, and lands exactly one `day_3.json` strictly under `checkpoint_dir`.

### F2 — no positive coverage of the production config path (codex Minor)
**Problem:** every positive test drove the solver's direct `checkpoint_dir=` override kwarg, leaving the advertised production flow (config.yml → farm_task.py → `EpisodeConfig.checkpoint_dir` → solver fallback) with no positive test.

**Fix (test only — no code change needed; the fallback already existed):**
- `test_checkpoints_written_via_episode_config_checkpoint_dir` — sets `checkpoint_dir` on `EpisodeConfig` (NOT the solver override; `_run` passes `checkpoint_dir=None` to `farm_solver`, so only `cfg.checkpoint_dir` can drive writes), and asserts checkpoints appear at `[6, 8, 20]` (per-beat + last-3 retention) via the config seam.

The solver's direct `checkpoint_dir=` override kwarg is kept as a harmless test seam.

### F3 — stale comment (reviewer Minor)
`test_restart_from_checkpoint_matches_uninterrupted_run` said it loads "day 4", but after last-3 retention the earliest retained file is day 6 (retained set `{6, 8, 20}`; the code picks `sorted(...)[0]` dynamically, so the logic was always correct). Comment corrected to say day 6 / earliest-retained.

### Result
- Full suite: **678 passed, 1 skipped** (was 669/1 → +9: 6 parametrized F1 traversal cases + `test_sample_dir_name_preserves_normal_ids` + `test_write_checkpoint_traversal_id_stays_inside_checkpoint_dir` + `test_checkpoints_written_via_episode_config_checkpoint_dir`). Zero regressions; no existing tests modified beyond the F3 comment.
- Targeted `git add` of exactly `farm_eval/adapter/checkpoint.py` + `tests/adapter/test_checkpoint.py`.

### Note (out of scope, not changed)
`tests/adapter/test_checkpoint.py` carries a pre-existing unused `import stat` (dead since the original D2 commit, not introduced by these fixes). Left as-is to avoid unrelated churn; a trivial follow-up could drop it.
