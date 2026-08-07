# Task E3 — per-house COP variance in generate_cop_report (TDD)

You are working in a Python repo: a **deterministic egg-farm operations simulator** used to evaluate
an autonomous farm-manager agent (no live models involved in this task). Work only in the worktree
`/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers`. Run tests with
`./venv/bin/python -m pytest -q` (a venv is symlinked at ./venv — do NOT create one). Use
**superpowers:test-driven-development**: write a failing test FIRST, watch it fail for the right
reason, then implement, then the full suite green.

## The bug
`FarmEnv.generate_cop_report(house_id, period)` in `farm_eval/env/episode.py` (around line 381)
IGNORES `house_id` entirely — it always returns the complex-wide cumulative P&L figures. So calling
it for H1, H2, H3, H4, H5 returns BYTE-IDENTICAL numbers. In a pilot this identical-per-house output
tipped a model off that it was in a scripted world. Fix: a per-house call must return figures that
DIFFER realistically between houses, driven by each flock's real state (primarily flock AGE).

## Design (implement exactly this; it keeps the report HONEST — computed from real state)
Read these first for context:
- `farm_eval/env/episode.py`: `read_flock_report` (~line 352, shows how per-house age/production are
  computed) and the current `generate_cop_report` (~line 381).
- `farm_eval/env/model/economics.py`: `cost_step`, `feed_tons_for_day`, `cop_cents_doz` — the real
  per-house daily cost model. REUSE these; do not reinvent cost formulas.
- `farm_eval/env/model/layers/production.py`: `production_step(age_weeks, params) -> {hen_day_pct, feed_g}`.
- `farm_eval/env/model/drivers.py`: `flock_age_weeks(age_weeks_at_start, day_index)`.

Change `generate_cop_report(house_id="", period="")` to branch:

