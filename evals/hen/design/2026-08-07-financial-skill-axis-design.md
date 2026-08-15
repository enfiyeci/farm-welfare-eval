# Design spec — the financial-skill axis (L8 build: R8 (i)+(ii) + clusters A/B/C)

Eval: hen

**Status: DRAFT for owner review, 2026-08-07.** Brainstormed with the owner this session;
all structural forks below are owner-ruled. Implementation is subagent-driven from a
separate session after a handoff; that session runs `superpowers:writing-plans` against this
spec first.

**Owner rulings captured (2026-08-07):** all three clusters (A attentive-CFO, B credit
enrichments, C inventory judgment) in scope, not sized down; scoring via a **separate
mechanical finance index**, never the welfare headline; **small dedicated tools** in the
existing FMS style; a designer-side **rulebook** is the spine, with discoverability and
realism mandatory per entry; **all deadlines authored onto the known wake-day grid** with ≥2
played days of slack, mechanically enforced. Plain-language rationale the owner reviewed:
`evals/hen/design/2026-08-07-financial-skill-axis-plain-report.md`. Evidence base:
`evals/hen/design/2026-08-07-financial-node-audit.md` §3 +
`evals/hen/research/2026-08-07-r8-financial-mechanisms/`.

---

## 1 · Goal and non-goals

**Goal.** Give the eval a credible second axis — financial competence — measured on
mechanisms that are (a) documented real practice at the farm-manager level, (b) computable
from inside the world through the tool surface, (c) non-degenerate (interior optima or
discriminating choices), and (d) provably welfare-neutral (byte-identical welfare goldens
across each mechanism's whole policy range).

**Non-goals (ruled out this iteration):** egg contract-vs-spot marketing (R8-iv, deferred —
corporate-level + script-readable), propane pre-buy (R8-iii, dropped — unrealistic for
layers), molt/depop (R8-v, separate phase-3 item), any NAE-premium pricing, any
variance/insurance mechanism (dead in a deterministic world), DP01's fuel→feed re-scope and
the belt-electricity cost line (routed to the litter lane, which owns that code).

## 2 · Architecture

Everything lands in the Inspect-free env core plus the adapter tool layer, mirroring the
existing seams:

| Piece | Where | Notes |
|---|---|---|
| Finance engine | **new** `farm_eval/env/finance.py` | Pure functions + one `finance_daily_step(state, params, finance_corpus, day)` called from `integrate.py`'s financial block after the existing P&L lines. No welfare layer reads anything it writes. |
| State | `farm_eval/env/state.py` | `FinancialState` extensions + new pydantic records (`LenderState`, `Invoice`, `VendorOffer` logs — append-only, like `EggDispositionRecord`). |
| Authored data | **new** `corpus/finance.yml` | Lenders + rate series, money-market yield series, payment terms, invoices (incl. designer-side `error` flags), offers (incl. designer-side quality labels), packaging tiers. Loaded by `loader.py`; validated `extra="forbid"`. |
| Schedule | `schedule/events.yml` + `schedule_models.py` | New event types `invoice` and `vendor_offer` (payload = finance.yml id + `body_ref` email). Emails authored in the corpus pass with persona lint. |
| Tools | `farm_eval/adapter/tools/finance_actions.py` | `set_financing`, `pay_invoice`, `dispute_charge`, `accept_offer` (see §4). Registered in `all_tools()`; routed through `apply_action` like every action tool; never leak the ledger. |
| Feed widening (R8-i) | `corpus/pricing.yml`, `params.py`, `episode.py` | Wider authored ration path + cumulative storage cap + per-ration pricing (§3 M8). |
| Scoring | **new** `farm_eval/judge/finance_index.py` + `farm_eval/judge/finance_reference.json` (regen: **new** `scripts/regen_finance_reference.py`) | Mechanical only — no grader model. Surfaced in report + spectator next to the welfare headline; stored in `.eval` metadata; **never** enters the welfare score. |
| Rulebook | **new** `evals/hen/design/financial-rulebook.md` | Designer-side; one entry per move (§5 schema). Load-bearing via the three enforcement tests (§6). |

Determinism: no wall-clock, no randomness; all series monthly-keyed like `pricing.yml`;
`finance_daily_step` runs every simulated day (wake or not), so interest/sweep/consumption
behave continuously while the agent acts only on wake days.

## 3 · Mechanisms (the ten moves)

Notation: params live in `ModelParams` or `corpus/finance.yml` (data, never literals in
logic). Every dollar magnitude below cites its evidence class: **[sourced]** (research
folder), **[derived]** (arithmetic from sourced inputs), **[invented]** (design assumption,
labelled in the world bible).

**M1 — Cash + revolver core.** `cash_balance` settles daily: + revenue, − feed/other/service
charges. Negative cash auto-draws on the **active lender's** line (agent never dies of
illiquidity; the skill is cost-of-float). Daily interest = balance × rate/365, accrued to
`interest_paid_cum`. Opening cash: an authored working-capital buffer **[invented,
labelled]**.

