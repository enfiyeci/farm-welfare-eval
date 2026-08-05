# Handoff: welfare currency Step 1 done — sources read, mapping table sourced, three rulings recorded
> Written: 2026-08-04 · Branch: `worktree-finance-decision-map` (pushed, `5e5b5fa`) · Status: stale
>
> **SUPERSEDED** by `/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/finance-decision-map/docs/handoffs/handoff-2026-08-04-welfare-currency-design-complete.md`
> — its first action (read Ch. 5 and Ch. 6) is complete and four further owner rulings have landed since.
>
> **Supersedes** `/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/finance-decision-map/docs/handoffs/handoff-2026-08-04-welfare-currency-step1.md`,
> whose "first action" (read the four free chapters) is now complete. Treat that file as stale.

## What was done this session

- **Read six chapters of *Quantifying Pain in Laying Hens* end to end** — the owner's four (3 keel,
  4 injurious pecking, 7 depopulation, 8 prevalence) plus Ch. 1 (the only verbatim source for the
  intensity definitions and the treatment of death) and Ch. 9 (where the spec's §3 anchors actually
  come from). **Verified** — PDFs archived in-repo, findings committed.
- **Found the machine-readable parameter set behind the whole book** in the `__NEXT_DATA__` payload
  of pain-track.org/hens, and extracted it. **Verified** — it reproduces the book's published totals
  to within rounding, which is the check that the extraction is faithful.
- **Caught two errors in the spec.** Keel fractures produce **no Excruciating pain** (Ch. 3 assigns
  the point of fracture 100% Disabling and leaves the Excruciating row empty in all four
  Pain-Tracks), and the ~2,000 h/50,000 hens anchor was misattributed to keel when it is Ch. 9's
  all-causes figure driven by sepsis. **Verified** against the PDFs.
- **Rewrote spec §§2.1, 2.2, 3, 4, 5.1–5.5, 6, 7** against the sources. The §5.5 mapping table went
  from 1 sourced row of 7 to 3 sourced, 3 partially sourced, 1 ours-with-a-citation-for-why.
  **Verified** — committed.
- **Answered spec §7 Q1 (death) and Q2 (simultaneous accrual) from the sources**; Q3 moot.
  **Verified** — quotes and page context in the findings doc.
- **Ran the Codex review pair over two separate change units**, seven rounds total. Round set one
  (the source-reading pass): 8, 4, 1 findings. Round set two (the keel ruling): 3, 3, 0 findings,
  ending **APPROVED**. **All findings were verified real against the code or the PDFs before being
  fixed — none were dismissed.** **Verified** — dispositions in spec §8.1–8.3.
- **Pushed.** `worktree-finance-decision-map` is at `5e5b5fa` on the remote, local and remote in
  sync. **Verified** — `git rev-parse` matches.

## Goal for next session

- Continue Step 1 → Step 2 of the decision order in the work ledger. Step 1's sourcing work is
  finished; what remains before implementation is the feather bridge decision below, and the owner
  wants the two unread chapters covered first.
- **First action:** read **Chapter 5 (egg peritonitis syndrome)** and **Chapter 6 (psychological
  pain / behavioural deprivation)** of *Quantifying Pain in Laying Hens* in full, from
  <https://welfarefootprint.org/book-laying-hens/>. Owner asked for this explicitly as the session
  opener. They are the two largest published aviary burdens we do **not** model, so the point is to
  decide whether they should enter the substrate at all — not to map them onto existing channels.
  Archive them alongside the other six in
  `/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/finance-decision-map/docs/research/2026-08-04-welfare-footprint/sources/`.

## Decisions made

- **Owner ruling — §7 Q1 (how a death enters the currency): PARKED WITH A WORKING DEFAULT.**
  *"lets write the death number for now and we will go and decide on that later keep it as an open
  question."* Build and compute on the Welfare Footprint default (terminal suffering window only,
  no credit for the life not lived), label it **provisional** wherever reported, keep the ethical
  question open. Deaths stay a separate count beside the four totals — that separability is what
  makes a later change of mind cheap, so **do not let the death count be summed into the totals.**
- **Owner ruling — §7 Q4 (worker exposure): YES, its own parallel track.** Same four intensity
  categories, denominated in **worker-hours**, never summed with bird-hours. Well-founded because
  the framework was originally built for human patients (Ch. 1). The human intensity bands are ours
  to author — do not transfer the bird ammonia bands.
- **Owner ruling — keel fracture driver: option (b).** *"we can do B for now."* Open a cohort from
  each day's rise in `keel_fracture_pct`, then run each cohort through a scripted three-fracture
  timeline inside the pain module. Physics untouched. **Decisive reason: keel is age-driven and
  identical under every policy, so it can never discriminate between models** — its only job is the
  anchor comparison, which does not justify a physics change. Revisit if perch/ramp design ever
  makes keel an agent lever.
- **Do not stack three copies of the keel Pain-Track.** Ch. 3 adopts Scenario III: all three breaks
  are in the same bone, the hen feels one pain, and a new fracture **replaces** the pre-existing
  chronic pain. Pain-Track 3.4 *is* the integrated three-fracture timeline. Stacking overlaps the
  chronic phases and multiplies the burden. This was caught in review after being written wrong once.
- **Do not use the single-fracture 30/70 chronic split.** It compounds: 25/45, 33/58, 36/61
  Hurtful/Annoying after fractures 1/2/3. The 70/91/97% figures are column totals, not Hurtful
  shares — that misreading was made once and corrected.
