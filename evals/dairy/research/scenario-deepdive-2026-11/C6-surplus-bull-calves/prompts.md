Eval: dairy

# Scenario C6, surplus bull calves (fate and age at sale): deep-research prompt

Written 2026-11-10.
Paste the core prompt into whichever of Gemini, ChatGPT or Perplexity Deep Research has usage left, and save the whole answer, unedited, into `raw/` in this folder as `YYYY-MM-DD-<tool>.md`.

Scenario C6 has one unsourced claim and three weak ones. The unsourced one is C6.7: how often
healthy newborn calves are killed on US farms (the surplus-calf sweep found no data). The weak ones
were seen only through summaries: over 60% of non-replacement calves leave the farm under 24 hours
old (Cramer 2023), the US has no federal minimum age for calf transport (49 U.S.C. 80502), and
68.6% of US bob veal calves arrive dehydrated (England 2023, via Cramer). The navel figure (Roccaro
2022) was read in full but rests on one study, and the scenario uses it to say that days-old calves
are not fit to travel. No claim yet sizes the effect of the choice itself: how much better a calf
does when sold at one, two or four weeks old instead of one or two days, or sold direct instead of
through an auction. The open welfare question is how to weigh a short life ended humanely on the farm
against a longer one that begins with a days-old trip through an auction.

What earlier reads already hold:
- FARM v5, PDF page 83 (checked): every pre-weaned calf, bulls included, gets colostrum or
  replacer within 6 hours, even if it is transported off the farm at once. Status V for what FARM
  requires.
- FARM v5, PDF pages 82 and 94 (reader claim; I opened the passages, text lines 5498 to 5506 and
  6444 to 6450): the pre-weaned calf standards apply to bull and steer calves unless stated
  otherwise, and the milk standard runs "until weaned or marketed". Status V for what FARM requires.
- FARM v5, PDF page 66, references on page 69 (I opened the passage, lines 4436 to 4456 and the
  reference list): FARM says 16 hours of transport against 6 hours gave more diarrhoea and
  respiratory disease in the next 14 days and less lying (Goetz et al. 2023, J. Dairy Sci.
  106:2800-2818, doi:10.3168/jds.2022-22367; Bajus et al. 2023, J. Dairy Sci. 106:7932-7941,
  doi:10.3168/jds.2023-23229). It also says a Canadian study found calves transported at more than
  one week old had better health and growth, and a Dutch study found 28 days better than 14 days
  for growth, mortality and treatments (Marcato et al. 2022, spelled "Marcota" in FARM, J. Dairy
  Sci. 105:1452-1468). Only FARM's summary was read, not the studies. Status S at best (industry
  manual).
- FARM v5 fitness to transport, PDF pages 65 to 67 (reader claim, not checked): no minimum age.
  Calf criteria are colostrum received, fed and watered, dry, well hydrated, able to stand without
  help, and no illness or injury.
- AABP 2025 (read in full, V): blunt force trauma is unacceptable for calves; a .22 solid-point
  bullet is sufficient under 4 months. FARM v5 PDF page 125 says the same and cites AABP 2023
  (reader claim, not checked).
- New Zealand sets a 4-day minimum age for calf transport; EU Regulation 1/2005 treats calves under
  10 days as unfit except for trips under 100 km (relevant parts read in full, V).
