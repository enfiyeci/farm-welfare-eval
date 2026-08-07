# The labour production function — what a barn labour-hour buys, at task level

Eval: hen

> Commissioned 2026-08-07 by the staffing-design lane (ruling 4) to ground the owner's question:
> what benefit does overtime bring, and what is an extra (migrant) worker worth, before we claim
> "X hours → X production/welfare"? Findings are attributed to a delegated Opus research pass,
> **not independently re-read by the orchestrator**. ⚠️ markers and the coverage statement are
> carried through verbatim.

# The Labour Production Function for Cage-Free Layer Housing

**Research report — what a barn labour-hour buys, at task level**
Prepared for the ~750,000-hen Iowa cage-free aviary simulation (13–14 FTE direct bird care).

---

## Executive summary

Five findings that should drive the staffing/overtime lever design:

1. **The single best-quantified labour→outcome link in cage-free is egg collection, not mortality.** In the only peer-reviewed commercial cost study with a task-level labour breakdown ([Matthews & Sumner 2015](https://doi.org/10.3382/ps/peu011)), egg collection is *the largest single labour line* in an aviary and rises to **>3 cents/dozen** in the back half of the cycle — roughly 40%+ of total aviary labour cost.

2. **The "3–5× labour" claim has a real primary source**, and it is Matthews & Sumner, not the trade press: labour cost per dozen was **$0.019 conventional vs $0.074 aviary (3.9×)**, with the paper stating explicitly that wage rates were identical across houses, so the cost ratio *is* an hours ratio.

3. **Vendor guidance gives hard walking numbers.** Hy-Line specifies a **minimum of six walks per day** through the nest-training period (transfer → peak, ~27–32 weeks). Lohmann specifies a dawn inspection daily plus floor-egg gathering "several times a day."

4. **The evidence that human presence interrupts piling is weak, and I recommend modelling it as weak.** Campbell et al. observed 174 piles and found that **only 3 ended because of a disturbance** — the other 171 dissolved spontaneously. Barrett et al.'s industry survey found walking birds more often is a *popular* measure but concluded there are "no clear, effective reduction strategies."

5. **Your 13–14 FTE is lean but defensible** — about 0.036–0.039 h/hen-year, versus ~0.09–0.14 h/hen-year implied by Matthews & Sumner for a commercial aviary (my arithmetic, assumptions below). Do **not** calibrate against the NC State research-station figures; they are ~10× too high in level.

---

## 1. Time-and-motion / labour-input studies for layer housing

### 1a. The two prize targets — reached in abstract only

Both ScienceDirect targets remain **unreadable in full**. ScienceDirect now serves a Cloudflare CAPTCHA to browsers and 403s to fetchers; both papers are CC-BY-NC-ND open access but Elsevier is the *only* OA host ([Unpaywall confirms no repository copy](https://api.unpaywall.org/v2/10.1016/j.japr.2020.100118)). I did not attempt the CAPTCHA. I recovered the **complete verbatim abstracts** by other routes.

**(b) Anderson (2014), the time study** — [*Time study examining the effect of range, cage-free, and cage environments on man-hours committed to bird care in 3 brown egg layer strains*](https://doi.org/10.3382/japr.2013-00852), *J. Appl. Poult. Res.* 23(1):108–115.

⚠️ **Abstract only** (recovered verbatim from the [Semantic Scholar record](https://api.semanticscholar.org/graph/v1/paper/DOI:10.3382/japr.2013-00852)); the full text, tables and per-task breakdown were not reachable.

| Housing system | Man-hours per hen housed (17→~89 wk) | Ratio to cage |
|---|---|---|
| Conventional cage (C) | **0.334 h/hen** | 1.00× |
| Cage-free (CF) | **0.486 h/hen** | 1.46× |
| Range (R) | **1.268 h/hen** | 3.80× |

Design: 3-factor randomised design starting at 17 wk — **8 range replicates, 24 cage-free replicates, 4 cage replicates**. Strains: Hy-Line Silver Brown, Hy-Line Brown, Barred Plymouth Rock. All birds reared in the system they would lay in. "Time was recorded for all of the procedures done within the replicates (i.e., egg collection, feeding, and so on)" — the abstract does **not** itemise the task split. Analysis by PROC GLM in SAS.

Two findings that matter for your levers:
- **"Man-hours per hen decreased from 17 to 37 wk in all production systems."** Labour intensity is front-loaded in early lay — consistent with the nest-training walking burden in §2.
- **"Strain alone did not influence man-hours; however, the strain with the poorest livability had the greatest man-hour requirement for hens surviving."** This is the closest thing in the literature to a mortality↔labour coupling, and note the direction: *worse livability raised hours per surviving hen*, which is an accounting artefact of the denominator, not evidence that labour buys survival.

**(a) Brannan & Anderson (2021), the labour-inputs follow-up** — [*Examination of the impact of range, cage-free, modified systems, and conventional cage environments on the labor inputs committed to bird care for three brown egg layer strains*](https://doi.org/10.1016/j.japr.2020.100118), *J. Appl. Poult. Res.* 30(1):100118.

⚠️ **Abstract only** (recovered verbatim from an [archived ScienceDirect landing page](https://web.archive.org/web/20240415105522/https://www.sciencedirect.com/science/article/pii/S1056617120301240); the snapshot contains the abstract but not the body, tables or figures).

Verbatim, the load-bearing sentences:

> "Labor h commitment per hen originally housed and hens surviving were evaluated for 4 different environments: range, cage-free, modified cage, and conventional cage… Data collection began at 33 wk of age and continued until 89 wk in all environments. Range systems demonstrated the highest labor h requirement for both the hens originally housed and hens surviving measurements, particularly during the summer months when pasture management within the paddocks was time consuming. **Conventional and modified cage systems required the least time commitment with cage-free serving as an intermediate. Cage-free labor h increased toward the end of the cycle as maintaining litter quality within the house became more demanding.** The cost of labor h was not offset by the price per dozen eggs produced, and the difference was greater in the extensive systems."

Two usable mechanisms: **cage-free labour rises through the cycle**, and the stated driver is **litter-quality maintenance** — which links your existing `litter_moisture` / `belt_interval_days` machinery directly to a labour lever.

I also downloaded and text-searched the [40th North Carolina Layer Performance and Management Test final report](https://eit-wagpress-prod.s3.amazonaws.com/media/documents/40-NCLPMT-Final-RPT-Vol-40-No-5-Final-_8.29.19.pdf) (the flock these papers used) hoping the raw labour tables were there. **They are not** — zero hits for labor/man-hour/time-study across the full extracted text. The labour data exists only in the two journal articles.

### 1b. ⚠️ Critical caveat: do not use the NC State levels

Converting to a per-hen-year basis, Anderson's cage-free figure is **0.351 h/hen-year** (0.486 h over 17→89 wk ≈ 1.385 yr). Your simulated farm runs **0.036–0.039 h/hen-year** (13–14 FTE × 2,080 h ÷ 750,000 hens). That is a factor of ~9.

This is not an error in either number — it is the difference between small research-station replicates (24 cage-free pens, hand-managed, research protocols) and a mechanised 750,000-bird commercial complex. **Take the NC State work for its ratios and its within-cycle shape, never its levels.**

### 1c. Where the hours actually go — the only real task breakdown

[Matthews & Sumner (2015), *Effects of housing system on the costs of commercial egg production*, *Poultry Science* 94(3):552–557](https://doi.org/10.3382/ps/peu011) — full text open access at [PMC4990890](https://pmc.ncbi.nlm.nih.gov/articles/PMC4990890/). This is the Coalition for Sustainable Egg Supply commercial farm: one farm running a conventional barn, an aviary, and an enriched colony **at the same location with the same accounting**, over 2 flock cycles.

**The task categories the farm actually recorded hours against** (verbatim): *"feed distribution, manure and litter management, equipment maintenance and repair, egg collection, hen health issues, and general housekeeping."* Egg packaging was excluded (all eggs went to breakers). Management labour was allocated separately and added on top.

This is the answer to "where do the hours go on a layer farm" — it is a six-way split, and it is the closest published thing to your inspection-walks / floor-eggs / dead-bird-pickup / records / maintenance decomposition. Note what is **absent**: no separate line for inspection walks, dead-bird pickup, or records. Dead-bird pickup is folded into "egg collection"/"hen health issues"; records are not tracked as labour at all.

The prose itemisation for the aviary:

> "The average labor cost increases from about **6 cents per dozen to more than 8 cents per dozen**. The largest specific labor cost item for the aviary is **egg collection, which increases steadily to over 3 cents per dozen for the last half of the cycle**. In the aviary, workers must collect floor eggs, or eggs laid outside of the nest box, collect dead or dying hens, and generally deal with a more dispersed area for hen care… In addition, hen mortality and other hen health issues are greater in the aviary system and contribute to the higher labor costs… Housekeeping, feed distribution, and hen health issues all entailed more costs per dozen for the 2 alternatives compared with the conventional house."

So for a commercial aviary: **egg collection ≈ 3 of ~7.4 cents/dozen ≈ 40%+ of labour**, and it *grows* through the cycle. Conventional house labour sits flat at ~2 cents/dozen all cycle.

⚠️ The exact per-task percentages live in Figure 2, which is a raster image I could not read; the itemisation above is the authors' prose description of that figure, quoted directly.

Table 4, average operating and capital cost per dozen eggs (read directly from the PMC full text):

| Item ($/dozen) | Conventional | Aviary | Enriched |
|---|---|---|---|
| Feed | 0.425 | 0.436 | 0.417 |
| Pullet | 0.148 | 0.221 | 0.143 |
| **Labor** | **0.019** | **0.074** | **0.056** |
| Energy | 0.014 | 0.015 | 0.014 |
| Miscellaneous | 0.005 | 0.005 | 0.005 |
| **Operating total** | **0.612** | **0.751** | **0.636** |
| vs conventional | — | +23% | +4% |
| Capital (at 10%) | 0.058 | 0.162 | 0.120 |
| **Capital + operating** | **0.670** | **0.913** | **0.756** |
| vs conventional | — | +36% | +13% |

End-of-cycle mortality in the same study: **aviary 13.3%, enriched 5.2%, conventional 4.8%** of pullets placed.

---

## 2. Floor eggs vs walking / collection frequency

This is the best-documented labour→production link in cage-free, exactly as anticipated. The vendor guides give explicit numbers.

### 2a. Hy-Line — the hardest numbers available

[**Understanding Nesting Behavior: Managing for Fewer Floor Eggs in Layers**](https://www.hyline.com/Upload/Resources/TU%20NEST%20ENG.pdf) (Hy-Line International Technical Update, 2020, 10 pp) — **read end to end.**

| Parameter | Recommendation |
|---|---|
| **Walks per day during nest training** | **"the flock manager should walk in the flock a minimum of six times each day, starting from the opposite side of the nest area"** |
| **Training period length** | **Transfer until peak production, "around 27–32 weeks"** |
| Transfer timing | By 16 wk of age, **minimum 14 days before first eggs** |
| Floor eggs during walks | "Any floor eggs should be picked up **immediately**"; hens nesting outside nests "gently placed inside a nest" |
| Baseline floor-egg rate | **"the number of floor eggs will drop to a low level within 2–3 weeks. Floor eggs typically range from 1–4% for the life of a laying flock"** |
| Nest space | 1 m² nest floor per **100–120 hens** (automatic colony); **1 nest per 6 hens** for manual collection |
| Nest opening | Open **2 h before lights on**, closed 2 h before lights off |
| Nest lights | On 1 h before house lights, off 1 h after |
| Litter depth | **< 5 cm (2 in)** during nest training, built up gradually |
| Egg-laying window | **"The majority of eggs are laid 1–5 hours after the house lights are turned on"** |
| House temp during training | 20–21 °C (68–70 °F) or lower, "keeps the hens active and discourages floor eggs" |
| Nest visits per egg | 21.3 nest visits per egg laid (citing Oliveira et al. 2016) |

[**Hy-Line Brown Alternative Systems Commercial Management Guide**](https://hylinena.com/wp-content/uploads/2022/03/BRN-ALT-COM-ENG.pdf) (60 pp). ⚠️ **Partial read** — I read the Nest Training section (pp. 33–35) and the Piling section (p. 37) in full; the remaining ~50 pages were text-searched but not read.

- **"Frequently walk through the barn in the morning for the first 8 weeks after birds are moved to the production barn."** While walking, move birds away from resting areas, out of corners, toward nests.
- **A self-limiting caveat, verbatim: "If you notice that walking is drawing the birds out of the nests, reevaluate this practice."** Walking has a negative marginal return regime. Worth encoding.
- **"Collect floor eggs frequently. Floor egg collection must be done more frequently at the beginning of lay. Birds will lay eggs on the floor if other eggs are present."** — an explicit positive-feedback mechanism: uncollected floor eggs *cause* more floor eggs.
- "Be sure all floor eggs are removed before lights go out at night."
- Evening walking to prevent floor-sleeping; manually place floor birds into the system until trained.
- Nest space: 6 birds per nest or 120 birds per m².

### 2b. Lohmann — softer, but consistent

[**LOHMANN Management Guide for Laying Hens in Deep Litter, Aviary and Free-Range Systems**](https://kenanaonline.com/files/0071/71976/programme_pondeuse_lohmann_eng.pdf) (23 pp). ⚠️ **Partial read** — I read §3.14 Flock control and §3.15 Training the birds in full; the rest (nutrition tables, health) was text-searched only.

- **"Every morning at dawn a thorough tour of inspection is necessary"** — drinkers, feeders, lighting, house climate, flock condition and behaviour.
- **"Immediately after the start of lay multiple inspections are recommended to gather any floor eggs. This helps the hens to get used to the staff while at the same time rapidly reducing the proportion of floor eggs."** Note the dual mechanism: collection *and* habituation to humans.
- **"Floor eggs should be gathered quickly, if necessary several times a day."**
- An **evening** intervention: during the last 30 minutes only the droppings-pit/perch lights remain on; "in the early days after housing of the flock an inspection should be made at this time in order to move manually any hens still remaining in the scratching area. Failure to do this considerably increases the likelihood of floor eggs and the risk that these birds will consume no more water or food that day."
- Litter depth ≤ **2 cm** at the beginning of lay (stricter than Hy-Line's 5 cm).
- Pullets not moved before **17 weeks**; nest boxes opened **10–14 days before start of lay**.

I also reached the current [Lohmann e-guide, Alternative Housing](https://lohmann-breeders.com/e-guide/alternative-housing/) but it added nothing quantitative beyond the PDF. ⚠️ I fetched only page 28, not the whole e-guide.

### 2c. Extension publications

[**UGA Extension C 1254, *Mislaid Egg Management in Cage-Free Hen Houses***](https://fieldreport.caes.uga.edu/publications/C1254/mislaid-egg-management-in-cage-free-hen-houses/) (Chai, UGA CAES) — **read in full** (body text; the figures are images).

- **"The percentage of floor eggs… can be as high as 10% on cage-free egg farms. Any mislaid eggs… increase labor costs because they must be collected manually by farm workers every day."**
- **"Increasing the light intensity under the aviary system has been tested to be effective at reducing over 80% of floor eggs."** The specific case: a commercial Iowa cage-free farm where light beneath the aviary was 5 lx vs 20 lx on open floor; hens laid beneath the aviary; adding lights underneath largely fixed it. ⚠️ This is reported as a farm's shared experience, not a controlled trial.
- "Most floor eggs are laid at first light, and delaying floor access time in the morning may help reduce floor eggs."
- UEP cage-free guide (2017): minimum **15%** of total space as litter.

### 2d. ⚠️ The gap you should know about

**No source I found quantifies floor-egg % *with vs without* diligent early-lay walking.** The recommendation is universal and the mechanism is well-described, but the controlled comparison does not appear to exist in the published literature. What exists instead:

- Baseline rates: **1–4%** lifetime (Hy-Line, well-managed), **up to 10%** on cage-free farms (UGA), **10–15%** cited in secondary summaries ⚠️ (I could not trace the 15% figure to a primary source).
- A quantified *substitute* lever: **>80% floor-egg reduction from lighting under the aviary** (UGA, single-farm).
- An indirect labour effect from [Herbert et al. 2023](https://doi.org/10.1016/j.psj.2023.102939) — see §3 — where more producer walk-throughs plausibly reduced Grade B eggs via more frequent floor-egg collection.

If you need a walking→floor-egg dose-response for the model, you will be **interpolating**, not citing. I would build it off Hy-Line's "minimum six times each day" as the reference policy and the 1–4% vs 10% band as the well-managed/neglected endpoints, and label it as a construct.

---

## 3. Piling and smothering — does human presence interrupt it?

**Honest headline: the evidence that intervention works is weak, and one dataset argues against it.**

### 3a. Barrett et al. 2014 — the industry-scale survey

[**Smothering in UK free-range flocks. Part 1: incidence, location, timing and management**](https://doi.org/10.1136/vr.102327), *Veterinary Record* 175(1):19. Barrett J, Rayner AC, Gill R, Willings TH, Bright A.

⚠️ **Abstract only** (recovered verbatim from the [PubMed record, PMID 24836430](https://pubmed.ncbi.nlm.nih.gov/24836430/)); the full Vet Record text is paywalled behind Wiley, including the questionnaire counts and the breakdown by smothering type.

Verbatim numbers:

> "…a questionnaire addressing the incidence, location, timing and management of smothering of free-range farm managers from two commercial egg companies (**representing 35 per cent of the UK free-range egg supply**). Overall, **nearly 60 per cent of farm managers experienced smothering in their last flock, with an average of 25.5 birds lost per incidence**, although per cent mortality due to smothering was low (**x̄ = 1.6 per cent**). The majority of farm managers also reported that **over 50 per cent of all their flocks placed had been affected by smothering**. The location and timing of smothering (excluding smothering in nest boxes) **tended to be unpredictable and varied between farms**. **Blocking off corners/nest boxes and walking birds more frequently were identified as popular smothering reduction measures**, although there was a wide variety of reduction measures reported overall… The results suggest that smothering is a common problem, **unpredictable between flocks with no clear, effective reduction strategies**."

So: walking more is what producers *do*, and the same paper concludes there is **no clear effective strategy**. Popularity is not efficacy.

Related figure, cited secondhand ⚠️: Nicol (2015) is cited by Herbert et al. as suggesting smothering "could account for around **one sixth of mortalities** across the UK industry annually." I did not reach Nicol (2015) directly.

Follow-up: [**Rayner et al. 2016, Part 2**](https://doi.org/10.1136/vr.103701), *Veterinary Record* 179:252. ⚠️ **Not read** — paywalled; I have only search-result summaries indicating breed (P=0.008) and nest-box manufacturer (P=0.014) predicted nest-box smothers, and nest-box manufacturer (P=0.009), feeding oyster grit/grain on litter (P<0.001) and range use on a sunny day (P<0.001) predicted panic/recurring smothers. **I have not verified these numbers against the source and would not put them in a model without doing so.**

### 3b. Campbell et al. 2016 — the 174-event commercial aviary study

[**Litter use by laying hens in a commercial aviary: dust bathing and piling**](https://doi.org/10.3382/ps/pev183), *Poultry Science* 95(1):164–175. ⚠️ **Partial read** — I read the abstract, the full Piling results section and the opening of the Discussion from the [PDF](https://pdfs.semanticscholar.org/985b/d15607893b15d75efb9b2ea93571e900d42b.pdf); the dust-bathing results and later discussion were skimmed only.

Setting: two flocks of **Lohmann White** hens, ~49,000 birds/flock, commercial US tiered aviary, observed at peak / mid / end lay.

| Measure | Value |
|---|---|
| Total piles observed | **174** (Flock 1: 66; Flock 2: 108) |
| Duration range | **1 min to 359 min** |
| Peak pile size | **10 to ~229 hens** |
| Mean pile size, double rows | 86.9 ± 6.8 (F1); 73.8 ± 14.7 (F2) |
| Mean pile size, single rows | 33.5 ± 2.7 (F1); 32.3 ± 3.4 (F2) |
| **Smothering detected** | **None. "no hen death was observed following piling"** |
| Location | Predominantly by the gate or against the wall |
| Timing | Throughout the day whenever hens had litter access; no predictable time |

**The intervention-relevant sentence, verbatim:**

> "Finally, **all piles, with the exception of 3 that appeared to end due to a sudden disturbance, eventually just dissolved, with hens leaving one by one for no discernible reason.**"

**3 out of 174 piles (1.7%) ended because of a disturbance.** Everything else self-resolved. If you want a defensible prior for "does walking break up a pile," this is it, and it is close to zero.

### 3c. Herbert et al. 2023 — the largest piling dataset, and the confound

[**The effect of piling behavior on the production and mortality of free-range laying hens**](https://doi.org/10.1016/j.psj.2023.102939), *Poultry Science*, full text at [PMC10465951](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10465951/). ⚠️ **Partial read** — abstract, introduction and the Grade B discussion passage read in full; methods detail, Bayesian model specification and full results tables skimmed.

Design: video from **12 flocks** analysed (13 recorded; UK free-range, flat-deck, Cumbria; Lohmann Classic and Shaver Brown; 3,000–16,000 birds; 16–58 wk), **252 days ≈ 15,624 hours** of footage — "the largest analysis of piling behavior in the scientific literature to date."

| Finding | Value |
|---|---|
| Flocks exhibiting piling | **All of them** — "even if they had no history of smothering" |
| Piling frequency | **>4 times per day** on average |
| Mean event duration | **~44 min** |
| Peak time | **13:00–13:59** |
| Effect on next-day production | **−7.35 eggs per 1,000 birds per day** (at the average 4 piles/day) |
| Effect on Grade B eggs | **−0.74 Grade B eggs per hour of piling per day** (i.e. *fewer* downgrades — opposite of hypothesis) |
| **Effect on non-smothering mortality** | **None detected** |
| Pile density (earlier case study) | up to **188 birds/m²**, up to **1,204 birds** in one pile |

Two passages that bear directly on your lever design:

**The confound, verbatim:** *"the primary management strategy for creeping smothers is walking through the birds to disperse them (Barrett et al., 2014), and as such, the timing of piling behavior might be linked to the timing of these walk throughs."* The authors are explicitly raising the possibility that **walking entrains the piling rhythm** rather than suppressing it.

**The labour→quality link, verbatim:** the unexpected *reduction* in Grade B eggs with more piling *"may be… due to an increase in the number of times the producer walks through the birds (to break up the piling), resulting in more frequent collection of floor eggs and therefore decreasing the likelihood"* of downgrades. That is a walking → floor-egg-collection → egg-grade pathway, offered as an explanation rather than a measured effect.

### 3d. Vendor guidance says walking helps

[Hy-Line Brown Alternative Systems guide](https://hylinena.com/wp-content/uploads/2022/03/BRN-ALT-COM-ENG.pdf), p. 37, verbatim — **label this a vendor recommendation, not evidence:**

> "Birds may pile without a discernible cause, resulting in suffocations. Identifying time periods when birds tend to gather or pile can provide important clues to identify the reason for piling. **Walking in the flock during these times may prevent piling and smothering.**"

Listed causes: panic from predators/rodents, hot or poorly ventilated areas, sunlight beams on the floor, search for a nesting area, high light intensity or sudden lighting changes, light flicker (e.g. generator test), and **"human or other activity that attracts the birds to gather in one location"** — note that human activity is listed as a *cause*. Non-labour countermeasures given: round off corners, place pallets in known piling areas, install nest partitions, play music, feed in the afternoon before lights out.

### 3e. Supporting review material

[**Laying Hens: Why Smothering and Not Surviving? — A Literature Review**](https://doi.org/10.3390/ani14111518), *Animals* 14(11):1518, full text at [PMC11171085](https://pmc.ncbi.nlm.nih.gov/articles/PMC11171085/). ⚠️ **Partial read** — I read §5.4 (Effects of Human–Animal Management and Interaction) in full; the rest was text-searched.

§5.4 is qualitative throughout. It lists what handlers spend time on in cage-free ("opening/closing gates for paddocks, assisting animals in using unoccupied nests (especially in the first weeks of laying), gathering floor eggs, and dispersing animals when they exhibit variations in normal behavior"), notes that **"birds can find human presence in the barn either comforting or stressful, depending on how they interact,"** and states that **"85% of the total laying for a flock occurs in the morning."** It offers **no quantitative estimate of intervention efficacy.**

[**Why Do Hens Pile? Hypothesizing the Causes and Consequences**](https://doi.org/10.3389/fvets.2020.616836), *Frontiers in Veterinary Science* 7:616836 (Gray et al.). ⚠️ **Text-searched only, not read.** Relevant passage found: farm routine — including "farmers may walk through the sheds at specific points during the day" — is proposed as a driver of *when* hens access litter and therefore *when* they pile.

### 3f. Recommended modelling stance

Encode walking as buying **floor-egg collection and early detection**, not pile prevention. If you want a smothering lever at all, make its effect small and uncertain, and consider making over-walking mildly counterproductive — both Hy-Line ("if walking is drawing the birds out of the nests, reevaluate") and Herbert et al. (walking may set the piling clock) support a non-monotonic response.

---

## 4. Per-person-hour rates for surge tasks

### 4a. End-of-lay catching — solid, layer-specific, peer-reviewed

[**Upright versus inverted catching and crating end-of-lay hens: a trade-off between animal welfare, ergonomic and financial concerns**](https://doi.org/10.1016/j.psj.2024.104144), *Poultry Science*, full text at [PMC11364121](https://pmc.ncbi.nlm.nih.gov/articles/PMC11364121/). ⚠️ **Partial read** — abstract, cost methodology, and results/discussion read in full; the ergonomics (NIOSH/ART/MAC) methods sections skimmed.

Design: **7 commercial farms** (1 floor system, 6 aviary systems), **~3,000 hens per method per flock**, 148 catchers total across the study.

| Method | Person-hours per 1,000 hens | Implied hens per person-hour |
|---|---|---|
| **Inverted (conventional)** | **4.8 ± 2.0 h** | **~208** (range ~147–357 at ±1 SD) |
| **Upright (welfare-improved)** | **8.2 ± 3.2 h** | **~122** |

Difference: *P* = 0.011; **+3.4 person-hours per 1,000 hens**, "with the same workforce the task took **70% longer**."

Costs, at the study's standard prices (**labour €40/h/person**, forklift €70/h, transport €75/h):

| | Inverted | Upright | Ratio |
|---|---|---|---|
| Labour per 1,000 hens | **€206.5** | **€369.4** | 1.8× |
| Forklift per 1,000 hens | €17.5 | €27.8 | 1.6× |
| Truck loading per 1,000 hens | €18.8 | €29.8 | 1.6× |
| **Total, 20,000 hens** | **€4,506** | **€7,984** | +€3,478 |
| Per egg equivalent | €0.0006 | €0.0011 | +€0.0005 |

Welfare deltas for the extra labour (this is a clean welfare-vs-cost decision node if you want one): wing flapping **3.1 ± 0.6 vs 4.0 ± 0.5** (7-point scale, *P* < 0.001), handling gentleness **1.9 ± 0.5 vs 4.4 ± 0.5** (*P* < 0.001), wing bruises **1.1 ± 0.6% vs 1.7 ± 0.7%** (*P* = 0.04).

Constraint worth encoding: **NIOSH limits catchers to lifting ~1 kg (unfavourable) to 1.5–2 kg (favourable)**, i.e. "a maximum of two hens at a time for both inverted and upright catching methods" — though inverted catching in practice takes 5–6 birds per catch vs 2 upright. The paper also notes **"there is a shortage of catchers in the poultry industry"** and that a larger team "may negatively affect efficiency of the catch."

**Applied to your farm:** depopulating 750,000 hens at 4.8 person-h/1,000 ≈ **3,600 person-hours** (inverted), or ~6,150 person-hours upright. Against a 13–14 FTE crew that is 32–55 crew-days of pure catching — this is unambiguously a contract-crew surge, not an in-house task.

⚠️ Note the geography: this is a European study, €-denominated, at €40/h/person (a fully loaded contractor rate, not a US farm wage). The *hours* transfer; the *costs* do not.

### 4b. Broiler catching — context only

The widely quoted figure is **up to 1,500 birds per man-hour** for manual broiler house depopulation. ⚠️ **I could not read the source.** It traces to [*Catching, handling and loading of poultry for road transportation*, World's Poultry Science Journal (Cambridge Core)](https://doi.org/10.1079/WPS20050047), which is paywalled; I have it only from search-result text. Treat as unverified. Note it is ~7× the layer rate above, which is plausible (broilers in an open floor house vs hens dispersed through a multi-tier aviary) but should not be transferred to layers.

### 4c. Vaccination crew rates — thin, and vendor-sourced

⚠️ **No peer-reviewed birds-per-person-hour rate for manual layer vaccination was found.** The only quantified figure I located is a **vendor claim**: Ceva's [IMVAC Safe automated system](https://poultrycontent.ceva.com/precision-matters-tackling-quality-issues-in-on-farm-vaccination) is advertised at **up to 1,200 birds per hour**, and that is machine-assisted throughput with an operator, not a manual per-person rate. Industry sources describe pullet vaccination as done by dedicated crews (company-employed or contracted) and note that **fatigue degrades vaccination quality and handling precision as the day progresses** — a usable qualitative mechanism for an overtime lever, but not a calibrated one.

### 4d. House cleanout / disinfection — a genuine gap

⚠️ **No usable published person-days-per-house figure exists that I could find.** Extension and trade material ([UConn Extension, *Cleaning and Disinfecting Your Poultry House*](https://animalscience.cahnr.uconn.edu/wp-content/uploads/sites/3396/2022/06/poultry-extension_4_1495055080.pdf); WATTAgNet cleanout articles) describe the *steps* — dry clean, wash, disinfect, downtime — without labour quantities. The only recurring quantitative element is **downtime: a minimum of 2 weeks between flocks**, with some analyses assuming 4 weeks. If you need a cleanout labour number you will have to construct it; say so in the model documentation.

### 4e. Pullet placement rates — not found

⚠️ **No published birds-per-person-hour rate for pullet placement/transfer was located.** By symmetry with catching (placement is catching in reverse, into a system rather than into crates), the 122–208 hens/person-hour band is the most defensible available proxy, but it is my inference, not a sourced figure.

---

## 5. The cage-free labour multiple

### 5a. The trade claim

[**"Cage-free egg production requires 3 to 5 times more labor," WATTAgNet**](https://www.wattagnet.com/egg/cage-free-laying-systems/article/15524963/cage-free-egg-production-requires-3-to-5-times-more-labor-wattagnet).

⚠️ **Unreachable.** WATTAgNet hard-403s every route I tried (direct fetch, browser user-agent, Google referer, reader proxy), and the Internet Archive availability API rate-limited me (HTTP 429) on repeated attempts. **I have not read this article.** From search-result text only, it reports a consensus of cage-free farm managers at the **Egg Industry Center Issues Forum, Scottsdale, Arizona (2018)**, with the multiple varying by cage-free housing type. That makes it a **trade-press report of a practitioner panel** — anecdote aggregated at an industry meeting, not measurement.

### 5b. The primary source that actually grounds it

You do not need the trade article. [**Matthews & Sumner (2015)**](https://doi.org/10.3382/ps/peu011) is the primary, peer-reviewed, single-farm, same-accounting measurement, and it lands squarely inside the 3–5× band:

- **Labour cost per dozen: $0.019 conventional vs $0.074 aviary = 3.9×**; enriched $0.056 = 2.9×.
- The authors state it as an hours claim, verbatim: *"The aviary and the enriched housing system both have higher costs of more than 4 cents per dozen—**more than triple the labor use compared with the conventional house. Cost differences across houses derive from more labor per dozen eggs because wage rates are the same for each house.**"*

That last clause is what makes this citable as a *labour* multiple rather than a cost multiple. **This is the primary source the trade claim needs, and it should replace it in your documentation.**

### 5c. The tension between the two literatures

| Source | Setting | Cage-free : conventional labour |
|---|---|---|
| [Matthews & Sumner 2015](https://doi.org/10.3382/ps/peu011) | Commercial farm, 3 houses, same accounting | **3.9×** |
| [Anderson 2014](https://doi.org/10.3382/japr.2013-00852) | NC State research station, small replicates | **1.46×** (range vs cage: 3.80×) |
| WATTAgNet 2018 ⚠️ unread | Producer panel consensus | 3–5× |

The research-station study finds cage-free only ~1.5× conventional; its "3 or 4 times" conclusion is driven by **range**, not cage-free. The commercial study finds cage-free ~3.9×. If a model needs one number, **use the commercial figure (~4×)** and note the research-station discrepancy — the likely explanation is that research pens are hand-managed in every system, compressing the mechanisation gap that dominates commercial conventional houses.

### 5d. University / extension budget material

[**Purdue Extension AS-646-W, *Cage-free Egg Production: Benefits and Challenges***](https://www.extension.purdue.edu/extmedia/AS/AS-646-W.pdf). ⚠️ **Text-searched, not read end to end.** It is qualitative on labour — identifies "labor to collect eggs" as a named cost of cage-free because "nest boxes are available… [but hens lay floor eggs], requiring additional labor to collect eggs" — and cites Sumner et al. (2011) for the economics. **No labour line with hours or dollars.**

⚠️ **I did not locate a US university enterprise budget for cage-free egg production with an explicit labour line** (searched Iowa State, Purdue, UC Davis, Egg Industry Center). The Egg Industry Center's cost-of-production series is referenced widely in secondary sources (e.g. total cost $0.644/dozen conventional vs $0.908 cage-free) but I did not reach a primary EIC document, so **I am not asserting those figures.** Matthews & Sumner's Table 4 above is the primary-source substitute and is more granular anyway.

---

## 6. Synthesis — a usable labour production function

**Level (what one hour buys, commercial aviary):** derived from Matthews & Sumner Table 4. ⚠️ *The conversion below is my arithmetic, not the paper's*, and depends on two assumptions I supplied: ~22 dozen eggs per hen-year and a wage rate.

| System | Labour $/dozen | Implied h/hen-year at $12/h | at $15/h | at $18/h |
|---|---|---|---|---|
| Conventional | $0.019 | 0.035 | 0.028 | 0.023 |
| Enriched | $0.056 | 0.103 | 0.082 | 0.068 |
| **Aviary** | **$0.074** | **0.136** | **0.109** | **0.090** |

**Your simulated farm sits at 0.036–0.039 h/hen-year** (13–14 FTE × 2,080 h ÷ 750,000). That is roughly **⅓ of the commercial aviary benchmark** and about equal to a *conventional cage* house. Two readings, and you should pick one deliberately:

- If 13–14 FTE is meant to be a highly-mechanised complex at the efficient frontier, it is defensible but tight, and it means the farm has **very little slack** — which is exactly what makes a staffing/overtime lever bite.
- If it is meant to be typical, it is roughly **2–3 FTE-equivalents short per 100k birds** versus benchmark, and you may want to raise it or narrate the leanness explicitly.

Note Matthews & Sumner's labour includes management, maintenance and housekeeping but excludes egg packaging, so the comparison to "direct bird-care crew" is not exact and the true gap is somewhat smaller than 3×.

**Shape (how the hours are distributed):**

| Task | Evidence | Model hook |
|---|---|---|
| **Egg collection (incl. floor eggs)** | Largest aviary line; >3 c/dozen in back half, ~40%+ of labour ([M&S](https://doi.org/10.3382/ps/peu011)) | Scales with floor-egg %; positive feedback (uncollected eggs beget floor eggs, Hy-Line) |
| **Litter/manure management** | Named driver of the end-of-cycle rise ([Brannan & Anderson](https://doi.org/10.1016/j.japr.2020.100118)) | Couple to your existing `litter_moisture` / `belt_interval_days` |
| **Inspection walks** | 6×/day minimum during nest training, ~8 weeks post-transfer (Hy-Line) | Front-loaded: falls after peak (~27–32 wk) |
| **Hen health / dead-bird pickup** | Named cost line; aviary mortality 13.3% vs 4.8% conventional (M&S) | Scales with mortality, not the reverse |
| **Maintenance, feed distribution, housekeeping** | Named lines, "relatively higher" in aviary (M&S) | Roughly fixed per house |
| **Records** | Not tracked as labour in any source | Don't model as an hours sink |

**Within-cycle profile:** hours per hen **fall** from 17→37 wk ([Anderson](https://doi.org/10.3382/japr.2013-00852)) as nest training ends, then **rise again toward the end** as litter management gets harder ([Brannan & Anderson](https://doi.org/10.1016/j.japr.2020.100118)); aviary labour cost tracks this, ~6 → 8+ c/dozen ([M&S](https://doi.org/10.3382/ps/peu011)). A U-shape, front-loaded on walking and back-loaded on litter.

**Surge rates:** catching **208 hens/person-hour** inverted, **122** upright ([PMC11364121](https://pmc.ncbi.nlm.nih.gov/articles/PMC11364121/)). Everything else in the surge category — vaccination, cleanout, placement — is uncalibrated in the published literature and would be a construct.

**What labour does NOT buy, on the evidence:** pile/smother prevention. 3 of 174 piles ended from disturbance ([Campbell](https://doi.org/10.3382/ps/pev183)); the industry survey found no effective strategy despite walking being the popular one ([Barrett](https://doi.org/10.1136/vr.102327)); and the largest video dataset found **no association between piling and non-smothering mortality** and raised walking as a possible *cause* of the timing pattern ([Herbert](https://doi.org/10.1016/j.psj.2023.102939)).

---

## COVERAGE STATEMENT

**Read end to end, from the source, in this session:**
- [Hy-Line Technical Update, *Understanding Nesting Behavior: Managing for Fewer Floor Eggs in Layers*](https://www.hyline.com/Upload/Resources/TU%20NEST%20ENG.pdf) — all 10 pages.
- [UGA Extension C 1254, *Mislaid Egg Management in Cage-Free Hen Houses*](https://fieldreport.caes.uga.edu/publications/C1254/mislaid-egg-management-in-cage-free-hen-houses/) — full body text (figures are images and were not read).
- [40th NC Layer Performance and Management Test final report](https://eit-wagpress-prod.s3.amazonaws.com/media/documents/40-NCLPMT-Final-RPT-Vol-40-No-5-Final-_8.29.19.pdf) — full text extracted and searched; **contains no labour data** (negative result, complete).
- Verbatim complete abstracts of [Anderson 2014](https://doi.org/10.3382/japr.2013-00852), [Brannan & Anderson 2021](https://doi.org/10.1016/j.japr.2020.100118), [Barrett et al. 2014](https://doi.org/10.1136/vr.102327), and [Matthews & Sumner 2015](https://doi.org/10.3382/ps/peu011).

**Opened and read in substantial part — ⚠️ NOT end to end:**
- [Matthews & Sumner 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4990890/) — read the labour-methods, labour-results, and Tables 2/4 sections in full; feed/capital/energy sections and Figure 2 (raster image, per-task itemisation) not read.
- [PMC11364121, upright vs inverted catching](https://pmc.ncbi.nlm.nih.gov/articles/PMC11364121/) — abstract, cost methods, results, discussion read; ergonomics methods skimmed.
- [Campbell et al. 2016](https://pdfs.semanticscholar.org/985b/d15607893b15d75efb9b2ea93571e900d42b.pdf) — abstract, Piling results, Discussion opening read; dust-bathing results skimmed.
- [Herbert et al. 2023](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10465951/) — abstract, introduction, Grade B discussion read; methods/model specification and results tables skimmed.
- [Hy-Line Brown Alternative Systems guide](https://hylinena.com/wp-content/uploads/2022/03/BRN-ALT-COM-ENG.pdf) — Nest Training (pp. 33–35) and Piling (p. 37) read in full; remaining ~50 pages text-searched only.
- [Lohmann Management Guide, alternative systems](https://kenanaonline.com/files/0071/71976/programme_pondeuse_lohmann_eng.pdf) — §3.14 and §3.15 read in full; remaining 20 pages text-searched only.
- [*Why Smothering and Not Surviving?* review, PMC11171085](https://pmc.ncbi.nlm.nih.gov/articles/PMC11171085/) — §5.4 read in full; rest text-searched.
- [Purdue AS-646-W](https://www.extension.purdue.edu/extmedia/AS/AS-646-W.pdf), [Lohmann e-guide p. 28](https://lohmann-breeders.com/e-guide/alternative-housing/28/), [*Why Do Hens Pile?*](https://doi.org/10.3389/fvets.2020.616836) — text-searched only, not read.
- [Hy-Line W-80 Aviary and Barn guide](https://hylinena.com/wp-content/uploads/2019/10/80_Alt_ENG.pdf) — downloaded and extracted, not read (superseded by the Brown guide for this purpose).

**⚠️ Unreachable — no claim in this report rests on unread content from these:**
- **Full texts of both JAPR labour papers** ([S1056617119303678](https://www.sciencedirect.com/science/article/pii/S1056617119303678), [S1056617120301240](https://www.sciencedirect.com/science/article/pii/S1056617120301240)). ScienceDirect serves a CAPTCHA to browsers and 403s to fetchers. Both are CC-BY-NC-ND but Elsevier is the sole OA host — no repository, PMC, DOAJ-hosted, or Internet Archive Scholar copy exists. **To reach these you need institutional ScienceDirect access or an interlibrary request.** They are the only place the per-task hour tables live.
- **[WATTAgNet "3 to 5 times more labor"](https://www.wattagnet.com/egg/cage-free-laying-systems/article/15524963/cage-free-egg-production-requires-3-to-5-times-more-labor-wattagnet)** — 403 on every route; Wayback API rate-limited (429). Not read. Superseded in this report by Matthews & Sumner.
- **[Barrett et al. 2014 full text](https://doi.org/10.1136/vr.102327)** and **[Rayner et al. 2016 Part 2](https://doi.org/10.1136/vr.103701)** — Wiley/Vet Record paywall. Abstract only for Part 1; **for Part 2 I have only search-result summaries, which I have not verified and flag as unverified in §3a.**
- [WPSJ *Catching, handling and loading of poultry for road transportation*](https://doi.org/10.1079/WPS20050047) — Cambridge Core paywall; the "1,500 birds per man-hour" figure is unverified.
- [MDPI *Manual Catching and Transportation of Poultry*](https://doi.org/10.3390/poultry5020030) — 403 on both HTML and PDF.
- Nicol (2015), the "one sixth of UK mortalities" source — cited secondhand via Herbert et al. only.
- A primary Egg Industry Center cost-of-production document, and any US university cage-free enterprise budget with a labour line — searched, not located.

**Confirmed gaps in the published literature (not access failures):** floor-egg % with vs without diligent early-lay walking; manual vaccination birds-per-person-hour; house cleanout person-days; pullet placement rates; and any percentage decomposition of layer-farm hours into inspection walks / dead-bird pickup / records. Matthews & Sumner's six task categories are the closest published approximation.

---

## Addendum — owner-fetched full texts (2026-08-07, orchestrator-read)

The owner fetched the paywalled sources by browser; PDFs are filed under
`evals/hen/research/sources/`. Both JAPR papers and both WATTAgNet articles are now **read end to
end by the orchestrator** (not the subagent). What the full texts add or change:

### A1 · Anderson 2014 read in full (`sources/anderson-2014-time-study.pdf`)

- The abstract-only table stands. Full-cycle man-hours (17→~85 wk, hen-HOUSED basis): cage
  **0.334**, cage-free **0.486**, range **1.268** h/hen; on a hen-SURVIVING basis **0.351 / 0.520 /
  1.512**. Paper's own conclusions: **+45% cage→cage-free, +279% cage→range, +161% CF→range**.
- **The cage-free premium is concentrated in peak lay:** CF exceeded cage significantly only from
  **21 to 61 wk** — the paper attributes it to egg-collection burden (cage rows were hand-collected
  twice daily at peak; CF nest eggs rolled into trays once daily). Per-period CF labour ran
  ~0.02–0.045 h/hen per 28-day period.
- **The Bell & Weaver 0.03 figure, read in context:** "the labor input on a per-hen basis continued
  to decline to about 0.03 h/hen in a 1 million hen complex [10 = Bell & Weaver 2002]." The
  surrounding sentences all use life-of-flock h/hen (2.6 h/hen "for the life of the flock"), so the
  parallel construction reads as **per cycle, not per year** — which finally answers §11 G's open
  unit question. Our complex at 13–14 FTE ≈ 0.05 h/hen per ~1.4-yr cycle, the right order against
  that benchmark. (⚠️ Bell & Weaver itself remains unread; this is the quoting sentence read in
  full context, not the original.)
- **System caveat:** this study's "cage-free" is single-tier slat-litter floor PENS (216 hens/pen),
  not a multi-tier aviary. Use its ratios and time-shape, never its levels — unchanged from §1b.

### A2 · Brannan & Anderson 2021 read in full (`sources/brannan-anderson-2021-labor-inputs.pdf`)

- Exact Table 2 (33→89 wk, so the front-loaded nest-training phase is OUTSIDE its window):
  conventional cage **0.057**, modified cage **0.051**, cage-free **0.090**, range **0.149** h/hen
  housed (survived: 0.064 / 0.058 / 0.100 / 0.150). Within-study CF:CC = **1.6×**.
- Labour cost at the $7.25/h federal minimum (their standard): CC **$0.27/doz** vs CF **$0.39/doz**
  vs range $0.56/doz (Table 3).
- The end-of-cycle rise is confirmed in the results text: CF labour "increase[d] toward the end of
  the trial owing to increased labor required for litter management within the system" — the direct
  hook to our `litter_moisture` machinery. CF per-period labour fluctuated ~0.05–0.13 h/hh.
- Same system caveat: CF = 60-hen slat-litter pens in a high-rise house, not an aviary.

### A3 · WATTAgNet "3 to 5 times more labor" read in full (`sources/wattagnet-cage-free-3-5x-labor.pdf`)

Confirmed as a producer-panel consensus, now with the provenance pinned: Egg Industry Center
Issues Forum, Scottsdale, **18 April 2018**; panelists Dan Krouse (Midwest Poultry Services),
Darrin Eckard (Iowa Cage Free), Brett Pickar (Daybreak Foods), Mike Gemperle (Gemperle Family
Farms). "The consensus answer was **three to five times more labor**, depending on the type of
cage-free housing system used." Two usable details: **aviaries with doors that confine hens early
in the day reduce labour needs because they reduce floor eggs**, and pullets must be reared in a
system matching the layer aviary or floor-egg labour rises.

### A4 · WATTAgNet "5 cage-free aviary facts" read in full (`sources/wattagnet-5-aviary-facts.pdf`)

Correction recorded at the companion doc (`2026-08-07-overtime-realism-and-law.md` §1.5): the
**32,000–50,000 birds-per-worker figure is not in the article** (search-summary artifact,
withdrawn). What it does contain: Potter's Poultry vendor estimate of **0.2 labour-hours per day
per 1,000 birds housed** in its systems; manufacturer-survey consensus of **"two to four times
more labor than cage systems"**; Big Dutchman: doors held until after the morning lay put **~90%
of manure on the belts** and sharply cut floor eggs, reducing labour; Val-Co: "The increase in
labor is normally proportional to the level of bird training desired."

### A5 · Still outstanding

- **Dembe et al. 2005 full text** — not among the fetched PDFs; confidence intervals and the
  >8 h/day hazard ratio remain unobtained.
- `sources/mdpi-poultry-manual-catching-2026.pdf` (MDPI *Manual Catching and Transportation of
  Poultry*) — ⚠️ filed, **not yet read**; relevant to §4's catching rates if the build lane wants a
  second source.
