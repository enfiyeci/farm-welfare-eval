Eval: dairy

# Finding and treating lame cows: what changes in the scenario

Written 2026-11-11 from `verified.md` (the Gemini answer, checked claim by claim). This is the layer
to cite. Only checks re-run against raw source text, or sources read in full, move a claim to S or V;
abstract-level confirmations count as W. Most treatment evidence is from UK trials on newly and
mildly lame cows; no US trial of treatment timing was found.

## The welfare claim itself

The scenario turns on one contrast: score the herd and treat new cases within days, or treat only
the cows that look obviously lame at the trimmer's next routine visit. The evidence on its size
splits into four parts.

- **Most lame cows go unnoticed (V for Australia, W for the US).** Farmers on 50 Australian pasture
  farms had found about 24% of the cows that trained scorers called lame, though every very lame cow
  was already found (Beggs 2019). In US herds, managers' estimates ran 2.5 to 3.1 times below scored
  prevalence (Wells 1993, Espejo 2006; abstracts). So the "treat the obvious ones" option leaves
  most mild and moderate cases untreated until they worsen or meet the trimmer.
- **Early treatment helps the treated cow (W).** Two UK trials with fortnightly scoring compared
  trimming within 48 hours of a cow first scoring lame with the farmers' usual approach. In
  Groenevelt 2014, 41% of early-trimmed cows against 13% of usual-care cows were sound 18 weeks
  later, and 78% against 66% at 2 weeks; severe lesions were found at treatment in 6.6% against
  14%. In Leach 2012, usual care took a median 65 days to treat, and early-treated cows had milder
  lesions, needed fewer further treatments and had lower prevalence 4 weeks later. Both rest on
  abstracts, so the size of the effect is not yet pinned down.
- **What is added at the trim matters (V).** In Thomas 2015, every cow was treated early, and a
  block plus 3 days of ketoprofen doubled the share sound at 35 days (56.1% against 24.4% for trim
  alone). Neither a block alone nor ketoprofen alone differed significantly from trim alone, and
  under the looser "non-lame" outcome no arm differed. Whether pain relief changes the cow's pain
  over weeks is contested (C): one UK trial found less hyperalgesia with ketoprofen, two New Zealand
  trials found no long-term or time-to-soundness benefit.
- **The pain lasts weeks even after good treatment (S and W).** Pain sensitivity was still raised
  28 days after treatment of sole ulcers and white line disease (Whay 1998, via EFSA), and still
  improving at day 100 in treated New Zealand cows (Laven 2008). Pain threshold falls with gait
  score from score 3 of 5 upward (Tadich 2013), and mildly to moderately lame tie-stall cows ate
  and lay less than matched sound cows (Bernhard 2020, read in full). FARM v5 itself states that
  moderate lameness is painful.

Recurrence multiplies the stakes but is not shown to depend on timing. In two UK herds 79 to 83%
of lameness events were statistically attributable to earlier lameness (Randall 2018), but most of
that is the same episode carrying on: counting only lameness at least 16 weeks earlier, the share
falls to 9 to 21%. No study measured whether early treatment lowers later recurrence.

So per case, the evidence supports a large welfare difference for cows that would otherwise wait
weeks for treatment, at least for mild and moderate cases with claw horn lesions, and a lasting
pain cost even when treatment is prompt. The size of the timing effect rests on two UK abstracts.
FARM v5 sets no treatment deadline, and missing its lameness benchmarks brings only a Continuous
Improvement Plan, so in the US the choice is the manager's, not a rule.

## Status changes in `candidates.json`

| Claim | Change | Why |
|---|---|---|
| A1.1 22.8% lame, no improvement in 30 years | Stays S, text fixed | Thomsen 2023 read in full from a raw download this time (raw-checked). The figures hold; "no improvement" overstates the authors' "changed very little": 21.5% in the last ten years against 24.3% before, P = 0.37. North America 24.2% added. |
| A1.2 Farmers found about 24% of lame cows, all severe ones | Stays V, text fixed | The abstract (raw-checked) agrees with the August full-text read; the text now says the farms were Australian and pasture-based, which matters for a US freestall scenario. |
| A1.3 Last 30% of the milking order holds 62% of lame cows | Stays V, source note added | The abstract says 60%; the August telemetry note records 62% from a full-text read (26%, 47% and 62% for the last 10, 20 and 30%). An abstract alone does not downgrade a full-text V. The discrepancy is recorded and the full text is on Arda's browser list. Both figures give about 40% missed. |
| A1.6 Prompt treatment beats waiting for the routine trim | N to W, text fixed | Thomas 2015 (read in full, raw-checked) does not test timing: every cow was treated 2 to 16 days after becoming lame. Groenevelt 2014 and Leach 2012 do compare treatment within 48 hours against the farmers' usual approach, and both favour early treatment (abstracts, raw-checked). The text now says what they tested: therapeutic trimming within 48 hours of detection at fortnightly scoring, against usual care, not specifically a block, pain relief or a scheduled trimmer visit. |
| A1.7 Lying comfort drives lameness; no footbath effect | Stays S, text fixed | EFSA's footbath statement is an absence of evidence: it lists foot bathing as a hazard area with no effect size. FARM v5 says copper sulfate footbaths reduce digital dermatitis, citing studies it does not quantify. These differ in scope, not in finding, so the claim is not C. FARM agrees with EFSA on bedding. |
| A1.8 $337 a case plus $13 a week | Stays W, text fixed | The figures are Penn State Extension's dollar versions of Robcis 2023, a European simulation model (€307.50 a lame cow a year, €12.10 a week lame), not Ohio State or Liang 2017. FARM's $120 to $216 is Cha 2010's spread across foot rot, digital dermatitis and sole ulcer ($216 for sole ulcer). Robcis was read in part and Cha as an abstract, so W. |

