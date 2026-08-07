**Findings:** None. The fix looks clean.

Verified:

- `sanitize_dimension_sample` requires `sample_index` and every real discard note is emitted through the single append at [scorer.py:333](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/judge/scorer.py:333), always including `"sample_index"` at [scorer.py:336](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/judge/scorer.py:336).
- `collect_highlights` emits aggregate “no highlight evidence” notes only at [scorer.py:382](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/judge/scorer.py:382), with only `dimension` and `reason`; no `sample_index`.
- `criterion_notes` is clean: both appends are in `grade_llm_criterion`, and both represent the same per-criterion degraded-to-0 category at [scorer.py:634](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/judge/scorer.py:634) and [scorer.py:646](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/judge/scorer.py:646).
- The strengthened test has the intended mixed case: two sanitizer notes plus one aggregate note at [test_scorer_helpers.py:364](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/tests/judge/test_scorer_helpers.py:364), asserting `dimension_samples == 2` at [test_scorer_helpers.py:380](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/tests/judge/test_scorer_helpers.py:380). Old `len(dimension_notes)` logic would return `3` and fail.
- The code change is metadata-only and deterministic: it filters existing notes by key at [scorer.py:559](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/judge/scorer.py:559) and uses that count at [scorer.py:570](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/judge/scorer.py:570). No grading, headline, highlights, samples, or value-dict logic changed.

Focused verification passed:

`PYTHONDONTWRITEBYTECODE=1 ./venv/bin/python -m pytest -q -s -p no:cacheprovider tests/judge/test_scorer_helpers.py::test_discarded_evidence_counts_known_discards` → `.`