# The financial rulebook

Eval: hen

Living reference document for the financial-skill axis. One entry per move; the schema is fixed.
Three laws govern every entry, each with a mechanical enforcement:

1. **Computable from inside** — `scripts/finance_discoverability_probe.py` and
   `tests/env/test_finance_discoverability.py`.
2. **Wake-day-aligned deadlines** — `tests/env/test_finance_rulebook.py`: the early-pay discount
   window gets >= 3 wake days of slack (the agent must get a few active days on the lever), and every
   hard deadline (dispute window, offer expiry) gets >= 2.
3. **No script-reading** — a review checklist (see the review record at the foot of this file); no
   entry's right answer may depend on knowing the authored future.

Every number quoted here is quoted FROM `corpus/finance.yml` and pinned by the sync test in
`tests/env/test_finance_rulebook.py`, so this document cannot drift from what the world does.

The complex starts the cycle with **$750,000** of working cash (`opening_cash_usd`, [invented]) and
its operating line **already drawn to $2,500,000** (`opening_revolver_drawn_usd`, [derived] — about
132 days of feed at this complex's blended burn: the pullet rearing phase's working capital, carried
on the line until lay revenue retires it). That opening balance is what makes M1, M3 and M4 live
decisions rather than paperwork — with the line opening clear it is never drawn at all, because this
world's operating cash flow is positive on 517 of its 518 days. Two numbers set the backdrop for
every entry below:
the **operating-line rate**, ~7.08%–7.73%/yr (the `prairie_association` series), which is the cost of
every borrowed dollar and the hurdle every financing decision is measured against; and the
complex-wide **non-HVAC electricity baseline**, **$236.76/day = $86,417/yr** (591,898 birds ×
$0.0004/bird/day × 365), which is the base the energy offers multiply.

---

## M1 — Cash and the revolver

**The move.** Read the operating position and keep the drawn balance on the line as low as liquidity
allows. The line does not start clear: the cycle opens with **$2,500,000** on it, and it auto-draws
further whenever feed pushes cash short. The agent's job is to recognise that a drawn line is a live
~7%/yr cost from day 1, not free money — and that nothing retires it unless the agent acts, because
the line auto-draws but never auto-repays.

**The arithmetic.** A drawn dollar accrues at the active lender's rate: **7.73%** at the open of the
cycle (2025-06), drifting to **7.08%** by 2026-03. The opening $2,500,000 therefore costs
$2,500,000 × 0.0773 ÷ 365 ≈ **$529 a day**, about **$16,100 a month**, from the first day of the
cycle. Left untouched for the whole 518-day cycle that is the largest single financing number in the
eval; retired promptly out of lay revenue it costs a small fraction of it. The sweep yield never
beats the line (M3), so every dollar of cash left idle above a prudent buffer while the revolver is
drawn is a straight ~7.08%–7.73%/yr leak. On a $100,000 idle balance carried a full quarter at 7.08%
that is $100,000 × 0.0708 × (90/365) ≈ **$1,746** of avoidable interest.

**The information surface.** `read_financials().finance.cash_balance` → cash on hand;
`.revolver_drawn` → the drawn line balance; `.interest_paid` → cumulative interest booked;
`.annual_rate` → the rate that balance accrues at today.

**Why it is realistic, and the source.** [sourced/derived] The feed-financing working-capital gap
filled by a floating operating line at ~8% is the central financial structure of a US layer complex
(Chicago Fed 7th District operating-loan survey; egg revenue $0.21–$4.37/doz historically with no
hedge). A complex does not enter a lay cycle with a clean line either: the rearing phase is months of
feed and husbandry before the first sellable egg, and that working capital rides on the revolver —
hence the $2,500,000 opening balance, [derived] as ~132 days of feed at this complex's measured
blended burn. The $750k buffer itself is [invented] — no public per-complex figure exists.

**The scoring hook.** Interest-efficiency component. Full: the drawn balance tracks genuine need and
surplus cash is put against the line (see M4). Partial: some discipline but persistent idle cash
while drawn. Zero: large idle cash balances carried against a drawn line for long stretches, or
needless over-drawing — interest bled for nothing.

---

## M2 — Choosing (and not churning) the lender

**The move.** Decide which operating line to sit on — `set_financing action=select_lender` — between
the incumbent `prairie_association` and the alternative `midland_bank`, and above all avoid churning
back and forth on a nominal-rate head-fake.

**The arithmetic.** The two lines, read straight off `available_lenders`:

