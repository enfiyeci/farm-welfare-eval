# Stocking-density archive claims — the 2026-08-03 session's research record

Eval: hen

Claimed 2026-08-07 by the litter lane (P8) from
`origin/archive/stocking-density-task6-local-2026-08-06`, exactly per the claim list in
[`../2026-08-07-litter-prep/03-stocking-density-branch-claims.md`](../2026-08-07-litter-prep/03-stocking-density-branch-claims.md)
§D. These files predate the repo reorganization; they were checked out file-by-file (never
branch-merged) and moved into the post-reorg layout in one commit. The archive branch itself stays
as a ref on origin — archive means keep-the-ref, never delete.

## Files, in reading order

| File | What it is | Read status at claim time |
|---|---|---|
| [`2026-08-03-nh3-moisture-decomposition.md`](2026-08-03-nh3-moisture-decomposition.md) | **The load-bearing one.** The three calibration defects under any litter lever: the belt→moisture curve overshoots the measured 14.4–20.1 % belt-regime band; the 9.2–47.4 ppm "aviary" ammonia rail is Hinz 2010's floor-housing row (real aviary row: median 11.4, max 18.5 ppm at weekly belts); the 21.4 → 23.0 hens/m² density-reference provenance error. Plus better anchors (GK Ch. 5 survey, eq. 18) and the Kang demotion. | Read in full by the litter-prep session (474 lines); its own findings verified at source per its source-access table. |
| [`2026-07-30-density-coefficients.md`](2026-07-30-density-coefficients.md) | The density coefficients research behind the stocking-density wave. | ⚠️ Catalogued by provenance only — not read by the claiming session. |
| [`2026-07-31-density-decision-research.md`](2026-07-31-density-decision-research.md) | The density decision-node research. | ⚠️ Catalogued by provenance only — not read by the claiming session. |

Claimed in the same commit, homed elsewhere by convention:

- The four source PDFs + the Hinz text layer → `evals/hen/research/sources/` (Miles 2011 — closing
  a fetch-list item; Hinz 2010 full volume + extracted text pp. 139–150; Kang 2018; Mendes 2010).
- The blocked-Task-6 handoff → `docs/handoffs/2026-08-03-task6-blocked-three-calibration-defects.md`
  (the four pending owner decisions and the sequencing logic).
- The stocking-density plan (Task 6 BLOCKED status) → `evals/hen/archive/plans/2026-07-29-stocking-density-plan.md`.

## Corrections that supersede parts of these documents — do not carry forward

1. **The decomposition doc's §8 day-2 caveat ("day 2's surface has no maximum") is WRONG.** The
   printed positive β_MQ in Miles Table 4 is the article's own typo; the sign is negative, settled
   by arithmetic against the paper's Table 5
   ([`../2026-08-07-litter-prep/02-source-traces.md`](../2026-08-07-litter-prep/02-source-traces.md) §2).
   The doc's derived turnover (~37–43 % at our house temperatures) is unaffected and confirmed.
2. **`pdftotext` silently drops minus signs from tables in these PDFs** (Miles Table 4 day-2 β_MQ;
   De Jong Table 1 slopes). If a reviewer claims a sign error, check the rendered page before
   believing either side.
3. An earlier revision of the claim doc carried an unmeasured "~95 commits"; the measured number is
   64 (`git rev-list --count origin/main..<archive-branch>`, checked 2026-08-07).

What was deliberately NOT claimed: the DP22/DP23 signature work, the grader-facts/deadline-snapshot
judge work, and the Task 3/5 model code — superseded by, in conflict with, or pending the same owner
decisions that blocked Task 6. The litter lane re-derives what it needs from this research record.