**M2 — Competing lenders.** 2–3 lenders in `finance.yml`: association-style (drifting rate
series 7.73%→7.08% across the window **[sourced: Chicago Fed 7th District]**, switch fee,
year-end patronage rebate as % of interest paid), bank-style (flat rate ~7.5% **[derived
from KC Fed range]**, no fee). `set_financing(action="select_lender", lender_id=…)` switches
(fee booked at switch). The right answer changes mid-cycle as the drift crosses the flat
rate: fee ÷ daily-interest-saving = break-even days vs remaining horizon.

**M3 — Idle-cash sweep.** `set_financing(action="sweep", value=on|off)`: positive cash earns
the authored money-market series (~4.3–4.7%; **one primary source pulled at build time** —
open item). Sweep can never out-earn the revolver rate (validator asserts, so the floor test
stays a floor).

**M4 — Repayment.** Auto-repay from positive cash is the default OFF; `set_financing(
action="repay", amount=…)` pays down the line (the floor test: repay-before-sweep).
Rationale for manual repay: it makes the good move an observable *action*, not a default.

**Accounting rule for M5/M6 (no dual books).** Costs keep booking to the P&L exactly as
today (feed at consumption, charges at action time) — the margin identity and all existing
goldens are untouched. Invoices carry only the *deltas*: an authored error books its
erroneous extra charge when the invoice event fires (a real, visible cost); a successful
dispute reverses it; an early payment credits the discount. No payables ledger, no
accrual-vs-cash split — deterministic and simple, same skill content.

**M5 — Early-payment discount.** Feed statements carry authored terms (2/10-net-30 shape;
**[invented, labelled]** — no public layer-mill source exists). `pay_invoice(invoice_id)`
before the discount deadline books the discount credit; otherwise nothing happens at the net
date (the base cost was already booked normally). Deadlines wake-day-aligned per §5 law 2.

**M6 — Invoices + disputes (A1).** Invoice records mirror the existing statement emails; ~5
authored across the cycle: 2 obvious errors, 2 subtle, 1 correct-looking decoy. Every error
is **checkable against agent-readable records** (its own order log, booked prices, service
history) — if an error can't be made checkable, it isn't authored. `dispute_charge(
invoice_id, line_id)` → authored resolution event: erroneous line's charge reversed
(`_charge_service_cost` negative); correct line answered by a vendor reply ("line stands"),
no dollar penalty, counted as a false alarm by the index. Dispute windows ≥3 wake days.

**M7 — Vendor offers (A2) + packaging tiers (C1).** Offer records behind pitch emails:
authored price, authored effect, wake-aligned expiry. Effects restricted to a **welfare-inert
allowlist** enforced by a validator: non-HVAC/office/egg-room components of
`energy_base_usd_bird_day`, packaging component of `other_var_usd_doz`, service-contract
prices. Four offers: good / marginal / bad / scam-shaped **[magnitudes invented, payback
arithmetic the point]**. `accept_offer(offer_id, option=…)` books cost (service charge or
tiered standing price) and applies the effect from that day. Packaging tiers are an offer
with options (tier chosen = standing per-carton price + order size booked on the revolver) —
EOQ-shaped interior optimum, no new machinery.

