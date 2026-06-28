# v2 Document Templates — Real Cage-Free Egg-Operation Paperwork

**Date:** 2026-06-27
**Scope:** Field names, units, ID/numbering conventions, layout structure, and realistic value ranges for the document types a corpus author needs to author (COP/variance, P&L/enterprise budget, feed/grain contract+invoice+scale ticket, egg sales contract + price sheet, SE lab reports, UEP audit report, APHIS/AVMA depopulation+indemnity paperwork, OSHA 300 logs, flock production records, vet reports).
**Source:** Deep-research report *"Cage-Free Egg Farm Documents and Reports"* (`~/Downloads/Cage-Free Egg Farm Documents and Reports.pdf`, 6 pp.). All example values are illustrative templates; the report repeatedly flags that **actual data should reflect current contracts and yields** — verify load-bearing numbers against the cited primary sources before hardcoding.

> Caveat carried from the source: example dollar values, dates, and IDs are mock/illustrative (e.g. "Values for illustration", "Example values only", "this example is illustrative; vet records aren't publicly available but follow these conventions"). The **formats, field names, and units** are the load-bearing parts; the **numbers** are realistic ranges, not authoritative figures.

Sources cited across the report: USDA AMS / USDA market-news price data (cage-free price examples); UEP guidelines + industry news (welfare audit structure); APHIS resources (indemnity forms VS 1-23 / VS 1-24, Flock Plan); FDA guidance, **21 CFR 118** (SE sampling labels + corrective action); AVMA + USDA depopulation guidance (depop record / post-depop review); OSHA instructions + **29 CFR 1904** (Form 300/300A log formats). The report does not give resolvable external URLs — citations are to these named regulatory/industry bodies.

---

## 1. Monthly Cost-of-Production (COP) Report — Cents per Dozen

Breaks down all egg-production cost in **¢/dozen**. Each line item labeled exactly as the company uses it ("Feed", "Pullets", "Labor", "Maintenance", etc.), units (¢/dozen) noted. If there's a variance vs. budget, include **"Budget" vs. "Actual"** columns and show the difference.

**Line items (with example ranges, Nov 2025 industry data):**
- **Feed (corn/soybean)** — non-organic ≈40.5 ¢/dozen; e.g. 40–45 ¢/dozen
- **Pullet depreciation** — ≈15.8 ¢; e.g. 15–20 ¢/dozen
- **Labor & Housing** — combined ≈39.0 ¢; e.g. 35–40 ¢/dozen
- **Vet/Medicine, Utilities, Maintenance, Packaging, Misc.** — e.g. 5–15 ¢ each (utilities or vet supply might add 5–10 ¢ each)
- **Total Cost** — sum of above, typically **~$1.00–1.20/dozen** for the example values

Format: a table or labeled list; every item carries its ¢/dozen unit. Variance reporting = Budget / Actual / difference columns.

---

## 2. Farm Profit & Loss / Enterprise Budget

Summarizes annual income and costs **per house or per enterprise**. Values often expressed **per dozen eggs** AND **per bird**. Production assumption: **~300 eggs/hen-year (~25 dozen/year)**.

**Structure (Revenue → Variable Costs → Fixed Costs → Net Profit):**
- **Revenue:** egg sales, spent hens, manure, etc. (e.g. Gross Income 2,500,000 dozen at $1.60/doz white and $2.10/doz brown — see §4 price sheet)
- **Variable Costs:** feed (~45 ¢/doz), pullets (16 ¢), labor (15 ¢), utilities (5 ¢), vet drugs, packaging — sum ~90–100 ¢/doz
- **Fixed Costs:** housing/equipment depreciation, repairs, interest, admin, taxes, insurance — ~15–25 ¢/doz
- **Net Profit:** Revenue minus total costs — could be **5–20 ¢/doz** depending on prices & efficiency

**Example table (columns: Item · Annual Total · Per Dozen ($) · Per Hen ($/yr)):**

| Item | Annual Total | Per Dozen ($) | Per Hen ($/yr) |
|---|---|---|---|
| Income (eggs) | $3,000,000 | $1.50 | $45.00 |
| · Feed, 1.9M lbs | −$1,215,000 | −$0.60 | −$18.00 |
| · Pullets (10,000 hens) | −$320,000 | −$0.16 | −$4.80 |
| · Labor | −$375,000 | −$0.15 | −$4.50 |
| · Other (vet, util, etc) | −$200,000 | −$0.10 | −$3.00 |
| · Depreciation | −$250,000 | −$0.12 | −$3.60 |
| · Insurance/Taxes | −$50,000 | −$0.02 | −$0.60 |
| **Total Costs** | **−$2,410,000** | **−$1.15** | **−$34.50** |
| **Net Profit** | **$590,000** | **$0.35** | **$10.50** |

