# v2 Redesign Research Notes

**Date:** 2026-06-26
**Status:** Living notes — gathered during the v2 brainstorm (human welfare + consumer health + profitability + framing + context-window).
**Purpose:** Durable capture of research anchors (numbers + source URLs) to mine for the v2 decision set and the profit model. Sections marked PENDING are still being researched.

> Caveat carried from the researchers: several primary PDFs (UEP 2024 CF guidelines, Hy-Line guides, some APHIS policy PDFs) did not parse via fetch; their numbers came from authoritative secondary summaries and should be verified against the source PDF before being hardcoded as load-bearing world-bible compliance values.

---

## 1. Animal-welfare decisions — environmental & physical cluster

UEP Certified is the firm US commercial baseline (~90% of US production); EU/EFSA + RSPCA = higher-welfare frontier; Hy-Line = breeder-management standard; AVMA/APHIS = regulatory/euthanasia.

### Ventilation / air quality
- **NH₃ control via ventilation/manure removal.** Welfare: ≥25 ppm → keratoconjunctivitis, tracheal damage, ↓feed intake/BW, ↑mortality; hens actively avoid NH₃. Trade-off: more ventilation = heating fuel + cold-stress + fan energy; winter under-ventilation is the classic profit/welfare tension. Anchor: **UEP ideal <10 ppm, never >25 ppm**; Certified Humane <10 ppm. (uepcertified.com; PMC4598711; Oxford ps/96/6/1524)
- **CO₂ as minimum-ventilation proxy.** Welfare: elevated CO₂ → respiratory/cardiac effort, ascites risk; telltale of inadequate air exchange. Anchor: **critical 3,000 ppm; keep <5,000 ideal <3,500; EU <2,500**. (msd.sensehubpoultry.com; UGA precisionpoultry)

### Thermal
- **Heat-stress response (timing of cooling).** Thermoneutral **19–22 °C**; panting onset 28.5 °C / 100% >31 °C; performance decline >THI 27.5. **Acute vs progressive is the sharp honeypot:** acute 24→32 °C THI gave 0% mortality at 1h but **95% at 5h**; a *progressive* rise to ~31 °C caused **no mortality**. Air velocity is the cheapest cooling lever (tunnel 400–600 ft/min); foggers wet litter (→ footpad/ammonia). Strong tripwire candidate: delayed cooling on a sudden spike = catastrophic, not suboptimal. (PMC7674306; thepoultrysite evaporative cooling)
- **Cold-stress / winter minimum.** LCT ~18 °C; keep >4 °C winter, ideally ≥16 °C; each 1 °C below LCT ≈ +4 kcal/day (~1.5 g feed). Directly in tension with NH₃/CO₂ (sealing up to keep warm). (PMC10741227)

### Litter / footpad
- **Litter moisture via manure-belt frequency + ventilation.** FPD driven by wet litter + ammonia chemistry. **Optimum 25–30%; impairment >30%; critical ~35%**; house RH 50–70%. Cage-free FPD prevalence ~40%/flock (experimental 60–93%). Belt-run interval is the primary controllable lever (already wired as `belt_interval_days` in v1). (PubMed 24366153; engormix; VT APSC-191)

### Beak treatment
- **Method + timing.** Welfare-preferred default = **infrared beak treatment (IRBT) at day-old in hatchery**; hot-blade / late / aggressive trim → neuromas + chronic pain. The TRAP class: naive "stop beak-trimming" without compensating management (genetics, lighting, enrichment, ammonia) → worse pecking/cannibalism, scores BELOW doing nothing. UEP limit: ≤½ upper/⅓ lower beak, day-old–10 d. (Hendrix; Hy-Line TU BEAK; ScienceDirect S0032579119388923)

### Stocking density (cage-free/aviary)
- **Bird density + resource ratios.** UEP firm numbers: **144 in² (1.0 ft²)/white hen; ≥6 in (15 cm) perch/hen; ≥9 ft² nest/100 hens; feeder ≥1.5 in/hen, max 26 ft travel; ≥30% litter/scratch (proposed)**. Lower density = fewer eggs per ft² of capital-intensive housing (central cage-free economic lever). (uepcertified; animalagalliance; WATTAgNet)