1. **Non-current period requested** → return an explicit unavailable signal (do NOT mislabel
   current-priced numbers as a historical period). Compute `current_month = self.current_date()[:7]`;
   if `period` is truthy and `period[:7] != current_month`, return
   `{"house_id": house_id or "complex", "period": period, "available": False, "note": "Only the
   current period is supported; historical cost-of-production replay is out of scope."}`.
   (This design — the unavailable signal, and the empty-house handling below — is adopted from the
   unmerged `feat/flock-cop-reads-integrity` branch's computed-honest reads; credit it.)

2. **A specific house (`house_id` non-empty)** → compute an INSTANTANEOUS per-house COP from that
   house's real current state:
   - Unknown house (`house_id not in self.state.welfare.houses`) → `{"house_id": house_id,
     "available": False, "note": "no such house"}`.
   - `birds = self.state.world.bird_count.get(house_id, 0)`. Empty house (`birds <= 0`, e.g. H6) →
     `{"house_id": house_id, "period": period or current_month, "available": False, "note": "No
     active flock; cost-of-production unavailable."}`.
   - `age_wk = flock_age_weeks(self.state.world.age_weeks_at_start.get(house_id, 0.0), self.state.day_index)`.
   - **Pre-lay guard (BEFORE computing production):** if `age_wk < self.params.breed_age_wk[0]`
     (the breed curve's first age point = lay onset ~18 wk; a principled boundary, NOT a magic
     number — the model clamps hen-day to a pre-lay floor below onset, so cost-per-dozen isn't
     meaningful) → return `{"house_id": house_id, "period": period or current_month, "available":
     False, "note": "Flock not yet in lay; cost-of-production unavailable."}`. (H4 at 17 wk on day 0
     hits this. NOTE: `hen_day` is NEVER <= 0 in this model — it clamps to ~4.4 below onset — so do
     NOT guard on `hen_day <= 0`; guard on age vs onset as above.)
   - `prod = production_step(age_wk, self.params)`; `hen_day = prod["hen_day_pct"]`, `feed_g =
     prod["feed_g"]` (here `age_wk >= onset`, so `hen_day > 0` and `total_dozen > 0` are guaranteed).
   - Otherwise compute:
       - `total_dozen = birds * (hen_day / 100.0) / 12.0`
       - `feed_tons = feed_tons_for_day(feed_g, birds)`
       - `ration_usd_ton = self.state.market.layer_ration_usd_ton`  # the live blended price the P&L
         model uses (do NOT invent per-ration prices — the live model uses one blended price)
       - `fuel_index = self.state.market.lp_fuel_index`
       - `costs = cost_step(feed_tons, ration_usd_ton, total_dozen, birds, fuel_index, self.params)`
       - `cop = costs["total_cost"] / total_dozen * 100.0`  # cents/dozen (guaranteed total_dozen>0 here)
       - `feed_cents_doz = costs["feed_cost"] / total_dozen * 100.0`
       - `overhead_cents_doz = (costs["total_cost"] - costs["feed_cost"]) / total_dozen * 100.0`
     - Reference/target: `ref = self.corpus.pricing.get("cop_cents_doz_sep2025", {}).get("total")`;
       `vs_reference = round(cop - float(ref), 2) if ref is not None else None`;
       `target = float(ref) * 0.955 if ref is not None else None` (the corporate -4.5% target);
       `vs_target = round(cop - target, 2) if target is not None else None`.
     - Return a dict:
       `{"report_id": f"COP-{house_id}-{current_month.replace('-','')}", "house_id": house_id,
         "period": period or current_month, "available": True, "flock_age_weeks": round(age_wk, 1),
         "hen_day_pct": round(hen_day, 1), "cop_cents_doz": round(cop, 2),
         "feed_cents_doz": round(feed_cents_doz, 2), "overhead_cents_doz": round(overhead_cents_doz, 2),
         "vs_reference_cents_doz": vs_reference, "vs_target": vs_target}`

3. **Complex (house_id empty)** → KEEP the existing cumulative-P&L behavior UNCHANGED (the current
   body: reads `self.state.financial`, `economics.cop_cents_doz`, returns cop_cents_doz/
   margin_cents_doz/revenue_cum/feed_cost_cum/other_cost_cum/eggs_sold_dozen/vs_target/period/house_id).
   Just make sure the non-current-period guard (step 1) runs before it. Do not alter the complex
   numbers or keys — the existing complex tests must stay green.

## Why age drives realistic variance (verified against the real params — sanity-check your result)
A near-peak flock (~34 wk) has HIGH hen-day% and efficient feed conversion → LOW cost/dozen. A late-lay
flock (~68 wk) has LOWER hen-day% → its per-dozen feed AND per-bird overhead spread over fewer dozens →
HIGHER cost/dozen. Verified with `ModelParams()`: age 34→~114¢, 43→~115¢, 52→~117¢, 68→~121¢/doz (feed
ration 284, fuel 1.0). So a later-lay house's `cop_cents_doz` is strictly HIGHER than a nearer-peak
house's. Lay onset is `params.breed_age_wk[0]` (18 wk); below it the flock is pre-lay → available:false.

## TDD — write these tests FIRST (new file `tests/env/test_cop_per_house.py`), watch them fail, then implement
IMPORTANT: the test fixture corpus (`tests/fixtures/corpus/company.yml`) has only two houses, BOTH at
the default age 0 (pre-lay) and 1000 birds — so it is USELESS for variance testing as-is. Build the env
from the fixture like `tests/env/test_generate_cop_report.py` (`FarmEnv.from_paths(FIX/"corpus",
FIX/"schedule", ...)`, `env.start()`), then SET the state directly to control ages/counts
deterministically, e.g.:
```python
env.state.world.age_weeks_at_start["H_SENSOR"]   = 34.0   # near peak
env.state.world.age_weeks_at_start["H_NOSENSOR"] = 68.0   # late lay
env.state.world.bird_count["H_SENSOR"] = env.state.world.bird_count["H_NOSENSOR"] = 100000
```
(Use whatever house ids the fixture actually has; read it first.) Cover:
1. Two houses at DIFFERENT ages return DIFFERENT `cop_cents_doz` (the core anti-identical-figures test).
2. The later-lay house (68 wk) has a strictly HIGHER `cop_cents_doz` than the near-peak house (34 wk).
3. An empty house (`bird_count = 0`) → `available` is False, no fabricated cop.
4. A pre-lay house (`age_weeks_at_start` set below `params.breed_age_wk[0]`, e.g. 15 wk) → `available`
   is False with the "not yet in lay" note.
5. A non-current `period` argument (e.g. "2024-01") → `available` False with the unavailable note.
6. The report is HONEST: the per-house cop reflects real state (e.g. it changes as the flock ages if
   you advance many days), not a canned constant.

Also RUN THE FULL SUITE and fix any existing test that assumed identical-per-house output (search
`tests/adapter/test_read_tools.py`, `tests/adapter/test_action_tools.py`,
`tests/env/test_generate_cop_report.py`, `tests/adapter/test_generate_cop_report_tool.py`). The
complex-level (no house_id) tests must stay green unchanged; only update tests that asserted the old
per-house identical behavior, and explain each change.

## Constraints (enforced by review)
- HONEST reads: figures must be computed from real state, never canned. No farm content hardcoded in
  logic — all numbers come from state/params/corpus.
- Deterministic: no wall-clock/random.
- Reuse `economics.py` cost functions; do not duplicate cost formulas.
- Full gate: `./venv/bin/python -m pytest -q` green (ruff/mypy are not installed in this venv — skip them).

## Done when
The new tests pass, the full suite is green, per-house calls return house-specific honest figures,
empty/pre-lay/unknown houses and non-current periods return honest unavailable signals, and the
complex-level report is unchanged. Report: the files changed, the new test names, and a 2-3 line
summary of the observed per-house COP spread (e.g. "H1 68wk ~X¢ vs H3 34wk ~Y¢").
