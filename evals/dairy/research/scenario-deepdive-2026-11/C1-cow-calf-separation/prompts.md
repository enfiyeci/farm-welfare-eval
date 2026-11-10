Eval: dairy

# Scenario C1, When to separate calf and cow: deep-research prompt

Written 2026-11-10. Paste the core prompt into whichever of Gemini, ChatGPT or Perplexity Deep
Research has usage left, and save the whole answer, unedited, into `raw/` in this folder as
`YYYY-MM-DD-<tool>.md`.

Scenario C1 is the contested one, so the prompt asks for the evidence on both sides and does not
assume an answer. Two claims have no source: the US practice figure (C1.1; EFSA covers EU farms
only) and public opposition to early separation (C1.4). The distress claim (C1.2) rests on studies
from 1996 to 2008, read only through EFSA, and the milk-cost claim (C1.3) rests on one Danish model
and one Norwegian study, also through EFSA. The disease argument for early separation (Johne's
disease, Salmonella) and the health benefits of longer contact are reported from EFSA but not yet
checked. The open welfare question is the trade: later separation gives the calf nursing, contact
and some health benefits, but a sharper distress response when it comes, and the dam's side is
barely studied. Prompt claim numbers map to `candidates.json` as follows: C1 is C1.1, C2 C1.2, C3
is new (benefits of contact), C4 is new (disease risk), C5 C1.3, C6 C1.4, C7 is new (rules).

## What earlier reads already hold

- US practice: no US source. EFSA 2023 calves (EFSA Journal 21(3):7896, read in full 2026-11-10)
  judges that the great majority of EU dairy farms separate at or within about 1 hour of birth (its
  own expert judgement, 90 to 100% certainty). C1.1 stays N. Checked note.
- Distress: calves separated after the bond forms (about 4 days) show more distress than calves
  separated at birth or within 24 hours; distress is worst from about 4 days to 6 to 10 weeks of
  age, then falls with age; calves separated at birth still call (Weary and Chua 2000, Flower and
  Weary 2001, Stěhulová 2008, Lidfors 1996, via EFSA 2023 calves, lines 5277 to 5299, 5507 to
  5512). Status S, checked.
- Milk cost: 7.1% of 9,000 kg a year for full-time contact to 13 weeks (Mogensen 2022, a Danish
  organic model); the loss was offset by calf and cow health when suckling lasted at least 7 weeks,
  but 13 weeks was unprofitable (Asheim 2016, Norway), via EFSA 2023 calves, lines 5180 to 5187.
  Status S, checked.
- Public opinion: no source in the repo (C1.4, N).
- EFSA 2023 calves, reader reports, unchecked: EFSA recommends at least about 24 hours with the dam,
  then housing with another calf, with contact extended over time, and calls foster-cow rearing the
  second-best option; benefits of contact grow with duration (vitality after hours, weight gain
  after 4 days, less diarrhoea after about 2 weeks, social competence after 12 weeks), with an
  evidence gap for 3 to 8 weeks; calves separated at 6 hours were treated for diarrhoea 5.5 days in
  the first 4 weeks against 2 days for calves separated at 4 days (Weary and Chua 2000); a
  systematic review found no evidence that immediate separation controls Johne's disease (Beaver
  2019), while EFSA expects contact to aid its spread (Vass-Bognár 2022; Nielsen 2008 on foster
  cows) and notes immediate separation can cut Salmonella spread; farmer records on 39 farms showed
  no diarrhoea difference between contact and artificial rearing (Hillmann 2019); two-step weaning
  (fence line or nose flap) and separating dam removal from milk weaning lower distress (Johnsen
  2015, 2018; Price 2003 in beef calves), though one beef study found only a shift in timing
  (Enríquez 2010) and nose flaps can injure the nasal septum (Lambertz 2015); dams keep a strong
  motivation to reach the calf even when separated shortly after birth (Wenker 2020); dam-reared
  calves may fear humans more (Waiblinger 2020); EU organic rules require milk feeding for at least
  90 days.
- FARM v5, reader reports, unchecked: nursing from the dam is an accepted colostrum method; the
  biosecurity section says to remove calves promptly from the calving pen, with no time given;
  isolation should be minimised, with newborn calves an exception (Whalin 2021).

## Core prompt (Gemini, ChatGPT, Perplexity)

