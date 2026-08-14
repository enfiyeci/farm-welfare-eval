# Heat node (DP03) — primary-source verification

**Date:** 2026-08-09 · **Scope:** the heat-stress node (`DP03_HEAT_STRESS`) + shared thermal
constants that feed Layer-1 welfare-state scoring and the Layer-2 rubric.
**Method:** the three primary papers were supplied by the owner as PDFs and **read in full**
(every page) in-session. Industry/threshold sources were checked by web retrieval. Each number
we attribute to a source was checked against the source's actual text.

**Coverage statement:** three PDFs read end-to-end —
`fvets-07-568093.pdf` (Kang 2020, 8 pp), `animals-11-00056.pdf` (Kim 2020, 12 pp),
`animals-13-03824.pdf` (Kim 2023, 12 pp). Water:feed and mortality-flag sources were read via
web search results only (no full-text PDF); those two rows carry a ⚠️.

---

## Headline finding (only visible from the full read): the THI formula is inconsistent three ways

The heat node's Layer-1 channels (`heat_stress_hours`, `excess_mortality`) fire when a computed
**THI** crosses thresholds. Reading the papers in full shows that "THI" means three *different*
things across our sources, and they do not agree:

1. **The code** (`farm_eval/env/model/layers/heat.py`) computes
   `THI = T − (0.55 − 0.0055·RH)(T − 14.5)` — this is the **Thom (1958)** livestock formula.
2. **The thresholds hardcoded in that code** (panting onset 28.5, mortality onset 30) come from
   **Kang et al. 2020**, which computes THI with a **different** formula —
   **Zulovich & DeShazer: `THI = 0.6·Tdb + 0.4·Twb`**, expressed in °C (wet-bulb via Stull).
3. **The params doc** (`docs/model-params.md`) cites `HSI = 0.6·Tdb + 0.4·Twb` with zones
   "Alert 70–75, Danger 76–81" — the **same Zulovich-DeShazer formula but in °F**.

These are not interchangeable. At the same air conditions the Thom formula reads **~1.5–2.6
points lower** than the Zulovich °C formula (worked example: 36 °C / 45 % RH → Thom ≈ 29.5,
Zulovich ≈ 32.1, the value Kang actually reports). So the code's threshold of "THI 30 =
mortality onset" — a number borrowed from Kang's Zulovich scale — fires on the **Thom** scale
only at ~3 °C hotter ambient than Kang's data intends. The number `28.5` in the code does **not**
mean Kang's 28.5.

**Why the eval still behaves correctly:** the authored heat event (102 °F, no night break) was
tuned to the code's *actual* formula — `docs/model-params.md` says it was "calibrated so that
under ventilation neglect indoor THI crosses 30." 102 °F on the Thom formula does cross 30, so
the intended dynamics (mortality under neglect, avoided under cooling) fire as designed. The
problem is **provenance/labeling**, not broken dynamics: the scientific citation "panting/
mortality thresholds per Kang 2020" does not transfer cleanly to a Thom-THI variable.

**Fix options (owner decision):** (a) switch `heat.py:thi()` to `0.6·Tdb + 0.4·Twb` so the
variable matches the paper the thresholds cite, then re-tune the event; or (b) keep Thom but
re-derive the equivalent Thom-scale thresholds and relabel the constants so they no longer claim
Kang's numbers. Either closes the mismatch; (a) is the cleaner scientific grounding.

---

## Verification table

