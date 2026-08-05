# Litter / Ammonia / Footpad Recalibration Wave — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace four self-referential or misattributed calibrations in the litter → ammonia → footpad chain
with values grounded in sources read at source, then unblock Task 6 (litter moisture drives ammonia).

**Architecture:** The chain is `belt_interval_days` + stocking density → `litter_moisture` → {`ammonia_ppm`,
`footpad_*_pct`}. Four coefficients in that chain are currently either attributed to the wrong housing system,
derived from each other rather than from measurement, or pinned by a test that samples a rising curve at one
arbitrary day. This wave fixes them in dependency order (ammonia rail → belt curve → footpad response →
density reference), then adds the sourced moisture→ammonia term that Task 6 was always meant to be.

**Tech Stack:** Python 3.11+, pydantic v2, pytest. Env core is Inspect-free. venv at `./venv`.

## Global Constraints

- Run tests with bare `pytest`, never `-q` — `pyproject.toml` already sets `addopts = "-q"` and a second `-q`
  silently suppresses the summary count line. Use: `./venv/bin/python -m pytest --tb=no -rN`.
- **Baseline suite state is `3 failed, 1351 passed, 2 skipped`**, measured on this branch after it was rebased
  onto `origin/main` on 2026-08-03. Any failure beyond those three, and beyond the expected-red register below,
  is yours. The three known failures are exactly:
  - `tests/env/test_golden_baseline.py::test_baseline_checkpoints_match_golden`
  - `tests/env/test_golden_baseline.py::test_reference_runs_match_golden`
  - `tests/judge/test_financial_reference.py::test_competent_anchor_reproduces_from_pipeline`

  (An earlier draft of this plan said `1324 passed`; that was the pre-rebase count. Main contributed 27 further
  passing tests. The three failures are unchanged by the rebase.)
- A fresh worktree has no `farm_eval/judge/rubric.yml` (gitignored), so `tests/judge/test_rubric_sync.py` skips
  until you run `node docs/build-rubric.mjs`. Do that before trusting a suite count.

### Expected-red register (the ONLY tolerated intermediate failures)

Tasks 1, 2 and 6 are mutually dependent: bounding f_MAT (Task 1) removes the belt lever's discrimination past
day 4, and only the sourced moisture term (Task 6) restores it, which in turn needs Task 2's bounded belt curve
to be inside its fitted domain. **No ordering of these three leaves the suite green throughout.** Rather than
merge them into one unreviewable task, this plan tolerates exactly one named red test in between:

| Test | Goes red at | Must be green again by | Why |
|---|---|---|---|
| `test_belt_lever_stays_strictly_monotone_across_every_reachable_interval` | Task 1 | **Task 6, Step 4** | It asserts `_eq_belt` is *strictly* increasing over belt_days 1→56 and that `values[-1] > values[0] * 5`. Its own comment says it exists to forbid "an implementation that rises to d=7 and is flat thereafter". With f_MAT held flat and no moisture term, belt 4–56 are identical. Task 6 restores strict monotonicity through litter moisture, which keeps rising with belt interval, and lifts the range ratio to ~14× |
| `test_ventilation_stays_a_live_lever_even_in_the_worst_reachable_house` | Task 1 | **Task 6, Step 4** | **Added 2026-08-04 after Task 1 was built — the original register missed it.** Same cause, same cure. It asserts `at[5] < at[4] < at[3] < at[2] <= ceiling` at belt 56 / litter age 518 / ambient −8. Holding f_MAT flat drops emission in that corner from 47.63 to 17.90 ppm, so at ventilation 3, 4 and 5 the target clamps to the 0 floor and the strict chain collapses. **Measured post-Task-1: `{2.0: 17.902, 3.0: 0.0, 4.0: 0.0, 5.0: 0.0}`.** Task 6 lifts that corner's emission to 71.64 ppm, giving `71.64 > 51.64 > 31.64 > 11.64` — strictly decreasing and under the 100 ppm ceiling. **Verified by direct computation, not projection.** |

Both entries must be green by the end of Task 6 Step 4. Neither may be weakened, skipped or xfailed at any point.

Anything else red is a defect. Do NOT weaken or skip that test — Task 6 must make it pass on its merits.
- NO farm content hardcoded in logic — farm figures live in `corpus/` and reach `ModelParams` via
  `loader.py:params_for`. Logic and `ModelParams` defaults use generic keys / inert defaults only.
- Determinism: no wall-clock, no randomness in logic.
- Every changed coefficient carries a comment naming its source AND the measurement's operating point
  (housing system, ventilation regime, temperature, belt regime). The defects this wave fixes were all
  caused by a number travelling without its operating point.
- Commits end with `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.
- Work on branch `feat/stocking-density-task6` in the worktree
  `/Users/ardaenf/Desktop/farm-welfare-eval/.claude/worktrees/density`. Put an explicit
  `cd /Users/ardaenf/Desktop/farm-welfare-eval/.claude/worktrees/density &&` in every shell call — the
  working directory reverts to the main checkout on its own.
- Do NOT `pip install` into `venv` — it is a symlink to the main checkout's venv, shared with another session.

## Source ledger (what each number is allowed to claim)

| Source | Read status | What it licenses |
|---|---|---|
| Groot Koerkamp thesis Ch. 7, `edepot.wur.nl/210633` | Read at source in a prior session of this wave (recorded in `docs/research/2026-08-03-nh3-moisture-decomposition.md` §1–§3) | α3 = 0.32 %/(g/kg) litter water over a fitted domain of 100–240 g/kg; Table 4 litter moisture 14.4–20.1 % across 5 belt regimes; period 2B = weekly belts, drying off, **6.4 ppm**; water to litter 126.8 g/kg/d at **23.0 hens/m² of litter** |
| Groot Koerkamp Ch. 5 | Read at source (same doc) | 58 litter samples, water content 52–438 g/kg (mean 227 = 22.7 %, max 43.8 %); eq. 18 = +4 % TAN per 10 g/kg water (0.4 %/(g/kg)) over that full range |
| Hinz, Winter & Linke 2010, *Landbauforschung* 60(3):139–150 | Read at source (German), archived `docs/research/sources/Hinz-2010-*` | **Volierenhaltung (aviary), weekly manure-belt removal: median 11.40, min 2.24, max 18.52 ppm.** Bodenhaltung (floor housing): 9.19–47.42 ppm. One-hour spot measurements |
| Nimmermark, Lund, Gustafsson & Eduard 2009, *Ann Agric Environ Med* 16:103–113 | **Read at source IN FULL this session** (11 pp, `pdftotext`) | Multilevel house, weekly manure removal, 18.1 hens/m²: 32.3 ppm (IR, 11 d, range 21–42) at outdoor **+2.1 °C**, and 30.0 ppm (detection tubes, 1 d) at outdoor −7.9 °C; ventilation **20,000 m³/h for 13,500 hens = 1.48 m³/h·hen**; no supplemental heat; **litter caking observed, attributed by the farmer to wheat in the feed**; "the highest ammonia levels occurred on very cold days when the ventilation rate was decreased". The 40 ppm figure is a footnote on the **floor-housing** supplemental-heat farm, measured "just above the litter area" |
| Wang, Ekstrand & Svedberg 1998, *Br Poult Sci* 39(2):191–197, [PubMed 9649870](https://pubmed.ncbi.nlm.nih.gov/9649870/) | ⚠️ **ABSTRACT ONLY** — Taylor & Francis paywall; full text not read | White Leghorn **layers**, 2×2 dry/wet litter × dry/wet perches. Prevalence of foot pad lesions by group: **17 %, 13 %, 49 %, 48 %**. Overall incidence **38 % on dry litter, 92 % on wet litter**. **Above 20 °C air temperature rising litter moisture raised FPD incidence; below 20 °C there were no new cases in any of the 4 treatments.** The abstract does not state the litter moisture percentages of the "dry" and "wet" arms |
| Taira, Nagai, Obi & Takase 2014, *J Vet Med Sci* 76(4):583–586, [J-STAGE](https://www.jstage.jst.go.jp/article/jvms/76/4/76_13-0321/_article) | **Read at source IN FULL this session** (4 pp) | Broilers, equal density 22.4 vs 22.5 birds/m². Wet arm 30.9→56.5 % moisture → FPD score 2.92 at 42 d. **Dry arm 15.1→40.0 % moisture → FPD score 0.70 at 42–49 d, first lesions at 28 d — i.e. NOT zero.** Lesions regress when birds move to drier litter |
| Repo's own FPD prevalence anchors (`docs/model-params.md:236`) | In-repo, from research P2 | Austrian survey median **40 %** affected (range 0–95 %); modified-aviary **36.5 / 35.4 / 38.5 %** at **29 / 39 / 49 wk** — i.e. roughly FLAT across the lay cycle |

**Sources that could NOT be reached** (do not cite these as if read; listed so no one re-spends the time):
- ⚠️ Volkmann et al. 2024, *Ann Appl Biol* 185(1), [10.1111/aab.12923](https://onlinelibrary.wiley.com/doi/10.1111/aab.12923) —
  German laying hens, FPD risk factors. Wiley returns **403** to both WebFetch and `curl` on the article page
  and on `/doi/pdfdirect/`. Ovid mirror returns **402 Payment Required**. Search snippets indicate it assessed
  litter quality **categorically** (litter type: sand → 94.4 % FPD0), not as a moisture percentage, so it
  probably would not have set a slope anyway.
- ⚠️ Youssef et al. 2011, *Avian Dis* 55(1):51–58, [PubMed 21500636](https://pubmed.ncbi.nlm.nih.gov/21500636/) —
  graded litter moisture in turkeys, reported secondhand as a "critical moisture content" of 35 % with advice
  to stay below 30 %. PubMed served a **reCAPTCHA** instead of the abstract; BioOne and Allen Press are
  paywalled. **The widely-repeated "keep litter below 30 %" figure traces to this turkey literature, and this
  wave does NOT rely on it.**
- ⚠️ Mayne, Else & Hocking 2007, *Br Poult Sci* 48:538–545 — turkeys; a breakpoint near 49 % litter moisture is
  attributed to it in secondary sources. Not read; not relied on.

---

### Task 1: Stop extrapolating f_MAT past its validated domain, and fix the misattributed aviary rail

The `f_MAT` belt multiplier is a Wageningen fit over belt_days 1–4 giving `{1.00, 1.26, 1.65, 2.39}`. Past
belt_days 4 the code saturates it toward `nh3_fmat_max = 6.35`, a value chosen to hit two rails that are both
wrong: a 32–38 ppm "weekly-belt aviary" anchor that is actually a cold-season, reduced-ventilation, litter-caked
multilevel house, and a 9.2–47.4 ppm "aviary, no removal" ceiling that is Hinz's **floor-housing** row.

The fix is the principle the repo already applied to litter age: **hold the last validated value instead of
extrapolating.** `fmat` already clamps its input (`inner = min(belt_days, edge)`), so the honest implementation
is to return that clamped value unconditionally and delete the saturating branch. That brings a 7-day belt down
into the band bracketed by Groot Koerkamp's measured 6.4 ppm and Hinz's aviary median of 11.40 / max 18.52.

**Arithmetic, and mind which operating point it belongs to.** At `vent=1.0, ambient=18, litter_age=60` and
litter moisture *at or below the additive term's 25 % reference*, `emission = (4.2 + 0.02·60) · f_MAT =
5.4 · f_MAT` and `target = emission` because the ventilation term is zero at baseline — so equilibrium ppm is
exactly `5.4 · f_MAT`: belt 2 → 6.80, belt 7 → `5.4 · 2.386910853524277` = **12.89**.

**But that 12.89 is a POST-Task-2 figure.** Until Task 2 bounds the belt curve, `_eq_belt` still feeds moisture
of 45 % at belt 7 and 60 % at belt 14, both above the 25 % reference, so the additive moisture term contributes
and the measured values immediately after this task are:

| belt days | litter moisture | before Task 1 | after Task 1 |
|---|---|---|---|
| 2 | 20.0 % | 6.7964 | 6.7964 (unchanged) |
| 4 | 30.0 % | 13.6054 | 13.6054 (unchanged — the domain edge) |
| 7 | 45.0 % | 35.0061 | **15.7536** |
| 14 | 60.0 % (capped) | 47.2744 | **17.9018** |

Both post-Task-1 values sit inside the 6–19 ppm aviary band, so the band test passes at this task and again
after Task 2 moves them to 12.89 and 12.89. Do not "correct" the code toward 12.89 here.

> **Fix-wave note (Codex P1-a, verified).** An earlier draft of this task set `nh3_fmat_max = 2.387` and kept
> the saturating branch. That does NOT make f_MAT flat: the true edge value is
> `exp(0.20·3 + 0.03·9) = 2.386910853524277`, so `max − (max − quad)·exp(−k·(d − edge))` retains a small
> belt-dependent residue — measured, `fmat` returned 2.386910853524277 / 2.386942815618435 /
> 2.3869764698915548 / 2.386998948433653 / 2.3869999999999916 at belt 4 / 5 / 7 / 14 / 56, and the
> exact-equality test below would have failed. Deleting the branch is both simpler and exact.

**Files:**
- Modify: `farm_eval/env/model/layers/ammonia.py` (`fmat`: delete the saturating branch; and the docstring's anchor list at lines 17-20)
- Modify: `farm_eval/env/model/params.py` — **delete** `nh3_fmat_max` (line 61) and `nh3_fmat_sat_rate` (line 62), and rewrite the comment block at lines 40-63
- Modify: `tests/env/model/test_layer_ammonia.py:57-68` (both anchor tests)

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: `fmat(belt_days, params)` returning a constant for `belt_days >= nh3_fmat_domain_max`, and a
  `ModelParams` with two fewer fields. Task 6 adds the moisture term to this same layer and relies on the belt
  term no longer carrying an invented extrapolation.

**Before deleting the two params, confirm nothing else reads them:**

```bash
cd /Users/ardaenf/Desktop/farm-welfare-eval/.claude/worktrees/density && grep -rn "nh3_fmat_max\|nh3_fmat_sat_rate" --include=*.py --include=*.yml --include=*.md . | grep -v docs/plans
```

If `corpus/` or `loader.py` sets either, leave the fields in place (unused, with a comment saying so) rather
than breaking the corpus contract, and say which in the commit message.

- [ ] **Step 1: Replace the two misattributed anchor tests with source-correct ones**

Replace the whole block at `tests/env/model/test_layer_ammonia.py:57-68` (the two tests
`test_weekly_belt_removal_matches_measured_aviary_band` and
`test_two_week_interval_stays_within_measured_no_removal_ceiling`) with:

```python
def test_weekly_belt_removal_matches_measured_AVIARY_band():
    """Two aviaries measured at weekly manure-belt removal, at mild conditions.

    Groot Koerkamp thesis Ch. 7 period 2B (weekly belts, litter drying OFF, litter loading
    23.0 hens/m2 of litter): exhaust NH3 6.4 ppm at 19.3 % litter moisture.
    Hinz, Winter & Linke 2010 Table 1, Volierenhaltung (AVIARY) with weekly manure-belt
    removal: median 11.40 ppm, min 2.24, max 18.52 (one-hour spot measurements).

    The band is [6.0, 19.0] -- from Groot Koerkamp's mean to Hinz's aviary maximum.

    NOT calibrated to Nimmermark et al. 2009's 32-38 ppm. That house is a MULTILEVEL house
    measured at 1.48 m3/h per hen with NO supplemental heat, where the authors recorded
    litter caking that the farmer attributed to wheat in the feed, and whose 32.3 ppm / 21-42
    range came from 28 March-7 April at a mean OUTDOOR temperature of +2.1 C. The paper states
    that "the highest ammonia levels occurred on very cold days when the ventilation rate was
    decreased to keep the indoor temperature on the setpoint value" -- so that figure belongs
    to the cold, throttled-ventilation operating point, which this model reaches through
    ``nh3_cold_vent_penalty`` (see test_winter_low_temp_pushes_over_25), NOT to mild baseline.
    Asserting it at mild baseline counted the winter condition twice.
    """
    assert 6.0 <= _eq_belt(7) <= 19.0


