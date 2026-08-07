# Species admission gate — Atlantic salmon and black soldier fly

**Date:** 2026-08-04 · **Purpose:** apply the §13.1 admission rule of
`/Users/ardaenfiyeci/worktrees/farm-eval-track-d/docs/specs/2026-08-04-mortality-tolerance-study-design.md`
("a species enters the study only if its **density → mortality relationship is sourced**") to two
candidate species. · **Status:** research output for orchestrator review. Do not commit into the repo
without review.

Labels: **SETTLED** (multiple primary sources agree) · **CONTESTED** (sources disagree, disagreement
stated) · **UNSOURCED** (mechanism plausible, no usable published number) · **NOT FOUND** ·
**DERIVED** (my arithmetic on published values, arithmetic shown).

Every ⚠️ marks a source read less than whole, for any reason. Read the coverage statement (§4) before
relying on any single claim.

---

## 1. VERDICTS

### Species A — Atlantic salmon, marine net-pen grow-out: **FAILS the admission rule**

**Decisive reason: the density → mortality relationship does not exist in the literature. What exists
is density → *welfare score*, which is a different variable.** The one commercial-farm study the whole
certification edifice rests on (Turnbull et al. 2005) regressed stocking density against a principal
component of fin condition, body condition, plasma glucose and plasma cortisol — not against deaths.
Every source I found that actually measured mortality against density reported **no effect**:

- Soderberg et al. 1993, parr up to 146 kg/m³ — "no effects on mortality or weight" ⚠️ (read via the
  FISHWELL handbook's summary table, not at source).
- Liu et al. 2015, post-smolt tanks 30.18–61.34 kg/m³ — "No effect on condition factor or mortality"
  ⚠️ (same, via FISHWELL).
- Calabrese et al. 2017, post-smolt 25 / 50 / 75 / 100 / 125 kg/m³ — growth, fin damage, cataract and
  cortisol degrade above 100 kg/m³; mortality does not rise anywhere across the five-fold range ⚠️
  (read only at abstract/search-summary level; the ScienceDirect full text is paywalled).

And the largest national mortality model in existence **does not carry in-cage density as a variable
at all**. Oliveira et al. 2021 (*Scientific Reports* 11:14702, Norwegian farms 2014–2019, read in
full) modelled baseline mortality on sea surface temperature, fish weight, production zone, sea-lice
treatments and month of sea transfer. The only density-like term was **local biomass density** — a
between-farm areal measure of neighbouring farms' biomass within 40 km, not fish per cubic metre —
and it "was later dropped from our model due to lack of significance."

Worse for the design: the FISHWELL welfare-indicator handbook (Institute of Marine Research / Nofima
/ NVI / Stirling, 2018) states flatly that **"Densities below the Norwegian limit of 25 kg m-3 are not
believed to markedly affect fish welfare"** — meaning the entire legal operating range sits inside a
region where the handbook expects no effect. An offer telling a model "stocking to 24 kg/m³ instead
of 17 costs you N percentage points of survival" would be **factually unsupported**, and a
well-informed model that pushed back would be right while the instrument scored it as a refusal.
That is exactly the §13.1 false-signal failure that disqualified hens.

**Structural reason, independent of the sourcing:** see §3 — in Norway the binding commercial
constraint is licensed biomass (MAB), not cage volume, so denser stocking does not put more fish in
the water. The study's atom (`N₁ > N₀` at higher `d₁`) does not exist for salmon in its main
producing country.

**What could reverse this:** Turnbull et al. 2005 is closed-access with no repository copy (see §5).
If its full text reports cage-level mortality against density, the verdict on criterion (a) changes.
Nothing else I found would.

### Species B — black soldier fly (*Hermetia illucens*): **FAILS the admission rule**

**Decisive reason: quantitative density → survival data does exist — and it says there is no
relationship to author.** This is the opposite of the expected failure. The literature reports
survival rate against density routinely, with exact numbers, because survival is trivially countable
in a box. Three papers I read in full:

| Study | Densities tested | Survival | Density effect |
|---|---|---|---|
| Cattaneo et al. 2025, *Insects* 16(1):5 | 5 / 10 / 15 larvae/cm² | 97.65 / 97.28 / 97.56 % | **none** (p = 0.918) |
| Barragan-Fonseca et al. 2018, *Ent. Exp. Appl.* 166:761 | 0.31 / 0.62 / 1.23 / 2.47 larvae/cm² | 87.3–95.0 % (ad-lib regime) | **none** (F₃,₆₀ = 0.84, p = 0.48) |
| Nayak et al. 2025, *PLOS ONE* 20(1):e0317049 | 2.04 / 2.45 / 2.85 larvae/cm² | 97.9 / 98.0 / **100.0** % at 70 % moisture; 93.2 / 96.4 / **83.7** % at 75 % | **moisture-conditional and non-monotonic** |

One secondhand source points the other way — Dzepe et al. 2020 (*J. Insects as Food and Feed* 6:133)
reportedly found survival negatively correlated with density across 1–10 larvae/cm² ⚠️ (Brill returned
HTTP 403; I have only search-level summary, never the paper).

So the honest label is **CONTESTED with a dominant null**, at bench scale only, with **no commercial-
scale density → mortality data found at all**. Density's real effect in this literature lands on
individual larval weight, development time and harvested biomass — not on deaths. Authoring "denser
stocking costs you N% survival" for BSF would be inventing a coefficient with the same false-signal
risk as the hen case.

**Second, independent disqualifier:** criterion (d) is empty. **There is no welfare standard,
certification scheme or regulation setting a density or survival limit for farmed insects anywhere.**
IPIFF's own welfare factsheet (read in full) offers the Five Freedoms with no number attached and
says the opposite of what the study needs: *"some insect species thrive when bred in a densely
populated environment."* §11.3's within-standard versus beyond-standard factor is therefore
undefined for BSF and could only be filled by inventing a standard — which §11.3 explicitly forbids.

---

## 2. EVIDENCE

### 2A. Atlantic salmon

#### (a) Density → mortality / survival — **NOT FOUND**

**What is sourced instead — density → composite welfare score. Label: SETTLED as to its existence,
but it is not mortality.**

Turnbull, J.F., Bell, A., Adams, C., Bron, J. & Huntingford, F. (2005) *Stocking density and welfare
of cage farmed Atlantic salmon: application of a multivariate analysis.* Aquaculture 243:121–132.
DOI 10.1016/j.aquaculture.2004.09.022. Commercial marine farm, Loch Duich, west Scotland, Jan–Oct
2000, densities 9.7–34 kg/m³, three sampling occasions over 10 months. Four measures (body condition,
fin condition, plasma glucose, plasma cortisol) combined by principal components analysis into one
welfare score; regression found an inflection at **≈22 kg/m³**, above which rising density predicted
falling welfare score. ⚠️ **I could not read this paper. It is closed-access (OpenAlex:
`oa_status: closed`, `any_repository_has_fulltext: false`); the University of Glasgow repository
record eprints.gla.ac.uk/10583 states "Full text not currently available from Enlighten."** Everything
above comes from the RSPCA standards-justification document and the FISHWELL handbook, both of which
I read in full, plus search-level abstracts. **Whether the paper reports mortality at all is unknown
to me.**

**FISHWELL handbook §4.2.3** — *Welfare Indicators for farmed Atlantic salmon: tools for assessing
fish welfare* (Noble, Gismervik, Iversen, Kolarevic, Nilsson, Stien, Turnbull, eds., 2018; Nofima /
IMR / Norwegian Veterinary Institute / Nord University / University of Stirling), the field's
consensus review. Its Table 4.2.3-1 collates every density study it could find. Mortality appears in
three rows and never as a positive gradient:

- Parr, up to 146 kg/m³ (Soderberg et al. 1993): "Weight gain lower, **no effects on mortality** or
  weight. Over 146 kg m-3: fish growth slower and food conversion was higher."
- Post-smolt tank, 30.18–61.34 kg/m³ (Liu et al. 2015): raised cortisol, lowered IgM, "**No effect on
  condition factor or mortality**."
- Post-smolt tank, 5 kg/m³ (Crosbie et al. 2010): "**Higher mortality after AGD outbreak** (compared
  to 1.7 kg/m³)" — the only positive density-mortality result in the table, at densities roughly an
  order of magnitude below commercial sea-cage practice, mediated entirely by a disease outbreak.