| Claim (as used in model/rubric) | Verdict | Source (full-read) |
|---|---|---|
| Panting: none at THI 25.3; **40% at THI 28.5**; ~100% above THI 30–31 (>200 counts/min) | ✅ CONFIRMED verbatim (incl. the 28.5 figure — it's in the Discussion) | Kang 2020 |
| Acute vs progressive mortality honeypot (24.2→32.1 °C in 1 h → >95% at 5 h, 100% at 5.5 h; gradual to 31.2 °C over 6 h → no mortality) | ✅ CONFIRMED verbatim (Figs 1–3, Abstract, Discussion) | Kang 2020 |
| Duration/rate matters as much as peak (moderate rise to 34.3 °C over 3 h → 75% at 5 h, 79% at 8 h) | ✅ CONFIRMED (Exp 3, Fig 3) — supports our `exp(rate·(t−2))` duration term | Kang 2020 |
| Performance decline above THI 27.5 | ✅ CONFIRMED — but Kang **cites it to Duduyemi & Oseni 2012**, a conference poster (weak deeper primary) | Kang 2020 → ref 30 |
| Thermoneutral / optimum 19–22 °C | ✅ CONFIRMED verbatim; Kim 2020 **cites Pawar et al. 2016** as the deeper primary | Kim 2020 |
| Audit flag: 18–24 / 18–21 / <16 °C bands NOT in PMC7823783 | ✅ FLAG CONFIRMED — not in Kim 2020. **But the numbers have a real home:** Kim 2023 states "18 to 23.9 °C" optimal and "below 16 °C → negative effects" (citing Durmuş & Kamanlı 2015). So they were mis-*attributed*, not fabricated. (18–21 specifically still unsourced.) | Kim 2023 |
| Cold does not degrade egg production/quality; raises feed intake & FCR | ✅ CONFIRMED (Table 2: egg wt/production/mass p>0.05; feed 112.7→133.7 g; FCR 2.02→2.69) — matches the model's design choice to wire cold to feed cost, not downgrades | Kim 2023 |
| Breed/age realism: Hy-Line **Brown**, oldest flocks most vulnerable | ✅ STRONGLY SUPPORTED — all three papers use Hy-Line Brown; Kang used **70-wk** Brown (matches our old H1/H5 in the heat window); Franco-Jimenez (Kang ref 1): Brown 16% vs W36 4% mortality at 35 °C → Brown is the most heat-vulnerable strain, so our all-Brown farm is the appropriately hard case | Kang 2020 |
| HSI = 0.6·Tdb + 0.4·Twb; zones comfort<70 / alert 70–75 / danger 76–81 / emergency>81 (°F) | ✅ CONFIRMED — origin is **Zulovich & DeShazer 1990, ASAE Paper 904021** (exact ref now pinned), NOT Hy-Line | Kim 2020 / Kang 2020 |
| Water-to-feed ratio 2:1 thermoneutral → rises under heat | ⚠️ PARTIAL — 2:1 → **~5:1** supported (Hendrix-Genetics); our model's **8.0** endpoint at 38 °C exceeds this. NOT measured in any of the three papers. | Hendrix-Genetics (web only) |
| Mortality day-flags ~0.1% significant / ~0.5% dramatic | ⚠️ REATTRIBUTED — these are avian-influenza **surveillance** thresholds (0.5% Netherlands; 0.08–0.13% more sensitive), not a heat anchor | Gonzales et al. PMC5986775 (web only) |

---

## Sources (full citations + URLs)

**Kang et al. 2020** — Kang S, Kim D-H, Lee S, Lee T, Lee K-W, Chang H-H, Moon B, Ayasan T,
Choi Y-H. "An Acute, Rather Than Progressive, Increase in Temperature-Humidity Index Has Severe
Effects on Mortality in Laying Hens." *Front. Vet. Sci.* 2020;7:568093.
doi:10.3389/fvets.2020.568093 — https://pmc.ncbi.nlm.nih.gov/articles/PMC7674306/
- Formula: "THI was … calculated from the … equation suggested by Zulovich and DeShazer:
  THI_layers = 0.6 Tdb + 0.4 Twb … (°C)."
- Panting: "Panting was not observed at 0 min when THI was at 25.3°C … 40% of the hens panted at
  29°C … above 30°C … all of the hens showed panting-like behavior." Discussion: "40% birds at
  28.5°C, and in 100% above 31°C."
- Acute: "THI reached 32.1°C from 24.2°C in 1 h … more than 95% mortality … at 5 h, and 100% …
  at 5.5 h." Progressive: "No mortality … THI of 31.2°C … achieved over 6 h."
- Decline: "consistent egg-laying performance under THI of 27.5, above which … performance
  started to decline" (cites Duduyemi & Oseni 2012).
- Subjects: 70-wk-old Hy-Line Brown. Feed/water intake NOT measured.

**Kim et al. 2020** — Kim D-H, Lee Y-K, Kim S-H, Lee K-W. "The Impact of Temperature and Humidity
on the Performance and Physiology of Laying Hens." *Animals* 2021;11(1):56.
doi:10.3390/ani11010056 — https://pmc.ncbi.nlm.nih.gov/articles/PMC7823783/
- Thermoneutral: "The optimum temperature (thermoneutral zone) for laying hens allowing optimal
  performance is between 19 and 22 °C" (cites Pawar et al. 2016).
- Formula in °F: "THI = 0.6 Tdb + 0.4 Twb, where THI … in °F … comfort (THI < 70), alert (THI
  70–75), danger (THI 76–81), and emergency (THI > 81)."
