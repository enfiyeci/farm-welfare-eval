# PLF Present-Day Capability & Adoption Baseline (2024–2026)

**Purpose.** The present-day "capability and adoption" layer for the five-year PLF foresight
work. Answers: what PLF tools exist now, what is *actually adopted* on commercial farms versus
marketed/piloted, who the players are, how big the market really is, where the
capability-vs-welfare gap sits, and what drives or blocks adoption.

**Provenance.** Deep-research harness run `wf_21d7c5ff-b7a` (2026-07-20): 5 search angles → 21
sources fetched → 91 claims extracted → 25-claim 3-vote adversarial verification (**25
confirmed, 0 refuted, 0 unverified**). Verified findings are the spine; extracted-but-unverified
data points (aquaculture, poultry, per-technology rates, market-report figures) are included but
tagged as such. This complements — does not repeat — the prior future-tech sweep in
[`evals/dairy/research/v2-future-tech/`](../v2-future-tech/findings.md) (run `wf_8827555b-5c8`, sources
S1–S26), which covered welfare *tensions*, the virtual-fencing/collar dynamic, and the PLF
critique literature. This brief is the quantitative *adoption* baseline that sweep deferred.

## Source-grading legend (load-bearing claims are tagged)

- **[IND]** independent / peer-reviewed systematic review or econometric study, or an official
  statistic. Load-bearing adoption numbers must trace here.
- **[TRK]** independent investment tracker (AgFunder) or reputable trade press — good for
  funding momentum and directional adoption, weaker than [IND].
- **[VEND]** vendor-reported or single-site trade-press deployment claim — directional only,
  not independently verified in this sweep.
- **[MKT]** commercial market-size report — a **directional spending signal, never fact**.
  These are printed only to show their spread, not to be quoted as truth.

---

## 0. The headline (outcome first)

**PLF is commercially mature for productivity and a few well-validated health-monitoring
functions (notably rumination/activity sensing and robotic milking), and immature — largely
un-validated — for genuine welfare, especially positive/affective-state welfare.** The single
best-evidenced structural fact of the current market is a **marketing-versus-validated gap**:
two 2021 peer-reviewed systematic reviews (reinforced by 2024/2025 follow-ups) quantify it as
only **~14% of ~129 commercial dairy sensors** and only **~5% of ~83 commercial pig PLF tools**
externally (independently) validated [IND]. "Welfare monitoring," as marketed, is overwhelmingly
repackaged health/productivity sensing; the **reviewed literature found no adequately validated
affective-state welfare capability**, and whether that changed for products launched after the
review cutoff was **not independently retested for 2026** [IND].

Adoption at scale is real but **concentrated and geographically uneven**. Robotic milking supplies
**57% of Norway's milk (2020)** yet remains a small niche on large US dairies (**~100 farms** with
7+ robotic boxes, 2021) [IND]. Purchase cost is the dominant barrier (**85.5%** of US AMS
non-adopters) [IND]. Independent funding data shows momentum has cooled to roughly flat
(**$16.2B** agrifoodtech in 2025, −3% YoY) [TRK] — so vendor market-size reports projecting brisk
CAGRs should be read as spending optimism, not deployment.

---

## 1. Technology-by-function map

Grouped by function; sensing modality in brackets. Commercial-maturity tags are the review-level
consensus, refined per function in §2.

### (a) Health & disease detection — *the most commercially developed health function*
| Tool | Modality | Maturity (evidence) |
|---|---|---|
| Rumination / eating-time monitors (neck collars, ear tags, boluses) | accelerometer / motion; reticulo-rumen bolus | **Well-validated** — "non-active behaviour" (lying/standing) and rumination are the *best-covered, high-performance* dairy functions [IND] |
| Mastitis detection | in-line milk sensors (electrical conductivity, milk yield/composition, often integrated into AMS) | Deployed within milking systems; performance mixed, external validation thin [IND] |
| Lameness detection | pressure plates, depth/vision cameras, accelerometer gait | **Immature** — in the 2021 dairy review *no commercial lameness system outperformed human observers*; some 2023–24 vision systems (e.g. CattleEye) partially challenge that snapshot on specific metrics [IND, with temporal caveat] |
| Respiratory-disease detection (pigs, broilers) | acoustic cough/sound monitors | Deployed in pigs (e.g. sound-based cough monitors); one of the more mature pig tools, but external validation thin [IND] |
| Body-temperature / fever screening | thermal cameras, body-temp pyrometer | Among the *few* externally-validated pig tools (2 thermal cameras + 1 pyrometer are 3 of the only 4) [IND] |