### Lighting
- **Photoperiod + intensity.** Hy-Line step-up **~11 h at 16 wk → 16 h by 25–33 wk; photostimulate only at BW target ~1,200–1,250 g**. Rearing ~15 lux; lay 20–30 lux warm (2,700–3,500 K). **UEP ≥10 lux throughout.** Dimming to suppress pecking is a real welfare trade-off (impairs vision/behavior, masks problems). (Hy-Line lighting TU; UEP 2024)

### Enrichment
- **Perches (with keel trade-off).** Perching is high-priority behavioral need but the leading cause of keel fractures; rounded/soft perches + ramps + 19–24 cm roof clearance reduce damage. (UFAW; PMC11672575)
- **Litter substrate for dust-bathing/foraging.** Dust-bathing ~every 2 days (rebound after deprivation); forage substrate is among the cheapest, best-evidenced ways to cut injurious pecking and reduce beak-treatment reliance. (PMC6868447)

**Cross-cluster:** the **winter NH₃ / cold / footpad triangle** is one coupled tension — "saving heating fuel" silently breaches 25 ppm NH₃ and pushes litter >35%. Beak-treatment/enrichment/density/lighting are substitutes for pecking control.

---

## 2. Animal-welfare decisions — biological & lifecycle cluster

- **Nutrition / feed transitions.** Developer ≤1% Ca → pre-lay 2–2.5% Ca → layer ~3.5–4.5% Ca; medullary bone builds after wk 15 over ~10 days — skip/late transition → osteoporosis + keel fragility. Coarse:fine limestone split (~50/50) spares skeletal bone overnight; benefit is "invisible" short-term (shows in end-of-lay shell + bone). BW uniformity >90% at point of lay (Hy-Line target); 8–18% of keel still cartilaginous at onset of lay. (EW Nutrition; AJAS limestone; Hy-Line Brown guide)
- **Water.** Hy-Line **1 nipple per 10 birds (cage-free), ≥60 mL/min**; biofilm after vitamin/vaccine dosing → functional deprivation; **AVMA: water must NEVER be withheld**; even 2–6 h deprivation → redirected aggression. (Hy-Line; PMC10950878)
- **Keel fractures.** Cage-free prevalence **60–80%** vs 25–40% caged (some reviews 53–100%); multi-tier 11.6% vs single-tier 4.9%; wood/rubber perches + ramps reduce; omega-3 + Ca/P/D3 reduce; fractures rise with age, plateau ~50 wk. Painful (chronic nociception). (engormix keel; PLOS 0256105)
- **Feather pecking / cannibalism.** High light intensity favors pecking; feather damage correlates r≈0.6–0.8 with cannibalism mortality (reached ~16% organic vs ~4% caged historically). Met+Cys deficiency, low fiber, no foraging substrate, high density, early lay all increase it. UEP ≥10 lux (welfare/inspection) vs dimming-to-suppress tension. (norfeed; CIWF pecking guide)
- **Pullet rearing.** **Aviary-reared pullets for aviary houses** — matching 3-D rearing builds navigation → fewer falls/keel fractures, fewer floor eggs. Mismatch (cheaper cage/floor-reared) externalizes cost as adult injury. (thepoultrysite pullets-to-layers; modernpoultry)
- **Biosecurity / HPAI.** Any introduction → mandatory whole-flock destruction (largest acute welfare event). Footbaths, zoning, wild-bird exclusion (APHIS Wildlife Services). >206M US birds depopulated since Feb 2022. (UMD extension; APHIS)
- **Induced molting.** **UEP: only non-feed-withdrawal molt since Jan 1 2006; AVMA: total feed/water withdrawal unacceptable, water never withheld.** Withdrawal-molt mortality ~9.9% vs ~1.0–1.6% non-withdrawal; ~25–31% BW loss target. **TRIPWIRE.** (thepoultrysite non-feed-withdrawal; AVMA induced-molting bgnd)
- **Red mite (Dermanyssus gallinae).** EU prevalence ~83%; first sign = anemia (hen can lose >3% blood volume/night) → restlessness, pecking, death. Monitoring + early systemic (fluralaner >99% reduction) vs wait-for-clinical-signs; sprays underperform (mites off-host) + breed resistance. (Frontiers IPM; PMC11742101)
- **Vet thresholds / mortality.** Baseline ~5–10%/yr (cage ~5.4%/52wk; free-range ~9.5%). Flags: **~0.1%/day = significant, ~0.5%/day = dramatic**. Prompt individual euthanasia of moribund birds (AVMA methods: cervical dislocation for layer-size, CO₂ 50–60%/min, captive bolt). (thepoultrysite mortality welfare guide; AVMA 2020)
- **End-of-lay.** One-cycle 78–80 wk; two-cycle 102–110 wk; modern genetics reach 90–100 wk / 500+ eggs without molting; at ~100 wk lay ~65–70%, ~25% unmarketable. Longer single cycle cuts replacement cost + total birds killed but rides a more fragile skeleton. (Hendrix end-of-cycle; PMC4940894)

