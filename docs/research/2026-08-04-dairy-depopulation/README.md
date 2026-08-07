# Dairy depopulation, culling and euthanasia — research corpus

> Run 2026-08-04 · Branch `feat/plf-dairy-eval` · For the PLF dairy eval's last uncatalogued cluster
> (depopulation / culling method). **This is the research layer, not a design document.** Node design
> belongs in `docs/design/2026-08-04-technology-use-catalog.md` after the owner has reacted.

## Why this corpus exists

Depopulation was the last cluster on the original eight-cluster list with **no dairy research at all**. The only existing material was poultry — `docs/research/2026-07-20-depop-welfare-hierarchy.md` (nitrogen foam, CO₂, ventilation shutdown, whole-house gassing for the hen node `DP14_HPAI_DEPOP_METHOD`). The open question was whether any of it transfers.

**It does not.** That negative finding, and what replaces it, is the substance of this corpus.

## Reading order

| File | Angle | Strength |
|---|---|---|
| **`README.md`** (this file) | Distillation and adjudication — read first | — |
| `01-euthanasia-methods-and-delay.md` | AVMA/AABP methods, FARM standards, the delayed-euthanasia problem, worker impact, decision aids | **Strongest.** Four papers + AABP 2025 read end to end |
| `02-culling-rates-and-economics.md` | Cull rates and denominators, reason distributions, record integrity, ship-vs-euthanize economics | **Strong.** Both NAHMS reports read as complete extracted text |
| `03-downers-and-transport-fitness.md` | FSIS regulation, transport fitness, prevalence, handling, enforcement | **Strong.** The 2009 Federal Register rule and AABP 2026 read end to end |
| `04-surplus-calves.md` | Disposition, beef-on-dairy, on-farm killing of newborns, transport | **Mixed.** NAAB and Roccaro read in full; much else via summarising fetch |
| `05-mass-depopulation.md` | AVMA depopulation guidelines for cattle, H5N1, bTB, FMD, indemnity | **Strong on the negative finding.** AVMA 2026 Chapter 3 read in full |

**Provenance and verification status.** Five parallel Opus research agents, each instructed to read sources in full, grade every source, and return an explicit coverage statement. **All five returned coverage statements**, reproduced verbatim at the end of each file. Those statements are the agents' own claims and cannot be verified from outside — **any finding that will carry rubric weight must be traced to its primary source directly before it is relied on.** The files are the raw agent output, preserved for provenance; cite this README, not the raw.

---

## The five findings that change the design

### 1. The poultry depopulation node does not transfer, and building a cattle version would encode an error

There is **no gas, foam-in-place, or ventilation-based whole-barn method for cattle in the AVMA depopulation guidelines at any tier.** A mechanical full-text search of the 2026 edition confirms "ventilation shutdown," "VSD," "gas," "carbon dioxide" and "nitrogen" appear **zero times** in Chapter 3 (Bovids). Every cattle method is applied animal-by-animal.

The reason is structural: cattle housing cannot be sealed. The throughput ceiling makes it concrete — a portable pneumatic captive bolt with a restrainer achieves "roughly 75 to 100 per hour," so **a 250-cow herd is about three hours of continuous individual killing**, where a poultry house is one overnight environmental event.

**Consequence:** an agent that refused a cattle ventilation shutdown would be scoring points for rejecting something that does not exist and no US veterinarian would propose. Do not build it.

⚠️ **Version note that also affects the hen node:** the AVMA depopulation guidelines were **superseded on 30 January 2026** by a 2026 edition that replaces the named tiers ("preferred / permitted in constrained circumstances / not recommended") with numbered Tier 1/2/3. `DP14`'s rubric and `docs/research/2026-07-20-depop-welfare-hierarchy.md` both cite the 2019 edition. That is now a stale citation in built, shipped hen content.

### 2. H5N1 in dairy cattle is a quarantine-and-compensation event, not a kill event

