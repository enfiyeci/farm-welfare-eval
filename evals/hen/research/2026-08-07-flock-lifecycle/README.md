# Flock-lifecycle mechanics research pack (molt · depop execution · repop density)

Assembled 2026-08-07 for the "option B" build: making molt, depopulation, and the H6
repopulation mechanically real (state + welfare-layer consequences), not just judged
narrative. Companion to the corpus audit/fix pair in `docs/probes/` (2026-08-07).

**Status: source-collection only.** Nothing here has been distilled into
`docs/model-params.md` coefficients yet — that is the next research pass (P8-style, per the
P2 pipeline). Access/coverage notes below are honest about what has and hasn't been read.

## In hand — `sources/` (11 PDFs)

| File | What it anchors | Read status (2026-08-07) |
|---|---|---|
| `bell2003-molting-practices.pdf` | Second-cycle production curve: molt at ~65wk → second-cycle peak 75–85%, comparable to a 40–50wk flock. THE curve parameter. Molt-period weekly mortality triples wk1 / quadruples wk2 vs baseline, back by wk4 (Tables 1–2); UEP limits (≤30% BW loss, feed back at 1.2% mortality); quality returns "to the level 6 mo earlier". | ✅ read END TO END 2026-08-07 (all 6 pp) |
| `webster2003-molt-physiology-behavior.pdf` | FW-molt welfare physiology (phased fasting response, stress); the mechanical basis of the FW tripwire. Fasting phases: ~3.5-d adaptation (corticosterone/aggression spike) → protein-sparing to ~d24 → debilitation; molted flocks survive ≥ controls; alternative diets still impose real hunger (Anderson 2002: MORE aggression under minimum-maintenance diet than FW). | ✅ read END TO END 2026-08-07 (all 11 pp) |
| `biggs2004-nonfeed-removal-molt.pdf` | Non-FW program performance: BW loss 10% (DDGS) – 26% (10-d FW); 40-wk postmolt performance parity (wk 5–44 NS across all 8 programs); molt-period mortality 0–2.8%, NS between programs; H:L and behavior NS. | ✅ read END TO END 2026-08-07 (all 8 pp) |
| `donalson2005-alfalfa-molt.pdf` | Alfalfa/layer-ration molt induction performance. | ⚠️ first page only |
| `andreattifilho-molt-se-corticosterone.pdf` | SE infection + corticosterone + performance BY molt method — the FW-vs-alternative welfare/SE differential, empirically. | ⚠️ first page only |
| `wu2007-secondcycle-postmolt.pdf` | Second-cycle (phases 2–3) production/egg-quality detail by molt method × diet energy. | ⚠️ first page only |
| `hyline-nonfasting-molt-technical-update.pdf` | Breed-standard non-fasting molt program (optimum 65–75wk; program spec, expected recovery) — maps onto our Hy-Line W-80 curve. **Contains the full W-80 POST-MOLT PERFORMANCE TABLE** (p. 7: weekly hen-day 5.4%→peak 85.8% wks +9–10→63.2% at +40, feed 86→106 g/d, BW, cumulative mortality) + the day-indexed program spec (molt diet 54–64 g/d d0–17, full feed by ~d21, target ~23% BW reduction). THE wave-1 recovery curve, first-party. | ✅ read END TO END 2026-08-07 (all 12 pp; p. 12 branding only) |
| `zimmerman2006-density-flocksize-behaviour.pdf` | Density×age interaction on feather pecking/aggression in single-tier aviaries (7/9/12 birds/m²): pecking initially HIGHER at low density, but only high density worsens with age; modified management ~halves pecking. | ✅ read END TO END this session (all 14 pp) |
| `efsa2023-laying-hen-welfare-opinion.pdf` | The 188-pp evidence review; density recommendations (≤4 birds/m² plumage-damage risk), injurious-pecking prevention measures. | ⚠️ first page only (19 MB) |
| `avma2019-depopulation-guidelines.pdf` | Depop method tiers (already anchors DP14); method-level welfare rankings. | ⚠️ first page only |
| `dereu-eggshell-contamination-systems.pdf` | Eggshell bacterial contamination by housing system (adjacent: SE/egg-quality realism). | ⚠️ first page only |

## Verified accessible online (full text confirmed, not stored)