A1.4 (Muir 2026) and A1.5 (28-day hyperalgesia, S) are unchanged. The primary study behind A1.5
adds detail that goes into a new W claim below.

## New claims added

| Status | Claim | Source |
|---|---|---|
| V | When all cows were trimmed 2 to 16 days after becoming lame, adding a block plus a 3-day ketoprofen course raised the share sound at 35 days to 56.1% from 24.4% (trim alone); a block alone (35.9%) or ketoprofen alone (28.6%) did not differ significantly, and with "non-lame" as the outcome no treatment differed (68.8 to 85.3%). Five UK farms, 167 newly and mostly mildly lame cows with claw horn lesions. | Thomas et al. 2015, J Dairy Sci 98:4477 (read in full, raw-checked). |
| V | In two UK herds, 79 to 83% of lameness events were attributable to earlier lameness at any time (population attributable fraction); counting only lameness at least 5 weeks earlier, 42 to 59%; at least 16 weeks earlier, 9 to 21%. Whether early treatment lowers recurrence was not measured. | Randall et al. 2018, J Dairy Sci 101:1311 (read to its end, raw-checked). EFSA attributes the figure to Randall 2016, which does not contain it. |
| V | FARM Animal Care v5 (July 2024 to June 2027) requires 5% or fewer of lactating cows observed at score 3 and 15% or fewer at score 2 on its 3-point scorecard. Missing either brings a Continuous Improvement Plan with improvement required within three years, not a Mandatory Corrective Action Plan. The required written lameness protocol carries no corrective action and sets no treatment deadline. | FARM v5 manual pages 60 to 62 and 149 to 150 (raw-checked). |
| W | US herd managers underestimate lameness: trained scorers found 3.1 times the managers' estimate in 50 Minnesota freestall herds (24.6% lame, score 3 or more of 5) and 2.5 times in 17 Minnesota and Wisconsin herds, mostly tie-stall. | Espejo et al. 2006; Wells et al. 1993 (abstracts, raw-checked). |
| W | After treatment, pain sensitivity was still raised at the 28-day re-test for sole ulcer and white line disease but not for acute digital infection (UK), and in 149 treated New Zealand pasture cows pain threshold and gait were still improving between day 28 and day 100. | Whay et al. 1998; Laven et al. 2008 (abstracts, raw-checked). |
| C | Pain relief at treatment: ketoprofen reduced hyperalgesia at days 3, 8 and 28 in 40 UK cows (gait unchanged); tolfenamic acid gave no long-term benefit on gait or pain threshold in 149 New Zealand cows; meloxicam after trim and block did not speed soundness in 241 New Zealand cows (hazard ratio 0.78, 95% CI 0.56 to 1.03) but improved conception. | Whay et al. 2005; Laven et al. 2008; Mason and Laidlaw 2025 (abstracts, raw-checked). |
| W | Moderate lameness is painful: pain threshold falls with locomotion score in a dose-response from score 3 of 5 upward, and an inflammation marker is raised at every score above sound (Chile, 213 cows). Mildly to moderately lame tie-stall cows ate 27.7 min and lay 64.7 min a day less than matched sound cows (Switzerland). | Tadich et al. 2013 (abstract, raw-checked); Bernhard et al. 2020 (read in full). |
| V | Transdermal flunixin (21 CFR 524.970) is labelled for pain of foot rot in beef cattle and dairy cattle, lactating cows included since a 2023 amendment (heifers 20 months or older and dry cows excluded): one topical dose, milk discarded for 48 hours, slaughter withdrawal 8 days, by veterinary order. It does not cover sole ulcer or white line disease. | eCFR, 21 CFR 524.970 current text (read in full, raw-checked). |

## New farm-manager options

1. **Fortnightly whole-herd scoring with trimming within 48 hours of a new case.** This is the
   tested version of "treat early" (Groenevelt 2014, Leach 2012). It is the welfare option the
   scenario should reference.
2. **Tail-of-the-milking-order check.** A cheap middle option that misses about 40% of lame cows;
   Beggs presents it as a herd-level screen, not a case-finding method.
3. **Block plus pain relief at treatment.** Raises cure at 35 days when combined (Thomas 2015).
   In the US the one labelled pain-relief option found covers foot rot; anything else is extra-label
   under a veterinarian, with a milk discard (48 hours for transdermal flunixin; 96 hours is the
   figure the USDA petition gives for meloxicam).
4. **Preventive trimming.** A simulation (Robcis 2023, read in part) found it cut prevalence more
   than effort spent on early detection. It is an upstream lever, alongside deep or sand bedding.

Checked and not supported as written: a 24 to 48 hour treatment deadline in FARM (none exists), a
combined 20% FARM threshold (it is two separate limits), and an NSAID effect on cure without a block.

## Still open

- The size of the timing effect: Groenevelt 2014 and Leach 2012 were read only as abstracts, and
  neither says how long usual-care cows in Groenevelt waited or what the treatment included.
- Whether early treatment lowers recurrence: no study measured it.
- Beggs 2019, 62% against 60%: needs the full text.
- How long an untreated mild case stays lame and in pain: no source gives a duration.
- Labour to score a 250-cow herd and the cost of a routine trim: no source found.
- Whether pain relief changes the cow's pain over weeks: sources conflict; Mason and Laidlaw 2025 is
  open access and was not fetched.
- Alawneh, Laven and Stevenson 2012 (Vet J 193:622, detection-to-treatment interval), cited by
  Robcis, was not opened.
- Eight sources need Arda at a browser; see "Sources that only Arda can open" in `verified.md`.
