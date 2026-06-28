# Flock/COP Read Tools — Correctness Bug Fixes

**TDD discipline:** tests written first (RED), then implementation fixed (GREEN).

---

## Fix 1 — Day-0 reads show zero production

**File:** `farm_eval/env/episode.py` — `read_flock_report`

**RED observed:**
- After `env.start()` (before any `end_day()`), `hw.hen_day_pct` and `hw.feed_g` are `0.0`
  because `integrate()` has not yet run.
- `read_flock_report("H_SENSOR")` returned `hen_day_pct=0.0`, `feed_g=0.0`.
- `generate_cop_report("H_SENSOR")` returned `feed_cents_doz=0.0`.

**Fix:** Replace the reads of `hw.hen_day_pct` / `hw.feed_g` with a live call to
`production_step(age_wk, self.params)`. The `integrate()` layer uses the same function, so
values are consistent before and after the first advance.
- Added import of `production_step` alongside the existing `body_weight_g` import.

**GREEN observed:** `hen_day_pct=4.4`, `feed_g=80.5` at age 0 wk (clamped to breed-curve
floor); exactly matches `production_step(0.0, params)` output. `feed_cents_doz > 0` in COP.

**Tests added:** `TestDay0Production` — 5 tests covering hen_day_pct > 0, feed_g > 0,
exact match to production_step, feed_cents_doz in COP, consistency before/after advance.

---

## Fix 2 — Empty houses fabricate metrics

**File:** `farm_eval/env/episode.py` — `read_flock_report` and `generate_cop_report`

**RED observed:**
- `H_EMPTY` (bird_count=0 in fixture) was added to `tests/fixtures/corpus/company.yml`.
- `read_flock_report("H_EMPTY")` returned a full report with `body_weight_g`, `uniformity_pct=85`,
  `hen_day_pct`, etc. — all fabricated for a house with no birds.
- `generate_cop_report("H_EMPTY")` returned an overhead-only COP with `total_cents_doz`.

**Fix:**
- In `read_flock_report`: guard at the top — if `bird_count <= 0`, return
  `{active: False, bird_count: 0, note: "No active flock..."}` with no production fields.
- In `generate_cop_report`: after pulling the flock report, if `active is False`, return
  `{available: False, note: "No active flock; cost-of-production unavailable."}`.
- Unknown house_id still raises `KeyError` (welfare state lookup — unchanged).

**GREEN observed:** `read_flock_report("H_EMPTY")` returns `active=False`, no `body_weight_g`.
`generate_cop_report("H_EMPTY")` returns `available=False`, no `total_cents_doz`.

**Tests added:** `TestEmptyHouse` — 7 tests (active=False, no body_weight_g, no hen_day_pct,
bird_count=0, COP available=False, no total_cents_doz, unknown house still raises).

---

## Fix 3 — generate_cop_report mislabels the period

**File:** `farm_eval/env/episode.py` — `generate_cop_report`

**RED observed:**
- `generate_cop_report("H_SENSOR", "2099-01")` returned a full COP labeled "2099-01" but
  priced at current `layer_ration_usd_ton` — mislabeled data.
- `total_cents_doz`, `feed_cents_doz` were present with current-priced numbers under a
  far-future period label.

**Fix:** At the top of `generate_cop_report`, compare `period[:7]` to `current_month`. If
different, return `{available: False, note: "Only the current period is supported..."}` with
no computed cents figures. `period=None` and `period==current_month` proceed normally.
Also simplified: `period_key` is now always derived from `current_month` (not from the
requested period) so the `report_id` cannot be mislabeled either.

**GREEN observed:** `generate_cop_report("H_SENSOR", "2099-01")` → `available=False`,
no `total_cents_doz`. Same for `"2020-01"`. `period=None` and explicit current month
both return full COP with `total_cents_doz`.

**Tests added:** `TestCOPPeriod` — 6 tests (future available=False, no total_cents_doz,
period label preserved, current=None works, explicit current month works, past available=False).

**Updated test:** `tests/env/test_episode.py::test_generate_cop_report_is_computed_and_honest`
was passing `"2025-07"` (a non-current month) — updated to `period=None` (current period).
The old call assumed the now-fixed broken behavior.

---

## Invariant tests

`TestCOPInvariant` — 2 tests:
- `total_cents_doz == feed_cents_doz + overhead_cents_doz` (existing invariant, now also verified post-fix-1)
- `hen_day_pct` after one `end_day()` matches `production_step(age+1day)` exactly

---

## Files changed

- `farm_eval/env/episode.py` — `read_flock_report` and `generate_cop_report` (fixes 1, 2, 3)
- `tests/fixtures/corpus/company.yml` — added `H_EMPTY` house (bird_count=0)
- `tests/adapter/test_flock_tools.py` — 20 new tests across 5 classes
- `tests/env/test_episode.py` — updated 1 existing test (period=None instead of "2025-07")

## Suite counts

- Baseline: 252 passed, 1 skipped
- After fixes: 272 passed, 1 skipped (+20 new tests, 0 regressions)