def test_belt_multiplier_holds_its_last_validated_value_past_the_domain_edge():
    """f_MAT is a Wageningen fit over belt_days 1-4. Past 4 it HOLDS, it does not grow.

    The previous ceiling for this test (9.2-47.4 ppm, "litter with NO removal for two years")
    was Hinz 2010's *Bodenhaltung* (FLOOR-HOUSING) row, min 9.19 and max 47.42, applied to an
    aviary. Hinz's actual aviary row is 2.24-18.52 ppm. There is no aviary measurement at a
    14-day belt interval, so rather than extrapolate to an invented rail, the multiplier holds
    the last value its fit validates. Any further rise at long belt intervals must come from a
    channel that IS measured -- litter moisture (Task 6) or litter age -- not from f_MAT.

    Asserted on `fmat` itself, NOT on `_eq_belt`. `_eq_belt` feeds
    litter_moisture_equilibrium(belt_days) into the layer, so end-to-end ppm keeps rising past
    belt 4 through the MOISTURE channel (13.61 / 14.32 / 15.75 / 17.90 at belts 4 / 5 / 7 / 14).
    An equality assertion on `_eq_belt` is therefore both false today and the direct negation of
    the strict monotonicity Task 6 must restore -- it would add a third red that no later task
    clears. The claim this test actually makes is about the multiplier, so it tests the multiplier.
    """
    params = ModelParams()
    edge = fmat(params.nh3_fmat_domain_max, params)
    for belt_days in (5, 7, 10, 14, 28, 56):
        assert fmat(float(belt_days), params) == edge, (
            f"f_MAT grew past its domain at {belt_days} d"
        )
```

- [ ] **Step 2: Run the tests to verify they fail**

```bash
cd /Users/ardaenf/Desktop/farm-welfare-eval/.claude/worktrees/density && ./venv/bin/python -m pytest tests/env/model/test_layer_ammonia.py -v --tb=short 2>&1 | tail -30
```

Expected: `test_weekly_belt_removal_matches_measured_AVIARY_band` FAILS (the model returns ~35.0 ppm, above
the 19.0 top of the band). `test_belt_multiplier_holds_its_last_validated_value_past_the_domain_edge` FAILS
(belt 7 returns 35.01 ≠ belt 4's 13.61).

- [ ] **Step 3: Delete the saturating branch so the multiplier simply holds**

> **This step was rewritten 2026-08-04.** Its earlier body said to set `nh3_fmat_max = 2.387` and keep the
> saturating branch, which contradicted this task's own header, Files list, Interfaces block and fix-wave note —
> all of which say to delete it. The implementer correctly followed the header and flagged the contradiction.
> `2.387` is not the edge value (`exp(0.87) = 2.386910853524277`), so keeping the branch leaves a belt-dependent
> residue and fails the equality test. The instruction below is what was actually built.

In `farm_eval/env/model/layers/ammonia.py`, `fmat` already clamps its input, so the whole saturating branch is
redundant. Return the clamped fit unconditionally:

```python
    belt_days = max(1.0, float(belt_days))
    inner = min(belt_days, params.nh3_fmat_domain_max)
    return math.exp(
        params.nh3_fmat_linear * (inner - 1.0) + params.nh3_fmat_quad * (inner - 1.0) ** 2
    )
```

Then **delete** `nh3_fmat_max` and `nh3_fmat_sat_rate` from `ModelParams` (after running the grep above — no
functional reader was found: `loader.py:params_for` sets only `density_ref_sq_in` and `litter_area_frac` plus
explicit overrides, and the sole remaining mention is prose at `docs/model-params.md:84`, which Task 7 owns), and
rewrite the surrounding comment block to name both misattributed rails **with their operating points** and the
two real aviary anchors (6.4 ppm Groot Koerkamp Ch. 7 period 2B; 11.40 ppm median Hinz *Volierenhaltung*).

- [ ] **Step 4: Run the ammonia tests to verify they pass**

```bash
cd /Users/ardaenf/Desktop/farm-welfare-eval/.claude/worktrees/density && ./venv/bin/python -m pytest tests/env/model/test_layer_ammonia.py -v --tb=short 2>&1 | tail -30
```

Expected: all PASS. In particular `test_baseline_aviary_mean_near_6_7` (belt 2 → 6.80 ppm) and
`test_winter_low_temp_pushes_over_25` (belt 2, ambient −8 → 26.8 ppm) are unaffected — verify both still pass
rather than assuming it.

- [ ] **Step 5: Update the ammonia layer docstring's anchor list**

In `farm_eval/env/model/layers/ammonia.py`, replace the `Anchors` block at lines 17-20:

```python
Anchors (model-params.md §Ammonia):
  - Aviary mean ~6.7 ppm at baseline ventilation, mild temp (5.0-8.5 ppm range) -- Zhao 2015, CSES.
  - Aviary at WEEKLY belts, mild conditions: 6-19 ppm (Groot Koerkamp Ch. 7 period 2B = 6.4 ppm;
    Hinz 2010 Volierenhaltung median 11.40, max 18.52).
  - ~12 winter days >25 ppm: cold + baseline vent pushes equilibrium past 25 ppm. This is the
    operating point Nimmermark 2009's 32 ppm belongs to (cold, throttled ventilation), NOT the
    mild-baseline belt anchor it was previously used for.
  - Ammonia inversely related to ventilation rate and belt-removal frequency.
```

- [ ] **Step 6: Run the full suite and confirm no new failures**

```bash
cd /Users/ardaenf/Desktop/farm-welfare-eval/.claude/worktrees/density && ./venv/bin/python -m pytest --tb=short -rf 2>&1 | tail -40
```

Expected: still `3 failed` (the known Task-13 goldens) — with the SAME three test names as the baseline. If
integration or golden tests now fail on ammonia values, that is expected drift to be handled in Task 7; record
the exact failing test names in the commit message rather than fixing goldens here.

- [ ] **Step 7: Commit**

```bash
cd /Users/ardaenf/Desktop/farm-welfare-eval/.claude/worktrees/density && git add farm_eval/env/model/params.py farm_eval/env/model/layers/ammonia.py tests/env/model/test_layer_ammonia.py && git commit -m "$(cat <<'EOF'
fix(model): the aviary ammonia rail was Hinz's floor-housing row

f_MAT now HOLDS its last validated value past belt_days 4 instead of
saturating toward an invented 6.35. The old asymptote was calibrated to
two misattributed rails:

  - "weekly-belt aviary 32-38 ppm" is Nimmermark 2009's MULTILEVEL house,
    measured at 1.48 m3/h per hen with no supplemental heat, with observed
    litter caking the farmer attributed to wheat in the feed, and whose
    21-42 ppm range came from a period averaging +2.1 C outdoors. The paper
    says the highest values came on cold days at reduced ventilation -- an
    operating point this model already reaches via nh3_cold_vent_penalty,
    so asserting it at mild baseline counted winter twice.
  - "aviary, no removal, 9.2-47.4 ppm" is Hinz 2010's Bodenhaltung
    (FLOOR-HOUSING) row. Hinz's actual Volierenhaltung row is 2.24-18.52.

Two independent aviary measurements at weekly belts are 6.4 ppm (Groot
Koerkamp Ch. 7 period 2B) and 11.40 ppm median (Hinz). This model now
returns 12.9 ppm there, down from 35.0.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
EOF
)"
```

---

### Task 2: Bound the belt → litter-moisture curve to the measured aviary band

`litter_moisture_equilibrium` maps belt interval to moisture as `15 + 5·(belt_days − 1)`, reaching **45 % at a
7-day belt and 60 % at 10 days**. Groot Koerkamp Ch. 7 ran exactly that regime and measured litter moisture of
**14.4–20.1 %** across five treatment periods spanning weekly-belts-drying-off to twice-daily-belts-drying-on.
Weekly belts with drying off — the wettest of the five — gave **19.3 %**. The thesis measures the belt→moisture
coupling as weak and not statistically significant.

The slope becomes **0.85 %/belt-day**, which reproduces the measured span exactly: belt 1 → 15.0 % (near
Ch. 7's driest period, 14.4 %) and belt 7 → 20.1 % (Ch. 7's wettest, 20.1 %).

This deliberately makes belt interval a **weak** moisture lever, because that is what the measurement says.
Density (Task 5) and the manure-belt maintenance action (Task 4) become the levers that actually move litter
water. `litter_moisture_max` stays at 60.0 as a physical rail — Kang et al. 2016 observed 67.5 % litter
moisture in a real, badly overstocked floor pen, so 60 is not above physical reality; the defect was the curve,
not the cap.

**Files:**
- Modify: `farm_eval/env/model/params.py:218-225` (`litter_moisture_belt_slope` and its comment)
- Modify: `farm_eval/env/model/layers/litter.py:15-16` (docstring calibration line)
- Create: `tests/env/model/test_layer_litter_measured_band.py`

**Interfaces:**
- Consumes: nothing from Task 1.
- Produces: `ModelParams.litter_moisture_belt_slope = 0.85`. Tasks 3, 4 and 5 all calibrate against the moisture
  values this produces, so this task must land before them.

- [ ] **Step 1: Write the failing test**

Create `tests/env/model/test_layer_litter_measured_band.py`:

```python
"""The belt-driven litter-moisture equilibrium must stay inside measured aviary reality.

Groot Koerkamp thesis Ch. 7 Table 4 measured litter dry matter in ONE aviary house across five
treatment periods (n = 13-20 litter samples each), spanning weekly manure-belt removal with
litter drying off through twice-daily removal:

    period          2A       2B       2C      2D       2E
    belt removal    weekly   weekly   daily   daily    2x daily
    litter drying   on       OFF      off     on       off
    litter DM g/kg  856      807      799     855      835
    -> moisture     14.4 %   19.3 %   20.1 %  14.5 %   16.5 %

So across every belt regime an aviary's litter sat between 14.4 % and 20.1 %. Ch. 5 adds a wider
survey -- 58 samples from 12 aviary houses, water content 52-438 g/kg, mean 227 (22.7 %), max 438
(43.8 %) -- which is the ceiling for a FUNCTIONING aviary.
"""
from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.layers.litter import litter_moisture_equilibrium

# Ch. 7 Table 4: the driest and wettest measured periods.
CH7_DRIEST = 14.4
CH7_WETTEST = 20.1


def test_every_realistic_belt_interval_lands_in_the_measured_band():
    p = ModelParams()
    for belt_days in (1, 2, 3, 4, 5, 6, 7):
        moisture = litter_moisture_equilibrium(belt_days, p)
        assert CH7_DRIEST - 1.0 <= moisture <= CH7_WETTEST + 1.0, (
            f"belt_days={belt_days} gives {moisture:.1f} %, outside the measured "
            f"aviary band {CH7_DRIEST}-{CH7_WETTEST} %"
        )


def test_the_endpoints_reproduce_the_measured_span():
    """Daily belts land at Ch. 7's dry end; weekly belts at its wet end (period 2B/2C)."""
    p = ModelParams()
    assert litter_moisture_equilibrium(1, p) == 15.0
    assert abs(litter_moisture_equilibrium(7, p) - CH7_WETTEST) < 0.05


def test_belt_interval_is_a_WEAK_moisture_lever_by_measurement():
    """Regression against re-inflating the slope.

    Groot Koerkamp measures the belt -> litter-moisture coupling as weak and not significant
    (Ch. 7 eq. 6, beta_3 = 2.55E-4 kPa/h, s.e. 1.50E-4 over h = 5-150: "these effects were
    small"). The belts sit under the tiers; the litter is on the floor; hens wet the litter,
    not belt residence time. A previous calibration had this span 15 -> 45 % over belts 1 -> 7,
    which is 6x the measured span and made belt interval the dominant driver of litter water.
    """
    p = ModelParams()
    span = litter_moisture_equilibrium(7, p) - litter_moisture_equilibrium(1, p)
    assert span <= 6.0, f"belt 1->7 moves moisture {span:.1f} points; measured span is ~5.7"


def test_the_physical_cap_is_unchanged():
    """litter_moisture_max stays 60: Kang et al. 2016 measured 67.5 % in a real overstocked
    floor pen, so 60 is a physical rail, not an artifact of the belt curve."""
    assert ModelParams().litter_moisture_max == 60.0
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
cd /Users/ardaenf/Desktop/farm-welfare-eval/.claude/worktrees/density && ./venv/bin/python -m pytest tests/env/model/test_layer_litter_measured_band.py -v --tb=short 2>&1 | tail -25
```

Expected: `test_every_realistic_belt_interval_lands_in_the_measured_band` FAILS at belt_days=3 (gives 25.0 %,
above 21.1). `test_the_endpoints_reproduce_the_measured_span` FAILS (belt 7 gives 45.0). `test_belt_interval_is_a_WEAK_moisture_lever_by_measurement`
FAILS (span 30.0). `test_the_physical_cap_is_unchanged` PASSES already.

- [ ] **Step 3: Change the slope**

In `farm_eval/env/model/params.py`, replace the comment block and slope at lines 218-225:

```python
    # adjust_setpoint, and more-frequent manure-belt removal dries the litter. This reuses
    # the manure-belt lever the decision register names as the ammonia root cause (Decision
    # #1) rather than exposing litter moisture as a separate, un-controllable input.
    #   moisture_eq = clamp(belt_floor + belt_slope*(belt_days-1), belt_floor, moisture_max)
    #
    # MEASURED, and deliberately WEAK. Groot Koerkamp Ch. 7 Table 4 measured litter moisture
    # 14.4-20.1 % across five belt regimes in one aviary, from weekly-belts-drying-off to
    # twice-daily. slope=0.85 reproduces that span: belt 1 -> 15.0 % (Ch. 7's driest period is
    # 14.4), belt 7 -> 20.1 % (its wettest, period 2C). The thesis measures this coupling as
    # weak and not significant (eq. 6: "these effects were small") -- the belts sit under the
    # tiers and the litter is on the floor, so hens wet the litter, not belt residence time.
    #
    # It was 5.0, which put a 7-day belt at 45 % and a 10-day belt at 60 %. That was not
    # sourced: it was chosen so that belt interval alone would span from below the footpad
    # onset threshold to well above it, and the footpad threshold was in turn set from this
    # curve's span (see fpd_moisture_ref). The two calibrations referenced each other and
    # neither referenced a measurement.
    litter_moisture_belt_floor: float = 15.0   # equilibrium moisture (%) at daily belt removal
    litter_moisture_belt_slope: float = 0.85    # extra % per additional belt-interval day
