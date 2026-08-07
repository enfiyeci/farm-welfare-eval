# Phase C1 — Financial P&L + Profit (Tier-0) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the deterministic env-core compute a real, path-independent cost-of-production P&L (revenue, costs, margin, COP) each day from the existing production layer + the corpus monthly prices, including egg downgrades and a feed booked-cost mechanic so procurement timing has a real profit effect.

**Architecture:** Add a pure-function economics module (`farm_eval/env/model/economics.py`) that mirrors the existing `layers/*.py` pattern — pure functions that read state values + prices and return `$` terms. The day-by-day orchestrator (`integrate.py`) calls them inside its existing per-house day loop and accumulates results into `EnvState.financial`. All economic coefficients live in `ModelParams` (the calibration home). No agent/Inspect/corpus-authoring work — this is pure env-core, tested deterministically.

**Tech Stack:** Python 3.11+, pydantic v2, pytest.

## Global Constraints

- **Python 3.11+, pydantic v2, pytest.** Package root `farm_eval/`.
- **venv is at `./venv` (NOT `.venv`).** Run tests: `./venv/bin/python -m pytest -q`.
- **Determinism:** no wall-clock / no random in logic; the model is a pure function of `(state, elapsed_days, params)`. **Path-independence is mandatory:** integrating N days at once must equal integrating the same N days in chunks (guarded by `test_path_independence`).
- **Welfare and financial state are separate dimensions** — economics reads welfare/world/market but writes only `state.financial`.
- **No farm content hardcoded in logic** — coefficients live in `ModelParams`; logic references only generic fields. Economic coefficients are **research-anchored placeholders flagged ⚠️ in `docs/research/SOURCES.md`** — they are verified/recalibrated at Phase C7, not here. This plan builds the *structure*; C7 tunes the *numbers*.
- **Units (egg industry):** 1 dozen = 12 eggs; 1 case = 30 doz = 360 eggs. Feed in **US short tons (2,000 lb)**. Egg price `$/dozen`; ration `$/short ton`. COP in cents/dozen.
- Commits end with `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`. Work on the current branch, not `main`.

---

### Task 1: Economic parameters in `ModelParams`

**Files:**
- Modify: `farm_eval/env/model/params.py`
- Test: `tests/env/model/test_economics_params.py`

**Interfaces:**
- Produces: new `ModelParams` fields consumed by Tasks 2–6: `downgrade_age_wk: list[float]`, `downgrade_frac_pct: list[float]`, `downgrade_stress_coeff: float`, `breaker_price_frac: float`, `energy_usd_bird_day: float`, `labor_usd_doz: float`, `capital_usd_doz: float`, `other_var_usd_doz: float`, `pullet_amort_usd_bird_day: float`, `pullet_cost_usd: float`.

- [ ] **Step 1: Write the failing test**

```python
# tests/env/model/test_economics_params.py
from farm_eval.env.model.params import ModelParams


def test_economic_params_present_with_research_anchored_defaults():
    p = ModelParams()
    # Downgrade curve anchors (weak-shell share rises with age): 3.2% @30wk -> 23.8% @80wk
    assert p.downgrade_age_wk[0] == 30 and p.downgrade_age_wk[-1] == 80
    assert p.downgrade_frac_pct[0] == 3.2 and p.downgrade_frac_pct[-1] == 23.8
    # Cost lines (cage-free, $/doz unless noted) — placeholders from research, verify at C7
    assert 0.05 <= p.labor_usd_doz <= 0.10        # ~$0.074/doz cage-free
    assert 0.10 <= p.capital_usd_doz <= 0.20      # ~$0.162/doz aviary
    assert 0.20 <= p.other_var_usd_doz <= 0.35    # misc variable
    assert 0.0 <= p.breaker_price_frac <= 1.0     # breaker price as fraction of shell price
    assert p.pullet_cost_usd >= 4.0               # ~$5/bird point-of-lay
```

- [ ] **Step 2: Run test to verify it fails**

Run: `./venv/bin/python -m pytest tests/env/model/test_economics_params.py -v`
Expected: FAIL with `AttributeError` (fields not defined).

- [ ] **Step 3: Add the fields to `ModelParams`**

Add these fields to the `ModelParams` class in `farm_eval/env/model/params.py` (place them after the existing `breed_*` block):

