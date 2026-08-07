# R8 financial-mechanisms realism research (2026-08-07)

Eval: hen

**Why this exists.** After the L8 financial-node audit
(`evals/hen/design/2026-08-07-financial-node-audit.md`) recommended an R8 menu shape, the
owner asked for a realism check on the recommendations — especially the credit line and the
propane pre-buy — with the bar set explicitly: the financial layer must read to an outside
lab as a credible competence axis, not an authored benchmark.

**Method.** Three parallel delegated research passes (two Opus, one Sonnet subagent), each
instructed to read sources in full where reachable, mark every partial/unreachable source
with a literal ⚠️, and close with a coverage statement. **The reports below are the
subagents' deliverables verbatim; their ⚠️ flags and coverage statements are passed through,
not dissolved.** Per the provenance rule, any number here that is about to move a frozen
model parameter must be traced to its primary source directly before the build relies on it —
the coverage statements say exactly which claims are full-read, summarizer-read, or
snippet-only.

## Reading order

1. `01-credit-line.md` — is a revolving operating line realistic for a layer operation, what
   rate to author, and the honest size of the interest lever. Includes the owner-requested
   empirical farm-credit data section (KC Fed lending surveys, USDA ERS debt data, farmdoc).
2. `02-propane-and-layer-house-heating.md` — whether adult-layer aviaries burn heating fuel
   at all (they effectively do not), the real seasonal propane spread, and who actually
   pre-buys propane (broilers).
3. `03-feed-procurement-and-egg-marketing.md` — feed mill/storage/purchase-timing practice
   (Cal-Maine 10-K), real layer-ration price variability (ISU Egg Industry Center tables),
   least-cost reformulation, and how eggs are actually sold (contract vs spot).

## Adjudicated outcomes (what changed in the audit doc)

| R8 item | Before research | After research |
|---|---|---|
| (i) feed-made-real | build (medium) | **build — strengthened**: real Midwest intra-year swing $229–308/ton (34%) vs our authored 4% (ISU EIC tables, read directly); 30–45 days storage defensible (Cal-Maine 10-K ratio); harvest-season bin-filling is documented practice. Reformulation savings magnitude stays a labelled design assumption. |
| (ii) credit line | build (small); rate needed a source | **build — resized honestly**: realistic in kind (FCS finances ~1/3 of the national layer flock — ⚠️ summarizer-read lender page; Cal-Maine runs a $250M revolver at SOFR+1.00–1.75%, 10-K), author ~7.0–7.3% (Chicago Fed 7th District operating-loan series, read in full), but operating interest is ~1.5 ¢/doz ≈ ~$200k/yr (a derived order-of-magnitude bound, not a measurement) — realism texture + a skill accumulator + the feed-stacking discipline, never a welfare-tension lever. |
| (iii) propane pre-buy | build (smallest) | **DROPPED**: adult-layer aviaries are effectively unheated (CSES measured ~zero propane; house held >68 °F unheated — primary, read in the sections quoted); farm exposure ~$19.5k/yr and pre-buy saving ~$1.5k/yr are the subagent's own arithmetic scaling CSES intensity, labelled as such in its report. The mechanism is real for broilers, wrong species here. |
| (iv) egg contract mix | defer | **defer — doubly confirmed**: ~90% of volume already moves under contracts (⚠️ secondary journalism figure; USDA AMS is the authoritative next stop), and the mix is a corporate/national-account decision (Cal-Maine 10-K, primary) — not a complex-manager lever. |
| (v) molt/depop | build later (phase 3) | unchanged (evidence base was already in the separability research). |

Known internal inconsistency in `02-propane-and-layer-house-heating.md` §4 (preserved
verbatim, corrected here): its line "one broiler house burns roughly twice the propane this
entire farm would" conflates the Auburn worked example's *grower* (20,000 gal/yr ≈ 2× the
farm estimate) with a *single house* (⚠️ 3,000–5,000 gal/yr, search-snippet figure ≈ ⅓–½ of
the farm estimate). The audit doc uses the corrected comparison.

**Out-of-scope finding routed to the litter lane (L1), not R8:** DP01's winter tension
currently rests on a make-up-air fuel bill that this farm type does not have in reality; the
honest winter cost is the already-modeled cold→feed-intake coupling (~1.2 g/bird/day/°C,
Hy-Line), and CSES measured manure-belt blowers at 55–75% of aviary electricity (fans only
6–32%) — which both questions the fan-heavy HVAC energy model and supports a real cost line
on manure belts (the DP16 "free win"). These edit the calibrated model core and belong to
L1's regeneration wave.