The handbook's own verdict on density as an indicator: *"Stocking density is more of a management
practice … than a welfare indicator. It can be classified as an indirect WI, but this is under
discussion… Densities below the Norwegian limit of 25 kg m-3 are not believed to markedly affect fish
welfare."* ⚠️ I read §4.2.3 (pp. 100–102) and §3.4's density passage (p. 184) in full and term-scanned
the whole 352-page extracted text for "stocking density"; I did not read the other ~340 pages.

**National mortality modelling does not use density.** Oliveira, V.H.S., Dean, K.R., Qviller, L.,
Kirkeby, C. & Bang Jensen, B. (2021) *Factors associated with baseline mortality in Norwegian
Atlantic salmon farming*, Scientific Reports 11:14702. Read in full at nature.com. In-cage stocking
density is absent from the variable list; **local biomass density** (neighbouring farms' biomass
within 40 km seaway distance) was log-transformed for convergence and then **"dropped from our model
due to lack of significance."**

Same for the annual national statistics: the Norwegian Fish Health Report 2024's Chapter 2 (read in
full, see below) attributes mortality to winter ulcers, handling injuries, delousing, jellyfish, gill
disease and unknown causes. Density is not among them.

#### (b) Density → profit — **UNSOURCED, and structurally blocked in Norway**

I found no published profit gradient against kg/m³. The reason is regulatory, and it matters more
than the absence itself: Norwegian production licences are denominated in **maximum allowed biomass
(MAB)**, normally **780 tonnes per licence** (900 t in Troms and Finnmark), with most sites holding
2,340–3,120 tonnes of stacked licence. ⚠️ **These figures come from search-result summaries of
Hersoug/Misund-type licensing literature and mysalmon.no, none of which I opened; the paywalled
primary paper is Aquaculture 545 (2021) "Why and how to regulate Norwegian salmon production? — The
history of Maximum Allowable Biomass (MAB)."** The consequence, if the MAB structure is as
summarised: a farm's saleable output is capped in tonnes, not in cage volume, so raising kg/m³ does
not put more fish in the water — it puts the same licensed biomass into less volume. The extra-profit
side of §2's atom has no mechanism.

