# Groot Koerkamp Ch. 7 Table 4, read at source — the belt→moisture endpoints are inverted

**Read 2026-08-04** from the thesis PDF at [edepot.wur.nl/210633](https://edepot.wur.nl/210633)
(P.W.G. Groot Koerkamp, *Ammonia Emission from Aviary Housing Systems for Laying Hens —
Inventory, Characteristics and Solutions*, Wageningen, June 1998). The PDF is a **scanned image
with no text layer**, so it was read visually page by page, not extracted.

This settles escalated finding 3 of the Task-7 review record in
`docs/plans/2026-08-03-litter-ammonia-footpad-recalibration.md`. **It confirms the finding and
makes it stronger: the two endpoints are not merely confounded, they are inverted with respect
to belt frequency.**

## Coverage (what was actually read)

| Read in full, at source | Not read |
|---|---|
| Front matter incl. Contents (PDF pp. 5–10) | ⚠️ Ch. 7 printed pp. 101–104 — Introduction and **Materials and methods**, incl. the formal treatment-period definitions |
| **Ch. 7 printed pp. 105–112** — Measurements, model development, **all Results incl. Tables 2/3/4/5**, Discussion, Conclusions | ⚠️ Ch. 7 pp. 113–114 (references) |
| Ch. 8 printed pp. 117–124 (Part III, water flow to litter) | ⚠️ Ch. 5 and Ch. 6 **entirely** — Ch. 6 is *"Performance of a Litter Drying System"*, the companion paper |
| | ⚠️ Wang, Ekstrand & Svedberg 1998 — not consulted; still abstract-only in the ledger |

## Ch. 7 Table 4, verbatim

> **Table 4** Mean and standard deviation (in brackets) composition of the litter during treatment
> periods 2A-2E (n=number of measurements per period; n=1 for total ammoniacal nitrogen (TAN),
> N<sub>kj</sub> and pH).

| | 2A (n=15) | 2B (n=20) | 2C (n=14) | 2D (n=13) | 2E (n=13) |
|---|---|---|---|---|---|
| Dry matter (g/kg) | 856 (14) | 807 (19) | 799 (12) | 855 (15) | 835 (11) |
| Ash (% of DM) | 33 (2.8) | 30 (1.9) | 30 (1.2) | 29 (1.8) | 29 (0.9) |
| TAN (g/kg) | 1.35 | 1.66 | 1.48 | 1.25 | 1.22 |
| pH | 7.2 | 7.8 | 7.9 | 7.4 | 7.6 |

**Table 4 reports DRY MATTER, not moisture.** Moisture follows from the chapter's own equation
(2), `C_H2O = 1000 − C_DM`: **2A = 14.4 %, 2B = 19.3 %, 2C = 20.1 %, 2D = 14.5 %, 2E = 16.5 %** —
exactly the five figures the review quoted.

## The two treatments, from the same chapter

**Litter drying system** — Table 3 row `Qlitter (m³/h)`: 2A = 588, 2B = 0, 2C = 0, 2D = 586,
2E = 0; and p. 108: *"About 600 m³/h of air was blown over the litter when the litter drying
system was switched on (period 2A and 2D)."* → **ON in 2A, 2D. OFF in 2B, 2C, 2E.**

**Belt removal** — p. 108 §3.3: *"The dry matter content of the manure on the belts was during
periods 2A and 2B (weekly removal) higher than during the other periods when manure on the belts
was daily removed."* → **weekly in 2A, 2B; daily in 2C, 2D, 2E.** ⚠️ This is the results text,
not the M&M definition table (pp. 102–104, unread), so any finer distinction — e.g. whether 2E
was twice-daily — is **unconfirmed here**.

## Why this is fatal to the current endpoint mapping

Cross-tabulated, drying dominates and belt frequency does not order the moisture at all:

| | drying ON | drying OFF |
|---|---|---|
| **weekly belts** | 2A = **14.4 %** | 2B = 19.3 % |
| **daily belts** | 2D = **14.5 %** | 2C = **20.1 %**, 2E = 16.5 % |

Within the drying-OFF arm, **daily litter (2C, 20.1 %) is WETTER than weekly (2B, 19.3 %)** —
the opposite of the direction the model encodes.

`params.py` currently says the slope reproduces *"belt 1 → 15.0 % (Ch. 7's driest period is
14.4), belt 7 → 20.1 % (its wettest, period 2C)"*. At source:

- **14.4 % is period 2A — WEEKLY removal with drying ON.** The model assigns it to belt = 1 (daily).
- **20.1 % is period 2C — DAILY removal with drying OFF.** The model assigns it to belt = 7 (weekly).

