# Labour time study and BLS data, read in full — 13–14 FTE holds, but only under one assumption

> Owner obtained these on 2026-08-06. This closes the empirical half of decision 04 and resolves the
> time-base ambiguity that was the biggest open number in the earlier staffing research.

## 1. The time base is resolved

The paper is **Anderson 2014, *J. Appl. Poult. Res.* 23:108–115** (NC State, Piedmont Research
Station, Salisbury NC). Read in full, 8 pp.

Its h/hen figures are **totals for one entire laying cycle of about 64–68 weeks** — not daily, not
weekly, not annual. Table 2's caption says "total man-hours per hen", and the text: *"Over the entire
production cycle, a significant... increase of 0.334, 0.486, and 1.268 h/hen was observed."* That
settles the unit question the earlier WATTAgNet-derived figure left hanging.

**Measured labour** (Table 2, p. 113; P<0.0001):

| System | h/hen housed, whole cycle | h/hen surviving |
|---|---|---|
| Cage | 0.334 | 0.351 |
| **Cage-free** | **0.486** | 0.520 |
| Range | 1.268 | 1.512 |

Cage → cage-free is **+45%**; cage → range **+279%**.

**What was counted** (p. 109, 111): not bird care alone, despite the title. Total direct labour —
feeding and feed weigh-backs, egg collection, daily mortality and production recording, egg-quality
data, manure removal, general maintenance, and paddock rotation for range. Caretakers signed in and
out per pen to the nearest minute.

## 2. The FTE answer, and the assumption it rests on

Extrapolating the measured cage-free figure directly:

```
0.486 h/hen per cycle ÷ ~1.23–1.30 yr   ≈ 0.37–0.40 h/hen/year
× 750,000 hens                          ≈ 279,000–296,000 h/year
÷ 2,080 h per FTE-year                  ≈ 134–142 FTE   (~180 FTE per million hens)
```

That is roughly **10× our 13–14 FTE**. But the paper explains why it would be: these are small
experimental replicates — 216 birds per pen, 24 separate pens, caretakers walking pen to pen. That is
a research-labour structure, not one automated commercial building.

Anderson quotes a figure for the automated case (p. 113): *"the labor input on a per-hen basis
continued to decline to about 0.03 h/hen in a 1 million hen complex."* Applying his own cage-free
multiplier to it: 0.03 × 1.45 ≈ 0.0435 h/hen/cycle → ~0.033 h/hen/year → ×750,000 ≈ 25,100 h/year →
**≈ 12 FTE**.

**So 13–14 FTE is defensible — and only — if the complex is assumed highly mechanised**: belt egg
collection, automated feed and ventilation, mechanised manure handling. Under the manual small-plot
regime this paper actually measured, it would need about ten times the staff.

⚠️ **The reconciliation rests on a number nobody has verified.** The 0.03 h/hen figure is a
one-sentence secondary citation inside Anderson's paper, to Bell & Weaver, *Commercial Chickens Meat
and Egg Production*, 5th ed. (2002) — and **Anderson does not state whether it is a whole-cycle total
or an annual rate**. So the same unit ambiguity that this paper resolved for its own figures is simply
pushed back one level into the source it quotes. If it is annual rather than per-cycle, the
reconciliation moves by a factor of ~1.3.

**Note also that this reframes the scoping question.** The earlier research asked whether 13–14 FTE
means barn labour or the whole payroll. Anderson's measurement counted egg collection, manure removal
and maintenance as well as bird care — so the real variable is not *which tasks* but *how automated
the farm is*.

## 3. BLS injury rates, confirmed at source — and NAICS 1123 exists

Rates per 100 full-time workers, 2024 (Table 1, p. 1):

| Industry | NAICS | Total recordable | Days away from work |
|---|---|---|---|
| Private industry, all | — | 2.3 | 0.8 |
| Agriculture, forestry, fishing, hunting | 11 | 3.9 | 1.4 |
| Animal production and aquaculture | 112 | 4.0 | 1.7 |
| **Poultry and egg production** | **1123** | **4.4** | **1.6** |
| Cattle ranching | 1121 | 3.7 | 1.8 |
| Hog and pig farming | 1122 | 4.2 | 1.4 |

Independently confirmed against the BLS NAICS 112 industry page, which reports the same 2024 figures.

**Poultry and egg workers are recorded injured or ill at roughly 1.9× the private-sector rate**, and
miss work for it at twice the rate. This is a real, citable worker-welfare anchor and it is
poultry-specific — better than the California state figure the earlier pass had to fall back on.

Adjacent context, not requested: 105 deaths in animal production in 2023, 124 in 2024, with a BLS
series break from the 2022 NAICS revision. ⚠️ Counts, not rates.

## 4. BLS wages, confirmed

SOC 45-2093, Farmworkers, Farm, Ranch and Aquacultural Animals. ⚠️ **May 2023 vintage**, not 2024 —
the file's own header and its April 2024 modification date both say so.

| Metric | Value |
|---|---|
| National employment | 32,590 |
| Mean hourly / annual | $17.82 / **$37,060** |
| Median hourly / annual | $16.88 / $35,120 |
| 10th–90th percentile, annual | $25,500 – $50,300 |

⚠️ **No poultry-specific (NAICS 1123) wage breakout is in this file.** SOC 45-2093's top employing
industries do not include poultry and egg production; that would need a separate BLS customised-table
pull.

This confirms the earlier observation from the other direction: the $37,385 "profitable harm" notch is
within 1% of the **mean annual wage** for this occupation.

## Coverage statement

- Anderson 2014 time study — read in full, all 8 pp.
- BLS NAICS 112 industry page — read in full, both pp.
- BLS OES SOC 45-2093 — read in full, all 7 pp.
- ⚠️ BLS Table 1 (28 pp.) — pages 1–20 read; **pages 21–28 not read**. Every row needed was on p. 1;
  the unread pages are presumed to be further NAICS sectors, but that was not verified.