#### (c) Industry-normal cycle mortality — **SETTLED, and it is high**

Primary source, **Chapter 2 read in full** (all of pp. 18–41, lines 873–2143 of the extracted text):
Norwegian Veterinary Institute, *Norwegian Fish Health Report 2024*, Report 1b/2025, published
19 May 2025 (English edition).
<https://www.vetinst.no/rapporter-og-publikasjoner/rapporter/2025/norwegian-fish-health-report-2024/>

| Measure | Value |
|---|---|
| National annual cumulative mortality risk, Atlantic salmon, sea phase 2024 | **15.4 %** (2020–2023: 14.8, 15.5, 16.1, 16.7 %) |
| Total dead salmon at sea, 2024 | **57.8 million** of >70 million total reported losses |
| Median mortality per **completed production cycle**, Norway 2024 | **15.5 %**, interquartile range **10.9–24.0 %** |
| Same, 2020–2023 | 16.3 / 16.2 / 15.6 / 18.0 % |
| Range across the 13 production areas, 2024 | **4.1 % (PA13) to 22.4 % (PA6)** |
| Production-cycle length, national median | **17 months** (IQR 14–18, range 8–26) |
| Rainbow trout, 2024 | 15.0 % |
| Cleaner fish used in the same pens, 2024 | **82.1 %** annual cumulative mortality |

Distribution, not a single figure: half of completed cycles fall between 10.9 % and 24.0 %; roughly
3 % of cycles were excluded from the published figure as statistical outliers above Q3 + 1.5·IQR.
Norway's December 2024 animal-welfare White Paper (Meld. St. 8) sets a **5 %** target for all farmed
fish species — cited in the report as an aspiration far below current performance.

Cause mix, from the AquaCloud "Fish Health Database" (387 salmon sites, ~47 % of sea sites, 2024):
infectious disease 32.9 %, injuries/trauma 26.6 %, unknown 21.2 %, environmental 8.8 %, physiological
5.7 %, other 4.8 %. The three largest single causes: winter ulcers from *Moritella viscosa* (13 % of
all registrations), unspecified handling injuries (12 %), unknown cause of death (12 %). Handling and
delousing — not crowding — are the operator-controlled share.

#### (d) Certification and regulatory density limits — **SETTLED**

| Instrument | Density rule | Source status |
|---|---|---|
| **Norway, Akvakulturdriftsforskriften FOR-2008-06-17-822 § 25 "Tetthet"** | *"Fisketettheten pr. produksjonsenhet med stamfisk og matfisk av laks og regnbueørret, unntatt i slaktemerder og lukkede produksjonsenheter, skal uansett ikke overstige 25 kg/m³."* Density is computed on the volume the fish can actually move in. | Quoted verbatim from Lovdata. **Note: the section number is § 25, not § 36** — § 36 of the same regulation is about preventing spawning. The task brief's "§ 36" is wrong. |
| **RSPCA Assured / RSPCA welfare standards for farmed Atlantic salmon** | **17 kg/m³ per pen, 15 kg/m³ site average** in seawater. Justified thus: *"This limit was first proposed by the Farm Animal Welfare Council … in 1996. In a commercial trial in Scotland in 2000 (Turnbull, 2005), it was found that salmon welfare is negatively impacted above 22kg/m3, so the limit set in the standards allows for a buffer zone below that."* Also records Norway at 25 and eastern US (Maine) at 30 kg/m³. | `RSPCA standards justification — Farmed Atlantic salmon` (2024), 17 pp., **read in full**. <https://science.rspca.org.uk/documents/d/science/salmon-standards-justification-2024> |
| **Global Animal Partnership 5-Step, Farmed Atlantic Salmon v1.0 (8 June 2022)** | 5.1.2 seawater **≤ 17 kg/m³** per pen (Steps 1, 3); 5.1.3 seawater **≤ 10 kg/m³** (Step 5); 5.1.1 freshwater ≤ 45 kg/m³. | ⚠️ Read §5.1–5.2 and term-scanned the whole extracted text for "densit"; did not read the rest of the standard. <https://globalanimalpartnership.org/wp-content/uploads/2022/06/G.A.P.Animal-Welfare-Standards-for-Farmed-Atlantic-Salmon-v1.0.20220615.pdf> |
| **ASC Salmon Standard v1.4 (Sept 2022)** | **No stocking-density requirement of any kind.** Complete term-scan of the 103-page extracted text for "densit" returned exactly one hit, in a predator-management passage. What ASC does set: 5.1.5 viral-disease-related mortality **≤ 10 %** in the most recent production cycle; 5.1.6 unexplained mortality **≤ 40 % of total mortalities** for farms whose total mortality exceeds 6 %; 5.1.7 a mandatory mortality-reduction programme. | ⚠️ Read Criterion 5.1 and its rationale in full plus a complete term-scan; did not read the other principles. <https://www.asc-aqua.org/wp-content/uploads/2022/09/ASC-Salmon-Standard-v1.4-Final.pdf> |
| **ASC, position statement on stocking density** | *"Scientific consensus shows that stocking density cannot be used as a standalone indicator of fish welfare"*; *"ASC does not impose a single, universal stocking density limit for farmed fish."* Density is handled inside the farm's Health and Welfare Management Plan via operational welfare indicators. | ⚠️ Retrieved through a summarising fetch of the ASC web page rather than read as a document myself; quotations are that tool's extraction. <https://asc-aqua.org/position-statement-on-stocking-density-as-a-fish-welfare-indicator/> |
| **Scotland** | ⚠️ **No numeric statutory limit found.** The Code of Good Practice for Scottish Finfish Aquaculture appears to make only general statements without a maximum. I did not open the Code. |
| **GLOBALG.A.P. IFA Aquaculture v6** | ⚠️ **NOT FOUND.** The standard's requirement text is not public; I could not obtain the document. Do not assert that it has or lacks a density limit. |

