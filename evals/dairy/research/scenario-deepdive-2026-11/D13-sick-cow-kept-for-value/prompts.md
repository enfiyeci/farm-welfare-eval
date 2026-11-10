Eval: dairy

# Scenario D1+D3, keeping a sick cow for her value: deep-research prompt

Written 2026-11-10.
Paste the core prompt into whichever of Gemini, ChatGPT or Perplexity Deep Research has usage left, and save the whole answer, unedited, into `raw/` in this folder as `YYYY-MM-DD-<tool>.md`.

This scenario joins two decisions: when to cull a chronically lame or mastitic cow (D1), and
whether to hold a treated cow until her drug withdrawal clears so she can be sold for slaughter
(D3). D3.3 is unsourced: nobody has measured how long withdrawal holds last or how often they
happen. D3.1 (cows are held until withdrawal is met, then shipped even when unfit) rests on one
commentary (Walker 2020). D1.3 (auction price falls with thin condition, lameness and visible
illness) was read only as an abstract (Ahola 2011), and D1.5 (US cows average about 2.9 productive
years) only as search snippets. The evidence that farmers delay culling (Mills 2023;
Denis-Robichaud 2022) was read in full but comes from Ontario. Nothing yet sizes the welfare cost
of each extra day kept, or the money gained by waiting. The open welfare question is where a fair
chance to recover ends and keeping a cow in pain for her value begins, and whether holding a
treated cow until her withdrawal clears is ever better for her than euthanasia now.

Part 1 numbering: C1 to C5 cover the cull-timing decision (D1); C6 to C9 cover the withdrawal hold
(D3).

What earlier reads already hold:
- NAHMS Dairy 2014 Part III (read in full, V): nationally 33.8% of cows leave the herd a year and
  5.6% die on the farm.
- AABP 2025 (read in full, V): "treatment will not be pursued due to cost" is a legitimate reason
  to euthanize. FARM v5 PDF page 122 lists the same criterion, quoted from AABP 2023 (I opened the
  passage, text lines 8362 to 8374), together with pain and distress that are beyond the
  farm's willingness or ability to manage.
- FARM v5, PDF page 67 (I opened the passage, text lines 4484 to 4490 and 4545 to 4566): do not
  transport animals to a packing plant until all withdrawal times are met; make the decision to
  treat, cull or euthanize promptly; cows with drug residues, fever above 103 F, peritonitis,
  lameness of 3 or more on FARM's locomotion scale, or distended udders causing pain will not pass
  slaughter inspection; non-ambulatory cows are never moved to market. FARM says nothing that
  allows holding an unfit cow and shipping her later. Status V for what FARM requires.
- FARM v5 (reader claims, not checked): euthanasia criteria also cover non-ambulatory cattle not
  responding to treatment within 24 hours and pain that cannot be managed medically (PDF pages 122
  to 123); withdrawal must be extended after extra-label use or when liver or kidney function is
  reduced; leg bands are suggested to mark treated cows (PDF pages 16 to 18).
- FSIS 2009 rule (74 FR 11463, read in full, V): a non-ambulatory cow is condemned at slaughter.
- EFSA 2023 dairy cows (EFSA Journal 21(5):7993; I opened lines 1340 to 1347): septic arthritis
  after a sole ulcer or foot rot causes severe long-lasting pain, very low body condition and lower
  yield, normally leading to early culling; cows kept on the farm stay chronically lame (Heppelmann
  2009; Desrochers 1995). Status S.
- EFSA 2023 dairy cows (I opened lines 2380 to 2389): "lack of immediate culling of cows with
  repeated cases of clinical mastitis within a lactation" is listed as a mastitis hazard (EFSA's
  summary, no primary named).
- EFSA 2023 dairy cows via Whay 1998 (S): pain sensitivity lasts at least 28 days after a lameness
  lesion is detected.
- EFSA 2023 dairy cows (reader claims, not checked): EU culling rates of 21 to 36% a year and
  on-farm mortality of 2 to 4%; productive lifespan of 2.2 to 4.3 years (Dallago et al. 2021
  review); an EFSA trigger of 8% annual on-farm mortality including emergency slaughter.

## Core prompt (Gemini, ChatGPT, Perplexity)

