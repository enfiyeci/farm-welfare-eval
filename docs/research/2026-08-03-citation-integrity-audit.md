# Citation-integrity audit of `docs/research/` — 2026-08-03

**Why this exists.** The research in this directory was gathered under a looser sourcing standard.
This audit re-checks whether cited sources actually say what is attributed to them, and records
what could not be verified. It does NOT re-do the research or change any conclusion — findings
below are for adjudication, not applied fixes.

**Status: COMPLETE for the scoped set.** All six batches have returned, including the re-dispatch
of the one that failed. ⚠️ The `v2-*` files (~77 citations) were deliberately out of scope — they
target a future redesign nothing is built on. Their absence from this audit is a scoping choice,
not a clean bill of health.

⚠️ **Provenance of the findings, which bounds how far they can be trusted.** Sections 1, 2 and 2.1
were produced directly by the author of this file. **Sections 3 through 3e are delegated results:
sub-agents fetched and read the sources and returned coverage statements, and the author did not
independently re-read those papers.** Their verdicts are reported here as the agents stated them.
That makes each one a reasonable lead, not a settled fact — a wrong or incomplete agent reading
would survive into this document unchanged. Before acting on any individual finding below, open
the cited paper and confirm it. Section 5 says which findings most warrant that.

---

## 1. Structural findings (verified directly, no fetching required)

### 1.1 ⚠️ P1 is the only source PDF with no source links at all

Extracting embedded URLs from every research PDF in `docs/research/sources/`:

| PDF | Real source URLs |
|---|---|
| `P1-compliance-context.pdf` | **0** (only font-license boilerplate) |
| `P2-model-calibration.pdf` | 17 |
| `P4-welfare-decision-brief.pdf` | 19 |
| `P5-corpus-realism.pdf` | 17 |
| `P6-rubric-anchors.pdf` | 13 |

P1 is the stated source for `evals/hen/world/world-bible.md` §12 (compliance) and the §8 APHIS indemnity
table — the most load-bearing "firm" regulatory facts in the eval, and the ones a target model
could be scored against. Their provenance is currently unverifiable from the artifact itself.
`evals/hen/world/world-bible.md` contains zero external citations of its own.

### 1.2 The project already flagged this and the flag appears unactioned

`evals/hen/research/v2-redesign-research.md` carries this caveat from its own researchers:

> several primary PDFs (UEP 2024 CF guidelines, Hy-Line guides, some APHIS policy PDFs) did not
> parse via fetch; their numbers came from authoritative secondary summaries and should be
> verified against the source PDF before being hardcoded as load-bearing world-bible compliance
> values.

Those numbers are now hardcoded — in `evals/hen/world/world-bible.md` §8/§12 and in `corpus/pricing.yml`
(`aphis_indemnity_usd_head`, asserted in `tests/env/test_pricing.py`). §2 below is the
verification that caveat asked for, done for UEP.

### 1.3 235 unresolvable citation tokens in two documents

`P4-welfare-decision-brief.md` (147) and `2026-07-28-substrate-realism/vitamin-d3-decision.md`
(88) contain deep-research citation markers wrapped in Unicode private-use characters
(`U+E200`-range), rendering as opaque tokens like `turn17view0`. They carry no URL and cannot be
resolved to any source. `P4-welfare-decision-brief.md` also opens with a dead
`sandbox:/mnt/data/P4.md` link.

