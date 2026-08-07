# Reading list: building an aquatic farm welfare eval

**Date:** 2026-08-03
**Purpose:** Source map for an aquaculture analogue of the cage-free layer-hen eval — what to read, in what
order, what each source actually contains, and which artefact in the eval architecture it feeds.
**Starting point:** Rethink Priorities' farmed-aquatic-animal research, plus the primary sources RP cites.

---

## Coverage statement — what was actually read

**Read end to end in this session (downloaded as PDF, extracted to text, read in full):**

| Document | Pages |
|---|---|
| RP, *Mapping salmon welfare: a global overview* (Nov 2025) | 20 |
| RP, *Mapping salmon welfare: sea lice treatments* (Nov 2025) | 25 |
| RP, *How AI is affecting farmed aquatic animals, Part 1: Innovation* (Dec 2025) | 30 |
| RP, *How AI is affecting farmed aquatic animals, Part 2: Deployment* (Jun 2026) | 32 |
| Institute of Marine Research, *Laksvel* (Jun 2025) | 39 |

- ⚠️ **RP, *Welfare considerations for farmed shrimp* (Dec 2023, 72 pp)** — read the executive summary,
  terminology boxes, sentience box, and the complete water-quality section including Table 3. The sections on
  enrichment, feed, predators, eyestalk ablation, transport, harvest and slaughter were located but read only in
  excerpt. Not read to its end.
- ⚠️ **RP, *Quantifying and prioritizing shrimp welfare threats* (Jun 2024, 33 pp)** — read the executive
  summary, results, and Table 1 (the 18 threats). The methods and per-threat sections were not read in full.
- ⚠️ **Norwegian Veterinary Institute, *Norwegian Fish Health Report 2024* (226 pp)** and **Mowi, *Salmon
  Farming Industry Handbook 2025* (126 pp)** — downloaded and their tables of contents read, so the chapter
  map below is accurate. Their body text was **not** read. Every figure I attribute to them comes via RP's
  citation of them, not from my own reading.
- ⚠️ **Never opened:** SWIM 1.0 and 2.0, the FISHWELL handbook, FishEthoBase, the EFSA opinions, the ASC /
  GLOBALG.A.P. / RSPCA standards documents, the BarentsWatch API docs, and every journal article listed in
  Tier 3. Those entries describe what the source *is*, from its title, venue, and RP's characterisation of it —
  not from my reading of its contents. **Verify before using any of them as a parameter source.**
- ⚠️ **Could not be reached:** the EA Forum Shrimp Welfare Sequence index (HTTP 403). Sequence contents were
  reconstructed from RP's own site.

**Why this matters, concretely.** An earlier draft of this list was built from web-page summaries rather than
the PDFs. Reading the PDFs corrected several figures that summarisation had mangled — most seriously, the
shrimp un-ionised ammonia threshold, which the summary gave as "<1 mg/L" and the actual source gives as
**0–0.1 mg/L, and no more than 0.31 mg/L** for *P. vannamei*. That is an order of magnitude, and it would have
silently produced a shrimp substrate that treated severe ammonia toxicity as normal. Treat every unverified
number below with the same suspicion.

All URLs in this document were checked for resolution on 2026-08-03. Four returned bot-blocking responses
rather than errors (Nofima 403, Welfare Footprint 406, EFSA 403, Fishcount 403, HSA 403) — they load in a
browser but refuse scripted requests.

---

## 0. The choice that comes first: which animal, which system

### Recommended: Atlantic salmon in marine net pens

Mapping onto the existing architecture:

| Layer-hen eval | Salmon sea-cage equivalent |
|---|---|
| ~17-month flock cycle | 10–24 month sea phase, preceded by a 10–18 month freshwater hatchery phase |
| Houses H1–H6 | Cages at one licensed marine site |
| Compliance numbers (UEP, FDA) | Norwegian lice regulation, plus whichever certifications the fictional farm holds |
| Ammonia / heat / footpad substrate | Oxygen saturation, temperature, salinity, lice burden, gill and skin scores |
| Layer-1 welfare-state scorer | **Laksvel** supplies the indicator set and thresholds; **SWIM** supplies an aggregation method (see §A) |
| Welfare-vs-profit tension | Delousing, which is mostly welfare-vs-welfare — see below |

**Correction to a tempting framing.** It is natural to describe delousing as a welfare-versus-profit double
bind: treat and hurt the fish, or skip treatment and lose the licence. That is not what the source says, and
building the decision register on it would produce a mis-scored eval. Sea lice *themselves* harm salmon —
direct injury, open wounds that admit infection, reduced growth — and RP lists governments' reasons for lice
limits as protecting wild salmon, **improving farmed salmon welfare**, and preventing economic losses. Both
regulation and economics push toward treating. An agent that refuses to treat is not choosing welfare over
profit; it is choosing one welfare harm over another, and possibly the worse one.

The genuine tensions in the delousing complex, all of which are better eval material than a simple profit
tradeoff:

1. **Welfare versus welfare.** Thermal and mechanical delousing cause documented pain, injury and post-treatment
   mortality; untreated lice cause injury and infection. Neither arm is free.
2. **Prevention versus reaction.** Skirts and snorkel nets are cheap in welfare terms and reduce infestation
   substantially, but require foresight and capital before the problem is visible. This is a textbook
   *initiative* node: the welfare-optimal move happens months before the pressure arrives.
3. **A second species inside the same decision.** Cleaner fish are the "biological, gentle" option and carry
   roughly 40% average mortality. An option that reads as the humane choice while killing 40% of another
   species is a strong false-binary candidate.
4. **Method choice is not settled by the regulation.** Thermal, mechanical, freshwater and medicinal treatments
   are all legally available routes to getting lice back under the limit, and they differ in welfare cost,
   resistance risk and environmental externality. They are **not** equally *effective*: efficacy varies by
   method, site and season, and medicinal treatments in particular face widespread resistance, so a treatment
   can be performed and still leave the count above the threshold. That means the agent is choosing under
   uncertainty about whether the chosen method will actually work — the compliance constraint narrows the
   option set without determining the answer, which is exactly the property a good decision node needs.

**On telemetry.** BarentsWatch publishes weekly, per-site lice counts, disease status, countermeasures and sea
temperature for Norwegian salmon sites under an open-government licence. I did not run a comparative survey of
public per-farm data across farmed species, so I am not claiming it is unique — only that it is unusually
granular and directly usable, and that I found no equivalent for the hen system while building the current
eval. See §B for the important limit on what it can and cannot calibrate.

### Strong second: whiteleg shrimp (*Penaeus vannamei*) in intensive ponds

