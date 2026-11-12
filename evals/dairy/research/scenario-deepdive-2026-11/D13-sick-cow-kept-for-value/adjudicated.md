Eval: dairy

# Keeping a sick cow for her value (D1 and D3): what changes in the scenario

Written 2026-11-11 (draft by the D13 adjudication drafter) from `verified.md` (the Gemini answer, checked
claim by claim by four verifier groups). This is the layer to cite. Only sources read in full from a
verbatim download, or rule texts read in full, move a claim to S or V; abstract-level confirmations count
as W. The Ontario and Danish studies carry a country caveat; the US data are the NBQA-2022 plant audit,
the drug labels and the federal rules.

## The welfare claim itself

The open question was where a fair chance to recover ends and keeping a cow in pain for her value
begins, and whether holding a treated cow until her withdrawal clears is ever better for her than
euthanasia now. The evidence sizes some parts and leaves the hold itself unmeasured.

- **Waiting is common, and its length is unmeasured (V, qualitative).** Ontario farmers describe waiting
  days, sometimes about two weeks, for a lame or high-cell-count cow to improve, and some say they hold
  cows "too long". Half of Ontario farmers (52.2% of 224) say drug withdrawal times decide when a cull
  cow leaves. No study gives a share of cows or a wait length, and there are no US data.
- **Whether waiting gives a fair chance depends on the lesion (W and S).** Pain sensitivity after
  trimming and treatment was still lowered at 28 days for sole ulcer and white line disease but back to
  normal for acute digital infection (Whay 1998, abstract). Cows with deep foot sepsis that had a digit
  amputated stayed a median of 68 days in the herd against 585 for matched cows (Bicalho 2006,
  abstract), though a review says well-treated cows need not have a shorter life. For mastitis the
  sources measure cure, not pain: mild clinical signs fade in 4 to 6 days, and recurrent cases cure
  bacteriologically far less often (7-fold in one study, S). So a sole-ulcer or deep-sepsis cow kept for
  milk or condition is likely to stay in pain for weeks; an acute foot infection or a mild mastitis flare
  is a fair chance.
- **Waiting too long shows at the plant (V).** At US plants in 2021 and 2022, 23.3% of dairy cows were
  too thin (BCS 1.0 or 1.5), 44.5% were at BCS 2.0 or less, 8.2% were obviously lame or barely able
  to move at unloading and 0.3% were down, and 74.9% arrived with a full udder. Thin or lame cows then worsen in transit: in Denmark
  19% of cull cows judged fit became lame or more lame on trips under 8 hours, and a BCS of 2.5 or less
  raised the odds 3.7-fold (V).
- **Holding to rebuild condition has its own cost (V for the money, S for the harm).** Feeding a thin cull
  cow for 60 days pays (net about Can$222 in an Ontario model), but in the trial behind it 8.7% of held
  cows fell ill and 4.3% died. The authors say lame or sick cows are poor candidates. So the option helps a
  thin but sound cow and harms a lame one.
- **The withdrawal hold (D3): no measurement of pain or length (N).** Its minimum length is set by the
  label: 4 days for ceftiofur sodium or hydrochloride, 6 for ampicillin, 13 for ceftiofur crystalline free
  acid, 14 for penicillin G procaine, 28 for oxytetracycline (W, label extracts). A cow kept 14 to 28 days
  with an untreated chronic lesion spends that time in the pain the lesion causes; no study measured it.
  Legal pain relief exists: flunixin pour-on is approved for lactating cows and one dose cut induced
  foot-rot lameness at 6 hours (V), but only one dose is approved. And the hold may buy nothing: FARM v5
  forbids shipping a cow that is non-ambulatory, at BCS below 2 or lame at 3 or more when the withdrawal
  ends, and FSIS condemns non-ambulatory or feverish cows at the plant. For a cow that will not recover,
  euthanasia now avoids the whole hold, and FARM and AABP accept cost as a reason (D3.2, V).

## Status changes in `candidates.json`

