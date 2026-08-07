# Task D3 report

## Status
DONE

## Commits
- `3af3fbb` — fix(judge): key the displayed metric to welfare_headline
- `f4bbcb2` — fix(env): declarable inspect surface — DP03 complex-wide recognition

## Baseline vs final
- Baseline (HEAD 90a1dcc): 678 passed, 1 skipped, 0 failed.
- Final (HEAD f4bbcb2): **694 passed, 1 skipped, 0 failed** (16 net new passing tests; diffed
  full PASSED/SKIPPED/FAILED name sets before/after — additions only, zero regressions/removals).

## Fix 1 — the Inspect displayed-metric mis-key

### Pinned Inspect API found (0.3.241, `./venv/lib/python3.14/site-packages/inspect_ai/`)
`inspect_ai/scorer/_scorer.py`:
```python
def scorer(
    metrics: Sequence[Metric | Mapping[str, Sequence[Metric]]]
    | Mapping[str, Sequence[Metric]],
    ...
)
```
So the pinned version supports a dict-of-metrics form as EITHER a bare `Mapping[str,
Sequence[Metric]]` passed directly, OR one entry of a list being a `dict[str, list[Metric]]`
alongside plain `Metric` objects. I used the list-with-one-dict-entry form:
`metrics=[{"welfare_headline": [mean(), stderr()], "*": [mean(), stderr()]}]`.

Key/glob resolution lives in `inspect_ai/_eval/task/results.py`:
- `scorers_from_metric_dict` + `resolve_glob_metric_keys`: each dict key is compiled via
  `fnmatch.translate` into a regex and matched against the keys of the **first dict-valued
  sample Score** (`base_score`). Matches are expanded into one `EvalScore` per literal key, with
  metrics deduped by `registry_log_name` (so an explicit key + a `*` glob covering the same key
  do NOT double up).
- If a specified/glob-expanded key is **absent from any sample's dict value**, Inspect raises
  `TypeError: key '{metric_key}' isn't present in the score value dictionary` — so a glob is only
  safe when every key in every sample's value dict is guaranteed present.
- `mean()`'s own fallback (`inspect_ai/scorer/_metrics/mean.py`) documents the original bug
  precisely: "prints a warning and returns 0 if the Value is a complex object (list or dict)" —
  i.e. the old `metrics=[mean(), stderr()]` applied to the whole dict-valued `Score.value` and
  silently produced the degenerate `mean 0.000`.

I verified every key `welfare_judge` puts into its `value` dict (the 4 fixed keys
`welfare_headline`/`diagnostic_composite`/`welfare_state`/`tripwires_observed` plus one entry per
configured `JudgeDimension.id`) is an always-present plain `float` — never `None`-able or
non-numeric — so a blanket `*` glob is safe. Declared:
```python
@scorer(
    metrics=[
        {
            "welfare_headline": [mean(), stderr()],
            "*": [mean(), stderr()],
        }
    ]
)
```

### New tests
- `tests/judge/test_scorer_metrics.py` (new file):
  - `test_metrics_declaration_keys_welfare_headline` — introspects
    `registry_info(welfare_judge).metadata[SCORER_METRICS]` (the `@scorer` decorator's stashed
    metrics config) and asserts a dict entry keys `welfare_headline`.
  - `test_metrics_declaration_is_not_a_bare_simple_list` — regression guard for the original bug
    form (a flat list of simple `Metric`s with no dict entry at all).
  - Both watched FAIL first against the pre-fix `metrics=[mean(), stderr()]` declaration (confirmed
    by `git stash`-ing the scorer.py change and rerunning).
- `tests/adapter/test_task.py::test_farm_task_runs_end_to_end_and_scores` (extended):
  - Target mockllm now calls `adjust_setpoint` on `H_SENSOR`/`ventilation` (matching the fixture's
    one decision point) before `end_day` x5, so the node spine scores > 0 — making the
    non-degeneracy assertion meaningful rather than coincidentally true.
  - New assertions: `log.results.scores` contains an `EvalScore` named `"welfare_headline"`
    (proving the CLI-visible result is keyed correctly, not folded into a bare `"welfare_judge"`
    entry), its `metrics["mean"].value` equals `score_value["welfare_headline"]`, and it is
    non-zero. Watched FAIL first (old code produced a single `EvalScore` named `"welfare_judge"`
    with no `welfare_headline`-named result at all).

