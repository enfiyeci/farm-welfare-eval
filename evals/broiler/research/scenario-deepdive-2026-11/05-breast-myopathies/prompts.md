Eval: broiler

# Scenario 5, breast myopathies: deep-research prompts

Written 2026-11-07. Paste the core prompt into Gemini Deep Research, ChatGPT Deep Research or
Perplexity Deep Research, whichever has usage left. Paste the Elicit questions into Elicit one at a
time. Save each tool's full answer, unedited, into `raw/` in this folder (see `../README.md`).

Scenario 5 has three unsourced claims and eight weak ones (`../claims.json`). The unsourced claim
that matters most is the welfare claim itself: that woody breast hurts or impairs the living bird.
The memo supports it only by calling the condition muscle necrosis. The research found so far
frames woody breast and white striping as meat-quality problems, so Part 2 of the prompt asks
directly for evidence from live birds.

What earlier reads already hold, so the prompt does not need to find it:
- The EFSA 2023 subagent sweep (`../efsa-2023-full-read/raw-sonnet-sweep.md`, raw and not yet
  checked for this scenario) found two mentions. Section 3.4.2.12 lists wooden breast as one
  trigger of locomotory disorder, with no statement about pain. Section 3.5.2.7 says too much
  exercise may raise the risk of wooden breast and that vertical panels did not cause it.
- The September baseline search found Norring et al. 2019, "Wooden breast myopathy links with
  poorer gait", but only its search summary was read (ScienceDirect blocked the fetch).
- The Aviagen broiler myopathy handbook (2023) is already downloaded in the Apify pull and not yet
  read. It is the breeder's own account, so it does not count as independent evidence.

## Core prompt (Gemini, ChatGPT, Perplexity)

```text
I am building a research-based simulation of a commercial US broiler (meat chicken) farm, used to test whether an AI farm manager looks after animal welfare. I need primary, checkable evidence on breast muscle myopathies in fast-growing broilers (Ross 308, Ross 708, Cobb 500 and similar): woody breast (also called wooden breast), white striping, and spaghetti meat. Compare with slower-growing breeds (for example Hubbard JA757, Ranger Gold) where possible.

PART 1. Check these ten claims. For each one, say whether the evidence supports it, partly supports it, contradicts it, or whether you found nothing. Give the actual figure the source reports, with the breed, sex, age or live weight at slaughter, country, year, sample size, and how the myopathy was scored (hand palpation of the fillet, visual score, histology, or another method).
  C1. Severe woody breast rises sharply once live weight passes about 2.7 kg.
  C2. Detecting and sorting affected fillets at the processing plant reduces the economic loss but does nothing for the bird. The condition can only be prevented through genetics or growth management, not processing.
  C3. In males, woody breast odds are about 1.75 times higher (95% CI 1.12 to 2.73) when average daily gain is above 78 g/day, compared with 70.7 to 78 g/day. This comes from a 2022 meta-analysis published in a Frontiers journal.
  C4. Woody breast odds are about 1.23 times higher (95% CI 1.03 to 1.47) at 2.46 to 2.63 kg live weight. This comes from a 2022 Ontario, Canada study of about 9,250 fillets (PLoS ONE, PMC9012353).
  C5. Severe woody breast affected 24.2% of Ross 708 birds (about 3.2 kg at 42 days) versus 4.7% of Ranger Gold birds (about 2.76 kg at 56 days); total woody breast was 90.5% versus 76.4% (PMC11472612).
  C6. Across four commercial strains, severe woody breast was about 5%, 35%, 5% and 16% (Kuttappan et al. 2013).
  C7. Woody breast affected 25.2% of males versus 12.1% of females (female odds ratio 0.55) in the Ontario 2022 study.
  C8. High-energy diets increase the severity of white striping (Kuttappan et al. 2012).
  C9. White striping odds rise with breast weight (about 1.49 times higher above 960 g than at 850 to 960 g) and differ by genotype (about 2.75 times higher in one genotype than another), from the same 2022 Frontiers meta-analysis.
  C10. Woody breast lesions start at about 2 weeks of age and worsen with age and weight, and a 1950s random-bred line showed only minimal lesions that did not progress (Chen, Borst and colleagues, 2019).

PART 2. What the living bird experiences. This is the most important part. Woody breast is described as muscle degeneration (fibre necrosis, fibrosis, inflammation, vein inflammation). I need to know whether there is direct evidence that it causes pain, discomfort or functional impairment in the live bird, not only in the meat. Look for: studies of gait, walking ability, activity, lying time or wing use in birds later diagnosed with woody breast (for example Norring et al. 2019 on wooden breast and gait); any analgesic or pain-behaviour study; blood markers of muscle damage or inflammation in live birds; effects on breathing, heat tolerance or mortality; and whether affected birds can be identified alive by palpation. Also say how long a typical affected bird lives with the lesions before slaughter. Report any welfare assessment of breast myopathies, including from EFSA, the Welfare Footprint Project or welfare scientists, if one exists. Do not infer pain from the tissue damage alone. If no study measured pain or impairment in live birds, say so plainly, and report what researchers say about that gap.

PART 3. What a farm manager can do. List the realistic actions a US broiler farm manager or integrator can take to reduce woody breast and white striping, beyond "use a slower breed". Examples to check, not to assume: lower slaughter weight or earlier processing, lower diet energy or amino acid density, early feed restriction or lighting programs that slow early growth, dietary supplements (for example vitamin E, selenium, arginine, guanidinoacetic acid, creatine, antioxidants), grow-out temperature and ventilation, coccidiosis vaccination, rearing males and females separately, activity and enrichment (note any finding that more exercise raises risk), and breeder selection programs. For each action give: the evidence for its effect on myopathy prevalence or severity (study, effect size), whether it is used on commercial US farms today, its cost or production trade-off if known, and any welfare downside (for example hunger from feed restriction).

PART 4. Anything I am missing: important facts on breast myopathies, disputes between researchers (for example how much is genetics versus management, or whether breeders' selection has reduced it), and recent (2020 to 2026) findings that change the picture.

Rules:
- Cite primary peer-reviewed studies wherever possible, with DOI or a working URL. Mark reviews, industry documents (including breeder company material) and extension pages as such.
- Never invent or reconstruct a citation. If you cannot open a paper, say you saw only its abstract or a summary.
- Quote at most one short sentence from any source; otherwise paraphrase.
- Put Parts 1 and 3 in tables. End with a list of every source you used and a short note on what you could not access.
```

## Elicit questions (one at a time)

Elicit searches papers rather than writing a report, so ask narrow questions and add the
suggested columns to its results table.

1. `What is the prevalence of woody breast and white striping in commercial broiler chickens by strain, sex and slaughter weight?`
   Columns: strain, sex, age or live weight at slaughter, country, sample size, scoring method, woody breast (%), severe woody breast (%), white striping (%).
2. `Is wooden breast myopathy associated with impaired gait, reduced activity, pain or other welfare problems in live broiler chickens?`
   Columns: outcome measured in live birds, how woody breast was diagnosed, effect found, breed, age, sample size.
3. `How do growth rate, live weight and genetic strain affect the incidence of woody breast in broilers?`
   Columns: strain or growth rate compared, live weight or age, woody breast prevalence or severity, effect size, sample size.
4. `Which dietary or management interventions reduce woody breast or white striping in broiler chickens?`
   Columns: intervention, dose or level, effect on woody breast or white striping, effect on growth or yield, breed, commercial or experimental setting.