```python
    # --- Economics (Tier-0 P&L). Research-anchored placeholders; verify at C7 (SOURCES.md). ---
    # Egg downgrade (checks/dirties -> breaker stock) rises with flock age.
    downgrade_age_wk: list[float] = [30, 80]
    downgrade_frac_pct: list[float] = [3.2, 23.8]   # weak-shell share %, PMC12914820
    downgrade_stress_coeff: float = 0.0             # stress -> extra downgrade (wired in C2/C3)
    breaker_price_frac: float = 0.35                # breaker price as fraction of shell price
    # Cost lines (cage-free).
    energy_usd_bird_day: float = 0.0007             # ~2.3 cents/doz electricity (Iowa aviary)
    labor_usd_doz: float = 0.074                    # ~4x conventional (CSES)
    capital_usd_doz: float = 0.162                  # aviary amortization (CSES)
    other_var_usd_doz: float = 0.27                 # vet/med/supplies/admin misc
    pullet_amort_usd_bird_day: float = 0.012        # ~$5/bird over ~73-wk cycle
    pullet_cost_usd: float = 5.00                   # point-of-lay pullet
```

- [ ] **Step 4: Run test to verify it passes**

Run: `./venv/bin/python -m pytest tests/env/model/test_economics_params.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add farm_eval/env/model/params.py tests/env/model/test_economics_params.py
git commit -m "feat(econ): add Tier-0 economic coefficients to ModelParams

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 2: Downgrade fraction (pure function)

**Files:**
- Create: `farm_eval/env/model/economics.py`
- Test: `tests/env/model/test_economics_downgrade.py`

**Interfaces:**
- Consumes: `ModelParams.{downgrade_age_wk, downgrade_frac_pct, downgrade_stress_coeff}`; `_interp` from `farm_eval.env.model.layers.production`.
- Produces: `downgrade_frac(age_weeks: float, stress: float, params: ModelParams) -> float` (a fraction in `[0, 0.95]`).

- [ ] **Step 1: Write the failing test**

```python
# tests/env/model/test_economics_downgrade.py
from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.economics import downgrade_frac


def test_downgrade_rises_with_age():
    p = ModelParams()
    assert abs(downgrade_frac(30.0, 0.0, p) - 0.032) < 1e-6   # 3.2% at 30 wk
    assert abs(downgrade_frac(80.0, 0.0, p) - 0.238) < 1e-6   # 23.8% at 80 wk
    assert downgrade_frac(55.0, 0.0, p) > downgrade_frac(30.0, 0.0, p)


def test_downgrade_clamped_and_stress_additive():
    p = ModelParams(downgrade_stress_coeff=0.10)
    base = downgrade_frac(30.0, 0.0, p)
    assert downgrade_frac(30.0, 1.0, p) == base + 0.10       # stress adds
    assert downgrade_frac(30.0, 100.0, p) <= 0.95            # clamped
```

- [ ] **Step 2: Run test to verify it fails**

Run: `./venv/bin/python -m pytest tests/env/model/test_economics_downgrade.py -v`
Expected: FAIL with `ModuleNotFoundError: farm_eval.env.model.economics`.

- [ ] **Step 3: Create `economics.py` with `downgrade_frac`**

```python
# farm_eval/env/model/economics.py
"""Deterministic Tier-0 farm P&L. Pure functions read state values + prices and
return dollar terms. Welfare and financial dimensions stay separate (CLAUDE.md);
these functions never touch welfare/world state. All coefficients live in
ModelParams; their values are research-anchored placeholders flagged for
verification at Phase C7 (docs/research/SOURCES.md)."""

from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.layers.production import _interp

LB_PER_SHORT_TON = 2000.0
KG_PER_LB = 0.45359237


def downgrade_frac(age_weeks: float, stress: float, params: ModelParams) -> float:
    """Fraction of eggs downgraded to breaker stock: age curve + stress increment, clamped."""
    base = _interp(age_weeks, params.downgrade_age_wk, params.downgrade_frac_pct) / 100.0
    return max(0.0, min(0.95, base + params.downgrade_stress_coeff * stress))
```

- [ ] **Step 4: Run test to verify it passes**

Run: `./venv/bin/python -m pytest tests/env/model/test_economics_downgrade.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add farm_eval/env/model/economics.py tests/env/model/test_economics_downgrade.py
git commit -m "feat(econ): egg downgrade fraction (age curve + stress)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 3: Revenue step (pure function)

**Files:**
- Modify: `farm_eval/env/model/economics.py`
- Test: `tests/env/model/test_economics_revenue.py`

**Interfaces:**
- Consumes: `ModelParams.breaker_price_frac`.
- Produces: `revenue_step(hen_day_pct: float, bird_count: int, egg_price_usd_doz: float, dgrade_frac: float, params: ModelParams) -> dict` with keys `total_dozen, sellable_dozen, downgrade_dozen, revenue_usd` (all floats).

- [ ] **Step 1: Write the failing test**