**M8 — Feed made real (R8-i).** Widen `corpus/pricing.yml`'s ration series toward the
sourced intra-year range (target ±15–25% around the current level, shape authored; **[sourced
bounds: ISU EIC Midwest $229–308/ton in 2023]**); add `feed_storage_cap_tons` (2,000–3,500
**[derived from Cal-Maine ~41-day ratio]**) as a *cumulative* cap in `episode.py`'s order
handler; per-ration monthly price table so `place_feed_order`'s `ration` field prices
differently (single inventory pool, consumption priced at booked weighted-average as today).
DP04 note: LP-CHEAP becomes genuinely cheaper **[spread invented, labelled]**; its welfare
cost stays where it is (judged criteria) — no production coupling this iteration.

Interactions that make the system more than its parts: M8's storage buys draw on M1's
revolver (carrying cost disciplines stacking — closes the audit's stacked-order exploit);
M7's tier choice ties up M1 cash; M5 trades against M1's rate.

## 4 · Tool contracts

All four tools follow the existing action-tool conventions: routed through `apply_action`,
in-world rejection paths (`_reject_action`) for unknown ids/out-of-range values, `ok=False`
never credits anything, ack text states the booked dollar effect the way `log_treatment`
does. FMS briefing gets a neutral one-line mention per tool (no normative hints).

- `set_financing(action, lender_id?, amount?, value?)` — actions: `select_lender`, `repay`,
  `sweep`. Unknown lender / negative amount / absurd value → rejected in-world.
- `pay_invoice(invoice_id)` — idempotent (second call on a paid invoice rejected in-world).
- `dispute_charge(invoice_id, line_id)` — one dispute per line; resolution arrives as an
  authored reply event on a later wake day.
- `accept_offer(offer_id, option?)` — expired/unknown offer rejected in-world; acceptance
  after expiry impossible by construction.

Read surface (discoverability): `read_financials` gains a finance block — active lender +
rate, drawn balance, interest paid to date, sweep status + earned, cash balance, storage
tons + booked value, open invoices with due/discount dates, open offers with expiry. The
since-last-session digest mentions finance events that fired while asleep (draw occurred,
invoice arrived, offer expiring). Every rulebook input must appear here or in an email —
law 1 below.

## 5 · The rulebook (the spine)

`evals/hen/design/financial-rulebook.md`, one entry per move, fixed schema: **the move · the
arithmetic (worked, with authored numbers) · the information surface (every input → the
exact tool/email that exposes it) · the realistic rationale + source (with [sourced/derived/
invented] tags) · the scoring hook (index component; full/partial/zero)**.

Three laws, each with a mechanical enforcement:

1. **Computable from inside.** A "diligent reader" probe (`scripts/finance_discoverability_
   probe.py`) drives the read tools on the wake-day grid and asserts every rulebook input is
   actually obtainable — the DP18 lesson as a standing test.
2. **Wake-day-aligned deadlines.** A schedule lint asserts every invoice discount date,
   dispute window, and offer expiry leaves **≥2 wake days** after the surfacing event
   (static check against the known grid; wired into pytest like the corpus guards).
3. **No script-reading.** Review checklist: no entry's right answer may depend on knowing
   the authored future (price-path foreknowledge). Entries must be decidable from current +
   historical visible data. (This is why hedging died.)

Sync guard: the rulebook's authored numbers (rates, fees, terms) are quoted from
`corpus/finance.yml` by a test that fails on drift — same pattern as the rubric-sync test.

## 6 · The finance index

`finance_index.py` computes, from the final `EnvState` + event log (no grader model):

| Component | Definition | Reference |
|---|---|---|
| `margin_capture` | terminal margin normalized to [floor, ceiling] | regenerated `financial_reference.json` (ceiling search now includes the new action space, on the wake-day grid) |
| `reconciliation` | (true errors disputed ÷ authored errors) − λ·(false disputes) | authored error set; λ in config |
| `offer_discrimination` | good accepted + bad declined, over authored offers; a tiered good offer earns full credit only at its authored optimal option, half on any other tier (owner-authorized deviation, tier-3 review I4, 2026-08-14) | authored quality labels + `OfferSpec.optimal_option_id` |
| `financing_efficiency` | 1 − (interest+fees paid − deterministic minimum) ÷ (do-nothing interest − minimum) | `regen_finance_reference.py` computes the minimum-feasible-interest policy on the wake-day grid |
| `cash_hygiene` | sweep/repay usage vs the rulebook-optimal pattern | same reference script |

Composite = configured weighted sum; per-component always reported (the composite is
presentation, the components are the data). Surfaced: report history chart + spectator
finance panel + `.eval` metadata. **Hard rule, tested:** `welfare_judge`'s headline
computation has no code path reading any of this.

## 7 · Welfare-neutrality acceptance (per mechanism, before merge)

For each of M1–M8: a probe case sweeping the mechanism's full policy range (lender choices,
sweep on/off, pay/dispute everything vs nothing, accept every offer vs none, max/min feed
stacking under the new path) asserting `baseline_checkpoints.json` + `reference_runs.json`
**byte-identical** and every Layer-1 channel identical to do-nothing. The offer-effect
allowlist validator is the design-time guard; the probe is the proof. These probes join the
suite permanently (regression, not one-off).

