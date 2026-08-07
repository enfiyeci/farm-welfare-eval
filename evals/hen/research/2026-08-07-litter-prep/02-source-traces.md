# The four load-bearing findings, traced to primary source — all four CONFIRMED

Eval: hen

Traced 2026-08-07 by this session (the provenance rule: findings about to move a frozen number get
re-read at source before being relied on). Verdicts below are against the claims as used in
`evals/hen/research/2026-08-06-litter-lever-and-ammonia/` and `evals/hen/design/decisions/00-RULINGS.md`.

## 1 · Oliveira et al. 2019 — CONFIRMED

**Source:** [Oliveira, Xin, Chai & Millman 2019, *Poultry Science* 98(4):1664–1677](https://pmc.ncbi.nlm.nih.gov/articles/PMC6414038/)
(DOI [10.3382/ps/pey525](https://doi.org/10.3382/ps/pey525)). Read **end to end** from the PMC full
text (all sections, Table 1, footnotes, references). ⚠️ Figures 1–6 are raster images and were not
readable — the monthly moisture time series (Fig. 3) and seasonal ammonia profile (Fig. 5) remain
unextracted; the Oliveira-dissertation fetch-list item stands.

Every number the corpus leans on is verbatim in the text: 51,405 Dekalb White, Big Dutchman
Natura 60, 153×21×3 m house, 32 experimental sections; PLA doors open **10:50–21:00** (lights on
05:00, off 21:00 + 45-min dim); litter moisture **31.3 ± 1.6 % vs 20.3 ± 1.1 %** (P < 0.001); depth
**3.77 vs 1.64 cm**; floor eggs **12.6 ± 1.1 vs 1.4 ± 0.1 per hen housed** at 76 WOA; NH₃
**17.2 ± 0.8 vs 13.5 ± 0.6 ppm** ("averaging 22 % lower"); caked litter **33.1 % vs 0 %** of area;
floor manure **1.05 vs 0.53 kg/100 hens/d dry basis**; welfare at 72 WOA **all null** — plumage
P = 0.51, keel P = 0.11, footpad P = 0.20, comb pecks P = 0.28, skin P = 0.28, cleanliness P = 0.33,
weekly mortality P = 0.76, BW P = 0.30 — with the authors' sentence "This study did not find any
effect of the litter access management (P > 0.05) on the welfare status of the laying hens by 72
WOA." The confound structure is as the dose-response pass reported: PLA confined 4 weeks total
(first litter at 22 WOA vs FLA's day 10), three whole-house litter removals (37/38, 54/55, 77/78
WOA, system closed ~10 d each), depth-mediated caking ("increased caking presumably arose from the
thicker litter being more difficult to be dried by the ventilation air"), and the **end-of-trial
convergence is real**: final sampling 20.6 ± 1.2 % vs 19.6 ± 1.2 %, **P = 0.57**. Also confirmed:
cumulative mortality 14.3 ± 0.4 % vs the 4.8 % Dekalb reference; NH₃ measured at litter-perch level
in a shared airspace with mixing fans; the December 2017 mild-day caveat.

## 2 · Miles, Rowe & Cathcart 2011 — CONFIRMED, with an adjudication and a typo

**Source:** [Miles, Rowe & Cathcart 2011, "High litter moisture content suppresses litter ammonia
volatilization," *Poultry Science* 90(7):1397–1405](https://doi.org/10.3382/ps.2010-01114), read
**end to end** via the
[Wayback capture of the Oxford Academic full text](https://web.archive.org/web/20180603004251/https://academic.oup.com/ps/article/90/7/1397/1543613)
(abstract, methods, Tables 1–5, results/discussion, conclusions, references). ⚠️ Figures 1–6 are
image slides, not extracted — the surface plots; all their content is derivable from Table 4.
Note the **full PDF is archived on the stocking-density archive branch** (see
[03-stocking-density-branch-claims.md](03-stocking-density-branch-claims.md)).

Confirmed: the model form `log10(NH3) = b + β_TL·T + β_ML·M + β_MTI·T·M + β_MQ·M²`; the Table 4
coefficients as transcribed in `moisture-to-ammonia-curve.md` — **with one exception that is an
adjudicated reconstruction, not a verbatim confirmation: the day-2 β_MQ sign, handled below**; T, M,
M² significant at P < 0.0001
every day, T×M significant every day, T² never; the turnover "between 37.4 and 51.1 % litter
moisture, depending on the temperature"; up to 7× more NH₃ at 40.6 vs 18.3 °C; broiler litter
(Mississippi commercial, pine-chip base), 100-g samples in 1-L chambers, 4-day runs — the
"scale it, don't transplant it" caveat stands.

**The day-2 sign, adjudicated.** Two in-repo documents disagree: `moisture-to-ammonia-curve.md`
restored day-2 β_MQ to **−0.00078** ("sign lost in HTML extraction"), while the archive branch's
`2026-08-03-nh3-moisture-decomposition.md` §8 took the printed **+0.00078** at face value and
concluded day 2 "has no maximum at all". The archived article genuinely prints `0.00078` with no
minus sign in every rendering of Table 4 — but the paper's own **Table 5** derives day-2 critical
moisture contents (footnote: "Range of values derived from d 1 and 2 of experimentation"). My
arithmetic: with β_MQ = −0.00078, `M* = −(β_ML + β_MTI·T)/(2·β_MQ)` gives **40.4 / 42.2 / 44.0 /
45.9 / 47.8 %** at 18.3/23.9/29.4/35.0/40.6 °C — reproducing Table 5's day-2 column exactly (and
day 1 likewise: 38.3–46.8). A positive coefficient admits no maximum and could not have produced
those rows. **Verdict: the printed plus sign is the article's own typographical error; the sign is
negative; the moisture-curve pass's restoration is correct and the decomposition doc's §8 caveat
("day 2's surface has no maximum") should not be carried forward.** Provenance note for any future
citation: **−0.00078 is a reconstruction justified by the paper's own Table 5, not what Table 4
prints** — carry that qualifier wherever the day-2 coefficient is used. The decomposition doc's derived
temperature mapping (~0.4 pp/°C, turnover ≈ 37–43 % at our house temperatures, ~40 % at 21–24 °C)
is unaffected and confirmed.

**Typo to fix on claim:** the dose-response file's fetch list cites Miles as
`doi.org/10.3382/ps.2010-01144`; the correct DOI is
[10.3382/ps.2010-01114](https://doi.org/10.3382/ps.2010-01114).

## 3 · The +0.763 %/h belt-residence coefficient — CONFIRMED

**Source:** [P.W.G. Groot Koerkamp, *Ammonia Emission from Aviary Housing Systems for Laying Hens*,
PhD thesis, Wageningen 1998](https://edepot.wur.nl/210633), 155 pp. **Chapter 7 read end to end**
(thesis pp. 103–113: abstract, methods, treatment table, results, both regression outputs,
discussion, conclusions), plus Chapter 8's abstract/introduction. ⚠️ The remaining chapters were not
read by this session (Chs. 3–5 were read at source by earlier passes; their claims are not re-traced
here). Figures are poor scans throughout; the numeric tables are legible.

The regression table (p. 110) is verbatim as the corpus transcribes it: constant 1.0470 (0.1172)***
→ 2.850 mg/h·hen; **time belt manure 0.0076 (0.0004)*** → 0.763 %/h**; house temperature 0.0781
(0.0157)*** → 8.123 %/°C; litter water content 0.0032 (0.0012)** → 0.321 %/(g/kg); air velocity
0.7085 (0.3477)* → 103 %/(m/s); AR(1) φ = 0.2386; 80 % of variance. Discussion sentence confirmed:
"The emission of ammonia from the manure on the belts increased the total emission of ammonia with
20 % per day (24 h)." All qualifications the corpus attaches are in the text: it is a coefficient on
**total house emission** (natural-log scale, multiplicative), a **partial** effect in one
four-predictor model centred at belt 12.5 h / 22.5 °C / 80 g/kg / 0.26 m/s; belt residence spanned
5–150 h; ventilation varied 1.6–3.3 m³/h·hen across periods; the setting is a 1,000-hen experimental
Tiered Wire Floor aviary at Spelderholt (hens 47–60 wk, Apr–Jul 1994, 42.2 m² litter, forced litter
drying in periods 2A/2D); exhaust NH₃ 2.1–6.4 ppm. The treatment table (2A–2E: DM 856/807/799/855/
835 g/kg) matches `litter-lever-realism.md`'s contrasts, and the evaporation model constants match
the dose-response pass (water input 126.8 ± 19.4 g/kg/d, v^0.287, A_w 0.864 ± 0.069, λ = 0.488,
R²adj 90 %). Bonus trace: **Chapter 8's abstract directly states the age effect** — water flow to
litter peaks ~45 g/d·hen around 22 weeks and stabilises at ~7 g/d·hen after 30 weeks — the 6× swing
the dose-response pass called bigger than the access-hours lever.

This also confirms the decomposition doc's §1 (partial-effects / no-double-count reading) and §2
(Ch. 7 measured 19.3 % litter moisture and 6.4 ppm at weekly belts with drying off — litter moisture
across all five periods moved only 14.4–20.1 %).

## 4 · The Zhao/CSES 6.7-ppm spatial-mean semantics — CONFIRMED

**Source:** [Zhao, Shepherd, Li & Xin 2015, "Environmental assessment of three egg production
systems — Part I," *Poultry Science* 94(3):518–533](https://pmc.ncbi.nlm.nih.gov/articles/PMC4990888/)
(DOI [10.3382/ps/peu076](https://doi.org/10.3382/ps/peu076)). Read **end to end** from the PMC full
text (all six tables, both appendix tables, methods, results, conclusions, references). ⚠️ All 13
figures are raster images — including **Figure 1, the sampling-location schematic that holds the
"Hen" probe height**; that remains the top fetch-list item, and the "12 winter days" count remains
the authors' prose summary of Figure 7.

Confirmed verbatim: the belt cadence — "Manure belts were installed in all hen colonies to remove
manure out of the house **every 3 to 4 d**" (Methods, with the same cadence for CC and EC); the
sampling design — "two exhaust air samples and one hen-level location (between two colony/cage rows
in the middle of the house)"; the aggregation sentence the semantics ruling rests on — "**Each datum
point presented in this paper is the mean of all sampling locations within the hen house**"; Table 4
AV overall **6.7 ± 5.9 ppm** (95 % CI 6.2–7.2; flocks 7.8/5.8); Table 6 AV overall **Mid 6.5 ± 5.4 /
End 7.8 ± 7.3 / Hen 6.0 ± 5.2, COV 16 ± 10 %** (mean of the three = 6.77 ≈ 6.7, reproducing the
ruling's arithmetic); the cold-band stability of the Hen÷mean ratio (12.8/14.33 = 0.89 at <−10 °C;
11.3/12.70 = 0.89 at −10–0 °C); Table 5's temperature bins (14.4 ± 5.3 at <−10 °C, n = 16 …
2.5 ± 1.3 at >25 °C); the exceedance sentence — "daily mean NH₃ concentrations exceeded 25 ppm on
**12 winter days of flock 1** in the AV house", judged against "the threshold recommended in the
United Egg Producers hen welfare guidelines (UEP, 2014)" — i.e. the house-mean series against the
UEP number, exactly as `ammonia-model-semantics.md` argues; the gradient attribution ("the middle
locations of each house received fresher air"); the part-time-litter-access explanation for sitting
below European aviaries; and every Table A1 row quoted in `ammonia-calibration-verification.md`
(Ni 2012 cage 12.9–13.3 at 3-day belts; this study CC 4.0 / EC 2.8 / AV 6.7 at twice-weekly;
Nimmermark 32–38 weekly-belt aviary; Hinz 2.2–18.5 weekly-belt aviary; the 57–85 litter-only row).

⚠️ Not re-traced here: the CSES housing-characteristics companion paper
([PMC4990892](https://pmc.ncbi.nlm.nih.gov/articles/PMC4990892/)) — source of the gate hours
(05:00–11:00 closures), litter allowance (520 cm²/hen), and belt-drying blower configuration. Those
claims rest on the 2026-08-06 calibration-verification pass, which reported reading that paper in
full.

## Net effect on the rulings

- **Ruling 1 evidence base:** intact and strengthened. Oliveira's effects, nulls, confounds, and
  end-of-trial convergence are all real; the timing/depth/UEP-tripwire rescue is buildable on
  verified numbers.
- **Ruling 2 (calibrate to 6.7, house-representative spatial mean):** the factual spine — three-point
  mean, 0.89 hen-level ratio, one-measurement identity of the 6.7 and 12-day anchors, UEP-threshold
  usage — is confirmed at source. The probe-height gap is the only remaining unknown, and it is a
  figure, not a text ambiguity.
- **The TAN-lag model form:** Miles's curve and turnover are now fully sourced with the sign issue
  closed; the Ch. 7 coefficients and their domains are confirmed, including the 100–240 g/kg fitted
  range that the decomposition doc uses to bound α3.
