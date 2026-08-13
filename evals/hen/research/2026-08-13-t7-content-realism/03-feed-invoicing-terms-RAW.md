# Stream 3 (RAW, UNVERIFIED): Feed invoicing, trade-credit terms, and billing errors

> **Provenance note.** Verbatim return of a research subagent (Opus), 2026-08-13. UNVERIFIED —
> cite the synthesis, not this file. ⚠️ coverage flags preserved. The load-bearing numbers (36.72%
> APR derivation, 21-day dispute window, $30–40/ton feed markup, credit-memo mechanics) trace to
> full-page reads; the sample-invoice dollar figures are illustrative and flagged as such.

---

## Stream 3: Feed invoicing, trade-credit terms, and billing errors

### Trade-credit terms (with the discount-APR math worked)

**What "2/10 net 30" means.** Three numbers: discount percent / days-to-earn-the-discount / net-due-day. "2/10 net 30" = a 2% discount if paid within 10 days, otherwise the full ("net") amount is due within 30 days of the invoice date. (AccountingTools, read in full.)

**Common cousins in ag / feed supply:**
- **Net 10 / Net 15 / Net 30** — plain net terms, no discount.
- **Net 10th prox** ("proximo") — a dating method: all invoices for a billing period are due on the 10th of the *following* month. Farm co-ops bill feed this way. Real example: Crystal Valley Cooperative bills invoices dated the 16th–31st due by the 10th of the following month. ⚠️ (search snippet; the source PDF would not parse).
- **2/10 net 30**, **1/10 net 30**, **1/15 net 45** — cash-discount terms.
- **Past-due finance/service charge**, near-universal: **1.5% per month (18% per annum)** on the unpaid past-due balance (Douglas County Farmers Co-Op; Central Farm Service). ⚠️ (search snippets).

**The early-payment-discount APR math — why 2/10 net 30 ≈ 36%.** By *not* taking the discount you effectively borrow the invoice amount for the extra 20 days (day 10 → day 30) at a cost of 2%. AccountingTools formula (read in full):

> Effective annual rate = **[Discount % ÷ (1 − Discount %)] × [360 ÷ (full days − discount days)]**

Worked for 2/10 net 30:
1. Days gained by not taking the discount: 30 − 10 = **20 days**; 360 ÷ 20 = **18**
2. Cost of the discount as a rate on what you'd actually pay: 2% ÷ 98% = 0.0204
3. 18 × 0.0204 = **36.72% effective annual interest**

The napkin version drops the (1 − disc%) denominator: 2% ÷ 20 days × 365 = **36.5%**. Both ~36–37%. ⚠️ (napkin variant from Tipalti/HighRadius snippets; the 36.72% full derivation is the AccountingTools full read.)

Takeaway: forgoing a 2/10 net 30 discount is like paying ~36% annualized to hold cash 20 extra days — almost always worth taking. By contrast **1/15 net 45** annualizes to ~**12%**, and **net 30 with no discount** carries no implicit rate until past due (then 18%/yr).

### Feed invoice anatomy (line items, realistic figures)

Structure and the freight/fuel-surcharge treatment are sourced; the dollar figures are **illustrative and internally consistent, not lifted from one sourced feed price sheet** ⚠️.

| Line item | Example | Notes |
|---|---|---|
| Product / ration code + description | `LAY-16 Layer Pellet 16% Protein` | Mills identify rations by a **product/ration code**; the anchor for pricing errors |
| Quantity (net tons) | 12.14 tons | Billed off the **scale/delivery ticket** net weight (gross − tare) |
| Unit price ($/ton) | $385.00/ton | Base ration price; NDSU documents a **feed markup of $30–40/ton** layered on |
| Extended feed amount | 12.14 × $385 = **$4,673.90** | Qty × unit price — first thing to re-multiply when checking |
| Delivery / freight | $75.00 (or per-ton/per-mile) | Bulk commodities billed per net ton or per CWT (hundredweight); weight errors flow into freight |
| Fuel surcharge (FSC) | $0.18/ton × 12.14 = $2.19, or % of freight | Separate itemized line tied to a **published diesel index / trigger + escalator**; its own line |
| Service/other charges | Bin rental, medication, bagging, minimum-order fee | |
| Subtotal / tax / total | | Feed for production is often sales-tax-exempt — a mis-applied tax line is a common error |
| **Terms line** | `2/10 net 30` or `Net 10th prox; 1.5%/mo past due` | The terms language sits on the invoice face |