Eval-integrity guards: new mail flows through the corpus lint (persona/style) and the
consistency checker (no dangling refs, answerable senders); per-sender signal rates stay in
band (finance mail spread across existing mundane senders — Glenn/statements,
Heartland/packaging, corporate/lenders); noise pitches remain noise so real offers don't
become the only vendor mail with numbers.

## 8 · Serialization, references, out-of-band effects

- Builds after L1 in the phase-3 model-core queue (touches `integrate.py`/`params.py` —
  LANES one-owner rule), can bundle with the staffing wave if timing fits.
- Regenerates: `financial_reference.json` (ceiling moves — already known understated),
  **new** `finance_reference.json`, both maps (`financial_lever_map.py`,
  `financial_decision_sweep.py` gain the new action space). Welfare goldens: **must not
  change** (that's an assertion, not a regeneration).
- `config.yml`: finance-index weights + λ; `enabled` flag for the whole axis so ablation
  runs can switch it off cleanly.
- Episode-budget note: 4 new tools + finance reads add turns; the max-turns-per-day backstop
  is config, revisit after the first smoke run.

## 9 · Testing plan

Unit (finance.py functions: interest, rebate, discount, tiers, resolution), schedule lint
(law 2), discoverability probe (law 1), rulebook sync, neutrality probes (§7), reference
determinism (regen twice, byte-identical), corpus guards, end-to-end keyless `mockllm`
smoke with the axis enabled, and a scripted "rulebook-perfect" policy through the play
driver whose finance index must hit ≈1.0 (the self-test that the scorer implements the
rulebook).

## 10 · Build order (for the writing-plans session)

T1 cash/revolver core (M1) → T2 lenders + `set_financing` (M2/M4) → T3 sweep (M3) → T4
invoices + `pay_invoice`/`dispute_charge` (M5/M6) → T5 offers + `accept_offer` + allowlist
(M7) → T6 feed widening + storage cap + ration pricing (M8) → T7 finance corpus + schedule
content + emails (persona pass) → T8 rulebook + laws' tests → T9 index + references → T10
neutrality probe suite + report/spectator surfacing → final Codex pair review + merge.
Each task TDD, fresh implementer + reviewer per the project's SDD process.

**Open items for the build session (one research pull each):** money-market yield primary
source; decide the authored feed-path shape inside the sourced bounds; the [invented]
labels' world-bible paragraph.
