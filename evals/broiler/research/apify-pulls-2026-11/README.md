# Apify data pulls for the broiler world (November 2026)

Source material for making the broiler simulator realistic: breed targets, controller alarms,
farm economics, company and standards documents, and how growers describe their work.
Pulled with Arda's free Apify credit (promo period October 13 to November 12, 2026).
Arda picked pulls 1 to 5 on November 5, 2026, and asked for broad coverage.

## What is in git and what is not

This repo is public. Manuals, handbooks, standards PDFs and video transcripts are other
people's copyrighted work, so they stay in `raw/`, which is git-ignored and lives only on
the MacBook that ran the pulls. Git holds the inputs, the URL indexes and this README.
Anything used in the simulator is paraphrased or turned into numbers with a citation.

| Path | In git | What it is |
|---|---|---|
| `inputs/google-queries.txt` | yes | 68 Google queries for pulls 1 to 4 |
| `inputs/youtube-queries.txt` | yes | 25 YouTube searches for pull 5 |
| `index/` | yes | URL lists with titles, one row per source, tagged by pull |
| `raw/` | no | Apify datasets as downloaded, PDFs and page text, transcripts |

## The pulls

| # | Pull | Feeds |
|---|---|---|
| 1 | Breed handbooks and performance targets (Aviagen Ross and Ranger, Cobb, Hubbard; approved-breed lists) | Bird model: growth, feed and water by age; the breed-choice decision |
| 2 | Controller manuals and alarm guidance (Munters/Rotem, Fancom, Big Dutchman, Chore-Time, Cumberland, Valco, SKOV, Stienen, Hotraco, Agri-Alert; UGA and Auburn housing tips) | Alarm thresholds, delays and nuisance alarms for the wake plan |
| 3 | Grow-out economics (extension budgets, grower pay and settlement, house build, propane, power, litter; UK and EU cost studies) | Farm prices; the company-owned versus contract-grower ruling |
| 4 | Company and standards documents (NCC, RSPCA, Red Tractor, GAP, BCC, EU Directive 2007/43, EFSA 2023, Defra code; integrator welfare reports; catching, feed withdrawal, records, biosecurity, depopulation) | Farm documents, the processor's closeout report, scoring anchors |
| 5 | Grower videos on YouTube with transcripts | Daily routine, alarms, catch day and tone for the simulator's emails (paraphrase only) |

## Runs and cost

Filled in as each run finishes.

| Run | Apify Actor | Run ID | Items | Cost |
|---|---|---|---|---|
| Discovery search, pulls 1 to 4 | apify/google-search-scraper | ZRxrE1wsbN5jds77L | 135 result pages, 1,029 unique URLs | $0.57 |
| Grower videos, pull 5 | streamers/youtube-scraper | 1gl7gwpSLnVRFaO8k | running (179 videos at $0.70 when last checked) | cap $4 |

## How the search results were split (November 5, 2026)

`index/search-results.csv` holds all 1,029 unique result URLs, tagged by pull and query.
From those, 201 links to social media and login-walled sites (Facebook, YouTube, Scribd,
ResearchGate, LinkedIn, Instagram, Reddit, Academia, Studocu) were dropped. 272 PDFs are
downloaded directly into `raw/pdf/` (log: `raw/pdf/_log.tsv`). Of the 556 remaining web
pages, a keyword filter kept 463 on-topic pages, fetched directly into `raw/html/`
(log: `raw/html/_log.tsv`). The filter also dropped a few relevant manual index pages, such
as some manufacturer "Manuals" pages; their URLs are still in the CSV.
Pages that fail a direct fetch go to Apify's Website Content Crawler instead.
