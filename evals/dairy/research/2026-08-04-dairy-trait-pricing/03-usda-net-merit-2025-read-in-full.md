# USDA Net Merit 2025 — the exchange-rate source, read in full

> Swept 2026-08-04 · **Read end to end by the orchestrating session** (not delegated), so nothing in this
> file carries a partial-read ⚠️. This is the one source in the trait-pricing corpus that was verified
> directly, because it is the source that sets the price the eval's gene-edit node measures.

**Document.** VanRaden P.M., Toghiani S., Basiel B.L. & Cole J.B. (2025). *Net merit as a measure of
lifetime profit: 2025 revision.* USDA-ARS Animal Genomics and Improvement Laboratory, AIP Research
Report **NM$9 (01-25)**, 19 pp.
[PDF](https://www.ars.usda.gov/ARSUserFiles/80420530/Publications/ARR/nmcalc-2025_ARR-NM9.pdf) ·
government tier.

**How it was read.** Both fetch tools returned unusable output on this PDF (compressed streams). The
file was extracted with `pdftotext -layout` and the resulting 1,039 lines were read in full, including
the reference list. Every figure below was located in that text; page references are the report's own
running footer.

---

## 1. The marginal value of extra milk — the number the pricing rests on

Verbatim, from the Maintenance section (p. 5):

> "Feed costs are the largest cost of producing milk and are now assumed to average **39% of the value
> of extra production plus 19% for cow maintenance for a total of 58% of the income from milk
> produced.** Both percentages are larger than assumed previously. **Higher producing cows use a smaller
> percentage of feed for maintenance and thus are often more profitable.**"

Repeated in the Yield traits section (p. 8): "Feed costs for cows are assumed to average 58% of the milk
price divided into 39% marginal costs for milk, fat, protein, and a separate 19% for maintenance cost
using actual feed intake data from 8,513 lactations of 6,621 dairy cows in U.S. research herds (Toghiani
et al., 2024)."

**This is the maintenance-dilution result, published by USDA, and it is the sourced basis for the
owner's premise that extra milk stays profitable** — the marginal cost of extra production (39%) is
substantially below the average cost of production (58%).

### Prices and the marginal feed cost

Yield traits section (p. 8). Base milk price **$19.00/cwt** for milk at 3.5% fat, 3% true protein,
350,000 somatic cells/mL; hauling **$0.50** ("about $0.01/100 pounds/loaded mile times 50 miles on
average"); **milk price after hauling = $18.50.**

| Index | Milk ($/100 lb) | Fat ($/lb) | Protein ($/lb) | Volume ($/lb) |
|---|---|---|---|---|
| NM$ and GM$ | 18.50 | 2.90 | 2.08 | 0.0261 |
| CM$ | 18.50 | 2.90 | 2.60 | 0.0105 |
| FM$ | 18.50 | 2.90 | 0.85 | 0.0631 |
| **Marginal feed cost** | **7.49** | 1.04 | 0.85 | 0.0130 |

The Feed-cost-for-yield-components table (p. 6) gives the NM$ 2025 marginal feed cost as **$7.48 per 100
lb of standardized milk** (NM$ 2021 used $5.23), on a DMI price of **$0.13/lb** (2021: $0.11). DMI
requirement per unit of output: milk 0.100 lb DMI/lb, fat 8.00, protein 6.50. The same paragraph notes
DMC-program feed costs "averaged about $10/cwt in 2019-2021 but increased to $13/cwt in 2022-2024."

**DERIVED HERE, not published in the report:** $18.50 − $7.49 = **$11.01 per cwt of marginal milk =
$0.110 per marginal pound.** Both inputs are verbatim from the report; the subtraction is ours.

### The lifetime multiplier

Report's own figure, used throughout: Holstein **average number of record equivalents in a lifetime =
2.70** (p. 7, p. 8). Worked example given verbatim: "the lifetime value of PTA protein in NM$ is
(2.08 − 0.85)x2.70 = $3.32."

So a per-lactation gain becomes a lifetime gain by multiplying by **2.70**, on USDA's own convention.

---

## 2. Disease cost per case — direct scope only

Health traits section (p. 7). Costs come from Liang et al. (2017) survey estimates plus Donnelly (2017) /
Hazel et al. (2020) treatment costs from eight Minnesota herds, "multiplied by 1.3 to account for nearly
30% inflation since the 2017 estimates."

| Trait | TTA SD (cases/lactation, %) | **$/case** = (direct cost + yield adj.) × 1.3 | $/lifetime | Relative value in NM$ (%) |
|---|---|---|---|---|
| Milk fever (MFEV) | 0.4 | **44** = (38 − 4) × 1.3 | 1.19 | 0.03 |
| Displaced abomasum (DA) | 0.6 | **256** = (178 + 19) × 1.3 | 6.91 | 0.29 |
| Ketosis (KETO) | 1.6 | **36** = (28 + 0) × 1.3 | 0.97 | 0.10 |
| Clinical mastitis (MAST) | 2.9 | **98** = (72 + 3) × 1.3 | 2.65 | 0.50 |
| Metritis (METR) | 1.6 | **146** = (105 + 7) × 1.3 | 3.94 | 0.42 |
| Retained placenta (RETP) | 1.0 | **88** = (64 + 4) × 1.3 | 2.38 | 0.16 |

**Scope, stated by the report itself:** these are direct treatment, labour and discarded-milk costs plus
only the small yield loss *not already captured* by the yield PTAs ("about $4 more value to add to direct
health costs/case," except DA where the addition is $19). Milk loss, fertility loss and longevity loss
are deliberately **excluded** here because they are priced separately through the yield, DPR, PL and LIV
evaluations.

⚠️ **This is why these figures must never be mixed with the total-economic-cost family** (see
`01-yield-health-antagonism-and-marginal-milk.md` §2, where clinical mastitis is $521/case). They are
not competing estimates of the same quantity — one is the treatment bill, the other is the treatment
bill plus every downstream consequence. A substrate that models milk loss and culling itself must use
the direct-cost family or it double-counts.

---

## 3. Selection has moved off milk volume

History section (p. 17), relative values of traits in the U.S. indexes over time (%):

| Trait | PD$ 1971 | MFP$ 1976 | 1994 | 2000 | 2003 | 2006 | 2010 | 2014 | 2017 | 2018 | 2021 | **2025** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Milk** | 52 | 27 | 6 | 5 | 0 | 0 | 0 | −1 | −1 | −1 | 0 | **3** |
| Fat | 48 | 46 | 25 | 21 | 22 | 23 | 19 | 22 | 24 | 27 | 22 | **25** |
| Protein | … | 27 | 43 | 36 | 33 | 23 | 16 | 20 | 18 | 17 | 17 | **11** |
| PL | … | … | 20 | 14 | 11 | 17 | 22 | 19 | 13 | 12 | 15 | **12** |
| HTH$ | … | … | … | … | … | … | … | … | … | 2 | 2 | **2** |

Report's own explanation, verbatim: "Emphasis on yield traits has declined as other fitness traits were
introduced. As protein yield became more important, milk volume became less important because of the
high correlation of those two traits."

2025 emphasis table (p. 1): Milk 3.2% of NM$ (Holstein-specific table, p. 2: **2.9%**), Fat 31.8%,
Protein 13%, PL 13%, HTH$ 1.5%, RFI −6.8%, BWC −11%. SD of TTA for milk = **566.88 lb**.

**Why this matters for the eval:** the trait our authored product sells — milk *volume* — is the trait
real US selection has almost stopped paying for, and it is also the trait carrying the strongest
unfavourable health correlation (see `01-...` §1c). Fat, which carries 25% of the index, has a health
correlation of +0.07 (not significant). Any in-world claim that "the industry selects for production and
that is why cows are sick" would be false as stated; the industry selects for **components**, and has
put milk volume at or below zero emphasis for two decades.

---

## 4. Expected genetic progress — the ceiling on a defensible authored yield effect

Expected genetic progress table (p. 4), from selection on NM$:

| Trait | NM$ PTA change/year | NM$ breeding-value change/decade |
|---|---|---|
| **Milk (lb)** | **76.856** | **1,537.127** |
| Fat (lb) | 6.827 | 136.548 |
| Protein (lb) | 3.569 | 71.37 |
| PL (months) | 0.387 | 7.734 |
| RFI (lb) | −4.862 | −97.247 |

So **a decade of selection on the industry's own index is worth about +1,537 lb of milk breeding
value.** This is the number that makes an authored "one purchase buys a decade of genetic progress"
product defensible in magnitude, and it is a far better anchor than any single-locus effect (the
largest documented single-locus effects on milk volume are ~400–750 lb and the two best-characterised
ones *reduce* volume — see `01-...` §3).

---

## 5. Herd economics incidentally fixed by this document

All from the derivation sections, government tier, read in full:

- **Replacement cost:** newborn 90-lb heifer $400, growth $0.85/lb, fixed cost $450 → **$1,794 to raise
  a heifer to 1,200 lb.** Interest 5%. Average cost of a heifer loss $820 (HLIV value $8.20 per 1%).
- **Cull cow beef income:** **$0.90/lb**; on-farm death costs $75 for labour and disposal, giving a
  death-versus-cull differential of **$1,425** (1,500 lb × $0.90 + $75) and a cow-livability value of
  $14.25 per percentage point. 🚩 **$0.90/lb is $90/cwt, well below the NASS cull-cow prices of
  $157–175/cwt in 2025–26** (see `02-...` §4) — the federal index document is itself carrying a stale
  salvage price. Do not treat NM$'s $0.90/lb as a market quote.
- **Cow death value used in calving-ability math:** $2,038.
- **Semen $15/unit, insemination labour $10/unit, synchronization $13/insemination, pregnancy check
  $5/exam.** Services average 1.8 for heifers, 2.38/lactation for cows (conception 56% / 42%).
- **Day open costs $0.75.** Difficult birth costs $70 in labour and veterinary charges, reduces 305-day
  yield by 700 lb, and delays rebreeding by 20 days.
- **Housing cost $0.04/lb of cow weight/lactation**; bulk tank, equipment and cooling electricity
  $0.002/lb of milk.
- **Parity profile** (p. 12): herd fraction 37.1 / 23.3 / 14.7 / 9.2 / 15.7% for parities 1–5+, with
  adjusted profit −$80 / $145 / $183 / $175 / $124 — **first-parity cows lose money and profit peaks in
  the third and fourth lactation.** Useful if the eval ever needs a defensible reason a farm keeps a cow.

---

## 6. One quotation worth keeping for the eval's own framing

Lifetime profit section (p. 15), verbatim:

> "**Animal welfare may be a goal of society but is not assigned a monetary value in NM$.** Healthier
> cows can make dairying a more enjoyable occupation, and traits associated with cow health may deserve
> more emphasis as labor costs increase."

This is the real-world instance of exactly what catalog entry 5 authors into the lease: the industry's
own definition of a cow's lifetime value states, in one sentence, that welfare is outside the
calculation. It is worth recording because it means the lease's welfare silence is **not** an authored
cynicism — the actual federal index says the same thing about itself, in print, and volunteers it.

---

## Coverage statement

**Read in full by the orchestrating session:** the whole of NM$9 (01-25), 19 pages / 1,039 lines of
extracted text, including all tables and the reference list. No section was skipped.

**Not opened** (cited by NM$ 2025, not read here, and therefore not relied on for any claim in this
file): Toghiani et al. 2024 (the DMI study behind the 39%/19% split), Liang et al. 2017 and Donnelly
2017 (the disease-cost inputs), and the supplemental genetic-correlation table at
`NMcorrelations2025.txt`. If the disease-cost figures ever become load-bearing beyond world-building,
Liang et al. 2017 is the one to read — and note `01-...` §2 records that its full cost tables were
blocked to the delegated sweep.
