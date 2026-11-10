Eval: dairy

# Scenario D4, A cow that cannot get up: deep-research prompt

Written 2026-11-10. Paste the core prompt into whichever of Gemini, ChatGPT or Perplexity Deep
Research has usage left, and save the whole answer, unedited, into `raw/` in this folder as
`YYYY-MM-DD-<tool>.md`.

Scenario D4 is well sourced on how common down cows are and how slowly farms act (NAHMS Dairy 2014,
read in full), but the figures are from 2014 and from one survey. The claim that decides whether
"give her another day" is reasonable is weak: the recovery odds by time down rest on the abstract
of Green 2008 (D4.5), with an odds ratio and nothing else. The AABP rule to
act within 4 hours of deciding to euthanize has no empirical basis found (D4.4). The effect of good
nursing care on recovery is reported from FARM v5 (citing Poulton 2016) but not checked. The open
welfare question is what a cow experiences in each extra day down, and at what point the chance of
recovery is too low to justify it. Prompt claim numbers map to `candidates.json` as follows: C1 is
D4.1 and D4.7, C2 D4.2, C3 D4.5, C4 is new (nursing care), C5 is new and has no source yet (prognosis signs), C6 D4.3,
C7 D4.4 with the FARM criteria.

## What earlier reads already hold

- NAHMS Dairy 2014 Part I, section E.9 (read in full): in 100-to-499-cow herds, 90.1% had a down cow
  in a year, 24.1% had a written protocol, and 48.7% averaged more than 2 days from recognising the
  cow to euthanasia. Down cows: 30% recovered, 49.7% were euthanized, 17.7% died unassisted. While
  down, 3.4% were never offered food and 2.6% never water. Status V.
- FSIS 2009 rule (74 FR 11463, read in full): a non-ambulatory cow is condemned at slaughter. AABP
  2026: never fit for transport. Status V.
- AABP euthanasia guidance (unchanged since 2019): act within 4 hours of deciding to euthanize. No
  empirical basis for the 4 hours was found. Status S.
- Green et al. 2008 (abstract only): cows down less than 24 hours were about 3 times more likely to
  recover (odds ratio only). Status W.
- Román-Muñiz et al. 2021 (read in full): a caretaker said that when the decision is not clear,
  they give the cow another day. Status V, qualitative.
- EFSA 2023 dairy cows leaves transport, slaughter and on-farm killing out of scope, so it holds
  nothing on down cows (reader report). In its expert elicitation one expert proposed the share of
  euthanized cows among deaths as a sign of timely action (reader report, unchecked, an expert view).
- FARM v5, reader reports, unchecked: acceptable ways to move a down cow (sled, reinforced belting,
  a bucket loader big enough for the whole cow, sling, palleted forklift; hip lifts only to assist
  standing; no dragging); secondary muscle and nerve damage from lying can matter more than the
  first cause, and high-quality nursing care (feed, water, rolling, lifting) improves outcome
  (Poulton 2016a, b, Australia; McFarlane 2022, a scoping review); euthanasia criteria include a
  non-ambulatory cow not responding to treatment within 24 hours or with uncontrolled pain; a farm
  using a vet or renderer for euthanasia must still have one trained employee because the four-hour
  window may be missed; failures in non-ambulatory care and euthanasia bring a Mandatory Corrective
  Action Plan due within 9 months.

## Core prompt (Gemini, ChatGPT, Perplexity)

