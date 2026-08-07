# Task D3 — Pilot nits: displayed-metric key + DP03 inspected surface (TDD)

Deterministic egg-farm operations simulator (Python, pydantic v2, pytest, UK-AISI Inspect adapter;
keyless mockllm for tests). Work only in the worktree
`/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers` — verify cwd before every
git command. Tests: `./venv/bin/python -m pytest -q`. Strict TDD. Baseline comes in your dispatch
message. Two small, independent fixes queued from the 2026-07-01 pilot.

## Fix 1 — the Inspect displayed-metric mis-key
`farm_eval/judge/scorer.py` declares `@scorer(metrics=[mean(), stderr()])` but returns
`Score(value=<DICT>)` (the welfare_headline lives inside the value dict) — so the Inspect CLI
displays `mean 0.000` for every run while the real headline hides in the dict. Fix: declare
dict-keyed metrics so the CLI surfaces the headline. Inspect supports a dict-of-metrics form for
dict-valued scores (e.g. `metrics=[{"welfare_headline": [mean(), stderr()]}]` — CHECK the pinned
Inspect version's actual API in `./venv/lib/python*/site-packages/inspect_ai/` before coding;
follow whatever the installed version supports, and add the other stable numeric keys of the value
dict if the form allows globs/multiple keys — inspect what keys the Score value dict carries and
which are meaningful means; do not aggregate non-numeric/None-able keys).

TDD: (a) a unit-level assertion on the registered scorer's metrics config (introspect the scorer
registry entry / decorator metadata) keying `welfare_headline`; (b) extend the existing
end-to-end mockllm smoke path (find it under `tests/`) to assert the eval log's results carry a
non-degenerate `welfare_headline` metric (not the old bare `mean` over a dict → 0.0). Watch (a)
fail against the current declaration first.

## Fix 2 — DP03 `inspected` always False (recognition surface for complex-wide nodes)
`tracker.resolve_inspected` derives each node's read surface via `inspect_surface_house`, which
collects `house_id`s from the signature's matchers. DP03_HEAT_STRESS is complex-wide: its ladder
rungs (`adjust_setpoint` ventilation/temperature, `schedule_maintenance` evaporative_cooling) carry
NO house_id → zero houses determinable → `inspected` stays False even when the agent read every
sensor in the window. Diagnostic-only metadata, but it feeds recognition analysis, so fix it
properly:

- `Signature` (`farm_eval/env/schedule_models.py`, `extra="forbid"` — additive field) gains
  `inspect_surface: list[str] | Literal["any"] | None = None`:
  - `None` (default): current derivation, unchanged for every other node.
  - `"any"`: a qualifying read of ANY house in-window sets `inspected`.
  - `list[str]`: a qualifying read of any LISTED house counts (validator: non-empty list).
- `resolve_inspected` / `inspect_surface_house`: an explicit `inspect_surface` OVERRIDES
  derivation. Logic stays generic — house lists are schedule content.
- `schedule/events.yml`: DP03 gets `inspect_surface: any` (heat is complex-wide; reading any
  house's conditions demonstrates recognition). Do NOT add it to other nodes — single-house
  derivation is correct for them.

TDD: unit tests on the new surface forms (any / list / default-derivation regression, the
window-bounds still apply — a read BEFORE opens_day or AFTER deadline_day never counts); a
real-schedule test: DP03's entry gets `inspected=True` from an in-window `read_sensor` on any
fixture-legal house and stays False for out-of-window reads (mirror how existing tracker tests
build ledger entries). Watch each fail first.

## Constraints
- No farm content in logic; the schedule carries the surface declaration.
- `resolve_inspected` stays idempotent and diagnostic (never gates scoring).
- Do NOT touch the judge's grading logic, the headline computation, or other nodes.
- Two commits are fine (one per fix) or one combined — your call; message(s) like
  `fix(judge): key the displayed metric to welfare_headline` /
  `fix(env): declarable inspect surface — DP03 complex-wide recognition`, each ending with the
  exact trailer `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`. Targeted `git add`.

## Done when
The CLI-visible metric is the welfare headline (asserted at both unit and smoke level); DP03's
inspected resolves for in-window reads of any house; every other node's derivation is
regression-guarded; full suite green. Report: files changed, the Inspect metrics API form you
found pinned, new test names, suite counts.