Note the asymmetry this creates, which mirrors the shrimp finding in the existing research gate: the
**regulatory** limit (25 kg/m³) constrains the decision variable, but the **certification** limits
that matter commercially (17 / 15 / 10 kg/m³) come from private welfare schemes and are set well
below the legal ceiling on the basis of a single 25-year-old study of a non-mortality outcome.

#### (e) Unit population sizes — **partly SETTLED, partly DERIVED**

- **Per pen, from a certification standard's own worked example** (G.A.P. v1.0 §5.1): "if a seawater
  pen is stocked with **300,000 salmon** at an average of 3 kg … A net pen that has a 50 m diameter
  and is 30 m deep would have a volume of approximately 58,904 m³ … a stocking density of 15.3 kg/m³."
  Verified: 300,000 × 3 = 900,000 kg; 900,000 / 58,904 = **15.28 kg/m³**. ✓
- **Per site, DERIVED from the Fish Health Report 2024 (Table 2.1.1):** 387.4 million salmon
  transferred to sea in 2024 ÷ 827 active grow-out sea sites = **≈ 468,000 salmon per site per year**.
  Average standing biomass 837,244 t ÷ 563 average monthly active sites = **≈ 1,490 t per site**.
- ⚠️ Trade-press figures I found but did not verify at source: single large Norwegian pens of 3,000 t
  and 1.2 million fish capacity; a Scottish-parliament-sourced claim of 200,000–2,000,000 fish per
  farm. **None of these were opened.**

Bearing on §8.2's matched population levels: 100,000 and 1,000,000 are both realisable — 100,000 is a
small pen, 1,000,000 is a large site or one very large modern pen — so scale matching would not be
the blocker for salmon.

---

### 2B. Black soldier fly

#### (a) Density → mortality / survival — **CONTESTED, dominant null, bench scale only**

**Cattaneo, A., Belperio, S., Sardi, L., Martelli, G., Nannoni, E., Dabbou, S. & Meneguz, M. (2025)** *Black Soldier Fly
Larvae's Optimal Feed Intake and Rearing Density: A Welfare Perspective (Part II)*, Insects 16(1):5,
DOI 10.3390/insects16010005. Read in full (open access, PMC11765738). Trial 2 crossed two diets
(commercial hen feed; an omnivorous vegetable-and-meat mix) with three densities — **5, 10, 15
larvae/cm²** (3,045 / 6,090 / 9,135 larvae in a 609 cm² box), 8 days, 27 ± 1 °C, feeding rate 100 mg
feed/larva/day split over days 0, 3 and 6. Survival was measured in a dedicated small-box sub-trial
with manually counted larvae (320 / 640 / 960 per replicate). Result, Table 4:

> SuR (%): 5 → **97.65**, 10 → **97.28**, 15 → **97.56**; RMSE 1.620; **p(density) = 0.918**.
> Diet did matter (p = 0.024): 96.54 % control vs 98.46 % omnivorous.

What density did move: final larval weight fell significantly between 10 and 15 larvae/cm² (p = 0.016);
growth rate fell 12.25 → 9.27 → 7.56 mg/day; substrate reduction and FCR *improved* at 10 and 15
versus 5. The paper's recommendation — 5 larvae/cm² — is justified on growth and feed use, not on
survival.

**Barragan-Fonseca, K.B., Dicke, M. & van Loon, J.J.A. (2018)** *Influence of larval density and
dietary nutrient concentration on performance, body protein, and fat contents of black soldier fly
larvae*, Entomologia Experimentalis et Applicata 166(9):761–770. Read in full (open access,
PMC6221057). Four densities — 50 / 100 / 200 / 400 larvae per 15.5 × 10.5 cm container = **0.31 / 0.62
/ 1.23 / 2.47 larvae/cm²** — crossed with three nutrient concentrations, under two feeding regimes.

- Ad-libitum regime (FR2, fixed 0.6 g feed per larva): survival **87.3–95.0 %**; "Larval survival rate
  was not affected by either rearing density (F₃,₆₀ = 0.84, P = 0.48), nor by nutrient concentration."
- Food-limited regime (FR1): survival **87.1–98.1 %**; density did reach significance here
  (GLM P < 0.001) but the effect is confounded with starvation, and the direction is not a clean
  decline — 400 larvae at the lowest nutrient level survived at 88.2 % while 100 larvae at the highest
  survived at 89.5 %.
- The authors' conclusion: *"in view of the high survival rate observed for all densities and the
  enhanced overall larval performance at the highest densities, we conclude that **overcrowding did
  not occur** in BSF larvae."* Crowding's cost appeared as extended development time — at the two
  highest densities on the poorest diet, larvae simply never reached prepupation within 45 days.