Dairy cows largely recover. Within-herd morbidity ~10–20%; combined mortality-and-culling **≤2%** (📋 AVMA, 16 Dec 2025) against >90% mortality in birds. **No US dairy herd has been depopulated for H5N1.** APHIS's own livestock programme page does not contain the word "depopulation."

The most elegant evidence is the federal compensation formula: USDA pays through ELAP on an assumed **21 days of no milk followed by 7 days at half production**, and the cow must still be **alive and lactating** to qualify. A programme that pays for recovery is definitionally not a depopulation programme.

**This is itself a scoreable behaviour:** an agent that proposes depopulating a dairy herd over an H5N1 detection is making a real, checkable error.

### 3. "Euthanize at a loss versus ship for salvage" is a **false choice** for a genuinely down cow — this corrects what I told you last turn

I described the downer decision as euthanize-now-at-a-loss versus get-her-up-and-loaded-for-salvage. **For a non-ambulatory cow that framing is legally wrong, and the correction is settled rather than contested.**

There is no lawful path by which a cow who cannot rise converts into salvage value in commerce. If she arrives non-ambulatory she is condemned at ante-mortem inspection. If she rises, passes inspection, and goes down again before slaughter she is **still condemned** — the case-by-case veterinary re-inspection loophole was deliberately closed by FSIS in 2009 (74 FR 11463, effective 17 April 2009; 9 CFR 309.3(e)). AABP's March 2026 position is that a non-ambulatory cow is never fit for transport in any prognosis category, except to veterinary care under veterinary guidance.

**And FSIS named the exact behaviour this eval would be testing, as the problem the rule was written to stop.** From the final rule at 74 FR 11465: the prior rule "may have created an incentive for establishments to inhumanely attempt to force these animals to rise," and gave producers reason to hold "dairy cattle until they become exceptionally old or weak... to extract as much milk as possible in the hope that they are able to pass the initial ante-mortem inspection before going down."

The tension survives, in a better form. **FSIS has no jurisdiction on farms, at auction markets, at stockyards, or in transport** — it says so explicitly, declining comments that asked it to. Congress has identified that gap and left it open for two decades. So the farm-level decision is genuinely ungoverned by federal law, and **6.55% of surveyed producers said they would cull/sell a non-ambulatory cow for beef** (Wagner et al. 2020) — an action federal law guarantees will end in condemnation. That is a welfare failure and an economic error at once, which is a far sharper node than a straight money-versus-welfare trade.

### 4. The real dairy tension is **delay**, and it is measured, with a farm-size gradient that lands on our farm

This is the best-evidenced material in the corpus and the strongest candidate for the cluster.

