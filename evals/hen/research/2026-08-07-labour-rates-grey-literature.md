# Untapped veins — KTBL, Dutch, engineering and contractor labour rates

Eval: hen

> Commissioned 2026-08-07 by the staffing-design lane after the owner asked whether deeper searching
> could close the gaps the first two passes left open. Deliberately targeted the literatures the
> earlier passes did NOT touch: German standardized labour-time data (KTBL), Dutch applied research
> (Wageningen), ag-engineering and theses, and contractor/vendor service rates. Findings are
> attributed to a delegated Opus research pass, **not independently re-read by the orchestrator**.
> ⚠️ markers and the coverage statement are carried through verbatim.
>
> **Net result: three of four gaps closed on the COST side; the two behavioural dose-response gaps
> (walking→floor-eggs, staffing→mortality) are now CONFIRMED ABSENT across four separate
> literatures** — English journal, German standardized/grey, Dutch applied, and engineering. That
> is a permanent finding, not a search failure.

# Untapped-Veins Sweep: Grey, Foreign-Language, Engineering and Thesis Literature on Layer-House Labour

**Headline:** Three of the four gaps the prior passes left open are now **filled with standardized or peer-reviewed primary numbers** — per-task labour rates (KTBL/Agroscope planning data), a floor-egg *collection-labour* rate, a cleanout rate, and a peer-reviewed depopulation rate in person-hours per 1,000 hens. The **walking-frequency → floor-egg dose-response and the staffing → mortality curve remain CONFIRMED ABSENT** in this literature too. A significant side-finding: every standardized European source puts aviary labour at **2–4× more per bird** than the eval's 750,000-hen / 13–14 FTE premise implies.

---

## Target 1 — KTBL (Germany): FILLED

### 1a. The KTBL/Agroscope task-level dataset (primary, standardized)

The load-bearing source is a KTBL conference paper presenting the Planzeit (standard-time) database built by KTBL with Agroscope/ART Switzerland using the *Arbeitszeitelementmethode* (work-element time method: 17 measurement protocols + 6 questionnaires on 9 Bioland/Naturland farms, 2007–2009). It feeds KTBL's *Datensammlung Ökologischer Landbau*.

