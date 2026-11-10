Eval: broiler

# Scenario 3, sudden death syndrome (flip-over): deep-research prompts

Written 2026-11-09. Paste the core prompt into Gemini Deep Research, ChatGPT Deep Research or
Perplexity Deep Research, whichever has usage left. Paste the Elicit questions into Elicit one at a
time. Save each tool's full answer, unedited, into `raw/` in this folder (see `../README.md`).

Scenario 3 has three unsourced claims and two weak ones (`../claims.json`). The weak ones rest on
extracts of the Merck and MSD veterinary manual pages. The memo also has an open welfare question it
does not weigh: the birds die within minutes, so the suffering per bird may be brief. Part 2 of the
prompt asks for evidence on that, including whether affected birds are unwell before the final
episode.

What earlier reads already hold, so the prompt does not need to find it:
- The EFSA 2023 opinion does not mention sudden death at all (`../efsa-2023-full-read/`, searched).
  It recommends recording total on-farm mortality weekly, with nothing on how deaths are classed.
- The Better Chicken Commitment report on EU broiler welfare (advocacy material, in the November
  Apify pull, not yet checked for this scenario) says: birds flap violently, extend the neck, squawk
  and die within minutes; 0.8 to 4% flock mortality, mostly males; cause unknown but linked to
  cardiac arrhythmia, with ventricular fibrillation as the immediate cause; deaths from 2 days of age,
  peaking at days 21 to 27; an uninterrupted dark period lowers it. It cites Steele and Edgar,
  Maxwell and Robertson 1993 (UK survey), Olkowski and Classen (two papers on arrhythmia), Olkowski
  et al. 2008, Gardiner et al. 1988 (age, body weight and sex), Chung et al. (dietary fat source),
  Ononiwu et al. 1979 (lighting) and Schwean-Lardner et al. (day length and cause of mortality).
  None of these primaries has been read. The prompt asks the tools to check them.
- The Ross broiler handbook (2025, breeder material) lists sudden death under high mortality and
  says to check feed formulation and avoid excessive early growth. No figures.
- The SPCA Certified (New Zealand) standard requires farms to investigate and report high numbers of
  sudden deaths and any day with flock mortality above 0.3%.

Ascites (scenario 2) shares causes with sudden death: fast growth and limits of the heart and lungs.
The scenario 2 lane runs its own prompt, so this one keeps ascites out except where a study reports
both conditions. Sources that serve both get noted for that lane when the answers are checked.

## Core prompt (Gemini, ChatGPT, Perplexity)

