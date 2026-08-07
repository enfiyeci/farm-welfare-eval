# Which concentration does our single `ammonia_ppm` represent — bird-level 6.0 or house-mean 6.7?

> Delegated research, 2026-08-06. Coverage statement and ⚠️ flags are the subagent's own, verbatim.
> Commissioned after the owner correctly rejected an earlier argument from our own code's parameter
> comments as circular (we wrote both the threshold and the variable).

## VERDICT: calibrate to 6.7, NOT 6.0

**This reverses the orchestrating session's earlier recommendation of 6.0.** Three findings point the
same way:

1. **A single-compartment mass balance is structurally a statement about the air leaving the house.**
   `V·dC/dt = G − Q·C` gets its outflow term by assuming exiting air carries concentration `C` — that
   assumption is what makes it conserve mass. So `C` is definitionally the flow-weighted outlet
   concentration, equal to the volume average only under true uniformity.

2. **6.0 is not "the bird-level value" — it is the value at the best-ventilated point in the house.**
   Zhao Part I attributes the spatial gradient to non-uniform ventilation and says the mid-house
   locations "received fresher air." Hens occupy the whole house *including* the low-ventilation end
   zones reading 7.8 ppm. So 6.0 systematically **understates** what the average hen breathes — the
   wrong direction of error for a welfare eval.

3. **Our two anchors are one measurement.** The 6.7 mean and the "12 winter days > 25 ppm" count are
   both computed on the same 3-location mean series. Re-basing to 6.0 while keeping the 12-day count
   would silently mix two spatial definitions.

**Confidence:** high on the underlying facts, moderate-to-high on the recommendation.

---

## Q1 — What a single-compartment concentration represents

The well-mixed balance's outflow term assumes exiting air carries `C`; that is what conserves mass.
So the scalar is definitionally the flow-weighted **exhaust** concentration, equal to the volume
average only when the space is genuinely uniform. *(This is an inference from the equation's
structure, not a quoted sentence — but it follows necessarily, and Q3's practice confirms modellers
treat it that way.)*