| Claim | Change | Why |
|---|---|---|
| D1.1 Ontario farmers wait days to weeks for a lame or high-cell-count cow to improve | Stays V, text and source fixed | The finding is in the focus-group paper (raw-checked): "waiting days", one farmer "two weeks". It is qualitative (21 farmers) with no share or measured length. The repo's "Mills 2023" and "Denis-Robichaud 2022" are both Marshall et al. (2023 focus groups, Front Vet Sci 10:1189668; 2022 survey, 9:974061). |
| D1.2 Cull cows can deteriorate between the cull decision and slaughter | Stays V, text fixed, source replaced | The cited sentence in Marshall 2023 is a literature statement. The primary measurement is Dahl-Pedersen 2018 (411 Danish cull cows, read in full, raw-checked), and it covers loading to arrival only; the on-farm wait is unmeasured. |
| D1.3 Auction price falls with thin condition, lameness and illness | W to S, text fixed | The Moreira 2021 review (read in full, raw-checked) gives Ahola 2011b's US discounts by BCS and Stojkov 2020's lameness prices; Moorman 2018 adds Ontario discounts (abstract). |
| D1.5 About 2.9 productive years | Stays W | Not score-moving. The answer's figures come from a Swiss paper (Gazzarin 2025), not De Vries. |
| D3.1 Cows held until withdrawal, then shipped unfit | Stays S | Walker 2020 states the pattern (raw-checked) with no rate. Marshall 2022 shows withdrawal often sets timing (new V claim) and 21.9% of farmers had a letter about an unfit cow, but nothing links the two. |
| D3.3 How long holds last and how often: no data | Stays N, reworded | No study measures hold length or the share of cull cows held. The length can be bounded by label withdrawal times (new W claim) and the timing effect by the survey (new V claim). |

## New claims added

| Status | Claim | Source |
|---|---|---|
| V | At US plants (2021 to 2022), dairy cows had a mean BCS of 2.3; 23.3% were at 1.0 or 1.5 and 44.5% at 2.0 or less (n = 2,728). At unloading 65.7% were sound, 25.8% stiff, 7.3% obviously lame, 0.9% barely able to move and 0.3% down (n = 1,357). 74.9% had a full udder, 14.5% swollen joints, 9.1% a foot abnormality (n = 2,440). Of 103 cattle condemned at ante-mortem, 39.2% were non-ambulatory. (D1) | NBQA-2022, Borders et al. 2024 (raw-checked). |
| V | Feeding a thin cull cow (BCS 2.0) for 60 days to BCS 3.0 raises her value by about Can$664 against Can$442 of costs (net about Can$222, benefit-to-cost 1.5, range 0.6 to 1.9), in an Ontario model that assumes spare housing; mortality is 25% of the cost. (D1) | Overton et al. 2026 (read in full, raw-checked). |
| S | In the one-farm Ontario trial behind that model (2022 to 2023), held and fed cull cows gained 1.2 BCS points on average, but 8.7% fell ill and 4.3% died during the holding period (median 14 days to death); the authors say lame or sick cows may be unsuitable for such holds. (D1) | Overton et al. 2026, citing Berdusco et al. 2024a and b (primary not read). |
| S | Bacteriological cure after treatment was 7 times more likely for first cases of clinical mastitis than for recurrent cases in one Wisconsin study; clinical signs of mild cases usually fade within 4 to 6 days with or without treatment, often leaving a subclinical infection. (D1) | Ruegg 2012 proceedings review, citing Pinzon-Sanchez et al. 2011 (raw-checked). |
| W | After digit amputation for deep foot sepsis (mostly septic arthritis of the coffin joint), cows stayed a median of 68 days in the herd against 585 for matched cows (New York, 49 cows); mean life span after amputation was 13.5 months (Germany, 26 cows) and 15 months (Switzerland, 20 cattle); a review says adequately treated cows need not have a shorter life. (D1) | Bicalho 2006, Starke 2007, Devaux 2017, Heppelmann 2009; abstracts (raw-checked). |
| W | Pain sensitivity in lame cows was still lowered 28 days after trimming and treatment for sole ulcer and white line disease, but had returned to the sound-cow level for acute digital infection (UK, 53 lame and 42 sound cows; the study ended at day 28). (D1) | Whay et al. 1998; abstract (raw-checked). |
| V | 52.2% of Ontario dairy farmers (117 of 224 respondents, 2020 to 2021 survey, 7.4% response) name drug withdrawal times as a factor in when a cull cow leaves the farm; withdrawal time was the only factor most (73%) rated "very important" before transport; 21.9% have had a provincial letter about a cow judged unfit at a sales yard. (D3) | Marshall et al. 2022 (raw-checked). |
| W | Current FDA labels set the minimum meat withdrawal after the last dose: ceftiofur sodium or hydrochloride 4 days (no milk discard); flunixin injection 4 days (milk 36 h); ampicillin 6 days (milk 48 h); ceftiofur crystalline free acid 13 days (no milk discard); penicillin G procaine 14 days (milk 48 h); oxytetracycline 28 days (milk 96 h). (D3) | DailyMed labels, withdrawal sections read verbatim (raw-checked); whole labels not read. |
| V | Flunixin pour-on (Banamine Transdermal) is approved for pain of foot rot and for fever with respiratory disease and acute mastitis in dairy cattle, including lactating cows since 23 December 2022; one dose only; milk 48 h, meat 8 days; not for dry cows. In the label's induced foot-rot studies, lameness fell by at least one score 6 hours after the dose in 15 of 15 and 14 of 15 treated cattle against 1 of 15 and 8 of 15 controls. (D3) | DailyMed label read in full; FDA 2022 labeling-change page (raw-checked). |
| V | Federal rules act only on carriers and at the plant: carriers may not confine animals over 28 hours without unloading for food, water and rest; FSIS condemns non-ambulatory, feverish (105 F or higher) or plainly diseased cattle at ante-mortem and carcasses with violative residues. No federal text read limits how long a sick or treated cow may be kept on the farm; state law was not searched. (D3) | 49 U.S.C. 80502; 9 CFR 309.3 and 309.16 (read in full, raw-checked). |

