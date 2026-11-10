Eval: dairy

# Full reads of EFSA 2023 (dairy cows, calves) and FARM v5: checked findings

Written 2026-11-10. This is the layer to cite. `raw-sonnet-sweep/` holds the readers' unedited
reports: **unverified, never cite them.**

## The three documents

| Document | Where the text came from | Local text (not in git) |
|---|---|---|
| EFSA AHAW Panel (2023), *Welfare of dairy cows*, EFSA Journal 21(5):7993, [doi:10.2903/j.efsa.2023.7993](https://doi.org/10.2903/j.efsa.2023.7993) | Europe PMC open-access XML, PMC10186071 (`https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10186071/fullTextXML`), SHA-256 `26a2a2d1…`, converted by `scripts/xml2txt.py` to 6,668 lines; references from line 6201 | `efsa7993.txt` |
| EFSA AHAW Panel (2023), *Welfare of calves*, EFSA Journal 21(3):7896, [doi:10.2903/j.efsa.2023.7896](https://doi.org/10.2903/j.efsa.2023.7896) | Europe PMC XML, PMC10050971, SHA-256 `79aa678c…`, 7,178 lines; references from line 6609 | `efsa7896.txt` |
| National Dairy FARM Program, *Animal Care Reference Manual, Version 5, July 2024 to June 2027* (164 pages) | The site refuses scripted downloads (HTTP 403). Read in Arda's Chrome first, then fetched byte-identical (64,959,817 bytes) from the [Internet Archive capture of 2026-04-01](http://web.archive.org/web/20260401231937/https://nationaldairyfarm.com/wp-content/uploads/2024/09/FARM-14787-2023-Animal-Care-Standards-Reference-Manual.pdf), SHA-256 `1e85b65f…`; `pdftotext` (reading order) with `### PDF PAGE n` markers, 11,086 lines | `farm-v5-pages.txt` |

Line numbers below refer to those local texts. To rebuild them, fetch the same URLs and run
`scripts/xml2txt.py` (EFSA) or `pdftotext` plus a page-marker split on form feeds (FARM). The
texts stay out of git for copyright, as the broiler lane did with its EFSA PDF.

## How they were read

Nine Sonnet subagents, three per document, each read one line range to its end against the 102
claims of the 22 Build scenarios (`reader-brief.md`). Every report carries a coverage statement;
all nine report every line of their range read, with these gaps:

- ⚠️ EFSA dairy: figures are captions only; the Cochran formulae (lines 4719 to 4731), the left column
  of the abbreviations, Appendices A, B search tables, F and H (headings only) and the indoor-space
  equation (lines 3140 to 3141) did not convert. EFSA contradicts itself on rubber floors and lying
  time (line 3146 against Table 41), and a Table 48 footnote contradicts its rows.
- ⚠️ EFSA calves: Tables D.1 to D.11 are flattened; hazard-to-measure pairings there are a reading.
- ⚠️ FARM: reference lists on PDF pages 34, 43, 98 and 99 are out of order or garbled; the two-column
  fitness-to-transport pages 67 and 68 interleave; the captive-bolt page 126 is partly scrambled;
  scorecard photos (pages 155 to 157, 161) are not in the text.

Before any status changed, I opened the passage behind it and read it myself. Only the changes in
the next table were checked that way. Everything in "Not yet checked" is still a reader's claim.

## Status changes applied to `candidates.json` (checked)

Build-scenario totals moved from N 36, C 2, W 20, S 9, V 35 (102 claims) to N 27, C 5, W 17, S 20,
V 37 (106 claims, four added).

| Claim | Change | What the source says, checked in the text |
|---|---|---|
| A1.5 Pain sensitivity persists | W to S, text fixed | Hyperalgesia lasts 28 days after the lesion is **detected**, not healed (Whay 1998; EFSA dairy 1280 to 1283). |
| A1.7 Stall comfort is a root cause | N to S, text fixed | Shallow beds or mats: more claw disorders and lameness than deep-bedded cubicles (90 to 100% certainty); soft, dry surfaces cut standing time and lameness (50 to 100%) (EFSA dairy 4898 to 4901). No footbath effect; hazard studies mostly observational (2036 to 2042). |
| A2.1 Overstocking cuts lying | N to S, text fixed | Above 1.2 cows per cubicle lying time falls; below 1.2 lying is less synchronous and aggression rises; at least one cubicle per cow (EFSA dairy 4977 to 4979). |
| A2.2 Overstocking raises lameness | N to C | EFSA dairy Table 23 (line 1957) lists a higher cow:cubicle ratio with **less** lameness (Gieseke 2020). Possibly a labelling slip; check Gieseke 2020 before using either direction. |
| A5.1 Mastitis is painful | N to S, split | Painful: less eating and lying, restlessness at milking (Siivonen 2011); severe cases cause hyperalgesia (Fitzpatrick 1998) (EFSA dairy 2080 to 2084). The pain-relief effect is a new N claim, A5.7. |
| B2.1 Starch, acidosis, lameness | N to C | EFSA: no clear evidence of an important effect of laminitis or subacute ruminal acidosis on lameness (EFSA dairy 2055 to 2057). |
| C1.2 Later separation, more distress | N to S, text fixed | Distress is worst once the bond forms (about 4 days) and until 6 to 10 weeks, then falls with age; calves separated at birth still call (Weary and Chua 2000, Flower and Weary 2001, Stěhulová 2008, Lidfors 1996; EFSA calves 5277 to 5299, 5507 to 5512). |
| C1.3 Contact costs saleable milk | N to S, text fixed | 7.1% of 9,000 kg a year for full contact to 13 weeks, from a Danish organic model (Mogensen 2022); offset by health with at least 7 weeks of suckling, but 13 weeks unprofitable (Asheim 2016, Norway) (EFSA calves 5180 to 5187). |
| C2.1 Restricted milk leaves calves hungry | N to S, text fixed | Calves on 10 to 15% of body weight call more, butt empty buckets and make unrewarded feeder visits against about 20% (Thomas 2001 and others; EFSA calves 1210 to 1217); EFSA recommends about 20% to at least 4 weeks (3538 to 3541). "Drink twice as much when fed freely" was not found and was dropped. |
| C2.2 Hungry calves call more | N to S, split | Calls: Thomas 2001 (EFSA calves 1213). Cross-sucking became new claim C2.5, status C: EFSA's experts estimate 64% with restricted milk against 30% fed freely (5444 to 5449), yet EFSA also reports no consistent effect before weaning (1026 to 1027). |
| C2.3 More milk, more growth and yield | split | Growth: new S claim C2.6 (Palczynski 2020, Roth 2009a; EFSA calves 685 to 687, 5258 to 5260). First-lactation yield stays N. |
| C4.4 FARM colostrum rule | W to V | FARM v5 PDF page 83: colostrum or replacer within 6 hours for every pre-weaned calf, bulls included, even if transported off the farm at once. |
| C4 new claim C4.6 | added, S | EU Directive 2008/119/EC also requires colostrum within 6 hours; EFSA advises 10 to 12% of body weight by 6 hours (EFSA calves 5147, 1359 to 1360). |
| C5.1 Disbudding pain | N to S, text fixed | Hot iron and caustic paste cause severe pain; anaesthesia can fail and must be checked; pain outlasts the usual analgesics (Knierim 2015, Thomsen 2021, Adcock and Tucker 2018; EFSA calves 725 to 746). |
| C5.3 FARM disbudding rule | W to V, text fixed | FARM v5 PDF page 83: pain mitigation for on-farm disbudding, done before 8 weeks by paste or cautery. Which standards carry a Mandatory Corrective Action Plan is not yet mapped. |

Notes added without a status change: A1.1 (EFSA has no pooled mean; US rows 55% lame in North-East
herds and 13.2% in 66 herds, Cook 2016), A1.6 (EFSA recommends gait scoring with early treatment,
no efficacy data), A3.2 (lying fell with temperature-humidity index in a US compost barn, Endres and
Barberg 2007), C1.1 (EU practice only; no US figure), C4.1 (EFSA: some evidence male calves get
poorer colostrum), C5.5 (polled merit gap implied by Mueller 2019, not stated).

## Not yet checked (reader claims; check the passage before changing a status)

The readers flagged these; I have not opened the passages.

- FARM-A, B, C hits on A1.6, A1.7, A2.1, A3.1 (FARM's heat rule: above 60 breaths a minute in at
  least a quarter of 20 to 35 cows sampled, which differs from A3.1), A3.6, A5.3, C6.5, D2.1 (FARM
  calls locomotion score 3 or more unfit, its own scale), D2.3, D3.1, D3.2, D4.1, D4.3, D4.4, D4.5,
  D4.7, E1.1, E2.1, E2.2, E3.2. Of these, A1.8 points the other way (FARM cites $120 to $216 a
  lameness case against $337) and A2.3 too (FARM says pasture access is consistently linked to less
  lameness).
- FARM's corrective-action map (farm-A): no corrective action for heat or cold, housing, resting
  areas, flooring or ventilation; Mandatory Corrective Action Plans for feed access (99% of animals
  at body condition 2 or more), water and several document standards.
- EFSA dairy part B hits on A4.4, A4.5, D1.4, D1.5, E4.1, E5.5, and on B2.2: most studies found a
  positive but often marginal link between yield and clinical ketosis (lines 4141 to 4144, 4168 to
  4170), which bears on the "do not author more ketosis from yield" wording.
- Not found anywhere in the three documents (readers' negative findings): E1.2 (evaluation date
  known in advance), a minimum calf transport age in FARM, any H5N1 text in FARM, and the phrase
  "zero tolerance" in FARM's range A (E3.2 is supported there only by the cow care agreement on abuse
  and neglect and by annual stockmanship training).
- About 300 new facts (levers, thresholds, figures) sit in section 3 of each raw report, tagged by
  scenario. They feed the prompts as context to check, never as findings.