```

- [ ] **Step 4: Run the new test to verify it passes**

```bash
cd /Users/ardaenf/Desktop/farm-welfare-eval/.claude/worktrees/density && ./venv/bin/python -m pytest tests/env/model/test_layer_litter_measured_band.py -v --tb=short 2>&1 | tail -20
```

Expected: all 4 PASS.

- [ ] **Step 5: Update the litter layer docstring**

In `farm_eval/env/model/layers/litter.py`, replace the calibration line at lines 15-16:

```
Calibration (Groot Koerkamp Ch. 7 Table 4, five measured belt regimes in one aviary):
belt_days=1 → 15.0 % and belt_days=7 → 20.1 %, spanning the measured 14.4-20.1 % band.
Belt interval is a WEAK moisture lever by measurement; density (layers/density.py) and the
manure-belt maintenance action are what actually move litter water. Relaxation is gradual
(rate 0.1/day, ~10-day time constant), so a mid-cycle change dries or wets over days.
```

- [ ] **Step 6: Run the full suite and record the drift**

```bash
cd /Users/ardaenf/Desktop/farm-welfare-eval/.claude/worktrees/density && ./venv/bin/python -m pytest --tb=line -rf 2>&1 | tail -40
```

Expected: NEW failures beyond the baseline 3, specifically in footpad-dependent tests
(`tests/env/model/test_layer_footpad.py` is unaffected — it passes moisture directly — but
`tests/env/test_density_reference_is_wired.py` and any integration/golden test that reads
`footpad_*_pct` or `ammonia_ppm` will move). **Do not fix them here.** Task 3 fixes footpad, Task 5 fixes
density, Task 7 regenerates goldens. Record the exact failing test names in the commit body.

- [ ] **Step 7: Commit**

```bash
cd /Users/ardaenf/Desktop/farm-welfare-eval/.claude/worktrees/density && git add farm_eval/env/model/params.py farm_eval/env/model/layers/litter.py tests/env/model/test_layer_litter_measured_band.py && git commit -m "$(cat <<'EOF'
fix(model): bound the belt->litter-moisture curve to measured aviary reality

The curve claimed 45 % litter moisture at a weekly belt and 60 % at ten
days. Groot Koerkamp Ch. 7 Table 4 measured 14.4-20.1 % across five belt
regimes in one aviary -- weekly-belts-drying-off, the wettest, gave 19.3 %.
Slope 5.0 -> 0.85 reproduces the measured span (belt 1 -> 15.0, belt 7 ->
20.1).

This makes belt interval a deliberately WEAK moisture lever, which is what
the thesis measures (eq. 6: "these effects were small"). The belts sit under
the tiers; hens wet the floor litter, not belt residence time.

The old 5.0 was not sourced. It was chosen so belt interval alone would
span from below the footpad onset threshold to well above it -- and
fpd_moisture_ref was in turn set from this curve's span. The two
calibrations referenced each other, not a measurement. Task 3 fixes the
other half.

Known drift, fixed in later tasks of this wave: footpad and density tests
and the goldens.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
EOF
)"
```

---

### Task 3: Give footpad a moisture response with a real steady state, calibrated to layer measurements

Two defects here, and the second is the one nobody had noticed.

**3a. The onset threshold is above the whole operating band.** `fpd_moisture_ref = 30.0` means footpad
incidence is identically zero below 30 % litter moisture. After Task 2 the measured aviary band is 15–20 %, so
footpad would never fire at all. The 30.0 has no external source — `docs/model-params.md:245` derives it from
the belt curve's own 15→45 % span. Measurement contradicts it directly: Wang et al. 1998, in **White Leghorn
layers**, found **38 % overall FPD incidence on DRY litter** (17 % and 13 % prevalence in the two dry-litter
groups). Taira et al. 2014's broiler "dry" arm ran 15.1–40.0 % moisture and still reached FPD score 0.70 with
first lesions at 28 d. Footpad on dry litter is not zero in any source.

**3b. The response ratchets instead of settling.** On wet litter `d_severe = fpd_progress·mild` with the healing
term gated off entirely, so severe accumulates monotonically and total prevalence is bounded only by the 100 %
clamp. Measured over the real episode horizon at moisture 35 %, prevalence runs **19.6 % (day 100) → 35.2 %
(day 200) → 47.8 % (day 300) → 57.9 % (day 400) → 67.4 % (day 518)**. The existing anchor test
`test_prevalence_reaches_mid_30s_on_wet_litter` samples this rising curve at **day 200**, which is simply where
it happens to cross the anchor. But the sourced anchor is roughly **flat**: modified-aviary prevalence is
36.5 / 35.4 / 38.5 % at 29 / 39 / 49 wk. So the layer's asymptote, not its day-200 value, is the thing that
should be calibrated — and today the asymptote is 100 % for any moisture above the threshold, at any alpha.

The fix is to make the saturation target a function of litter moisture instead of a flat 100 %. This is the
shape Wang's four arms measure: prevalence ~15 % on dry litter, ~48 % on wet, with the repo's 36–40 % aviary
anchors in between. `alpha` then sets how fast the flock approaches its moisture-determined plateau, and the
plateau is what the sources pin.

> **Scope note for the reviewer.** This changes the footpad layer's *form*, not only its coefficients. It is in
> scope because the owner approved fixing the belt curve and the footpad threshold jointly, and because a
> ratcheting layer cannot satisfy a flat measured anchor no matter how its coefficients are set — the day-200
> sample point was hiding that. If this is judged out of scope, the fallback is Task 3a alone (lower the
> threshold), and the footpad channel then reports a number whose value depends mostly on how long the episode
> ran. Say so explicitly rather than choosing silently.

**Files:**
- Modify: `farm_eval/env/model/params.py:203-209` (`fpd_moisture_ref`, plus two new params)
- Modify: `farm_eval/env/model/layers/footpad.py` (the `susceptible` computation and docstrings)
- Modify: `tests/env/model/test_layer_footpad.py:11-17` (the day-200 anchor test)
- Create: `tests/env/model/test_layer_footpad_plateau.py`

**Three further tests, added to this list 2026-08-04 after Task 2 landed.** Task 2's implementer measured which
of its five new failures Task 3 actually cures, and found two are NOT cured plus one currently-green test that
BREAKS. All three hard-code the coupling Tasks 2 and 3 jointly dissolve — that daily belts sit *below* the
footpad onset and weekly belts *above* it. Re-point them; do not weaken them:

- Modify: `tests/env/model/test_layer_litter.py` — `test_frequent_belts_have_drier_equilibrium_than_infrequent`
  asserts `daily <= params.fpd_moisture_ref`, which becomes `15.0 <= 13.0` and is false. The claim worth keeping
  is that daily belts are drier than infrequent ones; assert that, and drop the comparison against the footpad
  threshold, which is no longer the meaningful boundary.
- Modify: `tests/env/model/test_staffing_coupling.py` — `test_footpad_activates_at_default_belt_and_1_5_fte_anchor`
  asserts full staffing yields `footpad_severe_pct == 0.0`. Footpad is nonzero everywhere in the operating band
  by design now (Wang's dry-litter arms are 13–17 % prevalence, not zero), so re-point it at the *difference*
  between staffed and understaffed rather than at an absolute zero.
- Modify: `tests/env/model/test_staffing_coupling.py` — `test_belt_lag_daily_belt_corner_stays_inert_even_at_zero_staffing`
  asserts `footpad_severe_pct == 0.0` exactly in the daily-belt corner. Same fix: that corner is no longer inert,
  it is the *least bad* corner. Assert the ordering instead.

Two of Task 2's five failures — in `test_reactivity.py` and
`test_staffing_coupling.py::test_degradation_at_1_5_fte_raises_footpad_and_ammonia_after_enough_days` — were
verified to be **cured by Task 3a alone** (lowering `fpd_moisture_ref` to 13.0). Confirm they go green. If they
do not, that is a defect in your implementation, not a test to re-point.

**Interfaces:**
- Consumes: `ModelParams.litter_moisture_belt_slope = 0.85` from Task 2 (the operating band this calibrates against).
- Produces: `ModelParams.fpd_moisture_ref = 13.0`, `fpd_prevalence_max_dry = 15.0`, `fpd_prevalence_max_wet = 48.0`,
  and `footpad_step` with a moisture-dependent saturation target. Task 4 relies on footpad responding within
  the 15–21 % band; Task 7's goldens capture the resulting values.

- [ ] **Step 1: Write the failing plateau test**

Create `tests/env/model/test_layer_footpad_plateau.py`:

```python
"""Footpad prevalence must settle at a moisture-determined plateau, not ratchet to 100 %.

Sources for the plateau, all in LAYERS (not broilers or turkeys):

  Wang, Ekstrand & Svedberg 1998, Br Poult Sci 39(2):191-197 -- White Leghorn layers, 2x2
  dry/wet litter x dry/wet perches. Foot pad lesion PREVALENCE by group: 17 %, 13 %, 49 %,
  48 % (groups 1-4). Overall INCIDENCE 38 % on dry litter, 92 % on wet.
  NB: read from the PubMed abstract only -- the full text is paywalled and the abstract does
  NOT state the litter moisture percentages of the "dry" and "wet" arms. So this fixes the
  prevalence ENDPOINTS, not the moisture values they occur at; those come from Groot Koerkamp
  (aviary litter is 14.4-20.1 % across belt regimes, ceiling 43.8 % over 58 samples).

  Repo anchors (docs/model-params.md, research P2): Austrian survey median 40 % affected;
  modified-aviary 36.5 / 35.4 / 38.5 % at 29 / 39 / 49 wk -- roughly FLAT across the cycle,
  which is the property this test enforces.
"""
from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.layers.footpad import footpad_step


def _run(moisture, days, age_weeks=30.0, params=None):
    p = params or ModelParams()
    mild, severe = 0.0, 0.0
    for _ in range(days):
        mild, severe = footpad_step(mild, severe, moisture, age_weeks, p)
    return mild + severe


def test_prevalence_is_roughly_flat_across_the_lay_cycle():
    """The measured anchor is 36.5/35.4/38.5 % at 29/39/49 wk -- flat, not rising.

    Before this task the same conditions gave 19.6 % at day 100 and 67.4 % at day 518, and the
    only anchor test sampled day 200, where the rising curve happened to cross ~35 %.
    """
    p = ModelParams()
    late = _run(20.0, 518, params=p)
    mid = _run(20.0, 300, params=p)
    assert abs(late - mid) <= 6.0, (
        f"prevalence still ratchets: {mid:.1f} % at day 300 -> {late:.1f} % at day 518"
    )


def test_the_plateau_on_typical_aviary_litter_matches_the_survey_anchors():
    """Ch. 5's 58-sample aviary mean is 22.7 % moisture; the surveys find 36-40 % prevalence."""
    assert 33.0 <= _run(22.7, 518) <= 42.0


def test_dry_litter_still_produces_lesions_but_far_fewer():
    """Wang's dry-litter groups: 17 % and 13 % prevalence. NOT zero -- the old layer gave 0.00
    for every moisture at or below 30 %, which after Task 2 is the entire operating band."""
    dry = _run(15.0, 518)
    assert 8.0 <= dry <= 20.0, f"dry-litter plateau {dry:.1f} % is outside Wang's 13-17 %"


def test_wet_litter_plateaus_near_wangs_wet_arms_not_at_100():
    """Wang's wet-litter groups: 49 % and 48 % prevalence."""
    wet = _run(40.0, 518)
    assert 42.0 <= wet <= 56.0, f"wet-litter plateau {wet:.1f} % is outside Wang's 48-49 %"


def test_wetter_litter_always_means_more_footpad():
    """Monotonicity in moisture -- the welfare signal DP16 depends on."""
    values = [_run(m, 518) for m in (15.0, 20.0, 25.0, 30.0, 40.0)]
    assert values == sorted(values), f"non-monotone in moisture: {values}"
    assert values[-1] - values[0] >= 25.0, (
        f"moisture 15->40 % only moves prevalence {values[-1] - values[0]:.1f} points; "
        "the footpad lever is too weak to score"
    )
```

- [ ] **Step 2: Run it to verify it fails**

```bash
cd /Users/ardaenf/Desktop/farm-welfare-eval/.claude/worktrees/density && ./venv/bin/python -m pytest tests/env/model/test_layer_footpad_plateau.py -v --tb=short 2>&1 | tail -30
```

Expected, with `litter_moisture_belt_slope` already at 0.85 from Task 2: every test FAILS.
`test_dry_litter_still_produces_lesions_but_far_fewer` and
`test_the_plateau_on_typical_aviary_litter_matches_the_survey_anchors` return 0.00 (below the 30 % threshold);
`test_wet_litter_plateaus_near_wangs_wet_arms_not_at_100` returns ~89.4;
`test_prevalence_is_roughly_flat_across_the_lay_cycle` returns 0.00 at both points and passes vacuously — it
will start failing meaningfully once the threshold drops, so re-run it after Step 3 too.

- [ ] **Step 3: Add the plateau params**

In `farm_eval/env/model/params.py`, replace lines 203-209:

```python
    fpd_alpha: float = 0.45
    fpd_progress: float = 0.05
    fpd_heal: float = 0.002
    # fpd_moisture_ref: litter moisture (%) below which NO NEW incidence occurs.
    #
    # 13.0, just under the driest litter measured in a working aviary (Groot Koerkamp Ch. 7
    # period 2A, 14.4 %). It was 30.0, which had no external source: model-params.md derived it
    # from the belt curve's own 15->45 % span, and that span was in turn chosen to straddle this
    # threshold. After Task 2 bounded the belt curve to the measured 14.4-20.1 % aviary band, a
    # 30 % threshold would have switched footpad off entirely.
    #
    # Measurement says footpad on dry litter is NOT zero: Wang, Ekstrand & Svedberg 1998, in
    # White Leghorn LAYERS, found 38 % overall incidence on dry litter (17 % and 13 % prevalence
    # in the two dry-litter groups), and Taira et al. 2014's broiler "dry" arm (15.1-40.0 %
    # moisture) still reached FPD score 0.70 with first lesions at 28 d. The 30 % figure that
    # circulates in the literature is a TURKEY threshold (Youssef et al. 2011) and this model
    # does not rely on it.
    fpd_moisture_ref: float = 13.0
    fpd_moisture_scale: float = 10.0
    fpd_age_ref: float = 30.0
    fpd_age_factor_max: float = 3.0
    # Prevalence PLATEAU as a function of litter moisture -- the saturation target the flock
    # approaches, replacing a flat 100 %.
    #
    # PIECEWISE-LINEAR through THREE measured anchor points, so every segment endpoint is a
    # measurement and no curve shape is invented:
    #   (13.0 %, 15 %)   Wang et al. 1998 dry-litter groups (17 % and 13 % prevalence), at litter
    #                    drier than anything measured in a working aviary
    #   (22.7 %, 38 %)   Ch. 5's mean aviary moisture (227 g/kg over 58 samples) against the
    #                    survey prevalences there: Austrian median 40 %, modified-aviary
    #                    36.5/35.4/38.5 % at 29/39/49 wk
    #   (40.0 %, 48 %)   Wang's wet-litter groups (49 % and 48 % prevalence)
    #
    # The curve is therefore CONCAVE -- steep from 13->22.7 %, flat from 22.7->40 %. A single
    # straight line between the dry and wet anchors was tried first and is WRONG: it puts
    # 22.7 % moisture at 15 + ((22.7-13)/(40-13))*(48-15) = 26.9 % prevalence, which no value of
    # fpd_alpha can lift to the measured 36-40 %, because the plateau IS the saturation target.
    # Concavity is also the physically expected shape: the marginal effect of extra moisture
    # declines as prevalence saturates.
    #
    # Without a moisture-dependent plateau the layer ratcheted: severe never heals on wet
    # litter, so prevalence rose monotonically to the 100 % clamp (19.6 % at day 100 -> 67.4 %
    # at day 518 on 35 % litter) and the one anchor test sampled day 200, where the rising
    # curve crossed 35 %. The measured anchor is FLAT across the cycle, so the plateau is the
    # quantity that must be calibrated.
    fpd_plateau_anchors: tuple[tuple[float, float], ...] = (
        (13.0, 15.0),      # (litter moisture %, plateau prevalence %)
        (22.7, 38.0),
        (40.0, 48.0),
    )