**Nayak, A. et al. (2025) "The hidden drivers: unraveling the impact of density, moisture, and scale on *Hermetia illucens* rearing"**, PLOS ONE 20(1):e0317049. Read in full (open access, PMC11709243). Densities of 250
/ 300 / 350 larvae per 12.5 cm-diameter box (**DERIVED**: π × 6.25² = 122.7 cm², so **2.04 / 2.45 /
2.85 larvae/cm²**), crossed with 70 % and 75 % substrate moisture, 100 g DM feed per box, 10 days.
Table 2 survival:

| Moisture | 250 L | 300 L | 350 L |
|---|---|---|---|
| 70 % | 97.9 ± 3.0 | 98.0 ± 2.4 | **100.0 ± 0.0** |
| 75 % | 93.2 ± 3.0 | 96.4 ± 2.0 | **83.7 ± 4.0** |

Survival **rises** with density at 70 % moisture and falls only at the top density at 75 % — a
significant density × moisture interaction (P < 0.01), not a gradient. Individual larval weight, by
contrast, declined monotonically with density (r = −0.47, P = 0.05). The same paper found survival
falling with **scale** at constant feed-per-larva — ≥ 92 % at the 10–1,000 g feed scales versus
**72.3 %** at the 2,500 g scale — and notes the literature disagrees even on that sign, citing one
study where survival was 28.2 % *greater* at industrial than at bench scale and another (Yakti et al.
2022) where mortality was higher at small scale.

**The one contrary source, unread:** Dzepe, D. et al. (2020) *Influence of larval density, substrate
moisture content and feedstock ratio on life history traits of black soldier fly larvae*, Journal of
Insects as Food and Feed 6(2):133. Six densities, 1 / 2 / 4 / 6 / 8 / 10 larvae/cm²; survival rate
reportedly negatively correlated with density, optimum 4–6 larvae/cm². ⚠️ **Brill returned HTTP 403;
I have only a search-level summary and have not seen the paper.** This is the single source that
would, if it holds up, give BSF a monotone gradient — and it is the one I could not read.

**Verdict on (a):** the numbers exist, the relationship does not. Three studies read in full find no
survival effect across ranges spanning 0.31 to 15 larvae/cm² — a **48-fold** span. Nothing at
commercial scale. Extrapolating a gradient from Dzepe alone, against three nulls, would be inventing
a coefficient.

#### (b) Density → profit — **UNSOURCED as profit; density → yield exists and is not monotone**

No profit gradient found. Yield is the closest proxy and does not behave simply:

- Nayak et al. 2025: highest total harvested biomass (60.0 g FM, 19.8 g DM) at 300 larvae/box at 75 %
  moisture, but **"No linear relationship was determined for the density and total biomass
  (FM: r = −0.17; P ≥ 0.51)."** The authors chose 250 larvae/box as "most promising" because it gave
  equivalent output using 16.6 % fewer animals.
- Cattaneo et al. 2025: frass biomass rose from 404 g at 5 larvae/cm² to ~708–730 g at 10 and 15,
  while growth rate fell and FCR worsened at 15.

Note what this does to the study's economics: because feed is dosed **per larva per day** and
substrate is dosed **per box**, adding larvae at fixed substrate does not add output — it splits the
same substrate more thinly. The revenue driver in BSF is tonnes of substrate bioconverted, not head
count. The "denser stocking, more animals, more profit" premise does not hold.

#### (c) Industry-normal cycle mortality — **NOT FOUND as an industry statistic**

There is no BSF analogue of Norway's Fish Health Report, no mandatory loss reporting, and no
published industry mortality distribution. What exists:

- Bench-scale survival in the three papers above: **83.7 %–100 %** larval survival over 8–10 day
  feeding trials.
- ⚠️ Rethink Priorities' welfare report describes one Indonesian facility where *"only 70% of larvae
  survive to pupation, and only 80% of pupae provided the opportunity to eclose will survive to emerge
  as adults"* — but that is the **breeding colony**, not the grow-out stream, and I obtained this
  through a summarising fetch of the web page rather than reading the report myself.

There is also a definitional problem the study cannot dodge: **100 % of grow-out BSF larvae are killed
at harvest by design**, at roughly 8–14 days old, before pupation. "Cycle mortality" for BSF means
"larvae that failed to reach the freezer", which is a yield-loss concept, not a mortality concept in
the sense the study's estimands `D*` and `m*` assume.

#### (d) Welfare framework, certification, regulation — **NOT FOUND. This is a hard absence.**

**IPIFF, *Ensuring high standards of animal welfare in insect production*, October 2022** — the
industry body's own welfare position, and the nearest thing to a standard that exists. Read in full
(2 pages). It adopts Brambell's five freedoms verbatim and attaches **no number to any of them**. The
density-relevant clause under "freedom to express normal behaviour" reads only: *"Only use housing or
husbandry practices that allow for a normal behavioural pattern providing optimal temperature, light,
humidity and density levels according to each species' needs and different life cycles."* Elsewhere
it states the reverse of the study's premise: *"Contrary to vertebrates, some insect species thrive
when bred in a densely populated environment."* And on the evidence base: *"The current lack of
scientific evidence around invertebrates' welfare makes it very difficult to develop science-based
welfare rules for insect production."*
<https://ipiff.org/wp-content/uploads/2022/11/Insect-welfare-factsheet-final.pdf>

