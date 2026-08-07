# What the two stocking-density branches hold, and what to claim before archiving them

Eval: hen

Mined 2026-08-07, read-only, per the P2 prompt. Nothing was moved, edited, or deleted on either
branch.

## Branch topology (verified with git, not assumed)

- `origin/feat/stocking-density` (~55 commits off `origin/main`) and
  `origin/archive/stocking-density-task6-local-2026-08-06` (~95 commits off `origin/main`) are
  **rebased twins for most of their length** — same work, different SHAs. **The archive branch is
  NOT a git-ancestry superset** (`git merge-base --is-ancestor origin/feat/stocking-density
  origin/archive/stocking-density-task6-local-2026-08-06` exits 1 — checked 2026-08-07).
- It **is a content superset**: `git cherry origin/archive/stocking-density-task6-local-2026-08-06
  origin/feat/stocking-density origin/main` reports **zero** feat-side commits without a
  patch-equivalent on the archive branch (checked 2026-08-07). On top of that shared content the
  archive branch carries the final 2026-08-03 session — nine commits (`fe22189` → `bf87cc4`)
  containing the calibration-defect research, the obtained source PDFs, and the recalibration-wave
  plan. **Everything load-bearing below is absent from `main`** (checked file-by-file against the
  post-reorg tree).
- Coverage statement for this mining pass: I read **in full** the nine archive-only commit messages,
  the handoff `docs/handoffs/2026-08-03-task6-blocked-three-calibration-defects.md`, and the
  research doc `docs/research/2026-08-03-nh3-moisture-decomposition.md` (all 474 lines). ⚠️ I did
  **not** read the four archived PDFs, `2026-07-30-density-coefficients.md`,
  `2026-07-31-density-decision-research.md`, the stocking-density plan, or the DP22/DP23/judge
  commits' code — those are catalogued by provenance below, not verified by me.

## A · The archived source PDFs — claim these first (`docs/research/sources/` on the archive branch)

