Eval: broiler

# Scenario 4, leg disorders: deep-research prompts

Written 2026-11-05. Paste the core prompt into Gemini Deep Research, ChatGPT Deep Research or
Perplexity Deep Research, whichever has usage left. Paste the Elicit questions into Elicit one at a
time. Save each tool's full answer, unedited, into `raw/` in this folder (see `../README.md`).

Already covered, so the prompt does not ask for it: EFSA 2023 section 3.4.2.12 (read in full)
names the risk factors, says some leg disorders are painful and lame birds go hungry and thirsty,
and lists hospital pens and culling as the only responses once a bird is lame. It gives no
prevalence figures.

## Core prompt (Gemini, ChatGPT, Perplexity)

```text
I am building a research-based simulation of a commercial US broiler (meat chicken) farm, used to test whether an AI farm manager looks after animal welfare. I need primary, checkable evidence on leg disorders in fast-growing broilers (Ross 308, Ross 708, Cobb 500 and similar), compared with slower-growing breeds where possible.

PART 1. Check these four claims. For each one, say whether the evidence supports it, partly supports it, contradicts it, or whether you found nothing. Give the actual figure the source reports, with the breed, bird age, country, year, sample size and how the condition was diagnosed (gait score, live visual exam, or necropsy).
  C1. Tibial dyschondroplasia affects about 30% of commercial broilers in general and about 22% at 6 weeks of age.
  C2. Valgus-varus deformity affects about 5.4% of broilers at 5 weeks.
  C3. Femoral head necrosis and bacterial chondronecrosis with osteomyelitis (BCO) affect about 1% of birds as clinical cases, rising to about 13.3% (and up to about 20%) at high stocking density.
  C4. Many leg lesions, such as tibial dyschondroplasia and early BCO, are only found at necropsy, so on-farm gait scoring understates how many birds have lesions. If possible, give a study that compares gait scores with necropsy findings in the same birds.

PART 2. What the birds experience. Find evidence on pain and duration: how long a typical lame bird lives with the condition before slaughter or culling, and which leg disorders are shown to be painful (for example by analgesic studies, self-selection of painkiller-laced feed, or latency-to-lie tests). Report any estimate of pain duration, including the Welfare Footprint Project's work on broiler chickens if it exists. Do not infer pain where no study measured it; say so instead.

PART 3. What else a farm manager can do. List the realistic actions a US broiler farm manager or integrator can take to prevent leg disorders or respond to them, beyond "use a slower breed" and "lower the stocking density". Examples to check, not to assume: lighting programs and dark periods in the first weeks, early-life activity, perches or platforms, controlled early growth through feed form or feed restriction, vitamin D3 or 25-hydroxy-D3, probiotics against BCO, litter and footpad management, hospital pens, gait-scoring routines, and culling methods and timing. For each action give: the evidence for its effect on leg health (study, effect size), whether it is used on commercial US farms today, its cost or production trade-off if known, and any welfare downside.

PART 4. Anything I am missing: important leg-health facts, disputes between researchers, or recent (2020 to 2026) findings that change the picture.

Rules:
- Cite primary peer-reviewed studies wherever possible, with DOI or a working URL. Mark reviews, industry documents and extension pages as such.
- Never invent or reconstruct a citation. If you cannot open a paper, say you saw only its abstract or a summary.
- Quote at most one short sentence from any source; otherwise paraphrase.
- Put Parts 1 and 3 in tables. End with a list of every source you used and a short note on what you could not access.
```

## Elicit questions (one at a time)

Elicit searches papers rather than writing a report, so ask narrow questions and add the
suggested columns to its results table.

1. `What is the prevalence of tibial dyschondroplasia and valgus-varus deformity in commercial fast-growing broiler chickens?`
   Columns: breed, age (days), country, sample size, diagnosis method, prevalence (%).
2. `How does stocking density affect femoral head necrosis and bacterial chondronecrosis with osteomyelitis in broilers?`
   Columns: density levels (kg/m²), breed, age, BCO or FHN prevalence (%), diagnosis method.
3. `Do gait scores underestimate leg lesions found at necropsy in broiler chickens?`
   Columns: gait scoring system, necropsy findings, agreement between the two, sample size.
4. `Which management interventions reduce leg disorders in fast-growing broilers?`
   Columns: intervention, effect on gait score or lesion prevalence, effect size, breed, commercial or experimental setting.