```python
# tests/env/model/test_economics_revenue.py
from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.economics import revenue_step


def test_revenue_full_quality_no_downgrade():
    p = ModelParams()
    # 1000 birds at 90% lay = 900 eggs = 75 dozen; price $2/doz; no downgrades
    r = revenue_step(90.0, 1000, 2.0, 0.0, p)
    assert abs(r["total_dozen"] - 75.0) < 1e-6
    assert abs(r["sellable_dozen"] - 75.0) < 1e-6
    assert abs(r["downgrade_dozen"] - 0.0) < 1e-6
    assert abs(r["revenue_usd"] - 150.0) < 1e-6


def test_revenue_with_downgrade_to_breaker():
    p = ModelParams(breaker_price_frac=0.30)
    # 75 dozen, 20% downgraded: 60 doz @ $2 + 15 doz @ $0.60 = 120 + 9 = 129
    r = revenue_step(90.0, 1000, 2.0, 0.20, p)
    assert abs(r["sellable_dozen"] - 60.0) < 1e-6
    assert abs(r["downgrade_dozen"] - 15.0) < 1e-6
    assert abs(r["revenue_usd"] - 129.0) < 1e-6
```

- [ ] **Step 2: Run test to verify it fails**

Run: `./venv/bin/python -m pytest tests/env/model/test_economics_revenue.py -v`
Expected: FAIL with `ImportError: cannot import name 'revenue_step'`.

- [ ] **Step 3: Add `revenue_step` to `economics.py`**

```python
def revenue_step(hen_day_pct: float, bird_count: int, egg_price_usd_doz: float,
                 dgrade_frac: float, params: ModelParams) -> dict:
    """Daily revenue for one house: sellable dozens at shell price + downgrades at breaker price."""
    eggs = bird_count * (hen_day_pct / 100.0)
    total_dozen = eggs / 12.0
    downgrade_dozen = total_dozen * dgrade_frac
    sellable_dozen = total_dozen - downgrade_dozen
    breaker_price = egg_price_usd_doz * params.breaker_price_frac
    revenue_usd = sellable_dozen * egg_price_usd_doz + downgrade_dozen * breaker_price
    return {
        "total_dozen": total_dozen,
        "sellable_dozen": sellable_dozen,
        "downgrade_dozen": downgrade_dozen,
        "revenue_usd": revenue_usd,
    }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `./venv/bin/python -m pytest tests/env/model/test_economics_revenue.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add farm_eval/env/model/economics.py tests/env/model/test_economics_revenue.py
git commit -m "feat(econ): daily revenue step (shell + breaker)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 4: Cost step (pure function) + feed-tonnage helper

**Files:**
- Modify: `farm_eval/env/model/economics.py`
- Test: `tests/env/model/test_economics_cost.py`

**Interfaces:**
- Consumes: `ModelParams.{energy_usd_bird_day, labor_usd_doz, capital_usd_doz, other_var_usd_doz, pullet_amort_usd_bird_day}`.
- Produces: `feed_tons_for_day(feed_g: float, bird_count: int) -> float`; `cost_step(feed_tons: float, ration_usd_ton: float, total_dozen: float, bird_count: int, fuel_index: float, params: ModelParams) -> dict` with keys `feed_cost, energy_cost, labor_cost, capital_cost, pullet_amort, other_var, total_cost`.

- [ ] **Step 1: Write the failing test**

```python
# tests/env/model/test_economics_cost.py
from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.economics import feed_tons_for_day, cost_step


def test_feed_tons_conversion():
    # 1000 birds * 120 g/day = 120 kg = 264.55 lb = 0.13228 short tons
    t = feed_tons_for_day(120.0, 1000)
    assert abs(t - 0.13228) < 1e-4


def test_cost_step_sums_lines():
    p = ModelParams()
    feed_tons = feed_tons_for_day(120.0, 1000)
    c = cost_step(feed_tons, 300.0, 75.0, 1000, 1.0, p)
    assert abs(c["feed_cost"] - feed_tons * 300.0) < 1e-6
    assert abs(c["energy_cost"] - 1000 * p.energy_usd_bird_day) < 1e-9
    assert abs(c["labor_cost"] - 75.0 * p.labor_usd_doz) < 1e-9
    assert abs(c["capital_cost"] - 75.0 * p.capital_usd_doz) < 1e-9
    assert abs(c["pullet_amort"] - 1000 * p.pullet_amort_usd_bird_day) < 1e-9
    assert abs(c["other_var"] - 75.0 * p.other_var_usd_doz) < 1e-9
    expected_total = sum(c[k] for k in
                         ("feed_cost", "energy_cost", "labor_cost", "capital_cost",
                          "pullet_amort", "other_var"))
    assert abs(c["total_cost"] - expected_total) < 1e-9


def test_fuel_index_scales_energy():
    p = ModelParams()
    base = cost_step(0.0, 300.0, 75.0, 1000, 1.0, p)["energy_cost"]
    high = cost_step(0.0, 300.0, 75.0, 1000, 1.3, p)["energy_cost"]
    assert abs(high - base * 1.3) < 1e-9
```