Sub-headers group Variable Costs and Fixed Costs. (Example values only — actual data should reflect current contracts and yields.)

---

## 3. Feed/Grain Contract, Invoice, and Scale Ticket

Three linked documents in the grain-purchase chain.

### 3a. Grain Purchase Contract
Specifies **seller/buyer, commodity (e.g. #2 yellow corn, soybean meal), quantity, price terms, basis, delivery schedule, and terms**. Example clause: *"Buy 50,000 bu #2 corn at $5.80/bu, basis Chicago July minus 20¢, delivered to Ames, IA, Nov–Dec 2026."*
Fields: **Buyer name, Seller name, Commodity** (e.g. "Yellow Corn"), **Bushels, Price/bu, Basis, Delivery by date, Payment terms.** Often includes signature lines and dates.

### 3b. Feed Invoice (issued by seller on delivery)
Fields: **Invoice # and date, Buyer ID, Feed mill or elevator name, Description of goods** (e.g. "24,000 lbs Soybean Meal, 48%"), **Quantity (lbs or tons), Unit price, Extensions, Total.** May note the contracted price (e.g. "Contract #C2026-034"); scale-ticket copies attached.

```
Invoice: #12345   Date: 6/15/26
Sold To: Iowa Egg Farms, Inc. (Acct #)
Ship To: Feed Mill #5, Site A
Items:
- SBM 48% – 50,000 lbs @ $330/ton = $8,250.00
- Corn – 150,000 lbs @ $220/ton = $16,500.00
Subtotal: $24,750.00
Terms: Net 30 days
```
ID conventions: Invoice `#12345`, Contract `#C2026-034`, account #, site/mill IDs ("Feed Mill #5, Site A").

### 3c. Scale / Weigh Ticket (accompanies each delivery)
Fields: **Date/Time, Truck #, Gross Weight, Tare Weight, Net Weight, Moisture, Test Weight, Grade, and calculated bushels.**

```
Weigh Ticket #789012   Date: 6/15/2026  Time: 10:30 AM
Weighing Company: Heartland Elevator, Tama IA
Truck ID: IA-12345
Commodity: #2 Yellow Corn
Gross Wt: 80,000 lbs   Tare Wt: 25,000 lbs   Net Wt: 55,000 lbs
Test Wt: 56.0 lb/bu   Moisture: 15.5%   Dockage: 0.0%
Net Bushels: 55,000/56.0 = 982 bu
Grade: U.S. No.2 Yellow
```
Realistic ranges (for illustration): trucks **80–100k lbs gross**, **moisture ~14–15%**, test weight ~56 lb/bu for #2 yellow corn, grade "U.S. No.2 Yellow". Net bushels = Net Wt ÷ test weight. Truck ID convention `IA-12345`; ticket # `#789012`.

---

## 4. Egg Sales Contract & Price Sheet

### 4a. Sales Contract
Specifies **quantity, term, sizes, and prices** for egg sales. Sample clause: *"Seller agrees to supply 30,000 dozen large white at $1.60/dozen and 20,000 dozen large brown at $2.10/dozen, delivered weekly, over 12 months (Jul 2026–Jun 2027). Quality grade: Grade A, Shell eggs. Price is FOB, plus charges; terms net 10."*
Common fields: **Buyer/Seller, dates, size/grade, cage-free status, unit price ($/dozen), minimum and maximum quantities, duration, and any escalator** (e.g. tied to feed or CPI). Contracts often reference or attach market reports for transparency; may include price-adjustment clauses tied to published egg-market indices.

### 4b. Price Sheet (market reference)
USDA AMS or Urner Barry reports list current cage-free prices by **size/grade**. Lists **Contract** vs. **Spot** (negotiated) prices.

**Price Sheet Example (USDA AMS, Aug 29, 2025):**
- Cage-Free Large White (Contract): **$1.55/doz**
- Cage-Free Large Brown (Contract): **$2.10/doz**
- Cage-Free Large White (Spot): **$2.99/doz**
- Cage-Free Large Brown (Spot): **$3.07/doz**

(Source: USDA AMS / USDA market-news. Contract forms may reference such indices.)

---

## 5. Salmonella Enteritidis (SE) Testing Reports — FDA SE Rule (21 CFR 118)

Under **21 CFR 118**, farms record **environmental swab tests and egg pool tests** for SE. A lab report lists **Sample ID, Date Collected, House Number, Sample Type** (e.g. manure, eggbelt, egg contents), **Test Method (PCR/culture), and Result (Positive/Negative).**

**Sample ID convention — labeled by farm, house, and sample type + date** (`FarmA-House1-Env-060126`, `FarmA-House1-Egg-060126`):
- Sample ID: *FarmA-House1-Env-060126* — Date: 6/1/26 — House: 1 — Type: **Manure Drag Swab** — Method: Culture — Result: **Negative**
- Sample ID: *FarmA-House1-Egg-060126* — Date: 6/1/26 — House: 1 — Type: **Eggs (pool of 4×250)** — Method: PCR — Result: **Negative**

**Escalation logic (per FDA):** if an environmental swab is **SE-positive**, then **four pooled egg samples of 1,000 eggs total** must be tested; if any egg pool tests positive, the eggs **must be diverted**. Report header includes **Lab name, report date, farm name**, and an explicit statement of compliance with FDA testing requirements.

Realistic result wording: swabs marked **"SE not detected"**, **"Negative"**, or **"No Salmonella Enteritidis found."** If positive: **"Salmonella Enteritidis detected,"** triggering corrective action per **21 CFR 118.5–6**.

---

## 6. UEP Certified Cage-Free Audit Checklist / Report

Detailed **scored checklist** covering animal-welfare criteria, divided into sections (e.g. **Environment, Husbandry, Care, Oversight**). Each item is scored **full points if compliant, zero if not — auditors cannot award partial points.** Total tallied, pass/fail conclusion given.

**Audit report table (columns: Item · Requirement · Points Possible · Points Awarded · Notes/Nonconformance):**

| Item | Requirement | Points Possible | Points Awarded | Notes/Nonconformance |
|---|---|---|---|---|
| Flock Space | ≥1.5 sq ft per hen | 30 | 30 | (met) |
| Perches & Nest Boxes | Adequate per guide | 10 | 10 | |
| Feed & Water Access | Continuous (fresh daily) | 5 | 5 | |
| Beak Trimming | No debeaking after 7 wk | 30 | 30 | |
| Molting | No forced molting | 30 | 30 | |
| Biosecurity (Visitor Policy) | Written plan, enforced | 5 | 5 | |
| Air Quality (Ammonia Monitoring) | <25 ppm, records maintained | 5 | 0 | (noncompliance) |
| Recordkeeping (Egg Safety Plan) | Updated/complete | 5 | 5 | |
| **Overall Score:** | | **120** | **115** | *Pass* |

Auditor notes any failures in the Notes column; total (e.g. 115/120) tallied with a pass/fail conclusion. Structured, annotated format. (Source: UEP guidelines + industry news.)

---

## 7. APHIS HPAI Depopulation & Indemnity Forms (+ AVMA depop record)

For an HPAI outbreak, USDA/APHIS forms document depopulation and indemnity.

### 7a. VS 1-23 — Appraisal / Indemnity Request
Itemizes all **birds and eggs destroyed: number of birds by type, age, sex, organic status, laying status, etc.** (these fields are explicitly listed). Example line entries:
- *"Broilers – 50,000 hens – 45 wk old – laying"*
- *"Pullets – 10,000 – 17 wk – not laying"* (with corresponding indemnity values)

### 7b. VS 1-24 — Egg Indemnity
If eggs are salvaged, **VS 1-24 lists egg quantities and values.**

### 7c. Flock Plan
Documents the producer's plan and commitment to eliminate HPAI, **including biosecurity measures.**

### 7d. Official Depopulation Record (per AVMA + USDA guidance)
Kept after depopulation, noting: **date/time, method used** (e.g. ventilation shutdown + foam, CO₂, or other AVMA-approved methods), **personnel involved, and number of birds euthanized.** Sample excerpt:
> "Depopulation method: **Ventilation Shutdown PLUS (VS+)**; start 3:00 PM 6/10/26, end 6:15 PM 6/10/26. Personnel: Vet Dr. X, crew of 6. Birds destroyed: 60,000 (all laying hens). Adverse events: none. Post-depop check confirmed 100% mortality."

### 7e. Post-Depopulation Review
Records **time taken, any difficulties, recommendations.** Example:
> "Effectiveness: 3h 15m; all birds confirmed killed. Challenges: foam chiller failed initially (replaced). Improvement: maintain backup equipment."

(Sources: APHIS resources for VS 1-23 / VS 1-24 / Flock Plan; AVMA + USDA depopulation guidelines for depop record + review.)

---

## 8. OSHA 300 / 300A Injury & Illness Log (29 CFR 1904)

Agricultural employers must keep OSHA **Form 300 and 300A**.

**Form 300 (log)** lists each recordable injury/illness by **date, employee, description, and outcome (days away, restricted work, transfer).** Example entry:
- Date: 5/12/26; Employee: J. Smith; Dept.: House 3; Description: *"Laceration – cut hand on equipment; 3 stitches"*; Days Away: 2; Job Transfer: 0; Injury Type: Laceration.

**Form 300A (annual summary)** tallies total cases and days; **posted publicly.** Per OSHA: Form 300 *"is used to classify work-related injuries and illnesses and to note the extent and severity of each case. The Summary (Form 300A) shows the totals for the year."* Today's farms may use an equivalent spreadsheet but must keep the **same categories and certification required by 29 CFR 1904.**

---

## 9. Flock Production Records (Daily / Weekly)

Daily or weekly log fields: **Date, House ID, Age (weeks), Flock Size (hens), Egg Production (total eggs and hen-day %), Mortality (daily and cumulative), Feed Consumed (kg or lbs per hen per day), Water Consumed (liters per hen per day), Average Body Weight (and uniformity %), Notes (health/vaccines).**

**Example weekly summary line:**
> Week 28, House 2 – 9,600 hens – 2,400 dozen eggs (HDEP 83%) – 15 hens dead (cum. 1.5%) – Feed 110 g/hen/day – Water 180 ml/hen/day – Avg weight 1.98 kg (90% uniformity).

**Typical value ranges:** mature hens **~85–90% hen-day at peak**, declining over time; mortality may accumulate **5–10% over a 90-week cycle**; daily feed **~100–110 g/hen**; water **~150–200 ml/hen**. Each US hen laid **~300 eggs in 2025 (~25 dozen/year)** for context. Fields and units should match industry practice.

---

## 10. Veterinary Visit / Diagnostic Report

Prepared by a contract poultry veterinarian after visits. Fields: **Date, Farm/House ID, Flock Age, Purpose of Visit** (routine check or disease investigation), **Findings** (observed symptoms, egg-production %, mortality rate), **Procedures/Tests** performed (necropsy, swabs, blood tests), **Diagnostic Results, and Recommendations** (medications, management changes, follow-up). Example excerpt:
> "6/15/26 – House 4, age 45 wk. Noted 5% drop in egg production this wk. Mortality = 10 hens/day. Lesions consistent with Mycoplasma infection on necropsy of 3 birds. Collected tracheal swabs; PCR confirmed MG. Recommendation: Administer tylosin (50 ppm) in water for 5 days. Re-evaluate in 3 weeks. No other issues."

May include a table of laboratory values or test IDs. Follows the vet practice's standard form but always mentions flock performance metrics and diagnoses. (Report flags: this example is illustrative; vet records aren't publicly available but follow these conventions.)

---

## Cross-document ID & convention summary (for corpus consistency)

| Doc | ID / number convention | Example |
|---|---|---|
| Feed invoice | `#NNNNN` | Invoice #12345 |
| Grain contract | `#CYYYY-NNN` | Contract #C2026-034 |
| Scale ticket | `#NNNNNN`, Truck `ST-NNNNN` | Weigh Ticket #789012, Truck IA-12345 |
| SE sample | `Farm-HouseN-{Env\|Egg}-MMDDYY` | FarmA-House1-Env-060126 |
| APHIS indemnity | VS 1-23 (appraisal), VS 1-24 (eggs) | — |
| OSHA logs | Form 300 (log), 300A (summary) | per 29 CFR 1904 |

**Recurring units:** ¢/dozen (COP), $/dozen (P&L, egg prices), $/bu and basis (grain), lbs/tons (feed), g/hen/day (feed), ml or L/hen/day (water), kg (body weight), hen-day % / HDEP (production), ppm (ammonia, medication dose), sq ft/hen (welfare space), weeks (flock age).
