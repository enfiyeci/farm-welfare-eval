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
| `scripts/` | yes | The text pass and index builders (run with `python3 -I`, from outside `raw/`) |
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
| Grower videos, pull 5 | streamers/youtube-scraper | 1gl7gwpSLnVRFaO8k | 484 videos, 370 with English transcripts | $1.94 |
| Retry of failed and near-empty pages | apify/website-content-crawler | nkhhdrSZiCAdBkkwQ | 120 start URLs, 102 pages saved | $1.15 |
| **Total** (Apify console usage meter, November 5, 2026) | | | | **$3.65 of $105** |

Not on Apify, free: the UGA poultry housing tips archive (525 pages, 554 newsletter PDFs) and the
Auburn NPTC newsletters (105 PDFs), downloaded with plain curl because both sites serve plain HTML;
the 272 search-result PDFs and 463 pages; and one slow retry of the failed PDFs, which recovered
three Stienen manuals that the first download had cut off.

## How the search results were split (November 5, 2026)

`index/search-results.csv` holds all 1,029 unique result URLs, tagged by pull and query.
From those, 201 links to social media and login-walled sites (Facebook, YouTube, Scribd,
ResearchGate, LinkedIn, Instagram, Reddit, Academia, Studocu) were dropped. 272 PDFs are
downloaded directly into `raw/pdf/` (log: `raw/pdf/_log.tsv`). Of the 556 remaining web
pages, a keyword filter kept 463 on-topic pages, fetched directly into `raw/html/`
(log: `raw/html/_log.tsv`). The filter also dropped a few relevant manual index pages, such
as some manufacturer "Manuals" pages; their URLs are still in the CSV.
Pages that fail a direct fetch go to Apify's Website Content Crawler instead.

## Round one, turned into text (November 5, 2026)

`index/documents.csv` has one row per source URL (1,931 rows after round one; round two adds more, see the following section, tracking parameters removed) with the copy that read best, its
status and its length in characters. 1,738 read as text (28.6 million characters; 362 of them are
short, 400 to 1,500 characters), 16 were skipped on purpose (paywalled or abstract-only sites), 64
could not be fetched and 113 came back almost empty (under 400 characters, including 47 PDFs with almost no text, most of them page scans). `index/youtube-videos.csv` now also has a rough `grower_type` label from title,
channel and description: 78 commercial growers, 166 industry and extension, 104 backyard, 136 other
(labelled by a Sonnet pass; borderline calls carry a note). `scripts/yt.py` keeps these labels when it rebuilds the file.

To rebuild from `raw/`: `scripts/extract.py` (PDFs and pages to `raw/text/`),
`scripts/wcc_text.py` (crawler dataset to `raw/text/`), then `scripts/build_index.py`.
The round-two picker is `round-two-picker.html`, published at
https://claude.ai/artifact/KgFc47QMyiLn9QtJVoaXmE (private).

## Round two (November 9 to 10, 2026)

Arda picked A to F and H to L on November 9, 2026 (G, forum threads, was a no). Each paid run
had its cost cap set before it started, and runs went one at a time. Search picks used Google
Search for discovery, then plain curl (`scripts/fetch.sh`, free), then the crawler only for pages
curl could not get.

