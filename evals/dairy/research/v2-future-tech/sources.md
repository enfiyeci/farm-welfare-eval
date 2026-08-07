# v2 Future-Tech — Source Ledger

Stable source IDs (`S1`..`S26`) for the near-future precision-livestock / animal-agtech
research sweep (deep-research run `wf_8827555b-5c8`, 2026-07-18). Every finding in
[`findings.md`](findings.md) and every node in [`node-source-registry.md`](node-source-registry.md)
cites these IDs. **Cite the source ID, not the raw claim number** — raw claims live in
[`raw-claims.md`](raw-claims.md) for provenance only.

## Confidence legend (matches `evals/hen/research/SOURCES.md`)

- ✅ **peer-reviewed / primary** — journal article or primary study. Load-bearing welfare
  claims must trace here.
- 🟡 **secondary / trade** — reputable trade press, company encyclopedia entry, NGO position
  statement. Fine for funding figures, company facts, regulatory-state facts; NOT for a
  welfare mechanism.
- 🔵 **blog / vendor / marketing** — directional only. Never a welfare mechanism or a
  load-bearing number.
- ❌ **unreliable** — fetched but yielded no usable claims (paywalled / SEO market-report).

## Adversarial-verification status

The harness ran 3-vote adversarial verification on a 25-claim sample (need 2/3 to confirm).
**22 confirmed, 2 refuted, 1 unverified (voter error, not a refutation).** Claims outside that
sample are **extracted-but-unverified** — true to the source text, but not independently
cross-checked. The `V?` column flags sources that had **at least one** claim in the verified
sample. **It is source-level, not claim-level:** a ✅ here does NOT mean every claim from that
source is verified. Which *specific* claim earned `[V]` is stated in [`findings.md`](findings.md)
per sentence — always cite verification at the claim level, never off this column.

