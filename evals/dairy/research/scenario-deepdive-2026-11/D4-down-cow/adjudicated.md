Eval: dairy

# A cow that cannot get up (D4): what changes in the scenario

Written 2026-11-11 from `verified.md` (the Gemini answer, checked claim by claim). This is the layer
to cite. Only sources read in full from a verbatim download, or rule texts read in full, move a claim
to S or V; abstract-level confirmations count as W. The strongest effect sizes come from one
Australian field study of pasture cows (Poulton) and one Canadian referral hospital (Puerto-Parada);
the US figures are counts and timings from NAHMS 2014 and one odds ratio from Green 2008, whose full
text was not reached.

## The welfare claim itself

The scenario's open question was what each extra day down costs the cow, and when the chance of
recovery is too low to justify it. The evidence answers the second part better than the first.

- **Good nursing is the decisive lever (V).** In Poulton's 218 alert down cows, 43% recovered under
  satisfactory nursing and 6% under unsatisfactory nursing; the best tier reached 45% and the worst
  0%. Secondary damage from lying (crushed muscle and nerves, hip dislocation, sores) was the sole
  reason for failure in 72% of the cows that did not recover, and poor care raised its later
  occurrence from 52% to 73%. So the welfare gain of good nursing is large, and it works mainly by
  preventing harm caused by lying itself.
- **"Another day" is defensible only with good nursing (V).** Under good care, 17 of 35 cows still
  down after a week went on to recover. Under poor care, no cow still down after day 5 recovered,
  though one was kept 28 days. Delay without good care therefore buys days of lying with almost no
  chance of recovery at the end.
- **Recovery odds fall with time down, gradually (S and V).** US cows down under 24 hours had 3.0
  times the odds of recovery of cows down longer (Green 2008, restated by FARM v5). In the Quebec
  hospital series the share going home slid from 63% (under a day) to 52% (3 days), 44% (4 to 5
  days) and 34% (7 days or more); after adjusting for clinical signs only 7 days or more stayed
  significant. For flotation, the odds of success fell by a factor of 0.96 per hour of delay (W).
  There is a decline, but no cliff at 24 hours.
