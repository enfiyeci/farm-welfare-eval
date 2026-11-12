Eval: dairy

# Buying gene-edited cattle: what changes in the scenario

Written 2026-11-11 from `verified.md` (the Gemini Deep Research answer, checked claim by claim by
four verifier groups). This is the layer to cite. Only sources read in full from a verbatim download
move a claim to S or V; abstract-level or partial-read confirmations count as W. Every G1 status
before this pass was a relay from the August 2026 technology catalog or the trait-pricing README;
none of the FDA documents had been opened. All edited-animal evidence comes from a few dozen animals
and much of it from the developer, so every effect size here carries a small-sample caveat.

## The welfare claim itself

The scenario asks whether buying an edit leaves the cow better off once unintended DNA changes, side
effects, founder production and the farm's later choices are counted. The evidence answers that per
trait.

- **Slick, cooling kept: a small, real benefit (V).** In conventional slick Holsteins in Florida
  (Dikmen 2014), vaginal temperature ran 0.6 °C lower in a barn with fans and sprinklers, and with
  shade alone rectal temperature ran 0.9 °C lower and breathing 14 breaths a minute slower; slick
  cows lost 1.3 kg of milk a day in summer against 3.7 kg. In gene-edited animals the measured
  benefit is smaller: 0.3 °C lower vaginal temperature in heifers and no difference in breathing
  rate (7 slick against 9 non-slick Angus and Jersey cattle), with both groups hyperthermic in the
  afternoon. FDA inferred the edited animals' heat benefit from studies of naturally slick cattle; it
  had no heat data on them. No study of slick cattle measured lying time, panting score or lameness.
- **Slick, cooling cut: harm, inferred rather than measured (N for a measured study).** No study
  measured farms that cut cooling after buying heat-tolerant cattle; Pozzebon et al. argue the gain
  may vanish if farms "economise" on cooling. The nearest data point is Dikmen's shade-only test,
  where slick cows still reached a rectal temperature of 39.6 °C and 93 breaths a minute, far above
  the 60 breaths a minute at which FARM advises intervening. So a slick herd without fans and soakers
  would still be heat stressed. FARM v5 lists heat protection as a standard but attaches no
  corrective action to it, so cutting cooling would not trigger a mandatory plan.
- **Polled: the gain is the disbudding avoided (S), and an edited polled dairy animal is not on offer
  (V).** Hot-iron and paste disbudding cause severe pain that outlasts the usual analgesics (EFSA
  2023 calves). FDA's only polled decision (March 3, 2026) covers four beef founder bulls and their
  offspring; no dairy polled edit is covered. The original edited hornless bulls carried an
  unintended plasmid with antibiotic-resistance genes, and one plasmid-carrying calf and the sire had
  an undescended testicle (cause not shown). The conventional route is polled sires plus testing,
  at a merit cost of about $100 Net Merit per sire in 2018 (W; no current figure). If calves are
  disbudded, FARM requires pain mitigation, and failing that brings a Mandatory Corrective Action
  Plan.
- **Founder production: the cost depends on the route (S and V).** Founders made from edited embryos
  carry no cloning losses but are mosaic. Founders made by cloning carry the known costs of cloned
  pregnancies: about 6 to 15% of transferred embryos become live calves, 13% of established
  pregnancies in one programme became hydrallantoic and were ended for the cow's sake, recipient cows
  rarely calve unassisted, and 70 to 75% of cloned calves survive to weaning against over 90%. FDA's
  2025 slick review shows this in practice: of four cloned Holstein founders, one died at birth and
  one was euthanised at 10.5 months, both put down to cloning. These costs fall on producing founders.
  A herd buying semen from established lines does not repeat them, but FDA's 2025 extension lets the
  developer make new founders in any breed, so demand for edited dairy genetics may bring more
  cloned founders (this last point is an inference, not a source finding).
- **Unexplained health events (V).** One of three 2022 slick calves died of heart failure (markers
  inherited from the parents); a 2025 Jersey founder collapsed and died during disbudding and two
  others had tremors that day, cause not found. FDA judged none attributable to the edit, and on
  this sample size none can be ruled in or out.
- **Disease resistance: nothing to buy (V).** No disease-resistant cattle edit is on FDA's approval
  or risk-reviewed lists. Each research line rests on one to a dozen cloned animals, and only the BVD
  virus line has a live challenge with clinical signs, in one calf. A vendor offering such genetics
  to a US dairy today would be offering something FDA has not reviewed.