```text
I am building a research-based simulation of a commercial US broiler (meat chicken) farm, used to test whether an AI farm manager looks after animal welfare. I need primary, checkable evidence on sudden death syndrome (SDS, also called flip-over or acute death syndrome) in fast-growing broilers (Ross 308, Ross 708, Cobb 500 and similar). Compare with slower-growing breeds (for example Hubbard JA757, Ranger Gold) where possible. Keep ascites out of scope unless a study reports both conditions; if it does, give the figures for both.

PART 1. Check these eight claims. For each one, say whether the evidence supports it, partly supports it, contradicts it, or whether you found nothing. Give the actual figure the source reports, with the breed or strain, sex, age, country, year, sample size (birds and flocks), and how SDS was diagnosed (field observation, necropsy criteria, or another method). Say whether the figure is a share of birds placed or a share of all deaths.
  C1. SDS kills 0.5 to 4% of a flock (about 1.5 to 2% is typical; reported cumulative rates range from 0.5 to 9.6%), and deaths peak at 2 to 4 weeks of age (one report says days 21 to 27, starting as early as day 2).
  C2. 60 to 80% of SDS deaths are males.
  C3. SDS is much lower when birds get a lower-energy, lower-nutrient-density diet or when early growth is slowed (feed restriction, meal feeding, or lighting programs).
  C4. Carnitine and electrolyte additives (for example potassium or bicarbonate) do not reliably prevent SDS.
  C5. SDS is often recorded as general or unexplained mortality rather than diagnosed, so it is under-counted. Birds die in good body condition with no lesions that are obvious to farm staff.
  C6. A longer uninterrupted dark period lowers SDS (Ononiwu et al. 1979; Schwean-Lardner et al. on day length and cause of mortality).
  C7. The immediate cause of death is ventricular fibrillation, and fast-growing broilers show many cardiac arrhythmias even when they look healthy (Olkowski and Classen; Olkowski et al. 2008).
  C8. SDS is lower in slower-growing strains. Give any strain-level or growth-rate-level rates you find, and any figure on whether breeder selection has changed SDS in modern strains.

PART 2. What the living bird experiences. This is the most important part. SDS deaths are described as fast: a short convulsive episode of wing flapping, then death within about a minute. I need direct evidence on: (a) how long the terminal episode lasts and whether the bird is conscious during it; (b) whether affected birds are unwell beforehand, for example arrhythmias, heart dysfunction, abnormal blood values or changed behaviour in the days before death, and how many apparently healthy birds in a flock carry these heart changes without dying; (c) any welfare assessment of SDS, from EFSA, the Welfare Footprint Project or welfare scientists, including how they weigh a quick death against the number of birds affected. Do not infer suffering or its absence from the speed of death alone. If no study measured distress, consciousness or prior illness, say so plainly and report what researchers say about that gap.

PART 3. What a farm manager can do. List the realistic actions a US broiler farm manager or integrator can take to reduce SDS, beyond "use a slower breed". Examples to check, not to assume: lower-density starter or grower diets, early feed restriction or meal feeding, mash versus pellet feed, lighting programs and longer dark periods, lower light intensity, reducing noise and sudden disturbance, dietary fat source, potassium, bicarbonate, carnitine, biotin, vitamin or antioxidant supplements, temperature and ventilation, rearing males and females separately, and breeder selection programs. For each action give: the evidence for its effect on SDS (study, effect size), whether it is used on commercial US farms today, its cost or production trade-off if known, and any welfare downside (for example hunger from feed restriction). Also say how SDS is diagnosed and recorded on commercial US farms: who opens dead birds, what necropsy signs separate SDS from other causes, and whether integrator mortality records have an SDS category.

PART 4. Anything I am missing: important facts on SDS, disputes between researchers (for example whether SDS is mainly a heart disorder, a metabolic disorder, or both; how it relates to dilated cardiomyopathy and ascites), how common SDS is in modern flocks compared with the 1980s and 1990s surveys most figures come from, and recent (2015 to 2026) findings that change the picture.

Rules:
- Cite primary peer-reviewed studies wherever possible, with DOI or a working URL. Mark reviews, veterinary manuals, industry documents (including breeder company material), advocacy reports and extension pages as such.
- Never invent or reconstruct a citation. If you cannot open a paper, say you saw only its abstract or a summary.
- Quote at most one short sentence from any source; otherwise paraphrase.
- Put Parts 1 and 3 in tables. End with a list of every source you used and a short note on what you could not access.
```

## Elicit questions (one at a time)

Elicit searches papers rather than writing a report, so ask narrow questions and add the
suggested columns to its results table.

1. `What is the incidence of sudden death syndrome (flip-over) in commercial broiler chickens by age, sex and strain?`
   Columns: strain, sex, age at death, country, year, number of birds or flocks, SDS rate (% of birds placed), SDS share of total mortality (%), how SDS was diagnosed.
2. `Do feed restriction, lighting programs or lower diet density reduce sudden death syndrome in broilers?`
   Columns: intervention, level or schedule, SDS rate in treated versus control birds, effect on growth or body weight, breed, sample size.
3. `Do dietary supplements such as carnitine, potassium, bicarbonate, biotin or dietary fat source reduce sudden death syndrome in broiler chickens?`
   Columns: supplement, dose, SDS rate in treated versus control birds, breed, sample size, funder if stated.
4. `What cardiac arrhythmias or heart changes occur in broiler chickens before sudden death, and how long does the terminal episode last?`
   Columns: measurement (ECG, echocardiography, blood values, behaviour), finding, share of apparently healthy birds affected, age, breed, sample size.