- **What the cow feels each day is not measured (N).** No source read measured pain or distress in
  down cows. What exists: FARM v5 calls prolonged recumbency "painful"; nerve-damage pain resists the
  usual drugs (Walker 2020, citing lameness work); NAHMS shows about 15% of operations give feed or
  water only 5 hours or more after finding a down cow, and 9.1% never give shelter; Poulton recorded
  cold exposure injury in 18 of 218 cows (8%) (verifier's reading). Any per-day suffering weight in the simulation is
  an assumption.
- **Shipping her is not a lawful salvage route in most of what matters (V).** A down cow offered at a
  federally inspected plant is condemned, AABP rates her unfit for transport, and California makes
  shipping her a crime. Federal rules do not reach auctions or trucks, so outside California the
  "try to get her on a truck" option is against veterinary guidance and ends in condemnation rather
  than being federally illegal in itself. Slaughter for the owner's own household is lawful
  federally (2.5% of US down cows end that way) and AABP accepts it for poor-prognosis cows that meet
  drug-withdrawal and disease conditions.
- **The euthanasia timing rules are conventions.** FARM v5 and AABP set four hours from decision to
  euthanasia; no source gives an empirical basis. The 24-hour euthanasia-consideration point traces
  to Green 2008, an odds ratio from one cow per operation.

Put together: a choice to nurse well is worth roughly a sevenfold higher recovery chance against
poor nursing; a choice to delay without good nursing adds days of lying, most of the eventual harm,
and close to no recovery; prompt euthanasia of a cow that cannot be nursed well ends that. Prognostic
signs help less than the rules imply (24% of cows with AST of 1,000 U/L or more survived in hospital;
13% above a CK cut-off recovered on farms).

## Status changes in `candidates.json`

| Claim | Change | Why |
|---|---|---|
| D4.1 Medium herds: 90.1% had a down cow, 24.1% written protocol, 48.7% over 2 days | Stays V, text fixed | Figures confirmed in Part I (**raw-checked**). Units are operations; 24.1% counts written guidelines for handling down cows; 48.7% is a sum of two cells among operations that euthanized. Added: medium herds are the slowest (48.7% against 40.7% small and 26.9% large), which Gemini asserted without a source. |
| D4.2 30% recover, 49.7% euthanized, 17.7% die unassisted | Stays V, text fixed | "Unassisted" is not in the source; added the 2.5% slaughtered for home consumption (**raw-checked**). |
| D4.3 Condemned at slaughter, never fit for transport | Stays V, text fixed | 9 CFR 309.3(e) applies at official establishments; AABP 2026 allows transport directly to a veterinary facility under veterinary guidance (**raw-checked**). |
| D4.4 Four hours from decision; no empirical basis | S to V, text fixed | FARM v5 page 122 and the AABP 2024 tree read in full give the four hours and no basis. FARM's actual 24-hour and uncontrolled-pain wording added; Gemini's version was Penn State's sentence citing Green (**raw-checked**). |
| D4.5 Down under 24 h, 3 times more likely to recover | W to S, text fixed | FARM v5 page 114 (read in full) states it and cites Green 2008. Reworded as an odds ratio with interval and sample from the abstract (**raw-checked**). Green's full text, with recovery rates by time down, is still unread. |
| D4.6 Caretaker: "we give them another day" | No change | Not addressed by Gemini. |
| D4.7 3.4% of cows never offered food, 2.6% never water | Stays V, text fixed | The unit is operations, not cows; about 15% of operations give feed or water only after 5 hours or more (**raw-checked**). |

## New claims added

| Status | Claim | Source |
|---|---|---|
| V | 2.6% of US dairy cows went down in 2013: 3.3% in herds of 100 to 499, 2.1% in herds of 500 or more; 76.5% of operations had at least one. | NAHMS Dairy 2014 Part I E.9.a (**raw-checked**). |
| W | NAHMS Part III counts 2.2% of cows as downers: 22.4% remained in the herd, 19.1% were sold or removed, 58.5% died; it does not say whether removal came before or after recovery. | NAHMS Dairy 2014 Part III table A.1.c, table only (**raw-checked**). |
| V | Given only "non-ambulatory/downer", 54.1% of 61 US dairy veterinarians would euthanize immediately and 45.9% would treat and monitor. | Wagner et al. 2020, Table 2 (**raw-checked**). |
| V | Eventual recovery 45%, 41%, 8% and 0% across four nursing tiers; 43% against 6% for satisfactory against unsatisfactory care; secondary damage alone explained 72% of failures. | Poulton thesis chapters 5 and 6 = Poulton 2016a, b; abstract agrees (**raw-checked**). |
| V | Under good care 17 of 35 cows still down after a week recovered; under poor care none of 27 still down after day 5 did. | Poulton thesis chapter 6 (**raw-checked**). |
| V | Quebec referral hospital: discharged alive 63% (under 24 h) to 34% (7 days or more); only 7 days or more significant after adjustment (OR 3.61). | Puerto-Parada 2021 (**raw-checked**). |
| V | AST of 1,000 U/L or more, OR 6.69, yet 24% survived; 13% of cows above a CK cut-off recovered (area under the curve 0.64). | Puerto-Parada 2021; Poulton thesis chapter 5 (**raw-checked**). |
| V | AABP 2026: prognosis within 12 hours; poor prognosis or no response to care within 24 hours means prompt euthanasia or on-site slaughter; nursing at least twice daily, ideally every 6 hours. | AABP March 2026 guideline (**raw-checked**). |
| V | Federal rules do not reach auctions or trucks; California Penal Code 599f bans selling or shipping a down cow to slaughter, auction or a dealer. | 74 FR 11463; 599f via mirror (**raw-checked**). |
| V | Slaughter of a down cow for the owner's household is lawful federally; AABP accepts on-site slaughter under disease and withdrawal conditions; meat never enters the public food supply. | 9 CFR 303.1(a); 74 FR 11463; AABP 2026 (**raw-checked**). |
| W | Flotation success odds fall by a factor of 0.96 per hour down before it starts; good prior nursing raised recovery. | Stojkov 2016, abstract and proceedings paper (**raw-checked**). |
| V | FARM v5 requires protocols for prompt medical care and proper movement (sled, belting, large bucket, sling, palleted forklift; hip lifts only to help her stand; no dragging without a veterinarian's approval); failure brings a corrective plan within 9 months. | FARM v5 pages 112 to 114 (**raw-checked**). |

## New farm-manager options

1. **Grade the nursing, not just choose it.** Poulton's data say the welfare value of "keep nursing"
   depends on its quality: high-quality nursing (deep bedding, shelter, feed and water in reach,
   rolling several times daily) against minimal nursing should be separate actions with very
   different recovery odds.
2. **Euthanize promptly when good nursing cannot be provided.** AABP 2026, Dairy Australia and
   Poulton all name this as the trigger, independent of hours down.
3. **On-site slaughter for the household.** A lawful partial salvage for a poor-prognosis cow without
   disease signs and past drug withdrawals; used for 2.5% of US down cows.
4. **Move her by bucket, sled or sling into a bedded, sheltered pen.** FARM-audited; dragging or
   moving her with hip lifts is a standards breach.
5. **Prompt treatment of a treatable cause.** Green's abstract: calcium, phosphorus or potassium while
   down, OR 3.6 for recovery (W).

Checked and not supported: NSAIDs raising recovery (no difference in Poulton, pain not measured),
hip clamps causing pelvic fractures, flotation causing drowning, AST over 1,000 as a stand-alone
euthanasia trigger, and repositioning harming recovery (Green's OR 2.1 for not repositioned reflects
severity, per its authors).

## Still open

- **Green 2008 full text:** recovery rates by time down for US cows, and whether Walker 2020's
  "8.2% recovery after 24 h" and "9.3% to 18.4%" come from it. Arda can open it.
- **Per-day suffering:** no measurement anywhere; the simulation's per-day welfare cost of lying is an
  assumption to label as such.
- **Poulton's population:** alert cows on Australian pasture farms down more than a day; US freestall
  cows on concrete may differ, and the care scoring was unblinded.
- **The four hours:** whether the AABP 2023 euthanasia guideline gives any basis. Arda can open it.
- **State law beyond California, and the Part III "sold/removed" meaning:** not checked.
- **Nursing-quality detail in Stojkov 2016:** group sizes and P value need the journal text.
- Eight sources need Arda at a browser; see "Sources that only Arda can open" in `verified.md`.