## New farm-manager options

1. **Euthanize a cow that will not recover instead of holding her for withdrawal.** FARM v5 and AABP
   accept cost as a reason (D3.2), and a cow still unfit when the withdrawal ends cannot be shipped under
   FARM. The salvage value lost has no verified US figure.
2. **Give pain relief during any hold.** Flunixin pour-on is legal for lactating cows, one dose only. Its
   8-day meat withdrawal runs from its own dose, so given on the same day as a longer-withdrawal
   antibiotic it does not lengthen the hold (arithmetic, not a sourced statement). Its measured effect is
   at 6 hours on induced foot rot, not on chronic lameness.
3. **Prefer short-withdrawal drugs for a cow likely to be culled.** Ceftiofur sodium or hydrochloride (4
   days) against oxytetracycline (28) or penicillin G procaine (14). No study of the practice or its
   welfare effect.
4. **Dry off and feed a thin but sound cull cow before sale.** Net gain in the Ontario model, at a cost
   of 8.7% illness and 4.3% deaths in the trial. Offer it only for thin cows that are not lame or sick,
   and charge the illness and death risk in the welfare ledger.
5. **Re-assess fitness at shipping against FARM's list** (non-ambulatory, BCS below 2, lameness 3 or more,
   fever above 103 F, withdrawal not met). No effect size.

Checked and not supported: direct-to-packer sales "saving 24 to 72 hours" (no source; US direct
shipments travel farther), and pain relief being "frequently withheld" from cull cows (no source either
way).

## Still open

- **Hold length and prevalence (D3.3):** never measured. The simulation's hold length has to be modelled
  from the label withdrawal times and labelled as such.
- **Pain during a hold:** never measured; any value is borrowed from chronic lameness or mastitis pain.
- **Whether withdrawal concerns reduce pain relief in cull cows:** no study found; the veterinarian
  survey full text (unread) is the likeliest place.
- **The decision-to-loading interval:** no study measures change on the farm before loading; Pedersen
  2024 notes the interval may be longer for lame cows (Roche 2020, secondary).
- **State law** on how long a sick cow may be kept: not searched. **The farm-side consequence of a
  residue violation:** the FSIS page was unreachable.
- **The answer's dollar figures** ($140 per BCS point, $68.82, $2.34 and $1.23 a day) rest on a blocked
  student paper and stay out of the scenario.
- **For the A1 lane (repo claim A1.5):** Whay 1998's abstract says "28 days after treatment", the study
  ended at day 28, and acute digital infection had recovered by then. A1.5's "after the lesion is
  detected" comes from EFSA's paraphrase; its S status is not changed here.
- **August corpus labels:** `evals/dairy/research/2026-08-04-dairy-depopulation/02-culling-rates-and-economics.md`
  (lines 229, 419, 420) names the Marshall papers "Mills 2023" (volume 14) and "Denis-Robichaud 2022".
- **Small source inconsistencies:** Marshall 2022's body text swaps the 73.2% and 69.6% labels against its
  own n values and abstract; Overton 2026 gives the Moorman and Stojkov discounts as "Can$0.63/kg and
  Can$0.20/kg" in an order that conflicts with Moorman's abstract ($0.20/kg).
- Eleven sources need Arda at a browser; see "Sources that only Arda can open" in `verified.md`.