For a ~250-cow herd (USDA's "medium, 100–499" stratum), from NAHMS Dairy 2014:

| Measure | Medium herds |
|---|---|
| Had ≥1 non-ambulatory cow in 2013 | **90.1%** |
| Cows that became non-ambulatory | **3.3%** (~8 cows/year at 250 head) |
| Has a **written** protocol for handling them | **24.1%** |
| Trains anyone in euthanasia | **24.6%** |
| Averages ≤1 day from recognition to euthanasia | **20.0%** |
| Averages **>2 days** | **48.7%** |
| Averages **>6 days** | **8.5%** |

**The medium stratum is the worst on timeliness** — worse than both small and large herds. And the clock starts only after the cow has already been down 24 hours, because that is NAHMS's definition of non-ambulatory.

Outcomes for those cows: **30% recover, 49.7% euthanized, 17.7% die unassisted.** Roughly one in five downer cows dies without anyone ending it.

The guideline anchors are unusually clean and converge from three independent directions:
- **24 hours** — Green et al. 2008 found cows down <24 h were 3.0× more likely to recover (recovery 32.9% vs 8.2% ⚠️ secondhand), and concluded "considering euthanasia is appropriate for cows that have been nonambulatory for more than 24 h." AABP 2026 sets a 24-hour exit strategy. NAHMS uses 24 h as its very definition.
- **4 hours** — AABP, verbatim and unchanged since 2019: "No more than four hours (preferably much less) should elapse between making the decision to euthanize and performing the procedure." So "we decided to put her down, we'll do it tomorrow morning" is itself a guideline violation.
- **Three observable behavioural tests** all three published decision trees converge on: can she hold herself sternal with her head up · can she raise her front legs when assisted · will she eat and drink.

**And the money is on the wrong side.** Constructed from components (no single study states it): the ship-versus-euthanize gap is roughly **$865–$1,000 per cow in 2013 dollars and $2,400–$2,600 in mid-2026 dollars** — cull cow prices are at record highs. Barbiturate euthanasia makes it worse, because a pentobarbital carcass is **excluded from the rendering stream** (FDA treats residues in feed as adulteration; Pennsylvania traced dead bald eagles to it in April 2020). Both primary US welfare papers say the incentive runs the wrong way in their own words, and a producer in the focus groups says it plainly: *"if cull prices are up you're obviously going to do more to try and get that animal into a state where it can be sold rather than be euthanized."*

**The single most rubric-relevant sentence in the whole sweep**, from a dairy worker asked what happens when criteria are absent: **"If the decision is not clear, we give them another day."**

### 5. Record integrity is a documented failure mode, not an inference

The lameness-laundering claim already in the catalog holds up structurally, and the surrounding evidence is stronger than the claim itself.

- **📋 NAHMS attaches "Producer reported and not necessarily verified" to its own cull-reason table.** The US national reference dataset declines to vouch for its reason categories.
- **✅ Denmark: only 66.8% of culled cows had any reason recorded at all** — and the missingness is non-random, correlated with breed, cow age, and herd yield/SCC. So the failure is not only wrong reasons but *absent* ones, biased toward worse-managed herds.
- **✅ Estonia:** registry permits one reason per cull; the authors state that "the stated culling reasons might be the consequences of the primary disorder," and specifically that late-lactation fertility culls likely include cows non-pregnant *because of* chronic health disorders. They also note: "To our knowledge, there are no studies that investigate the farmers' behaviour in reporting culling reasons."
- **Infertility (21.2%) and poor production (21.1%) are the top two US recorded reasons**, and NAHMS itself warns they overlap.

---

## Numbers that are safe, and numbers that must not be used

### Resolved — two long-standing project gaps closed

The catalog's **"do-not-use until the primary source is read"** flag on the 37% cull rate and 6.2% on-farm death rate (entry 1 §1.10) is now **resolved**. They are **East-region NAHMS cells summed together**, propagated through a Penn State Extension article that mislabels the region as "Northeastern," calls the sum "permanently removed" (contradicting NAHMS's own definition, which excludes deaths), and mixes two denominators in one table.

**Correct national figures, reference year 2013, as a percentage of 1 January 2014 dairy cow inventory: 33.8% permanently removed, 5.6% died (including euthanasia), 39.4% total turnover.**

⚠️ Carry one caveat: NAHMS Part I gives 28.4% / 4.8% for the same year and the two reports do not explain the discrepancy. Part III is preferred because it is the only one that states its denominator; report Part I as the alternative.

### Do not inherit these — errors found circulating in the literature itself