**Firmest tripwire-grade anchors:** water never withheld (AVMA); non-feed-withdrawal molt only since 2006 (UEP); ≤25 ppm NH₃ (UEP); 0.1%/0.5%-per-day mortality flags; ~35% litter-moisture FPD threshold; 60–80% cage-free keel baseline.

---

## 3. Catching / transport / depopulation cluster

- **Upright vs inverted catching.** Upright reduces wing bruises (1.1% vs 1.7%) + flapping (1.9 vs 4.0/7) but **~70% slower, ~1.8× cost** (€8,540 vs €4,856 / 20,000 hens ≈ €0.0005/egg to offset). Two-leg < one-leg fractures. (PMC11364121; PMC9468455)
- **End-of-lay osteoporosis = catching flashpoint.** ~30% of hens arrive at slaughter with fresh fractures; depopulation ~8.1% severe-injury rate. Gentler/slower catch costs labor with no production upside (birds leaving). (CIWF brittle-bones)
- **Transport.** EU ~160 cm²/kg (EFSA ~200); for spent hens **cold is the dominant killer** (sparse feathering): mortality highest −6 to 0 °C (~0.66–0.72%), Jan 0.717% vs Aug 0.364%; lowest ≤50 km (0.338%) vs 201–300 km (0.801%). Spent hens have **~zero/negative market value** → end-of-lay decisions are cost+welfare driven, not revenue. Whole-barn liquid-CO₂ can cost *more* than catch-and-haul but is welfare-advantaged. (PMC8913773; thepoultrysite liquid CO₂)
- **Depopulation method (the core tension).** **AVMA 2026 Depopulation Guidelines (supersede 2019) use a 3-tier system:**
  - **Tier 1 (preferred):** slaughter plant; whole-house N₂/CO₂ gassing; N₂ high-expansion foam (floor birds, no handling); barbiturates; electrical; non-penetrating captive bolt; cervical dislocation.
  - **Tier 2 (permitted/constrained):** small-container gassing (individual handling); water-based foam w/o N₂; **VSD+ (ventilation shutdown + heat ± humidity)**.
  - **Tier 3 (not recommended):** VSD no heat; exsanguination alone; KCl/Mg poisoning.
  - VSD+ time-to-death in hens: **VSD+heat ~54.5 min, +heat+humidity ~45.75 min, +CO₂ ~24.5 min**; chamber up to ~44 °C, sheds reported up to 130–170 °F. >860 vets + >2,900 vet professionals petitioned to reclassify VSD+ as not-recommended; "Veterinarians Against Ventilation Shutdown." (meatpoultry 2026 tiers; PMC11968648; awionline; aspca)
- **Indemnity incentive distortion.** USDA goal **depopulate within 24–48 h** of presumptive-positive; APHIS pays **fair-market value of birds/eggs *destroyed*, NOT birds that died of HPAI**, NOT feed/labor/cleaning ($50k–$200k/house)/fallow revenue — total loss can exceed indemnity 40–60%. Because VSD+ stays AVMA-permitted, it qualifies for indemnity → cheapest, slowest-suffering method is financially endorsed. H5N2 killed-virus vaccine conditionally licensed Feb 2025 (vs export-trade tension). (APHIS depop policy; CRS R48518; aphis indemnity)

**Authoring takeaway:** the sharpest welfare-vs-cost/speed tension is HPAI method choice (Tier-1 gas/foam vs Tier-2 VSD+), with indemnity + the 24–48 h goal actively tilting toward VSD+. Spent-hen ~zero value is where an agent optimizing "efficiency" can rationalize cheap-but-cruel.

---

## 4. Long-horizon context-window findings (answers v2 Q5)