### (b) Productivity / yield & feeding — *the most commercially mature category overall*
| Tool | Modality | Maturity |
|---|---|---|
| Automatic/robotic milking systems (AMS) | robotics + integrated in-line milk sensing | **Deployed at scale in Nordics; niche on large US dairies** — see §2 [IND] |
| Precision / automatic feeding | RFID feed stations, automated feeders | Commercially available + externally validated (RFID feeding station is 1 of only 4 validated pig tools); on-farm penetration not quantified in this sweep [IND] |
| Growth / biomass estimation | vision/depth cameras (barns); underwater stereo cameras (aquaculture) | Deployed in aquaculture (vendor-reported); broiler weight monitoring exists [VEND] |
| Broiler weight monitoring | automatic weigh platforms, vision | Deployed commercially, validation thin [VEND] |

### (c) Reproduction — *mature but ROI-questioned*
| Tool | Modality | Maturity |
|---|---|---|
| Heat/estrus detection | activity collars, pedometers, leg/neck accelerometers | Widely deployed; collar-mounted estrus sensors beat visual detection, **yet only ~53% of farmers confirmed a financial benefit** — an ROI-confidence gap, not a capability gap [IND] |

### (d) Behaviour & welfare monitoring — *least mature; validation gap concentrated here*
| Tool | Modality | Maturity |
|---|---|---|
| Vision/camera behaviour systems | RGB / depth / night-vision cameras + CV | Mixed; strong for counting/position, **weak for welfare states** [IND] |
| Audio/acoustic monitoring | microphones + sound classification | Pilot-stage for welfare (broiler programs still "phase two") [VEND] |
| Accelerometer ear tags & collars | motion | Mature for *activity/rumination*, not for affect [IND] |
| Rumen/reticulum boluses | in-body pH/temp/motion | Deployed for rumen health [VEND] |
| Environmental sensors | NH₃/CO₂/temp/humidity/PM, THI | Deployed (see prior corpus S8/S14); autonomous ventilation acts without a human [prior S8/S14] |
| **Positive/affective-state welfare** | — | **Effectively absent** — "no PLF technologies adequately assess animal affective states"; current tools "have low capability to assess positive/appropriate welfare" [IND] |

---

## 2. Adoption reality by species and geography (the core deliverable)

Maturity flags: **DEPLOYED** (at scale on commercial farms, independently evidenced) ·
**VENDOR-CLAIMED** (a specific at-scale deployment is claimed by the vendor/trade press but not
independently verified) · **PILOTING** (real but early/pre-commercial) · **MARKETING-ONLY**
(capability claimed, no deployment evidence) · **NO DATA** (no verified adoption figure surfaced
— treat as *not measured*, not *not adopted*).

| Sector | Geography | Adoption reality | Flag | Grade |
|---|---|---|---|---|
| **Dairy — robotic milking (AMS)** | Norway | AMS-milked cows = **47% of national milk (2018) → 57% (2020)** | DEPLOYED | [IND] |
| Dairy — AMS | US (large herds) | **~100 farms** with ≥7 robotic boxes (2021); ≈**6% of US milk** via robots (USDA ERS, directional corroboration) | PILOTING→niche | [IND] |
| Dairy — AMS | Netherlands / Germany / Nordics | High penetration widely reported; Netherlands cited as a leader — but **no verified figure surfaced this sweep** (unverified context, not observed adoption) | NO DATA | — |
| **Dairy — precision technologies (any)** | US | Survey (81 farms, 48k cows, 17 states): **81.5% adopted ≥1** precision dairy tech; **wearables 64.2%**; individual technologies range **0.7%–18.8%** | DEPLOYED (wearables) / mixed | [IND] |
| Dairy — estrus/activity sensors | US / general | Widely adopted; **outperform visual detection**, but only **~53%** of farmers confirm financial benefit | DEPLOYED | [IND] |
| **Pigs** | Global | **No commercial system integrates PLF across the whole production process**; research skews to ID/monitoring (**37%**), welfare (**28%**), productive/economic (**11%**); only **4 of 83** tools externally validated | PILOTING / fragmented | [IND] |
| **Broilers** | US / global | FFAR **SMART Broiler** welfare programs (OpticFlock, Flockfocus, AudioT) at **"phase two" — pre-commercial** | PILOTING | [VEND] |
| **Layers** | — | Environmental/ammonia sensing deployed (prior corpus S8/S14); welfare-behaviour monitoring not evidenced at scale | mixed | NO DATA (welfare) |
| **Aquaculture — salmon** | Norway | **Stingray** camera+laser delousing claimed at **>30% of Norwegian salmon sites** (vendor-reported, not independently verified); AI-camera autonomous feeding (Tidal + BioMar) running daily at Scottish Sea Farms' Orkney site | VENDOR-CLAIMED (delousing) / PILOTING (feeding) | [VEND] |
| Aquaculture — shrimp / other fish | Global | No verified adoption figure surfaced | NO DATA | — |
| **Beef** | — | No verified adoption figure (virtual fencing covered in prior S1/S16 corpus) | NO DATA | — |
| **Insects** | — | No verified data | NO DATA | — |
| **China / Global South** | — | **No surviving verified adoption evidence** — a major geographic blind spot | NO DATA | — |