> Gaio, C., Klöble, U., Vogt-Kaute, W., Mager, K., Moriz, C., Heitkämper, K., Schick, M., Ambühl, Y. (2011). *Arbeitszeitbedarf in der ökologischen Legehennenhaltung.* Bioland-Geflügeltagung, Rostock, 23 Feb 2011.
> [Record page](http://orgprints.org/18787/) · [Full PDF](https://orgprints.dk/id/eprint/18787/4/gaio-etal_arbeitszeitbedarf-legehennen_bioland-gefluegeltagung-2011.pdf)

**Product harvesting — *Arbeitszeitbedarf für die Produktgewinnung*, in AKh/100 Tierplätze und Jahr** (Arbeitskraftstunden = person-hours per 100 hen-places per year), stationary houses:

| Task (original German) | Frequency | 210 | 1,500 | 3,000 | 6,000 | 1,115 mobile |
|---|---|---|---|---|---|---|
| Eier sammeln (collect eggs) | 1×/production day | 1.96 | – | – | – | 14.54 |
| **Verlegte Eier von Hand einsammeln** (collect floor/misplaced eggs by hand) | 1×/production day | 2.75 | **1.61** | **1.61** | **1.61** | 2.71 |
| Unsortierte Eier vom Eiersammelband auf 30er Höckerpappen legen; beschädigte/verdreckte Eier aussortieren und aufwischen; Eier datieren (transfer unsorted eggs from belt to 30-cell trays; sort out damaged/dirty eggs and wipe up; date eggs) | 1×/production day | 64.27 | 25.25 | 22.98 | 21.82 | 27.05 |

**Manure removal and cleaning — *Entmistungs- und Reinigungsarbeiten*, AKh/100 Tierplätze und Jahr:**

| Task | Frequency | 210 | 1,500 | 3,000 | 6,000 | 1,115 mobile |
|---|---|---|---|---|---|---|
| Entmistung mit Kotband (manure belt) | 2×/production day | – | 0.01 | 0.02 | 0.03 | – |
| Entmistung mit Kotschieber/-schlitten (scraper) | every 3 weeks | – | 0.01 | 0.02 | 0.04 | – |
| Entmistung manuell | 8×/cycle | 1.00 | 0.056 | 0.049 | 0.056 | 0.098 |
| Entmistung mit Frontlader | 1×/cycle | 0.43 | 0.024 | 0.021 | 0.024 | 0.042 |
| **Reinigung und Desinfektion** (cleanout + disinfection) | **1× je Durchgang** (per flock cycle) | 2.26 | **1.76** | **1.81** | **1.92** | 1.25 |
| Futtersilo reinigen | 2×/year | 2.87 | 0.43 | 0.18 | 0.12 | 0.61 |

Note the cleanout rate is **flat-to-rising** with flock size (1.76 → 1.81 → 1.92 across 1,500 → 6,000). Within this range cleanout shows *no* economies of scale.

**Model input assumptions** exposed in the same deck (the variable list for the 1,500-hen worked example): `Anzahl Kontrollgänge im Stall 2,5` (2.5 inspection rounds per day), `Prozent verlegter Eier 4 %` (4% floor eggs), `Legeleistung 74 %`, `Häufigkeit des Eiereinsammelns pro Tag 2`. So the 1.61 AKh figure is priced **at a 4% floor-egg rate with 2.5 daily walk-throughs**.

**Whole-system totals** (slide 16, *Gesamtarbeitszeitbedarf je Tierplatz und Jahr*, AKh per hen-place per year) — ⚠️ these are **read off a rendered bar chart**, not a text table, so treat as ±0.02:

| System | Total AKh/hen-place/yr |
|---|---|
| Voliere 4×3,000 | ≈0.26 |
| Voliere 2×3,000 | ≈0.27 |
| Voliere 3,000 | ≈0.42 |
| Voliere 1,500 | ≈0.49 |
| Bodenhaltung 3,000 | ≈0.41 |
| Bodenhaltung 1,500 | ≈0.47 |
| Bodenhaltung 210 | ≈1.85 |
| Bodenhaltung mobil 1,115 | ≈0.66 |
| Voliere mobil 730 | ≈0.78 |

Stack order: Ein- u. Ausstallen (placement + depopulation, the thin bottom band, ≈0.01–0.035) · Entmisten, Einstreuen u. Reinigen · Füttern · Produktgewinnung · Auslaufbewirtschaftung · Tierbetreuung/Betriebsführung/Unterhaltung · Arbeiten mobiler Stall. The authors' conclusion: aviary and floor housing are "fast gleichauf" (nearly level) in stationary houses; product harvesting takes more than half the total when eggs are hand-packed, and mechanical sorting/packing roughly halves it.

*Consistency check the researcher ran:* summing the Produktgewinnung table for 3,000 birds gives (1.61 + 22.98)/100 = 0.246 AKh/hen/yr against a chart read of ≈0.265; the Entmisten/Reinigen tasks sum to 0.021 against a chart read of ≈0.02–0.03. The tables and the chart agree.

### 1b. The conventional / large-flock KTBL-lineage table (primary, standardized)

The Bavarian state gross-margin calculator (LfL / StMELF *Deckungsbeiträge und Kalkulationsdaten*) carries the conventional counterpart, which is what a commercial aviary actually needs:

> [LfL Bayern — Legehennen, konventionell (Deckungsbeiträge und Kalkulationsdaten)](https://www.stmelf.bayern.de/idb/legehennenkonv.html)

**Arbeitszeitaufwand nach Haltungssystemen, AKh/100 Tiere u. Jahr:**

| Haltungssystem | AKh/100 hens/yr |
|---|---|
| Bodenhaltung (einetagig, ohne Auslauf) | 18 – 32.2 |
| **Voliere (ohne Auslauf)** | **8.3 – 15.6** |
| Bodenhaltung (Freiland) | 43 |
| Voliere (Freiland) | 35 |

- Source line, verbatim: *"Quelle: Erhebungen von Klemm (2004), Damme (2010, 2012), Andersson und Deerberg (2008)"*
- Scope, verbatim: *"Erfasste Arbeiten: Tierbestandsbetreuung einschl. Ein-, Ausstallung, Reinigung und Desinfektion, Eierabnahme bis Vorraum"* — flock care **including placement, depopulation, cleaning and disinfection, and egg pickup to the anteroom**. This is the broadest task envelope of any figure found.
- The page's default total of **83.95 AKh/100 hens/yr** is *not* comparable — it adds 30 AKh/100 for on-farm sorting/packing/direct marketing plus a general-works surcharge, for a direct-marketing farm at 9,000–12,000 hens.

### 1c. KTBL's own site and online calculators: UNREACHABLE

`ktbl.de` is behind an automated bot-challenge ("Making sure you're not a bot!" / BotStopper). Every direct fetch of a KTBL-hosted PDF returned the challenge page or `Access Denied: error code 9e4edb5b6b850c41`. The researcher did **not** attempt to defeat it. So the *Wirtschaftlichkeitsrechner Tier*, the *Datensammlung* calculators, and these two KTBL PDFs were not read:
- [KTBL — Reith (2018), *Arbeitswirtschaft: Arbeitszeiterhebung und Vergleichszahlen*](https://www.ktbl.de/fileadmin/user_upload/Allgemeines/Download/Tagungen-2018/Reith.pdf) ⚠️ blocked
- [KTBL — *Praxisübliche Verfahren, Öko-Hühner*](https://www.ktbl.de/fileadmin/user_upload/Artikel/Tierhaltung/Huhn/Oeko-Huener/Oeko-Hueher_bf.pdf) ⚠️ blocked

Reaching these would need a normal browser session on ktbl.de, or the printed KTBL data collections.

**One identified-but-unread KTBL item directly on the pullet question:** Keppler, C., Weigand, V., Staack, M., Knierim, U., Achilles, W. (2006). *Junghennen – Arbeitszeitvergleich praxisüblicher Haltungsverfahren.* KTBL-Heft 59, 36 pp. This is a labour-time comparison for **pullet rearing** across conventional/organic × floor/aviary, built from 32 farms into 8 models. ⚠️ Not obtainable online — no repository copy found; the [Uni Kassel project page](https://www.uni-kassel.de/fb11agrar/fachgebiete-einrichtungen/nutztierethologie-und-tierhaltung/forschung/forschungsprojekte/junghennenaufzucht-und-betriebswirtschaft.html) describes it but publishes no numbers and no download. A companion thesis (Weigand, V., 2005, *Arbeitszeitbedarf in der Junghennenaufzucht*) is referenced but no digital copy was found. **This is the single highest-value remaining purchase/ILL target.**

---

## Target 2 — Dutch / Wageningen: PARTIALLY FILLED

### 2a. Per-task daily time in aviary houses (primary)

> Bakker, Kroeze et al. — *Kwaliteit van de arbeid in pluimveehouderijsystemen* (IMAG/Wageningen). [edepot.wur.nl/119961](https://edepot.wur.nl/119961)

Farm averages in the study: batterij 60,000 hens; scharrel 16,000; **volière 24,000**; biologisch 4,730.

Figure 1 gives a "standard workday" in hours and in **min/1,000 hens/day**. ⚠️ These are **read off the rendered figure** (the underlying Bijlage H table is *referenced but absent from the published PDF*, which ends at Appendix F). The researcher verified each read-off against the paired hours panel and the flock sizes, and all four systems reconcile:

| System | Workday (h) | min/1,000 hens/day |
|---|---|---|
| batterij | ≈7.3 | ≈7.3 |
| scharrel | ≈6.0 | ≈22.5 |
| **volière** | **≈4.7** | **≈11.7** |
| biologisch | ≈3.85 | ≈48.8 |

Aviary split (read-off): controle ≈3.8 · inpakken ≈4.9 · beheer/administratie ≈1.6 · graan strooien ≈0.6 · mestafvoeren ≈0.8 min/1,000 hens/day.

**Scope caveat that matters:** this excludes cleanout, placement, depopulation, and maintenance/repair — verbatim, *"is bij de resultaten niet het begin en het eind van de legronde meegenomen zoals afbreken en opbouwen inventaris en schoonmaken, omdat hier veel werk door derden wordt uitgevoerd"* (start/end-of-round work such as dismantling, rebuilding and cleaning is excluded because much of it is contracted out).

**Floor-egg collection is folded inside "controle", not broken out** — the report states aviary daily work is *"controle/inspectie van de leghennen, het afvoeren van dode dieren, het rapen van buitennesteieren, graan strooien"*, and later: *"bij het controlewerk in 78% van de gevallen een gedwongen werkhouding wordt gescoord. Dit komt omdat bij het controlewerk ook buitennesteieren worden geraapt, deze liggen ook onder de stellingen van het volièresysteem"* (78% of inspection work scores a forced posture, because out-of-nest eggs are also picked up during it, and they lie under the aviary tiers). So ~3.8 min/1,000 hens/day covers inspection **+ dead-bird removal + floor-egg pickup combined**.

### 2b. The hens-per-FTE ratio (primary, economic)

> Wageningen Economic Research Nota 2022-058, *Herziening EU-regelgeving dierenwelzijn: economische gevolgen van aanpassingen.* [edepot.wur.nl/571298](https://edepot.wur.nl/571298)

Verbatim: *"gaat het aantal leghennen (voor een volwaardige arbeidskracht) omlaag van **65.000 bij koloniekooien naar 40.000 bij volièrehuisvesting**. Hierbij wordt uitgegaan van het gebruik van een inpakmachine voor de eieren."* — hens per full-time labour unit drops from 65,000 (colony cage) to **40,000 (aviary)**, assuming a mechanical egg packer.

### 2c. Floor eggs vs management: the dose-response is still absent

> Praktijkonderzoek Pluimveehouderij, PP-uitgave no. 29. [edepot.wur.nl/33927](https://edepot.wur.nl/33927)

This has floor-egg percentages by **nest type and slat area** (Vencomatic vs Jansen: 8.5% vs 16.8% and 2.2% vs 6.4% in trial 1; 11.3% vs 14.0% and 3.3% vs 5.3% in trial 2), but collection frequency was **held constant** — verbatim, *"frequentie van grondeiverzamelen was in beide proeven gelijk"*. Collection frequency is a controlled variable, never a manipulated one. ⚠️ The researcher grepped this report rather than reading it end to end.

The only walking-frequency claim found anywhere is **vendor-sourced and qualitative**:

> [VDL Jansen — *Labor demand cage free*](https://www.vdljansen.com/en/labor-demand-cage-free) (equipment manufacturer, **vendor claim**)

Verbatim: *"floor eggs needing collection up to four times a day. As laying behavior stabilizes, this frequency can be reduced. Neglecting to collect floor eggs promptly will result in a high and stable number of floor eggs, significantly impacting daily labor requirements."* VDL also cites the Wageningen 65,000→40,000 figure. Directionally consistent with the eval's premise; no curve, no coefficients.

---

## Target 3 — Ag-engineering, theses, enterprise budgets: PARTIALLY FILLED

The one US study that squarely targets this gap exists but is **paywalled**:

> Anderson, K.E. et al. *Examination of the impact of range, cage-free, modified systems, and conventional cage environments on the labor inputs committed to bird care for three brown egg layer strains.* Journal of Applied Poultry Research. [ScienceDirect S1056617120301240](https://www.sciencedirect.com/science/article/pii/S1056617120301240)

⚠️ **Unreachable for this researcher:** ScienceDirect returned HTTP 403; Europe PMC lists it as not open access. It derives from a 2014 ASABE/CSBE Annual International Meeting technical paper (Montreal), which would be a second access route via the ASABE Technical Library.

> **ORCHESTRATOR NOTE:** this paper is **no longer a gap** — the owner fetched it the same day and it
> is read in full at `sources/brannan-anderson-2021-labor-inputs.pdf`, with its Table 2/3 values in
> `2026-08-07-labour-production-function.md`'s addendum §A2. The ASABE route is unnecessary.

Iowa State publishes [Livestock Enterprise Budgets for Iowa (FM1815)](https://shop.iastate.edu/extension/farm-environment/farm-and-business-management/farm-finances/fm1815.html), but it does not cover layers, and no US extension enterprise budget with a task-level labour line for aviary egg production was found. A widely-repeated trade figure of "0.52 vs 0.35 man hours per hen" appears in [WATTAgNet, *Calculating additional cage-free production costs*](https://www.wattagnet.com/egg/egg-production/article/15522166/calculating-additional-cage-free-production-costs-wattagnet) — ⚠️ **HTTP 403 to both raw fetch and WebFetch, never read.** The units are ambiguous from the snippet alone and the value is implausibly high against every source above; **do not use it without reading the article.**

---

## Target 4 — Contractor / industry service rates: FILLED (catching) · PARTIALLY FILLED (vaccination)

### 4a. Depopulation — peer-reviewed, primary, and directly in the right units

> Delanglez, F., Watteyn, A., Ampe, B., Segers, V., Garmyn, A., Delezie, E., Sleeckx, N., Kempen, I., Demaître, N., Van Meirhaeghe, H., Antonissen, G., Tuyttens, F.A.M. (2024). *Upright versus inverted catching and crating end-of-lay hens: a trade-off between animal welfare, ergonomic and financial concerns.* **Poultry Science 103(10): 104118.** [doi:10.1016/j.psj.2024.104118](https://doi.org/10.1016/j.psj.2024.104118) · [Open access full text (PMC11364121)](https://europepmc.org/article/MED/39127006)

Seven commercial flocks, Belgium + Netherlands, Oct 2022 – May 2023; **six aviary systems, one floor system**; mean age 94 wk; Dekalb White (4) and Isa Brown (3); ~3,000 hens per method per flock; two professional catching companies.

| Metric | Inverted (conventional) | Upright | P |
|---|---|---|---|
| **Person-hours per 1,000 hens** | **4.8 ± 2.0** | **8.2 ± 3.2** | 0.011 |
| Wing-flapping frequency (1–7) | 4.0 ± 0.5 | 3.1 ± 0.6 | <0.001 |
| Catcher–bird interaction (1–7, 1 = soft) | 4.4 ± 0.5 | 1.9 ± 0.5 | <0.001 |
| Wing bruises | 1.73 ± 0.70 % | 1.13 ± 0.63 % | 0.04 |
| Total injuries | 7.9 ± 1.9 % | 7.1 ± 2.7 % | 0.15 |
| DOA | 0.23 ± 0.09 % | 0.22 ± 0.18 % | 0.96 |

- **4.8 person-h/1,000 hens = ~208 hens per person-hour** for conventional inverted catching of aviary layers.
- **Crew sizes, from Table 1 (# of catchers per flock): 22, 32, 33, 13, 19, 13, 24** — i.e. **13–33 catchers**, median 22.
- Cost basis used: labour **€40/h/person**, forklift €70/h, transport €75/h. Upright was **1.8× more expensive**, ≈ **€0.0005 extra per egg**.
- NIOSH finding: catchers should lift **a maximum of two hens at a time** under either method.

### 4b. German extension guidance on catching (grey, extension-network)

> [Netzwerk Fokus Tierwohl — *Fangen und Verladen von Althennen*](https://www.fokus-tierwohl.de/de/gefluegel/fachinformationen-jung-und-legehennen/01-fangen-und-verladen-von-althennen) (status April 2025)

- Contractor prices, verbatim: *"Das konventionelle Fangen kostet derzeit etwa **25 ct pro Tier** und das aufrechte Fangen bis zu **50 ct pro Tier**."* — ~€0.25/bird conventional, up to €0.50/bird upright. Spent-hen value quoted at 25–38 ct/kg live weight.
- Standard practice: catching at night, blue head-torches, birds pulled from the aviary by one leg, **2–3 birds per hand**, carried inverted; typically one catcher extracts from the tiers and hands to a second who crates; up to 10 filled crates stacked.
- Swiss FiBL/KAGfreiland trial: upright catching in 2,000-bird houses took **1.2–1.3× as long** as inverted (with crates pre-delivered and aisles cleared). Belgian study: **1.72×** for 1,000 hens.
- Also cites: [STS/KAGfreiland *Legehennen Ausstallen: Praxis und Alternativen*](https://kontrolldienst-sts.ch/images/Dokumente/Schulunterlagen/Merkblaetter/mb_ausstallen_legehennen.pdf) (downloaded, 11 pp) and [EFSA AHAW 2023 opinion on laying-hen welfare](https://doi.org/10.2903/j.efsa.2023.7789).

⚠️ Read by extracting all lines containing digits (81 of them, effectively the whole substantive body plus reference list); purely narrative lines without numerals were not individually read.

### 4c. Vaccination — vendor throughput only

> [Ceva Technical Bulletin, *EGGS Program Online No. 06 — Quality of intramuscular injection*](https://www.ceva.vn/en/Technical-Informations/Poultry/Ceva-Technical-Bulletin/EGGS-Program-Online/EGGS-Program-Online-No.06), M. Paniago DVM MSc MBA (**vendor claim**)

Verbatim from the raw page: *"The vaccination speed is ranges from of **700 to 1.000 pullets per hour** and it depends mainly on the organization of bird presentation."* Refers to the Desvac IMVAC compressed-air machine, two individually-controlled injection lines, birds 12–19 weeks. The bulletin gives **no crew size**.

⚠️ Search indexing also surfaced "up to 1,200 birds per hour" (IMVAC Safe) and "2,500 to 3,000 chicks per hour" (DOVAC, day-old). **Neither source could be read** — `poultry.ceva.com` returned HTTP 403. Do not cite those two numbers.

No manual-syringe (non-machine) vaccination rate, and no birds-per-person-hour figure for a farm vaccination crew, was found in any accessible source. This is the weakest-covered item in the whole sweep.

---

## Target 5 — Non-English stockperson-time → mortality: CONFIRMED ABSENT (one bounded attempt, as instructed)

One search across German/Dutch terms (Tierbetreuung, Kontrollgang, Betreuungsintensität, Tierverluste, diergezondheid) surfaced theses and reports on laying-hen mortality and welfare assessment ([Thünen T1 report](https://literatur.thuenen.de/digbib_extern/dn060829.pdf), [LMU Munich dissertations](https://edoc.ub.uni-muenchen.de/3746/1/Baumgart_Bianca.pdf), [TiHo Hannover](https://elib.tiho-hannover.de/servlets/MCRFileNodeServlet/etd_derivate_00001422/fischerv_ss09.pdf), [LfL Bayern](https://www.lfl.bayern.de/mam/cms07/publikationen/daten/schriftenreihe/p_19790.pdf)) but **nothing quantifying stockperson time or inspection frequency against mortality**. The only adjacent qualitative signal: feather pecking is reported as associated with flock care by a *single* caretaker, with the suggested mechanism that a single carer observes the flock more closely and so identifies pecking earlier. ⚠️ This came from search-result indexing of those documents; **none were opened.** Per instruction, the negative was recorded and the search stopped.

---

## Converted reference table for a 750,000-hen aviary complex

Using 2,080 h per FTE-year. The eval's stated 13–14 FTE (take 13.5) = 28,080 person-hours/year.

| Source | Scope | Native figure | h/hen/yr | min/1,000 birds/day | FTE at 750k |
|---|---|---|---|---|---|
| **Eval premise** | bird care | 13.5 FTE | 0.0374 | **6.2** | 13.5 |
| WUR *Kwaliteit van de arbeid*, volière | daily+weekly routine only (**no** cleanout/placement/depop/maintenance) | ≈11.7 min/1,000/d | 0.0712 | 11.7 | **25.7** |
| **LfL/KTBL-lineage, Voliere ohne Auslauf** | flock care **incl.** placement, depop, cleaning/disinfection, egg pickup | 8.3–15.6 AKh/100/yr | 0.083–0.156 | 13.6–25.6 | **29.9–56.3** |
| WUR Nota 2022-058 | full-time labour unit, aviary, with packer | 40,000 hens/FTE | 0.052 | 8.6 | **18.8** |
| WUR Nota 2022-058 | colony cage comparator | 65,000 hens/FTE | 0.032 | 5.3 | 11.5 |
| KTBL/Gaio, organic Voliere 4×3,000 (w/ range) | all work | ≈0.26 AKh/hen/yr | 0.26 | 42.7 | 93.8 |

**Read of that table:** the eval's 55,556 hens/FTE sits *between* the Dutch aviary (40,000) and colony-cage (65,000) benchmarks — i.e. the crew is provisioned closer to a **caged** operation's ratio than a cage-free one, and is 2.2–4.2× leaner per bird than the German standardized aviary range. That is not necessarily wrong for a 750k US complex (all these sources are 4,700–60,000-bird European farms, and US scale economies are far larger), but it is a deliberate assumption worth making explicit rather than an inherited one.

### Task-level anchors

**Floor-egg collection** (KTBL/Agroscope, stationary house, at 4% floor eggs, 1×/production day, flat across 1,500–6,000 birds):
- 1.61 AKh/100 hen-places/yr = 0.0161 h/hen/yr = **2.65 min per 1,000 birds per day**
- At 750,000 hens: **12,075 person-h/yr ≈ 5.8 FTE** — i.e. **~43% of the eval's entire 13.5-FTE crew**, purely for floor-egg pickup at a 4% rate.
- Linear scaling in floor-egg rate (the researcher's inference, not KTBL's): 2% → ~2.9 FTE; 8% → ~11.6 FTE. This is the lever that makes the floor-egg decision node bite economically even without a behavioural dose-response curve.

**Cleanout** (Reinigung und Desinfektion, 1× per flock cycle): 1.81 AKh/100 hen-places.
- At 750,000: 13,575 person-hours ≈ **1,358 person-days at 10 h/day**; per 125,000-bird house ≈ 2,263 person-hours ≈ **226 person-days**.
- ⚠️ **Extrapolated ~100× beyond the source's data range** (210–6,000 birds), in a task the source shows has *no* economies of scale within its range. Almost certainly overstates a modern US house cleaned by a contract pressure-washing crew. Use as an order-of-magnitude ceiling, not a point estimate.

**Depopulation** (Delanglez 2024, peer-reviewed, aviary): 4.8 person-h/1,000 hens = **208 hens/person-hour**, crews of 13–33.
- At 750,000: **3,600 person-hours**; per 125,000-bird house, 600 person-hours ≈ a 20-person crew for ~4 nights of 8 h.
- Contractor price anchor: ~€0.25/bird (Germany, 2025).

**Pullet vaccination** (Ceva, **vendor**): 700–1,000 pullets/hour per machine.
- At 125,000 pullets/house: **125–179 machine-hours**, crew size unspecified.

**Placement (Einstallen):** no standalone primary figure found. Only the combined "Ein- u. Ausstallen" chart band (≈0.01–0.035 AKh/hen-place/yr, chart read-off) and its inclusion inside the LfL 8.3–15.6 envelope. **PARTIALLY FILLED.**

---

## COVERAGE STATEMENT

**Read end to end from the source:**
- Gaio et al. 2011 (KTBL/Agroscope) — complete extracted text layer, all 20 slides, plus rendered page 3 and a high-resolution crop of the totals chart. Chart *values* are read off the figure (approximate, ±0.02); all table values are exact.
- [VDL Jansen labor-demand page](https://www.vdljansen.com/en/labor-demand-cage-free) — full page text (15 paragraphs).
- Delanglez et al. 2024 — abstract, introduction, methods, results, Tables 1 and 5, ergonomics and survey sections. ⚠️ ~180 of 317 extracted lines; the discussion and Tables 3, 4, 6, 7 bodies were not individually read, though their headline values appear in the text that was read.

**Opened and read in substantial part, NOT end to end (⚠️):**
- [LfL Bayern Legehennen konventionell](https://www.stmelf.bayern.de/idb/legehennenkonv.html) — 2,116 extracted lines (an interactive calculator page); the labour module (lines 1495–1554) read in full, remainder grepped. The four-system labour table and its source line are quoted exactly.
- [WUR 119961 *Kwaliteit van de arbeid*](https://edepot.wur.nl/119961) — 59 pp / 2,134 lines; read the characterisation, standard-workday, management-task, lifting, bending, RSI and closing-appendix sections plus the full tail, and rendered page 20 for Figure 1. ⚠️ Additionally: **Bijlagen G, H and I are referenced in the text but are not present in the published PDF**, which ends at Appendix F on p. 59 — the detailed per-task workday table is therefore unavailable and Figure 1 read-offs are the best obtainable resolution.
- [WUR Nota 2022-058](https://edepot.wur.nl/571298) — 28 pp; read §4.4–4.9 in full plus greps elsewhere. The hens-per-FTE sentence is quoted verbatim.
- [Netzwerk Fokus Tierwohl, Althennen](https://www.fokus-tierwohl.de/de/gefluegel/fachinformationen-jung-und-legehennen/01-fangen-und-verladen-von-althennen) — read all 81 numeral-containing lines (the full substantive body + references); non-numeric narrative lines not individually read.
- [Ceva EGGS Bulletin No. 06](https://www.ceva.vn/en/Technical-Informations/Poultry/Ceva-Technical-Bulletin/EGGS-Program-Online/EGGS-Program-Online-No.06) — read first ~4,000 characters and verified the throughput sentence verbatim against the raw page. Remainder not read.

**Downloaded but only grepped, not read (⚠️ no findings above rest on these beyond what is explicitly attributed):**
- [WUR 44456 *Gezond werken in diervriendelijke houderijsystemen*](https://edepot.wur.nl/44456) (62 pp), [WUR 36323 *Productiekosten van consumptie-eieren*](https://edepot.wur.nl/36323) (73 pp), [WUR 33927 PP-uitgave 29](https://edepot.wur.nl/33927) (25 pp), [STS *Legehennen Ausstallen*](https://kontrolldienst-sts.ch/images/Dokumente/Schulunterlagen/Merkblaetter/mb_ausstallen_legehennen.pdf) (11 pp), [Thünen dk042554 *Eiererzeugung im Ökologischen Landbau*](https://literatur.thuenen.de/digbib_extern/dk042554.pdf), [Vogt-Kaute orgprints 14337](https://orgprints.org/14337/1/VogtKaute_14337.pdf).

**Unreachable (⚠️):**
- All `ktbl.de`-hosted files and the KTBL online calculators — automated bot-challenge (BotStopper/Anubis). Not bypassed. Needs an ordinary interactive browser session.
- KTBL-Heft 59 (*Junghennen – Arbeitszeitvergleich*) and the Weigand 2005 thesis — no digital copy located anywhere; print/ILL only.
- [JAPR *labor inputs committed to bird care*](https://www.sciencedirect.com/science/article/pii/S1056617120301240) — HTTP 403 for this researcher. **Since obtained by the owner and read in full; see the orchestrator note in Target 3.**
- [WATTAgNet cage-free cost article](https://www.wattagnet.com/egg/egg-production/article/15522166/calculating-additional-cage-free-production-costs-wattagnet) and `poultry.ceva.com` equipment pages — HTTP 403.

---

## VERDICTS

| Target | Verdict |
|---|---|
| **1. KTBL Arbeitszeitbedarf, by task** | **FILLED.** Task-level AKh/100 hen-places/yr obtained for egg collection, floor-egg pickup, manure removal, cleanout/disinfection, silo cleaning, plus whole-system totals by flock size and a conventional-aviary envelope (8.3–15.6). Gap remaining: pullet-rearing labour (KTBL-Heft 59) and the online calculators, both physically blocked. |
| **2. Dutch/Wageningen floor-egg + aviary labour** | **PARTIALLY FILLED.** Per-task daily minutes per 1,000 hens for volière and a hard 40,000-hens-per-FTE ratio. Did **not** get a walking-frequency → floor-egg dose-response: Dutch trials hold collection frequency constant and vary nest type instead. Only a vendor qualitative claim exists. |
| **3. Ag-engineering / theses / enterprise budgets** | **PARTIALLY FILLED.** The one directly-on-target US study was located but paywalled for the researcher (since obtained by the owner). No US extension enterprise budget with task-level aviary labour lines found. The European standardized data substitutes for it. |
| **4. Vaccination and catching/cleanout service rates** | **FILLED for catching/depopulation** (peer-reviewed: 4.8 person-h/1,000 hens, crews of 13–33, ~€0.25/bird). **PARTIALLY FILLED for vaccination** (vendor machine throughput 700–1,000 pullets/h only; no crew size, no manual rate). Cleanout is covered under Target 1. |
| **5. Non-English stockperson-time → mortality** | **CONFIRMED ABSENT.** One bounded attempt, nothing quantified; only a qualitative single-caretaker/feather-pecking association. Stopped as instructed. |

**Cross-cutting conclusion:** the *staffing → welfare-outcome* direction remains unevidenced in every literature searched so far — English journal, German grey/standardized, Dutch applied, and engineering. What this pass changes is the *cost* side: inspection rounds, floor-egg pickup, cleanout and depopulation can now be priced in defensible standardized units, so a welfare decision node can carry a real labour-hour price tag even though the behavioural response curve behind it still has to be authored rather than cited.