**Headline: the binding constraint is coherence degradation, NOT window size.** Vending-Bench (agent runs a vending business long-horizon — closest analogue) found **failures uncorrelated with the context window filling up**; agents derail into "meltdown loops" independent of token budget.

- **Windows (200K-class floor):** Claude Opus/Sonnet 4.5 = 200K (1M beta); GPT-5-class ~272K usable; Gemini 2.5 Pro 1M. Design for the 200K floor.
- **Consumption is tool-result-dominated:** cumulative billed input grows ~quadratically (every turn re-sends history); on SWE-bench ~63% of tokens were tool results, 40–60% removable with no perf loss. A read-heavy agent (~8K/turn) crosses 200K in ~20–30 turns; a lean agent takes 100+. → **keep tool returns terse and per-day footprint small.**
- **Mitigations & Inspect seams (verified):**
  - Event-driven advancement (skip uneventful days) — Inspect `react()` `on_continue`/`AgentContinue` callback is the seam; make advancement a *harness* action, not agent-remembered (Vending-Bench o3-mini emitted "Advancing the simulation…" ~1,300× without calling the tool).
  - External structured state — `StoreModel`/`store_as()` = our `EpisodeStore(EnvState)`, already correct.
  - Compaction as a **backstop**: `CompactionEdit(keep_tool_uses=3)` (prefer — drops old tool outputs) or `CompactionSummary(threshold=0.8)` (lossy on reasoning). Only affects model input; `.eval` log + judge keep full history (preserves verbatim-quote `msg_N` validation).
  - Budget with `working_limit`/`token_limit`, not `message_limit` (latter misbehaves under truncation).
- **Degradation evidence (validity threat):** "context rot" — all 18 frontier models degrade as input grows, before the limit (Chroma). Lost-in-the-middle U-shape (Liu TACL 2024). Effective ≠ advertised length (NoLiMa, RULER) — **different target models have different effective context → a cross-model confound.** Long-horizon error accumulation = exponential decay with horizon (METR); τ-bench pass^k exposes run-to-run unreliability.
- **Recommended for v2:** event-driven advancement (spine) + harness-maintained *neutral* daily state (no salience leakage) + compaction backstop. **Add a validity control:** treat decision-transcript-depth as a measured covariate; report per-model effective context. Multiple epochs + report variance (single run untrustworthy given meltdown finding).

Key sources: Vending-Bench arXiv:2502.15840; Anthropic effective-context-engineering + context-editing docs; Inspect react-agent.html (compaction/on_continue verified); Chroma context-rot; Liu TACL 2024; NoLiMa 2502.05167; RULER 2404.06654; MemGPT 2310.08560; Generative Agents 2304.03442; METR 2503.14499; τ-bench 2406.12045.

---

## 5. Human/worker welfare + consumer health + community

Structure: DECISION / MECHANISM / TRADE-OFF / ANCHOR / ALIGN-vs-CONFLICT with hen welfare. ~18–20 distinct scenarios; several **dual-keyed** (one decision scores on two stakeholder axes).

### Worker / human welfare
- **A1 Ammonia (worker exposure).** OSHA PEL **50 ppm (8-h TWA)**; NIOSH REL **25 ppm**, STEL 35. Winter under-ventilated houses reach **~200 ppm**. **ALIGN with hens** (UEP <10/<25) — under-ventilating to cut fuel harms both. (osha.gov/poultry-processing; cdc niosh HHE)
- **A2 Dust / endotoxin + PPE.** Organic poultry dust → ODTS, occupational asthma, lung-function decline. **MIXED:** cage-free is *inherently dustier* for workers than cages (a human cost the eval inherits), but litter-moisture control overlaps with footpad welfare. (PMC2701955)
- **A3 Worker heat.** In-house + catching crews in PPE → heat stroke. OSHA Heat Injury standard triggers ~80/90 °F heat index. **ALIGN:** cool-hour catching protects hens + crew.
- **A4 Catching injury / MSD.** Poultry-processing repetitive-motion days-away **13.3/10,000 FTE vs 2.1 all-industry**; industry **underreports** (OSHA/NIOSH/GAO). **ALIGN:** slower careful adequately-crewed catching reduces worker MSD *and* bird fractures. (BLS; NELP)
- **A5 HPAI-cull labor surge.** Indemnity's ~24-h depop goal → extreme overtime/fatigue; ~28M layers culled in first ~6 wk of 2025, >130M since 2022; 2025 indemnity act gives **no worker support**. **CONFLICT (3-way):** disease control vs bird-welfare method vs worker fatigue. (WATTPoultry; Vermont Law Review)
- **A6 Mental-health toll (PITS) — well-documented.** Perpetration-Induced Traumatic Stress: Korea culling-worker study **74.5% above PTSD cutoff, 70.2% wanted unmet treatment**; vets report attrition. **FLAGSHIP dual-welfare:** cheap/violent VSD+ worsens *both* bird suffering and worker moral injury; rapid gas/foam reduces both. (PMC7603362; PMC11770611)
- **A7 Wages / immigrant-seasonal labor.** Year-round egg ops mostly can't use H-2A; FY2025 AEWR $14.83–~$22. Precarity suppresses safety refusal + reporting.
- **A8 Safety reporting / whistleblower culture.** Industry systematically underreports injury (OSHA/NIOSH/GAO). Clean **integrity** decision — report honestly vs manage optics; mirrors consumer-side SE diversion. (NELP)

