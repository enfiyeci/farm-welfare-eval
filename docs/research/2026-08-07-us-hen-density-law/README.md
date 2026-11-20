# US laying-hen stocking density: what is actually law, and what is only certification

Eval: cross · Research pass 2026-08-07 · Requested by the owner after the Track D casebook
claimed "beyond standard" offers without a sourced standard.

## Why this exists

Track D's offers are labelled `StandardBand.BEYOND` in the code, and the casebook says the
final ladders sit far below any US cage-free standard. Both claims rested on an unsourced
144 sq in figure and on general knowledge about US law. This pass sources them.

**The short answer.** There is **no US federal limit** on how densely laying hens may be
housed on a conventional farm. The binding numbers come from (a) a private certification,
UEP Certified, which covers >90% of US egg production, and (b) about ten state laws, most of
which restrict *sale* of eggs in the state rather than production.

## 1. Federal law: essentially nothing

The federal Animal Welfare Act excludes farm animals used for food from its definition of
"animal" — livestock and poultry "used or intended for use as food or fiber" are outside the
Act entirely, so it cannot be invoked for on-farm density at all.

The one federal exception found: USDA's Organic Livestock and Poultry Standards final rule
(published 2023, in force 2024) does set poultry stocking densities — but only for
certified-organic operations, not conventional ones.

⚠️ **Coverage caveat.** Both statements above come from search-result summaries and
secondary sources (Congressional Research Service R47179, USDA National Agricultural Library,
advocacy explainers), **not** from reading 7 U.S.C. §2132 or 7 CFR Part 205 end to end. If
this is going into a document the model reads, read the primary text first.

## 2. UEP Certified cage-free — the number the industry actually runs on

Quoted verbatim from the **2024 Cage-Free Housing Animal Welfare Guidelines**, page 21,
"Guidelines for Indoor Floor Space" (the document states these space requirements are
unchanged from the 2017 edition, which is the edition the state laws cite):

> At placement, hens must be given a minimum of the following:
> - 1.0 square foot per hen in multi-tier housing
> - 1.0 square foot per hen in slatted floor housing
> - 1.5 square feet per hen in single-level all litter floor housing

So **144 sq in per hen for multi-tier / aviary housing** and **216 sq in for single-level
all-litter**. The repo's existing 144 sq in figure (`docs/research/2026-08-04-trackd-hen-rescue.md`)
is therefore **correct for the aviary case**, which is what the hen eval models.

Also from page 21, and relevant if we ever state space in a document:

> Usable floor space includes the combined litter and drop-through area, including elevated
> tiers and covers over belts, but excludes perch and nest space where the kick-out feature
> is being utilized. For equipment installed after December 31, 2025, the minimum nest space
> may not be included in the floor space calculation.

Enforcement teeth (pages 6–8): more than 90% of US eggs are produced under UEP Certified;
participants are audited annually by independent auditors (FACTA, USDA/AMS, Validus); a
participant needs 90% to pass, and **"failure to meet the space allowance guidelines… will be
cause for failure of the audit — regardless of the total points achieved."**

**A discrepancy this pass resolved:** a web search returned "116.3 square inches" as a UEP
cage-free figure. That is wrong. 116.3 sq in is the **American Humane Enriched Colony**
standard — a *caged* standard — which appears in Washington State's law for buildings built
after 1/1/12. It is not a cage-free number.

## 3. State law — mostly sales bans, a few production rules

From the **UEP State Hen Housing Summary** (both pages read in full). ⚠️ **This document is
dated 08/19/22 and is four years stale**; treat the dates as of-2022 and re-verify anything
load-bearing.

| State | Requirement | Compliance date |
|---|---|---|
| California | Cage-free + usable floor space of UEP 2017 cage-free | Current |
| Massachusetts | Cage-free; standards consistent with UEP Certified Cage-free | Current |
| Nevada | **144 sq in per hen**, then cage-free | 7/1/22, then 1/1/24 |
| Oregon | UEP Certified hen housing (pre-2012 enclosures); then cage-free + UEP 2017 | Current, then 1/1/24 |
| Washington | **116.3 sq in** (American Humane Enriched Colony, post-2012 buildings); then cage-free + UEP 2017 | Current, then 1/1/24 |
| Arizona | **1 sq ft** usable floor space; then cage-free + UEP 2017 | 1/1/23, then 1/1/25 |
| Colorado | **1 sq ft** usable floor space; then cage-free | 1/1/23, then 1/1/25 |
| Michigan | Cage-free + UEP 2017 usable floor space | 1/1/25 |
| Utah | Cage-free + UEP 2017 — **production only, does not address sales** | 1/1/25 |
| Rhode Island | UEP **2016** edition usable floor space — **production only, does not address sales** | 7/1/26 |
| Ohio | No new permits for conventional cages on new farms — **agreement expired 2020** | Expired |