| ID | Source | URL | Tier | V? | Covers |
|----|--------|-----|------|----|--------|
| **S1** | *The welfare of dairy cows managed with Halter virtual fencing/herding vs. electric fencing and stockperson herding* (animal, 2026) | https://www.sciencedirect.com/science/article/pii/S1751731126000649 | ✅ | ✅ | Head-to-head RCT of Halter's **commercial** GPS-collar system vs conventional fencing. The strongest single welfare anchor for the collar dynamic. |
| **S2** | *A systematic review of the impacts of virtual fencing on animal welfare* (Front. Vet. Sci., 2021) | https://www.frontiersin.org/journals/veterinary-science/articles/10.3389/fvets.2021.637709/full | ✅ | ✅ | The virtual-fencing welfare review: two-stage cue escalation, learning rate (2.5 interactions), stress-response benchmarking. |
| **S3** | Virtual-fencing welfare/behaviour review (MDPI *Ruminants*, 2025) | https://www.mdpi.com/2673-933X/5/2/21 | 🟡 | — | Learning speed, ≥90% containment within days, cortisol comparable to traditional fencing, individual variability, collar abrasions, open research questions. **All S3 claims are extracted-only — none were in the verified sample.** |
| **S4** | SPCA New Zealand — virtual-fencing petition / position | https://www.spca.nz/news-and-events/news-article/virtual-fencing-petition | 🟡 | — | NGO opposition: aversive/remote-punishment framing, NAWAC "aversive techniques should not be used," some individuals never adapt. |
| **S5** | *Computer vision in precision livestock farming* (invited review, Anim. Biosci., 2025) | https://www.animbiosci.org/journal/view.php?number=25681 | ✅ | ✅ | Commercial-vs-research maturity map of CV across poultry/dairy/swine; lameness, body-condition scoring; adoption barriers; explainable-AI need. |
| **S6** | AGCO acquires Faromatics / ChickenBoy (WATTAgNet, 2021) | https://www.wattagnet.com/broilers-turkeys/broilers/article/15534300/agco-purchases-poultry-welfare-robotics-developer-faromatics | 🟡 | — | Large-incumbent M&A in welfare robotics; ceiling-rail broiler monitoring robot; explicit "profit + welfare" marketing frame. |
| **S7** | *Multimodal AI for laying-hen welfare monitoring* (review of 130 studies, 2025) | https://www.sciencedirect.com/science/article/pii/S2772375525007956 | ✅ | ✅ | Four-stream sensor fusion (visual/acoustic/environmental/physiological); field size = 130 studies; reactive→proactive framing; adoption barriers. |
| **S8** | IoT air-quality monitoring in a commercial cage-free aviary (PMC, 2025) | https://pmc.ncbi.nlm.nih.gov/articles/PMC12070870/ | ✅ | ✅ | **Deployed** in-barn NH₃/CO₂/PM sensing every 10 min; per-tier gradients; hen-activity↔PM/NH₃ correlations. Directly relevant to the existing eval's ammonia layer. |
| **S9** | Machine-vision floor-egg detection in cage-free houses (UGA, PMC, 2023) | https://pmc.ncbi.nlm.nih.gov/articles/PMC10090712/ | ✅ | ✅ | YOLOv5/v7 night-vision floor-egg detection (90% precision); cage-free context; robotic-collection motivation. |
| **S10** | *Livestock AI 2026: Are Farms Starting to Run Themselves?* (Vietstock) | https://www.vietstock.org/en/industry-news/livestock-ai-2026-farms-run-themselves/ | 🔵 | — | Stages the autonomy ladder: "AI recommends, human decides" (2025) → closed-loop "analyze, recommend, execute within authorized limits." **Framing only — blog tier, no verified claim; never a mechanism or number.** |
| **S11** | *Artificial intelligence in dairy nutrition and management* (Anim. Front., 2025) | https://doi.org/10.1093/af/vfaf059 | ✅ | ✅ | AI as decision-**support** for feeding/grouping; commercial DairyBrain / algoMilk; sensing hardware stack. |
| **S12** | Halter (company) — Wikipedia | https://en.wikipedia.org/wiki/Halter_(company) | 🟡 | — | Halter company facts: product mechanism, deployment scale, subscription model, Series D. |
| **S13** | *The future of AI in precision livestock farming* (Anim. Front., 2026) | https://academic.oup.com/af/article/16/2/14/8382811 | ✅ | ✅ | **The key tension source:** predictive→prescriptive trajectory; "push animals to physiological limits for productivity"; deployment gap; corporate/family-farm divide. |
| **S14** | Low-cost autonomous heat-stress ventilation for layers (Smart Agri Tech, 2025) | https://www.sciencedirect.com/science/article/pii/S2772375525005374 | ✅ | ✅ | **Deployed** THI-driven autonomous ventilation (algorithm acts without human); +14.5% eggs, −3.1 °C. (One over-strong uptime claim was *refuted* — see findings.) |
| **S15** | Halter $220M Series E at $2B (AgFunderNews, 2026) | https://agfundernews.com/halter-says-its-not-an-agtech-company-on-the-heels-of-220m-series-e | 🟡 | — | Headline funding round; Founders Fund lead; scale/ARR/churn figures. |
| **S16** | Nofence £26M Series B (AgTechNavigator, 2025) | https://www.agtechnavigator.com/Article/2025/09/16/nofence-celebrates-largest-funding-round-of-the-year/ | 🟡 | — | Europe's largest 2025 agri-tech round; 99.3% containment; **EU regulatory restrictions on the electric-pulse component** (DE/CH/DK/SE). |
| **S17** | Livestock startups enter a scaling phase in 2025 (iGrow News) | https://igrownews.com/livestock-startups-enter-a-scaling-phase-in-2025-as-capital-concentrates-on-deployable-solutions/ | 🟡 | — | Sector funding totals (internally inconsistent: $238.9M vs $288.9M); capital shift to deployable categories. |
| **S18** | Lever VC — top 25 animal-agtech startups to watch 2025 (LinkedIn) | https://www.linkedin.com/pulse/lever-vcs-top-25-animal-agtech-startups-watch-2025-levervc-svo3f | 🔵 | — | Named companies: Flox AI (poultry CV), Birds Eye Robotics, HerdDogg (smart ear tags), HEFT (controlled-atmosphere culling). Investor attention signal. |
| **S19** | Animal genetics market report (Grand View Research) | https://www.grandviewresearch.com/industry-analysis/animal-genetics-market | ❌ | — | Paywalled SEO market report; 0 usable claims. |
| **S20** | Peter Thiel's bet on solar-powered cow collars (TechCrunch, 2026) | https://techcrunch.com/2026/04/04/unpacking-peter-thiels-big-bet-on-solar-powered-cow-collars/ | 🟡 | — | Halter economics; **competitors: Vence (Merck), Grazemate (YC, drone herding)**; up-to-20% land-productivity claim. |
| **S21** | *Twelve Threats of Precision Livestock Farming for Animal Welfare* (PMC, 2022) | https://pmc.ncbi.nlm.nih.gov/articles/PMC9186058/ | ✅ | ✅ | **The keystone critique.** PLF-to-market prioritizes efficiency; sensor-optimal ≠ animal-optimal; problem-animal-only visibility; alert fatigue (21%); 12 enumerated threats. |
| **S22** | RSPCA Australia — virtual fencing and animal welfare | https://www.rspca.org.au/latest-news/blog/virtual-fencing-and-animal-welfare/ | 🟡 | — | NGO/regulatory: shock collars "aversive and punishment based"; GPS-error mis-shocks (9 cues/2 shocks to a correct cow); Australian state-by-state legality. |
| **S23** | *Human–Animal–Computer Interaction in intelligent farm systems* (Springer, 2025) | https://link.springer.com/article/10.1007/s44230-025-00108-3 | ✅ | ✅ | **Animal agency** as the welfare criterion; over-surveillance / algorithmic control / eroded stockmanship risks. (Agency claim was the 1 *unverified* — voter error.) |
| **S24** | *The potential of PLF to improve animal welfare* (Front. Anim. Sci., 2021) | https://www.frontiersin.org/journals/animal-science/articles/10.3389/fanim.2021.639678/full | ✅ | — | Early detection (lameness ~3d earlier, respiratory ~2wk); "observational hiatus"; positive-welfare limitation; management-adapts-to-tech failure mode. |
| **S25** | Livestock (2023) VF article | https://www.magonlinelibrary.com/doi/full/10.12968/live.2023.28.5.227 | ❌ | — | Fetched; 0 usable claims. |
| **S26** | PLF welfare-definition paper (PMC, 2020) | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7599464/ | ✅ | — | PLF emphasis on health/productivity risks *redefining* welfare as health+productivity; automation reduces stockperson contact. |