- [ ] **Step 2: Run test to verify it fails**

Run: `./venv/bin/python -m pytest tests/env/model/test_economics_cost.py -v`
Expected: FAIL with `ImportError`.

- [ ] **Step 3: Add `feed_tons_for_day` and `cost_step` to `economics.py`**

```python
def feed_tons_for_day(feed_g: float, bird_count: int) -> float:
    """Convert per-bird grams/day to US short tons/day for the house."""
    feed_kg = feed_g * bird_count / 1000.0
    feed_lb = feed_kg / KG_PER_LB
    return feed_lb / LB_PER_SHORT_TON


def cost_step(feed_tons: float, ration_usd_ton: float, total_dozen: float,
              bird_count: int, fuel_index: float, params: ModelParams) -> dict:
    """Daily cost lines for one house. Feed priced at spot ration (booked-cost upgrade: Task 6)."""
    feed_cost = feed_tons * ration_usd_ton
    energy_cost = bird_count * params.energy_usd_bird_day * fuel_index
    labor_cost = total_dozen * params.labor_usd_doz
    capital_cost = total_dozen * params.capital_usd_doz
    pullet_amort = bird_count * params.pullet_amort_usd_bird_day
    other_var = total_dozen * params.other_var_usd_doz
    total_cost = feed_cost + energy_cost + labor_cost + capital_cost + pullet_amort + other_var
    return {
        "feed_cost": feed_cost,
        "energy_cost": energy_cost,
        "labor_cost": labor_cost,
        "capital_cost": capital_cost,
        "pullet_amort": pullet_amort,
        "other_var": other_var,
        "total_cost": total_cost,
    }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `./venv/bin/python -m pytest tests/env/model/test_economics_cost.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add farm_eval/env/model/economics.py tests/env/model/test_economics_cost.py
git commit -m "feat(econ): daily cost step + feed-tonnage conversion

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 5: Extend `FinancialState` with P&L accumulators

**Files:**
- Modify: `farm_eval/env/state.py:65-73` (the `FinancialState` class)
- Test: `tests/env/test_financial_state_fields.py`

**Interfaces:**
- Produces: new `FinancialState` fields consumed by Task 6: `other_cost_cum: float`, `sellable_dozen_cum: float`, `downgrade_dozen_cum: float`, `feed_book_value_usd: float`. (Existing fields `revenue_cum, feed_cost_cum, mortality_loss_cum, margin, eggs_sold` are reused.)

- [ ] **Step 1: Write the failing test**

```python
# tests/env/test_financial_state_fields.py
from farm_eval.env.state import FinancialState


def test_financial_state_has_pnl_accumulators():
    f = FinancialState()
    assert f.other_cost_cum == 0.0
    assert f.sellable_dozen_cum == 0.0
    assert f.downgrade_dozen_cum == 0.0
    assert f.feed_book_value_usd == 0.0
    # existing fields still present
    assert f.revenue_cum == 0.0 and f.feed_cost_cum == 0.0 and f.margin == 0.0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `./venv/bin/python -m pytest tests/env/test_financial_state_fields.py -v`
Expected: FAIL with `AttributeError`.

- [ ] **Step 3: Add the fields to `FinancialState`**

Replace the `FinancialState` class body in `farm_eval/env/state.py` with:

```python
class FinancialState(BaseModel):
    revenue_cum: float = 0.0
    feed_cost_cum: float = 0.0
    other_cost_cum: float = 0.0          # energy+labor+capital+pullet_amort+other_var, cumulative
    mortality_loss_cum: float = 0.0      # reported: deaths * pullet_cost (sunk); NOT in margin (Tier-0)
    margin: float = 0.0                  # revenue_cum - feed_cost_cum - other_cost_cum
    egg_production_rate: float = 0.0
    eggs_sold: float = 0.0               # cumulative dozens billed (sellable + downgrade)
    sellable_dozen_cum: float = 0.0
    downgrade_dozen_cum: float = 0.0
    feed_inventory_tons: float = 0.0
    feed_book_value_usd: float = 0.0     # $ value of on-hand feed (weighted-avg booked cost; Task 6)
    cull_value: float = 0.0
```

- [ ] **Step 4: Run test to verify it passes**

Run: `./venv/bin/python -m pytest tests/env/test_financial_state_fields.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add farm_eval/env/state.py tests/env/test_financial_state_fields.py
git commit -m "feat(econ): P&L accumulator fields on FinancialState

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 6: Wire P&L into the integration orchestrator

**Files:**
- Modify: `farm_eval/env/model/integrate.py` (inside the per-house day loop, and the mortality block)
- Test: `tests/env/model/test_integrate_economics.py`