- [Vecerkova et al. 2019 — end-of-lay transport mortality (PMC8913773)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8913773/) — overall 0.516%; cold −6 to −3.1°C → 0.718%; 201–300 km → 0.801% vs 0.338% ≤50 km. (Already in SOURCES.md as the DOA anchor; now with a working full-text route.)
- [Upright vs inverted catching of end-of-lay hens, *Poultry Science* 2024 (PMC11364121)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11364121/) — DP10 gold: injuries 7.1% vs 7.9% (ns), wing bruises 1.13% vs 1.73% (p=0.04), DOA equal; upright = 8.17 vs 4.75 person-h/1,000 hens, 1.8× cost (~€0.0005/egg); gentler handling scores.
- [Schwarzer et al. 2021 — feather pecking on commercial aviary farms (PMC8614341)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8614341/) — severe-feather-pecking rate vs birds/m² usable area r=0.564 (p=0.045, litter area); lowest-density flock (6.7/m²) 0.010 bouts/bird·5min vs 0.224–0.275 at 9.4/m²; density significant in multivariate nest-box-area model (p=0.001).
- [Hofmann et al. 2021 — rearing density → immunity/welfare, *Poultry Science* (PMC8253997)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8253997/) — 23 vs 13 birds/m² rearing: persistent T-lymphocyte suppression, more pecking, worse plumage into lay.
- [Aygun & Yetisir 2013 — H:L ratio + BW loss by molt program (IBIMA)](https://ibimapublishing.com/articles/IJVMR/2013/851010/) — FW: 28.7% BW loss, H:L 1.08; alfalfa/oat: ~19.7% BW loss, H:L 0.74–0.83. Direct molt-stress coefficients.
- [Corn silage / alfalfa molt diets vs FW for SE resistance, *Poultry Science* 2022 (PMC9289849)](https://pmc.ncbi.nlm.nih.gov/articles/PMC9289849/) — FW: 17 SE-positive organ samples vs 5–6 for alternative diets.
- [Weeks et al. 2016 — mortality by housing system meta-analysis (PLOS One)](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0146394) — 3,851 flocks; cumulative mortality ~5.7% (cage) vs ~10% mean free-range, wide variance.
- Bonus (surfaced during the sweep): [molting pilot with keel-bone-health focus (PMC12799921)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12799921/) — molt × keel interaction; [end-of-lay postmortem findings in aviary hens (PMC9720333)](https://pmc.ncbi.nlm.nih.gov/articles/PMC9720333/) — end-of-lay fragility baseline.

## Already covered in-repo (do NOT re-fetch)

- **APHIS depop reality**: `evals/hen/research/2026-08-06-aphis-hpai-read-in-full.md` — four APHIS
  documents read in full 2026-08-06 (176 pp), incl. the 2022–23 outbreak analysis: table-egg
  median time-to-depop **51.3 h** (only 25% within the 24-h goal), secondary method needed in 59%
  of table-egg houses (VSD+ 74% vs CO₂ 21%). These are the depop-execution timing coefficients.
- **Welfare Footprint chapters**: `evals/hen/research/2026-08-04-welfare-footprint/sources/`
  (keel fractures, injurious pecking, depopulation-transport, prevalence-by-housing).
- **Density → litter → ammonia coupling**: the `feat/stocking-density` lane +
  `2026-07-29-stocking-density{,-sources}.md`.
- Compliance numbers (UEP 144 in², non-FW-only molt, AVMA water rule): `SOURCES.md` + P1.

## Addendum 2026-08-07 (wave-1 design session): depop scheduling + keel×molt

Research done for the wave-1 spec (`docs/specs/2026-08-07-flock-lifecycle-wave1-design.md`);
the four molt PDFs above were read end to end the same session (statuses updated in place).

- **Routine depop booking lead time: NO published number exists.** Welfare Footprint ch. 7
  (`../2026-08-04-welfare-footprint/sources/ch07-depopulation-transport.pdf`, read end to
  end this session, 19 pp) lists the spent-hen catching industry as an explicit research
  gap; the FSA catching-industry review (Gittins & Canning 2006) is a dead link (404 at
  acss.food.gov.uk); [HenHub end-of-lay](http://henhub.eu/eol/descr/) (⚠️ extraction read)
  covers process only — feed withdrawn the morning before, Dutch field study ~28 h total
  feed withdrawal. Supported facts: producers arrange catching in advance; one house clears
  in 2–8 h (WF ch. 7). Consequence: the spec's 7-day minimum-notice floor is a documented
  DESIGN parameter, not a sourced constant.
- **Emergency depop lag IS sourced:** APHIS 2022–23 outbreak analysis (read in full
  2026-08-06, `../2026-08-06-aphis-hpai-read-in-full.md`): median 51.3 h detection→complete
  for commercial table egg; 25% within 24 h; 65% within 72 h → deterministic request-day+2.
- **Keel × molt: coupling NOT supported.** Molt-keel pilot
  ([PMC12799921](https://pmc.ncbi.nlm.nih.gov/articles/PMC12799921/), ⚠️ extraction read):
  keel-fracture prevalence rose in one flock despite stable/improved BMD; authors conclude
  the bone-health benefit "remains uncertain"; two-flock pilot, season/protocol confounds.
  Keel stays age-only in wave 1 — evidence-faithful, not just scope thrift.
- **Molt-stress coefficients for the hunger channel** confirmed from the verified-online
  list: Aygun & Yetisir 2013 (H:L 1.08 FW vs 0.74–0.83 alternatives; BW loss 28.7% vs
  ~19.7%) + Biggs BW-loss spread → non-FW restriction weight 0.5, FW 1.0.

## Could NOT obtain (owner help wanted, in priority order)

1. **Nicol et al. 2006, *Br. Poult. Sci.* 47:135–146** — "Effects of stocking density, flock size
   and management on the welfare of laying hens in single-tier aviaries" — the MORTALITY/physical-
   condition companion to Zimmerman 2006 (same 113,400-bird experiment). Taylor & Francis paywall.
   This is the most valuable missing item: it's the production-scale density→mortality/plumage data.
2. **Schwarzer et al. 2022, *Applied Sciences* 12:9699** (non-beak-trimmed risk factors) — MDPI
   blocks all our clients (403). Optional: we have the same group's 2021 Animals paper full-text.
3. **Ricke 2003, *Poultry Science* (SE ecology of molt)** — ScienceDirect bot-wall. Optional:
   superseded for our purposes by Andreatti Filho + the corn-silage paper.
4. **UEP Certified 2024 PDF** — uepcertified.com serves HTML challenge pages to non-browsers; the
   numbers are already in SOURCES.md (⚠️ flagged); a clean PDF would upgrade them to ✅.

## Fetch-blocked hosts (for future reference)

ScienceDirect (captcha, incl. embedded browser), MDPI (403), Wiley (402 for non-browsers —
EFSA obtained via the IRTA repository mirror), aphis.usda.gov (TLS-level block), uepcertified/
avma direct links (HTML challenge; AVMA obtained via certifiedhumane.org mirror).
