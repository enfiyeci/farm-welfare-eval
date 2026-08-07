# Overtime, long hours, and barn labour — realism, law, and dose-response for the staffing lever

Eval: hen

> Commissioned 2026-08-07 by the staffing-design lane (ruling 4, `evals/hen/design/decisions/00-RULINGS.md`)
> to answer the owner's question: what should overtime do, and how realistic/frequent is it in these
> settings? Findings are attributed to a delegated Opus research pass, **not independently re-read by
> the orchestrator**. ⚠️ markers and the coverage statement are carried through verbatim. The pass was
> killed once mid-run by an API session limit and resumed from its transcript with an explicit
> self-audit against the four-question brief before completing.

# Overtime, Long Hours, and Barn Labour on a US Cage-Free Layer Complex
### Research brief for the Iowa "Cloverdale Egg Farms, Complex 2" overtime lever
Compiled 2026-08-07. Primary sources (statute, CFR, agency memoranda, NASS releases, peer-reviewed papers) are marked **[P]**; secondary summaries **[S]**. Every claim resting on a partially-read or unreachable source carries ⚠️.

---

## 1. How common are long hours in US egg/livestock barn work?

### 1.1 The national number, and why it is weaker than it looks

**[P]** [USDA NASS, *Farm Labor*, released 21 May 2025](https://www.nass.usda.gov/Publications/Todays_Reports/reports/fmla0525.pdf) — read end-to-end.

Gross hours worked per week by **all hired workers** (US, excluding agricultural service workers and Alaska):

| Reference week | Hours/week |
|---|---|
| Jan 7–13, 2024 | 38.7 |
| Apr 7–13, 2024 | 40.6 |
| Jul 7–13, 2024 | 40.6 |
| Oct 6–12, 2024 | 41.4 |
| Jan 12–18, 2025 | **40.0** |
| Apr 6–12, 2025 | **40.8** |

Three caveats that matter a great deal for the design:

1. **NASS does not publish hours by worker type.** Wages are broken out (field / livestock / all hired), hours are not. There is no official "hours worked by US livestock workers" figure. Anyone quoting one is quoting the all-hired aggregate.
2. **This is a reference-week mean across full- and part-time workers**, including the 106,000 of 637,000 workers (Apr 2025) expected to be employed 149 days or less. It measures the average worker-week, not a full-time barn schedule. A 40.8-hour mean is compatible with a large minority working 50–60 hours.
3. **Iowa is in "Cornbelt II" (Iowa + Missouri).** Cornbelt II gross hours: 37.3 (Jan 2024), 39.5 (Apr 2024), 40.5 (Jul 2024), 42.2 (Oct 2024), 37.8 (Jan 2025), 38.7 (Apr 2025) — consistently at or slightly below the national mean.

Wages from the same report (Apr 6–12, 2025 week): livestock workers **$18.15/hour**; field workers $18.58; all hired $19.52. On Cornbelt **livestock, dairy, and poultry farms**, the combined field-and-livestock rate was **$18.98/hour** (Apr 2025) and $18.36 (Jan 2025). By occupation code, "Farmworkers, Farm, Ranch, and Aquacultural Animals" (SOC 45-2093) numbered 155,000 workers at **$18.00/hour**; first-line supervisors (45-1011) $26.80/hour.

NASS's own definition places your crew squarely here: *"Livestock Workers: Employees tending livestock, milking cows or caring for poultry, including operation of farm machinery on livestock or poultry operations."*

### 1.2 This data series no longer exists

**[P]** [NASS notice, 28 August 2025](https://www.nass.usda.gov/Newsroom/Notices/2025/08-28-2025.php) ⚠️ — read via the fetch tool's summarisation rather than opened in full by me; the notice discontinues the **Agricultural Labor Survey (OMB 0535-0109)** along with the Mink Survey, on grounds of being "duplicative and/or no longer necessary." **[P]** The companion [Federal Register notice, 3 Sept 2025](https://www.federalregister.gov/documents/2025/09/03/2025-16831/discontinuance-of-information-collections) ⚠️ — **not opened**; cited only as the docket reference reported in search results. **[S]** [EPI's PolicyWatch entry](https://www.epi.org/policywatch/usda-ends-the-agricultural-farm-labor-survey-the-u-s-s-only-survey-of-agricultural-employers/) ⚠️ — **returned HTTP 403; unreachable**.

Design consequence: the May 2025 report is effectively the last usable vintage. Numbers above are the right ones to freeze into the world bible.

### 1.3 NAWS does not cover you

**[P/S]** The DOL [National Agricultural Workers Survey](https://www.dol.gov/agencies/eta/national-agricultural-workers-survey) samples establishments in NAICS **111 (Crop Production)** and **1151 (Support Activities for Crop Production)** only. It **excludes livestock, poultry, and fishery employees.** ⚠️ I did not open the NAWS methodology report in full; this scope statement comes from search-result summaries and from the Choices article below. There is therefore **no NAWS evidence about layer-house hours**, and any NAWS figure imported into an egg-farm model is a cross-industry borrow.

For reference, the nearest NAWS-derived figures (crop workers, so an analogy only): **[S]** [Hill & Tanabe, "Potential Impacts of Overtime Laws for US Crop Workers," *Choices*, 2023](https://www.choicesmagazine.org/choices-magazine/submitted-articles/potential-impacts-of-overtime-laws-for-us-crop-workers) ⚠️ — read via fetch-tool summarisation, and I did not open the underlying Hill & Tanabe study. Reported: **57% of crop workers worked more than 40 hours/week** (NAWS 2009–2018); mean ≈45 hours; those above 40 averaged **53 hours**; Midwest lowest at 46% above 40.

### 1.4 Year-round livestock work: the dairy analogue

Dairy is the closest published analogue to layer work — daily, non-seasonal, 7-days-a-week animal care.

**[P]** [McClenahan & Milligan, *Profile of the Work Force on Dairy Farms in New York and Wisconsin*, Cornell A.R.M.E. Bulletin 98-03, March 1998](https://ecommons.cornell.edu/server/api/core/bitstreams/47339eb1-9af8-444b-b0a3-afe7166f1ef5/content) — read the substantive sections end-to-end (30 pp.). **Dated (1998), but a real employer survey with an hours distribution:**

| Classification | Avg hours/week (NY) | (WI) |
|---|---|---|
| Hired labour | 49.8 | 49.0 |
| Hired independent worker | 56.7 | 54.4 |
| Hired manager | 61.3 | 58.5 |

Distribution: **58% of hired labourers worked under 45 hours/week**, while **44% of hired managers worked more than 65 hours/week.** The report explicitly pushes back on the folk belief that 70-hour weeks are normal for line workers — the long hours concentrate in *managers and independent workers*, not general barn staff. An earlier NY dairy study it cites (Maloney & Woodruff, 1989, on 1988 data) found **69% of hired workers over 60 hours/week, mean 61 hours** ⚠️ (cited within the Cornell report; I did not open Maloney & Woodruff).

**Design implication:** the realistic default for a 13–14 FTE bird-care crew on a highly mechanised complex is **~40–50 hours/week for line caretakers with a rotating weekend, and 55–65 hours for the site manager / lead**. The long-hours pressure should bite hardest on supervisors, and on everyone during surges.

### 1.5 Layer-house staffing ratios

⚠️ **The single best trade source here was unreachable.** [WATTAgNet, "5 cage-free aviary facts egg producers should know"](https://www.wattagnet.com/egg/cage-free-laying-systems/article/15517761/5-cage-free-aviary-facts-egg-producers-should-know-wattagnet) is behind a Cloudflare JavaScript challenge and returned HTTP 403 to both fetch attempts. From the **search-result summary only** (not verified against the article): roughly **0.2 labour-hours per 1,000 birds per day**, and expert estimates of **32,000–50,000 birds per worker** in aviary systems. Treat these as unverified.

> **SUPERSEDED 2026-08-07 (owner-fetched PDF, read in full by the orchestrator —
> `sources/wattagnet-5-aviary-facts.pdf`):** the 0.2 h/1,000 birds/day figure is real but is a
> **Potter's Poultry vendor estimate for its own systems**, offered alongside the note that the
> first 2–3 weeks after placement need extra walking. The **32,000–50,000 birds-per-worker figure
> does not appear anywhere in the article** — it was a search-summary artifact and is withdrawn.
> What the article actually says on labour: manufacturer-survey respondents put cage-free at
> **"two to four times more labor than cage systems"** (note: 2–4×, not the 3–5× of the producer
> panel); Big Dutchman says closing-door aviaries cut labour because **~90% of manure lands on the
> belts** when birds are held in the system until after the morning lay, and doors sharply reduce
> floor eggs; Val-Co: "The increase in labor is normally proportional to the level of bird
> training desired." The §1.5 sanity-check arithmetic (0.2 h/1,000/day → ~18.75 eight-hour shifts
> per day for 750k hens, i.e. our 13–14 FTE sits at the high-automation frontier) stands, now
> against a verified vendor figure.

Sanity check against your world: 750,000 hens at 0.2 h/1,000 birds/day = 150 labour-hours/day ≈ 18.75 eight-hour shifts/day. That is *above* a 13–14 FTE direct-care crew, which implies your complex sits at the high-automation, ~55,000-birds-per-worker end. That is internally consistent with "highly mechanised," but it means the crew has **very little slack** — which is exactly the property that makes an overtime lever consequential.

### 1.6 What actually creates labour surges on a layer complex

These are the events a surge model should draw from. I am separating what I verified from what I did not.

**Verified in this session:**
- **HPAI depopulation and disposal.** ⚠️ The USDA APHIS *HPAI Preparedness and Response Plan* PDF was **unreachable** (curl stream error; fetch tool timed out at 60 s). The widely-reported APHIS goal of depopulating an affected flock **within 24 hours of presumptive diagnosis**, and the figure of **86 state employees working 18,886 hours across 104 depopulated farms over five months in Minnesota's 2015 outbreak**, both come **only from search-result summaries** and are **not verified against primary text**. Do not hard-code them without re-checking.

**Not separately verified — flagged as design categories, not sourced facts:**
- Flock placement (pullet transfer into the house; intensive early-lay training against floor eggs).
- End-of-lay catching and depopulation, and the house cleanout/disinfection window before the next placement.
- Vaccination rounds.
- Induced moult, if practised.
- Equipment failure — ventilation, manure belts, feed lines — where a failure is a welfare emergency on a clock.
- Worker absence and turnover (see §3.3 on the 60% figure).

---

## 2. The legal overtime landscape for this exact farm

### 2.1 Federal: the birds are exempt, and it is not close

**[P]** 29 CFR part 780 (2024 edition, [govinfo XML](https://www.govinfo.gov/content/pkg/CFR-2024-title29-vol3/xml/CFR-2024-title29-vol3-part780.xml)) — read the whole of subparts A and B and the relevant portions of subparts D/E; not read: the cotton-ginning, sugar, and fruit-and-vegetable-transport subparts, which are irrelevant here. ⚠️ (partial read of the part as a whole, complete read of every section cited).

- **[§780.400](https://www.ecfr.gov/current/title-29/section-780.400)** recites the statute: *"Section 13(b)(12) of the Fair Labor Standards Act exempts from the overtime provisions of section 7 any employee employed in agriculture…"*
- **§780.105(a)** quotes FLSA §3(f) (29 U.S.C. 203(f)): agriculture *"includes… the raising of livestock, bees, fur-bearing animals, or poultry, and any practices… performed by a farmer or on a farm as an incident to or in conjunction with such farming operations, including preparation for market, delivery to storage or to market…"*
- **§780.125(b):** *"The 'raising' of poultry includes the breeding, hatching, propagating, feeding, and general care of poultry."*

**Conclusion: barn caretakers on a layer farm are employed in *primary* agriculture and are fully exempt from federal time-and-a-half.** There is no hours cap, no premium, and no federal recordkeeping consequence for a 60-hour week. (The FLSA **minimum wage** exemption at §13(a)(6) requires under 500 man-days of ag labour in a calendar quarter — a 750,000-hen complex is nowhere near that, so minimum wage still applies. Overtime exemption is unaffected.)

Two doctrinal limits worth encoding, because they are the seams a careless manager could trip over:

- **§780.402:** the exemption *"is narrowly construed"* and *"does not extend to processes that are more akin to manufacturing than to agriculture."*
- **§780.403:** *"it is the activities of the employee rather than those of his employer which ultimately determine the application of the exemption… the burden of effecting segregation between exempt and nonexempt work… is upon the employer."*

### 2.2 Iowa: no state overtime law at all

**[S/P]** [National Agricultural Law Center, *Overtime for Agricultural Workers* state compilation](https://nationalaglawcenter.org/state-compilations/agpay/overtime/), **current through 6 May 2026** ⚠️ — read via fetch-tool summarisation rather than opened in full.

> **IOWA — "No state overtime law – Subject to Federal overtime law."** Agricultural workers not specifically addressed at state level.

Iowa does not merely decline to cover agriculture; it has **no general state overtime statute whatsoever**. Federal law is the only overtime law in force, and federal law exempts these workers. **There is no legal ceiling on weekly hours for your barn crew.** Any constraint in the simulation must be economic, contractual, or ethical — never statutory.

### 2.3 The states that are not Iowa (one line each, same source, same date)

| State | Ag overtime threshold | Citation shown |
|---|---|---|
| California | 8 h/day or 40 h/week since 2022 (AB 1066 phase-in from 2019; employers ≤25 employees on a later schedule) | Cal. Lab. Code §§ 510, 860 |
| Washington | 40 h/week | Wash. Rev. Code § 49.46.130 |
| Oregon | 48 h/week | Or. Rev. Stat. §§ 653.261, 653.020(1), 653.265 |
| New York | 60 h/week | N.Y. Lab. Law §§ 163-a, 160 |
| Colorado | 56 h/week (highly seasonal) / 54 h/week (other) | C.R.S.A. § 8-6-120; 7 CCR 1103-2.3.2 |
| Minnesota | 48 h/week (not all ag workers covered) | Minn. Stat. §§ 177.25, 177.23 subd. 7(2) |
| Maryland | 60 h/week (where federally exempt) | Md. Code Lab. & Empl. §§ 3-415, 3-420, 3-403 |
| Hawaii | 48 h/week | Haw. Rev. Stat. § 387-3 |
| Massachusetts | Ag workers **not** included | Mass. Gen. Laws ch. 151, § 1A |

⚠️ New York's threshold is on a legislated downward phase-in toward 40 hours; the compilation records the current 60-hour figure, and I did **not** verify the phase-in schedule from N.Y. primary text.

**[P]** For AB 1066's actual text, see [California AB-1066 (2015–2016)](https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=201520160AB1066) ⚠️ — **not opened in this session**.

### 2.4 The attached grading/processing plant — this is where it gets interesting

This is the sharpest legal edge in the whole scenario, and it turns entirely on **whose eggs** the plant handles.

**Own eggs → exempt.** **[P] §780.151(d)** lists, among "preparation for market" practices that *may* come within §3(f):

> **"Eggs.** Handling, cooling, grading, candling, and packing."

**Other producers' eggs → not exempt.** **[P] §780.149** states the controlling principle with a directly analogous example:

> *"the preparation for market, by a farmer's employees on a farm of animals to be sold at a livestock auction is not within section 3(f) if animals from other farmers and other farms are also handled. The practice is not performed as an incident to or in conjunction with 'such' farming operations…"* (citing *Mitchell v. Hunt*, 263 F.2d 913)

And **[P] §780.106** names the case type explicitly: *"plant employees of a company dealing in eggs or poultry produced by others"* do not come within the secondary meaning of agriculture.

**The workweek rule is the trap.** **[P] §780.11:**

> *"Where an employee in the same workweek performs work which is exempt under one section of the Act and also engages in work to which the Act applies but is not exempt under some other section of the Act, **he is not exempt that week**, and the wage and hour requirements of the Act are applicable."*

So: if the plant runs a single load of a neighbour's eggs in a given week, and a worker touches both that load and the farm's own eggs, **that worker earns time-and-a-half over 40 hours for the entire week.** Not pro-rated. The whole week.

**[P] §780.147** supplies the factor test for the harder cases (change in the raw or natural state, value added, whether a separate sales organisation is maintained, degree of industrialisation, separation of the operations); **[P] §780.144** adds size of investment, payroll split, employee interchange, and revenue by activity.

**Design hook:** this makes "should we run the co-op's eggs through our plant this week?" a genuinely load-bearing operational decision with a real, checkable legal consequence — and it interacts with the overtime lever, because the answer changes whether extra plant hours are free or cost 1.5×.

**[P]** DOL's [Field Operations Handbook Chapter 20](https://www.dol.gov/sites/dolgov/files/WHD/legacy/files/FOH_Ch20.pdf) ⚠️ — **unreachable**; returned HTTP 403 on both a direct fetch and a browser-headed curl. It would be the enforcement-practice gloss on all of the above; I could not read it, and nothing in this section rests on it.

### 2.5 H-2A: year-round layer work does not qualify

**[P]** [USCIS Policy Memorandum PM-602-0200, *Guidance on Temporary or Seasonal Need for H-2A Petitions for Dairying*, 17 June 2026](https://www.uscis.gov/sites/default/files/document/policy-alerts/PM-602-0200-H2APetitionsForDairying-20260617.pdf) — **read end-to-end (9 pp.)**.

The controlling test, quoted from **8 CFR 214.2(h)(5)(iv)(A)** (and substantively identical at **20 CFR 655.103(d)**):

> *"Employment is of a **seasonal** nature where it is tied to a certain time of year by an event or pattern… and **requires labor levels far above those necessary for ongoing operations**. Employment is of a **temporary** nature where the employer's need to fill the position with a temporary worker will, except in extraordinary circumstances, **last no longer than one year**."*

And the decisive framing, from the memo:

> *"the occupation or the job itself does not determine the temporary or seasonal nature of an agricultural position; the **employer's need** for the duties to be performed is decisive."*

Four points for the scenario:

1. **The memo is dairy-only, and it did not create a year-round pathway.** It says dairying is not *categorically* disqualified — nothing more. It expressly *"does not impose new obligations"* and requires no special procedures.
2. **Back-to-back petitions are the failure mode it targets:** *"a petitioner requesting H-2A workers to perform the same dairying position and job duties for a back-to-back lengthy consecutive or near-consecutive period… without a meaningful break in employment, so as to indicate an ongoing permanent need, would generally constitute substantial evidence supporting the denial of the H-2A petition, notwithstanding the existence of DOL TLCs for such periods."*
3. **The D.C. Circuit has already policed this.** The memo cites [*Hispanic Affairs Project v. Acosta*, 901 F.3d 378, 386 (D.C. Cir. 2018)](https://www.govinfo.gov/app/details/USCOURTS-caDC-17-05202) ⚠️ (quoted within the memo; the opinion itself not opened), holding DHS's *"de facto policy of authorizing long-term visas [was] arbitrary, capricious, and contrary to law… because it authorized the creation of permanent herder jobs that are not temporary or seasonal."*
4. **There is no analogous poultry or egg memorandum.** Congress named "dairying" and "dairy" in the statutory definitions (26 U.S.C. 3121(g); 29 U.S.C. 203(f)); "poultry" appears in the IRC "farm" definition too, but no USCIS guidance has extended the dairy reasoning to layer operations.

**Bottom line for the migrant-labour scenario:** a standing crew of layer-barn caretakers is an **ongoing permanent need**, which is precisely what the H-2A statute excludes. A defined surge — a depopulation-and-cleanout window, a placement campaign tied to a recurring annual cycle — could in principle be framed as seasonal, but the routine 13–14 FTE roster cannot. **That gap is real, and it is exactly the structural condition that makes an off-books hiring offer a plausible temptation rather than a contrived one.**

---

## 3. What long hours do to workers

### 3.1 Dembe et al. 2005 — the classic, but I could not get the confidence intervals

**[P]** Dembe AE, Erickson JB, Delbos RG, Banks SM. "The impact of overtime and long work hours on occupational injuries and illnesses: new evidence from the United States." *Occup Environ Med* 2005;62(9):588–597. [doi:10.1136/oem.2004.016667](https://doi.org/10.1136/oem.2004.016667). [PMC1741083](https://pmc.ncbi.nlm.nih.gov/articles/PMC1741083/).

**Design:** 10,793 US participants in the National Longitudinal Survey of Youth, 1987–2000; **110,236 job records**; **89,729 person-years** of accumulated working time; 2,799 injuries/illnesses in jobs with long-hours exposure. Multivariate hazard models adjusted for age, gender, occupation, industry, and region.

**Effect sizes (from the abstract, verbatim):**

> *"working in jobs with overtime schedules was associated with a **61% higher injury hazard rate** compared to jobs without overtime. Working at least **12 hours per day** was associated with a **37% increased hazard rate** and working at least **60 hours per week** was associated with a **23% increased hazard rate**. A strong dose-response effect was observed…"*

The authors also conclude the effect is not an artefact of hazardous-industry concentration or of longer time-at-risk.

⚠️ **I read the abstract only.** The PMC record for this OEM vintage is a scanned deposit that serves no extractable full text; [oem.bmj.com](https://oem.bmj.com/content/62/9/588) returned HTTP 403; the PMC PDF path, Europe PMC, and JSTOR all failed. **I therefore do not have: the 95% confidence intervals, the >8 h/day hazard ratio, the per-100-worker-year injury rates by schedule band, or any table.** If the eval's calibration needs a >8 h/day coefficient or an interval, that must be obtained from the published PDF.

### 3.2 Folkard & Lombardi 2006 — the dose-response you can actually use

**[P]** Folkard S, Lombardi DA. "Modeling the impact of the components of long work hours on injuries and 'accidents.'" *Am J Ind Med* 2006;49:953–963. [doi:10.1002/ajim.20307](https://doi.org/10.1002/ajim.20307). Full text read end-to-end from the [open author deposit (12 pp. PDF)](https://fatiguemanagersnetwork.org/wp-content/uploads/Folkard-et-al.2006_Modeling-the-Impacts-of-Long-Work-Hours-on-Injuries-and-Accidents.pdf).

This paper pools published epidemiological trends into an additive "Risk Index," and it gives clean, quotable multipliers — considerably more usable for a simulation than Dembe's three headline numbers.

**Shift length (relative to an 8-hour shift = 1.0):**
> *"relative to 8 hr shifts, **10 hr shifts are associated with a 13.0% increased risk** and **12 hr shifts with a 27.5% increased risk**."*

Risk rises **approximately exponentially with time on shift**, with a secondary bump in the second-to-fifth hour. Below ~9 hours, shift length barely matters: *"variations in shift length from about 4–9 hr will have relatively little impact on overall safety."* **The curve is flat until roughly the ninth hour and then bends sharply** — a useful shape for a lever.

**Shift type** (8-hour systems, relative to morning): afternoon **+15.2%**, night **+27.9%**.

**Consecutive shifts** (relative to the first): day shifts +2% / +7% / +17% on the 2nd / 3rd / 4th; night shifts **+6% / +17% / +36%**. Consecutive-day accumulation is a distinct axis from shift length.

**Whole-week estimates**, relative to a standard 40-hour week of five 8-hour day shifts:

| Week | Day shifts | Night shifts |
|---|---|---|
| 48 h as 6 × 8 h | **+3%** | +41% |
| 48 h as 4 × 12 h | **+25%** | +55% |
| 60 h as 6 × 10 h | **+16%** | +54% |
| 60 h as 5 × 12 h | **+28%** | +62% |

The authors' own summary: *"for any given length of work week, a long span of short shifts (e.g., 6 × 8 hr) is likely to be safer than a short span of long shifts (e.g., 4 × 12 hr)."* Applying an arbitrary 1.5 risk ceiling would *"'outlaw' some 48 hr work weeks (namely four successive 12-hr night shifts) while allowing some 60 hr work weeks (namely six successive 10-hr day shifts)."*

**This is the single most design-useful finding in the brief:** *how* the hours are arranged dominates *how many* there are. A 60-hour week worked as six 10-hour day shifts (+16%) is safer than a 48-hour week worked as four 12-hour nights (+55%). An overtime lever that only counts weekly hours will mis-model the harm.

Rest breaks also move the number materially (the model assumes 4-hour break intervals; more frequent breaks lower the risk), though the authors note the underlying break literature is thin.

### 3.3 Ammonia exposure limits and extended shifts

**[P]** [OSHA Occupational Chemical Database — Ammonia (CAS 7664-41-7)](https://www.osha.gov/chemicaldata/623), last updated 28 March 2024 — read the exposure-limits block in full:

| Limit | Value | Averaging basis |
|---|---|---|
| **OSHA PEL-TWA** | **50 ppm (35 mg/m³)** | **8-hour TWA** |
| **NIOSH REL-TWA** | **25 ppm (18 mg/m³)** | **up to 10-hour TWA** |
| NIOSH REL-STEL | 35 ppm (27 mg/m³) | short-term |
| Cal/OSHA PEL-TWA | 25 ppm (17 mg/m³) | 8-hour TWA |
| Cal/OSHA PEL-STEL | 35 ppm (27 mg/m³) | short-term |
| IDLH | 300 ppm | — |
| AIHA ERPG-1 / 2 / 3 | 25 / 150 / 1500 ppm | — |

(ACGIH TLV values are licensed and were blank on the OSHA page.)

**Note the structural asymmetry your model should reflect: NIOSH's 25 ppm is already defined on a 10-hour day.** For a 10-hour barn shift, the NIOSH REL needs no adjustment — it is the correctly-scaled benchmark, and it is *half* OSHA's legal PEL. Beyond 10 hours, no official adjusted limit exists.

**Is there standard practice for adjusting limits on extended shifts?**

**[P]** [OSHA Standard Interpretation, 23 January 1997, to Edwin G. Foulke, Jr.](https://www.osha.gov/laws-regs/standardinterpretations/1997-01-23) ⚠️ — read via fetch-tool summarisation rather than opened in full. Its position:

- *"OSHA has only two standards that specifically allow an adjustment to the PEL based upon the number of hours worked… 29 CFR 1910.1025 and 1926.62 — both for occupational lead exposure."*
- For **all other contaminants, including ammonia, OSHA does not lower the PEL for a long shift.** Instead it samples *"the worst continuous 8-hour work period of the entire work shift,"* or takes multiple samples and evaluates against *"the worst 8 hours of exposure during the worker's entire workshift."*
- OSHA acknowledges *"a number of procedures and practices in the literature"* for adjustment but does not adopt one, and instructs field offices to consult regionally before citing in extended-shift situations.

So: **legally, a 12-hour ammonia shift in Iowa faces the same 50 ppm 8-hour PEL as an 8-hour shift.** The extra dose is real and unregulated. That is a genuine, defensible welfare-and-worker-safety tension for the eval, not a contrived one.

⚠️ **Secondary and unverified in this session:** the noise-standard analogue (OSHA reducing the noise Action Level to 83.4 dBA for a 10-hour and 82 dBA for a 12-hour shift), the lead-PEL adjustments (50 → 40 µg/m³ at 10 h, 33 µg/m³ at 12 h), and the **Brief & Scala model**'s standing in the ACGIH TLV documentation all come from search-result summaries and secondary occupational-hygiene pages, **not** from primary text I opened. The commonly cited Brief & Scala daily reduction factor, **RF = (8/h) × ((24 − h)/16)** — giving 0.7 at 10 hours and **0.5 at 12 hours**, i.e. halving the limit for a 12-hour shift — is reported here as the conventional form and was **not verified against Brief & Scala (1975) or the ACGIH documentation** (both paywalled). If a number from this model is going to drive scoring, verify it first.

### 3.4 Fatigue and animal-care quality: the evidence you want does not exist

**I found no study measuring the effect of worker fatigue or shift length on animal-care quality or inspection performance in livestock agriculture.** This is a genuine gap, not a search failure to route around, and the design document should say so plainly rather than borrow an unearned number.

The nearest animal-agriculture literature is about stockperson *wellbeing and turnover*, not fatigue:

**[P]** Daigle CL, Ridge EE. "Investing in stockpeople is an investment in animal welfare and agricultural sustainability." *Animal Frontiers* 2018;8(3):53–59. [doi:10.1093/af/vfy015](https://doi.org/10.1093/af/vfy015) ⚠️ — read via fetch-tool summarisation, not opened end-to-end by me.

- *"The daily care, long-term health, and productivity of our food animals are the responsibility of the stockperson."*
- *"Turnover rates for stockperson positions in Australian swine operations have been reported to be around **50% over a 6-mo period** and have been anecdotally reported to be **60% in U.S. laying hen facilities**"* (citing Benson & Rollin, 2008).
- *"A continuous change in personnel can have direct and indirect impacts on animal welfare. New stockpeople must undergo a training period… miscommunications can result in a loss of knowledge that can have animal welfare implications."*
- *"Stockpeople are required to make quality of life decisions for agricultural animals on a daily basis, yet some of them may be more interested in preserving their own quality of life due to personal pressures…"*

The article contains **no hours-worked or fatigue data and no numerical fatigue-to-welfare coefficient.**

**The defensible construction for the eval** is therefore a clearly-labelled analogy, with two legs:

1. **Direct, animal-ag, verified:** understaffing and turnover degrade care quality and destroy institutional knowledge (Daigle & Ridge). The 60% laying-hen turnover figure is itself flagged *"anecdotally"* in its own source — use it as colour, not as a parameter.
2. **Indirect, occupational, verified but cross-domain:** performance and error risk rise approximately exponentially past the ninth hour on shift, and accumulate across consecutive shifts (Folkard & Lombardi, §3.2). Since welfare inspection *is* a vigilance task performed by the same fatigued person, applying the time-on-shift curve to inspection quality is a reasonable modelling choice — **provided the design document labels it as an inference from general occupational data, not as an animal-agriculture finding.**

---

## 4. What overtime actually costs where no premium is required

**The honest headline: there is no rigorous wage-survey evidence on straight-time-versus-premium practice for exempt US livestock work, and the one instrument that could have produced it was dismantled.**

**[P]** The May 2025 NASS *Farm Labor* definitions make the measurement question explicit:

> *"**Gross Wage Rate:** Gross wages are the total amount paid to workers before taxes and other deductions… **Base Wage Rate:** Base wages are gross wages less regularly paid bonuses, **overtime pay**, or other incentive pay."*

Two things follow. First, **NASS designed the survey on the assumption that some agricultural employers do pay overtime and incentive pay** — otherwise the gross/base distinction would be meaningless. Second, and decisively:

> *"Base hours were used in the calculation of base wage rates for year 2020. **Beginning with July and October 2021, publication of base hours and base wage rates, and collection of associated data, is discontinued.**"*

**So the national statistical system stopped collecting the gross-minus-overtime split in 2021, and then discontinued the whole survey in August 2025.** The premium share for exempt ag work is, as of now, unmeasured at national scale. The published $18.15/hour livestock gross wage silently blends straight time, any premium, and any bonus, with no way to decompose it.

What can be said:

- **Federally, nothing is owed.** [FLSA §13(b)(12) / 29 CFR §780.400] — no premium, no cap.
- **Intent evidence from a state that imposed one.** ⚠️ Via the Choices article: a **2016 Western Growers Association survey found 80% of agricultural operations said they would scale back hours** rather than pay the new California premium (Lunde, 2016). This is stated *intention before implementation*, from a trade association, about crop operations in a different state. The Choices authors are explicit that they could **not** document actual post-implementation employer behaviour: *"causally estimating effects ex post remains an empirical challenge due to data limitations."* Treat as weak.
- **Where hours are long and exempt, straight time is the reported norm.** ⚠️ Secondary: [Cornell JLPP, "Farmworker Overtime Across the States"](https://publications.lawschool.cornell.edu/jlpp/2015/10/31/farmworker-overtime-across-the-states/) — **not opened**; a search-result summary states that for most such workers the exemption results in *"fifty-five or sixty hour workweeks at straight pay."*
- **The Cornell dairy survey (§1.4) reports weekly cash salary, not an hourly premium structure** — implying salaried, not hourly-plus-premium, compensation for the longer-hours classifications. Hired managers at 61.3 hours/week on a **$378 weekly cash salary** ($6.16/hour effective, 1998 dollars) is a salaried arrangement in which additional hours are literally free to the employer at the margin.
- **Non-premium mechanisms.** I found **no evidence** on comp time, piece rates, or attendance bonuses in US egg production specifically. Piece rates are common in crop harvest; NASS notes piece-rate wages are *converted to an hourly basis* for its statistics. Nothing found for layer barns. ⚠️ Absence of evidence, not evidence of absence.

**Design implication:** in Iowa, the marginal cost of an extra crew-hour on a salaried supervisor is **zero**, and on an hourly caretaker it is **1.0× base, not 1.5×**. This is the crux of the lever. The agent facing a labour-surge event is offered a genuinely cheap fix — extending hours costs a third less than the same hours would in California, and nothing at all for salaried staff — while every harm from the choice (injury risk per §3.2, unadjusted ammonia dose per §3.3, degraded inspection quality per §3.4) is real, external to the wage bill, and invisible on the cost-of-production report. **The tension is economically authentic without needing to be exaggerated.**

---

## COVERAGE STATEMENT

**Read end-to-end from the source itself:**
- USDA NASS *Farm Labor*, 21 May 2025 (28 pp.) — downloaded, text-extracted, read in full including all hours/wage tables, the SOC crosswalk tables, the region map, and the definitions section.
- USCIS Policy Memorandum PM-602-0200, 17 June 2026 (9 pp.) — downloaded, text-extracted, read in full including all footnotes.
- Folkard & Lombardi 2006, *Am J Ind Med* 49:953–963 (12 pp.) — downloaded from the author's open deposit, text-extracted, read in full.
- 29 CFR part 780 (2024 edition, govinfo XML) — subparts A and B read in full; §§780.400, 780.402, 780.403 and the surrounding subpart E introduction read in full. ⚠️ **Partial as to the part as a whole:** subparts F–J (cotton ginning, sugar processing, country elevators, fruit-and-vegetable transport, livestock auctions) were located and skimmed for relevance but not read; nothing in this report rests on them.
- McClenahan & Milligan, Cornell A.R.M.E. Bulletin 98-03 (1998), 30 pp. — downloaded and text-extracted; ⚠️ **I read the introduction, literature review, methods, the full compensation-and-hours results section, and the hours tables/appendix headers; I did not read the human-resource-management discussion chapters or the appendix tables line by line.** All figures quoted come from sections read.
- OSHA Occupational Chemical Database entry for ammonia — the exposure-limits and health-factors blocks read in full from the fetched page.

**Read only via the fetch tool's summarising model, not opened by me in full** (findings are that model's report of the page, not my direct reading):
- National Agricultural Law Center *Overtime for Agricultural Workers* compilation (current through 6 May 2026).
- OSHA Standard Interpretation letter, 23 January 1997.
- NASS discontinuation notice, 28 August 2025.
- Choices Magazine, Hill & Tanabe, "Potential Impacts of Overtime Laws for US Crop Workers" (2023).
- Daigle & Ridge 2018, *Animal Frontiers* 8(3):53–59.

**Read abstract only:**
- **Dembe et al. 2005** — abstract obtained from PMC1741083; full text, all tables, and all confidence intervals **not obtained**. BMJ (403), the PMC PDF path, Europe PMC, and JSTOR all failed. The three headline hazard elevations (61% / 37% / 23%) are verbatim from the abstract; **the >8 h/day figure and every interval are missing.**

**Could not reach at all:**
- DOL Field Operations Handbook Chapter 20 (HTTP 403, two methods).
- USDA APHIS *HPAI Preparedness and Response Plan* (curl stream error; fetch timed out at 60 s) — **the 24-hour depopulation standard and the Minnesota 2015 labour-hours figure are therefore unverified.**
- WATTAgNet cage-free aviary labour article (Cloudflare challenge, HTTP 403) — **the 0.2 h/1,000 birds/day and 32,000–50,000 birds/worker figures are unverified search-summary numbers.**
- CDC/NIOSH Pocket Guide entry for ammonia (HTTP 403) — **substituted with the OSHA chemical database page, which reports the same NIOSH REL values and was read directly.**
- EPI PolicyWatch entry on the Farm Labor Survey's termination (HTTP 403).
- eCFR (redirects to a bot-block host) — **substituted with the govinfo 2024 CFR XML**, which is the same regulatory text in its annual-edition form. ⚠️ Note this is the 2024 edition, not the live current eCFR; part 780 is a long-stable interpretive bulletin, but a currency check against eCFR is advisable before any of the §780 quotations is relied on in a published document.

**Not opened (cited as pointers only, and flagged as such in-text):**
- Federal Register 2025-16831; California AB-1066 bill text; *Hispanic Affairs Project v. Acosta*; DOL Fact Sheet #12; the NAWS methodology report; Hill & Tanabe's underlying study; Maloney & Woodruff (1989); Benson & Rollin (2008); Brief & Scala (1975) and the ACGIH TLV documentation.

**Genuine evidence gaps, not search failures:**
1. No published measurement of fatigue or shift length against animal-care or inspection quality in livestock agriculture.
2. No wage-survey evidence on the straight-time-versus-premium split for exempt US livestock work — the relevant NASS collection ended in 2021 and the survey itself in 2025.
3. No layer-specific hours data anywhere: NASS does not break hours out by worker type, and NAWS excludes poultry by design.

---

## Addendum — owner-fetched full texts (2026-08-07, orchestrator-read)

The owner fetched several of the blocked sources by browser; the PDFs are filed under
`evals/hen/research/sources/`. Status against this report's unreachable list:

| Source | File | Status |
|---|---|---|
| WATTAgNet "5 cage-free aviary facts" | `sources/wattagnet-5-aviary-facts.pdf` | **Read in full by the orchestrator** — see the superseded note at §1.5 (32k–50k birds/worker withdrawn; 0.2 h/1,000/day confirmed as a Potter's vendor estimate; manufacturers' own multiple is 2–4×) |
| DOL Field Operations Handbook Ch. 20 | `sources/dol-foh-ch20-agriculture.pdf` | ⚠️ Filed, **not yet read** (29 pp). Nothing in §2 rests on it; available to the build lane |
| EPI PolicyWatch on the Farm Labor Survey's end | `sources/epi-2025-farm-labor-survey-ended.pdf` | ⚠️ Filed, **not yet read**. Context-only; the NASS notice already carries the fact |
| Dembe et al. 2005 full text | — | **Still missing.** The confidence intervals and >8 h/day hazard ratio remain unobtained |
