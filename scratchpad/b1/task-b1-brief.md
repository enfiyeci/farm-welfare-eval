# Task B1 — enabled_nodes node-selection config (TDD)

You are working in a Python repo: a **deterministic egg-farm operations simulator** used to evaluate an
autonomous farm-manager agent (no live models in this task). Work only in the worktree
`/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers`. Tests:
`./venv/bin/python -m pytest -q` (venv symlinked at ./venv — do NOT create one). Use
**superpowers:test-driven-development**: failing test FIRST, watch it fail for the right reason,
implement, full suite green.

## Goal
Add an optional `enabled_nodes` config: a list of decision-point ids. When set, ONLY those decision
points are seeded into the ledger, so ONLY their node scores enter the welfare headline / breakouts /
coverage denominator. `None` (the default) = all nodes enabled (unchanged behavior). This lets a
comparison sweep run a fixed SUBSET of the ~23 nodes (for ablations / salience studies). An unknown id
must FAIL LOUD (ValueError) — never silently ignored.

## Key insight (why one filter point suffices)
Scoring, stakeholder/category breakouts, and the headline mean ALL derive from the ledger
(`score_nodes` iterates `state.ledger`). So if a disabled node is never SEEDED into the ledger, it is
automatically absent from scores, breakouts, and the denominator. Therefore: filter at ledger-seeding
time (`open_due_decision_points`). Do NOT filter the shared cached schedule object (it is cached across
samples in `farm_eval/adapter/context.py::load_resources` — mutating it would corrupt other samples).
Do NOT change the scorer.

## Read first
- `farm_eval/env/events.py::open_due_decision_points(state, schedule, day)` — seeds ledger entries for
  every `dp` with `dp.opens_day <= day` not already present. THIS is the filter point.
- `farm_eval/env/episode.py` — `FarmEnv.__init__` (line ~70), `from_paths` (~78), and the two call
  sites of `open_due_decision_points` (~line 109 and ~133).
- `farm_eval/adapter/context.py` — `EpisodeConfig` (frozen dataclass, ~line 32) and `get_env` (~61).
- `farm_eval/farm_task.py` — builds `EpisodeConfig` from the config dict (~line 30).

## Implement
1. `EpisodeConfig` (context.py): add field `enabled_nodes: tuple[str, ...] | None = None`.
2. `get_env` (context.py): pass `enabled_nodes=cfg.enabled_nodes` into the `FarmEnv(...)` construction.
3. `FarmEnv.__init__` (episode.py): add param `enabled_nodes: Iterable[str] | None = None`. Store as
   `self.enabled_nodes: frozenset[str] | None = frozenset(enabled_nodes) if enabled_nodes is not None
   else None`. VALIDATE FAIL-LOUD: if `self.enabled_nodes is not None`, compute the schedule's DP ids
   `{dp.id for dp in schedule.decision_points}` and if any id in `self.enabled_nodes` is not among them,
   raise `ValueError(f"enabled_nodes references unknown decision point(s): {sorted(unknown)}")`.
4. `FarmEnv.from_paths` (episode.py): add the same `enabled_nodes: Iterable[str] | None = None` kwarg
   and pass it through to the constructor (so tests can use it).
5. `open_due_decision_points` (events.py): add a param `enabled_nodes: frozenset[str] | None = None`
   (default None). In the loop, skip a `dp` when `enabled_nodes is not None and dp.id not in
   enabled_nodes` (i.e. do not seed it). Update BOTH call sites in episode.py to pass
   `self.enabled_nodes`.
6. `farm_task.py`: read `cfg.get("enabled_nodes")` and pass it to `EpisodeConfig(...,
   enabled_nodes=tuple(cfg["enabled_nodes"]) if cfg.get("enabled_nodes") else None)`.
7. `farm_eval/config.yml`: it is currently empty — add a short comment documenting the optional key,
   e.g.:
   ```yaml
   # enabled_nodes: [DP01_AMMONIA_VENT, DP16_FOOTPAD]   # optional: run only these nodes (FIXED within
   #                                                     # a sweep). Omit / null = all nodes enabled.
   ```
   (a comment only — do not set a live value.)

## TDD — write these FIRST (new file `tests/env/test_node_selection.py`), watch fail, then implement
Use the REAL schedule (`schedule/`) + corpus (`corpus/`) via `FarmEnv.from_paths` (the test FIXTURE
schedule `tests/fixtures/schedule` has only one placeholder DP, so it can't exercise this). Pattern:
```python
from pathlib import Path
from farm_eval.env.episode import FarmEnv
ROOT = Path(__file__).resolve().parents[2]
def _env(enabled=None):
    env = FarmEnv.from_paths(ROOT/"corpus", ROOT/"schedule", seed=1, episode_end_day=511, enabled_nodes=enabled)
    env.start()
    return env
```
Cover:
1. `enabled_nodes=["DP01_AMMONIA_VENT","DP16_FOOTPAD"]`: seed the ledger past both nodes' opens_days
   (either advance the clock, or directly call `open_due_decision_points(env.state, env.schedule, 511,
   env.enabled_nodes)`), then assert `{e.dp_id for e in env.state.ledger} == {"DP01_AMMONIA_VENT",
   "DP16_FOOTPAD"}` — EXACTLY those two, nothing else.
2. `enabled_nodes=None` (default): after seeding to day 511, the ledger contains ALL the schedule's
   decision points (assert the count equals `len(env.schedule.decision_points)` — the full set).
3. An unknown id (e.g. `enabled_nodes=["DP01_AMMONIA_VENT","NOPE_NODE"]`) → `FarmEnv.from_paths(...)`
   raises `ValueError` (use `pytest.raises(ValueError)`).
4. Only enabled nodes score: build a tiny ledger from an enabled-nodes env (2 nodes), run
   `farm_eval.judge.scorer.score_nodes` over `env.state.ledger` with a fake `grade_fn=lambda e,c,s: 0.0`
   and the env's signatures (`{dp.id: dp.signature for dp in env.schedule.decision_points}`), and assert
   the returned dict's keys are a subset of the enabled set (a disabled node never scores). Keep it
   honest — pick enabled nodes whose windows you actually seed.

## Constraints
- Deterministic; no wall-clock/random. No farm content hardcoded in logic (ids come from config).
- Do NOT mutate the shared cached schedule. Do NOT modify the scorer.
- Full gate: `./venv/bin/python -m pytest -q` green (ruff/mypy not installed here — skip).
- Any existing test that calls `FarmEnv(...)` / `open_due_decision_points(...)` positionally must still
  work — add new params with defaults at the END so call sites are unaffected.

## Done when
New tests pass, full suite green, `enabled_nodes` filters ledger seeding (and thus scoring), unknown
ids fail loud, and `enabled_nodes=None` preserves the full-set default. Report: files changed, new test
names, and the final suite pass/skip count.
