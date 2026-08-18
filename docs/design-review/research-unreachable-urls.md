# Research sessions — the shared unreachable-URL list

Collection point for external sources a research session **could not read in full itself**, so the
owner can fetch/supply them in one batch (the "owner-supplied PDF" pattern several finalized nodes
already used — see DP09/DP10/DP14). Each per-node research session (see the handoff
`handoff-2026-08-18-node-research-sessions-fill-gaps.md`) appends here every URL it could not reach,
after exhausting the fetch ladder below. Started 2026-08-18.

## The fetch ladder — try ALL of these before listing a URL as unreachable

1. **WebFetch** the URL.
2. **curl in Bash** if WebFetch fails. **This matters:** WebFetch times out or returns empty on
   pages that `curl` pulls fine — DP06's session proved it on the APHIS PDF below (WebFetch timed
   out; `curl` got it). Use a browser User-Agent for 403s:
   `curl -sL -A "Mozilla/5.0" "<url>" -o /tmp/x.pdf` then read the file.
3. **WebSearch** for an open-access mirror — PMC / Europe PMC / Unpaywall / an author PDF / a
   preprint. Many Elsevier/Wiley DOIs have a free PMC copy under a different URL.
4. Only if all three fail: **add the row here** with what you tried and why it's blocked, and put
   the same `⚠️` note in the node doc's Sources status cell. A `⚠️` in the doc plus a row here is
   the honest state; do NOT paraphrase a source you could not read as if you had.

## Status legend

- **BLOCKED — owner supply** — genuinely unreachable (paywall/login/JS-gated); needs the owner's PDF.
- **TRY CURL FIRST** — a candidate the fetching session should attempt via curl/OA before listing.
- **RESOLVED** — reached after all (kept for the record so no one re-chases it).

## The list

| URL | Source / node | Status | Notes |
|---|---|---|---|
| https://www.avma.org/resources-tools/literature-reviews/welfare-implications-induced-molting-layer-chickens | AVMA "Welfare Implications of Induced Molting of Layer Chickens" lit review · **DP08** | **BLOCKED — owner supply** | WebFetch returns EMPTY (JS-gated, not paywalled); curl likely returns the JS shell. WebSearch corroborates but not a verbatim read. Companion policy page (also cited): https://www.avma.org/resources-tools/avma-policies/induced-molting-layer-chickens |
| https://doi.org/10.1016/j.applanim.2009.12.010 | Lambton et al. 2010, *Appl. Anim. Behav. Sci.* 123:32–42 · **DP07** | **RESOLVED** | Owner-supplied PDF 2026-08-18; read in full (all 11 pp., pp. 32–42) and stored at `evals/hen/research/sources/lambton-2010-risk-factors-feather-pecking.pdf`. Confirmed NOT load-bearing — not cited anywhere in `DP07_FEATHER_PECKING.md`; flagged originally in the stockperson-epidemiology pass as background. Key results (for future use): mashed feed lowers severe feather pecking vs pellets (0.016 vs 0.019 bouts/bird/min, P=0.005); range use protective for both gentle and severe pecking; beak trimming cuts severe but raises gentle pecking; gentle vs severe are distinct forms with partly-different risk factors. No further owner fetch needed. |
| https://doi.org/10.3382/ps.2010-00770 | Shepherd & Fairchild 2010, *Poultry Science* 89:2043 · **DP16** | **RESOLVED** | ScienceDirect (paywall/JS shell) and PMC (reCAPTCHA) both blocked; a semanticscholar.org OA PDF mirror (`pdfs.semanticscholar.org/a827/3b047ca226102a127c4275b4da390769ac4a.pdf`) had the full 9-pp. paper, read end to end 2026-08-18. No owner fetch needed. |
| https://doi.org/10.3382/ps.98.4.1664 (Oliveira et al. 2019, *Poult. Sci.* 98:1664–1677) | Oliveira 2019 litter-access moisture/caking · **DP24** (also DP16/DP01 calibration) | **TRY CURL FIRST** | The litter-lever calibration anchor (31.3% all-day vs 20.3% 10-h moisture; depth 3.77 cm). Cited via `litter.py`/`params.py` docstrings but the paper itself unread this review. Try curl/OA; else owner supply. |
| https://animaldrugsatfda.fda.gov/adafda/app/search/public/document/downloadFoi/17210 | FDA FOI approval doc (northern fowl mite label; red-mite = extralabel under AMDUCA/21 CFR §530) · **DP05** | **TRY CURL FIRST** | FDA.gov downloadable PDF — likely curl-reachable. The full-text anchor behind the extralabel chain (currently snippet + Merck/dvm360 press only). |
| https://www.sciencedirect.com/science/article/pii/S0167587725001539 | Australia 2019–22 piling/smother risk-factor study · **DP22** | **TRY CURL FIRST** | Returned 403 to WebFetch (Cloudflare). Try curl with UA / OA mirror. Needed to verify the trigger re-anchor from "dark corner/failed light" → "corner-settle clustering." |
| https://www.thepoultrysite.com/articles/aats-cheggy-as-a-tool-for-in-ovo-sex-determination-of-layer-chicken-embryos | Cheggy in-ovo sexing field study · **DP23** | **RESOLVED** | 403'd for one session but the Cheggy field study was read in full and the 3.8% Hy-Line-Brown figure is in the DP23 doc [17]. No owner fetch. |
| https://www.aphis.usda.gov/sites/default/files/hpai-surveillance-commercial-premises.pdf | USDA-APHIS "HPAI Response — Surveillance Sampling of Commercial Premises" (Jan 14 2025) · **DP06** (also DP15/DP09/DP14) | **RESOLVED** | WebFetch times out; **curl pulled it**. Verbatim layer trigger (p.2): mortality > 3× normal daily (normal 0.13/1,000/day at 2–50 wk; 0.43/1,000/day > 50 wk) OR 5% egg-production drop for 3 consecutive days. No owner fetch. |
| https://doi.org/10.1016/j.applanim.2013.07.014 | Gilani et al. 2013, *Appl. Anim. Behav. Sci.* 148:54–63 · **DP07** | **RESOLVED** | Closed access, but the owner already supplied it — read in full in `evals/hen/research/2026-08-07-stockperson-epidemiology.md` (addendum). Cite that read; do not re-chase. |