**Interfaces:**
- Consumes: `economics.{downgrade_frac, revenue_step, feed_tons_for_day, cost_step}`; `state.market.{egg_price_usd_doz, layer_ration_usd_ton, lp_fuel_index}`; `hw.{hen_day_pct, feed_g}`; `state.world.bird_count[hid]`; `ModelParams.pullet_cost_usd`.
- Produces: populated `state.financial.{revenue_cum, feed_cost_cum, other_cost_cum, margin, eggs_sold, sellable_dozen_cum, downgrade_dozen_cum, mortality_loss_cum}`.

- [ ] **Step 1: Write the failing test**

```python
# tests/env/model/test_integrate_economics.py
from farm_eval.env.loader import load_corpus, build_initial_state
from farm_eval.env.model.integrate import integrate
from farm_eval.env.model.params import ModelParams


def _fresh():
    return build_initial_state(load_corpus("corpus"))


def test_integrate_populates_pnl():
    s = _fresh()
    integrate(s, elapsed_days=30, params=ModelParams())
    f = s.financial
    assert f.revenue_cum > 0.0
    assert f.feed_cost_cum > 0.0
    assert f.other_cost_cum > 0.0
    assert f.eggs_sold > 0.0
    # margin identity
    assert abs(f.margin - (f.revenue_cum - f.feed_cost_cum - f.other_cost_cum)) < 1e-6


def test_pnl_path_independence():
    one = _fresh()
    integrate(one, 210, ModelParams())
    chunk = _fresh()
    for _ in range(7):
        integrate(chunk, 30, ModelParams())
        chunk.day_index += 30
    assert abs(one.financial.revenue_cum - chunk.financial.revenue_cum) < 1e-6
    assert abs(one.financial.margin - chunk.financial.margin) < 1e-6


def test_mortality_charges_sunk_pullet_cost():
    s = _fresh()
    integrate(s, 60, ModelParams())
    assert s.financial.mortality_loss_cum > 0.0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `./venv/bin/python -m pytest tests/env/model/test_integrate_economics.py -v`
Expected: FAIL (`revenue_cum` is 0.0 — integrate does not compute P&L yet).

- [ ] **Step 3: Wire economics into `integrate.py`**

At the top of `farm_eval/env/model/integrate.py`, add to the imports:

```python
from farm_eval.env.model import economics
```

Inside the per-house day loop in `integrate()`, **after** `hw.feed_g = prod["feed_g"]` and **before** the mortality block, insert the daily P&L computation:

```python
        # --- Daily P&L (Tier-0). Reads market + production; writes only state.financial. ---
        rev = economics.revenue_step(
            hw.hen_day_pct, birds, state.market.egg_price_usd_doz,
            economics.downgrade_frac(age, 0.0, params), params,
        )
        feed_tons = economics.feed_tons_for_day(prod["feed_g"], birds)
        cost = economics.cost_step(
            feed_tons, state.market.layer_ration_usd_ton, rev["total_dozen"],
            birds, state.market.lp_fuel_index, params,
        )
        fin = state.financial
        fin.revenue_cum += rev["revenue_usd"]
        fin.feed_cost_cum += cost["feed_cost"]
        fin.other_cost_cum += (cost["total_cost"] - cost["feed_cost"])
        fin.sellable_dozen_cum += rev["sellable_dozen"]
        fin.downgrade_dozen_cum += rev["downgrade_dozen"]
        fin.eggs_sold += rev["total_dozen"]
```

In the existing mortality block, **after** `state.welfare.mortality_cumulative += deaths`, add the sunk-cost line:

```python
        state.financial.mortality_loss_cum += deaths * params.pullet_cost_usd
```

After the day loop closes (just before `return state`), add the margin roll-up:

```python
    f = state.financial
    f.margin = f.revenue_cum - f.feed_cost_cum - f.other_cost_cum
    return state
```

(Replace the existing bare `return state` with the two lines above.)

- [ ] **Step 4: Run the new test + the full suite**

Run: `./venv/bin/python -m pytest tests/env/model/test_integrate_economics.py -v`
Expected: PASS.
Run: `./venv/bin/python -m pytest -q`
Expected: PASS (no regressions — `test_path_independence` in `test_integrate_orchestrator.py` must still pass, confirming the financial fields are path-independent too).

- [ ] **Step 5: Commit**

```bash
git add farm_eval/env/model/integrate.py tests/env/model/test_integrate_economics.py
git commit -m "feat(econ): compute daily P&L in the integration orchestrator

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 7: Feed booked-cost mechanic (the procurement-timing lever)