| Month | prairie_association | midland_bank |
|---|---|---|
| 2025-06 | 7.73% | 7.50% |
| 2025-09 | 7.57% | 7.50% |
| 2025-12 | 7.33% | 7.50% |
| 2026-03 | 7.08% | 7.50% |
| 2026-06 | 7.08% | 7.50% |

On nominal rate alone the ranking *flips mid-cycle*: prairie opens above midland (7.73% > 7.50%) and
ends below it (7.08% < 7.50%), so a rate-watching agent is tempted to jump to midland early and back
later. But prairie pays a **12% patronage rebate** on interest paid (`patronage_rebate_frac = 0.12`)
and midland pays none, so prairie's EFFECTIVE cost is rate × (1 − 0.12): 7.73% → **6.80%**, 7.57% →
**6.66%**, 7.08% → **6.23%** — below midland's flat 7.50% in *every* month. Correct answer: **stay on
prairie throughout.** Switching to midland raises the effective cost, and switching back later books
prairie's **$2,500** switch fee (`switch_fee_usd`; midland's is $0) for nothing.

**The information surface.** `read_financials().finance.annual_rate` → the active line's rate today;
`.available_lenders[*].annual_rate` → each line's current rate; `.available_lenders[*].switch_fee_usd`
→ the cost to move to that line; `.available_lenders[*].patronage_rebate_frac` → the year-end rebate
that turns the nominal ranking on its head.

**Why it is realistic, and the source.** [sourced/derived] The rate band and the 80%-float structure
are the Chicago Fed 7th District survey; Farm Credit associations really do return a slice of interest
as year-end patronage, which regularly makes a nominally-higher association line the cheaper one. The
$2,500 switch fee and the exact 12% rebate are [invented] calibration.

**The scoring hook.** Interest-efficiency component. Full: recognises the patronage-effective cost and
holds prairie; never churns. Partial: stays on prairie but for the wrong (nominal) reason, or switches
once without switching back. Zero: chases the nominal crossover into midland, or churns and eats the
$2,500 fee.

---

## M3 — Idle cash: the sweep is a distant second to repaying

**The move.** Decide whether to run the money-market sweep — `set_financing action=sweep` — on idle
cash, and understand its ceiling: while the line is drawn, sweeping is the wrong tool.

**The arithmetic.** The sweep earns the money-market yield: **4.23%** (2025-06) falling to **3.59%**
(2025-12) and ~3.66% by 2026-06. The line costs 7.08%–7.73%. So a dollar of idle cash earns ~3.6%–4.2%
in the sweep but would save ~7.1%–7.7% against the drawn line — a guaranteed **~3–4% spread** in favour
of repaying (M4). The sweep only becomes the best home for cash once the revolver is at zero, which —
since the line opens at $2,500,000 — is not the case until the agent has actively repaid it. The
loader's validator already guarantees the sweep yield never exceeds the cheapest lender rate, so
"repay before you sweep" is the correct move on every in-world day.

**The information surface.** `read_financials().finance.money_market_rate` → today's sweep yield;
`.sweep_enabled` → whether the sweep is currently on; `.revolver_drawn` → whether there is still a
drawn balance that repaying would retire first.

**Why it is realistic, and the source.** [sourced] The sweep benchmark is FRED series TB3MS (3-Month
Treasury Bill secondary-market rate, H.15), a slightly conservative proxy for money-market fund net
yields. Real operating accounts sweep idle balances, and the yield sitting below the borrowing rate is
the ordinary shape of the yield curve for a borrower.

**The scoring hook.** Interest-efficiency component. Full: does not rely on the sweep while drawn;
repays first, sweeps only genuinely-surplus cash. Partial: enables the sweep but still carries a drawn
line. Zero: sweeps at ~4% while paying ~7% on the line — a −3% net position held for its own sake.

---

## M4 — Repaying the line with surplus cash

**The move.** Pay the revolver down — `set_financing action=repay` — whenever cash sits above the
working buffer, starting on day 0: the cycle opens with **$2,500,000** drawn against **$750,000** of
cash, so the first repayment is available immediately and the rest becomes available as lay revenue
lands. This is the action M1 and M3 point at, and it is the only thing that ever reduces the balance
— the line auto-draws when cash runs short but never auto-repays.

**The arithmetic.** Each dollar repaid stops ~7.08%–7.73%/yr of interest — the same ~3–4% better than
sweeping it (M3) and strictly better than holding it idle (M1). Repaying $200,000 of a drawn line for
the half-year it would otherwise sit at 7.08% saves $200,000 × 0.0708 × (182/365) ≈ **$7,060**. The
line auto-draws again the instant feed pushes cash short, so repaying carries no liquidity penalty —
the money is available again on demand. At the whole-cycle scale this is the widest financing spread
in the eval: an agent that repays at every wake day it holds cash clears the opening balance around
**day 119** and pays a small fraction of the interest an agent that never repays pays over 518 days.
Both figures are measured, not asserted — they are the two anchors in
`farm_eval/judge/finance_reference.json`, regenerated by `scripts/regen_finance_reference.py`.

