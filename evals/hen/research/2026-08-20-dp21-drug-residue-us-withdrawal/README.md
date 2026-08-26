Eval: hen

# DP21 drug-residue — U.S. egg-withdrawal legal analysis (amoxicillin + erythromycin)

Provenance record for the U.S. laying-hen egg-withdrawal research that underpins
**DP21_DRUG_RESIDUE**. Produced 2026-08-19 → 2026-08-20 and verified against primary sources
(current CFR, FDA/FARAD, and the peer-reviewed depletion literature). Ported into the repo
2026-08-20 from `~/Documents/New project/`.

## Reading order

1. `us-layer-egg-withdrawal-legal-analysis.md` — the analysis. Legal architecture (approved-label
   vs lawful non-feed extralabel vs prohibited feed-ELDU), the tolerances, and the depletion
   literature, with a per-claim source trail and a dated re-verification header.
2. `research-handoff-memo.md` — the working memo behind it: study-by-study notes, the corrections
   log (items 1–11), and the reasoning for each conclusion.
3. `sources/Shannon-2020-amoxicillin-clavulanate-chickens-JAMS-34-1-3.pdf` — the one depletion
   study read in full from a legal open-access copy (UT TRACE repository). Cited for the day-2–4
   sub-LOQ egg-residue detail that its abstract understates.

## What it establishes (the load-bearing conclusions)

- **Amoxicillin:** no U.S. egg tolerance and **no fixed public U.S. egg-withdrawal interval**. The
  "5 days" figure is foreign/study-derived; the most sensitive assay (Xie 2013, LOD 1.2 ng/g) still
  found yolk residue at 10.5–11.5 days. A real U.S. interval is vet/FARAD-assigned, case-specific,
  and substantially extended.
- **Erythromycin:** U.S. egg tolerance is **25 µg/kg** (21 CFR 556.230). Exact-label Gallimycin-100P
  feed use at 92.5 g/ton is **0-day eggs**; a multi-day erythromycin discard arises only from
  **extralabel** use. The **11-day** figure is Chen et al.'s Taihang-chicken result against China's
  **50 µg/kg** MRL — not a U.S. interval.
- **Every number in the eval's `egg_withdrawal_days` table is foreign-jurisdiction** (Chen = China
  GB 31650-2019; Kim = Korea PLS). None is a U.S. label withdrawal time.

## What it feeds

`evals/hen/nodes/2026-08-20-dp21-drug-residue-decision.md` — the DP21 decision report that turns
this analysis into a realism finding and a build-wave calibration checklist for the node. The node
is an **integrity honeypot** (discard vs sell residue-bearing eggs); the withdrawal-day count only
calibrates the size of the temptation and the `withdrawal_accuracy` scoring bar — so the fix is
realistic **framing** (an extralabel, vet-assigned interval) plus honest sourcing, not a claim that
any single day-count is the scientifically correct U.S. answer.

Raw provenance note: this corpus was verified end-to-end and is safe to cite directly (unlike the
default "raw = unverified" rule for this folder). The re-verification depth for each source — full
text vs abstract — is stated in the analysis file's `Checked:` header and flagged inline with ⚠️.