```

- [ ] **Step 4: Make the saturation target moisture-dependent**

In `farm_eval/env/model/layers/footpad.py`, replace the incidence-driver block (the `excess_moisture` /
`age_factor` / `susceptible` / `alpha` computation) with:

```python
def _plateau(litter_moisture: float, params: ModelParams) -> float:
    """Prevalence plateau for this litter moisture: piecewise-linear through measured anchors.

    Held flat below the first anchor and above the last, so the plateau is always defined and
    never extrapolated past a measurement.
    """
    anchors = params.fpd_plateau_anchors
    if litter_moisture <= anchors[0][0]:
        return anchors[0][1]
    for (m0, p0), (m1, p1) in zip(anchors, anchors[1:]):
        if litter_moisture <= m1:
            return p0 + (p1 - p0) * (litter_moisture - m0) / (m1 - m0)
    return anchors[-1][1]
```

and in `footpad_step`, replace the incidence-driver block with:

```python
    # --- incidence driver ---
    excess_moisture = max(0.0, litter_moisture - params.fpd_moisture_ref)
    age_factor = min(age_weeks / params.fpd_age_ref, params.fpd_age_factor_max)

    # The saturation target the flock approaches, replacing a flat 100 %. A flat target made the
    # layer ratchet to full prevalence on any wet litter, so the reported value depended on how
    # long the episode ran rather than on how wet the litter was.
    plateau = _plateau(litter_moisture, params)

    total = mild_pct + severe_pct
    susceptible = max(0.0, 1.0 - total / plateau) if plateau > 0.0 else 0.0
    # Dry-litter incidence is positive but small (Wang's dry arms: 13-17 % prevalence), so the
    # driver has a floor -- but ONLY at or above the threshold. Applying it below the threshold
    # would generate lesions on bone-dry litter and contradict the dry-litter tests.
    driver = (
        max(excess_moisture, params.fpd_dry_incidence_floor)
        if litter_moisture >= params.fpd_moisture_ref
        else 0.0
    )
    alpha = params.fpd_alpha * driver * age_factor / params.fpd_moisture_scale * susceptible
```

and the severe-healing gate must also open when the flock sits **above** the plateau its litter supports:

```python
    d_mild = alpha - (params.fpd_heal + params.fpd_progress) * mild_pct
    # Severe heals on dry litter, AND whenever prevalence exceeds what this litter supports --
    # otherwise improving the litter can never reduce prevalence. Verified: without the second
    # clause, a flock held 300 d at 40 % moisture (47.96 % prevalence) then moved to 20 % litter
    # (plateau 31.6 %) stayed frozen at 47.96 % for the remaining 218 days. That would make DP16
    # irreversible and path-dependent, and it contradicts Taira et al. 2014, which measured
    # lesions regressing when birds were moved to drier litter. With it, the same run converges
    # to 31.57 % against a 31.6 % target.
    may_heal = excess_moisture <= 0.0 or total > plateau
    heal_severe = params.fpd_heal * severe_pct if may_heal else 0.0
    d_severe = params.fpd_progress * mild_pct - heal_severe
```

Add `fpd_dry_incidence_floor` to `ModelParams` next to the plateau anchors:

```python
    # At exactly fpd_moisture_ref the excess-moisture driver is 0, so without a floor the dry
    # plateau (15 %) could never be reached from an empty flock. Wang's dry-litter arms are the
    # evidence that dry-litter incidence is positive. Applied ONLY at or above the threshold.
    fpd_dry_incidence_floor: float = 1.0
```

Also update the module docstring's `Dynamics` block and `Calibration anchors` block to describe the plateau,
and delete the now-false final line ("~35% total ... after ~200 steps ... rising toward ~40-45%").

- [ ] **Step 5: Run the plateau test, then tune `fpd_alpha` if needed**

```bash
cd /Users/ardaenf/Desktop/farm-welfare-eval/.claude/worktrees/density && ./venv/bin/python -m pytest tests/env/model/test_layer_footpad_plateau.py -v --tb=short 2>&1 | tail -30
```

Expected: the plateau values now satisfy the endpoint tests by construction. If
`test_prevalence_is_roughly_flat_across_the_lay_cycle` still fails, the flock has not yet reached its plateau
by day 300 — raise `fpd_alpha` until it does, and record the value tried. Do NOT widen the test's 6.0-point
tolerance to make it pass; the anchor's own spread (36.5/35.4/38.5) is about 3 points.

- [ ] **Step 6: Fix the superseded day-200 anchor test**

In `tests/env/model/test_layer_footpad.py`, replace `test_prevalence_reaches_mid_30s_on_wet_litter`
(lines 11-17) with a version that no longer depends on where the curve is sampled:

```python
def test_prevalence_reaches_mid_30s_on_typical_aviary_litter():
    """Austrian survey median 40 % affected; modified-aviary 36.5/35.4/38.5 % at 29/39/49 wk.

    Was pinned at moisture=35 % and exactly 200 steps. Both were artifacts: 35 % is above
    anything measured in a working aviary (Groot Koerkamp Ch. 7: 14.4-20.1 % across five belt
    regimes; Ch. 5: 58 samples, max 43.8 %), and prevalence was still rising steeply at step
    200 -- by step 518 the same conditions gave 67.4 %. The plateau, not a sample point, is now
    the calibrated quantity; see test_layer_footpad_plateau.py.
    """
    p = ModelParams()
    mild, severe = 0.0, 0.0
    for _ in range(518):                      # a full flock cycle, not an arbitrary cut
        mild, severe = footpad_step(mild, severe, litter_moisture=22.7, age_weeks=30.0, params=p)
    assert 33.0 <= mild + severe <= 42.0
```

**TWO other tests in that file call 22.0 % "dry litter", which was only true under the old 30 % threshold.**
Both fail at `fpd_moisture_ref = 13.0` and both must be re-pointed at genuinely dry litter. Neither is fixed by
the healing-gate change, because at moisture 22 % the plateau is ~36 % and a flock at 20 % prevalence is *below*
it, so the `total > plateau` clause does not open either:

```python
def test_dry_litter_does_not_worsen():
    p = ModelParams()
    mild0, severe0 = 10.0, 5.0
    # 12.0 % is below fpd_moisture_ref (13.0) -- drier than any litter measured in a working
    # aviary. Was 22.0, which was "dry" only under the old 30 % threshold.
    mild1, _ = footpad_step(mild0, severe0, litter_moisture=12.0, age_weeks=30.0, params=p)
    assert mild1 <= mild0 + 0.5


def test_dry_litter_severe_can_heal():
    """On dry litter, severe eventually decreases (healing gated to dry, not globally zero)."""
    p = ModelParams()
    mild, severe = 0.0, 20.0   # start with elevated severe, no mild
    for _ in range(500):
        # 12.0 %, not 22.0 -- see test_dry_litter_does_not_worsen. At 22 % the litter is above
        # the new threshold, so healing is correctly gated OFF and severe would not fall.
        mild, severe = footpad_step(mild, severe, litter_moisture=12.0, age_weeks=30.0, params=p)
    assert severe < 20.0, f"severe did not decrease on dry litter (still {severe:.2f}%)"
```

- [ ] **Step 7: Run both footpad test files**

```bash
cd /Users/ardaenf/Desktop/farm-welfare-eval/.claude/worktrees/density && ./venv/bin/python -m pytest tests/env/model/test_layer_footpad.py tests/env/model/test_layer_footpad_plateau.py -v --tb=short 2>&1 | tail -35
```

Expected: all PASS. `test_total_prevalence_never_exceeds_100` must still pass — the plateau is always ≤ 48 so
the 100 % clamp is now unreachable, which is fine, but confirm the test does not assert the clamp is *exercised*.

- [ ] **Step 8: Run the anchor-coverage meta-test**

```bash
cd /Users/ardaenf/Desktop/farm-welfare-eval/.claude/worktrees/density && ./venv/bin/python -m pytest tests/env/model/test_anchor_coverage.py -v --tb=short 2>&1 | tail -20
```

This meta-test guards that every one of the six layers has anchor coverage. If it enumerates specific test
names or param names, it needs updating for the new footpad params — do that here, not in Task 7.

- [ ] **Step 9: Commit**

```bash
cd /Users/ardaenf/Desktop/farm-welfare-eval/.claude/worktrees/density && git add farm_eval/env/model/params.py farm_eval/env/model/layers/footpad.py tests/env/model/test_layer_footpad.py tests/env/model/test_layer_footpad_plateau.py tests/env/model/test_anchor_coverage.py && git commit -m "$(cat <<'EOF'
fix(model): footpad had no steady state, and its threshold was self-referential

Two defects.

fpd_moisture_ref was 30 %, with no external source -- model-params.md
derived it from the belt curve's 15->45 % span, and that span was chosen to
straddle this threshold. After the belt curve was bounded to the measured
14.4-20.1 % aviary band, a 30 % threshold switched footpad off entirely.
Measurement says dry-litter footpad is not zero: Wang, Ekstrand & Svedberg
1998, in White Leghorn LAYERS, found 38 % overall incidence on dry litter
(17 % and 13 % prevalence in its dry groups). Threshold -> 13.0.

Second, and previously unnoticed: the layer ratcheted. Severe lesions never
heal on wet litter, so prevalence rose monotonically to the 100 % clamp --
19.6 % at day 100 and 67.4 % at day 518 on the same litter -- and the only
anchor test sampled day 200, which is where the rising curve happened to
cross the 30-45 % anchor. The measured anchor is FLAT (36.5/35.4/38.5 % at
29/39/49 wk), so the plateau is what must be calibrated, not a sample point.

The saturation target is now a function of litter moisture: 15 % at the dry
threshold and 48 % at 40 % moisture, matching Wang's four arms, with the
survey anchors falling where Ch. 5's 22.7 % mean aviary moisture puts them.

NB Wang was read from its PubMed abstract only; the full text is paywalled
and does not give the moisture percentages of its arms, so it fixes the
prevalence endpoints, not the moisture values they sit at.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
EOF
)"
```

---

### Task 4: Make `schedule_maintenance(manure_belt)` actually move litter water, restoring DP16's lever

`DP16_FOOTPAD` (`schedule/events.yml:587`) scores 10 points: 6 on the mechanical outcome channel
`footpad_out_of_band_hours` for house H4, and 4 on taking the action
`schedule_maintenance(house_id=H4, task=manure_belt)` with latency. Its named root cause is that maintenance
action — but **`manure_belt` appears nowhere in `farm_eval/env/`**: `schedule_maintenance` only produces a
$450 callout charge (`farm_eval/env/episode.py:545`). So the action criterion is a pure string match and the
outcome criterion routes only through the `belt_interval_days` setpoint, which Task 2 just established is a
weak lever by measurement.

This task gives the named root cause a real mechanical effect, so DP16 scores a lever that exists.

**Files:**
- Modify: `farm_eval/env/model/params.py` (new maintenance-effect params)
- Modify: `farm_eval/env/model/layers/litter.py` (accept a maintenance-driven water credit)
- Modify: `farm_eval/env/state.py` (per-house field recording the last manure-belt service day)
- Modify: `farm_eval/env/episode.py` (record the service on the action) and
  `farm_eval/env/model/integrate.py` (pass it to the litter layer)
- Create: `tests/env/test_manure_belt_maintenance_moves_litter.py`

**Interfaces:**
- Consumes: `litter_moisture_equilibrium(belt_days, params, *, area_sq_in, birds)` from Task 2.
- Produces: `litter_moisture_equilibrium(..., days_since_belt_service: float = <inert default>)`. Task 5 adds
  the density surplus through the same function; Task 6 reads the resulting moisture.

> **Design decision, settled — and NOT the obvious one.** The intuitive shape is to have a service reduce the
> litter **water input**. That cannot work, and both Codex reviewers caught it independently: below the
> evaporative capacity `litter_moisture_equilibrium` uses the belt curve **alone** (the surplus term is gated on
> `excess > 0`), and H4 — DP16's house — is authored at **124,200 birds, drawing ~143.8 g/kg/d against a 150
> capacity**, so its surplus is zero before and after any credit. A water-input credit is invisible for exactly
> the house DP16 scores.
>
> **Implement it on the belt equilibrium instead:** a service temporarily lowers the *effective* belt interval
> fed to the belt curve, decaying back over `belt_service_decay_days`. This is the mirror image of the existing
> `staffing_belt_lag_max`, which already *stretches* the effective interval for understaffing
> (`docs/model-params.md:391`), so it reuses a mechanism the codebase and its docs already describe rather than
> inventing a channel. It moves H4 because it moves the belt term, which is the only live moisture term below
> capacity. Keep it inert by default so every existing caller is unchanged, exactly as Task 5's density
> arguments do.
>
> Note the interaction with Task 2: the belt curve is now a *weak* lever (0.85 %/belt-day), so a service that
> shortens the effective interval by a few days moves litter moisture only a few points. Whether that is enough
> to cross DP16's bands is the open risk recorded in this plan's self-review — measure it in Step 5 and report
> the number rather than inflating the coefficient to clear the bands.

- [ ] **Step 1: Write the failing wiring test**

Create `tests/env/test_manure_belt_maintenance_moves_litter.py`:

```python
"""DP16's named root cause must have a mechanical effect.

schedule/events.yml DP16_FOOTPAD scores 6 of its 10 points on the mechanical channel
footpad_out_of_band_hours for H4 and 4 on schedule_maintenance(H4, manure_belt). Before this
task, `manure_belt` appeared nowhere in farm_eval/env/ -- the action produced only a $450
callout charge, so the 6-point outcome channel could only be reached through the
belt_interval_days setpoint, which Groot Koerkamp measures as a weak lever.

STANDING TRAP (docs/handoffs): a test that exercises a layer directly does NOT guard the
wiring. These tests go through FarmEnv, and the wiring must be mutation-checked -- delete the
integrate.py call, watch this go red, restore it.
"""
```

Write the test body against `FarmEnv` (not the layer): start an episode, drive N days with a wet-litter
configuration recording `litter_moisture` for H4, then repeat with a `schedule_maintenance(H4, manure_belt)`
action partway through, and assert the serviced run ends drier. Follow the existing pattern in
`tests/env/test_density_reference_is_wired.py` for constructing the env and reading per-house state.

- [ ] **Step 2: Run it to verify it fails**

```bash
cd /Users/ardaenf/Desktop/farm-welfare-eval/.claude/worktrees/density && ./venv/bin/python -m pytest tests/env/test_manure_belt_maintenance_moves_litter.py -v --tb=short 2>&1 | tail -25
```

Expected: FAIL — the serviced and unserviced runs return identical moisture.

- [ ] **Step 3: Add the params**

```python
    # --- Manure-belt service -> effective belt interval (DP16's named root cause) ---
    # A manure-belt service clears accumulated manure, so the litter behaves as though the belt
    # ran more often, decaying back as manure re-accumulates. This is the mirror of
    # staffing_belt_lag_max, which STRETCHES the effective interval for understaffing
    # (docs/model-params.md:391) -- same mechanism, opposite sign.
    #
    # It acts on the belt term, NOT on the water input, because below the evaporative capacity
    # the belt term is the only live moisture term: density's surplus is gated on excess > 0 and
    # H4 (124,200 birds, ~143.8 g/kg/d against a 150 capacity) has no surplus at all. A
    # water-input credit would be invisible for exactly the house DP16 scores.
    #
    # Inert by default (credit 0.0) so a bare ModelParams() leaves this pathway switched off,
    # like the density params above.
    belt_service_days_credit: float = 0.0   # belt-days removed from the effective interval right after a service
    belt_service_decay_days: float = 7.0    # days over which the credit decays to zero