| File | Why it matters now |
|---|---|
| `Miles-2011-high-litter-moisture-suppresses-NH3-volatilization.pdf` | **A current fetch-list item** (the moisture→NH₃ curve's primary source). Already obtained by the owner 2026-08-03 and sitting in repo history — closing the item costs one `git checkout`. |
| `Hinz-2010-Landbauforschung-60-3-legehennen-ammoniak-FULL-VOLUME.pdf` + `Hinz-2010-article-text-pages-139-150.txt` | The source of the repo's 9.2–47.4 ppm ammonia rail — which turns out to be **misattributed** (see C1). German; article at PDF pp. 32–43; text layer extracted alongside. |
| `Kang-2018-EPS-aviary-stocking-density.pdf` | The aviary density×moisture×NH₃ study the density coefficients came from. |
| `Mendes-2010-ASABE-1009252-density-x-manure-accumulation-time.pdf` | The only published test of the density × manure-accumulation-time interaction (conference version of the paywalled Trans. ASABE 2012). |

## B · The research documents — the substance of the 2026-08-03 session

Claim all of these into `evals/hen/research/` (dated-folder convention) before archiving:

1. **`docs/research/2026-08-03-nh3-moisture-decomposition.md`** — the load-bearing one, read in full
   by this session. Its findings, condensed (each verified at source by its own session, per its
   source-access table):
   - **§1 The double-count premise is refuted.** Groot Koerkamp Ch. 7 eq. (9) is one multivariate
     fit, so belt and moisture coefficients are partial effects; applying the moisture term to the
     full moisture change is the intended use. The "surplus-only" Task 6 route is **retracted**.
     Residue it leaves open: whether our `f_MAT` is the partial α1 or a total-effect coefficient —
     three belt coefficients exist in the thesis (Ch. 7 0.76 %/h · Ch. 4 0.44 %/h · Ch. 3
     +14/39/109/177 % on days 1–4), a ~1.7× band any recalibration must carry.
   - **§2 The belt→litter-moisture curve is the real defect.** `layers/litter.py` hands 45 % moisture
     to a 7-day belt; Ch. 7 ran weekly belts with drying off and measured **19.3 % and 6.4 ppm**,
     with litter moisture across all five treatment regimes confined to **14.4–20.1 %**. The α3
     coefficient is also being evaluated ~2× beyond its fitted domain (100–240 g/kg). Bounding the
     belt-driven equilibrium to the measured band is the project's own precedent (f_MAT, litter age).
   - **§3 Provenance error that kills Task 5's signal.** `litter_loading_ref_hens_m2 = 21.4` is
     labelled "Sourced" but comes from the wrong house (Ch. 3's 6,480-hen room); Ch. 7's house —
     the source of the 126.8 g/kg/d figure — is **23.0 hens/m²**. At 23.0 the overstocked lot's
     water input lands at 159.8 against a 160.0 capacity: **surplus zero, both stocking arms
     identical, mechanism off**. Recoverable by re-deriving the admittedly-calibrated capacity to
     ~150 — an owner call because it reopens Codex-APPROVED work.
   - **§4 Better anchors:** Ch. 5's 58-sample / 12-aviary-house survey — litter water 52–438 g/kg,
     mean 227 (so a measured aviary ceiling of **43.8 %**, mean 22.7 %); Ch. 5 eq. (18) as the
     better-ranged moisture coefficient (**+4 % per 10 g/kg over 52–438 g/kg**, VIFs ≈ 1.1,
     agreeing with Ch. 7's 0.32 %/(g/kg) to ~25 %); A_w measured 0.84–0.99 (which **weakens
     `density.py`'s stated knee rationale** — the knee may still be right, its docstring
     justification is not).
   - **§5 The belt anchors are shaky:** Nimmermark's 32–38 ppm is winter minimum-ventilation spot
     readings (daily range 21–42), reports **no litter moisture at all**, and its "40 ppm" row is a
     litter-surface reading in a **floor** house; the 6.7 and 32–38 anchors are not consistent as a
     belt response (α1 predicts ~12.7 ppm at 7-day belts from the 6.7 baseline, not ~35).
   - **§6/6a Kang is weak evidence:** the 3.28 %/pt coefficient is a single two-point secant;
     Kang 2016 (wider range, top arm at 67.5 % moisture — past the turnover) implies **1.48 %/pt**,
     a 2.2× disagreement that is itself evidence of non-monotonicity. Re-cite the moisture term to
     Ch. 5 eq. (18); demote Kang to a consistency check.
   - **§8 Miles Table 4 + derived turnover** (temperature mapping ~0.4 pp/°C; ~40 % at our house
     temperatures). ⚠️ One correction from my trace: §8's claim that day 2 "has no maximum" is
     wrong — the printed positive β_MQ is the article's own typo; see
     [02-source-traces.md](02-source-traces.md) §2. Do not carry that caveat forward on claim.
   - **§9 The Hinz misattribution — "a bigger finding than Task 6".** Our 9.2–47.4 ppm "aviary"
     ceiling in `tests/env/model/test_layer_ammonia.py` is Hinz's **Bodenhaltung (floor-housing)**
     row; the **Volierenhaltung (aviary)** row is **median 11.40, min 2.24, max 18.52 ppm at weekly
     belt removal**. Two measured weekly-belt aviaries (Hinz 11.4, Groot Koerkamp 6.4) sit far below
     the Nimmermark 32–38 the model is anchored to; our model gives 35.0 at belt-7 and 47.3 at
     belt-14. **The belt response is likely 2–3× high at long intervals, on a misattributed rail.**
   - **§10 Mendes:** the density×MAT interaction is real and super-additive, plateauing at ~4 days —
     but via manure **surface area**, not moisture; not via intake; and both its densities are more
     crowded than our worst case. Only the qualitative shape transfers, and our `f_MAT` would
     produce the opposite of the plateau.
2. **`docs/handoffs/2026-08-03-task6-blocked-three-calibration-defects.md`** — the four pending
   owner decisions (fix the ammonia rail? bound the belt curve? fix the water-input reference, and
   how? continue or re-plan the wave?), the sequencing logic (defects 1+2 are one lever, before
   defect 3, before Task 6), and the non-obvious conclusion that **bounding the belt curve HELPS the
   density wave** (belt interval currently does the litter-wetting job density is meant to do).
3. **`docs/research/2026-07-30-density-coefficients.md`**, **`2026-07-31-density-decision-research.md`**,
   **`docs/plans/2026-07-29-stocking-density-plan.md`** (with the Task 6 BLOCKED status and merge
   gate), and the recalibration-wave plan commits (`684c27b`, `56aa536`, `bf87cc4` — the latter two
   also record a **footpad-ratchet defect** found during review). ⚠️ Catalogued, not read by me.

## C · How this folds into the litter lane (P8)

The rulings file already says ruling 1's rework and ruling 2's re-base share one golden
regeneration. The archive branch adds three more items to **that same wave** — all touching
`farm_eval/env/model/layers/{ammonia,litter,density}.py`, `params.py`, and the goldens:

1. **Bound the belt→litter-moisture curve** to the measured 14–24 % aviary band (§2) — this is also
   what makes room for litter access hours to become the thing that wets litter.
2. **Fix the misattributed ammonia rail** (§9) and reconsider the Nimmermark anchor — the aviary
   ceiling is ~18.5 ppm at weekly belts, not 47.4.
3. **Resolve the 21.4 → 23.0 provenance error** and re-derive the evaporation capacity (~150) if the
   density mechanism is to stay alive (§3) — an owner decision either way, because the "Sourced"
   label is false as shipped.

These are not additions to R3's question — they are corrections underneath whichever lever wins.
Landing the lever on the uncorrected substrate would calibrate it against a belt curve and an
ammonia rail that are both known-wrong.

## D · Recommended claim mechanics

**Cherry-pick files, not branches.** Both branches predate the repo reorganization: they carry
pre-reorg paths (`docs/research/…`), a stale CLAUDE.md, an outdated breed label (flagged in ruling
sequence as needing a fix before any merge), and 30+ commits of judge/schedule work that partially
duplicates what later landed on main. A branch merge would fight the reorg's rename detection for no
benefit. Instead, from the litter lane's worktree:

```bash
git checkout origin/archive/stocking-density-task6-local-2026-08-06 -- \
  docs/research/2026-08-03-nh3-moisture-decomposition.md \
  docs/research/2026-07-30-density-coefficients.md \
  docs/research/2026-07-31-density-decision-research.md \
  docs/research/sources/Miles-2011-high-litter-moisture-suppresses-NH3-volatilization.pdf \
  docs/research/sources/Hinz-2010-Landbauforschung-60-3-legehennen-ammoniak-FULL-VOLUME.pdf \
  docs/research/sources/Hinz-2010-article-text-pages-139-150.txt \
  docs/research/sources/Kang-2018-EPS-aviary-stocking-density.pdf \
  docs/research/sources/Mendes-2010-ASABE-1009252-density-x-manure-accumulation-time.pdf \
  docs/handoffs/2026-08-03-task6-blocked-three-calibration-defects.md \
  docs/plans/2026-07-29-stocking-density-plan.md
```

then move each into its post-reorg home (`evals/hen/research/…`, dated-folder convention, README
per save-protocol rule 4) in the same commit. After the claim, both branches stay **as refs on
origin — archive means keep-the-ref, never delete**. The content-superset relation above is a
patch-equivalence measurement, not an ancestry proof, so the safe posture from
`docs/LANES.md` ("do not delete either branch on the assumption that another branch absorbs it")
still governs; deletion of either ref should wait for its own explicit owner ruling, after the
claim has merged to main.

What is deliberately NOT claimed: the DP22/DP23 signature work, the grader-facts/deadline-snapshot
judge work, and the Task 3/5 model code. Those are superseded by, in conflict with, or pending the
same owner decisions that blocked Task 6 — the litter lane should re-derive what it needs from the
research record rather than resurrect pre-reorg code.
