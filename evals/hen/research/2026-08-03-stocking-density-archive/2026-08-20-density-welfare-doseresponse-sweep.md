# Density → welfare dose-response — supplementary sweep (2026-08-20)

**Why this ran.** DP25 node review, owner comment #169: "make sure we have a dynamic that accurately
calculates the welfare effects of the added chickens, make sure you do research." This sweep supplements the
in-repo primary research (Kang 2018 read in full, Groot Koerkamp) with a wider dose-response check across
mortality, keel, footpad, feather, and stress endpoints.

**Provenance / read discipline.** Run by a delegated research subagent (sonnet), 2026-08-20. ⚠️ **Coverage is
abstract-level throughout — the subagent read NONE of these sources end to end** (journal paywalls/login walls
blocked full text on nearly every one). Every row is flagged with a read level; two rows (EFSA 2023, Wilkins
2011) are SECONDARY (reconstructed from search-engine summaries, not the document) and are the weakest. The
design conclusion below rests on the *convergence* of many abstract-level sources PLUS the already-full-read
Kang 2018 [see `2026-07-31-density-decision-research.md`], not on any single unverified row. Anything the owner
will lean on numerically should be traced to source before the build encodes it.

**Bottom line.** Kang's ~19 hens/m² footprint knee is the best-quantified density threshold in the literature,
and nothing here contradicts it. Below the knee (~6–17 hens/m²) there is **no clean continuous dose-response**
for mortality, keel, footpad, or feather — the field evidence is null, inconsistent in direction, or U-shaped.
So the DP25 accrued-harm dynamic should be **threshold-shaped** (fires once density crosses into the
high-density regime), not a smooth sub-knee slope — which is exactly the shape the wired `density_factor`
already has.

## Source table (all read levels are the subagent's; ⚠️ = not read end to end)

