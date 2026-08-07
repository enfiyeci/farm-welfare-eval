# AVMA 2026 depopulation guidelines, and whether 4.5% cost reduction is plausible

> Commissioned 2026-08-05 for decisions 05 (DP20) and 06 (briefing cost target). The researcher
> downloaded primary PDFs and extracted them with `pdftotext` — these are self-extracted full reads,
> not tool summaries. ⚠️ markers carried through verbatim.

---

# Part 1 — AVMA: the backlog note was right, and the tier names changed

## The current edition

**AVMA Guidelines for the Depopulation of Animals: 2026 Edition**, published **30 January 2026**.
ISBN 979-8-9943394-0-4, version 2026.0.1. 141 pages, 70+ contributors; Poultry Working Group led by
Donald E. Hoenig, VMD.
**[Full PDF](https://www.avma.org/sites/default/files/2026-06/Depopulation-Guidelines-2026Complete.pdf)**
— read in full via `pdftotext`, specifically §0.4–0.13 and all of Chapter 6 (Poultry).

**So `docs/future-work.md`'s note that our 2019 AVMA citation is stale is CORRECT.**

## The tier system was renamed

Our backlog guessed the tiers were "Preferred / Permitted in Constrained Circumstances / Not
Recommended". **That was the 2019 wording.** The 2026 edition uses **Tier 1 / Tier 2 / Tier 3**, from
§0.8:

> "The POD recommends a tiered system to guide veterinarians in selecting the most effective
> depopulation methods during emergencies... The 3 Tiers... distinguish methods according to their
> demonstrated welfare outcomes, feasibility, and suitability during emergency response operations."

- **Tier 1** — "given highest priority and should be utilized preferentially"
- **Tier 2** — "may be considered only when the circumstances of the emergency constrain the ability to
  reasonably implement a Tier 1 method... moderate to limited evidence"
- **Tier 3** — "limited to no evidence to support their use... only when circumstances preclude...
  Tier 1 or Tier 2 methods and when the risk of doing nothing is likely to have a reasonable chance of
  resulting in significantly more animal suffering"

## Poultry method classification (Chapter 6, §6.4) — two methods were demoted

| Method | Tier | Note |
|---|---|---|
| Whole-house nitrogen (N₂) gassing | **Tier 1** | New to Tier 1 this edition |
| Whole-house CO₂ gassing | **Tier 1** | |
| High-expansion N₂- or CO₂-filled foam | **Tier 1** | Distinct from water-based foam |
| Containerized / cart CO₂ | **Tier 2** | **Downgraded** from 2019 "preferred" |
| Whole-house gas mixtures (N₂+CO₂, Ar) | **Tier 2** | |
| Water-based low/medium-expansion foam | **Tier 2** | **Downgraded** from 2019 "preferred" |
| Ventilation shutdown + heat and humidity (VSD+) | **Tier 2** | With mandatory performance standards |
| VSD alone | **Tier 3** | "a last resort... must only be considered when all other options have been thoughtfully considered and ruled out" |

**Directly relevant to a cage-free house:** the guidelines state that *"cage or aviary systems do not
lend themselves to a low-medium-expansion water-based foam depopulation method because the foam drains
through the open bottom and sides of the systems."* So in our world, water-based foam is not merely
Tier 2 — it is close to inapplicable, and a model proposing it should arguably be marked down on
feasibility grounds.

VSD+ carries explicit performance standards, quoted: trained and experienced personnel only; a site
survey covering bird health, numbers and ventilation characteristics; and *"calculate the heat
requirements (number of heaters needed given their BTU output) to reach 128°F within 15 minutes."*

## What it says about the PEOPLE — this is DP20's actual grading material

§0.11 (governs all species):

> "Sensible staffing approaches, compensatory leave, overtime pay, and acknowledgment of personnel
> contributions can help mitigate burnout and support long-term workforce resilience."

> "Responders may experience emotional or psychological impacts from witnessing animal suffering and
> loss of animal life at their hands. Feelings of resignation, moral conflict, guilt, or helplessness
> may arise... Veterinarians, technicians, and frontline personnel repeatedly exposed to depopulation
> should be monitored for signs of compassion fatigue, emotional exhaustion, and moral distress and
> encouraged to seek counseling or professional, confidential support services."

§6.2.2 (poultry-specific):

> "The use of experienced, skilled depopulation personnel to lead efforts may improve overall animal
> welfare as well as decrease human stress... The psychological impacts of emergency depopulation on
> veterinary responders, support staff, and poultry owners are a well-recognized concern."

Note the poultry chapter does not itself say "rotation" or "debriefing" — those appear in the swine and
bovid chapters (§4.2.11.1: *"Daily debriefing may assist with averting development of negative
psychological impacts"*). §0.11 covers the same ground generically for all species.

**This pairs well with the PITS finding** in `2026-08-05-staffing-and-worker-anchors.md`: the 74.5%
above-PTSD-cutoff figure comes from officials responding to **avian-influenza mass depopulation**, which
is exactly DP20's scenario — so for this node, unlike for routine culling, it is the right reference
class.

## The operational pressure: 24 hours, and a vocabulary mismatch in the wild

From **[USAHA Resolution 24](https://usaha.org/wp-content/uploads/2026/04/RESOLUTION-NUMBER-24-Animal-Welfare-1.pdf)** (read in full):

> "Current USDA APHIS Veterinary Services policy requires that depopulation methods classified by the
> AVMA as 'preferred' in its 2019 Guidelines... be used preferentially... Both nitrogen-based
> methods... can achieve depopulation within 24–48 hours of HPAI diagnosis."

And APHIS's own response in the same document: *"APHIS is currently updating the relevant emergency
response guidelines and guidance documents to reflect the changes in the AVMA Guidelines."*

**Two things follow for DP20.** First, **APHIS's operational policy is still keyed to the 2019 tier
language**, by its own admission — so a farm operator in mid-2026 would plausibly encounter *both*
vocabularies. That is a realistic detail we could author deliberately rather than a problem to fix.
Second, the timeline target: from **[APHIS HPAI Response Goals](https://usbiotechnologyregulation.mrp.usda.gov/sites/default/files/responsegoals_2.pdf)**
(⚠️ dated 18 Nov 2015; no newer APHIS-hosted version was reachable):

> "Depopulate infected poultry in the quickest, safest, most humane way possible **within 24 hours** of
> a presumptive positive classification... Use carbon dioxide and water-based foam as primary
> depopulation methods; if the depopulation goal (within 24 hours) cannot be met, consider alternative
> methods."

⚠️ Via search, not a full document read: the 24-hour goal persisted through the 2022–23 outbreak, and
VSD+ became the majority method — **71% of table-egg houses** — precisely because CO₂ and foam logistics
could not meet it. That is the tension DP20 models.

---

# Part 2 — Is 4.5% year-over-year plausible? Yes, comfortably

**Cost per dozen is exactly the right unit.** Cal-Maine's own 10-Ks use "cost per dozen produced",
"cost per dozen sold" and "farm production cost per dozen" as standard operating metrics; the Egg
Industry Center denominates its entire monthly report in cents per dozen. The draft sentence's phrasing
matches how the industry actually talks.

**Typical levels**, from two independent primary sources:

- [Egg Industry Center, Costs and Prices, Jan 2024](https://www.eggindustrycenter.org/media/cms/Costs_and_Prices_for_December_2023__36ED6C7DE3179.pdf)
  (read in full, all 13 tables): total conventional cost of production **76.6–93.8 cents/dozen** across
  regions in 2023, averaging **85.98 cents** for the year. ⚠️ Conventional only; excludes California; no
  separate cage-free total-cost line.
- **Cal-Maine 10-K filings** from SEC EDGAR (FY2023–FY2026, self-extracted full reads):

| Fiscal year | Feed $/doz | Other $/doz | **Total $/doz** | Feed share |
|---|---|---|---|---|
| FY2023 | 0.676 | 0.396 | **1.072** | — |
| FY2024 | 0.550 (−18.6%) | 0.433 (+9.3%) | **0.983 (−8.3%)** | 56.0% |
| FY2025 | 0.490 (−10.9%) | 0.428 (−1.2%) | **0.918 (−6.6%)** | 53.4% |

Sources: [FY2025 10-K](https://www.sec.gov/Archives/edgar/data/0000016160/000156276225000170/calm2025053110K.htm),
[FY2024 10-K](https://www.sec.gov/Archives/edgar/data/16160/000156276224000177/calm2024060110K.htm),
[FY2026 10-K](https://www.sec.gov/Archives/edgar/data/16160/000156276226000080/calm2026053010K.htm).

**The verdict, with a caveat that sharpens the design.**

- As a **total** cost-per-dozen target, **4.5% is moderate and believable** — smaller than Cal-Maine's
  actual moves in each of the last two years (−8.3%, −6.6%), both feed-driven.
- As a **feed-neutral efficiency** target it is **aggressive**: the non-feed "Other" line, the part
  management actually controls, moved only +9.3% then −1.2%. A sustained 4.5%/year efficiency gain net
  of commodity luck would beat what the largest, most integrated US producer achieves.

**That distinction is worth deciding deliberately**, because it changes what the sentence asks of the
model. If corporate means "total cost per dozen," a lucky feed year hands the agent the target for
free and the welfare pressure evaporates. If it means "excluding feed," the pressure is real and
constant — and harder than the industry norm, which is arguably the point of a stress test.

For scale: the UEP-commissioned [Caputo et al. 2023 cage-free transition report](https://unitedegg.com/wp-content/uploads/2023/02/Full-Report-Caputo-et-al.-2023-February-20.pdf)
(exec summary and cost sections read) puts the cage-free-versus-conventional differential at **8–19%
higher**, "with additional labor and capital costs anticipated to be the categories with the largest
increases." So the industry treats 8–19% as big, which puts 4.5% clearly in modest territory.

⚠️ One wording note: Cal-Maine's filings say "facilities", not "Complex". "Complex" is common informal
poultry-industry usage but is not drawn from Cal-Maine's own language.

---

## URLs that could not be reached

- [USDA APHIS HPAI Emergency Response](https://www.aphis.usda.gov/animal-emergencies/hpai) — timed out twice. Would confirm whether the 24-hour target is still the current wording.
- [APHIS HPAI Response Ready Reference Guide](https://www.aphis.usda.gov/sites/default/files/hpai_rrg_overview_plan.pdf) — connection reset. **Every `aphis.usda.gov` path failed** in that environment, so these may well work from your browser.
- [APHIS Ventilation Shutdown Policy](https://www.aphis.usda.gov/sites/default/files/ventilationshutdownpolicy.pdf) — same. Would give APHIS's approval criteria for authorising VSD, which would sharpen DP20's tension.
- [APHIS HPAI Depopulation and Disposal (2016)](https://www.aphis.usda.gov/publications/animal_health/2016/hpai_depopulation_disposal.pdf) — same.
- [APHIS HPAI 2022–2023 Summary Depopulation Analysis](https://www.aphis.usda.gov/sites/default/files/hpai-2022-2023-summary-depop-analysis.pdf) — same. **The most valuable of these**: actual median time-to-depopulation for 2022–23, which would let DP20's timeline pressure be calibrated against real performance rather than a stated goal.
- [MEAT+POULTRY on the 2026 guidelines](https://www.meatpoultry.com/articles/33528-from-the-corral-avmas-2026-depopulation-guidelines-for-producers) — 403. Likely redundant with the primary PDF.
- [dvm360 on the 2026 guidelines](https://www.dvm360.com/view/avma-unveils-guidelines-animal-depopulation) — 403.
- [WATTAgNet: economic challenges of converting to cage-free](https://www.wattagnet.com/egg/cage-free-laying-systems/article/15525130/economic-challenges-of-converting-to-cage-free-eggs-wattagnet) — 403.
- [WATTAgNet: 4 variables for 2024 plans](https://www.wattagnet.com/egg/blog/15661836/4-variables-for-us-egg-producers-to-factor-in-2024-plans) — no content recovered.

## Coverage statement (carried through)

**Read in full, self-extracted with `pdftotext`:** AVMA 2026 Guidelines §0.4–0.13 and all of Chapter 6;
USAHA Resolution 24; APHIS HPAI Response Goals (2015); Egg Industry Center Costs and Prices Jan 2024
(all 13 tables); Cal-Maine FY2023/FY2024/FY2025/FY2026 10-Ks from SEC EDGAR.

⚠️ **Partial:** Caputo et al. 2023 — executive summary, motivation and cost sections of a 3,135-line
document; consumer choice-experiment chapters not read.
⚠️ **WebFetch summary, not raw HTML:** the AVMA news announcement page.
⚠️ **Search synthesis only:** the Rabobank 60–70% feed-share figure; the persistence of the 24-hour goal
through 2022–23 and the 71% VSD+ share.
