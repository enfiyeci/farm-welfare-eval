# Footpad dermatitis thresholds in laying hens — evidence for the DP16 banding decision

> Commissioned 2026-08-05 to settle one question: is the 1.3-percentage-point spread DP16 produces
> (15.03% diligent vs 16.32% do-nothing) a welfare-meaningful difference, and would moving a band
> boundary through it be defensible?
>
> Findings are attributed to a delegated research pass, not independently re-read by the orchestrator.
> Every ⚠️ is carried through verbatim from the researcher — do not silently drop them when citing this.

## The answer: no, and moving the boundary is not defensible

Three independent lines converge.

**1. No scheme publishes a bright-line prevalence percentage for laying hens at all.** The
[Welfare Quality assessment protocol for laying hens v2.0](https://www.welfarequalitynetwork.net/media/1294/wq_laying_hen_protocol_20_def-december-2019.pdf)
— the most rigorous system in existence — deliberately avoids percentage cut-points, and says why in
its own methodology: experts do not reason linearly about prevalence, so *"for a given disorder a 10%
increase does not yield the same decrement in expert scores at the bottom of the scale... than at the
top."* It uses non-linear I-spline functions specifically to avoid treating equal percentage-point gaps
as equally meaningful. **The one system built by domain experts to turn prevalence into a welfare score
was engineered to reject exactly the move option (b) proposes.**

Its footpad measure is a 3-point scale (0 = intact; 1 = necrosis/proliferation or chronic bumble foot
without dorsally visible swelling; 2 = dorsally visible swelling), reported as the flock percentage in
each category and then fed through the non-linear index. The raw percentage is never itself a pass/fail.

**2. Real flock-to-flock variation is 60–90 points, not 1.3.**

| Study | Population | Prevalence |
|---|---|---|
| [HealthyHens, 8 European countries](https://pmc.ncbi.nlm.nih.gov/articles/PMC7697283/) | 107 organic flocks | mean 30.5%, range **0–80%** |
| [Italian commercial farms](https://pmc.ncbi.nlm.nih.gov/articles/PMC12032332/) | 50 flocks, WQ 0/1/2 scale | mean 46.3%, range **9.0–91.5%**; by system: enriched cage 34.1%, multi-tier 46.1%, floor 59.5% |
| Weitzenbürger et al. 2006, *Br. Poult. Sci.* 47(5):533–43 | small-group + furnished cages | 60–93% ⚠️ search synthesis only |
| Niebuhr et al. 2009, 8th Eur. Symp. Poultry Welfare | ~300 non-cage flocks | mean ~40% ⚠️ search synthesis only |

Housing system alone moves the mean by ~25 points. **A model whose best and worst policies differ by
1.3 points is not spanning the real signal** — which points at the lever being too weak, not the bands
being wrong.

**3. Several major schemes have no layer footpad standard at all.** Global Animal Partnership's
[5-Step laying-hen audit tool](https://certifiedhumane.org/wp-content/uploads/Standard_LayingHens-2023.pdf)
(⚠️ link is Certified Humane; the GAP tool was read separately) contains **no footpad item across any
step**, only a generic litter check ("is more than 10% of the litter area wet or caked?"). GAP's
*broiler* standard does cap footpad at an annual average score of 2 — an asymmetry worth noting. The
[RSPCA UK layer standards, July 2025](https://www.rspca.org.uk/documents/d/rspca/rspca-welfare-standards-for-laying-hens)
Health section has a detailed quantitative feather-loss protocol but **no footpad standard**.

## The only concrete numeric threshold found anywhere

Sweden and Denmark's **broiler** monitoring scheme sets a threshold of **80** on a severity-weighted
0–100 index (score-1 feet × 0.5, score-2 feet × 2, normalised) — not a raw prevalence percentage. Source:
[EURCAW-Poultry factsheet, "Foot Pad dermatitis (FPD) in Broiler Chicken"](https://sitesv2.anses.fr/en/system/files/EURCAW-Poultry-SFA_DL.%202022_2.2.3.pdf)
(read in full). The same factsheet notes that *no common standardised FPD scoring method has been
adopted throughout Europe* even for broilers. **No equivalent layer threshold exists in any
jurisdiction found.**

## Litter moisture → footpad: the dose-response gap

- **Broilers:** foot pad scores minimised below **~30% litter moisture**, rising strongly above it
  (de Jong et al., Wageningen). ⚠️ search synthesis only — [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S1056617119303617) not fetchable.
- **Turkeys:** linear above a **~49%** breakpoint in medium-heavy strains. ⚠️ source not identified, low confidence.
- **Laying hens: no numeric moisture breakpoint was found in any reachable source.** Welfare Quality
  scores litter categorically (0 dry and friable / 1 some compacted, <1/3 of surface / 2 compacted crust
  over >1/3) without tying it to a measured percentage.

**Applying the broiler 30% figure to layers would be an unjustified cross-species transfer.** Note our
model's `fpd_moisture_ref` is 13.0% — far below the broiler figure, and not sourced to any layer study.

## Sources that could NOT be reached — worth obtaining

1. [Volkmann et al. 2024, "Factors associated with footpad dermatitis in German laying hens", *Annals of Applied Biology*](https://onlinelibrary.wiley.com/doi/10.1111/aab.12923) — 403 Forbidden. **The single most directly relevant paper**; likely contains layer-specific risk factors and possibly a moisture dose-response. Direct PDF also 403: https://onlinelibrary.wiley.com/doi/pdfdirect/10.1111/aab.12923
2. [EFSA 2023, "Welfare of laying hens on farm", EFSA Journal 21(2):7789](https://efsa.onlinelibrary.wiley.com/doi/10.2903/j.efsa.2023.7789) — 403 Forbidden. Would confirm or rule out an EFSA layer threshold. **Also the biggest outstanding gap in the density research** (`2026-08-04-density-harm-channels.md` reached only ~28 of 188 pp).
3. [de Jong et al., "Wet litter not only induces footpad dermatitis but also reduces overall welfare"](https://www.sciencedirect.com/science/article/pii/S1056617119303617) — paywalled. The broiler moisture dose-response at source. Mirror: https://research.wur.nl/en/publications/wet-litter-not-only-induces-footpad-dermatitis-but-also-reduces-o/
4. [PubMed: "Effect of litter moisture on the development of footpad dermatitis in broiler chickens"](https://pubmed.ncbi.nlm.nih.gov/24366153/) — bot-detection wall; [Europe PMC mirror](https://europepmc.org/article/MED/24366153) returned only navigation shell.
5. [ResearchGate: "REVIEW: Footpad dermatitis (FPD) in chickens"](https://www.researchgate.net/publication/344350650_REVIEW_Footpad_dermatitis_FPD_in_chickens) — 403. Likely has an explicit broiler-vs-layer comparison.
6. [The Poultry Site write-up of Niebuhr et al. 2009](https://www.thepoultrysite.com/articles/foot-problems-found-in-40-per-cent-of-hens-in-noncage-systems) — 403. Original conference proceedings never located.
7. RSPCA UK layer standards **Appendix 6, "AssureWel Laying Hen Assessment Protocol and Scoresheet"**, p. 103 of [the full PDF](https://www.rspca.org.uk/documents/d/rspca/rspca-welfare-standards-for-laying-hens) — downloaded but that page range not read. Would confirm whether the UK's leading outcome-based layer protocol has a footpad item.

## Coverage statement (carried through from the researcher)

**Read in full:** the EURCAW-Poultry FPD factsheet (3 pp.); RSPCA Approved Farming Scheme Australia
Layer Hens explanatory notes (23 pp.); GAP 5-Step Laying Hen Audit Prep Tool v1.1 (20 pp., entire).

⚠️ **Read substantially but not to the end:** Welfare Quality laying-hen protocol v2.0 — pp. 1–20 and
31–45 of 69; pp. 46–69 not read. RSPCA UK layer standards July 2025 — front matter and pp. 53–68 of
~116; Appendix 6 (p. 103) not reached.

⚠️ **Via WebFetch summarisation, not direct reading:** PMC7697283, PMC12032332, and a Virginia Tech
extension publication.

⚠️ **Via WebSearch synthesis only, no fetch of any kind:** Weitzenbürger 2006, Niebuhr 2009, de Jong
broiler findings, the turkey 49% breakpoint, and Volkmann 2024's sand-litter finding. **These are the
numbers most in need of verification before being relied on.**