| # | Source | System / n | Density comparison | Key finding | Read level |
|---|---|---|---|---|---|
| 1 | Nicol et al. 2006, *Br Poult Sci* 47(2):135–146, [DOI](https://doi.org/10.1080/00071660600610609) | Commercial single-tier aviary, Shaver, 36 flocks/113,400 birds | 7 vs 9 vs 12 hens/m² | Mortality **non-monotonic** (9/m² > 12/m²); keel fracture ~60% by end of lay across all treatments; lower density → *poorer* feather condition | ABSTRACT ⚠️ (T&F paywalled) |
| 2 | Zimmerman et al. 2006, *Appl Anim Behav Sci* 101(1–2):111–124, [DOI](https://doi.org/10.1016/j.applanim.2006.01.005) | Companion to #1 | 7/9/12 hens/m² | Feather pecking/aggression rose with age only at 12/m², but *initial* level highest at low density (hierarchy effect) | ABSTRACT ⚠️ |
| 3 | Steenfeldt & Nielsen 2015, *Animal* 9(9):1509–1517, [DOI](https://doi.org/10.1017/S1751731115000713) | Organic multi-tier aviary | 6 vs 9 vs 12 hens/m² indoor | Laying rate lower at 12/m² (90.6 vs 94.3%); authors: welfare consequences "minor" | ABSTRACT ⚠️ |
| 4 | Wilkins et al. 2011, *Vet Rec* 169(16):414, [DOI](https://doi.org/10.1136/vr.d4831) | UK field survey, 67 flocks / 8 housing types | Housing type, not density | Keel damage 36% (furnished cages ⚠️CAGED) up to >80% in multilevel-perch systems — complexity, not density | SECONDARY ⚠️⚠️ |
| 5 | Rufener & Makagon 2020, *J Anim Sci* 98(S1):S36–S51, [link](https://academic.oup.com/jas/article/98/Supplement_1/S36/5894015) | Systematic review | Not a density gradient | KBF lowest in conventional cages, highest in furnished/floor/single-tier; **could not analyze density** (source studies don't report it usably) | ABSTRACT/partial ⚠️ |
| 6 | Decina et al. 2019, *BMC Vet Res* 15:435, [DOI](https://doi.org/10.1186/s12917-019-2168-2) | Canadian survey, 39 non-cage flocks | Density collected but **excluded from final model** | 6 management variables explained 64% of feather-damage variance; **density not a significant predictor** | ABSTRACT ⚠️ |
| 7 | Volkmann et al. 2024, *Ann Appl Biol* 185(1):108–115, [DOI](https://onlinelibrary.wiley.com/doi/10.1111/aab.12923) | German survey, 39 flocks/15,448 hens | Flock size (density unclear) | FPD driven by litter type/season/age (P<0.0001); **flock size not related** (P=0.878); 34.4% ≥ slight FPD | ABSTRACT ⚠️ |
| 8 | Schuck-Paim et al. 2021, *Sci Rep* 11:3052, [DOI](https://doi.org/10.1038/s41598-021-81868-3) | Meta-analysis, 6,040 flocks / ~176M hens | System type, not density | Mortality converges ~3–5% at 60 wk; falls 0.35–0.65 pp/yr operator experience; **does not isolate density** | ABSTRACT/partial ⚠️ |
| 9 | Campbell et al. 2017, *Animal* 11(6):1036–1045, [DOI](https://doi.org/10.1017/S1751731116002342) | Free-range **outdoor range** density ⚠️ | 2,000/10,000/20,000 hens/ha | Corticosterone highest at 20,000/ha; **middle density lowest** (non-monotonic); keel damage ↑ with age at all | ABSTRACT ⚠️ |
| 10 | Abraham et al. 2024, *Animals* 14(10):1513, [DOI](https://doi.org/10.3390/ani14101513) | Cage-free **pullets** ⚠️, Lohmann, 2,930 birds | ~16.2 vs ~8.0 hens/m² | Density main effect on only 1 measure (bursa weight); **no** effect on mortality, corticosterone, H:L, FCR | ABSTRACT ⚠️ |
| 11 | von Eugen et al. 2019, *Animals* 9(2):53, [DOI](https://doi.org/10.3390/ani9020053) | Laying **chicks** ⚠️ | under/conventional/over-crowded | Corticosterone elevated at **both** extremes — **U-shaped**, not monotonic | ABSTRACT ⚠️ |
| 12 | Janicka et al. 2025, *Animals* 15(4):604, [DOI](https://doi.org/10.3390/ani15040604) | Floor pens, heritage breed ⚠️ | 3/6/9 hens/m² | No corticosterone/cortisol difference; low-density birds more locomotion | ABSTRACT ⚠️ |
| 13 | EFSA (Nielsen et al.) 2023, *EFSA J* 21(2):7789, [DOI](https://doi.org/10.2903/j.efsa.2023.7789) | EU scientific opinion | Recommends max 4 hens/m² cage-free | States adult-hen density↔injurious-pecking associations are "**inconsistent**"; 4/m² reads precautionary, not a demonstrated knee | SECONDARY ⚠️⚠️ |

## Synthesis

- **Threshold, not slope.** Kang's break at ~19 hens/m² footprint is the sharpest quantified knee; Campbell
  (jump only at the highest outdoor density) and Nicol (all of 7/9/12 hens/m² "relatively poor regardless")
  are directionally consistent with the real knee sitting at the high end of the practical range.
- **No sub-knee continuous dose-response.** Mortality (Nicol non-monotonic; Schuck-Paim system-driven), keel
  (Wilkins/Rufener: complexity not density; review can't test density), footpad (Volkmann: litter/season/age,
  not flock size), feather (Decina drops density), and stress (von Eugen U-shaped; Campbell non-monotonic) all
  fail to support a smooth "more density = worse" line below Kang's knee.
- **Design implication.** Model the accrued-harm term as a threshold/knee anchored near Kang's regime for the
  physiological/environmental cluster (litter, ammonia, corticosterone, production, floor eggs); keep
  mortality/keel/footpad/feather flat below the knee (or driven by other levers already in the model). The
  wired `density_factor` (flat below evaporative capacity, super-linear above) already has this shape.
- **Definitional flag.** Kang = pen footprint; the sim's `density_factor` = hens/m² litter; the band = in²/hen
  usable. Reconcile via the [17] litter fraction (~45%) and tier multiplier (~1.85×); keep the knee on the
  litter-basis axis the water balance uses.

## Coverage statement (subagent, verbatim intent)

Opened ~20 URLs across PubMed, Europe PMC (+REST API), PMC mirrors, ScienceDirect, Cambridge Core, Wiley/EFSA,
T&F, Springer, MDPI, Oxford Academic, a Wageningen portal page, Crossref, and an IRTA PDF mirror. **Read to the
end: none** (every row ⚠️). Reachable as abstracts: rows marked ABSTRACT. Reconstructed from search summaries
only (weakest): EFSA 2023 (row 13) and Wilkins 2011 (row 4). Could not reach at all: the EFSA opinion full
text and Wilkins full text.

## Open follow-ups (owner may direct)

1. Confirm the sim's `hens/m²` convention (footprint vs usable) so the build places the knee correctly.
2. Chase full-text for EFSA 2023 + Wilkins 2011 through an institutional route if their numbers get leaned on.