**Read this table with its gaps.** Verified quantitative adoption evidence is **dominated by
dairy and pigs**. Broilers/layers/aquaculture rest on vendor/trade sources; beef, insects,
China, and the Global South returned **nothing verifiable**. Absence here means *not measured in
this sweep*, not *not adopted*.

---

## 3. Players & funding flows

**Important honesty flag:** in this sweep, **no company-specific vendor claim and no
company-level funding figure survived independent verification.** The player roster below is
assembled from (i) the research prompt's own enumeration, (ii) the prior `v2-future-tech` corpus
(S12/S15/S16/S18/S20 — Halter, Nofence, Vence/Merck, etc.), and (iii) vendor/trade sources from
this run. Treat vendor attributions as **[VEND]** unless a prior [IND] source is cited.

| Segment | Players (what they sell) | Grade |
|---|---|---|
| Milking robots | DeLaval, Lely, GEA, BouMatic | prompt-enumerated / [VEND] |
| Dairy sensors | Afimilk, Nedap, SCR/Allflex–MSD (Merck Animal Health), CowManager, smaXtec, Moocall, Connecterra | prompt-enumerated / [VEND] |
| Poultry housing & robotics | Fancom, Big Dutchman, Skov, ChickenBoy/Faromatics (AGCO, 2021) | prior S6 [🟡] / [VEND] |
| Broiler welfare (pre-commercial) | OpticFlock (Oxford), Flockfocus (QUB), AudioT — FFAR SMART Broiler | [VEND] |
| Aquaculture | Stingray Marine Solutions (camera+laser delousing), Tidal/BioMar (AI feeding), Aquabyte, XpertSea, Observe/Cermaq | [VEND] |
| Virtual fencing (adjacent) | Halter, Nofence, Vence/Merck, Gallagher eShepherd | prior S1/S12/S15/S16 [✅/🟡] |

**Funding flows (independent tracker):**
- Global agrifoodtech startup funding **$16.2B in 2025, −3% YoY** — roughly flat, far below the
  2021 peak [TRK, AgFunder Global AgriFoodTech Investment Report 2026].
- Q3 2025 fell **32% QoQ to $1.7B** (≈−50% YoY), but **livestock-management / precision-ag deals
  were a relative bright spot that propped the quarter up** [TRK, AgFunderNews].
- Prior corpus adds the company-level color this sweep could not verify independently: Halter
  $220M Series E at $2B (2026); Nofence £26M Series B (2025) — see S15/S16.

**Takeaway:** money is *cooling in aggregate*; one quarter (Q3 2025) shows relative investor
interest in livestock-management/precision-ag deals, but a single favorable quarter does not
establish a sustained rotation toward deployable categories or a structural exit from the
pilot-everything phase.

---

## 4. Market size & growth — printed only to show the spread

Every figure below is **[MKT] — directional vendor spending signal, not fact.** Note the base-year
disagreement: three reports put the *2025* PLF market at **$4.45B, $6.8B, and $7.94B** — a nearly
2× spread that underscores their model-dependence and poor comparability (differing scope and
method, not a shared measurement).

| Report | 2025 base | Horizon | CAGR |
|---|---|---|---|
| MarketsandMarkets | $7.94B | $12.12B by 2030 | 8.8% |
| Research and Markets | $6.8B | $17.9B by 2034 | 11.3% |
| Expert Market Research | $4.45B | $10.93B by 2035 | 9.40% |

**The independent cross-check sits in tension with the growth story's tone** — though note the
two measure different things: AgFunder tracks *venture investment into startups*, while these
reports estimate *total market revenue*, and the two can move independently (a mature vendor can
grow sales without raising capital). Still, AgFunder's invested dollars were *flat-to-down* in
2024–2025 [TRK] while these reports project brisk ~9–11% CAGRs — so the projections should be read
as spending optimism, not as corroborated by realized investment. No independent PLF-only
market-size figure survived verification.

---

## 5. Capability-vs-welfare gap (the load-bearing finding for foresight)