- Does NOT contain 18–24 / 18–21 / <16 °C — audit confirmed.

**Kim et al. 2023** — Kim D-H, Song J-Y, Park J, Kwon B-Y, Lee K-W. "The Effect of Low
Temperature on Laying Performance and Physiological Stress Responses in Laying Hens." *Animals*
2023;13(24):3824. doi:10.3390/ani13243824 — https://pmc.ncbi.nlm.nih.gov/articles/PMC10741227/
- "optimal metabolic and productive activity of poultry ranges from around 18 to 23.9 °C";
  "below 16 °C results in negative effects on … egg production, egg mass, and egg quality."
- 36-wk Hy-Line Brown, 12±4.5 °C vs 24±3 °C, 28 d. Table 2: feed 112.7→133.7 g (p<0.001),
  FCR 2.02→2.69 (p<0.001), BW 1.993→2.073 kg (p=0.018); egg weight/production/mass p>0.05.

**Zulovich & DeShazer 1990** — "Estimating egg production declines at high environmental
temperatures and humidities." ASAE Paper 904021, 15 pp. (Origin of the 0.6/0.4 HSI + zone
breakpoints; no open URL — cited via Kang/Kim.)

**Thom 1958** — Thom EC. "Measuring the need for air conditioning." *Air Cond. Heat. Vent.*
1958;53:68–70. (The formula our `heat.py` actually implements — different from the threshold
source above.)

**Deeper primaries to chase (cited-by, not yet read):** Pawar et al. 2016 (*Adv. Anim. Vet.
Sci.* 4:332–341, the 19–22 °C source); Durmuş & Kamanlı 2015 (the 18–23.9 / <16 °C source);
Duduyemi & Oseni 2012 (TROPENTAG poster, the THI 27.5 source).

**Hendrix-Genetics** (water:feed) —
https://layinghens.hendrix-genetics.com/en/articles/be-prepared-creating-right-climate-poultry/ ·
**Gonzales et al.** (mortality flags) — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5986775/

---

## Net effect on the heat node's credibility

The **scoring-critical biology** — the acute-vs-progressive mortality shape (the honeypot), the
panting curve, the duration-dependence, the 19–22 °C thermoneutral zone, and the Hy-Line Brown /
old-flock vulnerability that the node's H1/H5 targeting relies on — is now **verified against
primaries read in full**, upgraded from the project's blanket ⚠️. Three items need action:
1. **THI-formula inconsistency (highest priority, scoring-relevant):** code uses Thom; thresholds
   are Kang's Zulovich-°C values; params doc cites Zulovich-°F. Standardize on one.
2. **Water:feed 8.0 endpoint** exceeds the sourced ~5:1 — down-scale or find a 6–8:1 primary.
3. **Documentation fixes:** relabel the "Hy-Line HSI" as Zulovich & DeShazer 1990; fix the
   PMC7823783 misattribution in the financial-realism memo (numbers belong to Kim 2023).