| Pick | What | Apify Actor | Run ID | Items | Cost |
|---|---|---|---|---|---|
| A | Farm incident news | apify/google-search-scraper | 2E2z9VQg3fBT339ie | 613 unique results, 300 kept (291 pages, 9 PDFs) | $0.356 |
| B | NGO investigations and audit reports | apify/google-search-scraper | Mq2uvbxE3XoelqP7g | 407 unique, 229 kept (213 pages, 16 PDFs) | $0.216 |
| C | FSIS condemnations | none (NASS annual summaries, curl) | | `index/fsis-condemnations.csv`, 2018 to 2025 | free |
| D | UK planning applications | apify/google-search-scraper (`countryCode` gb) | x6fGpRrsVTpsVcjU8 | 315 unique, 198 kept (61 PDFs, 137 pages) | $0.180 |
| E | Grower contracts and settlement sheets | apify/google-search-scraper | Uh4llt7ljApoIZXEM | 241 unique, 184 kept (36 PDFs, 148 pages) | $0.131 |
| F | Job ads probe | misceres/indeed-scraper | 9wswlWx6UnDXDmnxI | 167 ads, 96 with pay | $1.002 |
| F | Job ads probe | curious_coder/linkedin-jobs-scraper | J741ZXPiNxwrmqtLp | 120 ads | $0.240 |
| H | Delmarva map | compass/crawler-google-places | Kg9EWGjNc8kobNIpy | 346 places (DE 183, MD 139, VA 23) | $1.384 |
| I | Transcripts for videos without them | johnvc/youtubetranscripts | x1RqUl54tTei4YQ9V, aPyFW8ldrf5yAbDFi | 114 videos tried, 43 transcripts | $0.119 |
| J | Controller manuals: search | apify/google-search-scraper | dldujyLxH1ur3FMAh | 14 queries, 245 results, 162 PDF links | $0.113 |
| J | Controller manuals: manual pages | apify/website-content-crawler | xvOI8ntiX5HdKefXB | 24 start URLs, 6 pages saved, 18 blocked; aborted after 12 minutes | $0.320 |
| K | Retry of the 63 unfetched sources | apify/website-content-crawler | KAq1mUK5DDp8CRWSI | 63 start URLs, 46 rows, 18 saved files | $0.542 |
| L | OCR of scanned PDFs | none (pdftoppm and tesseract) | | 47 of 48 round-one scans and 6 of 9 round-two scans now read | free |
| **Total** | (Apify console usage meter, November 10, 2026; round two's runs add up to $4.60) | | | | **$8.27 of $105** |

What each pick got:

- **A, B, D, E:** curl got A 219 of 291 pages, D 101 of 137 pages and 48 of 61 PDFs, E 113 of 148
  pages and 32 of 36 PDFs. The rest (about 160 URLs, the non-200 rows in each folder's
  `_log.tsv`) were not sent to the crawler. Their rows are in `index/search-results.csv` as
  `r2-A` to `r2-E`, and their text status is in `index/documents.csv`.
- **C:** since 2020 most condemned birds are logged as "Unknown" (24.5 million of about 9.58
  billion in 2025), so per-cause counts undercount. "Miscellaneous" is NASS footnote 1:
  inflammatory process (cellulitis), plant rejects, missing viscera or ascites.
- **F:** `index/job-ads.csv` (287 ads) with a rough `topic` label from `scripts/r2_jobs.py`:
  157 poultry, 16 kitchen ads that the word "broiler" pulled in, 114 other. LinkedIn returned
  mostly general farm jobs, because its search loosens keywords.
- **H:** `index/delmarva-places.csv` from `scripts/r2_maps.py`, with a rough `kind` (85 farm,
  52 feed, 18 integrator site, 6 hatchery, 6 processing, 21 service, 158 other). No phone
  numbers or street addresses; coordinates rounded to three decimals.
- **I:** 43 transcripts added to `raw/text/youtube/`, mostly Hindi and Indonesian, one English.
  71 videos have none (67 captions disabled, 3 no transcript, 1 age-restricted). The two Zulu
  and one Swahili auto-captions are probably misdetected speech.
- **J:** all 12 Rotem manuals from a dealer page (`inputs/r2-J-britt-rotem-pdf-urls.txt`, curl,
  `raw/r2-J-pdf/`). The search's 162 PDF links were fetched with curl; many are unrelated
  manuals, so `scripts/build_index.py` marks a search PDF `off-topic` unless its URL and text
  have at least two poultry or poultry-equipment-maker words (a rough filter: a few unrelated
  catalogs still pass). Val Controls (doc.valcontrols.com) makes industrial valve
  controllers, not poultry equipment; the poultry maker is Valco, so it was dropped. The crawler got 6 of 24 manual pages, most of them short: manualslib, device.report and
  manuals.plus answered every request with 403 (blocked), so the run was aborted at $0.320 instead
  of spending the rest of its $1 cap on retries.
- **K:** 28 of the 63 sources now read as text (17 from the crawler's saved PDF and Word files
  in `raw/r2-K-files/`, the rest from crawled pages). One saved PDF is a scan.

To rebuild round two's text from `raw/`: `scripts/extract.py`, `scripts/wcc_text.py` once per
crawler dataset (round one with no extra arguments; K with `kw r2-K-wcc`; J with `jw r2-J-wcc`),
`scripts/ocr.py`, then `scripts/build_index.py`. The crawler marks bot-check pages as failed.

`index/documents.csv` now has 2,957 rows across both rounds: 2,545 read as text (2,130 of them
1,500 characters or more), 240 could not be fetched, 93 are almost empty and 40 J search PDFs are
marked off-topic. The `pull` column is the topic a source was found for; K's retries keep their
round-one pull, and tracking parameters are removed from the URLs.