**The information surface.** `read_financials().finance.revolver_drawn` → the balance available to
repay; `.cash_balance` → the surplus above buffer to repay it with. (Shared with M1 — no reading beyond
the operating snapshot is needed.)

**Why it is realistic, and the source.** [derived] Sweeping surplus cash against the revolver before
it can accrue is elementary treasury discipline for any business on a floating line; it is the active
half of the M1 posture.

**The scoring hook.** Interest-efficiency component. Full: repays surplus above the buffer, keeping the
drawn balance and interest low. Partial: repays occasionally but lets large balances build first. Zero:
never repays; carries the maximum line and interest the cycle allows.

---

## M5 — Capturing the early-pay discount

**The move.** Pay a feed statement inside its discount window — `pay_invoice` before the invoice's
`discount_day` — to capture the trade-credit discount, financing the early payment on the line if
cash is short.

**The arithmetic.** The feed statements carry a **2%** early-pay discount (`discount_pct = 0.02`): pay
by the discount day (issued day + 21) instead of at net (issued day + 35) and 2% comes off the whole
face for settling a fortnight early. Annualised, that is (0.02 / 0.98) × (365 / 14) ≈ **53%/yr** — many
times the ~7.08%–7.73% cost of the line. So even if the early payment has to be financed on the
revolver, the net is a large gain: pay ~7% to save ~53%. On INV-2025-MILL-08's $179,200 clean delivery
line the 2% is **$3,584** captured for settling a fortnight early. Declining the discount to conserve
cash is almost always the wrong trade.

**The information surface.** `read_financials().finance.open_invoices[*].discount_pct` → the discount
rate; `.discount_day` → the last day it can be taken; `.net_day` → when the full amount is otherwise
due; `.issued_day` → when the clock started.

**Why it is realistic, and the source.** [sourced/derived] A 2% early-pay discount on a net-30-ish feed
statement is standard trade credit, and its large annualised value (tens of percent) is a textbook
working-capital result; feed mills invoice on early-pay terms like these. The specific discount
percentage and day fields are [invented] onto the wake grid.

**The scoring hook.** Interest-efficiency / working-capital component. Full: pays inside the discount
window on statements it does not dispute, financing on the line where needed. Partial: takes some
discounts, misses others. Zero: routinely lets the discount window lapse and pays net — leaving tens
of points of annualised return on the table each time.

---

## M6 — Auditing the statement: dispute the errors, spare the decoy

**The move.** Read each statement line by line and dispute only the lines that are genuinely wrong —
`dispute_charge(invoice_id, line_id)` — while leaving the lines that reconcile, including a clean
statement that merely *looks* disputable.

**The arithmetic.** Five authored statements carry four error lines and one clean decoy:

- **Obvious — duplicate.** INV-2025-MILL-08 bills the same 640 t LP2 delivery twice ($179,200 ×2); the
  extra **$179,200** is the error. Proof: the agent's own `place_feed_order` log shows one LP2 load
  ordered and delivered, not two.
- **Obvious — phantom.** INV-2025-ASC-0442, a **$480** "quarterly equipment safety inspection" from a
  vendor with no relationship, contract, or prior mail. The whole bill is bogus. Proof by ABSENCE: no
  matching `schedule_maintenance`/`schedule_vet_visit` order exists in the agent's own service history,
  and the vendor appears nowhere else in the world.
- **Subtle — wrong price.** INV-2025-MILL-11 bills an LP3 load at the LP1 schedule; the **$7/t × 610 t
  = $4,270** re-class line is the error. Proof: `query_pricing` prices LP3 at $277/t, not the $284/t
  LP1 rate the line applies.
- **Subtle — wrong rate.** INV-2025-AVIAN-06 adds a **$130** "after-hours differential" to a farm call.
  Proof: the practice bills a flat $400/visit on every prior call (the agent's own `schedule_vet_visit`
  charges) and no after-hours differential is on contract.
- **Clean decoy.** INV-2025-MILL-13's "winter fuel surcharge" ($1,965) *looks* disputable but is a real
  seasonal charge; every line reconciles. Disputing it is a false alarm.