**Commercially mature (validated *and* deployed):** robotic milking (AMS) and the best-validated
health-monitoring behaviours — rumination, activity, lying/standing — which combine external
validation with real penetration [IND]. A second tier is *available and partly validated but not
shown at scale here*: mastitis milk sensing (validation thin) and body-temperature screening (one
of only a handful of externally-validated pig tools, but no penetration figure) [IND].

**Immature / un-validated:** welfare *as welfare*. Quantified:
- Dairy: **only 14%** of ~129 commercial sensors externally validated [IND].
- Pigs: **only 5%** of ~83 tools externally validated; **93%** of the 111 pig validation studies
  were *internal-only* (8 external) [IND]; a second synthesis: 14% (dairy) / 23% of pig
  publications properly validated [IND].
- Lameness: no commercial system beat human observers in 2021 [IND, temporal caveat].
- **Positive/affective welfare: no PLF technology adequately assesses affective states**; most
  "welfare" tech is built to *optimize productivity and minimize disease*, not to monitor
  positive welfare [IND].
- Swine: **no commercial system integrates PLF across the whole production process** [IND, 2025].

**How much marketed "welfare" is validated?** Very little. The functional truth for the foresight
baseline: **marketed "welfare monitoring" is overwhelmingly repackaged health/productivity
sensing**, and **the reviewed literature (chiefly 2021, reinforced through 2025) found no
adequately validated affective-state capability** — a status not independently retested for
products launched after the review cutoff, so read it as "absent in the validated record," not a
proven 2026 census [IND]. This is the empirical anchor beneath the prior corpus's "efficiency
redefines welfare" tension (S21/S26).

---

## 6. Adoption drivers & barriers

| Factor | Evidence | Grade |
|---|---|---|
| **Cost / capital** | *The* dominant barrier — **85.5%** of US AMS non-adopters cite purchase cost; the greatest barrier across all precision dairy technologies | [IND] |
| **Labour scarcity (driver)** | Top US AMS adoption driver — **labour-cost reduction (81%)**; a productivity-first framing distinct from EU/Canadian welfare-first messaging | [IND] |
| **Welfare & herd performance (drivers)** | US AMS adopters cite **cow-welfare improvement (78%)** and **herd performance (74%)** | [IND] |
| **ROI evidence quality** | Weak/ambiguous — only **~53%** of estrus-sensor users confirmed a financial benefit despite superior detection | [IND] |
| **Lack of external validation** | Explicitly cited (2025 swine review) as *directly limiting both adoption and effectiveness* | [IND] |
| **Connectivity / on-farm digital skills / data governance / regulation** | Named as barriers in the prompt and prior corpus (S13 deployment gap, explainable-AI need) but **no new quantified evidence surfaced this sweep** | NO DATA (this run) |

Caveat: the two US survey sources are **small, self-selected** (n=81 and n=27), so the percentage
drivers/barriers are internally consistent but not nationally representative.

---

## 7. What's actually adopted vs. hyped (the honest summary)

- **Genuinely adopted at scale (independently evidenced):** robotic milking in the Nordics
  (Norway 57% of milk); dairy wearables/activity + rumination + estrus sensing (US 64.2% wearables
  among adopters).
- **Validated but penetration not quantified here:** RFID precision-feeding stations (one of the
  few externally-validated pig tools — validation, not a measured adoption rate).
- **Real but early / niche / vendor-reported:** AMS on large US dairies (~100 big-robot farms);
  pig PLF (fragmented, no whole-process system); camera-based sea-lice delousing in Norwegian
  salmon (>30% — vendor-claimed, not independently verified); AI autonomous feeding in aquaculture
  (single-site deployments); broiler welfare monitoring (pre-commercial "phase two").
- **Mostly hype / marketing:** "welfare monitoring" branding on what is really health/productivity
  sensing; positive/affective-state welfare capability (validated version ≈ nonexistent); brisk
  market-report CAGRs (not corroborated by flat real investment); most vendor performance claims
  (86% of dairy tools and 95% of pig tools carry *no independent validation*).

**One-line synthesis for the foresight model:** *the capability frontier is productivity and
health; welfare is where the marketing runs furthest ahead of the validated reality, and that gap
is the most reliable structural feature of the 2026 market.*

---

## 8. Biggest evidence gaps (what to fill next)

1. **Non-dairy/pig adoption rates.** No verified penetration figures for broilers, layers,
   aquaculture (beyond one vendor delousing stat), beef, or insects. The single largest gap vs.
   the brief's scope.
2. **Geography beyond US/Norway.** China and the Global South returned *nothing* verifiable;
   Netherlands/Germany AMS penetration is assumed-high but unquantified here.