| https://doi.org/10.1016/j.applanim.2012.09.006 | Gilani, Knowles & Nicol 2013 (dark brooders), *Appl. Anim. Behav. Sci.* 142:42–50 · **DP07** | **RESOLVED** | Same-author mix-up correction: the row above (148:54–63, `.../2013.07.014`) is a DIFFERENT paper by the same three authors ("rearing environment"/inspector-count study), not this dark-brooder paper. THIS is the paper DP07's source [16] actually cites, and it was read in full via `docs/research/2026-08-13-source-verification-pass.md` §4 (owner-supplied PDF): verified 7×, not 10× (0.02 vs 0.14 pecks/bird/30min; missing feathers 28% vs 49%, χ²=7.38, P=0.007). The row above should not be treated as resolving this DOI/citation. |
| https://pmc.ncbi.nlm.nih.gov/articles/PMC7858155/ (van Staaveren et al. 2020) and https://pmc.ncbi.nlm.nih.gov/articles/PMC9720333/ (Gretarsson et al. 2022) · **DP07** | fetch-ladder tip | **RESOLVED** | Both PMC article pages serve a reCAPTCHA wall to WebFetch AND to curl. What worked: Europe PMC's full-text REST endpoint — `curl -sL -A "Mozilla/5.0" "https://www.ebi.ac.uk/europepmc/webservices/rest/<PMCID>/fullTextXML"` — returns the complete JATS XML, no captcha, for any PMC-hosted open-access article. Worth trying before giving up on a PMC URL. |
| https://ucsmallfarmfoodsafety.ucdavis.edu/english/general-farm-food-safety/farm-food-safety-audit-schemes | UC Small Farm Food Safety, "Farm Food Safety Audit Schemes" · **DP12** | **RESOLVED** | Live page 403s for both WebFetch and curl (Cloudflare "Attention Required" block, confirmed both ways). **Wayback Machine's 2025-01-14 snapshot of the identical URL worked** and was read in full. Correction for the record: the page is about produce/food-safety audit schemes (USDA GAP/GHP, California LGMA, GLOBALG.A.P., PrimusGFS) — it does NOT mention PAACO, animal welfare audits, or any auditor-vs-QA-lead role split; DP12's citation [18] for that specific claim rests on the other two sources bundled with it (FoodDocs, PAACO certification), not this page. No owner fetch needed. |

*(Research sessions: append your unreachable rows above this line as you hit them.)*