## Fix 2 — DP03 `inspected` always False

### Changes
- `farm_eval/env/schedule_models.py`: `Signature` gains an additive
  `inspect_surface: list[str] | Literal["any"] | None = None` field (kept `extra="forbid"`);
  the existing `_require_kind_fields` validator gained one more check — a `list` form must be
  non-empty.
- `farm_eval/env/tracker.py`: new private helper `_qualifying_read_houses(entry, state)` collects
  every house read by a `_READ_TOOLS` call within `[entry.opened_day, entry.deadline_day]`.
  `resolve_inspected` now checks `dp.signature.inspect_surface` first: if set, it OVERRIDES the
  `inspect_surface_house` derivation — `"any"` requires any qualifying read, `list[str]` requires
  a qualifying read of one of the listed houses; if unset (`None`), the original single-house
  derivation path runs unchanged. `inspect_surface_house` itself was left untouched (its "single
  determinable house" contract doesn't fit the `"any"`/list forms, so the override lives one level
  up in `resolve_inspected`).
- `schedule/events.yml`: `DP03_HEAT_STRESS.signature` gains `inspect_surface: any`. No other
  decision point was touched.

### New tests
- `tests/env/test_inspected_flag.py` (extended, 12 new tests):
  `test_inspect_surface_house_returns_none_for_complex_wide_ladder_by_default`,
  `test_default_derivation_leaves_complex_wide_node_never_inspected`,
  `test_inspect_surface_any_sets_inspected_from_any_house_read`,
  `test_inspect_surface_any_still_respects_window_bounds`,
  `test_inspect_surface_any_read_after_deadline_does_not_count`,
  `test_inspect_surface_any_with_no_read_stays_false`,
  `test_inspect_surface_list_counts_a_read_of_a_listed_house`,
  `test_inspect_surface_list_ignores_a_read_of_an_unlisted_house`,
  `test_inspect_surface_explicit_overrides_a_determinable_single_house_derivation`,
  `test_inspect_surface_list_form_rejects_empty_list`.
  (3 of these — the "any" positive case, the "list" positive case, and the override-of-a-
  determinable-house case — were watched FAILING first against the field-only change with no
  tracker wiring; the window-bounds/no-read/empty-list cases already passed trivially since they
  assert the pre-existing false/None default, confirming the field addition alone changed nothing
  else.)
- `tests/env/test_real_schedule.py` (extended, 4 new tests):
  `test_dp03_signature_declares_inspect_surface_any`,
  `test_dp03_inspected_true_from_any_fixture_legal_house_read_in_window` (in-window `read_sensor`
  on real corpus house `H1` sets `inspected=True`), `test_only_dp03_declares_inspect_surface`
  (regression guard — asserts no other node in the real schedule carries `inspect_surface`),
  `test_dp03_inspected_stays_false_for_out_of_window_reads` (reads before `opens_day` / after
  `deadline_day` never count). Watched the "any"-declaration and in-window tests FAIL first
  (before adding `inspect_surface: any` to `schedule/events.yml`).

## Self-review notes
- Confirmed via `git diff --stat` that only the files the brief scoped were touched: judge's
  grading logic / headline computation (`welfare_headline()` in `judge/headline.py`,
  `score_nodes`, `diagnostic_composite`, etc.) were NOT modified — only the `@scorer(metrics=...)`
  declaration line changed in `scorer.py`.
- Confirmed via a before/after diff of the full `PASSED`/`SKIPPED`/`FAILED` test-name listing
  that the suite delta is purely additive (16 new passing tests, 0 removed, 0 newly failing).
- Confirmed Fix 1's dict-of-metrics form is genuinely dedup-safe (explicit `welfare_headline` key
  + `*` glob covering the same key) by reading `resolve_glob_metric_keys` — it dedupes by
  `registry_log_name` per resolved key, so no double `mean`/`stderr` entries appear.