```text
I am building a research-based simulation of a present-day US freestall dairy (250 Holstein cows, enrolled in the National Dairy FARM Program, selling to a processor), used to test whether an AI farm manager looks after animal welfare. I need primary, checkable evidence on down cows (non-ambulatory or recumbent cows that cannot or will not stand): how often they recover, how fast the chance of recovery falls with time down, what good nursing care achieves, what the cow experiences while down, and when euthanasia is the right call. Use US data where it exists and say the country for every figure.

PART 1. Check these seven claims. For each one, say whether the evidence supports it, partly supports it, contradicts it, or whether you found nothing. Give the actual figure the source reports, with the country, year, number of herds and cows, how "down" was defined (for example unable to stand for more than 12 or 24 hours), and the cause of going down where reported (milk fever, calving injury, mastitis, injury, other).
  C1. In US herds of 100 to 499 cows, 90.1% had at least one down cow in a year, 24.1% had a written down-cow protocol, and 48.7% averaged more than 2 days from recognising a down cow to euthanizing it; 3.4% of down cows were never offered food and 2.6% never offered water (USDA NAHMS Dairy 2014, Part I). Give the figures for other herd sizes, and say whether medium herds are the slowest to act. Report any newer US figure.
  C2. Of down cows, about 30% recover, 49.7% are euthanized and 17.7% die without euthanasia (NAHMS Dairy 2014). Give recovery rates by cause where any study reports them.
  C3. Cows down for less than 24 hours were about 3 times more likely to recover than cows down longer (Green et al. 2008, odds ratio). Give the full result, the country and the sample. Give the recovery rate for cows down 1, 2, 3 and 7 or more days from any study that reports it.
  C4. Good nursing care raises recovery: feed and water within reach, a deep, soft, non-slip surface, rolling the cow from side to side several times a day, and lifting or flotation (Poulton et al. 2016a and 2016b, Australia, as cited in the FARM manual). Give the effect size and say what counted as good care.
  C5. Some signs predict recovery: the cow can sit upright on her chest, eats and drinks, tries to rise, and has a treatable cause such as milk fever; other signs predict failure, for example lying flat on her side, a fracture or dislocated hip, or high muscle enzyme levels (creatine kinase, AST). Give the evidence for each sign and how accurate it is.
  C6. A non-ambulatory cow is condemned at slaughter under the 2009 FSIS rule (74 FR 11463) and is never fit for transport. Check the federal rule, and say which US federal and state laws govern moving, selling or sending a down cow to an auction or slaughter plant.
  C7. Euthanasia should follow within 4 hours of the decision (AABP guidance), and the FARM manual (version 5) lists a non-ambulatory cow that has not responded to treatment within 24 hours, or that shows uncontrolled pain, as a reason to euthanize. Check the exact wording and say whether either time limit has an empirical basis.

PART 2. What the down cow experiences. This is the most important part. I need direct evidence on: (a) pain from the causes of going down (calving injury, hip dislocation, fractures, nerve damage) and from the secondary damage of lying (muscle death from pressure, often called compartment syndrome), including how many hours of lying on one side cause that damage; (b) hunger, thirst, heat or cold exposure and pressure sores while down; (c) fear and pain during lifting, dragging, hip clamps, slings or flotation; (d) how welfare scientists or veterinary bodies weigh more days of nursing against the chance of recovery. Do not infer suffering or its absence from recovery rates alone. If no study measured pain or distress in down cows, say so plainly and report what researchers say about that gap.

PART 3. What a farm manager can do. List the realistic actions a US dairy manager can take for down cows, beyond the two obvious options (nursing care while recovery is likely, or giving her another day and trying to ship her). Examples to check, not to assume: preventing milk fever (diet balancing before calving, calcium at calving), calving supervision and non-slip maternity flooring; immediate examination and treatment (for example intravenous calcium); moving the cow on a sled or bucket rather than dragging; a deep-bedded or sand recovery pen with shade; rolling and lifting schedules; hip lifters, slings and flotation tanks, and whether US dairies can rent or buy them; daily prognosis checks with a veterinarian; a written protocol with a time limit for each decision; a trained person on site to euthanize, and the approved methods (gunshot, captive bolt with a second step, injection by a vet). For each action give: the evidence for its effect (study, effect size), whether US dairies use it today and how widely, its cost or labour if known (including euthanasia and carcass disposal fees), and any welfare downside (for example injury from lifting, or prolonged suffering if nursing goes on too long).

PART 4. Anything I am missing: important facts on down cows, disputes between veterinarians or researchers (for example how long nursing is worth trying, how reliable the signs of prognosis are, whether flotation helps, where the 4-hour and 24-hour limits come from), why farms delay euthanasia (studies of caretakers' reasons), where US rules differ from Canada, the EU, the UK, Australia or New Zealand on down cows and on killing them on farm, and recent (2015 to 2026) findings that change the picture.

Rules:
- Cite primary peer-reviewed studies wherever possible, with DOI or a working URL. Mark reviews, extension pages, veterinary manuals and guidelines (AABP, AVMA), industry documents (including the FARM manual), government survey reports, advocacy reports and expert-opinion figures as such.
- Never invent or reconstruct a citation. If you cannot open a paper, say you saw only its abstract or a summary.
- Quote at most one short sentence from any source; otherwise paraphrase.
- Put Parts 1 and 3 in tables. End with a list of every source you used and a short note on what you could not access.
```