The summary also notes Maine (12/31/2024) and Hawaii (12/31/2025) were pursuing legislation.

**The structural point for our purposes:** most of these are *sales* bans — they restrict
what may be sold in the state, not how a farm anywhere may house hens. Utah and Rhode Island
are the exceptions that regulate housing in-state and explicitly do not address sales. So a
producer's exposure depends on where it sells, which is a genuinely different (and more
interesting) constraint than "this is illegal".

⚠️ **2026 currency, from search summaries only — not verified against statute:** Michigan and
Utah took effect 1/1/25; Nevada's cage-free requirement took effect 1/1/24 and Nevada passed
2025 legislation permitting temporary suspension during avian-influenza supply shocks; some
states have reportedly moved to relax mandates during the bird-flu crisis. One conflict to
resolve: a secondary source puts Rhode Island at 1/1/26 while the UEP summary says 7/1/26.

## 4. What this means for Track D

Anchoring the Track D projection's index (current placement = 100) at the UEP multi-tier
minimum of 144 sq in, the final constant-cushion ladders imply:

| offer | index | implied space per hen |
|---|---|---|
| hen +9pp (smallest) | 138 | ~105 sq in |
| hen +30pp (top) | 291 | **~50 sq in** |
| shrimp +22pp (top) | 325 | ~44 sq in equivalent |

Every rung sits below the UEP cage-free minimum, and the top rungs sit below even the
conventional-cage allowance of 67–86 sq in per hen. **But the anchoring is an assumption:**
Track D's documents never state an absolute density, only an index, so nothing in the
materials establishes where the baseline sits.

**The gap this exposes.** Verified this session: the rendered Track D documents contain no
occurrence of "standard", "certification", "legal", "minimum", "regulat", "compliance", or
"sq in". The `StandardBand` within/beyond factor changes only which rung table is used —
not one word the model reads. **We have therefore never tested whether telling the model an
offer breaks a standard changes its behaviour**, despite building the factor for it.

## Sources

- [UEP 2024 Cage-Free Housing Animal Welfare Guidelines](https://uepcertified.com/wp-content/uploads/2024/10/2024-UEP-Revised-CF-Guidelines_Final.pdf) — ⚠️ read pages 1–8 and 21–22 in full (front matter, contents, compliance/auditing, Floor Space Per Hen, Feed and Water). **Not read:** pullet guidelines (18–20), perches, litter, nest space, environmental, molting, multi-tier systems (28).
- [UEP State Hen Housing Summary, updated 08/19/22](https://unitedegg.com/wp-content/uploads/2022/08/State-Hen-Housing-Summary-8-19-22.pdf) — **read in full** (both pages). Four years stale.
- [UEP Animal Husbandry Guidelines for U.S. Egg Laying Flocks (2017)](https://unitedegg.com/wp-content/uploads/2017/11/2017-UEP-Animal-Welfare-Complete-Guidelines-11.01.17-FINAL.pdf) — ⚠️ **not opened**; the 2024 document states it reprints its space requirements.
- [Congress.gov CRS R47179, The Animal Welfare Act](https://www.congress.gov/crs-product/R47179) — ⚠️ **not opened**; cited via search summary.
- [USDA Organic Livestock and Poultry Standards final rule](https://www.usda.gov/about-usda/news/press-releases/2023/10/25/usda-publishes-new-standards-organic-livestock-and-poultry-production-promotes-more-competitive) — ⚠️ **not opened**; cited via search summary.
- [ASPCA farm animal confinement bans by state](https://www.aspca.org/improving-laws-animals/public-policy/farm-animal-confinement-bans) and [The Humane League 2026 Eggsposé](https://thehumaneleague.org/article/2026-eggspose) — ⚠️ **not opened**; surfaced in search for the 2026 currency check.

## Coverage statement

Read end to end this session: the UEP State Hen Housing Summary (2 pages). Read in part with
the omissions named above: the UEP 2024 Cage-Free Guidelines. Everything about **federal law
and 2026 currency rests on search-result summaries, not primary sources** — the two claims
most worth hardening before any of this is put in front of a subject model.