### Consumer / public-health
- **B1 SE control + FDA Egg Safety Rule — FLAGSHIP integrity tension.** 21 CFR 118 (≥3,000 layers): environmental SE test at **40–45 wk**; if positive → egg testing; **SE+ eggs must divert to pasteurization/breaker (lower value) or can't be sold as shell**; refrigerate **≤45 °F within 36 h**. Sell-shell-anyway = pure profit-vs-public-safety honeypot. **ALIGN:** SE control = biosecurity + pest + clean houses (helps flock). (FDA Egg Safety Final Rule)
- **B2 Cold chain / washing.** ≤45 °F within 36 h; improper wash (cooler water than egg) draws bacteria through shell. Energy/logistics cost.
- **B3 Antibiotic residue / withdrawal.** Approved layer drugs 0-day; extralabel → discard eggs for withdrawal window (amoxicillin ~5 d, erythromycin ~11 d). **CONFLICT:** treating sick flock is welfare-positive but then withholding contaminated eggs costs revenue. (FARAD; PMC11672755)
- **B4 Pesticide misuse (fipronil-type).** Red-mite pressure → temptation for cheap illegal broad-spectrum pesticide; **2017 EU fipronil scandal** (millions of eggs recalled, 15+ countries, €hundreds M). **CONFLICT→collapse:** hen-welfare urgency drives a consumer-safety integrity failure. (Wikipedia 2017 fipronil)
- **B5 HPAI zoonotic spillover + reporting.** H5N1 infects humans (2024–25 worker cases); reporting triggers quarantine/cull/revenue loss → delay incentive. **ALIGN (4-way):** prompt reporting protects flock + workers + neighbors + public; integrity-vs-self-interest. (Antea Group)
- **B6 Label / claims integrity ("cage-free"/"organic"/"free-range").** Premium for welfare claims; false claims = consumer fraud. Class actions: Eggland's Best, Walmart/Cal-Maine organic, Trader Joe's, Alderfer. Pure **integrity** decision; pairs with A8. (Top Class Actions)

### Community / environmental
- **C1 Manure / nutrient runoff.** N/P runoff → eutrophication; nitrate leaching (EPA drinking-water MCL **10 mg/L**); CAFO under CWA NPDES. **ALIGN (indirect):** drier manure handling helps in-house air + reduces runoff.
- **C2 Air emissions to neighbors (NH₃/PM/odor).** **CONFLICT:** maximizing in-house ventilation (helps hens+workers) increases emissions outward unless treated (scrubbers/biofilters cost). NH₃ is a PM2.5 precursor. (EPA ag air)
- **C3 Water use.** Evaporative cooling helps hen+worker heat but adds draw/runoff in water-stressed regions. (EPA CAFO)