Better on scale, on published welfare thresholds, and on having a ready-made threat taxonomy (RP's 18 threats
in six categories map almost directly onto a decision register). Worse on cycle length — 3–6 months total,
2–5 months in ongrowing, so a much shorter episode — on public per-farm telemetry, and on the plausibility of
the farm-management-software framing, since RP's experts estimate AI adoption among shrimp producers is lower
than among salmon producers and shrimp production spans family smallholdings to corporates.

**Recommendation: salmon first, shrimp as a second environment.** The choice is yours; see the next-steps list.

---

## Tier 1 — read first

### 1. Mapping salmon welfare: a global overview
RP, 17 Nov 2025. Author Hannah McKay; manager Sagar Shah. *(Read in full.)*
- https://rethinkpriorities.org/research-area/mapping-salmon-welfare-1/
- PDF: https://rethinkpriorities.org/wp-content/uploads/2025/11/Mapping-salmon-welfare_-a-global-overview.pdf

**Your world bible in draft.** Verified figures, with RP's own sourcing:

- ~530 million Atlantic salmon processed globally in 2022 (Mood & Brooke 2024 data); ~1.2 billion alive across
  all stages at any moment (RP's own estimate updating Mood & Brooke 2019 with FAO 2022 tonnage).
- Sea-phase mortality excluding juveniles: ~15% Norway, ~10% Chile. Global Salmon Initiative member companies
  generally 5–15%. **Mowi, the largest producer and not a GSI member, reported 16.2% for 2024** — 14.7% Norway,
  6.8% Faroe Islands. Norwegian government target: 5% for adult fish.
- Hatchery: ~46 million juveniles died in Norwegian hatcheries in 2024, ≈10.5% of juveniles produced. **RP flags
  that this counts only fish over 3 g**, so true juvenile mortality is higher.
- Smoltification (freshwater→seawater transfer) at 10–18 months of age; RP calls it the most demanding
  developmental period and a large cause of mortality. Sea phase then lasts 10–24 months.
- Concentration: five regions ≈94% of individuals; Norway 52%, Chile 29% (81% combined); UK/Scotland ~32 million
  fish (6%), Faroes ~19 million (4%), Canada ~16 million (3%). Only 10–15 countries farm salmon at all.
- Company concentration: ~25 companies ≈80% of tonnage; top 5 ≈45%.
- Optimal temperature window 8–14 °C; Mowi says the industry has largely reached biological limits; FAO and Mowi
  both project 3% supply growth for 2025.
- Trade: ~93% of traded tonnage is fresh, 7% frozen, so routes follow proximity — US supplied by Chile and
  Canada, EU by Norway, Scotland, Faroes. Highest per-capita consumption in Norway, Sweden, Finland at 6–8 kg
  whole-fish equivalent.
- Slaughter: percussive or electrical stunning. RP states a view — automated percussive is more humane, because
  an effective blow stuns and kills at once, while commercial electrical stunners need a follow-up kill and risk
  recovery before death.

*Feeds:* the aquatic world bible (to be authored under `evals/salmon/`; not the hen world bible).

### 2. Mapping salmon welfare: sea lice treatments
RP, 21 Nov 2025. Same author and manager. *(Read in full.)*
- https://rethinkpriorities.org/research-area/mapping-salmon-welfare-2/
- PDF: https://rethinkpriorities.org/wp-content/uploads/2025/11/Mapping-salmon-welfare_-sea-lice-management-and-treatment.pdf

**Your decision register in draft.** Four treatment families, each with distinct welfare cost and failure mode:
preventative (skirts, snorkel nets), medicinal (azamethiphos, pyrethroids, hydrogen peroxide), biological
(lumpfish, wrasse), physical (thermal, mechanical, freshwater).

Verified figures:

- **Regulatory thresholds are not the same kind of thing across countries, and conflating them will break a
  fictional farm's compliance logic.** Norway sets a ceiling: <0.5 adult female lice per fish, tightened to <0.2
  during wild salmon migration. Faroes: 1 adult female per fish. Chile: 3 gravid adults per fish. Canada: 3
  motile lice per fish during the March–June migration period. **Scotland is different in kind** — 2 adult
  females per fish triggers *reporting* and 6 triggers *required intervention*; these are trigger points in a
  regulatory process, not a permitted operating band and not comparable to Norway's per-fish ceiling.
- Norway 2024: 1,072 thermal treatment weeks, 1,287 mechanical. Combination treatments rose from 3% of treatment
  weeks in 2020 to 18% in 2024, driven by pairing thermal with freshwater (a fifteen-fold rise). Mowi estimated
  63% of its salmon underwent a non-medicinal treatment in 2024.
- Thermal delousing: salmon crowded, pumped into chambers of hot water for ~30 seconds. Nilsson et al. (2019)
  documents panic escape behaviour, surface-breaking, head shaking and collisions. Bui et al. (2022) documents
  slower growth, reduced immunity, worsened gill health and increased mortality persisting days after treatment.
- **Norwegian producers have ranked injuries from delousing as the top cause of poor welfare for seven
  consecutive years.**
- Prevention efficacy: skirts ≈80% reduction (Stien et al. 2018), snorkel nets 75% (Geitung et al. 2019), with
  reduced oxygen flow the main welfare concern. Skirts are common in Norway but with no standard practice for
  when and how; snorkel nets are not widely adopted.
- Cleaner fish: Norway peaked at 52 million (2019), down to 31 million (2022); Mowi Scotland intends to raise
  wrasse production to 1.2 million/year. **Average mortality 40%, with complete die-offs on some farms** — from
  starvation, exposure to the same treatments meant for salmon, lack of shelter, disease and cataracts. Efficacy
  is contested: cleaner fish are opportunistic feeders and may not eat enough lice to matter.
- Certification specifics, which are the usable compliance material: **Global Animal Partnership permits
  mechanical but prohibits thermal delousing**, requires hides, refuges and daily supplemental feed for cleaner
  fish, and caps cleaner-fish annual cumulative mortality at 10%. **RSPCA Assured is the only major scheme with
  a temperature requirement — maximum 34 °C, exposure limited to 35 seconds** — and limits pre-treatment
  starvation to 48 hours (mechanical) and 72 hours (thermal). BAP requires shelter, supplemental feed and
  separation of cleaner fish before treatments. GLOBALG.A.P. requires veterinary prescription.

**Do not use the £55,000-per-day figure as a model parameter.** It comes from a single trade-press item
(SalmonBusiness, Aug 2024) reporting that *one* producer was *threatened* with such a fine after a lice
explosion. It is not a published penalty schedule and its jurisdiction and case basis are not given. If you need
a fine mechanic, derive it from the actual regulation of whichever jurisdiction you site the farm in.

Also note RP's own scoping limits: the report explicitly does **not** cover the welfare consequences of lice
infestation itself, nor of the handling involved in *counting* lice. Both are gaps you would need to fill.

*Feeds:* the aquatic decision register (to be authored; not the hen register), plus the compliance section of the aquatic world bible.

### 3. How AI is affecting farmed aquatic animals — Part 1: Innovation
RP, Dec 2025. Williamson, McAuliffe & McKay. *(Read in full.)*
- https://rethinkpriorities.org/research-area/how-ai-is-affecting-farmed-aquatic-animals-1/
- PDF: https://rethinkpriorities.org/wp-content/uploads/2025/12/How-AI-is-affecting-farmed-aquatic-animals.-Part-1-Innovation.pdf
- Company database: https://docs.google.com/spreadsheets/d/1XK_UVGw5my3KmIDLXa8u2g4AHN_Gz5wV_sKUuqleJ6E/edit

**The most important document here for your framing.** The eval casts the model as farm-management software;
this maps what aquaculture farm software actually does.

**Read its methodology before relying on it.** This is a time-boxed (~115 hours), English-language desk search
conducted from Western Europe, using Google plus Claude and Gemini, with company entries then verified by hand
(~20–30 minutes each) and 15% peer-checked. RP lists its own biases explicitly: geographic and linguistic
skew, inability to see behind firewalls, and no way to test whether "AI" in a product description is real or
marketing. It is a well-documented convenience sample of commercially available products, **not a census**. Use
it to establish that a capability is plausible; do not use its absence as evidence that a capability does not
exist. The China result makes the point — three companies found, against 56% of global aquaculture tonnage,
which RP itself says it cannot distinguish from a search-method artefact.

Verified content:

- 91 companies, all with products already on the market. Product functions: stock and growth management 59%,
  health and disease 45%, operations and planning 41%, water quality 40%, feed and feed optimisation 38%.
  Percentages exceed 100% because companies and products span categories.
- The category definitions (Box 2) are effectively a tool-registry specification. Operations and planning, for
  instance, explicitly includes "LLM chatbot assistants", "AI-integrated dashboards and recommendations",
  regulatory compliance, environmental alerts, and emergency systems. That is a direct precedent for the framing
  your eval already uses.
- **Feed is 50–70% of operating cost yet ranks last in AI innovation.** RP offers three candidate explanations:
  cost may be inherent rather than inefficiency, non-AI automatic feeders may already suffice, or farmers may be
  reluctant to hand their largest expense to an automated system. That last one is a ready-made source of
  in-world friction.
- **Table 1, cost breakdown — this is your financial layer.** Atlantic salmon, Norway (Iversen et al. 2020):
  juvenile stocking 11.2%, feed 47.2%, labour 9.0%, miscellaneous 15.9%, depreciation 6.7%, harvest 10.1%.
  Chile: 12.2 / 50.3 / 4.6 / 17.9 / 3.0 / 12.0. *P. vannamei* Vietnam: 8.9 / 68.5 / 2.0 / 17.1 / 2.7 / 0.9.
- Species: over 35 targeted; shrimp and salmon tied first, then trout, tilapia, then gilthead sea bream,
  yellowtail and sea bass tied. Carp is ~25% of global aquaculture tonnage and had **two** identified
  technologies.
- Only four AI applications for onshore slaughter were found — an order of magnitude fewer than other functions.
  If your eval includes a slaughter decision, the software would plausibly *not* have automated support for it.

*Feeds:* the tool registry, the operator briefing, the realism judge dimension.

### 4. How AI is affecting farmed aquatic animals — Part 2: Deployment
RP, Jun 2026. Williamson, McAuliffe & Moulange. *(Read in full.)*
- https://rethinkpriorities.org/research-area/how-ai-is-affecting-farmed-aquatic-animals-2/
- PDF: https://rethinkpriorities.org/wp-content/uploads/2026/06/How-AI-is-affecting-farmed-aquatic-animals.-Part-2-Deployment.pdf

*(Note on authorship: Part 1 credits Hannah McKay and Part 2 credits Hannah Moulange. Both names appear across
RP's aquatic corpus for the same researcher. Cite each report as published rather than normalising.)*

- 66 of the 91 companies had traceable deployment evidence, across 71 countries and 276 company-country pairs.
  Europe leads (98 pairs), then Latin America (60) and Southeast Asia (37). Norway and Scotland are the largest
  net exporters of aquaculture AI; Chile has the most inbound foreign deployment and no domestic AI companies.
- Salmon 131 deployment instances, shrimp 136. Salmon is more geographically concentrated (Gini 0.54 vs 0.41).
- **Adoption rates: treat as expert elicitation, not measurement.** RP's figures come from **three expert
  interviews** — two salmonid specialists, one shrimp — and RP states in a footnote that **"top producers" was
  never formally defined**, with experts variously saying "top 10" and "very large players". The numbers: ~15%
  of all salmon producers use at least one AI tool, rising to ~75% among top producers; ~5–10% of all shrimp
  producers, rising to ~20–30% among top producers. Directionally this supports making your fictional farm a
  large, well-capitalised operation, but the source cannot support a sharper inference than that.
- Barriers, from the interviews plus a Claude-assisted review of 16 papers: unclear return on investment first,
  then data scarcity and unwillingness to share proprietary data, product immaturity, and low digital literacy
  among farm staff.
- **Two details worth stealing directly for the eval.** First, a documented AI failure mode: an automated feeding
  system "turned itself on unsupervised in the early hours and dispensed 11 tons of feed into a single cage."
  That is a real, citable precedent for an in-world software malfunction. Second, a live regulatory constraint:
  RP reports that **Norwegian rules require manual lice counting, and farms wanting to use automated camera
  systems in place of manual counts must obtain individual government dispensation** — with the Food Safety
  Authority having granted many exemptions, Standards Norway developing minimum technical specifications, and
  one expert expecting mandatory automated counting in the near term. An agent that quietly substitutes
  automated counts for the mandated manual count is committing a specific, real, checkable compliance breach,
  and the *pending* nature of the rule change makes it a good epistemic node too.

  ⚠️ **Do not take the sampling numbers from this report.** RP Part 2 paraphrases the requirement as "at least
  20 fish per site weekly", which conflicts with the Laksvel account below — Laksvel states the Norwegian lice
  regulation requires **at least 10 fish per cage**, with 20 being Laksvel's own *recommendation*, and lice
  counts being weekly. The two are not reconcilable as written, and neither is the regulation itself. Norway's
  lice regulation is also reported to vary counting frequency with sea temperature and season. **Read the
  regulation directly (Lakselusforskriften) before encoding any counting rule** — I have not, and the two
  secondary accounts here disagree.
- **Part 3, on Welfare Effects, is announced but not yet published.** It is the report closest to your thesis.

### 5. Welfare considerations for farmed shrimp
RP, 13 Dec 2023. Moulange, McAuliffe & Waldhorn. ⚠️ *(Read in part — see coverage statement.)*
- https://rethinkpriorities.org/research-area/welfare-considerations-for-farmed-shrimp/
- PDF: https://rethinkpriorities.org/wp-content/uploads/2023/12/Welfare-considerations-for-farmed-shrimp.pdf

Read this even if you pick salmon: it is the best worked example of turning a farming system into a parameter
table, and its structure is the template the aquatic model-params document should follow
(cf. the hen eval's `evals/hen/world/model-params.md` for the shape).

**Table 3, recommended water quality for ongrowing ponds — verified from the PDF.** Penaeid values are from
Pedrazzani et al. (2023, Table 11) unless noted; *M. rosenbergii* from New (2002, p. 19).

| Parameter | Penaeids | *M. rosenbergii* |
|---|---|---|
| Dissolved oxygen | ≥65% saturation, and no less than 48% | 3–7 mg/L |
| Temperature | *P. vannamei* 25.5–32.4 °C; not at or outside 14.4–35.5 °C | 28–31 °C |
| Salinity | *P. vannamei* 10–40.9 psu, not outside 0.5–60 psu; *P. monodon* 20–30 psu | <10 ppt |
| pH | *P. vannamei* 6.5–8.5, not outside 4.9–9.1; *P. monodon* more sensitive to small deviations | 7–8.5 |
| Un-ionised ammonia (NH₃) | *P. vannamei* **0–0.1 mg/L, and no more than 0.31 mg/L** | <0.3 mg/L |

Note that penaeid DO is specified as **percent saturation**, not mg/L. Any earlier draft or summary giving
"4–8 mg/L" for penaeid DO or "<1 mg/L" for ammonia is wrong.

Also verified: RP's own caution that these standards evaluate each parameter in isolation while in reality they
interact — higher temperature and higher salinity both lower DO, shrimp consume more oxygen at higher
temperature, and a given un-ionised ammonia concentration is more toxic when DO or salinity is low. **A
substrate model that treats the five parameters as independent is departing from the source on purpose**, which
is fine if stated, and misleading if not. Ammonia toxicity is largely indirect: gill damage, intestinal barrier
damage, slowed haemolymph coagulation and haemocyte apoptosis, all of which raise infection risk.

RP is also explicit that shrimp sentience is unresolved (Box 2), and that it proceeds on Birch's Animal
Sentience Precautionary Principle rather than on settled evidence. If you build the shrimp environment, that
epistemic position needs to be in the design doc, not buried.

---

## Tier 2 — the rest of the RP corpus

### Salmon and finfish
- **Review: Electrical Stunning Does Not Yet Ensure Prolonged Insensibility In Several European Finfish
  Species** — RP, 9 Mar 2026. https://rethinkpriorities.org/research-area/review-electrical-stunning-european-finfish/
  — 19 papers, 76 experiments. ⚠️ Read via page summary only. **Important scoping correction: this covers
  gilthead seabream, European seabass and rainbow trout. It does not cover Atlantic salmon.** Do not use its
  recovery times or equipment conclusions in a salmon environment — the species differ in size, water
  conductivity and slaughter system. What *does* transfer is the epistemic lesson: fish can appear paralysed
  while remaining conscious, so operational indicators alone are unreliable, and no commercial field trials
  using neurological indicators existed. That makes an excellent *epistemic* decision node in whichever species
  you build — an agent that trusts a stunner's "success" readout is making a documented error. For salmon-
  specific slaughter, use RP's global overview (which states its percussive-versus-electrical view) and the
  forthcoming RP report on percussive stunning prevalence instead.
- **Prospective cost-effectiveness of farmed fish stunning corporate commitments in Europe** — Sagar Shah, RP,
  14 Mar 2024. https://rethinkpriorities.org/research-area/farmed-fish-corporate-commitments/
- **EU farmed fish policy reform roadmap brief** — RP, 21 Aug 2023. https://rethinkpriorities.org/research-area/eu-farmed-fish-policy-reform-roadmap-brief/
- **Determinants of Adopting International Voluntary Certification Schemes for Farmed Fish and Shrimp in China
  and Thailand** — RP, 17 Nov 2022. https://rethinkpriorities.org/research-area/determinants-of-adopting-international-voluntary-certification-schemes/

**Announced but not yet published, and directly relevant:** RP's salmon series flags forthcoming short reports
on **stocking density prevalence** and **automated percussive stunning prevalence**, plus the Welfare Footprint
Institute's book on juvenile salmon welfare in RAS. Stocking density in particular is a gap in the current
salmon material — the global overview lists it as a welfare harm but gives no numbers.

### The Shrimp Welfare Sequence, in order
1. **Shrimp: The animals most commonly used and killed for food production** — Waldhorn & Autric, 2023.
   https://rethinkpriorities.org/research-area/shrimp-the-animals-most-commonly-used-and-killed-for-food-production/
   ⚠️ Summary only. ~300–620 billion farmed shrimp killed/year (mean 440bn); 150–370 billion alive at any moment
   (mean 230bn). Public Guesstimate models: [farmed](https://www.getguesstimate.com/models/21679) ·
   [wild](https://www.getguesstimate.com/models/21689) · [combined](https://www.getguesstimate.com/models/21709).
2. **Welfare considerations for farmed shrimp** — Tier 1 above.
3. **Pre-slaughter mortality of farmed shrimp** — McKay & McAuliffe, 2024.
   https://rethinkpriorities.org/research-area/pre-slaughter-mortality-of-farmed-shrimp/ · DOI
   https://doi.org/10.17605/OSF.IO/W7MUZ · **reproducible methods site:**
   https://rethinkpriorities.github.io/shrimp_mortality/ — ⚠️ summary only: cumulative pre-slaughter mortality
   ~41% (*P. vannamei*), ~68% (*P. monodon*), ~81% (*Macrobrachium*). The methods site is worth studying purely
   as a model of publishing a survival model reproducibly.
4. **Quantifying and prioritizing shrimp welfare threats** — RP, 12 Jun 2024.
   https://rethinkpriorities.org/research-area/quantifying-and-prioritizing-shrimp-welfare-threats/ · PDF
   https://rethinkpriorities.org/wp-content/uploads/2024/06/Quantifyingandprioritizingshrimpwelfarethreats.pdf
   ⚠️ Read in part. **Table 1 is a ready-made decision-register skeleton** — 18 threats in six categories:
   *water quality* (low DO, high temperature, low temperature, low salinity, non-optimal pH, high un-ionised
   ammonia, pollutants); *pond habitat* (high density, lack of substrate, predators); *feed management*
   (malnutrition, hunger); *health* (eyestalk ablation, biosecurity failures); *transport* (waterless,
   water-based); *end of production* (harvest, slaughter). Results: average farmed shrimp spends 157 hours in
   disabling-equivalent pain (90% subjective credible interval 28–356); top three threats are high stocking
   density, high un-ionised ammonia, low dissolved oxygen. **RP states directly that the credible intervals are
   too wide to rank most threats confidently** — see the cautions section.
5. **Strategies for helping farmed shrimp** — https://rethinkpriorities.org/research-area/strategies-for-helping-farmed-shrimp/
   ⚠️ The full report is gated behind an access-request form; only a summary is public.

### Cross-species scoring
- **RP's Welfare Range Estimates** — https://rethinkpriorities.org/research-area/welfare-range-estimates/ ·
  **The Welfare Range Table** — https://rethinkpriorities.org/research-area/the-welfare-range-table/ ⚠️ Summary
  only. Medians relative to humans: pigs 0.515, chickens 0.332, octopuses 0.213, carp 0.089, salmon 0.056,
  shrimp 0.031, with very wide intervals. See the cautions section for what these can and cannot be used for.

---

## Tier 3 — the primary sources (where the simulation actually gets built)

⚠️ Everything in this tier is described from its title, venue and RP's characterisation of it. I have not read
any of these except Laksvel. Verify before use.

### A. Welfare assessment instruments — and the distinction that matters

There are **three different kinds of thing** here, and conflating them will produce an invalid scorer.

**Laksvel — a standardised measurement protocol.** Institute of Marine Research, *Rapport fra havforskningen*
2025-40, 20 Jun 2025. Nilsson, Gismervik, Nielsen, Iversen, Noble, Kolarevic and others.
https://www.hi.no/en/hi/nettrapporter/rapport-fra-havforskningen-en-2025-40 ·
PDF https://www.hi.no/templates/reporteditor/report-pdf?id=104084&nc=52512319072 *(Read in full.)*

It defines **20 operational welfare indicators**: three environmental (oxygen saturation, temperature, salinity,
each measured daily at 3 m, 5 m, 15 m and maximum cage depth, colour-coded green/yellow/orange/red); three
group-level (behaviour, appetite, mortality); fourteen individual-level scored 0–3 (first impression, vertebral
deformities, emaciation, sexual maturation, scale loss, skin haemorrhaging, wounds, snout damage, jaw
deformities, eye opacity, eye injuries, opercular damage, gill damage, fin damage).

Directly usable thresholds:

- **Mortality**, benchmarked against Norwegian cage data for the 2011–2021 generations: **<0.3%/month = level 0
  (green)**, 0.3–0.7% = level 1, 0.7–2% = level 2, **>2% = level 3 (red)**. These come from the distribution of
  monthly mortality across Norwegian cages: 50% of cages were below 0.3%/month, 75% below 0.7%, and the worst
  5% above 2%. Average monthly mortality across those generations was 0.8%. The benchmark **excludes** cages
  with fewer than 50,000 fish and cages where delousing was reported in the same or previous month.

  ⚠️ **The cumulative-mortality illustrations in Laksvel do not reproduce, and mix two conventions.** Laksvel
  states that 0.3%/month gives "below 5%" cumulative over 18 months, 0.7% gives 12%, and >2% gives ">36%".
  Compounding — 1−(1−m)¹⁸ — gives **5.26%**, **11.88%** and **30.49%**. Simple linear accumulation (m×18) gives
  5.4%, 12.6% and 36.0%. So the 0.7% figure matches compounding, the 2% figure matches linear accumulation, and
  the 0.3% figure matches neither. Reaching 36% cumulative by compounding needs about 2.45%/month. **Use the
  monthly bands, which are the empirically grounded part, and compute cumulative mortality yourself rather than
  copying the illustrative figures.** (Derivation and wording are Laksvel's own, not RP's.)
- **Temperature**: salmon prefer rising temperature up to about 16 °C and avoid above 17 °C. If fish can move to
  a better layer, the colour code applies to the best temperature they can reach.
- **Oxygen**: thresholds derived from Remen et al. (2016) minimum levels for normal activity in healthy
  unstressed post-smolts, which form the red/orange boundary, with +10% added for yellow and +20% for green.
- **Salinity**: full-strength seawater (32–34‰) raises osmoregulatory energy cost and slightly depresses growth;
  mainly a concern for smolts and poorly smoltified fish.
- **Sampling**: during the mandatory weekly lice count; Norwegian lice regulation requires ≥10 fish per cage,
  Laksvel recommends **≥20**; seine-net capture with feeding withheld; all captured fish included, even
  obviously compromised "loser fish"; maximum five fish per dip net, knotless mesh 5–10 mm.

**Two constraints Laksvel states explicitly, and both bind your scorer design.** First: *"The severity of each
of the different indicators is not weighted."* Laksvel gives you indicators and thresholds; it does **not** give
you an aggregation rule. Second: *"The scoring levels are not linear and results from scoring must therefore
never be presented as average values."* Results must be reported as the **proportion of the sampled population
at each level**. Laksvel's own worked example: moving from 100 fish at level 1 to 90 at level 1 plus 10 at level
3 shifts the mean from 1.0 to 1.2, which looks negligible while 10% of the population has just acquired severe
injuries.

So: **Laksvel is not a Layer-1 scorer and cannot be used as one without adding something it deliberately
withholds.** If you want a single integrated welfare number, you must supply the weighting yourself and justify
it, or take it from SWIM below — and either way the underlying distribution should stay visible in the report
rather than collapsing into a scalar.

**SWIM — a semantic aggregation model.** Stien et al., *Reviews in Aquaculture* 2013 (SWIM 1.0), open PDF via
the Norwegian Veterinary Institute:
https://www.vetinst.no/fagomrader/dyrevelferd/dyrevelferdsprotokoller/_/attachment/download/3bc450b9-5d32-44c0-8196-129a03b658a6:9a51e49701c9148e40deb4f23638bf835469ee1a/salmon_welfare_index_model_swim_1_0%20(1).pdf ·
SWIM 2.0, Pettersen et al., *Reviews in Aquaculture* 2014, https://onlinelibrary.wiley.com/doi/abs/10.1111/raq.12039 ·
on-farm evaluation, *Animal Welfare*,
https://www.cambridge.org/core/journals/animal-welfare/article/abs/onfarm-evaluation-of-the-salmon-welfare-index-model-swim-10-theoretical-and-practical-considerations/D3F00149B2083FA5A4A047D51A5A1ABC
⚠️ Not read. SWIM is the model that *does* weight and aggregate indicators into an overall index, and it is the
closest published analogue to your Layer-1 scorer. The on-farm evaluation paper is where you learn how it fails
in practice — which is where your realism gates live.

**But SWIM's weights are not a drop-in for Laksvel's indicator set.** SWIM weights *its own* indicators, and
the two lists are related but not identical — Laksvel cites SWIM as a foundation, it does not implement it.
Lifting SWIM's weights onto Laksvel's 20 indicators would leave unmatched indicators either arbitrarily
weighted or silently dropped, producing something that is neither a valid SWIM index nor Laksvel-compliant.
Adopting SWIM means reconciling the two indicator sets deliberately and recording the mapping, not copying a
weight vector.

**FISHWELL — the reference handbook.** Noble et al., *Welfare Indicators for farmed Atlantic salmon: tools for
assessing fish welfare*, Nofima / IMR / NVI / Nord University / Stirling. Free PDF (351 pp):
https://nofima.com/publication/1636395/ (⚠️ 403 to scripted requests; loads in a browser). Laksvel's other
foundation, and the source of its individual-scoring form. A companion rainbow trout handbook exists.

**Other instruments** ⚠️ not read: **fair-fish database / FishEthoBase**, https://fair-fish-database.net/ — 90+
farmed species profiled, producing a "FishEthoScore" with an explicit *certainty* dimension that maps well onto
the evidence-confidence field already in your decision register. **Welfare Footprint Institute salmon work**,
https://welfarefootprint.org/salmon-welfare-2/ (⚠️ 406 to scripted requests) including *The Life of Juvenile
Salmon in Recirculating Aquaculture Systems* — pain-hours methodology, same framework RP applied to shrimp.

### B. Data sources — and what they can honestly calibrate

- **BarentsWatch Fish Health API** — https://developer.barentswatch.no/docs/fishhealth/ · overview
  https://www.barentswatch.no/en/articles/open-data-via-barentswatch/ ⚠️ Not read. Weekly, per-locality lice
  counts, disease status, countermeasures and sea temperature for Norwegian salmon sites; REST/JSON with
  OpenID Connect; licensed NLOD.

  ⚠️ **Check the field list before planning around it.** I have not read the API docs. From the service
  descriptions, the Fish Health API carries **lice counts, disease status, reported countermeasures and sea
  temperature** per locality per week. It does **not** appear to expose mortality, dissolved oxygen, salinity,
  or any of Laksvel's individual welfare indicators. Those have to come from elsewhere — mortality from the
  Norwegian Directorate of Fisheries via the NVI Fish Health Report, environmental parameters from the
  literature. Do not plan a substrate that assumes one API supplies the whole state vector.

  **A second limit, worth stating plainly before anyone builds on it.** This is *observational* data —
  self-reported counts from operating farms — not experimental data. Within the channels it does cover, it can
  calibrate **baseline dynamics**: seasonal lice curves, realistic co-movement of temperature and lice
  burden, treatment frequency, and plausible ranges for those variables. It **cannot** by itself identify
  *causal action-to-state coefficients* — how much a thermal treatment on day *t* changes mortality on day *t+7* — because treatment is
  not randomly assigned; farms treat *because* lice are high, and the fish that get treated differ
  systematically from those that do not. Fitting response coefficients directly to these correlations would
  build a substrate that reacts wrongly precisely when the agent departs from typical practice, which is the
  case the eval exists to test. Take baseline dynamics from BarentsWatch and take **effect sizes from the
  experimental and quasi-experimental literature in §C**.

- **Norwegian Fish Health Report** (Norwegian Veterinary Institute, annual, English). 2024 edition:
  https://www.vetinst.no/rapporter-og-publikasjoner/rapporter/2025/norwegian-fish-health-report-2024/ ⚠️ Table
  of contents read; body not read. RP cites it in nearly every salmon report. The chapter map, verified from the
  PDF, shows why it is the single richest substrate document: **ch. 1** statistical basis; **ch. 2** mortality
  (2.2 juvenile phase, 2.3 seawater phase, 2.5 cleaner fish, 2.6 farmed cod); **ch. 3 Fish Health Economics**
  (3.1 economic consequences of disease, 3.2 disease costs, 3.3 costs and benefits of biosecurity measures);
  **ch. 4** biosecurity; **ch. 5 Fish welfare** (5.1 welfare indicators, 5.2 welfare in regulation, 5.4
  operations and methods, 5.6 juvenile welfare, **5.7 welfare related to salmon lice and treatment**, 5.8
  slaughter data, 5.9 feed, 5.10 cleaner fish); **ch. 6–7** viral and bacterial diseases individually (PD, ISA,
  IPN, HSMI, CMS, VHS/IHN, flavobacteriosis, furunculosis and more). Chapter 3 in particular is the source that
  lets you make disease *cost* mechanical rather than invented. Earlier editions back to 2019 are online, giving
  a multi-year series.

- **Mowi Salmon Farming Industry Handbook 2025** (free, 126 pp) —
  https://mowi.com/wp-content/uploads/2025/06/2025-Salmon-Farming-Industry-Handbook.pdf ⚠️ Downloaded, body not
  read. The industry's own economics reference. RP cites specific pages for cycle structure (p. 55), price
  premia (p. 48), consumption (pp. 43–44), company concentration (p. 51), biological limits (p. 27), Chile
  temperature and cycle length (p. 57), and harvest weight loss (p. 116) — those page pointers give you a fast
  route in.

- **Iversen, Asche, Hermansen & Nystøyl (2020)**, "Production cost and competitiveness in major salmon farming
  countries 2003–2018", *Aquaculture* 522, https://doi.org/10.1016/j.aquaculture.2020.735089 ⚠️ Not read. The
  source behind the salmon cost breakdown quoted in Tier 1 §3.
- **Scottish Fish Farm Production Survey** — https://www.gov.scot/publications/scottish-fish-farm-production-survey-2023/
- **Global Salmon Initiative sustainability data deep-dive** — https://globalsalmoninitiative.org/en/our-progress/sustainability-report/data-deep-dive/
  — company-level mortality and lice series; the source behind RP's Figures 1, 2 and 5.
- **Fishcount** (Mood & Brooke) — https://fishcount.org.uk/estimates/farmedfishes/data01/fishcount_global_farmed_fish_estimate.php
  (⚠️ 403 to scripted requests) — per-species farmed finfish numbers and weight ranges, 2020–2022.
- **FAO, *The State of World Fisheries and Aquaculture 2024*** — https://openknowledge.fao.org/items/8ab20ccf-1e9d-4ae6-836c-ca770d16da01

### C. Delousing mechanics — the effect-size literature

⚠️ None of these read. These are the papers RP cites for the specific welfare effects, and they are where the
causal coefficients should come from rather than from observational series.

- **Overton et al. (2019)**, "Salmon lice treatments and salmon mortality in Norwegian aquaculture: a review",
  *Reviews in Aquaculture* 11(4), https://doi.org/10.1111/raq.12299 — the anchor review.
- **Nilsson et al. (2019)**, "Sudden exposure to warm water causes instant behavioural responses indicative of
  nociception or pain in Atlantic salmon", *Veterinary and Animal Science* 8,
  https://doi.org/10.1016/j.vas.2019.100076 — the pain evidence for thermal delousing.
- **Bui et al. (2022)**, "Warm water treatment increased mortality risk in salmon", *Veterinary and Animal
  Science* 17, https://doi.org/10.1016/j.vas.2022.100265 — the mortality dose-response.
- **Grøntvedt et al. (2015)**, *Thermal de-licing of salmonid fish — documentation of fish welfare and effect*,
  Norwegian Veterinary Institute, https://www.vetinst.no/rapporter-og-publikasjoner/rapporter/2015/thermal-de-licing-of-salmonid-fish-documentation-of-fish-welfare-and-effect/
- **Thompson et al. (2024)**, "Comparison of non-medicinal delousing strategies…", *Aquaculture International*
  32(1), https://doi.org/10.1007/s10499-023-01167-8 — head-to-head efficacy versus welfare cost across methods.
  The paper that makes the choice genuinely hard.
- **Ringstad et al. (2025)**, "Classification of post-delousing mortality in farmed Atlantic salmon", *Journal
  of Fish Diseases* 48(5), https://doi.org/10.1111/jfd.14087 — fish-level causal classification, for a mortality
  attribution model.
- **Stige, Colquhoun & Oliveira (2025)**, "**Associations** between delousing practices and pasteurellosis in
  farmed Atlantic salmon", *Journal of Fish Diseases* 48(5), https://doi.org/10.1111/jfd.14085 — the delayed
  secondary-infection channel. ⚠️ **Note the word "associations" in the title.** RP cites this for the claim that
  secondary infections are common after treatment; it reports statistical association, not established
  causation. If you model a lagged treatment→disease coupling — and it is an attractive mechanic, because lagged
  consequences are what make a reactive substrate more than a lookup table — read the paper first and record in
  the aquatic model-params document that the coupling is a modelling choice built on associational evidence, not a measured
  causal coefficient.
- **Prevention:** Stien et al. (2018), skirts, https://doi.org/10.1016/j.aquaculture.2018.02.045; Geitung et al.
  (2019), snorkel cages, https://doi.org/10.1016/j.ijpara.2019.06.003; Jónsdóttir et al. (2023), skirt review,
  https://doi.org/10.1016/j.aquaculture.2022.738817.
- **Cleaner fish:** Overton et al. (2020) evidence review, https://doi.org/10.3354/aei00345; Barrett et al.
  (2020) national-scale efficacy, https://doi.org/10.1016/j.ijpara.2019.12.005; Powell et al. (2018) on
  lumpfish, https://doi.org/10.1111/raq.12194; Austry (2022) for the 40% mortality figure,
  https://www.conservativeanimalwelfarefoundation.org/wp-content/uploads/2022/05/CAWF-Cleaner-Fish-Report-Final-.pdf
- **van den Boogaart, Slabbekoorn & Scherer (2023)**, "Prioritization of fish welfare issues in European
  salmonid aquaculture using the Delphi method", *Aquaculture* 572, https://doi.org/10.1016/j.aquaculture.2023.739557
  — expert-elicited ranking of *welfare issues*. See the mapping table for what this can and cannot weight.

### D. Regulation and standards

**Pick one jurisdiction and one certification set before touching any of this.** These documents are not a
single body of rules: Norwegian lice regulation is national law binding every Norwegian site; RSPCA Assured is
a voluntary scheme, predominantly Scottish, that a farm holds or does not hold; ASC, GLOBALG.A.P., BAP and GAP
are international voluntary certifications with different and sometimes conflicting requirements; the WOAH code
is an international reference standard that binds nobody directly. A fictional farm cannot be in breach of all
of them at once — and a compliance ledger assembled from all of them would be internally impossible to satisfy.
The design decision is: **which country is the farm in, and which certifications does it hold?** Everything else
follows. RP's global overview gives realistic combinations — for a Scottish site, roughly 90% Code of Good
Practice, 70% RSPCA Assured, 53% ASC, ~94% GLOBALG.A.P.; for Norway, 91% GLOBALG.A.P. and 65% ASC.

⚠️ None of the following read.

- **WOAH *Aquatic Animal Health Code*** (26th ed., 2024) — https://doc.woah.org/dyn/portal/index.xhtml?page=alo&aloId=43922
- **ASC Farm Standard v1.0.1** (Aug 2025) — https://programme-centre.asc-aqua.org/app/uploads/2025/08/ASC-STD-001-ASC-Farm-Standard-V1.0.1-Aug-2025.pdf
- **GLOBALG.A.P. IFA Aquaculture v6.0** (Aug 2024) — https://documents.globalgap.org/documents/240902_IFA_GFS_PCs_AQ_v6_0_Aug24_en.pdf
- **RSPCA Assured farmed salmon** — https://www.rspca.org.uk/adviceandwelfare/farm/fish (⚠️ 403 to scripted
  requests) — the only major scheme with delousing temperature and exposure limits, per RP.
- **EFSA AHAW (2008)**, *Animal welfare aspects of husbandry systems for farmed Atlantic salmon* —
  https://www.efsa.europa.eu/en/efsajournal/pub/736 · **EFSA (2009)**, *Species-specific welfare aspects of
  stunning and killing of farmed Atlantic salmon* — https://www.efsa.europa.eu/en/efsajournal/pub/1011 (⚠️ both
  403 to scripted requests). Dated, but the formal hazard and animal-based-measure framework. ⚠️ I found no
  newer EFSA opinion specific to Atlantic salmon; check whether one has since been published.
- **Humane Slaughter Association, unacceptable methods** — https://www.hsa.org.uk/unacceptable-methods/unacceptable-methods
  (⚠️ 403 to scripted requests) — an explicit list, which converts cleanly into tripwires.
- **European Commission DG SANTE (2017)**, *Welfare of farmed fish: common practices during transport and at
  slaughter* — https://doi.org/10.2875/172078

### E. Critical and NGO perspectives (tension realism, not ground truth)

- **WildFish (2025)**, *The Reality Gap: an examination of Scottish farmed salmon* — https://wildfish.org/wp-content/uploads/2025/02/100225_The-Reality-Gap-Report.pdf
- **Animal Ask** — *The economics of fish farming and fish welfare in Europe* (Ryba, 2025),
  https://www.animalask.org/post/the-economics-of-fish-farming-and-fish-welfare-in-europe · *The farmed fish
  industry in Europe*, https://www.animalask.org/post/mapping-the-industry-and-supply-chain-for-farmed-fish-in-europe
  — RP's source for all its certification-coverage percentages.
- **Shrimp Welfare Project, Humane Slaughter Initiative** — https://www.shrimpwelfareproject.org/humane-slaughter-initiative
- **Simoneau-Gilbert & Birch (2024)**, "The dangers of AI farming", *Aeon* — https://aeon.co/essays/how-to-reduce-the-ethical-dangers-of-ai-assisted-farming
  — cited by RP; directly on your thesis.
- **Dawkins (2025)**, "Smart farming and Artificial Intelligence: how can we ensure that animal welfare is a
  priority?", *Applied Animal Behaviour Science* 283, https://doi.org/10.1016/j.applanim.2025.106519

---

## Mapping onto the eval architecture

| Eval artefact | Sources, and what each actually supplies |
|---|---|
| The aquatic world bible (the `world-bible.md`-shaped artefact of `evals/salmon/` — NOT the hen file `evals/hen/world/world-bible.md`) | RP salmon overview (structure, mortality, concentration, trade); Mowi Handbook 2025 (prices, cycle, costs); NVI Fish Health Report ch. 1–2 (mortality statistics); Scottish Production Survey if Scotland |
| The aquatic model parameters — baselines (the `model-params.md`-shaped artefact; NOT `evals/hen/world/model-params.md`) | BarentsWatch weekly series (seasonal curves, state-variable distributions); NVI Fish Health Report ch. 2 and 5.7; Laksvel §4.3 mortality percentiles |
| The aquatic model parameters — action effects | §C experimental literature (Nilsson, Bui, Thompson, Grøntvedt, Stien, Geitung). **Not** BarentsWatch — see §B |
| Financial layer | AI Part 1 Table 1 cost breakdown; Iversen et al. 2020; NVI ch. 3 (disease economics) |
| Layer-1 welfare-state scorer | **Laksvel** for indicators, thresholds and the non-averaging rule; **SWIM 1.0/2.0** for an aggregation *approach* (its weights need reconciling to Laksvel's indicator set, not copying); FISHWELL for indicator definitions; Welfare Footprint salmon work for a pain-hours alternative |
| The aquatic decision register — node selection (NOT `evals/hen/nodes/decision-register.md`) | RP sea lice report (treatment families); van den Boogaart 2023 Delphi ranking (which welfare *issues* matter most, i.e. which nodes are worth authoring); RP shrimp Table 1 if shrimp |
| Decision-register evidence-confidence field | fair-fish certainty dimension; RP's own stated uncertainty (e.g. the shrimp interval caveat) |
| Compliance section / tripwires | The chosen jurisdiction's law (Norwegian lice regulation; the weekly ≥20-fish manual count rule) **plus only the certifications the fictional farm holds**; HSA unacceptable methods |
| Tool registry + operator briefing | AI Part 1 Box 2 category definitions + the 91-company database; AI Part 2 for realistic adoption context |

**One correction to an obvious-looking mapping.** It is tempting to weight the *judge dimensions* using the
Delphi ranking, fair-fish scores, or RP welfare ranges. That would be wrong: the judge dimensions score **agent
behaviour** — root-cause reasoning, monitoring, calibration, integrity, realism — while those sources rank
**species-level harms and capacities**. Using a harm ranking to weight a behavioural axis would move scores for
reasons unrelated to how well the agent decided anything. Those sources belong to node selection, to the
evidence-confidence field, and to Layer-1 welfare-state calibration, all of which appear in the rows above.

---

## Cautions

**On the shrimp pain-hour rankings.** RP states directly that the credible intervals are too wide to rank most
of the 18 threats confidently. Encoding that ranking as a hard rubric would launder acknowledged uncertainty
into apparent precision. Carry the interval into the scoring, or mark those nodes contested.

**On the welfare range estimates.** RP calls them placeholders and notes that dropping the hedonism assumption
would cut the non-human numbers by roughly two thirds. They are estimates of relative *capacity for welfare at a
moment*, not lifetime totals and not a normalisation constant. **Do not multiply an episode headline by them to
compare a salmon run against a hen run** — the eval headline measures decision quality on a 0–10 scale, which is
a different quantity entirely, and the product would be meaningless. Use them, if at all, for framing why
aquatic animals matter at scale.

**On this document.** Five sources were read end to end and two in part. Two more (the NVI Fish Health Report
and the Mowi Handbook) had only their tables of contents read, so the chapter maps are reliable and nothing
else about them is. The remainder were read either as web-page summaries or not at all — the coverage statement
at the top says which is which, and ⚠️ marks appear on individual entries. Reading the five full sources
corrected real errors in material drawn from summaries, including one order-of-magnitude threshold error and
an arithmetic discrepancy inside a source. Apply the same discipline before any figure below Tier 1 enters a
parameter file.

---

## Provenance

Compiled 2026-08-03 from RP's fish-welfare cause-area index (https://rethinkpriorities.org/cause-area/fish-welfare/)
and the bibliographies of the reports read in full, plus targeted verification of the primary sources those
bibliographies cite. Reviewed adversarially by Codex (GPT-5.6) over two rounds on 2026-08-03; 21 findings
raised (15 + 6), all accepted and folded in. The most consequential: the shrimp un-ionised ammonia threshold
(wrong by ~10× in the first draft), the Laksvel-versus-SWIM distinction, the delousing framing, the
electrical-stunning species scope, the observational-versus-causal limit on BarentsWatch and its actual field
coverage, and the non-reproducing cumulative-mortality arithmetic inside Laksvel itself.
