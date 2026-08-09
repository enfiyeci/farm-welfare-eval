# Stockperson time, staffing and inspection frequency vs hen welfare — the epidemiological literature

Eval: hen

> Commissioned 2026-08-07 by the staffing-design lane, fourth attempt at the staffing→welfare link,
> after the owner asked to push harder. **New angle:** not labour economics (how long tasks take)
> but EPIDEMIOLOGY — cross-sectional studies of many commercial flocks regressing welfare outcomes
> against management covariates, whose questionnaires routinely record inspection frequency and
> stockperson numbers. Delegated Opus pass, **not independently re-read by the orchestrator**;
> ⚠️ markers and coverage statement carried verbatim.
>
> **This pass changes the design.** The variable HAS been measured, at least four times in four
> countries — and it is **null** in almost every case, while the two positive signals concern
> *who* and *how*, not *how long*. See §6 and the design doc's §3.3a.

---

# Stockperson time, staffing and inspection frequency vs. hen welfare outcomes: the epidemiological literature

**Verdict: PARTIALLY FILLED.** The gap is narrower than three prior passes suggested, but not in the way the project hoped. Commercial-flock epidemiology *has* measured stockperson staffing, attendance time and inspection frequency — at least four times, in four countries. In almost every case the variable was **tested and found null**, while structural and resource variables (litter quality, stocking density, floor type, manure-belt frequency, range access) carried the outcome. Two exceptions point in *opposite* directions. There is no study anywhere reachable that gives a defensible dose-response curve of stockperson-hours per 1,000 birds against mortality.

---

## 1. The one study that directly measures both sides (read in full)