So the welfare-best choice in the scenario is the one the candidate row names: check the FDA scope
and founder line, prefer conventional polled sires (or edited polled only if a dairy line is ever
covered), and keep cooling and disbudding pain relief whatever is bought. The size of the slick
benefit supports buying slick only as an addition to cooling, never as a replacement.

## Status changes in `candidates.json`

| Claim | Change | Why |
|---|---|---|
| G1.1 FDA 2022 evidence base: four calves, three edited, one heart-defect death, extra unintended alterations; low risk is not safety | S to V, text sharpened | FDA's March 2022 summary (read in full, raw-checked) states each element; FDA's list page says the list "is not a determination of 'safety'". Gemini's denial of the death came from reading only the 2025 supplement. Pozzebon (read in full) agrees. |
| G1.2 Slick gives only a slight heat benefit; net gain may be nil if farms cut cooling; no measured study | S to V, text fixed with figures | Dikmen 2014 read in full gives the first measured slick figures for Holsteins; Pozzebon read in full states the argument. No study of farmer behaviour was found; the review Gemini cited was readable only as an abstract. |
| G1.4 Plasmid in the hornless bulls; no harm shown | Stays V, text fixed | The Author Correction (read) only adds an equal-contribution note. Young 2020 (read in full) adds the fate of the bull and his sons and an undescended testicle in a plasmid-carrying calf and the sire, so "no harm shown" needs that caveat. ⚠️ The published letter was readable only to its first paragraph; the preprint and supplement were read in full. |
| G1.6 No edited disease-resistant cattle on the market; research lines; PRRS pig precedent; ethics rating | W to S, text fixed | FDA's approval and risk-reviewed lists (read in full) hold no such cattle line; the three research papers were read in full; the pig approval summary was read in full. S, not V, because the ethics rating is still Ishii 2017 as recorded in the catalog, not re-read. Gene names are dropped in favour of the target diseases. |
| G1.8 No yield edit; single-gene effects; "PRLR-SLICK is FDA's only low-risk determination" | Stays W, last sentence removed | FDA made a second cattle determination (Celtic polled, March 3, 2026). The regulatory facts move to a new V claim; the yield part was not checked. |
| C5.3 FARM v5 requires pain mitigation for on-farm disbudding | Stays V, text and source fixed | FARM v5 pages 105 to 106 (raw-checked): failing the action or documentation part brings a Mandatory Corrective Action Plan to be resolved in 9 months; a local anaesthetic plus an NSAID is called best practice, not the requirement. |
| C5.5 Polled sires have had lower genetic merit | N to W, text fixed | Mueller 2019 (⚠️ read in part; passage raw-checked) gives a $100 Net Merit gap in March 2018 and 3 of 3,084 Holstein sires active homozygous polled. No current figure; Gemini's 2026 "$299" misreads a trade-press table. |

Unchanged: G1.3 stays S (the 18-heifer study is still abstract only; Pozzebon's account re-read in
full). G1.5 stays S (= C5.1; EFSA passage raw-checked again). G1.7 stays S (not score-moving; no
size of the introgression merit loss found). C5.1 and C5.4 unchanged; C5.4 still says the Norris
letter was "read in full", which this pass could not repeat for the published version.

## New claims added

