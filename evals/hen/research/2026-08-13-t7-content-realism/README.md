# T7 content-realism research (2026-08-13)

Web research to ground the **Task 7** finance-content authoring (five invoices, five offers, their
covering emails, and the schedule events) of the financial-skill axis
(`evals/hen/design/2026-08-07-financial-skill-axis-plan.md`, Task 7). Commissioned because the owner
chose to **steer the T7 content design before it is authored**, and asked for a deep sweep of how
real farm finances, dilemmas, vendor offers, and their language actually look.

## Reading order

1. **`SYNTHESIS-and-t7-steering.md`** — start here. The distilled findings + a concrete, model-grounded
   scenario slate for the five invoices and five offers, with offer paybacks **computed against the
   calibrated model**, plus the open steering decisions for the owner. **Cite this file, not the raw
   ones.**
2. Raw stream outputs (verbatim subagent returns, **UNVERIFIED**, kept for provenance):
   - `01-farm-cost-cashflow-RAW.md` — layer-farm cost structure, cash-flow dynamics, credit, dilemmas
   - `02-equipment-offer-paybacks-RAW.md` — LED / fan / audit offer economics and language
   - `03-feed-invoicing-terms-RAW.md` — trade-credit terms, feed-invoice anatomy, error taxonomy
   - `04-deceptive-offers-RAW.md` — scam-vs-marginal offer structure and language
   - `05-packaging-tiers-RAW.md` — egg-packaging costs and tiered pricing
   - `07-scam-specimens-RAW.md` — real scam email specimens & archetypes (follow-up pass; drove the
     final scam-email choice)
3. **`06-offer-email-drafts.md`** — the five offer covering-email drafts presented to the owner for
   the content decision (scam §4 = FINAL Candidate A, owner-chosen).

## Provenance & verification status

- Each raw file is one research subagent's (Opus) full return, retrieved 2026-08-13. They are
  **unverified at the primary-source level** — the orchestrator read each subagent's full return, not
  every underlying web page. The subagents' own **⚠️ coverage flags are preserved** inside each file;
  notable gaps include several 403'd/snippet-only pages (official USDA REAP, Poultry Site/MSU LED,
  Kansas City Fed lending) and vendor price tables captured via WebFetch extraction rather than raw
  reads. Two sources were read end-to-end from the document itself and are the load-bearing anchors:
  the **Iowa State Egg Industry Center** cost-of-production reports (Stream 1) and PCT packaging report
  (Stream 5).
- **Division of trust for the build:** the *realism* (what's a good/bad offer, invoice-error types,
  trade-credit math, packaging structure) comes from this research; the *offer payback economics* are
  computed by the orchestrator from the model code and coefficients (see the synthesis §1). Any web
  figure that becomes a `[sourced]` number in the corpus will be traced to its primary source during
  the build before it is written.

## Relationship to the R8 mechanism research

This extends `evals/hen/research/2026-08-07-r8-financial-mechanisms/` (which established *which*
mechanisms exist and their ground truth) with the **content realism** needed to author them credibly.