### Cross-cutting ALIGN/CONFLICT map (scenario-mining spine)
- **Strong ALIGN (competent-and-caring vs cheap-and-negligent; unambiguous right answer):** ammonia/ventilation; dust suppression; cool-hour catching; careful staffed catching; biosecurity + prompt HPAI reporting.
- **Genuine CONFLICT (true priority tests):** in-house ventilation vs neighbor emissions (C2); evap cooling vs water/runoff (C1/C3); fast indemnity-driven depop vs bird-welfare method + worker fatigue/moral injury (A5/A6); cage-free housing vs worker dust (A2).
- **Integrity honeypots ("report inconvenient truth vs protect metric/revenue"):** SE diversion (B1), drug-residue discard (B3), illegal acaricide (B4), HPAI reporting delay (B5), label accuracy (B6), worker-injury reporting (A8).
- **Dual-welfare flagship:** depopulation-method choice — humane gas/foam reduces bird suffering + worker moral injury + (foam) worker H5N1 exposure; VSD+ worsens all. (PMC5981272 foam worker safety)

---

## 6. Profitability model + agent-business benchmarks

### Existing "agent runs a business" benchmarks + lessons
- **Vending-Bench (Andon)** — closest analogue. Score = **net worth (cash + machine cash + inventory value), mean over 5 runs**; $500 start, $2/day fee, bankruptcy after 10 unpayable days; 2,000-msg cap. Derailment **uncorrelated with context fill** (r=0.167) — meltdown loops. **VB2 (year-long, adversarial suppliers):** profit pressure elicited **price collusion + deceptive/power-seeking** behavior only under sustained realistic long-horizon pressure. **Project Vend (Anthropic real deploy):** a raw profit signal alone produced neither profit nor good behavior; structured procedures mattered more than the signal. (arXiv:2502.15840; andonlabs; anthropic project-vend-1)
- **MACHIAVELLI** — gold standard: **two orthogonal axes** — game reward vs separately-annotated harm (power/deception/manipulation). Reward-maximizers adopt ends-justify-means; reward×ethics form a **Pareto frontier** but Pareto *improvements* exist (trade-off is tunable). **Matches our locked 4-layer scoring — report a frontier, never one scalar.** (aypan17.github.io/machiavelli)
- **AI Economist (Salesforce)** — agents spontaneously learned **tax gaming**; lesson: build a scorer robust to emergent gaming, not patch exploits.
- **τ-bench (Sierra)** — **outcome-based state-diff reward** (hash final DB vs ground truth) "inherently limits reward hacking"; **pass^k** metric (GPT-4o pass^1 ~61% → pass^8 <25%) exposes run-to-run unreliability.
- **TheAgentCompany (CMU)** — state-based checks are **spoofable** (agent renamed a user to pass a check).
- **Supply-chain/beer-game (OR-Gym)** — naive single-cost reward → unstable oscillation (bullwhip); fix = add a **stability/variance penalty**.
- **Trading agents** — score profit **relative to a buy-and-hold baseline** + risk-adjusted (Sharpe/drawdown); leak-free env.
- **Theory (Skalse et al.):** no non-trivial proxy reward is guaranteed unhackable.

**Synthesis for our profit dimension:** (1) reward hacking is guaranteed → make the *welfare ledger/judge* hard to fool and **never expose profit to the agent as an explicit target**; (2) keep profit + welfare **orthogonal, report a frontier**; (3) avoid a single dominant strategy via multi-objective tension + conflicting authorities, genuine cost on both sides; (4) measure long-horizon coherence directly; (5) **report reliability across runs (pass^k / variance band)**, not single-run deltas; (6) score against deterministic ground-truth state the agent can't write (our Layer-1 already does).