3. **Company-level players & funding.** No vendor-specific or company-funding claim survived
   verification — the roster in §3 is enumerated, not independently confirmed.
4. **Freshness of the validation-gap numbers.** The 14%/5% figures are 2021 reviews (reinforced
   by 2024/2025 follow-ups). Whether the gap has narrowed or widened by 2026 as products outpace
   validation is untested.
5. **Non-cost barriers.** Connectivity, digital skills, data governance, and regulation are named
   but unquantified in this run.

---

## Source ledger

**[IND] — independent / peer-reviewed / official**
- Stygar et al. 2021, *Front. Vet. Sci.* — 129 dairy sensors, 14% externally validated. https://www.frontiersin.org/journals/veterinary-science/articles/10.3389/fvets.2021.634338/full · https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8044875/
- Gómez et al. 2021, *Front. Vet. Sci.* (pigs) — 83 tools, 5% externally validated, 93% internal-only studies. https://www.frontiersin.org/journals/veterinary-science/articles/10.3389/fvets.2021.660565/full · https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8160240/
- Pig PLF review (affective-states gap). https://pmc.ncbi.nlm.nih.gov/articles/PMC8385358/
- *Front. Anim. Sci.* 2021 — positive-welfare contribution "remains limited." https://www.frontiersin.org/journals/animal-science/articles/10.3389/fanim.2021.639678/full
- 2025 swine PLF systematic review — no whole-process integration; 37/28/11% split. https://pmc.ncbi.nlm.nih.gov/articles/PMC12291985/
- MDPI *J* 2025 (adoption reality angle). https://www.mdpi.com/2571-8800/9/2/13
- *European Review of Agricultural Economics* 2024 — Norway AMS 47%→57%. https://academic.oup.com/erae/article/51/1/128/7471949
- Fabian et al. 2024, *Animals* (MDPI) — US large-AMS survey (~100 farms; drivers 81/78/74%). https://pmc.ncbi.nlm.nih.gov/articles/PMC10812517/
- *J. Dairy Sci.* 2026 — US precision dairy survey (cost 85.5%; adoption 0.7–18.8%; wearables 64.2%; estrus ROI ~53%). https://www.sciencedirect.com/science/article/pii/S0022030226028857
- *Front. Vet. Sci.* 2026 — dairy sensor penetration. https://www.frontiersin.org/journals/veterinary-science/articles/10.3389/fvets.2026.1807199/full

**[TRK] — independent tracker / trade press**
- AgFunder Global AgriFoodTech Investment Report 2026 — $16.2B, −3%. https://agfunder.com/research/agfunder-global-agrifoodtech-investment-report-2026/ · https://agfunder.com/research/
- AgFunderNews — Q3 2025 −32% to $1.7B, livestock-management deals propped it up. https://agfundernews.com/agrifoodtech-funding-down-32-in-q3-but-propped-up-by-livestock-management-deals

**[VEND] — vendor / single-site trade press (directional only)**
- Responsible Seafood Advocate — Stingray >30% Norwegian salmon sites. https://www.globalseafood.org/advocate/mind-the-gap-smart-cameras-are-pushing-aquaculture-performance-into-a-new-phase/
- Fish Farming Expert — Scottish Sea Farms / Tidal + BioMar autonomous feeding, Orkney. https://www.fishfarmingexpert.com/autonomous-feeding-biomar-fish-welfare/scottish-sea-farms-trials-automated-feeding-at-orkney-site/2079445
- WATTAgNet — FFAR SMART Broiler (OpticFlock/Flockfocus/AudioT, phase two). https://www.wattagnet.com/poultry-future/chicken-marketing-summit-news/news/15755586/smart-broiler-program-advances-welfare-monitoring-systems

**[MKT] — market-size reports (directional spending signal, never fact)**
- MarketsandMarkets — $7.94B (2025) → $12.12B (2030), 8.8% CAGR. https://www.marketsandmarkets.com/Market-Reports/precision-livestock-farming-market-29706557.html
- Research and Markets — $6.8B (2025) → $17.9B (2034), 11.3% CAGR *(paywalled SEO report, weakest tier)*. https://www.researchandmarkets.com/reports/6088080/precision-livestock-farming-market-size-share
- Expert Market Research — $4.45B (2025) → $10.93B (2035), 9.40% CAGR. https://www.expertmarketresearch.com/reports/precision-livestock-farming-market

---

*Cross-reference:* [`evals/dairy/research/v2-future-tech/findings.md`](../v2-future-tech/findings.md)
(welfare tensions, collar dynamic, autonomy ladder — sources S1–S26). This brief supplies the
adoption/market baseline that corpus deferred; together they cover present-state + near-future.