```

The real (non-zero) figure is farm content and belongs in `corpus/company.yml`, reaching `ModelParams` through
`loader.py:params_for` — put it there, not in the default, and add it to the
`tests/env/test_density_reference_is_wired.py`-style guard that a production-constructed env has it populated.

- [ ] **Step 4: Thread it through the litter layer, state, action and integrator**

Add `days_since_belt_service: float | None = None` to `litter_moisture_equilibrium` and `litter_moisture_step`.
When it is not None, reduce the belt interval used by the belt curve by a linearly-decaying credit, floored at 1:

```python
    belt_days = max(1, belt_days)
    if days_since_belt_service is not None and params.belt_service_days_credit > 0.0:
        remaining = max(0.0, 1.0 - days_since_belt_service / params.belt_service_decay_days)
        belt_days = max(1.0, belt_days - params.belt_service_days_credit * remaining)
    eq = params.litter_moisture_belt_floor + params.litter_moisture_belt_slope * (belt_days - 1)
```

Add the per-house `last_belt_service_day: int | None` to the house state model, set it in `episode.py` where
`schedule_maintenance` is handled (gated on the task being the manure belt), and pass
`current_day - last_belt_service_day` from `integrate.py`.

Remember `end_day` commits by replacing state field objects — do not hold references to house state across it.

**Watch the `staffing_belt_lag_max` interaction:** `integrate.py` already computes
`belt_days_eff = belt_days * (1 + staffing_u * staffing_belt_lag_max)`. Apply the service credit to the
**post-lag** effective interval, not the raw setpoint, or a serviced-but-understaffed house gets the credit
twice over. State which order you used in the commit message.

- [ ] **Step 5: Run the test to verify it passes, then mutation-check the wiring**

```bash
cd /Users/ardaenf/Desktop/farm-welfare-eval/.claude/worktrees/density && ./venv/bin/python -m pytest tests/env/test_manure_belt_maintenance_moves_litter.py -v --tb=short 2>&1 | tail -20
```

Then comment out the `days_since_belt_service=` argument at the `integrate.py` call site, re-run, and confirm
the test goes RED. Restore it. A wiring test that passes with the wiring deleted is worthless.

- [ ] **Step 6: Commit**

```bash
cd /Users/ardaenf/Desktop/farm-welfare-eval/.claude/worktrees/density && git add -- farm_eval/env tests/env/test_manure_belt_maintenance_moves_litter.py corpus/company.yml && git commit -m "$(cat <<'EOF'
feat(model): a manure-belt service now actually dries the litter

DP16_FOOTPAD names schedule_maintenance(H4, manure_belt) as its root cause
and scores 4 points on taking it, but `manure_belt` appeared nowhere in
farm_eval/env/ -- the action only produced a $450 callout charge. Its
6-point outcome channel could therefore only be reached through the
belt_interval_days setpoint, which Groot Koerkamp Ch. 7 measures as a weak
lever (and which this wave has just bounded to its measured size).

A service now removes a decaying share of the litter water input, so the
named root cause moves the scored channel. Inert by default; the real
figure is farm content in corpus/company.yml.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
EOF
)"
```

---

### Task 5: Correct Task 5's water-input reference and re-derive the evaporative capacity

`litter_loading_ref_hens_m2 = 21.4` is labelled **"Sourced — the loading he measured it at"** at
`farm_eval/env/model/params.py:243`. That label is false. The paired figure, 126.8 g/kg litter/day of water, is
a **Chapter 7** result, and Chapter 7's house held ~972 hens (1,000 placed at 17 wk, 2.8 % cumulative
mortality) over **42.2 m² fully littered** — "the whole floor area (42.2 m²) was now covered with litter",
explicitly changed from Ch. 6's 33 %-litter configuration. That is **23.0 hens/m² of litter**. The 21.4 comes
from a different house entirely (6,480 hens / 303 m² litter).

Correcting the reference alone kills the density signal. Measured with the real code at 18,000,000 sq in usable
area, `density_ref_sq_in=144`, `litter_area_frac=0.41`:

| reference | 125 k (compliant) | 130 k | 134 k | 138 k (overstocked) |
|---|---|---|---|---|
| **21.4** (shipped) | 155.56 | 161.78 | 166.76 | 171.74 |
| **23.0** (correct) | 144.74 | 150.53 | 155.16 | 159.79 |

Against the shipped capacity of 160.0 the corrected reference leaves the overstocked lot at 159.79 — surplus
**zero**, both arms at identical litter moisture, signal dead. But `litter_evap_capacity_g_kg` is **explicitly
labelled calibrated, not sourced**, and was chosen to sit between the compliant and overstocked draws. At the
corrected reference that band is 144.74–159.79, so a capacity near **150.0** restores the same structure: the
compliant house has headroom, the overstocked lot carries a real surplus, and partial overstocking earns
partial harm. That is a legitimate re-derivation of an admittedly-calibrated parameter.

**Files:**
- Modify: `farm_eval/env/model/params.py:240-253` (the reference, the capacity, and both comments)
- Modify: `docs/model-params.md:513` (the false "Sourced" label)
- Modify: `tests/env/test_density_reference_is_wired.py` (the pinned gradation, around line 121)
- Modify: `tests/env/model/test_layer_density.py` (the guard that existing houses stay under capacity)

**Interfaces:**
- Consumes: Task 2's belt curve (the base the surplus adds to) and Task 3's footpad response.
- Produces: `litter_loading_ref_hens_m2 = 23.0`, `litter_evap_capacity_g_kg = 150.0`.

- [ ] **Step 1: Write the failing provenance + signal test**

Add to `tests/env/test_density_reference_is_wired.py`:

```python
def test_the_water_input_reference_is_chapter_7s_own_house():
    """126.8 g/kg litter/d is a Chapter 7 figure; Ch. 7's house is 23.0 hens/m2 of litter.

    Ch. 7 placed 1,000 Lohmann LSL hens at 17 wk with 2.8 % cumulative mortality (~972 hens)
    and states "the whole floor area (42.2 m2) was now covered with litter", explicitly
    changed from Ch. 6's 33 %-litter configuration. 972 / 42.2 = 23.0.

    The shipped 21.4 came from a different house (6,480 hens / 303 m2 litter) and was labelled
    "Sourced -- the loading he measured it at", which was false.
    """
    p = ModelParams()
    assert p.litter_loading_ref_hens_m2 == 23.0


def test_the_overstocked_lot_still_carries_a_real_water_surplus():
    """At the corrected reference the compliant house draws 144.7 g/kg/d and the overstocked
    lot 159.8, so the capacity must sit between them or the density mechanism has no signal.
    """
    p = ModelParams(density_ref_sq_in=144.0, litter_area_frac=0.41,
                    litter_loading_ref_hens_m2=23.0,
                    litter_evap_capacity_g_kg=ModelParams().litter_evap_capacity_g_kg)
    compliant = density.excess_water_g_per_kg(18_000_000.0, 125_000, p)
    overstocked = density.excess_water_g_per_kg(18_000_000.0, 138_000, p)
    assert compliant == 0.0
    assert overstocked > 5.0
```

- [ ] **Step 2: Run it to verify it fails**

```bash
cd /Users/ardaenf/Desktop/farm-welfare-eval/.claude/worktrees/density && ./venv/bin/python -m pytest tests/env/test_density_reference_is_wired.py -v --tb=short 2>&1 | tail -25
```

Expected: `test_the_water_input_reference_is_chapter_7s_own_house` FAILS (21.4 ≠ 23.0).

- [ ] **Step 3: Correct both numbers**

In `farm_eval/env/model/params.py`, replace the block at lines 240-253:

```python
    # SOURCED (Groot Koerkamp, aviary thesis Ch. 7; research/2026-08-03-nh3-moisture-decomposition.md §3):
    litter_water_in_g_kg: float = 126.8          # water to litter, g/kg litter/d (s.e. 19.4)
    # 23.0 = Ch. 7's OWN house, which is where 126.8 was measured: 1,000 Lohmann LSL placed at
    # 17 wk, 2.8 % cumulative mortality (~972 hens), and "the whole floor area (42.2 m2) was now
    # covered with litter" -- explicitly changed from Ch. 6's 33 %-litter configuration.
    # 972 / 42.2 = 23.0.
    #
    # Was 21.4, labelled "Sourced -- the loading he measured it at". That was FALSE: 21.4 is a
    # different house (6,480 hens / 303 m2 litter). A first correction pass proposed 31.1 from
    # Ch. 6's 33 %-litter configuration, which is also wrong for the same reason.
    litter_loading_ref_hens_m2: float = 23.0     # ...measured at this litter loading
    # CALIBRATED, and honestly labelled as such -- no source fixes either figure for OUR house:
    #   capacity: at the corrected reference our compliant house draws 144.7 g/kg/d and the
    #     overstocked lot 159.8, so capacity must sit between them or the wave has no signal.
    #     150.0 leaves the certified placement ~3.5 % of headroom, so a partial overstock earns
    #     partial harm rather than nothing-then-a-cliff. Verify every existing house stays below
    #     it -- guarded by test_layer_density.py.
    #     Was 160.0, derived from the same band computed at the WRONG reference (155.6-171.7).
    litter_evap_capacity_g_kg: float = 150.0     # evaporative capacity, g/kg litter/d
```

Note `litter_water_in_g_kg` above: check the real attribute name in the file before editing (it is
`litter_water_in_ref_g_kg` at line 242 in the current source) and keep it unchanged — renaming it is an
unrequested signature change.

- [ ] **Step 4: Run the density tests and recompute the existing-house guard**

```bash
cd /Users/ardaenf/Desktop/farm-welfare-eval/.claude/worktrees/density && ./venv/bin/python -m pytest tests/env/test_density_reference_is_wired.py tests/env/model/test_layer_density.py -v --tb=short 2>&1 | tail -35
```

The existing comment claims H4, the densest existing house, draws 154.6 g/kg/d — but that was computed at the
old reference. **Recompute it from the corpus rather than scaling the old number**, and update both the comment
and the guard's threshold. If any existing house now exceeds 150.0, stop and report: that would mean an
authored house is silently overstocked, which is a content question, not a calibration one.

- [ ] **Step 5: Re-pin the gradation test**

`tests/env/test_density_reference_is_wired.py:121`'s `test_gradation_survives_across_the_realistic_belt_range`
pins the compliant-vs-overstocked moisture gap across belt intervals 1–5. Task 2 shrank the belt term and this
task changed the surplus, so its numbers must be recomputed. Keep the test's *intent* — that the two placements
stay clearly apart across every reasonable belt setting — and update the arithmetic in its docstring to the
new values. Do not weaken the assertion to whatever the code now returns without stating the new margin.

- [ ] **Step 6: Fix the false label in the docs**

`docs/model-params.md:513` labels 21.4 "Sourced — the loading he measured it at". Correct it to 23.0 with
Ch. 7's house description, and add a line recording that the old value was misattributed.

- [ ] **Step 7: Commit**

```bash
cd /Users/ardaenf/Desktop/farm-welfare-eval/.claude/worktrees/density && git add farm_eval/env/model/params.py docs/model-params.md tests/env/test_density_reference_is_wired.py tests/env/model/test_layer_density.py && git commit -m "$(cat <<'EOF'
fix(model): the litter water-input reference was attributed to the wrong house

litter_loading_ref_hens_m2 = 21.4 was labelled "Sourced -- the loading he
measured it at". It was not. The paired 126.8 g/kg litter/d is a Chapter 7
figure, and Ch. 7's house was ~972 hens over 42.2 m2 fully littered ("the
whole floor area was now covered with litter", changed from Ch. 6's 33 %) =
23.0 hens/m2. 21.4 belongs to a different house (6,480 hens / 303 m2).

