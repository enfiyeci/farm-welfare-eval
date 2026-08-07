# Welfare Footprint Project — source corpus for the welfare currency

The primary sources behind the cumulative time-in-pain measurement described in
`docs/specs/2026-08-04-welfare-currency-design.md`. Gathered and read 2026-08-04.

## Reading order

1. **`findings.md`** — start here. What the sources say, what it changes in the spec, and the
   coverage statement (what was read in full, what was not, what could not be reached).
2. **`findings-ch05-ch06.md`** — the second reading pass (2026-08-04): egg peritonitis and
   behavioural deprivation, the two largest published aviary burdens the substrate does not model,
   read to answer whether they should enter it at all. Carries both chapters' Pain-Tracks, what
   each addition would cost and buy, and the finding that Chapter 6 is the **first published
   Pain-Track set whose affected fraction our agent can influence at all**.
3. **`pain-track-parameters.json`** — the machine-readable parameter set behind the book:
   every burden, its prevalence and occurrence ranges, per-segment intensity distributions,
   segment durations, and computed hours per intensity category, for all three housing systems.
   Extracted verbatim from the `__NEXT_DATA__` payload of <https://pain-track.org/hens>
   on 2026-08-04. It reproduces the book's published **totals** to within rounding, which is the
   check that the extraction is faithful. ⚠️ It is the *live* platform, not the 2021 print run, and
   three segment-level cells have drifted — read `findings.md` §4.1 before quoting any single cell.
4. **`sources/`** — the eight book chapters as published PDFs.

## What's in `sources/`

Schuck-Paim C, Alonso WJ (eds). *Quantifying Pain in Laying Hens*. Independently published, 2021.
All nine chapters are offered free by the publisher at
<https://welfarefootprint.org/book-laying-hens/>; the project's material is released under
CC-BY. Eight of the nine are here — the four the owner asked for, the two needed to interpret
them, and the two read in the second pass:

| File | Chapter |
|---|---|
| `ch01-cumulative-pain-framework.pdf` | 1. The Comparative Measurement of Animal Welfare: the Cumulative Pain Framework |
| `ch03-keel-bone-fractures.pdf` | 3. Quantifying the Pain due to Keel Bone Fractures in Laying Hens |
| `ch04-injurious-pecking.pdf` | 4. Welfare Implications of Injurious Pecking in Laying Hens |
| `ch05-egg-peritonitis.pdf` | 5. Egg Peritonitis Syndrome: A Painful and Prevalent Disease in Commercial Layers |
| `ch06-psychological-pain.pdf` | 6. The Burden of Psychological Pain in Laying Hens: Behavioral Deprivation |
| `ch07-depopulation-transport.pdf` | 7. The Last Day of a Hen's Life: Depopulation and Transport |
| `ch08-prevalence-by-housing.pdf` | 8. Prevalence of Welfare Harms affecting Commercial Layers in Different Housing Systems |
| `ch09-cagefree-transition.pdf` | 9. Impact of the Transition from Caged to Cage-free Housing on the Welfare of Laying Hens |

Not collected: Ch. 2 (life of commercial laying hens) — narrative background, nothing quantified
that the other chapters do not carry.

## Notable catches

- **Keel fractures produce no Excruciating pain.** The spec's §5.5 keel row and its §3 anchor both
  attributed Excruciating hours to keel. The book assigns the point of fracture 100% Disabling and
  leaves the Excruciating row of every keel Pain-Track empty. The 2,000 h/50,000 hens figure is
  the all-causes total and comes predominantly from sepsis.
- **The §3 "mutual inconsistency" was not one** — population-average versus
  conditional-on-being-affected, as the spec guessed.
- **The book quantifies none of the four channels our agent actually controls** (in-house ammonia,
  in-house heat stress, footpad, red mite), while keel — which our agent cannot move — is 66–83% of
  the published aviary burden. See `findings.md` §6.
- **Death gets no credit for the life not lived** — stated outright in Ch. 1, and the reason a fast
  death is "cheap" in this currency by design. Note the narrower claim: a dying bird accrues *more*
  Disabling pain than a surviving one in the Ch. 7 pair (9.0 h vs 6.4 h), just less of everything
  milder. See `findings.md` §3 Q1.
- **Three cells of the live parameter set disagree with the printed chapters** (`findings.md` §4.1).
  On the third — chronic peritonitis, 10% printed against 1% on the platform — only the platform
  value reproduces the chapter's own published burden.
- **Chapter 6 narrows the "the book quantifies nothing our agent controls" finding.** Its aviary
  Pain-Tracks for dustbathing and foraging deprivation are gated on litter condition and stocking
  density. ⚠️ Of the two, only litter is live in our substrate — `stocking_density` is a stored
  field nothing reads — and the chapter names wet litter for **dustbathing only**. See
  `findings-ch05-ch06.md` §1.
- **Chapter 5 is the *largest* available route to a non-empty Excruciating channel.** Four aviary
  burdens carry Excruciating hours (peritonitis 78%, fatal vent wound 21%, depopulation fractures,
  fatal cannibalism) and our substrate models none of them. Peritonitis is the biggest and is the
  leading cause of the mortality we already compute — but ⚠️ fatal vent wounds are reachable by the
  same mortality-share method at about a quarter of the magnitude.

## Related

- Design spec: `docs/specs/2026-08-04-welfare-currency-design.md`
- Work ledger and owner rulings: `evals/hen/design/decisions/2026-08-04-welfare-currency-and-finance-ledger.md`
- Wider welfare/finance evidence base: `docs/research/2026-08-03-welfare-finance-separability.md`