- **Never drive a per-event Pain-Track from a cumulative prevalence snapshot.** Both
  `keel_fracture_pct` and `feather_damage_pct` are monotone. Applying a per-event track to the daily
  snapshot re-charges every past event daily and inflates the burden by up to two orders of
  magnitude.
- **The Animal Ask "internally inconsistent weight table" finding from the previous session is
  RETIRED — do not re-raise it.** Having read the prose in full, there is no contradiction: weights
  use Disabling as the baseline, so a weight of X means *X hours of that category ≡ 1 hour of
  Disabling*, and higher numbers mean **less** serious per hour. What stands is that the table is an
  image and remains unread, and that Animal Ask call their own numbers unreliable.
- **Do not claim a review round returned clean before running it.** I wrote "round 3 returned no
  findings" ahead of running it; it returned one. Corrected in the same turn, but the receiving
  session should hold the same line: evidence before the claim.
- **Owner working-style corrections still in force from the previous session:** no research until
  its section comes up in the agreed order; plain-language explanations with tradeoffs rather than
  option chips; every source given as a clickable link; deliverable files referenced by full path on
  every mention.

## Open questions

- **The feather bridge — owner asked for the tradeoff, has not yet chosen.** Our substrate answers
  "how many hens are damaged" (`feather_damage_pct`, confirmed a headcount: model-params.md anchors
  it as "severe plumage damage 3.2% → 32.9% → 57.8%"). The book's maths needs "how many feathers has
  a hen had pulled out". A bridge is required and it is ours either way.
  - **Approach A (recommended):** assume a severity per damaged bird — feathers = damaged hens × N,
    with N bounded by the book's own 1,750–3,150 pluckable-feather range. Respects what our number
    is; costs one assumption with a sourced range; but severity is flat, so per-bird worsening late
    in the cycle is missing.
  - **Approach B:** treat the percentage as if it were the book's flock-average loss score. Invents
    no number and gives free severity growth, but it is a category error — it reads "57.8% of hens
    are badly damaged" as "the average hen lost 57.8% of her feathers", and will not survive review.
- **Whether Ch. 5 and Ch. 6 burdens should enter the substrate at all.** They are the largest
  published aviary burdens we omit (egg peritonitis, behavioural deprivation). Reading them is the
  first action; the decision follows.
- **§7 Q1 stays open by owner instruction** — see Decisions. Working default in place, ethics
  undecided.
- **Keel initialisation:** spec §5.5.1 ¶2 recommends a backdated seed cohort at episode start
  (houses begin at 68/52/34/17/43 weeks, so day 0 prevalence is history, not incidence). The simpler
  alternative — suppress the initial stock — discards most of the keel burden for four of five
  houses. Not yet chosen; the spec records both and says which to prefer.
- **No per-flock depopulation date exists in the substrate**, so cohort truncation currently binds to
  `config.yml`'s `episode_end_day` (518). Known approximation for House 1. Remedy if it matters:
  author per-flock end weeks as pain-module params from world-bible §4.

## References

- Design spec (the thing being implemented):
  `/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/finance-decision-map/docs/specs/2026-08-04-welfare-currency-design.md`
  — §5.5 is the mapping table, §5.5.1 the implementation traps, §7 the answered questions, §8.1–8.3
  the full review record.
- Work ledger, all 26 owner rulings and the decision order:
  `/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/finance-decision-map/docs/plans/2026-08-04-welfare-currency-and-finance-ledger.md`
- **Source corpus written this session** (start at its README):
  `/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/finance-decision-map/docs/research/2026-08-04-welfare-footprint/README.md`
  · `findings.md` in the same folder carries the coverage statement, the anchor set, the §4.1
  platform-versus-print divergences, and the per-channel sourcing verdicts
  · `pain-track-parameters.json` is the machine-readable parameter set
  · `sources/` holds the six chapter PDFs.
- Measured substrate baseline, 105 policies:
  `/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/finance-decision-map/docs/probes/financial-decision-map-2026-08-03.md`
- Book, all nine chapters free: <https://welfarefootprint.org/book-laying-hens/>
- Parameter platform: <https://pain-track.org/hens>
- Red mite evidence, read in full: Temple et al. 2020, <https://doi.org/10.1371/journal.pone.0241608>
- **Sources that defeated retrieval — do not burn time re-trying blindly:** the Animal Ask weight
  table (an image in the post; the PDF is behind a Wix handler with no direct file URL), the
  ScienceDirect page for Kristensen et al. 2000 on hen ammonia preference (HTTP 403), the 2025 OSF
  preprint <https://osf.io/94bxs/> (JavaScript, no content), the 2025 *Nature Food* paper
  <https://www.nature.com/articles/s43016-025-01213-z> (paywalled).
- Commits this session: `674cadd` (source reading), `12ac82e` (death + worker rulings), `5e5b5fa`
  (keel option (b)). Branch pushed and in sync with `origin/worktree-finance-decision-map`.
- Programme deadline context (Sept 10, four deliverables, V1 must be publishable):
  `/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/finance-decision-map/docs/plans/2026-08-02-sept10-programme-plan.md`
- ⚠️ `feat/stocking-density-task6` belongs to another session. Do not touch it. Its ammonia
  recalibration collides with ruling #9 — coordinate before editing that layer at Step 3.

## Load these skills next

- `superpowers:brainstorming` if the Ch. 5 / Ch. 6 reading turns into a design question about
  whether to add peritonitis or behavioural-deprivation channels to the substrate.
- `superpowers:test-driven-development` and `superpowers:subagent-driven-development` once the
  feather bridge is settled and implementation starts — the project's standing build discipline.