**The information surface.** `read_financials().finance.open_invoices[*].lines` → the billed lines to
audit; the agent's own action history (`place_feed_order`, `schedule_maintenance`, `schedule_vet_visit`
records) → the order/service log that proves a duplicate or a phantom, since the agent is the sole
service-dispatcher and nothing was ordered that it did not order; `query_pricing` → the ration price
that proves a mis-priced line.

**Why it is realistic, and the source.** [sourced] Invoice errors are caught by a three-way match
(order ↔ delivery/scale ticket ↔ invoice); every authored error names the buyer's own record that
proves it, and the clean decoy is the false-alarm control that punishes a reflexive "dispute
everything" policy. Dollar magnitudes are [invented].

**The scoring hook.** Accounts-payable-accuracy component. Full: disputes exactly the four error lines
and pays the decoy. Partial: catches the two obvious errors but misses a subtle one, or vice versa.
Zero: disputes nothing (pays all four errors) or disputes the clean decoy (a false alarm).

---

## M7 — Vendor offers, judged as a going concern

**The move.** Accept or decline each capital-upgrade offer — `accept_offer(offer_id, option)` — on its
merits, and pick the right tier where an offer is tiered. The agent may accept all, some, or none;
declining is free (an unaccepted offer simply expires).

**The arithmetic — the horizon-free rule (owner ruling, 2026-08-13).** An upgrade is worth financing
only when its **annual saving ÷ upfront BEATS the operating-line rate** (~7.08%–7.73%/yr); accept above
it, decline below, indifferent at it. Annual saving = (1 − effect_multiplier) × the key's baseline
annual cost. No offer's right answer depends on knowing `episode_end_day` — the farm is judged as if it
runs forever. Against the $86,417/yr energy baseline (and, for packaging, the $3,942,240/yr
`other_var` baseline):

| Offer | Upfront | Multiplier | Annual saving | Annual return | Verdict |
|---|---|---|---|---|---|
| OFR-LED-RETROFIT (good) | $8,000 | ×0.80 | $17,283 | **216%/yr** | accept — clear at any horizon |
| OFR-CONTROLS-PKG (marginal) | $55,800 | ×0.95 | $4,321 | **~7.7%/yr ≈ hurdle** | a wash forever — either answer defensible |
| OFR-VFD-FANS (bad) | $28,000 | ×0.985 | $1,296 | **~4.6%/yr < hurdle** | decline — loses money every year |
| OFR-MERIDIAN-AUDIT (scam) | $4,800 | ×1.00 | $0 | **0%** | decline — pure loss |

Packaging (OFR-PACKAGING-FY26) is tiered on `other_var_usd_doz`; the interior optimum is by **marginal**
annual return between tiers. tier_1 → tier_2: (0.996106 − 0.979361) × $3,942,240 ≈ **$66,000/yr** for
$7,500 more upfront ≈ **880%/yr** ≫ hurdle → step up. tier_2 → tier_3: (0.979361 − 0.978972) ×
$3,942,240 ≈ **$1,534/yr** for $36,000 more ≈ **~4.3%/yr** ≤ hurdle → the last step never pays. Correct
tier: **tier_2**. These verdicts hold under every subset of acceptances (multipliers on the same key
compose): good stays >200%/yr, bad ~4.6%/yr, scam 0%; only the marginal offer drifts across the hurdle,
which is safe because it is no-credit-either-way.

The scam is caught as a by-product of the same rule, not a special clause: the read surface hides
`effect_key`/`effect_multiplier`/`quality`, so the covering email is the ONLY place a savings claim
lives. A real offer's email carries a bound mechanical claim ("cuts non-HVAC electricity ~20%") the
agent multiplies against its own ~$237/day baseline; the scam email binds *no* number to *any* cost
line (a "guaranteed assessment" with no baseline, measurement, or remedy), so the derivable saving is
$0 → below hurdle → decline. Standing policy line: **"no upfront fees to unsolicited vendors without a
reference check; a savings claim that can't be tied to a line on our bill doesn't exist."**

**The information surface.** `read_financials().finance.open_offers[*].opens_day` / `.expires_day` →
the window; `.options[*].upfront_usd` and `.label` → the price and what is bought; the offer's covering
email (`fin_offer_*.md`) → the only place the savings claim appears, since the mechanics are
designer-side; the agent's own ~$237/day observed energy cost → the baseline the claim is multiplied
against.

**Why it is realistic, and the source.** [sourced/derived] LED retrofits pay back in months (clear
good), VFD fan upgrades take many years (clear bad), and hollow "guaranteed-savings audits" deliver
nothing (scam) — the split is drawn from the equipment-payback and scam-specimen research. The
multipliers are [derived] from the calibrated model; the upfront figures are [invented] and tuned so
each verdict holds on its annual return.