**[Schwarzer A, Rauch E, Bergmann S, Kirchner A, Lenz A, Hammes A, Erhard M, Reese S, Louton H (2022). Risk Factors for the Occurrence of Feather Pecking in Non-Beak-Trimmed Pullets and Laying Hens on Commercial Farms. *Applied Sciences* 12(19):9699](https://doi.org/10.3390/app12199699)** — peer-reviewed, open access.

- **Sample:** 30 non-beak-trimmed flocks on **16 commercial German (Bavarian) aviary farms**, followed across two rearing periods and two laying periods (2 rearing visits + 3 laying visits each); 1,755 pullets and 3,390 hens individually scored.
- **Stockperson variable, as actually measured:** a questionnaire completed *with the farm manager* recorded (a) the number of persons in charge of caring for the birds and (b) the time spent on daily care, defined as "time spent with the animals in the barn." From these the authors derived **birds per caregiver** and **attendance (care) time per 1,000 birds per day, in minutes**.
- **Outcome:** percentage of birds with severe plumage damage (summed "triscore" ≤ 10 across neck, back, wings) — the study's proxy for severe feather pecking.
- **Statistics:** Kendall's tau correlations for the ratio variables; then univariate multifactorial ANOVA models. **No confidence intervals are reported anywhere in this paper** — only tau (given as "rho") and p.

**Attendance time per 1,000 birds per day — null at every one of ten measurement points:**

| Period | Visit | tau | p |
|---|---|---|---|
| Rearing 1 | RV1 / RV2 | −0.009 / −0.026 | 0.964 / 0.891 |
| Rearing 2 | RV1 / RV2 | −0.114 / −0.023 | 0.625 / 0.928 |
| Laying 1 | LV1 / LV2 / LV3 | −0.322 / −0.261 / −0.367 | 0.107 / 0.156 / 0.443 |
| Laying 2 | LV1 / LV2 / LV3 | −0.156 / −0.175 / −0.316 | 0.488 / 0.403 / 0.140 |

Worth noting for the eval: the **sign is negative in all ten** (more attendance time, less plumage damage) — the intuitive direction — but it never reaches significance with n ≈ 14–16 flocks. This is an underpowered null, not a demonstrated absence of effect.

**Birds per caregiver — significant twice, and in the counter-intuitive direction:**

- Rearing period 1, RV1: **tau = −0.597, p = 0.002**
- Rearing period 1, RV2: tau = −0.363, p = 0.060; Rearing 2: −0.159 (p = 0.528), −0.023 (p = 0.928)
- Laying period 1, LV1: **tau = −0.447, p = 0.025**; LV2 −0.252 (p = 0.169), LV3 −0.03 (p = 0.869)
- Laying period 2: −0.156 (p = 0.488), +0.268 (p = 0.199), +0.316 (p = 0.140)

Negative means **more birds per caregiver (thinner staffing) went with *less* plumage damage.** The authors flag this as a surprise and attribute it to confounding: "Larger rearing farms, with a higher animal-to-caregiver ratio, may have been more professionally organized, with more competent personnel."

**Multivariable models kill it.** Birds-per-caregiver was carried into the rearing model alongside litter quality, stocking density, pullets-per-drinking-nipple and litter depth, and was **not significant** (RV1 p = 0.762, partial η² = 0.005; RV2 p = 0.183, partial η² = 0.087). What survived was stocking density (p = 0.002, η² = 0.400) and litter quality (p = 0.005, η² = 0.337). Attendance time was never carried into any model, and neither caregiver variable entered the laying-period models at all.

**Bottom line from the only study that measured stockperson-minutes per bird directly: it does not predict feather pecking once litter quality and stocking density are controlled.**

---

## 2. The Canadian study that measured inspection frequency, duration *and* worker count

**[Decina C, Berke O, van Staaveren N, Baes CF, Widowski TM, Harlander-Matauschek A (2019). A cross-sectional study on feather cover damage in Canadian laying hens in non-cage housing systems. *BMC Veterinary Research* 15:435](https://doi.org/10.1186/s12917-019-2168-2)** — peer-reviewed, open access. ⚠️ Questionnaire table, full univariable results table, final model and methods read; **not the entire article end to end**.

- **Sample:** 39 non-cage flocks (17 single-tier floor, 22 multi-tier aviary), Canada, from 64 returned surveys of 122 distributed.
- **Stockperson variables, as actually measured:** the questionnaire's Flock Health block captured **"Inspection (frequency, duration, no. of workers, route, observations)"** and **"Flock behaviour in response to workers"**; the General block captured **years of farming experience**; the Rearing block captured **whether the farmer visited the pullet flock during rear**. The questionnaire "was based on a study by Lambton et al." — indirect evidence that the Lambton instrument also carried inspection items.
- **Outcome:** feather damage prevalence (%), farmer-scored on 50 birds per flock.
- **Result — the key negative:** variables were screened into Table 2 at a deliberately liberal **α = 0.25**. **None of the inspection variables (frequency, duration, number of workers, route) cleared even that threshold** — they do not appear in the univariable table at all. Two adjacent human-attention variables did clear it and both failed to reach significance:
  - **Farmer experience >10 years vs ≤10 years: coefficient −14.57 percentage points of feather damage, p = 0.1540**
  - **Farmer did NOT visit the pullet flock during rear vs did: +13.91 percentage points, p = 0.2129**
- **Final model (64% of variance):** flock age (+0.91/week, p = 0.0017), floor type (all wire/slatted +37.61, p < 0.001; combination +6.50, p < 0.001), manure-belt run frequency (1–2×/week +12.95; end-of-flock-only +20.13; p = 0.0151), plus non-significant enrichment, litter matching and dawn/dusk terms.

This is the cleanest available answer to the project's question, and it is a null: **inspection frequency, inspection duration and number of workers were measured on 39 commercial Canadian non-cage flocks and were not associated with feather damage even at α = 0.25.**

---

## 3. The Hemsworth-lineage poultry work: stockperson *time* null, stockperson *noise* real

**[Edwards LE, Coleman GJ, Butler KL, Hemsworth PH (2019). The Human-Animal Relationship in Australian Caged Laying Hens. *Animals* 9(5):211](https://doi.org/10.3390/ani9050211)** — peer-reviewed, open access. ⚠️ Read title through most of the Discussion; capture truncated, so closing Discussion and Conclusions **not** read.

- **Sample:** 19 laying houses across 10 farms, Victoria/NSW Australia, **conventional cages** (relevance caveat: not cage-free). Flock sizes 1,300 to 116,000.
- **Stockperson variables, as actually measured:** all stockperson behaviour observed over 2 full days and coded into 7 categories (Visual, Noise, Approach, Contact, Entry, Handle, Near Cage), **plus explicit time budgets — time in aisle, time at start/end of house, total time, time at aisle ends, stationary time, and speed of movement** — all normalised per cage per day. Plus a 10-subscale attitude questionnaire (n = 14 stockpeople).
- **Outcomes:** weeks sustained within 5% of peak egg production; albumen corticosterone; hen avoidance (withdrawal distance).
- **Results:** the parsimonious mixed model retained only cage width, average withdrawal distance and **all-stockperson noise**:
  - slope for √(noise frequency) = **−11.7 (SE 3.29)** weeks
  - slope for average withdrawal distance = **−0.062 (SE 0.0192)** weeks per cm
  - roughly a **5-week** loss of peak persistency across the observed noise range, another ~5 weeks across the withdrawal-distance range; cage width >60 cm was worth **≥10 weeks**.
- **Relevant negative:** of 32 stockperson behaviour measures, **the time-in-house variables did not enter any model.** How *long* stockpeople were in the shed did not matter; how much *noise* they made did. Mortality was recorded but never appeared in a retained model.

The paper's introduction points to **[Waiblinger S, Zaludik K, Raubek J, Gruber B, Niebuhr K (2018), *Proc. 52nd ISAE Congress*, Charlottetown, p. 187](https://www.applied-ethology.org/isaemeetings.html)** as having found stockperson attitudes associated with **feather damage and mortality** in Austrian commercial free-range flocks — exactly the target relationship. ⚠️ A **one-page conference abstract (grey literature)** that could not be obtained; content known only through Edwards et al.'s one-sentence description. No effect size, sample size or model verified.

---

## 4. The classic UK cross-sectional study: the one positive inspection finding

**[Green LE, Lewis K, Kimpton A, Nicol CJ (2000). Cross-sectional study of the prevalence of feather pecking in laying hens in alternative systems and its associations with management and disease. *Veterinary Record* 147(9):233–238](https://doi.org/10.1136/vr.147.9.233)** — peer-reviewed. ⚠️ **Abstract only.** Paywalled at Wiley/BVA; not open per Unpaywall; no repository copy found at Warwick or Bristol; CORE search returned 403. **The odds ratio, its confidence interval, and the model's full covariate list could not be obtained.**

From the abstract: 637 questionnaires, 51.5% final response (~328 respondents); outcome was farmer-reported feather pecking after point of lay; >55% reported it in their last depopulated flock. In the second logistic regression model (restricted to factors consistent throughout lay), the factors associated with **increased** risk were: <50% of the flock using the outdoor area on a fine day; three or more diet changes during lay; **"the inspection of the flock by one person"**; absence of loose litter at end of lay; house temperature <20 °C; **"turning the lights up when the flock was inspected"**; and use of bell-drinkers.

Two of those seven are stockperson/inspection variables. **"Inspection of the flock by one person" increasing feather-pecking risk is the single most on-target finding in this literature** — it is the "one person or several care for the flock" variable the brief predicted would exist. Without the full text the magnitude cannot be reported and was not reconstructed. Obtaining this paper is the highest-value remaining action.

---

## 5. Named studies checked and confirmed to contain NO stockperson covariate

These are real negatives, reported as such:

- **Bestman MWP, and the 107-flock European study.** [Bestman M (2022), *Welfare and health aspects of free ranges for laying hens*, PhD thesis, Utrecht University / Louis Bolk Institute](https://www.louisbolk.nl/sites/default/files/publication/pdf/thesis-welfare-and-health-aspects-free-ranges-laying-hens.pdf) — open access; ⚠️ **Chapter 2 only** read (methods and all result tables). Chapter 2 is the 107-flock, eight-country organic study. Its screened variable set is entirely nutritional, litter, range-access, parasite and vaccination factors — **no stockperson, staffing or inspection variable appears in Tables 2.2, 2.3 or 2.4, nor in the methods description of the candidate list.** Final model for brown hens: feather damage = 134 − 6.8 × (dietary protein at wk 55) + 21.6 × (no daily range access); protein p = 0.004, range access p = 0.001; 30% of variance, n = 53 flocks. The 2003 Livestock Production Science paper is closed access and ⚠️ not read.
- **[Nicol CJ, Pötzsch C, Lewis K, Green LE (2003). Matched concurrent case-control study of risk factors for feather pecking in hens on free-range commercial farms in the UK. *British Poultry Science* 44:515–523](https://doi.org/10.1080/00071660310001616255)** — ⚠️ abstract only, closed access. 100 flocks (50 case / 50 matched control), detailed flock-manager interview. **The only significant multivariable factor was range use** (OR 0.12 for >20% of birds ranging on sunny days). No stockperson variable mentioned in the abstract; cannot confirm from the abstract whether any was among the candidates.
- **[Rayner AC, Newberry RC, Vas J, Mullan S (2016). Smothering in UK free-range flocks. Part 2](https://doi.org/10.1136/vr.103822)** — ⚠️ abstract only, closed access. Significant predictors of nest-box smothers: breed (p = 0.008), nest box manufacturer (p = 0.014). Of panic/recurring smothers: nest box manufacturer (p = 0.009), feeding oyster grit or grain on litter (p < 0.001), range use on a sunny day (p < 0.001). **No stockperson, staffing or walking-frequency variable among the significant predictors.**
- **[Barrett J, Rayner AC, Gill R, Willings TH, Bright A (2014). Smothering in UK free-range flocks. Part 1](https://doi.org/10.1136/vr.102327)** — ⚠️ abstract only, closed access. ~60% of managers had smothering in their last flock, mean 25.5 birds per incident, mean 1.6% mortality from smothering. **"Walking birds more frequently" is named as a popular reduction measure — but as a reported practice, with no effect size attached.** This is the source of the widely-repeated claim that walking the house prevents smothering; on the reachable evidence, that claim rests on farmer preference, not on a measured association.
- **[Chowdhury P, Hemsworth PH, Fisher AD, Rice M, Galea RY, Taylor PS, Stevenson M (2025). Risk factors for smothering in three commercial free-range layer poultry farms, Australia 2019–2022. *Preventive Veterinary Medicine*](https://doi.org/10.1016/j.prevetmed.2025.106568)** — ⚠️ **abstract only** (ScienceDirect CAPTCHA). Prospective cohort, three farms; 12 deaths per 100 birds placed, of which 2 were smothering; **aviary vs flat-deck sheds HR 4.0 (95% CI 1.7–9.7)**; rainy days with humidity ≥70% **HR 3.7 (95% CI 3.5–3.9)** for indoor smothering; hazard also increased "in birds with low fear of humans and high fear of novel objects." A search-engine summary of the full text stated that the study recorded the number of staff managing each flock daily and the scheduled time of stockperson flock checks per shed — ⚠️ **unverified from the paper itself, and no staffing effect size appears in the abstract.** The most promising unread source; the only cohort study found that plausibly regresses smothering against scheduled inspection timing.
- **Norway aviary mortality study, [*Animals* / PMC9774736](https://pmc.ncbi.nlm.nih.gov/articles/PMC9774736/)** — open access; ⚠️ scanned, not read in full. 39 non-beak-trimmed commercial flocks at 70–76 weeks. **No stockperson or inspection covariate.**
- **[Schuck-Paim C, Negro-Calduch E, Alonso WJ (2021). Laying hen mortality in different indoor housing systems: a meta-analysis of data from commercial farms in 16 countries. *Scientific Reports* 11:3052](https://doi.org/10.1038/s41598-021-81868-3)** — open access; ⚠️ scanned, not read in full. 6,040 flocks, 176 million hens. A-priori moderators were **beak-trim status, flock size and hybrid colour** — no staffing variable. Its headline "experience" result (**mortality in cage-free aviaries declining ~0.35–0.65% per year** since 2000) is a **meta-regression on calendar year**, interpreted by the authors as accumulating system experience. Not a measured stockperson covariate, and should not be cited as one — though it is the strongest available quantitative support for the proposition that management competence, not housing type, drives cage-free mortality.
- **[Lambton SL et al. (2013). A bespoke management package can reduce levels of injurious pecking in loose-housed laying hen flocks. *Veterinary Record* 172:423](https://doi.org/10.1136/vr.101067)** — ⚠️ abstract only, closed access. 53 treatment vs 47 control flocks. **Dose-response on management effort:** the more of 46 management strategies employed, the lower the plumage damage (p = 0.004), gentle feather pecking (p = 0.021), severe feather pecking (p = 0.043), **mortality at 40 weeks (p = 0.025)** and likelihood of vent pecking (p = 0.021). The closest thing in the literature to "more husbandry attention → less mortality," but the exposure is a **count of strategies adopted**, not staffing hours, and which of the 46 concern inspection could not be read.

**Could not reach at all:** [Gilani AM, Knowles TG, Nicol CJ (2013), *Applied Animal Behaviour Science* 148:54–63](https://doi.org/10.1016/j.applanim.2013.07.014) and [Lambton SL, Knowles TG, Yorke C, Nicol CJ (2010), *Applied Animal Behaviour Science* 123:32–42](https://doi.org/10.1016/j.applanim.2009.12.010). ⚠️ Both closed access, both with **no record in Europe PMC** (so not even the abstracts were read), and Unpaywall confirms no OA copy. This matters: Schwarzer et al. cite **Gilani 2013** as having found "a relation between more experienced personnel and less plumage damage," with "the attendance of experienced staff during rearing … protective against feather pecking, both in the rearing and in the laying period." ⚠️ **That characterisation is Schwarzer's; Gilani et al. was not read and the variable definition, sample, effect size and whether it was multivariable cannot be confirmed.** Gilani 2013 is the second-highest-value unread source after Green 2000.

---

## 6. What this means for the eval

1. **The gap is real but it is a null-results gap, not an unexplored one.** Three independent commercial-flock studies (Germany n=30 flocks, Canada n=39, Australia n=19 houses) explicitly measured stockperson time, inspection frequency or staffing ratio against a welfare outcome and found nothing that survived adjustment. A design that assumes "more stockperson hours → measurably better welfare" is not supported by the epidemiology; a design that models it as *weakly* protective and heavily confounded by farm professionalism is.
2. **The two positive signals are about *who* and *how*, not *how long*.** Green 2000's "inspection by one person" increases risk, and Edwards 2019's stockperson *noise* costs ~5 weeks of peak persistency while time-in-house costs nothing. If the eval wants a defensible staffing lever, "number of independent people who see the flock" and "quality/manner of inspection" are better grounded than "minutes per 1,000 birds."
3. **Statistical power is the binding constraint, not researcher interest.** Every study here has 16–39 flocks. Schwarzer's attendance-time coefficient is negative at all ten measurement points and significant at none. The literature has not shown the effect is absent; it has shown nobody has run a study big enough to find it.
4. **For smothering specifically, the "walk the house more often" recommendation is unevidenced.** It appears in Barrett 2014 as a *reported farmer practice*, and Rayner 2016's regression found no management-attention predictor. If the eval scores an agent for increasing inspection walks to prevent smothering, that reward is grounded in industry convention, not in a measured effect size.

---

## Coverage statement

**Read end-to-end from the source:** Schwarzer et al. 2022 (full article body, sections 1–5, plus Tables 4, 5, 6 and 7 extracted directly from the rendered page).

**Read substantially but NOT end-to-end (⚠️ flagged at each claim):** Decina et al. 2019 (questionnaire table, full univariable results table, final model, methods — not the full article); Bestman 2022 PhD thesis (Chapter 2 methods and all result tables only, out of a 443,000-character document); Edwards et al. 2019 (title through most of the Discussion; capture truncated at 45,000 characters); Schuck-Paim et al. 2021 and Norway PMC9774736 (keyword-scanned only).

**Abstract only, full text paywalled and no legal open copy found (⚠️):** Green et al. 2000; Nicol et al. 2003; Barrett et al. 2014; Rayner et al. 2016; Lambton et al. 2013; Chowdhury et al. 2025.

**Not reached at all (⚠️):** Gilani et al. 2013 and Lambton et al. 2010 — closed access, absent from Europe PMC, no OA copy per Unpaywall, so not even the abstracts were read. Waiblinger et al. 2018 — conference abstract, not obtained; known only through a secondary one-sentence description.

**Blocked routes, for the record:** MDPI blocks command-line fetches (worked around via the browser, legitimately). ScienceDirect served a CAPTCHA, not attempted. CORE's search returned 403; Warwick's repository search returned no response. No ResearchGate author copies or routes of uncertain legality were used.

**Justification for PARTIALLY FILLED:** one peer-reviewed study (Schwarzer et al. 2022) delivers exactly the requested quantity — stockperson attendance-minutes per 1,000 birds per day and birds-per-caregiver, regressed against a scored welfare outcome on 16 commercial aviary farms, with reportable effect sizes — and a second (Decina et al. 2019) delivers a clean, well-specified negative on inspection frequency, duration and worker count. But no source reachable reports a confidence interval on any stockperson effect, no source links staffing to mortality, and the single most on-target finding — Green et al. 2000's elevated feather-pecking risk when one person inspects the flock — remains behind a paywall with its odds ratio unread.