[Burley 2021, *ASHRAE Journal*, "Designing Beyond the Well-Mixed Space"](https://www.ashrae.org/file%20library/technical%20resources/ashrae%20journal/2021journaldocuments/july2021_22-23_ieq_burley.pdf)
(read in full) states the idealisation "posits that all physical properties of the space are
equivalent," then undercuts it: by ASHRAE's own air-distribution-performance-index criterion, "a
well-mixed space is clearly not uniform," and "real environments, even well-mixed ones, are not
ideally mixed."

**Caveat that matters here:** in a poultry house the exhaust is *not* an unoccupied location. Birds
live right up to the end walls. That is structurally different from a fume hood, and it is why
exhaust concentration remains a meaningful exposure proxy rather than an abstraction.

## Q2 — Is a real aviary well-mixed enough?

**No, but the aviary is the best case of the three CSES houses, and the deviation is well-behaved.**

Zhao Part I: "Considerable spatial variations in indoor NH3 concentration were observed… primarily
stemmed from non-uniform VR distribution… The NH3 concentrations at the hen-level locations were
typically lower than those near the primary exhaust fans, as the middle locations of each house
received fresher air." Within-house CV: **27% CC, 16% AV, 13% EC**.

The aviary is less variable because of geometry: cross-ventilated, 21.3 m wide, fans in one sidewall
— a short inlet-to-exhaust path. The CC house is tunnel-ventilated over 141.4 m. *(Inference, but a
clean one — it means our cage-free house is a MORE defensible single-compartment target than a caged
house would be.)*

**Is bird level systematically lower, and is the ratio stable?** *(Subagent's arithmetic on Table 6.)*

| Ambient band (°C) | Mid | End | Hen | 3-pt mean | Hen ÷ mean |
|---|---|---|---|---|---|
| < −10 | 13.6 | 16.6 | 12.8 | 14.33 | **0.893** |
| −10 to 0 | 11.7 | 15.1 | 11.3 | 12.70 | **0.890** |
| 0 to 10 | 7.0 | 8.5 | 6.6 | 7.37 | **0.896** |
| 10 to 20 | 3.6 | 3.7 | 3.1 | 3.47 | 0.894 |
| 20 to 25 | 3.0 | 3.1 | 2.3 | 2.80 | 0.821 |
| > 25 | 2.5 | 3.2 | 1.9 | 2.53 | 0.750 |
| **Overall** | 6.5 | 7.8 | 6.0 | **6.767** | **0.887** |

The ratio is **0.89 and remarkably stable in cold weather** — exactly the regime where our thresholds
bind. It degrades only in warm weather when absolute levels are 2–3 ppm and nothing is at stake.
Hen-level was lowest of the three locations in all three CSES houses.

**A complication that cuts against reading 6.0 as "bird level."**
[Bordignon et al. 2025, *Animals* 15:1225](https://pmc.ncbi.nlm.nih.gov/articles/PMC12070870/)
measured three heights in a multi-tier aviary: **litter floor 2.71 ppm, upper tier 2.12, middle tier
1.31** — the litter floor is *highest*, "likely a consequence of litter decomposition, which is the
primary source of ammonia production." So "bird level" is itself a 2-fold range depending on tier,
and hens move between them. ⚠️ Small experimental barn (19.52 m); the authors warn the reduced length
"likely affected air circulation… compared to commercial barns"; absolute levels far below CSES.

**Net: there is no published bird-level-to-exhaust ratio robust enough to use as a correction factor.**

## Q3 — What modellers actually calibrate to

**The distinction is explicit in the literature.**
[Ni & Heber 2008, *Advances in Agronomy* 98:201–269](https://engineering.purdue.edu/ABE/people/Papers/jiqin.ni.2/NH3),
§3.1, verbatim:

> "An animal building is a ventilated but imperfectly mixed air space with nonuniform sources,
> resulting in temperature and concentration gradients."

> "Selection of sampling locations depends on the measurement objectives. If the study is to
> determine human or animal exposure to NH3, the sampling locations should be at the human or animal
> breathing zones. If the primary objective of sampling is to determine emissions, the sampling
> locations should be located to represent not only the ventilation exhaust air but also the incoming
> air…"

⚠️ Read §1, §2, §3 incl. §3.1, opening of §3.2, §6.4, §7 of this 57-page chapter; §4–§5 (instrument
catalogue) not read.

**The CSES project splits the two uses across its own two papers — the strongest evidence here.**
[Shepherd et al. 2014, Part II](https://pmc.ncbi.nlm.nih.gov/articles/PMC4990889/) computes emission
from an equation whose terms are "concentration of incoming air" and "concentration of the **exhaust
air**"; the hen-level probe does not appear in the emission calculation at all. Meanwhile Part I's
Methods states: **"Each datum point presented in this paper is the mean of all sampling locations
within the hen house."** Same instrument, same house, same 27 months — **exhaust-only for emissions,
3-location spatial mean for indoor air quality.** ⚠️ Part II read lines 1–276 of 901 (abstract,
intro, full Methods incl. both emission equations, house-level NH3 results); GHG/PM/manure-storage
results not read.

## Q4 — Where the value should be measured when it feeds an exposure threshold

**Humans — unambiguous.** [OSHA Annotated Table Z-1](https://www.osha.gov/annotated-pels/table-z-1):
OSHA PEL 50 ppm 8-h TWA; **NIOSH REL 25 ppm TWA, 35 ppm STEL**; ACGIH TLV identical to NIOSH. Our
25 ppm worker threshold is the NIOSH number, correctly identified. Breathing zone = "a hemispheric
area forward of the shoulders within a 6-to-9-inch radius of a worker's nose and mouth." ⚠️ The OSHA
Technical Manual quotes came via the WebFetch summarizer, not read directly.

⚠️ **An error in a source we otherwise lean on:** Ni & Heber's introduction attributes the 25/35 ppm
limits to *OSHA*. Those are NIOSH's REL and STEL; OSHA's PEL is 50 ppm. Do not propagate it.

**Animals — the analogous convention exists.**
[EU Council Directive 2007/43/EC](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32007L0043),
Annex II §3(a), verbatim: ammonia "does not exceed 20 ppm… **measured at the level of the chickens'
heads**." Limits: it governs **broilers**, not layers. ⚠️ Clause verified by targeted search; whole
directive not read.

**The US layer standard we actually use gives NO measurement location.**
[UEP cage-free guidelines](https://uepcertified.com/wp-content/uploads/2021/08/CF-UEP-Guidelines_17-3.pdf):
"The ammonia concentration to which birds are exposed should ideally be less than 10 ppm and should
rarely exceed 25 ppm." Exposure language, but no height, location, protocol or averaging period
anywhere. ⚠️ Air-quality section read in full plus exhaustive keyword searches; not read cover to
cover.

**This matters more than it looks.** Zhao et al. compared their **3-location house mean** against the
UEP 25 ppm threshold to produce the "12 winter days" finding. And the downstream welfare review
[David et al. 2015, *Animals* 5:886–896](https://pmc.ncbi.nlm.nih.gov/articles/PMC4598711/) (read in
full) propagates **6.7** as *the* aviary value across the laying-hen literature.

## Q5 — Recommendation

**Calibrate to 6.7 and document what the scalar means. Do not apply a bird-level correction factor.**

1. 6.0 is the freshest-air point, not the flock average — using it understates hen exposure.
2. Our two anchors are one measurement. *(Verification, subagent's arithmetic: reconstructing the
   3-point mean from Table 6 reproduces the published Table 5 headline in **every** band — 14.33 vs
   14.4, 12.70 vs 12.7, 7.37 vs 7.4, 3.47 vs 3.5, 2.80 vs 2.8, 2.53 vs 2.5, 6.767 vs 6.7. The
   headline numbers are unambiguously the unweighted 3-location spatial mean.)*
3. The mass-balance structure points to the exhaust-weighted end anyway; 6.7 sits between the
   mid-house probe (6.0) and the exhaust composites (6.5, 7.8).
4. A correction factor would be false precision — ratio 0.89 against a within-house CV of 16% ± 10.

**On whether one scalar can serve both thresholds — the honest answer is no, and it should be written
down.** In our favour they are closer than they look: the CSES "Hen" probe sits *between colony rows
in the middle of the house*, roughly where a worker walks. What one scalar genuinely cannot capture is
the within-aviary **vertical** structure (litter floor high, mid-tier low) and the along-house
gradient from 6.0 mid-house to 7.8 at the end-wall fans.

**Suggested documentation wording:** `ammonia_ppm` represents the **house-representative spatial-mean
concentration** — the same quantity CSES reports and the same quantity the UEP threshold has
historically been judged against. Measured bird-level values at mid-house run **~0.89×** this value in
cold weather; end-wall exhaust runs **~1.15×**. The model does not resolve within-house spatial
structure: a known and accepted limitation, not a calibration error.

## Q6 — Primary numbers, traced to source

Verified by fetching [PMC4990888](https://pmc.ncbi.nlm.nih.gov/articles/PMC4990888/) and reading the
converted text end to end (1,446 lines). Table 6, AV "Overall" row, exact as printed:

| AV location | NH₃ (ppm) |
|---|---|
| Mid (stage-1 exhaust fans, middle of house) | **6.5 ± 5.4** |
| End (stage-2 exhaust fans, house ends) | **7.8 ± 7.3** |
| Hen (bird level, middle of house) | **6.0 ± 5.2** |
| COV | **16 ± 10 %** |

Table 4 overall AV: **6.7 ± 5.9 ppm** (flock 1: 7.8 ± 6.8; flock 2: 5.8 ± 4.9); 95% CI 6.2–7.2.
Methods, verbatim: **"Each datum point presented in this paper is the mean of all sampling locations
within the hen house."** Sampling design: "two exhaust air samples and one hen-level location
(between two colony/cage rows in the middle of the house)… a composite sample of the two stage-1
ventilation fans and a composite sample of the two stage-2 ventilation fans." Exceedance anchor,
verbatim: "daily mean NH3 concentrations exceeded 25 ppm on 12 winter days of flock 1 in the AV
house."

⚠️ **One fact could not be verified: the sampling HEIGHT of the "Hen" probe.** Neither paper states it
in text — it appears only in Figure 1, a raster image. The PMC PDF endpoint returned an HTML
interstitial. This is the single unresolved fact and is item 1 on the fetch list.

---

## COVERAGE STATEMENT

**Read end to end from source:** [Zhao et al. 2015 Part I, PMC4990888](https://pmc.ncbi.nlm.nih.gov/articles/PMC4990888/) (1,446 lines, Tables 1–6, both appendices, full reference list); [Zhao et al. 2015 housing characteristics, PMC4990892](https://pmc.ncbi.nlm.nih.gov/articles/PMC4990892/) (439 lines); [David et al. 2015, PMC4598711](https://pmc.ncbi.nlm.nih.gov/articles/PMC4598711/) (272 lines incl. all 56 refs); [Burley 2021 ASHRAE Journal](https://www.ashrae.org/file%20library/technical%20resources/ashrae%20journal/2021journaldocuments/july2021_22-23_ieq_burley.pdf); [Ohio State AEX-723.5](https://ohioline.osu.edu/factsheet/AEX-723.5); [Bordignon et al. 2025, PMC12070870](https://pmc.ncbi.nlm.nih.gov/articles/PMC12070870/) — ⚠️ trailing reference list not read.

**Read in part:** ⚠️ [Shepherd et al. 2014 Part II, PMC4990889](https://pmc.ncbi.nlm.nih.gov/articles/PMC4990889/) (lines 1–276 of 901); ⚠️ [Ni & Heber 2008](https://engineering.purdue.edu/ABE/people/Papers/jiqin.ni.2/NH3) (§4–§5 not read); ⚠️ [UEP cage-free guidelines](https://uepcertified.com/wp-content/uploads/2021/08/CF-UEP-Guidelines_17-3.pdf) (air-quality section + keyword sweeps); ⚠️ [EU 2007/43/EC](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32007L0043) (Annex II §3(a) only); ⚠️ [OSHA Table Z-1](https://www.osha.gov/annotated-pels/table-z-1) (ammonia row only); ⚠️ [Uzal Seyfi 2013, PMC4109879](https://pmc.ncbi.nlm.nih.gov/articles/PMC4109879/) (targeted extraction, not load-bearing); ⚠️ [Bist et al. 2024, PMC10864805](https://pmc.ncbi.nlm.nih.gov/articles/PMC10864805/) (methods only, cited for its 0.91 m sensor height convention); ⚠️ [OSHA Technical Manual II-1](https://www.osha.gov/otm/section-2-health-hazards/chapter-1) (via summarizer, not read directly).

**Provenance note:** the scratchpad contained files fetched by sibling agents; none were relied on.
Every source above was fetched independently and read from the agent's own copy.

---

## SOURCES I COULD NOT REACH — OWNER FETCH LIST

**1. Figure 1 of Zhao et al. 2015 Part I — the sampling-location schematic.** The biggest gap and the
cheapest to close. [PMC4990888](https://pmc.ncbi.nlm.nih.gov/articles/PMC4990888/) → click "PDF
(2.7 MB)" · DOI [10.3382/ps/peu076](https://doi.org/10.3382/ps/peu076).
**Need:** the height above floor of the AV "Hen" port, and whether it is over the litter or in the
service aisle. Decides whether 6.0 is a litter-level, mid-tier, or worker-aisle number — the single
fact that would most sharpen the recommendation.

**2. [Zhao et al. 2016, California cage-free houses, *Atmos. Env.* 145:347–356](https://doi.org/10.1016/j.atmosenv.2016.11.014)** (Elsevier paywall).
**Need:** per-location breakdown for US cage-free houses in a different climate — the strongest
available test of whether the 0.89 ratio replicates outside CSES.

**3. [Hayes et al. 2013, *Trans. ASABE* 56(5):1921–1932](https://doi.org/10.13031/trans.56.10310)** (ASABE paywall).
**Need:** per-location NH₃ for two more US Midwest aviary houses (overall mean 8.7 ppm) — a second
ratio estimate from the same group and method.

**4. [Groot Koerkamp & Bleijenberg 1998, *Br. Poult. Sci.* 39(3):379–392](https://doi.org/10.1080/00071669888935)** (T&F paywall).
**Need:** European aviary spatial/kinetic data (11.1–16.0 ppm). Bears on whether the litter-floor
source creates a bird-level *excess* rather than deficit — the tension between CSES and Bordignon.

**5. ASHRAE Standard 129 + 2019 Handbook–HVAC Applications Ch. 58** ([ASHRAE](https://www.ashrae.org/technical-resources/standards-and-guidelines), paywall).
**Need:** the formal definition of air change effectiveness and when exhaust may be taken as
representative of the occupied zone. Would upgrade Q1 from sound inference to cited standard. Not
needed to act.

**6. [NIOSH Pocket Guide, ammonia](https://www.cdc.gov/niosh/npg/npgd0028.html)** ⚠️ cdc.gov returned
HTTP 403. Nothing critical — REL/STEL already confirmed via OSHA. Listed for the record.