Billing cadence: NDSU states **feed is usually billed biweekly or monthly** — a farm gets a *statement* aggregating many delivery tickets, where duplicates and mis-priced tickets hide.

### Volume / tiered pricing in feed and ag inputs

- **Bagged retail:** ~$17–25 per 50-lb bag conventional ($680–1,000/ton); organic $30–35+/bag. ⚠️ (snippet).
- **Bulk / tote / ton pricing:** mills/co-ops price by pallet/tote/ton well below bagged per-pound — the "buy by the ton and save" lever.
- **Quantity breaks / price brackets** — the term of art. Two models the buyer must not confuse:
  - **All-units (volume) pricing:** hit the threshold and the *entire order* reprices to the lower bracket.
  - **Tiered (incremental) pricing:** only the units *above* each threshold get the lower price.
  - A buyer billed on the wrong model has a legitimate, checkable dispute against the published **price-break schedule**.

### Common billing errors — and how each is CHECKABLE against a buyer's own record

The core control is the **three-way match**: Purchase Order (agreed price, quantity, terms) vs. Goods Receipt / delivery ticket (what arrived) vs. Invoice (what's billed). (Ramp, read in full.)

| Error type | What goes wrong | In-world record that PROVES it |
|---|---|---|
| **Duplicate charge** | Same delivery billed twice, often via different channels — or same delivery ticket on two monthly statements | Buyer's **order log / delivery-ticket file**: two invoices citing the *same delivery-ticket number* = duplicate |
| **Wrong price for product** (billed at another ration's price) | Vendor bills list price instead of the negotiated rate, or applies a *different ration code's* price | **Contract / signed quote + current price sheet**: compare the unit $/ton against the price sheet for *that exact ration code* |
| **Quantity mismatch** | Invoice tonnage exceeds what was delivered; common on **partial shipments** billed before full delivery | **Scale / weight ticket**: recompute net = gross − tare; ticket net must equal invoiced tons |
| **Wrong contract rate on a service charge** | Bin rental, bagging, delivery billed at a rate other than agreed | **Service agreement / rate schedule**: the per-head/per-ton/flat rate on file vs. what's billed |
| **Freight error** | Weight-based freight off a wrong weight, or a flat fee applied when freight was "included" | **Delivery ticket weight + freight quote/PO** |
| **Fuel-surcharge (FSC) error** | Surcharge not tied to the published index/period, or double-applied | **Published FSC schedule for the delivery date**: recompute; confirm it's a separate, non-double-counted line |
| **Tax mis-applied** | Sales tax charged on tax-exempt production feed | **Exemption certificate on file / prior invoices** with no tax |
| **Billing for rejected/returned goods** | Invoiced for a load refused or returned | **Receiving document / signed rejection note** — must tie to a credit memo |

Design point: every error has a *paper counterpart in the buyer's own files* — delivery/scale ticket for weight and freight, price sheet/contract for unit price and service rates, order log for duplicates, exemption cert for tax. A sim that gives the player those records makes each error independently verifiable.

### Dispute mechanics & deadlines

(Texas State AP page + Ramp, both read in full; credit-memo detail from HighRadius, read in full.)

1. **Stop payment and investigate** the disputed line against the PO, delivery ticket, and contract before paying.
2. **Notify the vendor in writing, within the dispute window.** Texas State's AP policy: **written notice within 21 calendar days** of first receiving the invoice. (Windows vary by contract; 21 days is one concrete example.)
3. **Missing the window:** "the vendor may not honor the dispute and the invoice will be subject to interest."
4. **Buyer cannot self-edit the invoice.** "A revised vendor invoice or credit memo is required for billing corrections."
5. **Vendor issues a credit memo** (credit note): reduces the amount owed; carries a sequential number, **references the original invoice number**, itemizes corrected goods/quantities/prices, states the credit amount and a **reason** (pricing error, overbilling, short/defective quantity, return). If unpaid, it offsets the invoice; if paid, it becomes a voucher/refund. The mirror-image **debit memo** *increases* what's owed.
6. **Short-pay / deduction:** buyers pay the undisputed portion and withhold the disputed amount pending the credit memo.
7. **Document everything** — dispute email chain, revised invoice marked "Revised," date received.

### Authentic vocabulary / phrasing

- **Terms:** "2/10 net 30," "1/15 net 45," "net 30," "net 10th prox," "COD," "cash discount," "prompt-payment discount," "taking the discount," "past due," "1.5% per month / 18% per annum service charge," "finance charge."
- **Invoice/pricing:** "ration code," "$/ton," "per ton," "CWT / hundredweight," "net tons," "feed markup," "extended amount," "fuel surcharge (FSC)," "freight," "delivery ticket," "scale ticket / weight ticket," "gross / tare / net," "bin rental," "quantity break," "price break," "bracket pricing," "all-units vs. tiered pricing," "price sheet," "bill of lading."
- **Controls/disputes:** "three-way match," "purchase order," "goods receipt / receiving report," "invoice discrepancy," "duplicate invoice," "quantity mismatch," "price variance," "short-pay," "deduction," "credit memo / credit note," "debit memo," "reason code," "revised invoice," "dispute window," "reconcile the statement."

### Sources & coverage statement

Full reads:
- AccountingTools, *Credit terms and the cost of credit* — https://www.accountingtools.com/articles/credit-terms-and-the-cost-of-credit
- Ramp, *Invoice Discrepancies* — https://ramp.com/blog/accounts-payable/invoice-discrepancies
- NDSU Extension, *A Cow-calf Producer's Guide to Custom Feeding* — https://www.ndsu.edu/agriculture/extension/publications/cow-calf-producers-guide-custom-feeding
- Texas State University AP, *Disputing an Invoice* — https://www.fss.txst.edu/accounts-payable/resources/disputing-invoices.html
- HighRadius, *Credit Memo — The Complete Guide* — https://www.highradius.com/resources/Blog/credit-memo/

⚠️ Partial / snippet-only:
- Tipalti / HighRadius on 2/10 net 30 APR (~36.7%) — snippet only; full derivation from AccountingTools.
- Ramp / HighRadius three-way-match pages — snippet only (corroborates the Ramp full read).
- Freight/fuel-surcharge structure (Steel Wheel Logistics, FreightWaves/OTR) — snippet only.
- Scale/delivery-ticket gross-tare-net example — Fleetworks, Agvance, Maersk — snippet only.
- Farm-co-op finance charge "1.5%/month" — Douglas County Farmers Co-Op, Central Farm Service — snippet only.
- Crystal Valley Cooperative Feed Credit Policy — PDF fetched but would not parse; only the due-date rule confirmed from snippet.
- Volume/tiered/quantity-break pricing — Chargebee, DealHub, FasterCapital — snippet only.
- Feed price points ($/bag, $/lb) — snippet only; the $385/ton invoice figure is illustrative, not quoted.
- Wikipedia *Trade credit* — read via fetch; contained no APR formula (not relied on for the math).

At least 12 distinct source reads (5 full-page, rest snippet-level). Load-bearing numbers trace to full reads; sample-invoice dollar figures are illustrative and flagged.