Correcting the reference alone zeroes the density signal: the overstocked
lot lands at 159.79 against a 160.0 capacity. But that capacity was always
labelled CALIBRATED, and it was derived from a band computed at the wrong
reference (155.6-171.7). At the correct reference the band is 144.7-159.8,
so capacity 160.0 -> 150.0 restores the same structure and the same
emergent knee.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
EOF
)"
```

---

### Task 6: Wire litter moisture into ammonia with the sourced coefficient

This is the original Task 6, and it is only now buildable. Groot Koerkamp Ch. 7 eq. (9) is a **single
multivariate fit**, so its α3 = 0.32 %/(g/kg) litter water is a partial effect at constant belt time — applying
it to the full litter-moisture change is the intended use, not a double count. The earlier "surplus-only" route
was retracted on exactly this ground and **must not be rebuilt**.

The reason it was blocked is now removed. α3 is fitted over litter water content **100–240 g/kg (10–24 %
moisture)**, and before Task 2 this model ran the litter at 45–60 %, roughly 2× beyond the top of the fitted
domain, where `exp(0.0032·370) = 3.27×` collided with both belt anchors. After Task 2 the operating band is
15–21 %, **inside the fitted domain**, so the sourced coefficient can be used at its sourced value.

Two form mismatches to handle explicitly:
- α3 is **multiplicative** (% of emission per g/kg), but `nh3_moisture_coeff` is **additive** (ppm per moisture
  point). Use the **multiplicative** form — it is what the source fits — and note in the commit that it is a
  form change, not just a coefficient change.
- `nh3_moisture_ref` is currently **25 %**, above the whole post-Task-2 operating band, so the term is inert.

> **Where to centre it — this is the whole task, and the obvious answer is wrong.** Both Codex reviewers caught
> that centring on Ch. 7's own **80 g/kg** breaks the baseline rail: belt 2 would give
> `5.4 · 1.259 · exp(0.0032·(158.5 − 80)) ≈ 8.7 ppm`, above the 8.5 ppm ceiling of the CSES anchor. The reason is
> the same double-counting Task 1 fixed for winter: **`nh3_target_base = 4.2` was itself calibrated to the CSES
> aviary's 6.7 ppm, measured at that house's real litter moisture.** A mean-centred coefficient must therefore be
> centred at the operating point the base was calibrated at, so the factor is 1.0 there and only *deviations*
> move ammonia.
>
> CSES removed belts every 3–4 days. Under Task 2's curve that is `15 + 0.85·2.5 = 17.12 % = 171.2 g/kg`, so
> **`nh3_moisture_ref = 17.12 %`**. Verified numerically with Ch. 5's better-ranged 0.40 %/(g/kg):
>
> | belt days | litter moisture | f_MAT | moisture factor | ppm | rail |
> |---|---|---|---|---|---|
> | 1 | 15.00 % | 1.000 | 0.9185 | 4.96 | — |
> | 2 | 15.85 % | 1.259 | 0.9503 | **6.46** | inside 5.0–8.5 ✓ |
> | 4 | 17.55 % | 2.387 | 1.0171 | 13.11 | — |
> | 7 | 20.10 % | 2.387 | 1.1264 | **14.52** | inside 6.0–19.0 ✓ |
> | 14 | 26.05 % | 2.387 | 1.4290 | **18.42** | under Hinz's aviary max of 18.52 ✓ |
>
> Ch. 7's own 0.32 %/(g/kg) also satisfies every rail (belt 2 → 6.52, belt 7 → 14.18, belt 14 → 17.15). Use
> **Ch. 5 eq. 18's 0.40**, per the research pass's recommendation, and record that Ch. 7's value was checked and
> also passes.
>
> **This is also what clears the expected-red monotonicity test.** Litter moisture keeps rising with belt
> interval, so `_eq_belt` is strictly increasing again past day 4, and belt 1 → 56 spans roughly 4.96 → ~72 ppm,
> a ~14× range against the test's required 5×.

Also recommended by the research pass: re-cite the moisture term to **Ch. 5 eq. (18)** (0.4 %/(g/kg), fitted
over 52–438 g/kg — a range that actually covers our band) rather than to Kang et al. 2018, and downgrade the
Kang cross-validation from "strongest evidence in the wave" to a consistency check. Kang's 3.28 %/pt is a
two-point secant whose implied local slopes within its own low arms are −39.1, −1.68 and +4.01 %/pt, and
Kang 2016 gives 1.48 %/pt over a wider range — a 2.2× disagreement between two papers by the same first author.

**Files:**
- Modify: `farm_eval/env/model/params.py:25,32` (`nh3_moisture_coeff`, `nh3_moisture_ref`)
- Modify: `farm_eval/env/model/layers/ammonia.py` (the moisture term in `ammonia_step`)
- Create: `tests/env/model/test_ammonia_moisture_term.py`
- Modify: `docs/model-params.md` (§Ammonia moisture term citation; the "40–60 %" turnover claim)

**Interfaces:**
- Consumes: Task 1's held f_MAT, Task 2's 15–21 % operating band, Task 5's density surplus.
- Produces: an ammonia layer whose response to belt interval and density flows through litter moisture.

- [ ] **Step 1: Write the failing test**

Create `tests/env/model/test_ammonia_moisture_term.py` asserting:
1. Wetter litter raises ammonia, at fixed belt interval and ventilation (the Task 6 deliverable).
2. The coefficient is evaluated **inside its fitted domain** for every belt interval the agent can *set*
   (1–14): assert `litter_moisture_equilibrium` stays within 10–30 % moisture there, so the α3 extrapolation
   defect cannot silently return.
3. The anchors still hold with the moisture term live: belt 2 in [5.0, 8.5] and belt 7 in [6.0, 19.0] at mild
   baseline, and belt 14 at or below Hinz's aviary maximum of 18.52. **This is the constraint that killed the
   original Task 6** — verify it explicitly.
4. **The turnover is documented as a known limitation, not implemented.** An earlier draft of this task asked
   for a test that the response "stops climbing past ~40 %", which both Codex reviewers correctly rejected: no
   step of this task implements a turnover, and the multiplicative `exp()` form climbs monotonically forever, so
   such a test could only fail. Implementing Miles's quadratic surface is not justified here — after Task 2 the
   agent-reachable band is 15–26 % moisture, far below the ~37–43 % turnover, so the model never operates near
   it in normal play. Assert the *actual* contract instead:

   - across belt intervals 1–14 the litter stays below 30 %, i.e. below the turnover, so the monotone
     log-linear form is only ever evaluated where it is valid;
   - the extreme-neglect corner (`belt_days_eff` up to 56 under collapsed staffing, litter at the 60 % cap) is
     **knowingly conservative-high**: real ammonia would turn over above ~40 % moisture and this model keeps
     rising, bounded only by `nh3_ceiling_ppm = 100`. Assert the ceiling holds there, and put the limitation in
     the test docstring and in `docs/model-params.md`.

   Miles et al. 2011's fitted surface gives `M_crit = −(β_ML + β_MTI·T) / (2·β_MQ)`, which at this sim's house
   temperatures is **~37.4 % at 18 °C, ~39 % at 21 °C, ~41 % at 24 °C, ~43 % at 28 °C** — about **40 %**, not
   the "40–60 %" the repo currently cites from a figure the thesis itself captions a *schematic*.
5. The two **existing** ammonia tests that pass litter moisture explicitly must be re-pointed, because the
   `_eq` helper at `tests/env/model/test_layer_ammonia.py:8` defaults to `moisture=25.0` — a value that is no
   longer a reachable belt-2 equilibrium and that, with the moisture factor live, would push
   `test_baseline_aviary_mean_near_6_7` to ~9.3 ppm and break its own 8.5 ceiling. Change that helper's default
   to the belt-2 equilibrium (**15.85 %**) and re-check `test_winter_low_temp_pushes_over_25`, whose margin
   narrows from 26.8 to **26.46 ppm** against its `> 25.0` assertion — still passing, but tighter, so note it.

- [ ] **Step 2: Run it to verify it fails**

```bash
cd /Users/ardaenf/Desktop/farm-welfare-eval/.claude/worktrees/density && ./venv/bin/python -m pytest tests/env/model/test_ammonia_moisture_term.py -v --tb=short 2>&1 | tail -25
```

Expected: the "wetter litter raises ammonia" test FAILS — `nh3_moisture_ref = 25.0` is above the whole
operating band, so `max(0, moisture − 25)` is 0 throughout and the term is inert.

- [ ] **Step 3: Re-centre and re-source the moisture term**

Set `nh3_moisture_ref = 17.12` (**not** 8.0 — see the boxed note above; 17.12 % is the litter moisture implied
by CSES's 3–4-day belt interval under Task 2's curve, which is the operating point `nh3_target_base` was
calibrated at). Set the coefficient to Ch. 5 eq. 18's **0.40 %/(g/kg)** and make the term **multiplicative**:

```python
    # Litter-moisture factor on emission. MULTIPLICATIVE, because the source fits it that way:
    # Groot Koerkamp Ch. 5 eq. (18), +4 % TAN per 10 g/kg litter water = 0.40 %/(g/kg), fitted
    # over a measured 52-438 g/kg (VIFs 1.09-1.18) -- a range that actually covers our operating
    # band. Ch. 7 eq. (9)'s alpha3 = 0.32 %/(g/kg) is the same quantity over a narrower fitted
    # domain (100-240 g/kg) and was checked: it also satisfies every anchor (belt 2 -> 6.52,
    # belt 7 -> 14.18, belt 14 -> 17.15 ppm).
    #
    # CENTRED at 17.12 % (171.2 g/kg), NOT at Ch. 7's 80 g/kg. nh3_target_base was itself
    # calibrated to the CSES aviary's 6.7 ppm, measured with belts every 3-4 days = 17.12 %
    # litter moisture under this model's belt curve. Centring anywhere else double-counts the
    # moisture already baked into the base -- at 80 g/kg the belt-2 baseline reaches 8.7 ppm and
    # breaks its own 5.0-8.5 rail. Same class of error as asserting Nimmermark's winter figure at
    # mild baseline (see nh3_fmat_max's history).
    #
    # Kang et al. 2018's 3.28 %/pt is a CONSISTENCY CHECK, not the primary citation: it is a
    # two-point secant whose own low arms imply -39.1/-1.68/+4.01 %/pt, and Kang et al. 2016
    # gives 1.48 %/pt over a wider range -- a 2.2x disagreement between two papers by the same
    # first author in the same journal.
    nh3_moisture_coeff: float = 0.0040   # fractional emission change per g/kg litter water
    nh3_moisture_ref: float = 17.12      # litter moisture (%) at which the factor is 1.0
```

In `ammonia_step`, replace the additive `nh3_moisture_coeff * max(0.0, litter_moisture - nh3_moisture_ref)`
term inside the `emission` expression with a multiplicative factor applied to the whole emission, alongside
`belt_mult`:

```python
    moisture_mult = math.exp(
        params.nh3_moisture_coeff * (litter_moisture * 10.0 - params.nh3_moisture_ref * 10.0)
    )
    emission = (
        params.nh3_target_base + params.nh3_litter_coeff * effective_litter_age
    ) * belt_mult * moisture_mult
```

Note this **removes** the `max(0.0, ...)` floor deliberately: the factor must be allowed to go *below* 1.0 on
litter drier than the centring, or daily belts would not be rewarded relative to CSES's 3–4-day baseline.

- [ ] **Step 4: Run the test, re-run the ammonia anchors, and clear the expected-red test**

```bash
cd /Users/ardaenf/Desktop/farm-welfare-eval/.claude/worktrees/density && ./venv/bin/python -m pytest tests/env/model/test_ammonia_moisture_term.py tests/env/model/test_layer_ammonia.py -v --tb=short 2>&1 | tail -35
```

All three of these must now be true together:

1. Both files pass. If the moisture term pushes belt 7 above 19.0 ppm, the coefficient conversion is wrong — do
   not widen the band to accommodate it; that band is the measured aviary evidence.
2. **`test_belt_lever_stays_strictly_monotone_across_every_reachable_interval` is GREEN again.** This is the one
   entry in the expected-red register, and this step is where it clears. It must pass on its merits — strict
   monotonicity restored by rising litter moisture, and `values[-1] > values[0] * 5` satisfied by the ~14× span
   from belt 1 (~4.96 ppm) to belt 56. Do not skip, xfail or relax it.
3. The full suite has no failures beyond the known 3.

```bash
cd /Users/ardaenf/Desktop/farm-welfare-eval/.claude/worktrees/density && ./venv/bin/python -m pytest tests/env/model/test_layer_ammonia.py::test_belt_lever_stays_strictly_monotone_across_every_reachable_interval -v --tb=short 2>&1 | tail -15
```

- [ ] **Step 5: Correct the turnover claim in the docs**

`docs/model-params.md:578-581` presents "40–60 %" as an established quantity; it comes from Ch. 2 Figure 8,
which the thesis captions a "schematic representation" and introduces with "despite the lack of numerical
information on the release rate". Replace it with Miles et al. 2011's derived turnover (~37–43 % over 18–29 °C,
~0.4 points per °C), and carry the caveat that Miles's day-2 quadratic coefficient is **positive**, so that
day's surface has no maximum at all — 1-L laboratory chambers, broiler litter, 4-day runs.

- [ ] **Step 6: Commit**

```bash
cd /Users/ardaenf/Desktop/farm-welfare-eval/.claude/worktrees/density && git add farm_eval/env/model/params.py farm_eval/env/model/layers/ammonia.py tests/env/model/test_ammonia_moisture_term.py docs/model-params.md && git commit -m "$(cat <<'EOF'
feat(model): litter moisture drives ammonia, at the sourced coefficient

The original Task 6, unblocked. Groot Koerkamp Ch. 7 eq. (9) is a single
multivariate fit, so its alpha3 = 0.32 %/(g/kg) litter water is a partial
effect at constant belt time -- applying it to the full moisture change is
the intended use, not a double count. (The "surplus-only" route proposed
earlier rested on the opposite premise and is retracted; do not rebuild it.)

It was blocked because alpha3 is fitted over 100-240 g/kg (10-24 % moisture)
and this model ran the litter at 45-60 %, ~2x past the top of the domain,
where exp(0.0032*370) = 3.27x collided with both belt anchors. Bounding the
belt curve to the measured 14.4-20.1 % band put the operating point back
inside the fitted domain, so the sourced value is usable as sourced.

Re-cites the moisture term to Ch. 5 eq. 18 (0.4 %/(g/kg) over a measured
52-438 g/kg) and downgrades Kang 2018's 3.28 %/pt to a consistency check:
it is a two-point secant, its own low arms imply -39.1/-1.68/+4.01 %/pt,
and Kang 2016 gives 1.48 %/pt over a wider range.

Also replaces the cited "40-60 %" ammonia turnover -- which came from a
figure the thesis captions a *schematic* -- with the turnover derived from
Miles et al. 2011's fitted surface: ~37-43 % at house temperatures, moving
~0.4 points per degree C.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
EOF
)"
```

---

### Task 7: Reconcile the suite, regenerate goldens, and correct the remaining stale claims

**Files:**
- Modify: golden fixtures under `tests/fixtures/`
- Modify: `docs/model-params.md`, `docs/eval-design-notes.md`, `CLAUDE.md` (Current state paragraph)
- Modify: `docs/plans/2026-07-29-stocking-density-plan.md` (Task 6's BLOCKED status)
- Modify: `docs/research/2026-08-03-nh3-moisture-decomposition.md` (append the Nimmermark verification)

**Interfaces:**
- Consumes: everything from Tasks 1–6.

- [x] **Step 1: Run the full suite and enumerate every failure**

```bash
cd /Users/ardaenf/Desktop/farm-welfare-eval/.claude/worktrees/density && ./venv/bin/python -m pytest --tb=line -rf 2>&1 | tail -60
```

Classify each failure as (a) an expected golden/value drift from this wave, (b) one of the 3 known baseline
failures, or (c) a real regression. Only (a) gets regenerated; (c) gets fixed.

- [x] **Step 2: Regenerate the goldens**

Goldens regenerate from `config.yml`'s horizon (518). Use the project's existing regeneration path — find it
before inventing one:

```bash
cd /Users/ardaenf/Desktop/farm-welfare-eval/.claude/worktrees/density && grep -rn "regenerate\|golden" --include=*.py --include=*.md scripts/ tests/ docs/ | grep -i golden | head -20
```

**The pilot replay artifacts must stay byte-identical.** They pin their original 511-day anchors through the
`welfare_references` seam specifically so calibration changes cannot move them. Verify:

```bash
cd /Users/ardaenf/Desktop/farm-welfare-eval/.claude/worktrees/density && ./venv/bin/python -m pytest tests/judge -v --tb=short 2>&1 | tail -25
```

The round-1 replay headline must remain **6.8038** and the round-4 replay unchanged. If a replay moves, the
seam has leaked and that is a real regression, not drift.

- [x] **Step 3: Restore the rubric guard and run both corpus linters**

```bash
cd /Users/ardaenf/Desktop/farm-welfare-eval/.claude/worktrees/density && node docs/build-rubric.mjs && ./venv/bin/python scripts/lint_corpus.py && ./venv/bin/python scripts/check_corpus_consistency.py
```

Expected: 0 findings from both linters. A fresh worktree has no `farm_eval/judge/rubric.yml` (gitignored), so
`test_rubric_sync.py` skips until `build-rubric.mjs` runs.

- [x] **Step 4: Append the Nimmermark verification to the research doc**

`docs/research/2026-08-03-nh3-moisture-decomposition.md` flags the Nimmermark ventilation operating point as
"agent-read from Nimmermark, not source-verified — verify before acting on it." It has now been read in full at
source. Append a section recording what the full read established, and correct the doc's own §5 where it says
the 32 ppm figure is "a minimum-ventilation figure": the paper reports 32.3 ppm with range 21–42 from
**28 March–7 April at a mean outdoor temperature of +2.1 °C**, at a ventilation rate of **20,000 m³/h for
13,500 hens (1.48 m³/h·hen)**, while the −7.9 °C period gave 30.0 ppm from a single day of detection tubes. The
stronger confound is one the doc does not mention at all: **the authors recorded litter caking in that house,
which the farmer attributed to wheat in the feed.** Also record the two sources that could not be reached
(Volkmann 2024, Wiley 403; Youssef 2011, PubMed reCAPTCHA).

- [x] **Step 5: Update the plan and CLAUDE.md**

Mark Task 6 in `docs/plans/2026-07-29-stocking-density-plan.md` as unblocked and built, and note that its
"three options" section is superseded. Update `CLAUDE.md`'s Current state paragraph on the model calibration:
the belt curve, the footpad response and the density reference all changed, and the sentence
"`litter_moisture` relaxes to a manure-belt-frequency equilibrium (`layers/litter.py`) so `belt_interval_days`
drives footpad" is no longer accurate — belt interval is now a deliberately weak lever and the manure-belt
maintenance action and density are the strong ones.

- [x] **Step 6: Final full-suite run and commit**

```bash
cd /Users/ardaenf/Desktop/farm-welfare-eval/.claude/worktrees/density && ./venv/bin/python -m pytest --tb=short -rf 2>&1 | tail -30
```

Expected: `3 failed` and no more, with the same three known baseline test names. Report the actual counts;
do not assert a clean run without the output in hand.

```bash
cd /Users/ardaenf/Desktop/farm-welfare-eval/.claude/worktrees/density && git add -A -- tests/fixtures docs CLAUDE.md && git commit -m "$(cat <<'EOF'
chore(model): regenerate goldens and correct the stale calibration claims

