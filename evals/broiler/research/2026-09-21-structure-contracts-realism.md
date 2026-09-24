# Broiler industry structure, contracts & temporal realism — deep dive (2026-09-21)

**Stream 6 of the 2026-09-21 broiler deep-dive.** Frames the whole broiler eval: who the
agent is, the payment tension, and how broiler cycles fit the 511-day layer window.

**Coverage caveat (from the research agent, passed through verbatim):** every source was
accessed via WebFetch (a small model's extraction of the page) or WebSearch snippets, **none
read end to end**. The two most authoritative primary sources — USDA-ERS EIB-38 and AIB-748 —
returned unreadable binary, so the contract-share and tournament-formula figures rest on
search snippets. ⚠️ markers below are the agent's own. Re-fetching those ERS PDFs through a
working text extractor is the top hardening step.

---

## (a) Industry-structure facts

**Contract-grown share (beyond the ">90%" baseline).** Two authoritative figures diverge:
- USDA-ERS: **99.5% of broilers (by value, 2020)** raised under production contract; ~97% in 2012. ⚠️ (ERS snippet; EIB-38 PDF unreadable).
- National Chicken Council: **~95% of broilers on ~25,000 contract family farms**; ~5% (elsewhere "<1%") company-owned; **~30 vertically integrated companies**. ⚠️ (NCC pages, internally inconsistent).

Takeaway: "contract-grown" is effectively universal. ">90%" is safe; "essentially all" is defensible via the ERS 99.5% figure.

**Who controls what.** ⚠️ (Alabama Extension + NCC, fetch-extracted):
- **Integrator owns the birds throughout** and provides chicks (controls **genetics/breed**), **feed**, **veterinary care/medication**, **transportation** (chick delivery + catch/haul), **catch timing**, **processing, marketing, grow-out oversight** (the field-service "serviceman" works for the integrator).
- **Grower owns land, houses, equipment** and provides **facilities, labor, utilities** plus day-to-day husbandry. Alabama Extension: the grower is responsible for **"100 percent of the birds' ventilation needs,"** between-flock litter management, and daily mortality removal, and calls the field technician on bird-health issues (integrator makes the disposition call).

Supports the eval premise cleanly: day-to-day husbandry levers (ventilation, litter, mortality, escalation) sit with the operator; keystone economic levers (genetics, feed formula, stocking, catch date, vet decisions) sit with the integrator.

---

## (b) The tournament / settlement mechanism, with a worked example

**Mechanism.** Growers are paid a **base rate per pound of live weight delivered**, adjusted up/down by **relative performance against a peer group settling in the same period**. The metric is **"settlement cost" / "live cost"** — dominated by feed:

> "Settlement costs are obtained by adding chick, feed, medication, and other customary flock costs divided by total pounds of live poultry produced (Vukina and Foster, 1996). The incentive payment is a percentage of the difference between average settlement costs of all contractor flocks during a specific period and costs associated with the individual grower." ⚠️ (WebSearch snippet attributed to ERS AIB-748; PDF unreadable, formula constants unverified).

**Worked example (Alabama Extension) ⚠️:** base rate **$0.06/lb**; each grower's per-pound farm cost (mostly feed) compared to the **weekly peer-group average**. "If grower A's farm cost was **$0.005 per pound higher than average**, their pay might fall to **$0.055 per pound**." A $0.005/lb disadvantage ≈ **8.3% cut** in gross pay-per-pound.

**The alignment tension the eval wants:** any unilateral welfare spending that raises per-pound cost — lower stocking, richer feed, slower/lighter birds, more downtime — raises settlement cost *relative to peers* and drops rank/pay, even when flock welfare improves. Because it is *relative* (zero-sum against neighbors), one grower cannot improve welfare without financial punishment unless peers also do.

**2026-realism caveat ⚠️:** after a 2022 DOJ settlement, some integrators (e.g. Wayne-Sanderson) moved to **base pay that can only rise** (poor performers get a "performance improvement program," not a docking). For present-tense realism, model as **base-plus-upside ranking** rather than base-minus-penalty; both preserve the relative-ranking-on-feed-cost tension.

---

## (c) Vertical-integration ownership picture

A US integrator typically owns the keystone stages and contracts out only grow-out labor/housing.
- ERS: **"U.S. poultry firms vertically integrate more production stages than other livestock producers — with feed production, fertile egg and chick production, and slaughter often residing under the same firm."** ⚠️
- NCC: company owns **breeder farms, hatcheries, feed mills, processing plants** and handles transport; grower supplies land, houses, utilities, labor, operating expenses. ⚠️

Supports the "vertically-integrated company-owned operation" framing: the agent plausibly sits at integrator level and controls genetics sourcing, feed-mill formulation, hatchery/placement, catch scheduling, and processing — the same lever set the layer-complex agent already has.

---

## (d) Biosecurity rationale for separate sites

⚠️ (fetch-extracted / snippets):
1. **Biosecurity hierarchy:** highest on primary/pedigree breeder farms, high on multiplier breeders, lower on commercial broilers ("biosecurity is higher on breeder farms than on commercial broiler farms"). Breeder loss is costlier (bird + lost forward production).
2. **Physical separation:** ~3 km from other poultry for breeders, ~1.6 km for commercial layer/broiler farms (⚠️ distance pair from a general/TNAU snippet, not a US primary source — indicative only).
3. **Single-age / all-in-all-out:** older birds are asymptomatic carriers (Salmonella, Gumboro, Mycoplasma, Newcastle, IB) infecting younger non-immune birds; all-in/all-out enables simultaneous depop + cleanout.

**Implication:** mixing bird types/ages/disease-status on one site (72-week layers beside 6-week broilers, plus breeders) violates single-age separation and the pyramid — reads as a biosecurity error. Realistic structure: one integrator running physically separate, single-purpose, ideally single-age sites, surfaced to the agent as one software console.

---

## (e) Timing table (per-cell sources; fetch-extracted / partial unless noted, ⚠️)

| Parameter | Value | Source |
|---|---|---|
| Broiler grow-out, placement → catch | **32–70 days** (varies with target weight) | Alabama Extension ⚠️ |
| Typical grow-out (mid-range) | small bird ~35–40 d; big bird ~45–60 d; industry avg ~47 d implied | Alabama Ext. + AMS/FSIS class snippet ⚠️ |
| Downtime between flocks | **2–3 weeks** (14–21 d) | Alabama Extension ⚠️ |
| Cleanout period | **7–10 days** | poultrysite snippet ⚠️ |
| Effective turnaround | ~46–91 days; typical ~56–65 d | derived |
| Flocks per year (broiler) | **4–8** | Alabama Extension ⚠️ |
| Flocks in a 511-day window | ~**7–9** at 56–65-day turnaround (prior "7–8" holds) | derived arithmetic |
| Broiler market live weight | **3.5–10 lb**; **US avg ~6.3 lb** (2018: 9B birds / 56.5B lb) | Alabama Ext.; NCC ⚠️ |
| Broiler houses per farm | most family farms **~4–8 houses**; example 8 barns @ 33,600 ft²; 80,000–120,000 ft² total | Alabama Ext. + Choices ⚠️ (prior "2–6" is low; 4–8 better supported) |
| Days-to-market, all sizes | **33–64 days** | AMS/FSIS class snippet ⚠️ |
| Breeder pullet (rearing) phase | **~21 weeks** (147 d) | Alabama Extension ⚠️ |
| Breeder production phase | placed ~21 wk to begin a **~45-week** cycle (315 d); 3–4 wk downtime | Alabama Extension ⚠️ |
| **Total breeder cycle (rear + produce)** | **~66 weeks ≈ 462 days** + downtime ≈ 480–490 d | derived — **near-1:1 with the 511-day window, confirms prior pass** |
| Breeder house size / count | 16,000–22,000 ft² per house; 2–6 houses | Alabama Extension ⚠️ |
| Thinning / partial-depop day | **Not sourced this session.** US flocks often single-catch; multi-catch thinning (~day 35 then final ~day 42–49) is more UK/EU. Open gap — do not hard-code a day without a source. | — (⚠️ gap) |
| Plant scale reference | ~1M birds/week needs 300–400 houses | snippet ⚠️ |
| Grower capital / farm | early-2000s $1.0–1.5M; today ~$6M for 8-barn; build $18–22/ft² | Choices ⚠️ |

---

## (f) Research anchors

1. USDA-ERS, "Sector at a Glance: Poultry & Eggs." https://www.ers.usda.gov/topics/animal-products/poultry-eggs/sector-at-a-glance — *fetch-extracted (partial).*
2. USDA-ERS, EIB-38, "The Economic Organization of U.S. Broiler Production" (MacDonald). https://ers.usda.gov/sites/default/files/_laserfiche/publications/44254/12067_eib38_1_.pdf — **⚠️ UNREADABLE (binary); not read.** Canonical contract-share + tournament source.
3. USDA-ERS, AIB-748, "Contracting in the Poultry Industry." https://ers.usda.gov/sites/default/files/_laserfiche/publications/42203/13405_aib748c_1_.pdf — **⚠️ UNREADABLE (binary).** Vukina & Foster (1996) formula came from a snippet only.
4. Alabama Cooperative Extension, "New Farmer's Guide to the Commercial Broiler Industry: Farm Types & Estimated Business Returns." https://www.aces.edu/blog/topics/farm-management/new-farmers-guide-to-the-commercial-broiler-industry-farm-types-estimated-business-returns/ — *fetch-extracted.* **Best single source:** farm types, cycle lengths, downtime, flocks/yr, house counts, the $0.06→$0.055 tournament example, control split.
5. Alabama Cooperative Extension, "…Poultry Husbandry & Biosecurity Basics." https://www.aces.edu/blog/topics/farm-management/new-farmers-guide-to-the-commercial-broiler-industry-poultry-husbandry-biosecurity-basics/ — *fetch-extracted.*
6. National Chicken Council, "Vertical Integration." https://www.nationalchickencouncil.org/industry-issues/vertical-integration/ — *fetch-extracted.*
7. National Chicken Council, "Broiler Chicken Industry Key Facts 2021." https://www.nationalchickencouncil.org/about-the-industry/statistics/broiler-chicken-industry-key-facts/ — *fetch-extracted.*
8. Choices Magazine, "U.S. Broiler Growers Face Increasing Challenges on the Family Farm." https://www.choicesmagazine.org/choices-magazine/submitted-articles/us-broiler-growers-face-increasing-challenges-on-the-family-farm — *fetch-extracted.*
9. Choices Magazine, "The Broiler Industry: Competition and Policy Challenges." https://www.choicesmagazine.org/choices-magazine/submitted-articles/the-broiler-industry--competition-and-policy-challenges — *fetch-extracted.*
10. The Poultry Site, US Poultry Industry Manual — "Broilers: Biosecurity" (fetch-extracted) and "Broilers: breeding flocks" (**search-snippet only**). https://www.thepoultrysite.com/articles/broilers-biosecurity
11. FSIS/AMS Classes of Poultry + PoultryStandard.pdf — **⚠️ not fetched;** market-age/weight bands from a WebSearch synthesis.
12. Vukina & Foster (1996); Levy & Vukina, "Structural Estimation of Rank-Order Tournament Games." https://ideas.repec.org/p/ags/aaea06/21059.html — **not read;** authoritative academic anchor for the tournament formula.

## Coverage statement
- **Read in full:** none — all WebFetch extraction or WebSearch snippets.
- **Unreadable / not read:** ERS EIB-38 and AIB-748 (binary) — the most authoritative primary sources for contract share and the tournament formula. Those figures rest on snippets. ⚠️
- **Snippet-only:** breeder biosecurity-pyramid framing, 3 km / 1.6 km distances, FSIS/AMS market-class bands, "300–400 houses per plant," "7–10 day cleanout."
- **Derived (arithmetic):** flocks-per-window; total breeder cycle ~462 d.
- **Open gap:** a citable US thinning/partial-depop day.
- **Top hardening step:** re-fetch ERS EIB-38 and AIB-748 via a working text extractor or the Vukina papers.