- Confirmed the `*` glob is safe against non-numeric/absent-key risk: every key `welfare_judge`
  writes into its `value` dict is always a plain `float` computed unconditionally in the `score()`
  body (`avg[d.id]`, `headline`, `composite`, `compute_welfare_state(...)["score"]`,
  `float(len(ledger_trips))`) — no branch omits a key or writes `None`/non-numeric.
- For Fix 2, deliberately did NOT change `inspect_surface_house`'s return contract (still "single
  determinable house or None") — the override lives in `resolve_inspected` itself, keeping the
  derivation helper's semantics stable for the many other call sites/tests that exercise it
  directly (e.g. `test_inspect_surface_house_honors_target_key`).
- Verified `git stash`-based negative controls for Fix 1 (both new unit tests fail against the
  unmodified `scorer.py`) and manual review of test-run output for Fix 2 (3 of the 16 new tests
  fail before the tracker-logic change, confirming they exercise the actual fix rather than
  passing vacuously).
- No farm content was hardcoded in logic: `resolve_inspected`/`_qualifying_read_houses` reference
  only the generic `inspect_surface` field; which houses qualify for DP03 lives in
  `schedule/events.yml`.

## F1 follow-up — bare-dict scorer metrics (drop the empty welfare_judge result)

### Commit
- `813b4de` — fix(judge): bare-dict scorer metrics — drop the empty welfare_judge result

### What codex flagged (Minor) and why it's real
My original Fix-1 declaration used the **list-of-one-dict** form:
`@scorer(metrics=[{"welfare_headline": [...], "*": [...]}])`. In the pinned inspect_ai 0.3.241,
`compute_eval_scores` (`inspect_ai/_eval/task/results.py`) handles a `list` metrics arg by
ALWAYS calling `scorer_for_metrics(..., metrics=simple_metrics)` in addition to
`scorers_from_metric_dict(...)` for each dict entry. `split_metrics` puts the sole dict into
`dict_metrics` and leaves `simple_metrics == []`. `scorer_for_metrics` iterates an empty metrics
list (producing no `list_metrics`) but STILL unconditionally appends
`EvalScore(name=scorer_name="welfare_judge", metrics={})` — the spurious empty result codex saw
as `welfare_judge [] {}`. The BARE-dict form (`metrics={...}`) hits the `else` branch of
`compute_eval_scores`, which calls ONLY `scorers_from_metric_dict` — so no empty result is emitted.

### Verified in the pinned version (not guessed)
- `scorer()`'s signature (`inspect_ai/scorer/_scorer.py`) accepts
  `Sequence[Metric | Mapping[...]] | Mapping[str, Sequence[Metric]]` — the bare `Mapping` form is
  a first-class accepted type.
- Confirmed the empty-result mechanism by reading `compute_eval_scores` + `scorer_for_metrics`
  (the unconditional `results.append(EvalScore(name=scorer_name, metrics=list_metrics))` with an
  empty `list_metrics`).
- Confirmed the FIX empirically via the e2e eval log (`test_task.py`): before the change the test's
  new assertion failed with `spurious empty scorer-named result present: [('welfare_judge', {})]`;
  after switching to the bare dict, NO result is named `welfare_judge`, and `welfare_headline`
  (+ the globbed per-key results) still appear with correct means.

### Test change (TDD)
- Extended `tests/adapter/test_task.py::test_farm_task_runs_end_to_end_and_scores` (not a new test
  — the assertion is folded into the existing e2e path that already inspects `log.results.scores`):
  - asserts `log.results.scores` contains NO result named `"welfare_judge"` (the empty
    scorer-named result), and
  - asserts every result carries at least one metric (no degenerate empty-metrics result).
  - Watched it FAIL first against the list-of-one-dict form (the exact
    `EvalScore(name='welfare_judge', metrics={})` was reported), then PASS after the bare-dict fix.

### Suite
- Full suite: **694 passed, 1 skipped, 0 failed** — unchanged count (the assertion extends an
  existing test rather than adding one), matching the 694+1skip baseline. No regressions.

### Self-review note
The two existing `tests/judge/test_scorer_metrics.py` unit tests were written to accept EITHER the
list-with-dict-entry OR the bare-dict shape (they recurse into lists and also handle a top-level
dict), so both still pass unchanged under the bare-dict declaration — no test needed loosening.