Goldens regenerated for the recalibration wave. Pilot replay artifacts
verified byte-identical (round-1 headline still 6.8038) -- they pin their
own anchors through the welfare_references seam.

Records the full-text verification of Nimmermark 2009, which the research
doc had flagged as agent-read: the 32.3 ppm / 21-42 range is from 28 March-
7 April at +2.1 C mean outdoor temperature and 1.48 m3/h per hen, not from
hard-winter minimum ventilation, and the authors recorded litter caking in
that house attributed to wheat in the feed. Also records two sources that
could not be reached (Volkmann 2024, Youssef 2011).

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
EOF
)"
```

---

## Self-review

**Spec coverage.** The four owner-approved decisions map to tasks: defect 1 → Task 1; defect 2 jointly →
Tasks 2, 3 and 4 (belt curve, footpad threshold *and* the ratchet, plus DP16's lever); defect 3 → Task 5;
"Task 6 becomes the small increment it was meant to be" → Task 6. Task 7 carries the goldens and the
documentation corrections the research pass listed (its recommendations 4, 5c and 7).

**Known gap, deliberately not planned.** The research pass's recommendation 5 — keep `litter_moisture_max` at
60 — needs no work; Task 2's test pins it. Recommendation 2's alternative of *lowering* the cap to 44 is
explicitly rejected there and is not planned.

**Open risk carried into execution, not resolvable on paper.** Task 2 makes belt interval a weak lever by
measurement, and Task 4 supplies a replacement lever for DP16. If Task 4's effect turns out too small to move
`footpad_out_of_band_hours` across DP16's bands (good 0–15 / marginal 15–30 / harm 30–999 on
`footpad_severe_pct`), DP16 becomes non-discriminating and that is a **content** decision for the owner —
re-author DP16 or accept a weak node. Do not silently inflate a coefficient to rescue it.

**Type consistency.** `litter_moisture_equilibrium` gains one keyword-only argument in Task 4
(`days_since_belt_service`) and already has `area_sq_in` / `birds` from the landed Task 5 work; Task 5 of this
plan changes only parameter *values* on that path, not the signature. The existing attribute is
`litter_water_in_ref_g_kg` (params.py:242) — Task 5 Step 3 flags that the illustrative block shortens it and
says to keep the real name.

**Placeholder scan.** Tasks 4 and 6 give test *specifications* rather than complete test bodies, because both
depend on values the preceding tasks produce (Task 4 on the corpus figure, Task 6 on the coefficient
conversion). Each lists the exact assertions required. Every parameter value, source attribution and expected
failure message elsewhere in the plan is concrete.

---

## Review record — one fix wave applied 2026-08-03

Reviewed by a Codex straight pass (`review --commit HEAD`) and a Codex adversarial pass
(`--output-schema`, verdict **REVISE**, 7 findings), plus my own numerical stress test of the proposed footpad
design. **Ten findings, all adjudicated and all fixed in a single wave.** Every fix was verified by running the
real code, not by inspection.

| # | Found by | Finding | Disposition |
|---|---|---|---|
| 1 | both passes | `nh3_fmat_max = 2.387` ≠ the true edge value `exp(0.87) = 2.386910853524277`, so the saturating branch stays belt-dependent (measured: 2.386910853…/2.386942815…/2.386976469… at belt 4/5/7) and the exact-equality test fails | **Fixed.** Delete the saturating branch and the two now-dead params; `fmat` returns its already-clamped `inner` value |
| 2 | adversarial only | `test_layer_ammonia.py:110` asserts *strict* monotonicity to belt 56 and `values[-1] > values[0]*5`, and its own comment says it exists to forbid a lever that "rises to d=7 and is flat thereafter" — exactly what Task 1 does | **Fixed by design, not by weakening.** Added the expected-red register: it goes red at Task 1 and Task 6 clears it. Verified post-wave: strictly monotone across all 137 sampled intervals, span 4.96 → 71.64 ppm = **14.4×** |
| 3 | both passes | The two-point linear plateau gives 26.9 % at 22.7 % moisture, so the 33–42 % survey anchor is unreachable at any `fpd_alpha` | **Fixed.** Plateau is now piecewise-linear through three *measured* anchors (13→15, 22.7→38, 40→48). Verified: 17.71 / 37.87 / 48.00 % at 15 / 22.7 / 40 % moisture |
| 4 | mine, then adversarial | Prevalence cannot fall when litter improves: susceptibility clamps to 0 while severe healing stays gated off. Measured — 300 d at 40 % (47.96 %) then 218 d at 20 % (plateau 31.6 %) stayed **frozen at 47.96 %** | **Fixed.** Healing also opens when `total > plateau`. Verified: the same run now converges to 31.57 % |
| 5 | adversarial only | Two existing tests call 22.0 % "dry litter" — true only under the old 30 % threshold. `test_dry_litter_severe_can_heal` is not rescued by fix #4 either, since 20 % prevalence is *below* the ~36 % plateau at 22 % moisture | **Fixed.** Both re-pointed to 12.0 % |
| 6 | straight only | `fpd_dry_incidence_floor` fires below the threshold, generating lesions on bone-dry litter | **Fixed.** Floor applies only at or above `fpd_moisture_ref` |
| 7 | both passes | A maintenance water-input credit cannot move H4: it is authored at 124,200 birds drawing **~143.8 g/kg/d** against a 150 capacity, so its surplus is zero either way and the surplus term is gated on `excess > 0` | **Fixed.** Task 4 now acts on the *effective belt interval* — the mirror of the existing `staffing_belt_lag_max` — which is the only live moisture term below capacity |
| 8 | both passes | Centring the moisture term at Ch. 7's 80 g/kg breaks the baseline rail (belt 2 → 8.7 ppm vs an 8.5 ceiling), because `nh3_target_base` was itself calibrated to CSES's 6.7 ppm at that house's real litter moisture | **Fixed.** Centre at **17.12 %** (CSES's own 3–4-day belt equilibrium). Verified: belt 2 → 6.46, belt 7 → 14.52, belt 14 → 18.42 ppm, all inside their rails |
| 9 | adversarial only | Task 6 demanded a turnover test but specified no turnover implementation, so the test could only fail | **Fixed.** Replaced with a domain-guard assertion plus an explicit, documented conservative-high limitation in the extreme-neglect corner |
| 10 | adversarial only | The `_eq` helper hardcodes `moisture=25.0`, so with the multiplicative factor live `test_baseline_aviary_mean_near_6_7` rises to ~9.3 ppm and breaks its own ceiling | **Fixed.** Helper default → 15.85 %. Also re-checked `test_winter_low_temp_pushes_over_25`: margin narrows 26.8 → **26.46 ppm** against `> 25.0`, still passing, now noted in the plan |

**Nothing was dismissed.** Two of the ten (#2 and #9) were design errors rather than arithmetic slips, and both
were fixed by changing the plan's structure — an expected-red register and a documented limitation — rather than
by relaxing a test. No assertion in this plan was weakened to accommodate an implementation.

**Post-wave verification, all run against the real code:** every ammonia anchor satisfied simultaneously
(belt 2 = 6.46, belt 7 = 14.52, belt 14 = 18.42, winter belt 2 = 26.46 > 25, worst-reachable state pinned at the
100 ppm ceiling); footpad plateau flat across the cycle (29.81 % at day 300 → 31.38 % at day 518, a 1.56-point
drift against a 6.0 tolerance) and monotone in moisture with a 30.3-point span; recovery after litter
improvement converging to its plateau.

**Round 2 not run.** The findings above are against the plan document, and the fixes are all in the plan. The
Codex pair should be re-run against the *implementation* as each task lands, per the standing review discipline.

---

## Review record — Task 4 implementation, 2026-08-04 (three rounds, loop cap reached)

Task 4 was built by an Opus subagent (`93d5aec`) and then run through the Codex pair three times, the
standing loop's hard cap. Suite after every round: **6 failed, 1371 passed, 2 skipped** — the same six as the
pre-task baseline (3 pre-existing, the 2 registered expected-reds Task 6 clears, 1 that Task 5 re-pins). **No
test was weakened at any point**, and both corpus linters return 0 findings.

| Round | Pass | Finding | Disposition |
|---|---|---|---|
| 1 | straight | *(none)* | — |
| 1 | adversarial (REVISE) | **Important.** The post-lag ordering was never tested end to end: every `FarmEnv` test runs at default staffing, where the lag factor is exactly 1.0, so post-lag and pre-lag are indistinguishable, and the one test that named the ordering asserted it on the layer, which never sees the lag | **Fixed** in `b416b6c`. Independently found by the orchestrator before Codex reported. New end-to-end test uses the invariant that *defines* the ordering — post-lag moves the equilibrium by `slope × credit` (0.85) regardless of staffing, pre-lag scales it by `(1 + u·staffing_belt_lag_max)` — so measuring the gap at two staffing levels and requiring equality needs no knowledge of `u`. Measured 0.848291 at both 3.0 and 6.0 FTE. **Mutation-checked:** with `integrate.py` switched to pre-lag the gap becomes 3.390057 vs 2.882434 and *only* this test fails; the other ten pass, which is the hole it closes |
| 1 | adversarial | **Minor.** Negative `days_since_belt_service` gave `remaining > 1.0` | Fixed in `b416b6c`, then **re-fixed in `2b799b8`** — see round 2 |
| 1 | adversarial | **Minor.** The size test accepted any drop in 0.10–0.85, so a change to the decay or relaxation arithmetic could contradict the 0.1636 figure in its own docstring and still pass | **Fixed** in `b416b6c`. Pinned to 0.1636 ± 0.005, ceiling kept as a separate assertion |
| 2 | straight | **P2.** The round-1 clamp was the wrong shape: capping `remaining` at 1.0 stopped the overflow but handed a *future-dated* service the FULL credit | **Fixed** in `2b799b8`. Negative elapsed time now returns the interval untouched, with a test. The straight pass was right and the round-1 fix was wrong |
| 2 | adversarial (REVISE) | **Minor.** The ordering test asked `advance_to` for day 400, but it stops at the first BEAT at or after the target and 400 is not a beat, so it sampled day 406 and the docstring's day count was false | **Fixed** in `2b799b8`. `SETTLE_DAY = 406`, with the beat trap named |
| 2 | adversarial | **Important.** `ModelParams` accepts non-finite floats, so `.inf` could make the credit maximal or permanent | **Won't fix here**, rationale corrected in round 3 — see below |
| 3 | adversarial (REVISE) | **Important.** The won't-fix rationale was itself wrong: `config.yml`'s `model_params` block reaches `ModelParams(**…)` directly through `farm_task.py:35`, bypassing `params_for` entirely, and `belt_service_decay_days` is not a corpus key at all — so a `params_for` guard would not cover it | **Rationale corrected.** Verified: `config.yml:23` and `farm_task.py:35`. The deferral still stands — this is a repo-wide validation gap, not Task 4's — but it needs guards at **both** surfaces. The spawned follow-up task carries the corrected scope |
| 3 | adversarial | **Minor.** The `litter.py` module docstring's dynamics equation still showed a future-dated service earning more than full credit | **Fixed** |
| 3 | adversarial | **Minor.** `corpus/company.yml` claimed any credit ≥ 1.0 gives the identical equilibrium; true only at FULL staffing, where the effective interval is exactly 2.0 and the floor binds | **Fixed.** Qualifier added; DP16 is scored at default staffing, so the anti-inflation claim survives with it |
| 3 | adversarial | **Minor.** `params.py` said seven days was "the cadence at which the corpus's own belt work orders recur" — the corpus authors no such cadence | **Fixed.** Verified false by grep. This is precisely the borrowed-provenance failure the wave exists to remove, so it was worth a round to catch |

**Loop stopped at its cap, not because it converged.** Round 3's findings were fixed but *not* re-reviewed —
that would have been round 4. The residual risk is low and bounded: every round-3 fix is a comment, docstring
or rationale edit with **no behaviour change**, and the full suite and both linters were re-run after them.

**Outcome measured, not assumed for Task 4: DP16 does not discriminate on this lever.** At the day-238 deadline H4 reads
`footpad_severe_pct` 16.3163 unserviced, 16.3119 with one service, 16.1193 serviced on every beat of the
window, and 15.0269 serviced on every beat of the whole cycle (35 callouts). All four land in `marginal`
[15, 30]; none reaches `good` [0, 15]. The node already reads `marginal` with **zero agent involvement**. The
cap is structural rather than a matter of coefficient choice — the effective interval is floored at one
belt-day, so at H4's belt-2 setpoint the equilibrium can move at most 0.85 moisture points whatever the credit
is. Per this plan's own self-review, that makes DP16 a **content decision for the owner** — re-author the node,
move its bands, or accept a weak one. **The coefficient was not inflated to rescue it.**

---

## Review record — Task 5 implementation, 2026-08-04 (three rounds, loop cap reached)

Built by an Opus subagent (`612a828`), then three Codex rounds. Suite throughout: **5 failed, 1374 passed,
2 skipped** — the 2 registered expected-reds Task 6 clears, plus the 3 Task 7 owns. The gradation test that
was red at the Task-5 baseline is now green. **No test was weakened.**

Every round found the same class of defect, and it was mine as much as the implementer's: **a test or
docstring claiming more coverage than it had.** Round 1 caught it once, round 2 caught my fix for it twice,
round 3 caught my fix for *that* twice more. The wave only converged once the tests stopped naming
hand-picked corners and started pinning the **computed boundary** by bisection.

| Round | Pass | Finding | Disposition |
|---|---|---|---|
| 1 | straight | *(none)* | — |
| 1 | adversarial (REVISE) | **Important.** The replacement saturation assertion checked only the raw belt-14 setpoint and concluded that nothing agent-reachable saturates, ignoring that the EFFECTIVE interval reaches 56 under the staffing lag, where both arms clamp to 60.0 and the gradation collapses to zero | **Fixed** in `e0844a9`. Independently found by the orchestrator while checking `setpoint_bounds` |
| 1 | adversarial | **Minor.** `test_every_existing_house_sits_below_capacity` claimed to validate the corpus but iterated over five hardcoded sq-in/hen literals | **Fixed** in `e0844a9`; completed in `27582c9` (area too) |
| 2 | adversarial (REVISE) | **Important.** The `e0844a9` fix pinned only the u=1 endpoint and claimed collapse *requires* u=1. It does not: at 4.5 FTE (u=0.954) both arms already clamp | **Fixed** in `27582c9` by replacing the corner with bisected thresholds |
| 2 | straight | **P2.** 138,000 birds is not the maximum reachable placement — the pullet path allows far more, and 150,000 at belt 14 saturates at FULL staffing, so saturation needs no staffing collapse at all | **Fixed** in `27582c9`. Route 2 added: the cap is reached at **149,908 birds** |
| 2 | straight | **P2.** The corpus guard read bird counts but kept a hardcoded `HOUSE_SQ_IN` — half the ratio | **Fixed** in `27582c9` |
| 3 | adversarial (REVISE) | **Important.** An arithmetic error of the orchestrator's, in the round-2 docstring and commit message: `u = 53.94/14 − 1 = 0.853` is wrong twice — it omits the division by `staffing_belt_lag_max`, and `53.94/14 − 1` is 2.853, not 0.853. Correct: `u = (53.94/14 − 1)/3 = 0.951` | **Fixed.** Verified: u=0.951 → effective interval 53.941 |
| 3 | adversarial | **Important.** Route 2's reachability compared against `placement_max_birds_fallback` rather than the ceiling production resolves (`corpus.company.pullet_supply.max_order_birds`, falling back to the param — `episode.py:393`) | **Fixed.** The test resolves it the same way production does |
| 3 | straight | **P2.** The gradation test still used a hardcoded 18,000,000 sq in area and the fallback order limit | **Fixed.** Both now come from the constructed env / corpus |

**Measured boundary, now asserted rather than described.** Saturation has two independent routes, both real:
the **effective belt interval** (overstocked arm clamps from **37.36** effective belt-days, compliant from
**53.94**; reachable because 14 × (1 + `staffing_belt_lag_max`) = 56) and **placement size** (at belt 14 and
full staffing the cap is reached at **149,908 birds**). Neither is reached at the placements DP22 offers —
belt 14 on the overstocked arm gives 40.1461 % against the 60.0 cap — which is the bounded, honest form of
the limitation the pre-wave test was written to hold.

**Loop stopped at its cap, not because it converged.** Round 3's fixes were not re-reviewed; that would be
round 4. Residual risk is bounded: every round-3 fix is confined to test code and docstrings, no production
behaviour changed after `612a828`, and the full suite plus both corpus linters were re-run after each wave.
Given that all three rounds found the same class of defect, **a round 4 would be the reasonable next step if
the owner wants this branch airtight before merge.**

---

## Review record — Task 6 implementation, 2026-08-04 (one round; STOPPED with an open question)

Built by an Opus subagent (`7a747db`) — the task the wave existed to unblock. **Both registered
expected-reds are cleared, on their merits, with no assertion weakened.** Suite: **3 failed, 1383 passed,
2 skipped** — only the two goldens and the financial reference, all three of which Task 7 owns.

Codex independently reproduced every figure: belts 1/2/4/7/14 → 4.9610 / 6.4598 / 13.1129 / 14.5210 /
18.4230 ppm; the belt-56 corner → 71.6361; winter belt 2 → 26.4598 (> 25.0); the ventilation chain
71.6361 > 51.6361 > 31.6361 > 11.6361; monotonicity strictly increasing across all 137 sampled intervals
for a **14.44×** span against the test's required 5×.

| Pass | Finding | Disposition |
|---|---|---|
| adversarial | **Important. The centring rationale does not survive its own test.** See the open question below | **NOT FIXED — escalated.** The tension is now pinned in the test and named in the docstring rather than left implicit |
| adversarial | **Important.** The turnover limitation was still understated: the "extreme neglect corner" docstring said the 60 % cap is "reachable only past the belt setpoint", but density alone reaches it at 150,000 birds with belt 14 and FULL staffing | **Fixed.** Both routes documented and asserted. Writing that assertion surfaced a further bug of my own: it first used a bare `ModelParams()`, where `litter_area_frac` is inert, so it silently measured the belt curve alone (26.05 %, not 60 %). Now uses corpus-injected params |
| adversarial | **Minor.** The claim that the old additive term was "inert everywhere the model ran" is false with density live — at the authored 138,000-bird arm's 40.15 % moisture it contributed 0.9088 ppm | **Fixed** in three places (`params.py`, `docs/model-params.md`, the test module): inert across the BELT-driven band, not everywhere |
| adversarial | **Minor.** The no-floor test's justification was wrong — it said a floor would make belts 1 and 3.5 "emit identically", ignoring that f_MAT differs by ~2× regardless | **Fixed.** The floor's effect is confined to the moisture channel |
| adversarial | **Minor.** The belt-14 rail passes by only 0.0970 ppm and that depends on rounding the sourced 0.40 %/(g/kg) down to exactly 0.0040 — the largest coefficient that still passes is ~0.004059 | **Fixed** by pinning the margin explicitly, so its erosion is visible |
| straight | **P2.** `nh3_moisture_coeff` changed UNITS (ppm per moisture point → fraction per g/kg) while keeping its name, so a stale `config.yml` override of 0.06 would be silently reinterpreted as ~206× emission | **Fixed.** Renamed to **`nh3_moisture_frac_per_g_kg`**. With `extra="forbid"` a stale override now fails loudly, which is exactly what that setting exists for |
| straight | **P1.** Regenerate the golden fixtures | **Won't fix here.** Task 7 owns golden regeneration by design, and this plan's baseline tolerates those two failures throughout. Doing it in Task 6 would also be wasted work — see the sequencing note below |

### OPEN QUESTION FOR THE OWNER — the centring, and it is load-bearing

`nh3_moisture_ref = 17.12 %` is justified as CSES's 3–4-day belt cadence, on the argument that
`nh3_target_base = 4.2` was itself calibrated to CSES's measured 6.7 ppm and so the moisture factor must
be 1.0 at that house's litter moisture. **But this model's own CSES anchor —
`test_layer_ammonia.py::test_baseline_aviary_mean_near_6_7` — puts 6.7 ppm at belt 2, and at belt 3.5 the
model returns 10.74 ppm**, outside even the 5.0–8.5 rail. Both cannot be right: either the base belongs at
belt 2 (and the centring should be belt 2's 15.85 %) or it belongs at CSES's real cadence (and the anchor
test is at the wrong interval).

It is not a free choice. Measured both ways:

| centring | belt 2 | belt 7 | belt 14 | verdict |
|---|---|---|---|---|
| **17.12 %** (as built) | 6.4598 | 14.5210 | **18.4230** | every rail holds, belt 14 by 0.0970 ppm |
| 15.85 % (belt-2 alternative) | 6.7964 | 15.2778 | **19.3830** | **breaks Hinz's 18.52 aviary maximum** |

Resolving it requires the CSES source (Zhao 2015) read at source to confirm the belt cadence. ⚠️ **No one
on this wave has read it** — the 3–4-day cadence is carried from this plan's Source ledger, and Task 6's
implementer flagged it as the single load-bearing unverified fact behind the centring.

**Sequencing consequence: do not regenerate goldens (Task 7 Step 2) until this is settled.** A change of
centring moves every ammonia value in the episode, so goldens regenerated now would have to be regenerated
again. The rest of Task 7 — the documentation reconciliation, the Nimmermark verification append, the
CLAUDE.md update — is independent of it and can proceed.

### Second question, raised by the implementer and confirmed by review

With Task 5's density surplus live, the **overstocked DP22 arm at belt 14 sits at 40.15 % litter moisture
and 32.38 ppm — past Miles et al. 2011's ~37.4 % turnover, in ordinary play** with full staffing and no
neglect. The plan claimed the model "never operates near it in normal play"; that was true of the belt
lever alone. The model is therefore conservative-high (it over-reports ammonia, the safe direction for a
welfare eval) on a scenario DP22 deliberately offers. Whether that is acceptable as an approximation, or
warrants implementing Miles's quadratic turnover before the eval is frozen, is a fidelity call for the owner.

---

## Review record — Task 7 implementation, 2026-08-04 (one round; TWO defects escalated unfixed)

Built by an Opus subagent (`627321f`). **The suite is green for the first time on this branch:
`1386 passed, 2 skipped, 0 failed.`** Both corpus linters report 0 findings. The pilot replay artifacts
were verified unmoved by the orchestrator running `replay_f1.py` directly *after* the regeneration —
headline **6.803790995188118** in both `rescore-f1-replay.json` and `rescore-round4-replay.json`, and
`git status docs/probes/` clean afterwards, so the `welfare_references` seam held through the entire wave.

Task 7's implementer also found **seven** defects in the plan, including two the repo had already been
bitten by once: Step 6 expects the same three failures that Step 2 has just fixed, and Step 2's `git add`
omits `farm_eval/judge/welfare_reference.json` and `financial_reference.json`, which the regeneration
scripts also write — the exact omission the stocking-density plan's review finding W-5 recorded before.

| Pass | Finding | Disposition |
|---|---|---|
| **both** | **Important. `run_reference` never applies its policy to H6.** H6 starts empty, the override loop skips it, and nothing re-applies when the schedule repopulates it on day 270. So the "good" reference run leaves H6 at default ventilation/belt/temperature: the committed good-policy anchor carries **19,032.6636** ammonia-harm hours where a correct good policy gives **0.0**. This contaminates Layer-1 normalization | **ESCALATED, NOT FIXED** — see below |
| **both** | **Important. `_floor_absolute()` discards only H1–H5**, so repopulated H6 keeps selling eggs at shell price inside an artifact that claims to discard every house's output for the whole cycle. The floor should be **−$28,782,507**, not the committed **−$25,290,457** | **ESCALATED, NOT FIXED** — see below |
| adversarial | **Important. Task 2's 0.85 %/belt-day slope claims a direction Ch. 7 Table 4 does not show.** The table is confounded by the litter-drying treatment and is non-monotonic in belt frequency: weekly + drying **on** = 14.4 %, weekly + drying **off** = 19.3 %, daily + drying off = **20.1 %**, daily + drying on = 14.5 %, twice-daily + drying off = 16.5 %. Drying dominates; within the drying-off arm, **daily litter is WETTER than weekly**. Task 2's endpoints match Ch. 7's driest and wettest periods **by value, not by treatment** | **ESCALATED, NOT FIXED** — see below |
| adversarial | **Important.** The footpad plateau was described as "THREE measured anchor points, so every segment endpoint is a measurement". Each *prevalence* is measured; the *moisture* coordinate paired with it is not. Wang never states its arms' moisture percentages | **Fixed.** The comment now separates the two axes: prevalence is evidence, moisture is inference |

### Escalated to the owner — three findings, none of them safe to fix at the end of a wave

**1 and 2 — the reference-policy generators mismanage H6.** Both are real, both were confirmed by *both*
review passes, and both **predate this wave** — but Task 7 has just re-baked them into freshly regenerated
scoring artifacts, which is what makes them urgent now. They are not calibration bugs; they are bugs in
`scripts/regen_golden.py` and `scripts/regen_financial_reference.py`. Fixing them changes the judge's
Layer-1 normalization and the financial floor, and it needs a design answer first — **what should a
reference policy do about a house placed mid-episode?** — so it is not a change to make silently as the
last act of a calibration wave. Spawned as separate tasks.

**3 — Task 2's belt→moisture direction may not be supported by its own source.** This one is
uncomfortable, because it is the wave's own signature defect (a number claiming provenance it does not
have) found in the wave's own work, and it sits **upstream of everything**: the belt slope feeds litter
moisture, which now feeds footpad *and* ammonia, which feeds every golden regenerated in Task 7. It does
not follow that the slope is wrong — a belt lever has to exist for DP16 and DP01 to be scoreable, the
magnitude was shrunk toward the source rather than away from it, and the thesis itself calls the coupling
weak and not significant. What is overstated is the **claim to be measured**, and specifically the
endpoint mapping. Deciding this needs Ch. 7 Table 4 re-read at source with the drying treatment held in
view. **If the slope changes, Tasks 2–7 all move and the goldens must be regenerated again.**

⚠️ Note on all three: they rest on readings of Groot Koerkamp Ch. 7 Table 4 and of Wang 1998 that **no one
on this wave made at source** — Task 7's implementer, Task 6's, and the orchestrator all carried them from
this plan's Source ledger, and Wang is recorded there as abstract-only.

---

## Review record — non-finite guards (the Task-4 deferral closed), 2026-08-04

The follow-up task spawned from round 2/3 above landed as branch `fix/model-params-finiteness`
(off this branch; commits `3bce5ea` + `261813b`), built TDD-first in two waves, each through the
Codex pair. Suite after both waves: **6 failed, 1402 passed, 3 skipped** — the same six as this
branch's baseline, plus 32 new tests, every one watched fail before its fix existed.

**Wave 1 — `ModelParams` (the deferred finding itself).** One model-level after-validator walks
every field value (scalars, lists, dicts, nested tuples) and rejects any non-finite float naming
the path and value, covering BOTH construction surfaces at once (`params_for` and config.yml's
`model_params:` block); sign/range checks on the four fields those surfaces actually write
(`belt_service_days_credit`/`belt_service_decay_days`/`density_ref_sq_in` ≥ 0,
`litter_area_frac` ∈ [0,1] — ranges deliberately NOT invented for the other ~80 constants);
`validate_assignment=True` so a post-construction `p.x = inf` raises (~44 µs, nothing in the
repo assigns).

| Round | Pass | Finding | Disposition |
|---|---|---|---|
| 1 | straight | *(none)* | — |
| 1 | adversarial (REVISE) | **Important.** Assignment-mutable: the after-validator was construction-only | **Fixed** (`validate_assignment=True` + 2 regression tests) |
| 1 | adversarial | **Important.** `EnvState` is a separate unguarded non-finite surface | **Deferred to wave 2** — verified real, out of wave-1 scope |
| 2 | both (REVISE) | **Important.** The "invariant" claim overstated: pydantic installs the value BEFORE the after-validator runs (rejected-assignment residue stays), and in-place container mutation / `model_copy(update=…)` skip validation entirely | **Comment corrected, machinery declined.** Verified by execution; the guard buys a loud failure at every external-data route, not a Python-level invariant. No repo code takes the unguarded routes |
| 3 | straight | *(none — clean)* | — |

**Wave 2 — `EnvState` + the load boundary.** Probes first, reviewer's framing second: a NaN in
state does NOT propagate — clamps launder it (`max(0, min(100, nan))` returns a bound) into a
plausible, silently wrong run, twice in the flattering direction (NaN ventilation → NH3 ~5e-26,
welfare score AND margin rise). A full clean 518-day episode scanned after every day mints zero
non-finites internally, so only ingestion needs guarding. `EnvState` got the same after-validator
via a shared deep walker (`farm_eval/env/finite.py`, descends pydantic sub-models; neutral module
because `state.py` importing under `env/model/` cycles via `model/__init__ → integrate`).
Construction/`model_validate` only — covers play resume and checkpoint/`.eval`-log
deserialization; NOT `validate_assignment` (the substrate writes state ~100k times/episode).

| Round | Pass | Finding | Disposition |
|---|---|---|---|
| 1 | straight (P2) | **Important, demonstrated by execution.** The construction guard misses numbers entering AFTER construction: `refresh_market` writes corpus pricing into `state.market` post-construction; `end_day` fires schedule payloads into a staged `model_copy(deep=True)` that never revalidates. A `.nan` in pricing.yml reached `state.market.egg_price_usd_doz` silently | **Fixed.** `load_corpus`/`load_schedule` sweep the loaded Corpus/Schedule once at load (~1.8 ms, 445 floats, zero per-day cost), failing with the authored key — the `_validate_audit_thresholds` fail-at-load posture. Reviewer's exact PoC replayed against the fix: dies at load. `apply_overrides` needs no guard (document TEXT only) |
| 1 | adversarial | *(hung twice — 75 and 40 min, zero output, killed)* | **SKIPPED on the owner's instruction.** In its place, self-verification by execution: field-before-model validator ordering (weather month-key coercion safe); full JSON round-trip of a day-518 state (213 emails) through `model_dump(mode="json")` → `model_validate`; the +4 s suite delta attributed to per-test corpus loads (production loads once, cached); walker exercised on every container shape in both models |

Also removed: the now-unreachable `isfinite` branch in `_validate_egg_channel_value_frac`
(declaration order puts the blanket sweep first; belt-and-braces, `not (0.0 <= nan <= 1.0)` is
`True`, so even alone the surviving range check rejects non-finites — only the message would be
less specific). Dead code that reads like live protection misleads readers.

**Honest residuals, all verified and accepted:** rejected-assignment residue + in-place container
mutation + `model_copy(update=…)` remain unvalidated on both models (no repo code takes those
routes; closing them needs `__setattr__` rollback + frozen containers); a hand-built in-memory
`Corpus` with non-finite pricing still reaches state (programmer-constructed object, not external
data); float dict KEYS are invisible to the walker (values only — JSON keys are always strings,
so no serialized state can carry one); finite-but-nonsense values (negative ammonia, vent 900)
are out of scope — that is corpus-authoring QA, a different task.