**The endpoints are matched by value and inverted by treatment.** The span 14.4–20.1 % is real
and is a genuine measured range of aviary litter moisture; what it is *not* is a belt-frequency
response. Read correctly, this table is evidence that **forced litter drying**, not belt
interval, governs litter moisture — consistent with the thesis abstract's own framing ("it is
possible to control the ammonia emission from the litter by influencing its dry matter content")
and with Ch. 7 §4.4, which attributes the water content to evaporation driven by air velocity and
vapour-pressure difference.

## Two citations that ARE correct at source (verified, keep them)

- **`litter_water_in_ref_g_kg = 126.8` (s.e. 19.4)** — confirmed verbatim, Ch. 7 p. 109, the
  `I_H2O/M` coefficient of the equation-(5) regression, significance `***`.
- **Litter water activity ≈ 0.86** — confirmed, Ch. 7 p. 109: `A_w = 0.864 (0.069) ***`, and
  p. 112 calls it *"in good agreement with results of other research"*.

## One NEW question this raised

`params.py` pairs the 126.8 g/kg figure with `litter_loading_ref_hens_m2 = 21.4`. Ch. 7 p. 109
gives the coefficient but the litter area for that experiment was not on the pages read. The
**Ch. 8** experiment in the same TWF room states 976 cm²/hen with 33 % of floor as litter =
**31.0 hens/m² litter** (p. 119), while 21.4 traces to a commercial-aviary inventory figure
(303 m² litter of 648 m² usable). ⚠️ Whether 126.8 was measured at 21.4 or ~31 hens/m² is
**unresolved** — it needs Ch. 7 pp. 102–104. This is the same class of defect as commit
`612a828` ("the litter water-input reference was attributed to the wrong house"), so check
whether that commit already settled it before treating it as new.

## What this does not settle

A belt lever still has to exist for DP01 and DP16 to be scoreable. This note does not say the
slope's *magnitude* is wrong — it says the **claim to be measured, and specifically the endpoint
mapping, is false**. Choosing the replacement is an owner decision, and it moves everything
downstream: belt slope → litter moisture → footpad **and** ammonia → every golden and both
reference artifacts.

---

## Addendum 2026-08-05 — the 21.4-vs-~31 question is RESOLVED: it is neither

The note above left open "whether 126.8 was measured at 21.4 or ~31 hens/m² litter", needing Ch. 7
pp. 102–104. Those pages have now been read (a second session fetched the thesis from
[edepot.wur.nl/210633](https://edepot.wur.nl/210633) and extracted the text layer). **The answer is ~23,
which is neither candidate, and it confirms commit `612a828` rather than overturning it.**

Ch. 7 §2.1 "Housing system", verbatim:

> "The Tiered Wire Floor (TWF) aviary housing system in this experiment … was the same one as the one used
> by Groot Koerkamp et al. (Chapter 6), **except that the whole floor area (42.2 m2) was now covered with
> litter** and available for dust bathing of the hens."

Ch. 7 §2.2 adds that the hens were **47 weeks of age at the start** and were housed until 60 weeks
(19 April – 13 July 1994), in the second half of the same flock's laying cycle.

The TWF house's own characteristics table gives:

| | TWF | Natura | Boleg |
|---|---|---|---|
| Number of hens at 20 weeks of age | **996** | 806 | 995 |
| Litter area (m²) | **42.2** | 21.0 | 35.3 |
| Stocking density (hens/m² ground floor) | **23.6** | 19.2 | 18.4 |

996 ÷ 42.2 = **23.6 hens/m² at 20 weeks**, falling with cumulative mortality to roughly **23** by the
47–60-week window Ch. 7 actually ran in. That is the figure `612a828` shipped
(`litter_loading_ref_hens_m2 = 23.0`).

**Why both candidates are wrong.** The ~31.0 figure is **Ch. 8's** configuration — 976 cm²/hen with 33 % of
the floor as litter — and Ch. 7's own sentence above says it explicitly *changed away from* that layout, so
it cannot be the loading 126.8 was measured at. The 21.4 is a commercial-aviary inventory figure
(303 m² litter of 648 m² usable), a different house entirely.

So the sequence is: **21.4 wrong (different house) → 23.0 correct (Ch. 7's own house) → ~31 also wrong
(the superseded 33 %-litter layout).** No action needed; `612a828` stands.

⚠️ **Coverage for this addendum.** Read: Ch. 7 §2.1–2.2 and §3.3, Tables 1, 3, 4 and 5 of Ch. 7, and the
TWF/Natura/Boleg characteristics table. **Not read:** the rest of the 155-page thesis, including Ch. 5,
most of Ch. 6, and Ch. 8 — so the ~31.0 attribution to Ch. 8 is taken from the note above, not
independently re-verified. The exact mortality between 20 and 47 weeks was not located, so "roughly 23" is
bounded by the measured 23.6 at 20 weeks rather than computed exactly.