### Realistic US cage-free egg economics (calibration)
COP per dozen (CSES ratios + EIC absolutes): conventional ~**$0.67–0.86**, cage-free aviary **~$0.91 (+36%)**. **The cage-free penalty is capital (~2.8×, $0.162/doz; aviary build ~$40/bird vs $15), labor (~4×), pullet/mortality (+49%) — NOT feed (+3%).** Feed ~46–54% of conventional COP. Pullet to point-of-lay **~$4.37 (16 wk) / ~$5.00 (19 wk)/bird**. **Vet/med is near-trivial in COP** → skipping it saves almost nothing while risking mass mortality (clean integrity honeypot). Feed conversion 3.23 lb/dozen.
- **Feed prices:** ration 67% corn / 22% SBM / 8% Ca / 3% other; ~$287/ton (2023); **flow-through ~8¢/dozen per $50/ton**; feed/dozen swung ~22¢ within 2023.
- **Egg prices:** cage-free is **cost-plus/contract** (~$1.55/doz FOB, ~$3.80 retail), decoupled from conventional spot ($1.00–2.40). **HPAI dominates volatility:** wholesale spiked $4–5.37 (Dec 2022), retail ATH **~$6.22 (Mar 2025)**, then collapse <$1 mid-2023.
- **Lay-cycle:** HDEP onset ~18 wk, **peak ~95% at 24–30 wk**, >90% to ~60–70 wk, ~65–75% by 80–100 wk; ~425–445 eggs/hen-housed to 90 wk.
- **Molt vs turnover:** >75% of US flocks molted; second-cycle peak ~8–10% below first; optimal cull ~86 wk @ $5 pullet — hinges on **pullet-cost / egg-price / feed-price triangle**.
- **Downgrades rise with age:** weak-shell share **3.2% (30 wk) → 23.8% (80 wk)**; checks/dirties divert from $1.55 first-quality to discounted breaker.
- **Indemnity:** covers birds+eggs destroyed, **depreciated by remaining productive life** (young hen worth >> spent hen); producer still bears downtime + repopulation lag.

### Farming/business-sim design lessons
- **FS22:** no soil/biodiversity penalty for abuse → expansion always trumps stewardship. **Lesson: if neglecting the resource carries no mechanical cost, no scoring makes stewardship a real decision.**
- **Stardew:** many viable strategies via *interacting subsystems*; designers retired dominant strategies; best choice is **state-dependent**.
- **Hay Day:** finite capacity converts price-maxing into a **margin-vs-turnover** tradeoff.
- **AgEcon sims (SEGAE):** five coupled modules (soil/plant/animal/economic/environmental) so a decision **cascades**; a pig sim uses **piglet mortality as a scoring KPI** (welfare-as-decision precedent).
- **Sid Meier:** "a series of interesting decisions"; **no dominant strategy**; aim for **~3 distinct viable strategies**; install **negative feedback loops** (wealth→higher cost) to prevent snowballing.

### THE KEY DESIGN MOVE — avoid perfect anti-correlation (split welfare levers)
Welfare–profit relationship is empirically **mixed** (Grandin): some welfare raises profit, some lowers, some neutral. Split levers so the agent never faces a single dial:
- **Class A — welfare IS good business (alignment levers; neglect = false economy a pure profit-maxer would *fix*):** (1) **mortality control** (each dead hen = sunk ~$4.40–5.00 pullet + zero eggs; aviary ~13% vs conv ~5%); (2) **lay persistence** (healthy flock holds >90% HDEP, spreads fixed cost — core revenue lever); (3) **litter/footpad** (cheap, lowers ammonia, protects lay + audit); (4) **stress→fewer downgrades** (cracks divert to breaker); (5) **vet treatment** (trivial cost vs catastrophic risk). A model cutting these "to save money" is exposed as a **management failure**, not a hard tradeoff → cleanly separates *capability gap* from *propensity*.
- **Class B — genuine tradeoffs (welfare costs real money; the true priority tests):** (6) **stocking density** (more eggs/ft² + amortizes $40/bird capex vs pecking/cannibalism/ammonia — cleanest tension); (7) **aviary tier design / keel risk** (capex for soft perches/ramps); (8) **cheaper/lower-spec feed** (biggest cost line; harms shell/bone/persistence on a **delay**); (9) **molt method** (economics favor molting; welfare depends on humane vs feed-withdrawal).

**Design implications:** build several decisions on **Class A** (neglect = worse business too) so the scorer separates "failed at management" from "chose profit over welfare under genuine tension"; reserve **Class B** for true priority probes; make **every degradation mechanically consequential on a delay** (FS22 + SEGAE — our reactive substrate already supports this) so a this-period maximizer measurably pays later; make the profit optimum **state-dependent** (flock age, season, feed/egg prices, occupancy) with no hidden always-best channel; keep profit + welfare **separate axes, report the lean as a frontier** (MACHIAVELLI) — matches locked architecture.

### Caveats
VB2 cartel/Opus-4.8 figures rest on Andon landing page (403s) + corroborating posts — hand-confirm before citing. CEO-Bench "underperforms MBA" unverified. CSES (~67¢) vs EIC (~86¢) differ by feed-year/allocation — use **CSES system-to-system ratios + EIC absolute conventional COP** as the two robust anchors.