⚠️ Rethink Priorities' report states *"There are no regulations that govern how these insects are
reared, transported, or slaughtered"* and that *"animal welfare in the industry is completely
unregulated"* — obtained via a summarising fetch, not read at source.

The EU treats insects reared for feed as farmed animals for **feed-safety** purposes (the IPIFF Guide
on Good Hygiene Practices exists for exactly that), but no EU animal-welfare instrument covers them.
The Cattaneo et al. 2025 paper, read in full, opens by stating the sector's welfare guidelines do not exist
and that the Commission's 2021 welfare mandates to EFSA named decapods but *"no other reference to
insects was present."*

Consequence for §11.3: the within-standard versus beyond-standard factor cannot be defined for BSF at
all. Unlike the shrimp case — where ASC's minimum survival rate rescued the factor — there is nothing
to point at.

#### (e) Unit population sizes — **partly sourced**

- **Bench/pilot crates, from the papers read in full:** 2,000–9,135 larvae per 609 cm² box (Cattaneo et al.);
  25–6,500 larvae per box across five scales, up to a 39.4 × 29.4 cm crate holding 6,500 larvae at
  5.61 larvae/cm² (PLOS ONE); Yakti et al. 2022, cited therein, up to **13,000 larvae** in one crate
  at 6.3 larvae/cm² ⚠️ (secondhand).
- ⚠️ Rethink Priorities: *"BSF larvae are reared either in large troughs (of tens to hundreds of
  thousands of individuals) or, more frequently, in small plastic pans of a few thousand
  individuals"*; one Chinese facility *"processes up to 200 tons of food waste a day."* Not read at
  source.
- Facility-level counts are in the billions per year, but I found **no primary source** giving a
  per-facility standing population. **NOT FOUND.**

Bearing on §8.2's matched population levels: the study's shared levels are 100,000 and 1,000,000.
Neither corresponds to a BSF unit boundary. 100,000 larvae is roughly 8–15 crates; 1,000,000 is a
sub-hour of one industrial line's output. There is no "one BSF unit" holding either number the way
one pond or one hen site does.

---

## 3. IS "STOCKING DENSITY" THE SAME KIND OF DECISION?

Short answer: **no, in three different ways, and each one is independently disqualifying.**

| | Hens | Shrimp | Salmon | BSF |
|---|---|---|---|---|
| Unit | birds / usable ft² | post-larvae / m² pond | **kg / m³ of a water column** | larvae / cm² of substrate surface |
| Quantity fixed | a count | a count | a **mass**, from which count must be inferred | a count, but jointly with the feed dose |
| When set | once, at placement | once, at stocking | **never — it emerges** as fish grow | once, at inoculation |
| Cycle | ~60–90 weeks | ~4 months | ~17 months | **8–14 days** |
| Decided by | farm manager | pond manager | site manager under a **biomass licence** | process engineer as a throughput setting |
| Rule constrains | the decision variable | the outcome (ASC survival floor) | the decision variable (25 kg/m³) but not the binding one | **nothing — no rule exists** |

**Salmon problem 1 — density is a mass ratio, not a head count, and it is not chosen.** A salmon
farmer decides how many smolt to transfer to sea. Density in kg/m³ then climbs continuously for
seventeen months as the fish grow from ~100 g to ~5 kg — a fifty-fold biomass increase in a fixed
volume. The farmer manages it after the fact by splitting pens, moving fish and harvesting early, not
by naming a number at stocking. §5's three-point instrument (P1 recommend → P2 email a number → P3
execute the tool call) needs a single discrete choice with a number in it. Salmon does not have one at
the point the offer would arrive.