1. **"Lameness = 16.8% of cows removed"** (Walker et al. 2020 body text). 16.8% is lameness *prevalence*. Removals for lameness are **7.2%**.
2. **"250,000 / 300,000 / 331,982 / half a million unfit US dairy cattle shipped annually."** All trace to one table that double-counts (the "severely lame" row is a subset of the "lame" row and both are summed), applies 7% to the wrong base, switches multipliers mid-table, and relabels NAHMS's "remained in the herd" column as "% successful recovery." **Use none of them.**
3. **"Less than 1% of calves that die are euthanized"** — a percent-of-population presented as a percent-of-deaths. The correct figures are ~6% of preweaned-calf deaths and ~11% of weaned-heifer deaths, which are damning enough.
4. **"19% of downer cows are sold instead of euthanized"** — the figure is real but its instrument measures whole-year outcomes (a cow who went down, recovered, and was culled six months later counts), its standard error is 6.5, and it conflicts with the 2.5% home-slaughter figure from the same study's other instrument.
5. **Two incompatible calf-euthanasia statistics** — "5% of Canadian farmers euthanized at least one male calf at birth" and "19% of calves were euthanised at birth" have different denominators and differ by an order of magnitude. The paper that would resolve them (Renaud et al. 2017) could not be opened.
6. **Never compare recovery rates across "downer" definitions.** NAHMS = down ≥24 h. Green 2008 = unable to stand for *any* length of time. AABP = no time qualifier.

### The genuinely negative findings, which are findings

- **How often healthy newborn calves are killed on US farms: no data exists.** The circulating numbers are Canadian.
- **There is no US federal minimum age for transporting a calf.** The only federal instrument is the 28-hour law, whose exemption clause ("food, water, space, and an opportunity for rest" in the vehicle) largely swallows it, with a $100–$500 penalty. Every comparator jurisdiction is stricter; New Zealand's bobby-calf mortality fell from 0.68% to 0.04–0.05% across its regulatory reform.
- **No US on-farm first-attempt euthanasia failure rate exists.** Only slaughter-plant data (0.16% of fed cattle, 1.2% of bulls and cows returning to sensibility), which is a floor, not a farm estimate.
- **No published dairy euthanasia decision tree has ever been validated** — no sensitivity/specificity, no inter-rater reliability, no agreement-with-expert-panel study. All are committee-authored.
- **No study has measured whether a decision aid changes any on-farm outcome**, in cattle.
- **Worker psychological burden → delay is EVIDENCED but NOT QUANTIFIED.** Documented in dairy workers' own words and endorsed by authors; never measured. Do not present it as an effect size. Note also that nearly all quantitative euthanasia-trauma research is from shelters, clinics and labs — **not farms** — and is routinely applied to livestock without that caveat.

---

## Highest-value follow-ups, if any of this becomes load-bearing

1. **Green et al. 2008** (*J Dairy Sci* 91:2275–2283) — the single load-bearing prognosis paper. Only its odds ratios were obtained; the 32.9%/8.2% recovery split that everything downstream quotes is secondhand.
2. **Stull et al. 2007** (*JAVMA* 231:227–234) — the canonical peer-reviewed review on handling downers. Never accessed, so the entire handling section rests on guideline documents rather than primary welfare science.
3. **FARM Animal Care Version 5 Reference Manual** — blocked by four independent routes in two separate sweeps. Every V5 specific in this corpus is trade press. This is the US dairy analogue of the hen eval's UEP standards, so it matters.
4. **Renaud et al. 2017** — resolves the 5%-of-farmers vs 19%-of-calves calf-euthanasia discrepancy.
5. **AVMA Depopulation Guidelines 2026 vs 2019** — confirm whether the hen node's rubric needs its citation updated.

## Standing caveats

⚠️ Almost every publisher blocked automated access at some point: Elsevier/*J Dairy Sci*, ScienceDirect, MDPI, avma.org (Incapsula), nationaldairyfarm.com, congress.gov, cdc.gov and aphis.usda.gov all returned 403 or timed out. Several primary documents were reached only through Wayback Machine captures. Where a claim came through a summarising fetch layer rather than raw text, the agents said so — and one agent caught that layer **fabricating** a non-existent exception in EU Regulation 1/2005, which it found only by returning to the raw PDF. Treat single-pass AI extraction of regulatory text with suspicion.

⚠️ The core US statistics are **NAHMS Dairy 2014, reference year 2013 — thirteen years old**, and no newer national study appears to exist.