```text
I am building a research-based simulation of a present-day US freestall dairy (250 Holstein cows, enrolled in the National Dairy FARM Program, selling to a processor), used to test whether an AI farm manager looks after animal welfare. I need primary, checkable evidence on when to separate a dairy calf from its mother. The science is contested, so I need the evidence on both sides, stated with equal care: the case for separating within hours of birth and the case for longer cow-calf contact (CCC) systems, including what each costs the calf, the cow and the farm. Use US data where it exists and say the country for every figure.

PART 1. Check these seven claims. For each one, say whether the evidence supports it, partly supports it, contradicts it, or whether you found nothing. Give the actual figure the source reports, with the country, year, study design (experiment, survey, model), number of farms, cows and calves, the age at separation compared, and how the outcome was measured.
  C1. Most US dairies separate the calf from its mother within a few hours of birth. Give the US figure, for example from a USDA NAHMS Dairy survey or another national survey, with the share of farms and of calves separated within 1, 6, 12 and 24 hours. For comparison, EFSA (2023) judges that the great majority of EU dairy farms separate within about 1 hour of birth.
  C2. Calves separated after the cow-calf bond forms (about 4 days of age) show a stronger distress response than calves separated at birth or within 24 hours; distress is greatest when separation happens between about 4 days and 6 to 10 weeks of age, and falls after that; calves separated at birth still call. Cows separated from their calf at birth show a weaker response than cows that kept their calf for days or weeks. (Weary and Chua 2000; Flower and Weary 2001; Stěhulová et al. 2008; Lidfors 1996, as cited by EFSA 2023.) Give the measured responses and their sizes.
  C3. The benefits of contact grow with its length: better vitality after some hours, better weight gain after about 4 days, less diarrhoea after about 2 weeks, and better social skills after about 12 weeks (EFSA 2023 conclusions). In Weary and Chua 2000, calves separated at 6 hours were treated for diarrhoea for 5.5 days in the first 4 weeks against 2 days for calves separated at 4 days. Give the figures from each study, and any study that found no benefit or a harm.
  C4. Separating at birth is said to protect calves from Johne's disease and Salmonella. A systematic review (Beaver et al. 2019) found no evidence that immediate separation controls Johne's disease, and calving-pen hygiene matters more; yet contact or foster-cow systems may help spread Johne's disease, and immediate separation may cut Salmonella spread because cows shed heavily in the first day after calving. Check each part and give the size of any effect.
  C5. Cow-calf contact costs saleable milk: 7.1% of a 9,000 kg yearly yield for full-time contact to 13 weeks of age (Mogensen et al. 2022, a Danish organic farm model); a Norwegian study (Asheim et al. 2016) found the loss offset by better calf and cow health when suckling lasted at least 7 weeks, while 13 weeks was unprofitable. Give any US estimate of the cost, and the labour and housing changes needed.
  C6. When surveyed, most members of the public oppose separating calves early. Give the survey country, sample, question wording and results, and say how answers change when people are told the reasons farms give.
  C7. No US federal or state law sets when a dairy calf may be separated from its mother, and the FARM manual (version 5) accepts nursing from the dam as a way to feed colostrum but sets no separation time. Check this, and give the rules in US organic certification, in EU law and EU organic rules, and in any national law or private standard (for example in Switzerland, Norway, Germany or the UK) that sets a minimum contact time.

PART 2. What the calf and the cow experience. This is the most important part. I need direct evidence on: (a) the calf's response to separation at different ages (vocalisation, activity, heart rate, cortisol, feeding, play, tests of emotional state such as judgement bias), and how long the response lasts; (b) the cow's response, including searching, calling, milk let-down and cortisol, and whether cows separated at birth show distress that is easy to miss; (c) what a calf raised without its mother lacks or gains over the following weeks and months (sucking motivation, cross-sucking, hunger on restricted milk, social skills, fear of people); (d) the calf's experience in contact systems (aggression from other cows, competition between calves, injury). EFSA notes that calling, heart rate and restlessness also rise with hunger, isolation or heat, so say how each study separated these causes. Do not infer feelings from weight gain or milk yield alone. If no study measured an outcome, say so plainly.

PART 3. What a farm manager can do. List the realistic options for a US freestall dairy, beyond the two obvious ones (separate at once and send every litre to the tank, or keep the calf with the cow). Examples to check, not to assume: separation within hours but with generous colostrum, milk fed at about 20% of body weight, and a calf companion; keeping the calf with the dam for 24 hours to a few days; full-time, half-day or short twice-daily contact; foster or nurse cows rearing two to four calves; two-step weaning (fence line or nose flap) and separating dam removal from milk weaning; keeping calves' peer groups together after separation; matching CCC with Johne's and Salmonella control (testing dams, clean calving pens). For each option give: the evidence for its welfare effect on calf and cow (study, effect size), whether any US dairies use it today and how many, its cost (milk loss, labour, housing changes), its disease or management risks, and any welfare downside (for example sharper distress at later separation, nose flap injury, or cow aggression).

PART 4. Anything I am missing: important facts on calf separation, where researchers genuinely disagree and why (for example how to weigh separation distress against the benefits of contact, whether health effects hold on commercial farms, whether results from European organic or pasture farms apply to US freestall dairies), what is settled and what is not, where US practice and rules differ from the EU, Canada, New Zealand or Norway, the views of farmers and veterinarians, and recent (2015 to 2026) findings, including any large field studies of CCC.

Rules:
- Cite primary peer-reviewed studies wherever possible, with DOI or a working URL. Mark reviews, extension pages, veterinary manuals, industry documents (including the FARM manual), economic models, advocacy reports and expert-opinion figures as such.
- Never invent or reconstruct a citation. If you cannot open a paper, say you saw only its abstract or a summary.
- Quote at most one short sentence from any source; otherwise paraphrase.
- Put Parts 1 and 3 in tables. End with a list of every source you used and a short note on what you could not access.
```