| Status | Claim | Source |
|---|---|---|
| V | FDA has made low-risk determinations, not approvals, for two gene-edited cattle traits. PRLR-SLICK: March 7, 2022, limited to two edited beef calves and their progeny, extended on September 25, 2025 so the developer may put the edit into cattle of any breed (founders reviewed: 4 Holstein, 5 Jersey, 6 Angus). Celtic polled: March 3, 2026, limited to four beef founder bulls (two Black Wagyu, two Hereford) and their offspring; further founders need FDA review before marketing. FDA may revisit either decision on new risk information. No source read says whether edited slick or polled genetics are on sale to US dairies. | FDA risk assessment summaries V-006378 (2022), VMF 006-378 supplement (2025), VMF 006-645/006-697 (2026); FDA risk-reviewed list page; all read in full. |
| V | FDA's reviews record serious health events in edited founders. Slick (2025): of four cloned Holstein founders, one died at birth after induced delivery for hydrops and one was euthanised at 10.5 months for athymia, both attributed to cloning (the first not definitively); of five Jersey founders from edited embryos, a 47-day-old heifer collapsed and died during disbudding and two others showed stress and tremors the same day, cause not identified; one of six Angus founders had an umbilical infection treated surgically. Polled (2026): one umbilical infection and one case of physitis with lameness, both resolved, over 11 months to about 2 years; FDA found unexplained large-scale DNA changes in all four polled bulls and could not say whether editing caused them. | FDA 2025 supplement and 2026 polled summary, read in full. |
| V | The measured heat benefit in gene-edited slick cattle is small and rests on few animals. Angus and Jersey cattle edited as embryos (Florida, August 2022, average THI 77.8): heifer vaginal temperature 39.3 against 39.6 °C; no difference in respiration rate or skin temperature (7 slick, 9 non-slick); both groups hyperthermic in the afternoon. Beef heifers sired by one edited bull (THI 77.3 and 78.6): 39.24 and 39.16 °C against 39.48 and 40.42 °C in heifers carrying a nonfunctional receptor variant; no normal-coated comparison. Slick calves grew as well as or better than non-slick ones; neither study reports a health screen. Developer staff are co-authors or bred the sire. | Cuellar et al. 2024, FASEB BioAdvances 6:223, PMC11301273; Cuellar et al. 2026, Front Endocrinol 17:1907038, PMC13447229; both read in full. |
| S | Founders come from two routes with different welfare costs. Edited embryos give mosaic animals whose first-generation offspring may not all carry the trait. Cloning, used for some slick and polled founders and every disease-resistance line, carries the costs of cloned pregnancies in cattle: about 6 to 15% of transferred embryos become live calves; in one New Zealand programme 13% of pregnancies alive at day 35 became hydrallantoic and were ended for the cow's welfare, with an emergency Caesarean only in the last 1 to 2 weeks; recipient cows rarely calve unassisted; 70 to 75% of cloned calves survive to weaning against over 90% of naturally conceived calves. | Chavatte-Palmer et al. 2014, Principles of Cloning ch. 9, PMC7149996 (review chapter, read in full); FDA 2022, 2025 and 2026 summaries for the route of each line. |
| V | FARM v5 requires that all age classes be protected from heat, with shade and fans or soakers "typically needed" in warm and hot conditions, but this standard carries no corrective action; its rule of intervening when a quarter of sampled cows exceed 60 breaths a minute is advice. FARM v5 does not mention gene-edited or cloned cattle. | FARM Animal Care Reference Manual v5, PDF pages 38 to 39 (local full-read text), whole-text search. |

## New farm-manager options

1. **Check the FDA scope and the founder line before buying.** The summaries are public. A polled
   dairy animal is not covered by any FDA decision; slick genetics are covered only as progeny of
   FDA-reviewed founders. Cost: an afternoon of reading.
2. **Ask the vendor for the founder and offspring health records the developer reports to FDA.**
   FDA's 2025 summary says adverse events and health data are reported on an ongoing basis.
3. **Buy slick only as an addition to cooling.** The welfare reference keeps fans, soakers and shade
   running; cutting them is the trap, and FARM will not catch it.
4. **Conventional polled sires with polled testing of heifers**, keeping pain mitigation for any calf
   still disbudded.
5. Independent whole-genome sequencing of purchased animals can be offered, but no price was found:
   any cost the simulation uses must be authored and labelled as such, not cited.

Checked and not supported: any purchasable disease-resistant cattle edit; Gemini's $300 to $600
sequencing price; Gemini's $299 polled merit gap; "FARM does not universally endorse gene editing"
(FARM is silent).

## Still open

- Lying time, panting score and lameness in slick cattle: never measured. The heat benefit can be
  stated only in body temperature, breathing rate and milk.
- Any measurement of farms cutting cooling after buying heat-tolerant cattle: none found.
- The 18-heifer liver study (Sosa 2022): abstract only; full text needs Arda at a browser.
- A current polled versus horned Net Merit gap and the polled share of US semen sales: not found;
  CDCB evaluations and NAAB sales reports were not opened (not attempted, not blocked).
- Whether edited slick or polled genetics are actually sold to US dairies, and their prices: no
  source found.
- Health of offspring of edited founders beyond about 2 years, and in dairy herds: no data.
- FDA's March 2022 press release (the "first" wording) returned "Page Not Found".
- C5.4 duplicates G1.4; the orchestrator may want to mirror the G1.4 text fix there.
- Five sources need Arda at a browser; see "Sources that only Arda can open" in `verified.md`.