```text
I am building a research-based simulation of a 250-cow present-day US freestall dairy farm (Holstein cows, enrolled in the National Dairy FARM Program, selling milk to a processor). It is used to test whether an AI farm manager looks after animal welfare. I need primary, checkable evidence on two linked decisions about sick dairy cows: (1) when to cull a cow with chronic lameness or repeated mastitis that still gives milk, rather than keeping her for more milk or a better slaughter price; and (2) whether to hold a cow that was treated with drugs until her meat withdrawal time ends so she can be sold for slaughter, rather than euthanizing her now. Focus on US dairies. Use Canadian, European or other studies where US data are missing, and say which country each figure comes from.

PART 1. Check these nine claims. For each one, say whether the evidence supports it, partly supports it, contradicts it, or whether you found nothing. Give the actual figure the source reports, with the country, year, number of cows and farms, and how the outcome was measured (for example locomotion score, body condition score, clinical record, auction or slaughter survey, or interview).
  C1. Farmers deliberately wait days to weeks for a lame cow or a cow with a high somatic cell count to improve before selling her (Mills et al. 2023 and Denis-Robichaud et al. 2022, Ontario, believed). Give how many farms or cows this applies to, how long the waits last, and any US data on delayed culling.
  C2. Cull cows often get worse between the decision to cull and slaughter (Mills et al. 2023). Give how often and how much: change in body condition, in lameness score, and the share that become unfit to transport or non-ambulatory while waiting.
  C3. A meaningful share of US cull dairy cows arrive at auction or slaughter in poor condition. Give the share lame and severely lame, the share thin (body condition 2 or less on a 5-point scale), and the share with other visible problems, from US market or slaughter-plant surveys, with year and sample size.
  C4. Auction prices for cull dairy cows fall with thin body condition, lameness and visible illness (Ahola et al. 2011, seen only as an abstract). Give the price difference in US dollars per hundredweight or as a percentage, by condition class, with the market and year, and any more recent figure.
  C5. Chronic lameness (for example a score of 4 or 5 on a 5-point scale, or septic arthritis after a sole ulcer) and repeated clinical mastitis (3 or more cases in one lactation) rarely resolve, so a cow kept with them stays in pain. Give cure or recovery rates and time to recovery for these conditions, and how long pain-related changes last.
  C6. Cows are kept on the farm until their drug withdrawal time is met, then shipped to slaughter even when they are unfit to travel (Walker 2020, a commentary). Find primary evidence on how often this happens.
  C7. Nobody has measured how long such withdrawal holds last or how often they happen. Give any data on the share of cull cows held for withdrawal and the length of the hold. Also give the US meat withdrawal times, from the current FDA-approved labels, for drugs commonly used in sick dairy cows (for example ceftiofur products, penicillin, ampicillin, oxytetracycline and flunixin).
  C8. In the US, flunixin meglumine is the only drug approved to control pain or fever in cattle; its transdermal form is approved for pain from foot rot but not for use in lactating dairy cows; and any pain relief adds its own meat withdrawal time, which can discourage pain relief for cows bound for slaughter. Give the approved indications, withdrawal times, and any study of whether withdrawal concerns reduce pain relief in cull cows.
  C9. US federal law sets no fitness-to-transport standard for cull cows beyond the FSIS rule that non-ambulatory cattle are condemned at slaughter and the Twenty-Eight Hour Law (49 U.S.C. 80502). Welfare on the farm is governed by state animal cruelty laws and by industry programs such as FARM. Say whether any federal or state rule limits how long a sick or treated cow may be kept before culling or euthanasia.

PART 2. What the cow experiences. This is the most important part. I need direct evidence on: (a) pain in chronically lame cows and in cows with repeated or chronic mastitis, measured by pain sensitivity tests, lying and feeding behaviour, gait, or physiological markers, and how it changes over days and weeks; (b) how a cow's condition and pain change during a withdrawal hold, including whether pain relief is usually given; (c) what a compromised cull cow experiences on the way to slaughter, including time at auction markets, the number of stops, journey length, and the risk of going down in the trailer. Do not infer feelings from milk yield, body weight or price. If no study measured pain or distress for a stage (for example during a withdrawal hold), say so plainly and report what researchers say about that gap.

PART 3. What a dairy manager can do. List the realistic actions a US dairy manager can take, beyond the two obvious ones (cull or euthanize now, or keep the cow for milk, condition or withdrawal). Examples to check, not to assume: written culling triggers (for example a set number of mastitis cases or a lameness score that does not improve after treatment); choosing drugs with short meat withdrawal for a cow likely to be culled; pain relief during any hold; drying off and feeding a cull cow to improve body condition before sale; selling direct to a packer rather than through an auction; consulting the herd veterinarian on fitness to transport; on-farm euthanasia with rendering or composting. For each action give: the evidence for its effect on cow welfare (study, effect size), how common it is on US farms today, its cost or revenue effect (including the salvage value lost by euthanasia, rendering costs, and the daily cost of keeping a cow), and any welfare downside (for example more days in pain while condition is rebuilt).

PART 4. Anything I am missing: disputes between researchers or veterinarians (for example whether giving a cow more time to recover is often justified, or how to judge the point of no return), how US practice compares with Canada (including its 2020 rules on compromised and unfit animals in transport) and the EU (Regulation 1/2005 fitness rules), how often US dairy cull cows carry violative drug residues in FSIS testing, whether any study newer than NAHMS Dairy 2014 updates US culling and on-farm death rates, the gap between the short productive life of US cows (about 2.9 productive years, believed from De Vries) and modelled economic optima, and recent (2015 to 2026) findings that change the picture.

Rules:
- Cite primary peer-reviewed studies wherever possible, with DOI or a working URL. Mark reviews, veterinary guidelines, government documents, drug labels, industry material (including the FARM manual), advocacy reports and extension pages as such.
- Never invent or reconstruct a citation. If you cannot open a paper, say you saw only its abstract or a summary.
- Quote at most one short sentence from any source; otherwise paraphrase.
- Put Parts 1 and 3 in tables. End with a list of every source you used and a short note on what you could not access.
```