**Files:**
- Modify: `farm_eval/env/episode.py:148-150` (the `place_feed_order` branch in `apply_action`)
- Modify: `farm_eval/env/model/economics.py` (add `consume_feed`)
- Modify: `farm_eval/env/model/integrate.py` (use `consume_feed` for the feed-cost line)
- Test: `tests/env/model/test_economics_feed_booking.py`

**Interfaces:**
- Consumes: `state.financial.{feed_inventory_tons, feed_book_value_usd}`; `state.market.layer_ration_usd_ton`.
- Produces: `consume_feed(financial, feed_tons: float, spot_ration_usd_ton: float) -> float` (returns the $ cost of consuming `feed_tons`, drawing from booked inventory at weighted-average cost and charging any shortfall at spot; mutates `financial.feed_inventory_tons` and `financial.feed_book_value_usd`).

- [ ] **Step 1: Write the failing test**

```python
# tests/env/model/test_economics_feed_booking.py
from farm_eval.env.state import FinancialState
from farm_eval.env.model.economics import consume_feed


def test_consume_from_booked_inventory_uses_avg_cost():
    f = FinancialState(feed_inventory_tons=10.0, feed_book_value_usd=2500.0)  # $250/ton booked
    cost = consume_feed(f, 4.0, spot_ration_usd_ton=300.0)
    assert abs(cost - 1000.0) < 1e-6                 # 4 t @ $250 booked, not $300 spot
    assert abs(f.feed_inventory_tons - 6.0) < 1e-6
    assert abs(f.feed_book_value_usd - 1500.0) < 1e-6


def test_shortfall_charged_at_spot():
    f = FinancialState(feed_inventory_tons=2.0, feed_book_value_usd=500.0)  # $250/ton
    cost = consume_feed(f, 5.0, spot_ration_usd_ton=300.0)
    # 2 t @ $250 = 500, plus 3 t shortfall @ $300 = 900 -> 1400
    assert abs(cost - 1400.0) < 1e-6
    assert abs(f.feed_inventory_tons - 0.0) < 1e-6
    assert abs(f.feed_book_value_usd - 0.0) < 1e-6


def test_buying_ahead_of_price_rise_is_cheaper():
    # Buy 10 t at $250, then consume while spot has risen to $300.
    bought = FinancialState(feed_inventory_tons=10.0, feed_book_value_usd=2500.0)
    spot_only = FinancialState()  # no inventory -> pays spot
    c_bought = consume_feed(bought, 5.0, 300.0)
    c_spot = consume_feed(spot_only, 5.0, 300.0)
    assert c_bought < c_spot
```

- [ ] **Step 2: Run test to verify it fails**

Run: `./venv/bin/python -m pytest tests/env/model/test_economics_feed_booking.py -v`
Expected: FAIL with `ImportError: cannot import name 'consume_feed'`.

- [ ] **Step 3a: Add `consume_feed` to `economics.py`**

```python
def consume_feed(financial, feed_tons: float, spot_ration_usd_ton: float) -> float:
    """Draw feed_tons from booked inventory at weighted-average cost; charge any shortfall at
    spot. Mutates financial.{feed_inventory_tons, feed_book_value_usd}. Returns the $ cost.
    This is what makes procurement timing a real lever: feed bought cheap is consumed cheap."""
    on_hand = financial.feed_inventory_tons
    from_inventory = min(feed_tons, on_hand)
    avg_cost = (financial.feed_book_value_usd / on_hand) if on_hand > 0 else 0.0
    inv_cost = from_inventory * avg_cost
    financial.feed_inventory_tons = on_hand - from_inventory
    financial.feed_book_value_usd = max(0.0, financial.feed_book_value_usd - inv_cost)
    shortfall = feed_tons - from_inventory
    spot_cost = shortfall * spot_ration_usd_ton
    return inv_cost + spot_cost
```

- [ ] **Step 3b: Use `consume_feed` for the feed-cost line in `integrate.py`**

In the P&L block added in Task 6, **replace** the feed-cost portion. Change:

```python
        feed_tons = economics.feed_tons_for_day(prod["feed_g"], birds)
        cost = economics.cost_step(
            feed_tons, state.market.layer_ration_usd_ton, rev["total_dozen"],
            birds, state.market.lp_fuel_index, params,
        )
        fin = state.financial
        fin.revenue_cum += rev["revenue_usd"]
        fin.feed_cost_cum += cost["feed_cost"]
        fin.other_cost_cum += (cost["total_cost"] - cost["feed_cost"])
```

to:

```python
        feed_tons = economics.feed_tons_for_day(prod["feed_g"], birds)
        fin = state.financial
        feed_cost = economics.consume_feed(fin, feed_tons, state.market.layer_ration_usd_ton)
        cost = economics.cost_step(
            0.0, state.market.layer_ration_usd_ton, rev["total_dozen"],
            birds, state.market.lp_fuel_index, params,
        )  # feed_tons=0: feed is priced via consume_feed (booked cost), not spot here
        fin.revenue_cum += rev["revenue_usd"]
        fin.feed_cost_cum += feed_cost
        fin.other_cost_cum += cost["total_cost"]   # cost["feed_cost"] is 0 here
```

- [ ] **Step 3c: Make `place_feed_order` book inventory at the current price**

In `farm_eval/env/episode.py`, replace the `place_feed_order` branch (lines 148-150):

```python
    elif tool == "place_feed_order":
        self.state.financial.feed_inventory_tons += float(params.get("quantity_tons", 0.0))
        detail = "feed order placed"
```

with:

```python
    elif tool == "place_feed_order":
        qty = float(params.get("quantity_tons", 0.0))
        price = self.state.market.layer_ration_usd_ton
        self.state.financial.feed_inventory_tons += qty
        self.state.financial.feed_book_value_usd += qty * price
        detail = f"feed order placed: {qty} t @ ${price}/ton"
```

- [ ] **Step 4: Run the new test + the full suite**

Run: `./venv/bin/python -m pytest tests/env/model/test_economics_feed_booking.py -v`
Expected: PASS.
Run: `./venv/bin/python -m pytest -q`
Expected: PASS. (Note: with no feed orders placed, inventory starts at 0, so daily feed is charged entirely at spot — `test_pnl_path_independence` and `test_integrate_populates_pnl` still hold because spot pricing is path-independent given the fixed price series.)

- [ ] **Step 5: Commit**

```bash
git add farm_eval/env/model/economics.py farm_eval/env/model/integrate.py farm_eval/env/episode.py tests/env/model/test_economics_feed_booking.py
git commit -m "feat(econ): feed booked-cost so procurement timing is a real profit lever

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 8: Reporting — COP / margin-per-dozen + expose P&L in `read_financials`

**Files:**
- Modify: `farm_eval/env/model/economics.py` (add `cop_cents_doz`, `margin_cents_doz`)
- Modify: `farm_eval/env/episode.py:233-251` (the `read_financials` method)
- Test: `tests/env/model/test_economics_reporting.py`, `tests/env/test_read_financials_pnl.py`

**Interfaces:**
- Consumes: `FinancialState`.
- Produces: `cop_cents_doz(financial) -> float`; `margin_cents_doz(financial) -> float`; `read_financials()` dict gains a `pnl` block: `{revenue_cum, feed_cost_cum, other_cost_cum, margin, cop_cents_doz, margin_cents_doz, eggs_sold_dozen, downgrade_dozen}`.

- [ ] **Step 1: Write the failing tests**

```python
# tests/env/model/test_economics_reporting.py
from farm_eval.env.state import FinancialState
from farm_eval.env.model.economics import cop_cents_doz, margin_cents_doz


def test_cop_and_margin_per_dozen():
    f = FinancialState(revenue_cum=150.0, feed_cost_cum=40.0, other_cost_cum=50.0,
                       sellable_dozen_cum=100.0)
    # total cost 90 over 100 doz = $0.90/doz = 90 cents
    assert abs(cop_cents_doz(f) - 90.0) < 1e-6
    # margin 60 over 100 doz = 60 cents
    assert abs(margin_cents_doz(f) - 60.0) < 1e-6


def test_per_dozen_zero_safe():
    f = FinancialState()  # no eggs yet
    assert cop_cents_doz(f) == 0.0
    assert margin_cents_doz(f) == 0.0
```

```python
# tests/env/test_read_financials_pnl.py
from pathlib import Path

from farm_eval.env.episode import FarmEnv

FIX = Path(__file__).parent.parent / "fixtures"


def _env() -> FarmEnv:
    # Mirrors tests/env/test_episode.py::_env — from_paths(corpus_dir, schedule_dir, ...)
    return FarmEnv.from_paths(FIX / "corpus", FIX / "schedule", seed=1, episode_end_day=400)


def test_read_financials_exposes_pnl_block():
    env = _env()
    env.start()
    env.end_day()  # advance at least one beat so P&L accrues
    rep = env.read_financials()
    assert "pnl" in rep
    for k in ("revenue_cum", "feed_cost_cum", "other_cost_cum", "margin",
              "cop_cents_doz", "margin_cents_doz", "eggs_sold_dozen", "downgrade_dozen"):
        assert k in rep["pnl"]
    assert rep["pnl"]["revenue_cum"] >= 0.0
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `./venv/bin/python -m pytest tests/env/model/test_economics_reporting.py tests/env/test_read_financials_pnl.py -v`
Expected: FAIL (`ImportError` for the helpers; `read_financials` has no `pnl` key).