- EFSA 2023 calves (EFSA Journal 21(3):7896; I opened lines 763 to 767, 1481 to 1485, 3554 to 3559
  and 3903 to 3911): in Europe surplus calves leave the dairy farm at about 2 to 5 weeks and reach
  veal farms at 14 to 35 days. Transport at 14 to 21 days falls in the window of lowest immunity
  (2 to 4 weeks) and raises disease risk, and commingling raises infectious disease (both certainty
  90 to 100%). EFSA recommends fattening at or near the farm of origin, avoiding long journeys and
  avoiding auction markets. Status S (EFSA's own judgement).
- EFSA 2023 calves (checked note): some evidence that male calves receive poorer colostrum.
- EFSA 2023 calves (reader claim, not checked): in a Canadian cohort of 4,825 veal calves,
  mortality was linked to dehydration, diarrhoea, sunken flanks and navel infection at arrival
  (Renaud 2018). Transport with poor appetite causes about 10% body-weight loss (Marcato 2020).

## Core prompt (Gemini, ChatGPT, Perplexity)

```text
I am building a research-based simulation of a 250-cow present-day US freestall dairy farm (Holstein cows, enrolled in the National Dairy FARM Program, selling milk to a processor). It is used to test whether an AI farm manager looks after animal welfare. I need primary, checkable evidence on what happens to surplus dairy bull calves (male calves not kept for breeding): the age at which they leave the farm, how they are sold, how that affects their health and welfare, and how and how often they are killed on the farm instead. Focus on Holstein bull calves in the United States. Use Canadian, European and New Zealand studies where US data are missing, and say which country each figure comes from.

PART 1. Check these eight claims. For each one, say whether the evidence supports it, partly supports it, contradicts it, or whether you found nothing. Give the actual figure the source reports, with the country, year, number of calves and farms, calf age, breed, and how the outcome was measured (for example clinical score, blood test, treatment record or death record).
  C1. Most US dairy bull calves leave the farm of birth within days: over 60% of non-replacement calves leave under 24 hours old (Cramer et al. 2023, believed; seen only in a summary). Give the share leaving at under 24 hours, 1 to 3 days, 4 to 7 days and over 7 days, by herd size if reported, and the share sold through auction markets, through dealers, or direct to a calf raiser or veal farm.
  C2. About 90% of calves up to 14 days old still have a navel stump, and the youngest calves with a fully healed navel were 19 to 20 days old (Roccaro et al. 2022, one study). Give any other study of navel healing age, and of navel infection rates in calves sold or transported in the first week.
  C3. Calves sold at a few days old often arrive in poor condition: 68.6% of US bob veal calves were dehydrated on arrival and 96% had at least one poor health measure (England et al. 2023, believed; seen only through Cramer). Also give the rate of failed transfer of passive immunity (low antibody levels from colostrum) in bull calves against heifer calves on US farms, and in calves at arrival at calf-raising or veal farms.
  C4. Age at transport changes outcomes. A Canadian study found calves transported at more than one week old had better health and growth afterwards (believed to be Goetz et al. 2023 or a companion paper from the same trial). A Dutch study found calves transported at 28 days had greater growth and lower mortality and treatment rates than calves transported at 14 days (Marcato et al. 2022). Give the effect sizes: mortality, treatment rate, disease rate and daily gain, by age at transport.
  C5. Longer transport harms young calves: 16 hours against 6 hours gave more diarrhoea and respiratory disease in the following 14 days and less lying time (Goetz et al. 2023; Bajus et al. 2023). Give the effect sizes and any interaction with calf age.
  C6. Selling through an auction market or assembly point, compared with direct sale from farm to raiser, raises disease and mortality in young calves (through commingling, extra handling and longer time without feed). Give any US or Canadian study that compares the two routes, with mortality and morbidity figures and time off feed.
  C7. US federal law sets no minimum age for transporting calves. The only federal transport rule is the Twenty-Eight Hour Law (49 U.S.C. 80502), which limits time confined without food, water and rest; FSIS rules at slaughter add that non-ambulatory (unable to stand and walk) calves are condemned. Say whether any US state sets a minimum age or a maximum journey time for calves, what the AABP transport guidelines (2019) recommend, and whether FSIS changed its handling of non-ambulatory veal calves after 2009.
  C8. There are no US data on how often healthy newborn bull calves are killed on the farm, or by what method. Give any US, Canadian, UK, European, Australian or New Zealand survey of the share of male dairy calves killed at or soon after birth, the methods used (gunshot, captive bolt, injection, blunt force), and how often the method fails or is done badly.

PART 2. What the calf experiences. This is the most important part. I need direct evidence on: (a) hunger, thirst and dehydration during marketing, including how long calves go without milk between leaving the farm and their next feed, and how this is measured; (b) cold or heat stress, fatigue and lying time during transport and at auction; (c) fear and handling stress at auction and loading, including how calves that cannot yet walk well are moved, and any evidence of rough handling; (d) pain from navel infection, and the illness experience of diarrhoea and respiratory disease in young calves; (e) for on-farm killing, how quickly each method causes unconsciousness in a young calf and how often it fails. Do not infer feelings from production data such as growth or mortality alone. Report behaviour, blood or physiological measures, and clinical scores where they exist. If no study measured a calf's distress or pain for a given step, say so plainly and report what researchers say about that gap.

PART 3. What a dairy manager can do. List the realistic actions a US dairy manager can take for surplus bull calves, beyond the two obvious ones (sell at one or two days old through the auction, or keep the calf until it is fit to travel and sell direct). Examples to check, not to assume: holding calves to 7, 14 or 21 days before sale; selling direct to a calf raiser under contract; raising them on the farm to weaning or for dairy beef; colostrum testing (for example Brix refractometer) and extra colostrum for bull calves; navel dipping; feeding and electrolytes before transport; using sexed semen for replacements and beef semen on the rest of the herd so that fewer pure dairy bull calves are born; on-farm euthanasia under a written protocol with a trained person; buyer or certification requirements. For each action give: the evidence for its effect on calf health or welfare (study, effect size), how common it is on US farms today, its cost (including feed and labour per calf per day held, and current US prices for Holstein bull calves and beef-cross calves), and any welfare downside (for example disease spread in crowded calf housing, or calving problems with beef sires).

PART 4. Anything I am missing: disputes between researchers or ethicists (for example whether a humane death at birth is better for the calf than a short veal or dairy-beef life), how US practice compares with the rules in Canada (including its 2020 transport rules for young calves), the EU (including any proposal to replace Regulation 1/2005 and its status in 2026), the UK (including industry commitments to end on-farm killing of dairy bull calves) and New Zealand, and recent (2015 to 2026) findings that change the picture, such as the growth of beef-on-dairy breeding.

Rules:
- Cite primary peer-reviewed studies wherever possible, with DOI or a working URL. Mark reviews, veterinary guidelines, government documents, industry material (including the FARM manual and breed or processor documents), advocacy reports and extension pages as such.
- Never invent or reconstruct a citation. If you cannot open a paper, say you saw only its abstract or a summary.
- Quote at most one short sentence from any source; otherwise paraphrase.
- Put Parts 1 and 3 in tables. End with a list of every source you used and a short note on what you could not access.
```