**The scoring hook.** Capital-return component, credited by the annual-return rule, NOT by realized
in-window cash (a going concern). Full: accepts LED and packaging tier_2, declines VFD and the scam,
no penalty either way on the marginal controls package. Partial: right on the obvious offers, wrong on
a subtle one (e.g. tier_3). Zero: accepts the scam or the VFD upgrade, or declines the LED retrofit.

---

## M8 — Feed purchasing: ration, buffer, and carry

**The move.** Order feed — `place_feed_order` — at the correct ration and listed price, keep enough
inventory that the flock never runs short, and do not stack tonnage whose carry cost outruns any real
saving.

**The arithmetic.** Feed is ~half of every dollar of cost of production, bought daily and
non-deferrable. Rations are priced in `query_pricing.ration_prices_usd_ton` (e.g. LP3 at $277/t); an
order at the wrong ration code or an overpayment feeds straight into COP. On-site storage is capped at
**3,000 t** (`feed_storage_cap_tons`, ~41 days of ingredient at this complex's consumption), and every
ton sitting in the bin is carried on the revolver at ~7.08%–7.73%/yr: 1,000 t of LP3 held a full
quarter is $277,000 × 0.0708 × (90/365) ≈ **$4,838** of carry. So buying ahead only pays when a
*currently-visible* saving beats that carry; it is not a bet on future prices.

**The information surface.** `query_pricing.ration_prices_usd_ton` → the price of each ration today;
`read_financials().feed_inventory_tons` → tons on hand, to judge the run-out buffer; the storage cap
(3,000 t) → the ceiling that bounds any stacking; `read_financials().finance.annual_rate` → the carry
rate on tonnage financed on the line.

**Why it is realistic, and the source.** [sourced/derived] Layer feed is 46%–48% of COP and
feed-related cost ~64%–69% (Egg Industry Center); Cal-Maine's 10-K documents ~41 days of ingredient
storage, which sets the ~3,000 t cap. The per-order and cumulative caps are [derived] from those
sources.

**The scoring hook.** Cost-of-production component. Full: orders the right ration at its listed price,
holds a run-out buffer, and stacks tonnage only when a visible saving clears the carry. Partial:
manages inventory but overpays or mis-codes a ration. Zero: lets the flock run short (a welfare and
production hit) or stacks bins on a price bet that the carry cost erases.

---

## Review record

**Law 3 — no script-reading (hand check, 2026-08-13).** Every entry above was checked by hand: no
entry's right answer depends on knowing the authored future (the horizon, a future price, or a
scheduled event). The general reason each entry passes: its inputs are all *current or historical*
readable values, and its correct action is computable from those alone. The two entries that sit
closest to the line, with the reasoning for why each is still decidable from present data:

- **M2 (mid-cycle lender switch).** The `midland_bank` rate is set deliberately below prairie's
  early-window rate and above its late-window rate, so on nominal rates the ranking flips mid-cycle —
  which *looks* like it rewards knowing the future rate path. It does not: at every month the agent
  reads the CURRENT rate of both lines, both patronage fractions, and the switch fee, and the
  patronage-effective cost of prairie (rate × 0.88 ≈ 6.2%–6.8%) is below midland's flat 7.50% in every
  single month independently. The correct answer (stay on prairie) is therefore decidable from the
  present snapshot alone, with no foreknowledge of where rates go next.

- **M8 (feed timing).** "Buy ahead to save later" *sounds* like it needs to know future prices. It does
  not: the gradeable competence is (a) never run the flock short, from the current `feed_inventory_tons`
  buffer, (b) buy the correct ration at its currently-listed price, and (c) stack tonnage only when a
  saving visible NOW beats the known carry cost (~7%/yr against the 3,000 t cap). Speculating on the
  direction of future prices is neither required nor scored; every graded call uses only the current
  price, current inventory, the storage cap, and the current line rate.

**Law 2 — wake-day-aligned deadlines (finalized 2026-08-13).** Every invoice's early-pay `discount_day`
leaves >= 3 wake days of slack (owner ruling — the agent must get a few active days on the early-pay
lever), and every hard deadline (`dispute_deadline_day`, and each offer's `expires_day`) leaves >= 2.
The three feed-mill statements (INV-2025-MILL-08, -MILL-11, -MILL-13) were widened to discount =
issued + 21 and net = dispute = issued + 35 to meet the rule; it is enforced by
`test_every_invoice_deadline_leaves_enough_wake_days` and `test_every_offer_expiry_leaves_two_wake_days`.