**Partly recoverable:** the *PDF* siblings retain real hyperlinks (P4's PDF has 19). The markdown
export lost them. That recovers the *set* of sources P4 drew on, but not the mapping from any
individual token to its source — the 147 in-text citations stay unresolved, so per-claim
traceability is not restored by extraction alone;
`vitamin-d3-decision.md` has no PDF sibling, so its 88 tokens are ⚠️ currently unresolvable —
and that document reached a binding decision ("DO NOT MODEL" vitamin D3, spec §2d).

### 1.4 Numeric research with no citations at all

Fourteen files carry zero external references. Excluding the ones where that is expected
(prompt templates, document templates), these make specific numeric claims with nothing behind
them:

- `2026-07-01-daily-labor-staffing.md` — "~40,000 hens per FTE" (aviary) vs "~65,000" (cage),
  "floor eggs 10–15%", per-task hour budgets.
- `2026-07-02-staffing-org-structure.md` — "Herbruck's… nearly 400 employees for ~10M hens",
  "2–3× more labor than conventional cages".
- `2026-07-28-substrate-realism/vitamin-d3-decision.md` — Hy-Line W-80 at 3,300 IU/kg; trials
  moving 2,500–2,760 → 5,000–5,520 IU/kg (see 1.3: tokens present, URLs absent).

These are not idle: `evals/hen/world/model-params.md` cites the staffing files as the basis for
`staffing_adequacy_zero_fte = 0.5` and the anchor fit f(2.5)=1.0 / f(2.0)≈0.84, and staffing is a
live agent lever (`set_staffing` in `farm_eval/adapter/tools/controls.py`, `DP20_HPAI_STAFFING`).

---

## 2. `world-bible.md` §12 checked against the real UEP standard

The UEP PDF does not parse through the fetch tool (reproducing the failure the §1.2 caveat
described), so it was downloaded and extracted locally with `pdftotext`. Source read:
*2024 Cage-Free Housing Animal Welfare Guidelines for U.S. Egg Laying Flocks*
(https://uepcertified.com/wp-content/uploads/2023/10/CF-UEP-Guidelines_2024.pdf), 11,140 words.

**Confirmed exactly (11 claims):**

| §12 claim | UEP 2024 text |
|---|---|
| 144 sq in/hen multi-tier or slatted | "1.0 square foot per hen in multi-tier housing" / "in slatted floor housing" |
| 216 sq in/hen single-level all-litter | "1.5 square feet per hen in single-level all litter floor housing" |
| Perch 6 in/hen, 20% elevated ≥16 in | "minimum of 6 inches of elevated perch space per hen… 20% of this perch space must be at least 16 inches above the adjacent floor" |
| Nest 1/5 hens or 9 sq ft/100 community | "community nest a minimum of 9 square feet… per 100 hens… individual nest boxes a minimum of 1 nest per 5 hens" |
| Feeder 1.5 in/hen trough | "minimum of 1.5 linear inches of feed trough… per hen when straight troughs are used" |
| Drinker 1 nipple/cup per 10 hens | "1 nipple drinker or cup per 10 hens" |
| Ammonia <10 ppm target, "must rarely exceed 25 ppm" | "should be less than 10 ppm and must rarely exceed 25 ppm" — verbatim |
| 20-day backfill window | "may place hens within a barn for 20 days after the initial hen placement" |
| Auto-fail list (space, backfilling, commingling, feed-withdrawal molt, willful abuse) | matches the standard's failure clause item for item |
| 90% to pass | "must receive 90% on a UEP Certified audit for a passing rate" |
| 7-day audit notice | "seven-day advanced notice" |

**Divergences (3):**

1. **"200-point checklist / 180/200" — NOT SUPPORTED.** The standard describes "a point scoring
   system" and requires 90%, explicitly "regardless of the total points achieved". No 200-point
   total appears in the document. The 90% is right; the 200-point denominator is unsourced.
2. **"Litter: 15% of total space" — PARTIALLY SUPPORTED.** The standard sets an absolute
   minimum: "at least 21.6 square inches per hen of scratch area". 21.6/144 = 15% holds only for
   1.0 sq ft multi-tier housing; for 1.5 sq ft all-litter it is 10%. Stating it as a percentage
   of total space generalizes a per-hen absolute. Harmless for this eval's multi-tier houses,
   wrong as a stated rule.
3. **"0.5 foot-candle (≈5.4 lux)" — minor divergence.** The standard's own parenthetical is
   "0.5 footcandles (5 lux)". 5.4 is the exact conversion but is not what the standard says.

**Reading:** the §12 numbers are substantially correct despite P1 carrying no citations — the
underlying research was sound even though its provenance was not recorded. The failure is
traceability, not (mostly) accuracy.

### 2.1 ⚠️ APHIS indemnity table NOT verified

`world-bible.md` §8 and `corpus/pricing.yml` assert a 2025 VS table with Layer 1st-lay 18–45 wk
at **$18.68/head**. A direct fetch of the APHIS valuation document
(https://www.aphis.usda.gov/media/document/1285/file) **timed out and was not read**. Secondary
reporting found via search states USDA raised the layer indemnity rate in March 2025 "from about
$7 to nearly $17 per lost bird", which does not obviously match $18.68. This may reflect
different age brackets or table versions. **Unresolved — needs the primary APHIS table.**

---

## 3. Citation errors found in the web-sweep research

⚠️ Delegated results — an agent fetched each source and reported these verdicts; they were not
re-checked by this file's author. Where a source could not be retrieved at all, that is stated as
unreachable rather than as an absence of the claim; the two are different and are kept distinct
throughout.

### `2026-07-13-financial-realism-web-sweep.md`

- **NOT SUPPORTED — PMC7823783 temperature bands.** The memo attributes a thermoneutral zone of
  18–24°C, an optimum of 18–21°C, and degradation below ~16°C to this paper. The paper states a
  single range — "The optimum temperature (thermoneutral zone) for laying hens allowing optimal
  performance is between 19 and 22 °C" — and studies only heat stress (26/30°C vs a 24°C
  baseline). None of the three cited figures appear in it. **Temperature bands feed the heat
  model, so this one warrants a look at whether the code inherited the wrong numbers.**
- **PARTIALLY SUPPORTED — FoodPrint feed share.** Memo says feed is 40–70% of cost of
  production; the source says "50-70 percent". The 40% lower bound is not in the source.
- **Misattribution — pullet +7¢/doz and labor +4¢/doz** are credited to FoodPrint but trace to
  the Agri-Pulse/CSES study, a different entry in the memo's own source list.
- **SUPPORTED — PMC10741227** low-temperature performance table: every figure and derived
  percentage checks out.
- ⚠️ **WATTAgNet and Agri-Pulse both returned HTTP 403** with no archive snapshot; their claims
  rest on search-result excerpts only, not the primary pages.

### `2026-07-12-web-sweep-eval-awareness-judge.md`

- **NOT SUPPORTED — arXiv 2604.11978 ("Long-Horizon Task Mirage").** The memo attributes a named
  "premature-completion" phenomenon framed as a harness-design problem. The paper presents a
  seven-category failure taxonomy and never uses that framing.
- **PARTIALLY SUPPORTED — FutureAGI judge-calibration post.** Memo says 100–300 labeled traces;
  the source says 200–500. The κ≥0.8 "strong" and κ<0.5 "rework" thresholds are not in the
  source at all — only κ≥0.6.
- **PARTIALLY SUPPORTED — Meridian Inspect-Petri page.** The cited page mentions only Petri 2.0;
  the memo's "Petri 3.0, May 2026" is not on it. The page is a generic landing page.
- **PARTIALLY SUPPORTED — gemini-cli issue #15772.** The core symptom is confirmed, but the
  memo's broader claim that it is "reported broadly for Gemini-3-family agents in other
  harnesses" is not supported by that issue.
- **PARTIALLY SUPPORTED — Zenith/ii.inc notes.** Confirms premature-completion generally but
  never mentions Gemini-3; grouping it as evidence of that specific phenomenon is the memo's
  inference.
- **SUPPORTED** — Petri 2.0 blog (37.2% / 21.7% / 47.3% all verbatim), LURE arXiv 2605.26438
  (AUROC 0.906; ⚠️ two reads of the same page disagreed on 44% vs 45% FPR), Rulers arXiv
  2601.08654, and two abstract-level checks (arXiv 2509.13333, 2510.20487 — ⚠️ abstract only).

### `p7-noise-eval-awareness-litreview.md` (sources 1–5 of 6)

- **SUPPORTED** — Petri 2025 prose-tell ratios (233×/183×/43×/14×/5.8×) all verbatim; Petri 2.0
  figures; Needham et al. arXiv 2505.23836 (AUC 0.83/0.92, agentic 0.88–0.95 vs chat 0.71–0.77 —
  confirmed in full text, not just abstract); Aranguri & Bloom (3–18pp, 34.9%→13.9%, >60%, ~75%).
- **PARTIALLY SUPPORTED — Apollo Research.** The "up to 33% sandbagging" figure and the
  "lower bound" framing are verbatim, but the "5–10% covert-subversion" range could not be found
  as a stated figure; it appears to be read off a chart.
- Two wording flags: the memo presents "no one is watching" as a quotation when the source says
  "removing explicit language that implied a lack of oversight"; and Aranguri & Bloom's "+25%" is
  the relative figure, not the 12.6-percentage-point figure, which a reader could conflate.

---

## 3b. Stocking density and depopulation — 18 citations checked

**This is the batch that matters most: `docs/plans/` already contains an implementation plan
written against this research.**

### 🔴 The memo's central design argument is not in its cited source

`2026-07-29-stocking-density.md` §1 concludes that density→feather-pecking should be modeled as
"a weak term amplified by genetics," and notes this "conveniently matches DP-D's
`genetics: low_pecking` action." The support cited for that density × genetic-line interaction is
PMC7070775.

**The paper does not contain that finding.** It discusses stocking density and genetic strain
differences as separate, unconnected topics, and explicitly states that the density interaction
it does report (with *group size*, not genetics) has an undetermined mechanism. The claimed
interaction is the load-bearing justification for a design decision, and its stated source does
not support it.

The same source was also cited for a 0.60–0.80 correlation between feather damage and
cannibalism mortality; that figure does not appear in the article either. (`-sources.md` had
already self-flagged this one.)

### Misattribution pattern: right paper, wrong originating claim

Twice, a figure is correctly quoted but credited to a paper that was itself only citing it, and
in both cases the carrier paper's *own* data gives a materially smaller number:

| Memo cites | For | Actually from | Carrier's own finding |
|---|---|---|---|
| PMC9720333 | cannibalism = 18.6% of layer mortality | Fossum et al. 2009 | ~11% |
| PMC10514442 | cage-free costs +36% total / +23% operating | Matthews & Sumner 2015 | +8–19% |

The 36% figure is used in the economics section; the carrier paper's own estimate is roughly half
that.

### Factual error in the reference-density table

Both stocking-density files state "Norwegian aviary maximum 9 birds/m²" and "organic 7 hens/m²".
The cited source (an EU CAP Network practice abstract, Netherlands-based) gives the **EU-wide**
legal maximum as 9 hens/m² for barn/free-range and **6** hens/m² for organic. Both the country
attribution and the organic figure are wrong.

### What held up

- **SUPPORTED in full:** PMC5850468 (520 vs 748 cm²/bird, all production and welfare figures
  digit-exact), PMC4598711 (every ammonia figure, plus correctly reporting that it contains *no*
  density→ammonia coefficient), PMC6527515, PMC9405104.
- **The depopulation research is clean.** Every checkable claim in
  `2026-07-20-depop-welfare-hierarchy.md` confirmed verbatim against primary sources —
  McKeegan et al. aversion timings (CO₂ feeding stops 12.4±2.0 s, median 18 gasps, N₂ 144.7±7.0 s,
  LAPS motionless 141.2±2.7 s, N₂ 399.4±7.9 s), the AVMA/AAAP VSD-vs-VSD+ classification, N₂-foam
  superiority (132 s vs 167 s vs 180 s), and the USDA $100M fund. One gap: the "birds voluntarily
  enter 60–80% CO₂" claim is not in the AAAP PDF and its other source is unreachable, so it
  currently has zero confirmed support.
- **The two stocking-density files agree with each other**, and `-sources.md`'s own honesty
  labels (FULL / ABSTRACT / SUMMARY) proved well calibrated — everything it marked FULL verified
  clean, and the claims it flagged as risky are precisely the ones that failed.

### ⚠️ Unreachable (6)

Tandfonline S4, ScienceDirect S9, dvm360, HSA gaseous-methods, Science.org H5N2 — all HTTP 403
via both fetch and direct curl with a browser user agent. Nature s41598-021-81868-3 hit a login
wall; plain text was recovered by curl and confirmed the 0.35–0.65%/year figure, but the
5–12% / 15.6–20.9% mortality ranges and "Norway 3.74% at 71 wk" could not be located in it.

S9 matters: the memo itself calls its 27±16% ammonia-reduction figure "the single most
load-bearing unverified number in the pass". It remains unverified — the paywall held.

---

## 3c. `2026-08-03-dairy-telemetry-parameters.md` — 9 citations checked

The newest document in the directory, and it contains the audit's only **contradicted** claim.

### 🔴 A figure attributed to a paper that states the opposite

The memo credits "1.5 kg/day more milk in the automated group over the first three weeks" to
PubMed 37678785. That paper's own abstract says: *"No differences were detectable between
treatments in daily or total milk yield to 21 DIM."* It is also a different trial from the one
described (n = 625/624, not 607/597), and disorder diagnosis was higher in the *visual-leaning*
arm, not the automated one.

This is worse than an unsupported citation — the cited source directly contradicts the claim. The
figure most plausibly belongs to the 2026 economic companion paper, but ⚠️ that paper is
paywalled and the reattribution rests on search-engine synthesis, not its primary text.

### "Corroborated jointly" overstates one source

The 21%-of-alerts-prompt-a-visual-check figure, plus its three behavioural modifiers, is
presented as jointly corroborated by two papers. It appears in PMC9186058 only — verbatim, along
with the modifiers. The Animal Bioscience paper does **not** contain it; that paper supports only
the separate point about practitioners experiencing alert quality through predictive values
rather than sensitivity and specificity. Two other claims attributed to PMC9186058 — that
repeated false alarms erode trust, and that 24/7 alerting is a stressor in European and Canadian
studies — were not found in it either.

### What held up

Exact, digit-for-digit matches on the economic evaluation (net-return ranges by herd-health
scenario and the full five-disease sensitivity table), the mastitis-challenge trial (sensitivity
70.0%, specificity 86.7%, 78.3% flagged ≥24 h early, 0.54°C rise), and the Wisconsin 37-farm
study (50,329 cow-lactations and the full nine-disease incidence table).

### ⚠️ Unreachable (3)

The 2013 reticular-bolus paper (403 at the cited URL; confirmed instead through secondary quotes),
the Cornell RCT (403 across four separate routes), and the 2026 economic companion (403/405).
The Cornell figures — 61%/24% examined, 37%/22% diagnosed — could only be sourced from an AI
search synthesis that showed signs of blending two companion papers with different group sizes.
**Do not wire those numbers into anything until the paper is read directly.**

---

## 3d. `2026-07-28-substrate-realism/` — 43 citation targets, all 5 files read in full

**This batch is the most solid research in the directory.** 28 targets were readable; the great
majority matched digit for digit, including Stratmann 2015 (soft vs hard perch 15.4%/21.5%,
P=0.0012), Abraham 2023 (bone mineral content, keel volume, mortality 9.9% vs 6.3%), Thøfner 2021
(4,794 birds, 86.16% prevalence, all three odds ratios), Cloft 2026 (four strains at 79 wk),
Rentsch 2024, Chew 2021, and the EIA Iowa electricity rates. All four rows the README itself
marks "VERIFIED at source" reconfirmed exactly, and the README's own self-correction about the
ramps review turned out to be accurate.

Three problems worth acting on:

1. **🔴 A floating number attributed to the wrong paper.** `keel-interventions.md` states
   "Heritability 0.08 ± 0.04 (0.22 log-transformed)" directly after the Kittelsen 2021 citation.
   That paper contains no heritability analysis at all — and could not, since it explicitly
   lacked individual-animal tagging. The figure's real source is unidentified.
2. **A citation that can never verify what it is cited for.** `egg-channel-value.md` cites
   `ams.usda.gov/mnreports/ams_3725.pdf` for a specific week's prices. That URL is USDA's *live*
   weekly bulletin — fetching it now returns a different week entirely (shell $1.31/doz against
   the cited $0.33). The underlying figures do check out via a secondary aggregator, but the
   primary citation points at content that will never again match.
3. **Minor price drifts:** Iowa wholesale propane peaked at $1.136/gal against a claimed
   $0.71–0.96 range; a Farm Bureau shell price is $0.25/doz where $0.35 is cited.

**`vitamin-d3-decision.md` confirmed unsourceable.** Read end to end: every apparent citation is
an unresolvable token. Every hard number in it — Hy-Line 3,300 IU/kg, the NRC 300 IU/kg floor,
the FDA 69 ppb ceiling, the IU conversion factor, adoption and national flock counts, and four
unnamed "Study A–D" trials — rests on them. Two of its underlying findings (Käppeli, Abraham) are
independently corroborated through properly-linked citations elsewhere in the same folder; the
rest have no followable trail.

⚠️ **15 of 43 targets unreachable**, mostly 403s and reCAPTCHA walls. The two that matter most:
the Stratmann 2015 *Applied Animal Behaviour Science* ramps paper — which drives the 0.80 ramp
factor, the single most important coefficient in the keel design — and the 1992 *Applied Poultry
Science* paper that is the sole source for the 0.75 breaker-value fraction.

## 3e. `p7-noise-eval-awareness-litreview.md` — remaining items

- **Probable wrong arXiv ID:** 2502.19669 is cited for "LLM reading comprehension is robust to
  typos", but resolves to a mechanistic-interpretability paper about which neurons and attention
  heads repair typos. Adjacent topic, not the claim made.
- **Three citations carry no URL or ID at all** — the Sonnet 4.5 system card (cited for a
  specific 13% figure and a steering result), the WebChoreArena/GAIA/Vending-Bench trio, and the
  Karvonen post. All were findable by search, and all checked out once found, but a reader cannot
  verify them from the document as written. Recovered links are in the batch report.
- **A naming collision is real and worth a footnote:** RULER (arXiv 2404.06654, long-context
  benchmark) and Rulers (arXiv 2601.08654, LLM-judge scoring framework) are genuinely different
  papers cited in neighbouring documents.
- **Minor:** the MITRE technique is officially "Virtualization/Sandbox Evasion: Time Based
  Checks", not "Time Based Evasion"; substance is right.
- **Confirmed exactly:** the Agentic Misalignment figures (55.1% vs 6.5%, ≈8.5×) with both
  self-diagnosed artifacts verbatim, SWE-Bench Illusion (76% vs ≤53%), and the synthetic-document
  finetuning findings. ⚠️ The Sonnet 4.5 system card PDF exceeded the fetch size limit and was
  checked only through secondary write-ups.

---

## 3f. `SOURCES.md` — the master registry, ~32 resolvable entries plus the UEP set

⚠️ Delegated result; the registry was read end to end (230 lines) by the agent, not by this
file's author.

### 🔴 Several UEP compliance numbers are wrong at the primary source

The registry carries its own "verify-before-hardcode checklist", and it names the UEP 2024
cage-free numbers as the single highest-priority set to check — precisely because its authors
could not get the PDF to parse. The agent located a copy and read all 29 pages. Four registry
entries do not survive. ⚠️ Three of the four (lighting, beak trim, the feeder/drinker merger)
sit on that eight-item checklist; the litter/scratch row is a separate registry entry. The
author of this file has not independently confirmed which rows compose the eight, so treat the
grouping, not the individual findings, as the soft part:

| Registry says | UEP 2024 actually says |
|---|---|
| "≥30% litter/scratch (proposed)" | an absolute **21.6 sq in per hen** — not a percentage at all |
| "UEP ≥10 lux" | **0.5 foot-candle ≈ 5 lux** — half the cited value |
| "≤½ upper / ⅓ lower beak" | "no more than **one-third of the upper beak**" — no lower-beak allowance exists |
| feeder space "max 26 ft travel" | the 26-foot limit is a **water/drinker** spec; two guideline items merged into one row |

Ammonia, nest space, perch space, the 1.5 in/hen feeder figure and the non-feed-withdrawal molt
rule all check out. Stocking density is right for multi-tier but omits the 1.5 ft²/hen
single-level case.

**This independently corroborates §2 from a second copy of the standard** — the lighting figure
in particular (≈5 lux, not 10) matches what was extracted locally there. It also vindicates the
registry's decision to single these numbers out as needing verification before use. Note the flag
does not discriminate between good and bad entries: all eight checklist rows carried the same
warning, and most of them passed. The flag identified the right *area* of risk, not the
individual failures.

### Other findings

- **WRONG TARGET:** PMC4897471 is cited for HPAI incubation being 1–5 days subclinical. It
  resolves to a 2014 paper on H5N1 mortality and pathology in Nigeria, which does not discuss
  incubation.
- **NOT SUPPORTED:** PMC10741227 is cited for a lower critical temperature of ~18°C, winter
  targets and a +4 kcal/°C figure. It contains none of them. (The same paper *does* correctly
  support a different claim elsewhere in the corpus — see §3, where its cold-stress table
  verified digit-exact. The paper is fine; one of the two citations is not.)
- **Numbers that drifted:** catching costs are cited as €8,540 vs €4,856 where the paper says
  €7,984 vs €4,506; keel-fracture prevalence is cited as 60–80% where the paper reports 86%
  overall, and the 11.6% vs 4.9% multi-tier comparison is not in it; a retail egg price is cited
  to a CBS article that only runs to December 2024 (the figure itself is real, and is $6.23 not
  $6.22, from other reporting).
- **A duplicate the registry does not flag:** two rows cite the same Gonzales & Elbers paper, once
  by DOI and once by PMC ID, and one of the two overstates it — the paper says detection took a
  mean of 12 days after mortality onset, which does not support "mass mortality within days".
- **A claim attributed to the wrong artifact:** honeypot-placement strategy is cited to the PETRI
  GitHub repository, whose README contains no discussion of it.
- **The same moving-target citation, third independent sighting:** "USDA AMS (Jun 2026)" for
  $0.50/$0.11 channel prices resolves to the live weekly bulletin, now showing $1.31/$0.2375.
- **Confirmed exactly:** heat mortality and panting onset, transport cold-kill mortality by
  temperature and distance, VSD+ time-to-death, the HPAI detection thresholds, RT-PCR latency,
  the egg-yolk drug-withdrawal table across two correctly-split sources, OSHA/NIOSH ammonia
  limits, and the EPA nitrate MCL.

⚠️ **Unreachable (9):** Federal Register, two FDA pages (404), CRS R48518, two USDA press releases,
Science.org, WATTPoultry, and High Plains Journal — bot-blocks and 403s rather than absent
content.

**Credit where due:** the registry's status legend is honest. It marks its own weak entries, and
the audit's failures cluster in exactly the rows it had already flagged.

---

## 3g. Web-sweep batch, clean re-dispatch

⚠️ Delegated result, like §§3–3f; the author did not re-read these sources.

The re-run reached the same conclusions as the compromised first attempt on every headline point
(temperature bands, the FutureAGI trace count of 200–500 not 100–300, the missing Petri 3.0
label, the FoodPrint misattribution), and added:

- The Long-Horizon Task Mirage and SHADE-Arena papers are used to support framings — "harness
  design problem" and "document volume as camouflage" — that their own abstracts do not state.
- Three citations carry no URL at all; one link is a dead redirect (`goodfire.ai` → `goodfire.com`).
- The Cornell RCT's group sizes and direction check out, but its 61%/24%/37%/22% figures are not
  in the reachable abstract. ⚠️ Do not wire those numbers in without the full text.

---

## 4. Method and coverage

Each batch was told to read its target documents end to end, fetch every cited source, and return
an explicit coverage statement naming anything it could not read in full.

⚠️ **Retrieval limit applying to everything above:** sources were reached through a fetch tool
that converts a page and extracts against a prompt, so "read in full" means the fetch returned
the whole page and reported doing so — not that raw HTML was inspected. Two reads of the same
LURE page disagreed on one digit, which is direct evidence this layer is not perfectly reliable.
The UEP standard in §2 is the exception: that PDF was extracted locally with `pdftotext` and the
quoted text is from the file itself.

⚠️ **One batch failed its brief.** The agent assigned the web-sweep files delegated its own work
instead of doing it and returned no findings. Its unauthorized sub-agents did return usable
reports, which is where §3 comes from; the batch has been re-dispatched with explicit
constraints, so §3 may be superseded or extended.

## 5. The findings that change what someone would do

Ranked by consequence. Nothing below has been changed; this is for adjudication.

⚠️ **Confidence differs by item — read the provenance before acting.** Each delegated item below
is a lead strong enough to justify opening the paper, and not strong enough to act on before
someone does. Item 3 comes from the batch whose first agent violated its brief; a clean
re-dispatch reached the same conclusion independently, which makes it the best-supported of the
delegated set. Items 1, 2, 4 and 5 each rest on a single agent's report.

**Item 6 is the exception and is not delegated.** Its UEP half was checked directly by this
file's author against a locally extracted copy of the standard, and independently corroborated
by an agent working from a different copy. Treat it as established — except the APHIS indemnity
table, which remains unverified.

1. **Stocking density: the central design argument has no source.** The density × genetic-line
   interaction justifying "weak term amplified by genetics" is not in PMC7070775. An
   implementation plan is already written against this. (§3b)
2. **Dairy telemetry: a claim contradicted by its own citation.** "1.5 kg/day more milk" is
   credited to a paper whose abstract says no milk-yield difference was detectable. (§3c)
3. **Financial realism: temperature bands not in the cited paper.** 18–24°C / 18–21°C / below-16°C
   are absent from PMC7823783, which gives a single 19–22°C range and studies only heat stress.
   Temperature feeds the heat model. (§3)
4. **Attribution errors in four places — related, but not one mechanism.** Two are the same
   carrier-paper failure, where a figure is credited to a paper that was itself only quoting it
   and whose own number is materially different: cannibalism 18.6% vs ~11%, and cage-free cost
   +36% vs +8–19%. The other two are different faults — a heritability figure sitting beside a
   paper that contains no heritability analysis, and a 21% alert figure credited to two papers
   when only one contains it. What they share is that the citation does not lead to the number.
   (§3b, §3c, §3d)
5. **Four wrong UEP compliance numbers in the master registry**, three of them on its own
   highest-priority verify-before-hardcode list: lighting at 10 lux rather than ≈5, beak trim
   allowing a lower-beak cut that does not exist in the standard, a drinker distance recorded as
   a feeder spec, and (a separate registry row) litter as a percentage rather than 21.6 sq in per
   hen. (§3f)
6. **Regulatory provenance is one hop short.** P1 carries no source links, yet supplies the
   world bible's "firm" numbers and `corpus/pricing.yml`. The world-bible half now verifies
   (11 of 14 exact, checked directly); ⚠️ the APHIS indemnity table remains unverified. (§1.1,
   §2, §2.1)

**The counterweight:** the substrate-realism folder and the depopulation research are in good
shape — dozens of figures confirmed digit-exact against primary sources, and their authors' own
confidence labels proved well calibrated. The problem is concentrated, not general.

**Not in scope of this pass:** the `v2-*` files (~77 citations). They target a future redesign
that nothing is built on yet, so they were deprioritized rather than cleared.