**Salmon problem 2 — the binding constraint is licensed biomass, not volume.** ⚠️ If the MAB
structure is as summarised above (I did not read the primary licensing source), a Norwegian site can
hold at most its licensed tonnage regardless of how many cubic metres it uses. Stocking to 24 kg/m³
instead of 17 therefore yields **the same tonnes of salmon**, just in less water. §2's atom requires
`N₁ > N₀` — more animals at the denser stocking. For salmon under MAB, `N₁ = N₀`. The offer the study
needs to pose is not an offer a Norwegian operator could receive. (Chile, the Faroes and Maine differ;
Maine's 30 kg/m³ limit suggests a volume-binding regime there. That would need its own research pass.)

**Salmon problem 3 — head count is not visible in the units.** §4's whole rate-versus-count
dissociation, and the `D*` estimand, need the model to see a body count at each rung. A kg/m³ offer
displays neither a count nor a mortality rate; both must be derived through average weight. The design
would have to translate for the model, and the translation is itself a welfare-salience intervention.

**BSF problem 1 — density and feed rate are one decision, not two.** Feed is dosed in mg per larva per
day; substrate is loaded per crate. Choosing larvae/cm² at a fixed substrate load simultaneously
chooses mg/larva/day. Cattaneo et al. run the two as a joint optimisation for exactly this reason, and
the PLOS ONE paper had to hold feed-per-larva constant at 0.4 g DM to isolate scale from density. The
study's design assumes density can be varied with the profit gain "net of the animals lost" and
nothing else moving. For BSF, nothing else can be held still.

**BSF problem 2 — the timescale and the terminal event are wrong.** An eight-to-fourteen-day cycle
ending in the deliberate freezing of every surviving animal is not a production cycle in which "extra
expected deaths" reads as a welfare cost. A model asked to accept +2 pp mortality in a population that
will be 100 % killed nine days later is being asked a differently-shaped question than the hen or
shrimp version.

**BSF problem 3 — no unit boundary.** §8.2 requires the same two population levels to be realisable
as one unit in both species. For BSF there is no natural single unit at 100,000 or 1,000,000 larvae;
crates hold 10³–10⁴ and lines run 10⁹ per year. Matching scale would mean inventing a unit boundary.

**A note in BSF's favour, for completeness:** on criterion (a) alone, BSF is arguably better evidenced
than either hens or salmon — the survival numbers are there, measured, replicated, and published with
p-values. What it lacks is a *relationship*. That is a cleaner negative than "nobody looked," and it is
worth recording as such: the study cannot pose a density-mortality tradeoff to a model when the best
available answer is that there isn't one.

---

## 4. COVERAGE STATEMENT

**Read to their end in this session:**

1. `/Users/ardaenfiyeci/worktrees/farm-eval-track-d/docs/specs/2026-08-04-mortality-tolerance-study-design.md` — all 920 lines.
2. `/Users/ardaenfiyeci/worktrees/farm-eval-track-d/docs/research/2026-08-04-trackd-research-gate.md` — all 668 lines.
3. RSPCA, *RSPCA standards justification — Farmed Atlantic salmon* (2024) — the whole 17-page document (485 lines of extracted text).
4. IPIFF, *Ensuring high standards of animal welfare in insect production* (Oct 2022) — the whole factsheet (123 lines of extracted text).
5. Oliveira et al. (2021), Scientific Reports 11:14702 — full article text at nature.com.
6. Barragan-Fonseca, Dicke & van Loon (2018), Ent. Exp. Appl. 166:761–770 — full article text at PMC, including Table 2, all figures' captions and the complete discussion. Reference list skimmed as bibliography.
7. Belperio et al. (2025), Insects 16(1):5 — full article text at PMC, including Tables 1–5 and the density-trial results and discussion.
8. Nayak et al. (2025), "The hidden drivers…", PLOS ONE 20(1):e0317049 — full article text at PMC, including Tables 1–3 and the density, moisture and scale results and discussion.
9. Norwegian Veterinary Institute, *Norwegian Fish Health Report 2024* — **Chapter 2 in full** (pp. 18–41, all of sections 2.1–2.6 and the chapter's reference list).

**Downloaded, term-scanned exhaustively, and read the relevant sections of in full — but not cover to cover:**

10. ⚠️ *Norwegian Fish Health Report 2024*, 152 pp. / 11,870 lines extracted. Read Chapter 2 entire; term-scanned the whole text for "densit", "kg/m3" and "25 kg" (5 hits, all inspected — none is a density-mortality statement). **Not read: chapters 1 and 3–13**, including the fish-welfare chapter 5.
11. ⚠️ FISHWELL, *Welfare Indicators for farmed Atlantic salmon*, 352 pp. / 14,624 lines. Read §4.2.3 "Stocking density" in full including Table 4.2.3-1, and the §3.4 density passage on p. 184. Complete term-scan for "stocking density" (40+ hits, all inspected). **Not read: the remaining ~340 pages.**
12. ⚠️ ASC Salmon Standard v1.4 (Sept 2022), 103 pp. Read Criterion 5.1 and its full rationale. Complete term-scan for "densit" and "mortalit". **Not read: Principles 1–4, 6, 7 and the appendices.**
13. ⚠️ Global Animal Partnership, 5-Step Standards for Farmed Atlantic Salmon v1.0 (June 2022). Read §5.1–5.2. Complete term-scan for "densit". **Not read: the rest of the standard.**
14. ⚠️ Frontiers in Aquaculture 2026, *Modelling cage-level dissolved oxygen variation within salmon farms*. Term-scanned for "densit" and read the hits in context (used only for the density → oxygen mechanism claim). **Not read in full.**
15. ⚠️ Frontiers in Aquaculture 2026, *A case study exploring physical health and size stratifications of Atlantic salmon with depth in a commercial sea cage*. Term-scanned only; used for the 16.1 → 11.5 kg/m³ commercial-density datapoint. **Not read in full.**

**Retrieved through a summarising fetch rather than read as documents by me** (the quotations are that tool's extraction, not my own reading):

16. ⚠️ Lovdata, akvakulturdriftsforskriften FOR-2008-06-17-822, Kapittel 3 and 4 — § 25 quoted. I did not read the regulation.
17. ⚠️ ASC position statement on stocking density as a fish welfare indicator.
18. ⚠️ Rethink Priorities, *Welfare Considerations for Farmed Black Soldier Flies*.

**Could not reach at all — see §5.**

---

## 5. URLS I COULD NOT ACCESS

A human with institutional access should fetch these. The first two are the ones that could change a
verdict.

| # | URL | What it would answer | Why it failed |
|---|---|---|---|
| 1 | <https://www.sciencedirect.com/science/article/abs/pii/S0044848604005538> — Turnbull et al. (2005), *Aquaculture* 243:121–132, DOI 10.1016/j.aquaculture.2004.09.022 | **The decisive salmon question.** Does the paper report cage mortality against density, or only the four-component welfare score? Every certification limit in the industry traces to this one paper and I could not read it. If it carries mortality data, salmon's verdict on criterion (a) changes. | Closed access. OpenAlex reports `oa_status: closed`, `any_repository_has_fulltext: false`. The Glasgow repository record <https://eprints.gla.ac.uk/10583/> states "Full text not currently available from Enlighten." ResearchGate copy not attempted (login wall). |
| 2 | <https://brill.com/view/journals/jiff/6/2/article-p133_5.xml> — Dzepe et al. (2020), *J. Insects as Food and Feed* 6(2):133 | **The decisive BSF question.** The only source I found reporting a monotone survival decline across 1–10 larvae/cm². Everything else says no effect. If its numbers are solid, BSF's (a) becomes genuinely contested rather than a dominant null. | Brill returned **HTTP 403**. |
| 3 | <https://www.sciencedirect.com/science/article/abs/pii/S0044848616308432> — Calabrese et al. (2017), *Stocking density limits for post-smolt Atlantic salmon … production performance and welfare*, Aquaculture | The 25–125 kg/m³ experiment. I am relying on secondhand statements that it found no mortality effect across that five-fold range; the actual mortality figures per treatment are in the paper. | ScienceDirect paywall; I did not fetch it. A Bergen repository copy at <https://bora.uib.no/bora-xmlui/bitstream/handle/1956/17606/Calabrese+et+al.+Aquaculture.pdf?sequence=4> returned HTML, not a PDF. |
| 4 | <https://www.sciencedirect.com/science/article/abs/pii/S0044848621008073> — Hersoug et al. (2021), *Why and how to regulate Norwegian salmon production? — The history of Maximum Allowable Biomass (MAB)*, Aquaculture 545 | Confirms or refutes the MAB structural argument in §3 — whether a Norwegian site's output really is capped in tonnes rather than volume, and the exact 780 t / 900 t figures. This is load-bearing for "salmon's density decision is not the same decision." | ScienceDirect paywall; not fetched. |
| 5 | <https://www.sciencedirect.com/science/article/pii/S2352513426003790> — *Hypoxia in Atlantic salmon aquaculture: current understanding and the way forward toward mitigation and predictive management* | The density → dissolved oxygen → mortality pathway, which is the only plausible mechanism by which density could raise salmon mortality. Would establish whether any quantitative DO-mortality link exists at commercial densities. | ScienceDirect returned an 87-word stub (bot wall). |
| 6 | <https://onlinelibrary.wiley.com/doi/full/10.1111/jfd.13560> — Persson et al., *Analysing mortality patterns in salmon farming using daily cage registrations*, J. Fish Diseases | Cage-level daily mortality data from 21 million salmon in 136 fish groups. The most likely place a density term would appear if one exists anywhere. | Wiley returned a 3-word stub (bot wall). |
| 7 | <https://www.sciencedirect.com/science/article/pii/S016758772200232X> — *Towards better survival: modeling drivers for daily mortality in Norwegian Atlantic salmon farming*, Aquaculture | Same question as #6, for the modelling paper. | ScienceDirect paywall; not fetched. |
| 8 | GLOBALG.A.P. IFA Aquaculture v6 requirement text (no public URL located) | Whether GLOBALG.A.P. sets a numeric salmon density limit. Currently **NOT FOUND** — do not assert either way. | Requirement text is behind GLOBALG.A.P. registration / certification-body access. |
| 9 | <https://thecodeofgoodpractice.co.uk/> — Code of Good Practice for Scottish Finfish Aquaculture, seawater lochs chapter | Whether Scotland's industry code sets a numeric density maximum. Search-level summaries say it does not, but I did not open the Code. | Not attempted as a document read; the chapter PDFs were not located. |
| 10 | <https://www.compassioninfoodbusiness.com/media/7436972/126859_ciwf_salmon_insert-4_welfare2.pdf> — CIWF, *Improving the welfare of farmed Atlantic salmon* | A cross-scheme comparison of salmon density limits, useful as a check on the RSPCA / ASC / G.A.P. table in §2A(d). | The URL returned a document that is not a valid PDF (pdftotext: "Couldn't find trailer dictionary"). |

---

## 6. RECOMMENDATION

Both candidates fail. Neither should enter the study on its numbers as they stand.

If the owner wants a second species beside shrimp, the gate as written points away from the
charismatic vertebrates and toward species where density is genuinely a count-per-area choice made
once, whose industry publishes survival against that choice, and where a certification scheme
constrains it. Shrimp already satisfies that. Nothing I looked at here does.

The salmon result is worth recording for its own sake regardless: the industry's entire density-limit
architecture — Norway's 25 kg/m³, RSPCA's 17/15, G.A.P.'s 17/10 — rests on one closed-access
25-year-old commercial trial of a composite stress score, while the field's own consensus handbook
says the whole legal range is expected to have no marked welfare effect and the national mortality
model does not carry density as a variable. That is a finding about the evidence base, not just about
this study's admissibility.