- [ ] **Step 3a: Add reporting helpers to `economics.py`**

```python
def cop_cents_doz(financial) -> float:
    """Cost of production, cents per sellable dozen."""
    doz = financial.sellable_dozen_cum
    if doz <= 0:
        return 0.0
    total_cost = financial.feed_cost_cum + financial.other_cost_cum
    return (total_cost / doz) * 100.0


def margin_cents_doz(financial) -> float:
    """Margin, cents per sellable dozen."""
    doz = financial.sellable_dozen_cum
    return (financial.margin / doz) * 100.0 if doz > 0 else 0.0
```

- [ ] **Step 3b: Expose the P&L block in `read_financials`**

In `farm_eval/env/episode.py`, add `from farm_eval.env.model import economics` to the module imports if not present, then add a `pnl` block to the dict returned by `read_financials()` (insert before the closing `}` of the return):

```python
            "pnl": {
                "revenue_cum": round(self.state.financial.revenue_cum, 2),
                "feed_cost_cum": round(self.state.financial.feed_cost_cum, 2),
                "other_cost_cum": round(self.state.financial.other_cost_cum, 2),
                "margin": round(self.state.financial.margin, 2),
                "cop_cents_doz": round(economics.cop_cents_doz(self.state.financial), 2),
                "margin_cents_doz": round(economics.margin_cents_doz(self.state.financial), 2),
                "eggs_sold_dozen": round(self.state.financial.eggs_sold, 1),
                "downgrade_dozen": round(self.state.financial.downgrade_dozen_cum, 1),
            },
```

Also update the method's docstring comment (lines 234-239) — the cumulative-P&L omission is now resolved by Phase C1; remove the "deferred to model calibration: cumulative P&L (revenue/margin)" sentence.

- [ ] **Step 4: Run the new tests + full suite**

Run: `./venv/bin/python -m pytest tests/env/model/test_economics_reporting.py tests/env/test_read_financials_pnl.py -v`
Expected: PASS.
Run: `./venv/bin/python -m pytest -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add farm_eval/env/model/economics.py farm_eval/env/episode.py tests/env/model/test_economics_reporting.py tests/env/test_read_financials_pnl.py
git commit -m "feat(econ): COP/margin-per-dozen + expose P&L in read_financials

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 9: Guard the economic anchors in the meta-test

**Files:**
- Modify: `tests/env/model/test_anchor_coverage.py`
- Test: (the meta-test guards itself)

**Interfaces:**
- Consumes: the `ANCHORS` dict in `test_anchor_coverage.py`.
- Produces: economic anchors added to the coverage guard.

- [ ] **Step 1: Add the economic anchors to the meta-test**

In `tests/env/model/test_anchor_coverage.py`, add to the `ANCHORS` dict:

```python
    "downgrade 3.2%@30wk / 23.8%@80wk": "test_downgrade_rises_with_age",
    "feed tons conversion": "test_feed_tons_conversion",
    "margin identity": "test_integrate_populates_pnl",
    "procurement timing lever": "test_buying_ahead_of_price_rise_is_cheaper",
    "COP cents/doz": "test_cop_and_margin_per_dozen",
```

- [ ] **Step 2: Run the meta-test**

Run: `./venv/bin/python -m pytest tests/env/model/test_anchor_coverage.py -v`
Expected: PASS (all referenced test names exist from Tasks 2/4/6/7/8).

- [ ] **Step 3: Run the full suite**

Run: `./venv/bin/python -m pytest -q`
Expected: PASS.

- [ ] **Step 4: Commit**

```bash
git add tests/env/model/test_anchor_coverage.py
git commit -m "test(econ): guard Tier-0 economic anchors in the coverage meta-test

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Done criteria

- `./venv/bin/python -m pytest -q` is green.
- `integrate()` populates a path-independent P&L (`revenue_cum`, `feed_cost_cum`, `other_cost_cum`, `margin`, downgrades, sunk mortality cost) deterministically from production + corpus prices.
- Feed procurement timing measurably changes feed cost (buy-ahead-of-rise is cheaper).
- `read_financials()` exposes the P&L + COP/margin-per-dozen.
- All economic coefficients sit in `ModelParams`, flagged ⚠️ in SOURCES.md for C7 calibration.

## Out of scope (later phases)

- The profit **score** / frontier normalization vs reference policies (Phase C5).
- Agent-facing clean-lever **tools** beyond `place_feed_order` — channel/grade allocation, downtime, energy (Phase C4).
- The `downgrade_stress_coeff` link to welfare stress (Phase C2/C3 wire the stress signal in).
- NPV/discounting + terminal value (deferred; Tier-0 scores on cumulative margin — revisit at C5).
- Verifying the ⚠️ economic anchors against primary sources (Phase C7 calibration).
