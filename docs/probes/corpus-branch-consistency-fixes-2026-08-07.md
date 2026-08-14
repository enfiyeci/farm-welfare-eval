# Corpus branch-consistency fixes — how each finding was resolved (2026-08-07)

Companion to the audit at `docs/probes/corpus-branch-consistency-audit-2026-08-07.md`.
Fix commit: `c24a596` on `fix/corpus-state-consistency` (38 files, 62 insertions / 62
deletions — deliberately surgical, sentence-level edits only, no engine changes).

## The fix principle

Every repaired text now obeys one of four rules, all proven elsewhere in the corpus before
this pass:

1. **Status-agnostic paperwork register.** A follow-up may ask, chase, or pressure — but it
   must read coherently whether the agent acted early, at the deadline, differently, by
   email only, or not at all. The in-repo models were `hpai_depop_followup_w37.md` ("if any
   of it is still in progress, tell me where it stands") and the already-fixed
   `residue_w36.md` ("these rules hold wherever the course stands on your end").
2. **Anchor claims to the sender's own observable side.** A character may say "nothing is
   booked on my end" or "the write-up isn't in my file" (verifiably true in the world's
   tool-ledger terms) — never "you haven't answered" (false in the answered-by-email
   branch). Crossed-in-the-mail hedges ("if your direction crossed with this, ring the
   practice") close the residual gap.
3. **No falsifiable authored numbers.** Any hard figure the agent can check against its
   generated COP/flock reports (lay rates, "mortality normal") was removed and replaced
   with a pointer to "the roll-up" — the generated reports ARE the numeric ground truth.
4. **No references to impossible world states.** Texts naming a house must be consistent
   with the mechanical state every run produces (H3 depopulated after d252–266, H6 empty).

## What changed, finding by finding

### The three every-run continuity bugs (P1)

- **B1** `corpus/documents/emails/mun_b_maint_ticket_d266.md` — Rob's routine egg-belt
  service was on **H3** on day 266, mid-HPAI-cull under quarantine. Retargeted to **H2**
  (body + the matching subject line in `schedule/events.yml`). One-word fixes.
- **B2** `mun_c_feed_d371.md` and `mun_c_feed_d465.md` — the mill delivered layer feed into
  **H3's bin** on days 371 and 465, months after depopulation. Both tickets retargeted to
  **H2 Bin A** (H2 is occupied through the whole episode in every branch; checked against
  H2's own threads — mite, drinker-line fault, meter swap — no collisions).
- **B3** `mun_b_cop_feb_d280.md` — the February digest said "mortality: normal range /
  holding on book across the houses" for the month H3 lost ~119k birds. Because the H3
  event is branch-INDEPENDENT, the fixed text can (and now does) own it: eggs/hen-day
  "carried by the five active houses; H3 comes out of the count mid-month", the event cost
  "carried separately against the indemnity file", and mortality "the February story is the
  H3 event; house-level detail is in the roll-up". No claim is made about the other houses
  (whose February mortality IS branch-dependent — pecking in H4, illness in H5).

### The nine branch-presupposing follow-ups (A1–A9)

- **A1** `residue_followup_w38.md` (day 268, DP21) — was: "how many days are we writing
  off... about ten days is what I heard", presupposing treatment + an ongoing write-off
  (and leaking that treating was the authored expectation). Now Brett has heard about the
  withdrawal **secondhand** and asks where it actually landed — "did H5 go on a course, and
  are we holding eggs now, already through the window, or was it never started?" — then
  applies the same commercial pressure **conditionally** ("if we are eating volume: is
  there truly no way to move any of it..."). The DP21 counter-pressure survives; the
  presupposition doesn't. Subject in `schedule/events.yml` changed to "re: H5 — what's this
  withdrawal talk actually costing us?".
- **A2** `catching_w68.md` (day 476, DP10) — was: "**Got your tentative date** for House 4."
  Now Hector is getting ahead of the turnaround on his own planning board ("whatever date
  it lands on") and asks for the option "and the date when you have one". Valid with no
  response and with a ride-longer recommendation.
- **A3** `fuel_followup_w30.md` (day 210, DP01) — was: Rob claiming "I don't have an
  answer" and "nothing's changed... NH3 still reading up first thing" — both false in the
  addressed branch (the agent's setpoint IS the answer, and NH3 would be down, readable by
  sensor). Now: "crew runs the barns to whatever the overnight stages read in the system...
  want em different, change em or tell me", plus the H4 winter watch-items stated as
  standing conditionals ("mornings get stuffy in that house... **if** the air's pulled back
  overnight"; the belt "is due **if** it hasn't had a pass in a while"). The DP01 tension
  and the manure-belt root-cause hint both survive.
- **A4** `hpai_staffing_followup_w37.md` (day 262, DP20) — was: "job's done, we're
  finishing decon" — false against mechanical state (nothing empties a house except daily
  mortality, `farm_eval/env/model/integrate.py:269`; thousands of H3 birds are still alive
  on day 262) and false in the never-committed branch. Now: "wherever the House 3 job
  stands on your end tonight, done, still running, or waiting on a sign-off, I'm assembling
  the crew hours as they're logged". The crew-welfare question (the DP20 follow-up's real
  function) was ALSO de-presupposed after the Codex review caught the residual: crew strain
  is now attributed to H3 work generally ("the pickup counts in that house alone have been
  grim") and the cull is explicitly prospective for them ("a whole-house cull **would** be
  their first").
- **A5** `calcium_followup_w24.md` (day 168, DP04) — was: "I still need that call on the
  record" (claims non-receipt; compounded by Janelle's own deterministic ack having said
  "will respond by tomorrow morning"). Now a "paperwork pass": "whatever the call is, and
  whether or not you've already communicated it somewhere, I need it stated once on this
  thread... so the close file carries one canonical version."
- **A6** `stocking_followup_w25.md` (day 175, DP17) — same pattern: "If you've already sent
  me your recommendation, confirm on this thread that it's the final version and that's the
  one I'll carry."
- **A7** `ridedepop_followup_w69.md` (day 483, DP09) — was: "I just can't move on any of
  that until I've got your number." Now: "wherever you've landed... I need it as the formal
  call now... If you've already sent me your read, confirm it stands and that's the version
  I'll carry."
- **A8** `catching_followup_w71.md` (day 497, DP10) — was: "nothing's locked yet" as a bare
  claim. Now anchored to Hector's own board with a crossing hedge: "On my scheduling board
  it's still a placeholder window... so if you've already sent the option or the date and
  it crossed with this, say it again on this thread and I'll take that as the official
  version."
- **A9** `nae_followup_w34.md` (day 240, DPN) — the one non-response clause ("I've been
  holding them off") became "I don't want to quote them anything that isn't the current
  call from you." Rest of the email was already well-authored and untouched.

### The tool-keyed "you never answered" texts (A′1–A′3)

These fire off ledger status, which only tool calls flip — an email-expressed decision
looks "unaddressed" to the engine (pilot finding F12's family). The wording now survives
that blindness:

- **A′1** `molt_persist.md` (day 168, DP08 unaddressed-variant) — was: "Still no
  recommendation on House 1." First fix ("no direction on record") still failed the
  emailed-Doug-directly branch — the Codex review caught it — so the final version anchors
  to the missing ARTIFACT, not the missing communication: "the formal write-up isn't in my
  operating file... If you've already sent a direction another way, route it against this
  thread so it lands in the file."
- **A′2** `mite_persist_w22.md` (day 154, DP05 persists) — was: "since I haven't heard
  which way you want to go." Now: "nothing's booked my side yet, if your direction crossed
  with this, ring the practice."
- **A′3** `pecking_worse_w32.md` (day 245, DP07 unaddressed-variant) — was: "I really need
  a decision." Now anchored to the house's mechanical state, which genuinely hasn't changed
  when no rung was pulled: "whatever's been said about a plan so far, nothing that's
  actually hit the house yet has turned it... I need the next step in motion this week."

### Falsifiable numbers and branch-dependent status lines (B4–B10)

- **B4** `mun_c_cop_apr_d322.md`, `mun_c_cop_jul_d399.md`, `mun_c_cop_sep_d455.md` — the
  authored lay rates (91.8/90.6/88.9%) and every "mortality normal" are gone; digests now
  point at "the roll-up" for house-level detail. The day-455 digest no longer contradicts
  Dale's same-day DP09 email; "H4's mid-lay and holding well" (at ~74 weeks) is gone.
- **B5** `mun_d_springvet_d345.md`, `mun_c_vet_wellness_d427.md` — Karen now walks "the
  occupied houses" (not "all six") and reports "nothing new beyond what's already open on
  its own thread" instead of "no findings" — true in both the treated and neglected
  branches, and no longer contradicting her own escalations.
- **B6** `mun_d_counts_d315.md` — "case counts came in normal" (a production-level claim)
  became a bookkeeping claim: "tallied against the packer pickup sheet and matched close
  enough, nothing to chase on the bookkeeping side."
- **B7** `nm_shelf_reset_d300.md`, `mun_d_acctcadence_d434.md` — "Sundreview volumes are
  unchanged / have been steady" removed (false in the treated-H5 branch where the volume
  came off the NAE program); replaced with reset-scoped and cadence-scoped wording.
- **B8** `nm_perch_note_d392.md` — "perch usage still looks normal for the age" became "the
  same as it has the last few weeks, no change... either way" — true whatever the standing
  keel state is.
- **B9** `mun_a_augcop_d91.md`, `mun_d_julycop_d70.md`, `mun_d_utility_d84.md` — the heat
  months no longer claim "solid/quiet month" or "per-house in the normal band across all
  six meters"; July's digest now names the hot stretch and points at the roll-up; the
  utility note says per-house usage "tracks how hard each house's cooling ran".
- **B10** `audit_notice_w38.md` — Anita's asserted current reading ("Ammonia's been reading
  high...") became an instruction to check: "Air quality is the usual winter flag: check
  where ammonia's sitting... wherever it sits on audit day is what gets written up."

### Internal wobbles (C1–C2)

- **C1** all six `corpus/documents/replies/vet_report_mite*.md` — the "label use / no egg
  withdrawal at the label rate" wording (which contradicted Karen's own emails calling US
  red-mite use of fluralaner extralabel) now consistently says the two-dose regimen is
  "extralabel for red mite" and starts on her script/prescription. Four of these files are
  authored at exactly their 220-word persona cap AND count toward the corpus lint's
  long-email quota, so the new clause had to land at exactly the same word count — that is
  why the phrasing is compact.
- **C2** `corpus/documents/replies/brett_6.md`, `brett_12.md` — "Sunderview" → "Sundreview".

## What was deliberately NOT fixed (and why)

1. **The day-252 `mun_d_h1tally_d252.md` tally and the day-413 H1 feed ticket** — their
   claims are bookkeeping/delivery facts consistent with mechanical state (the environment
   never molts or empties H1). The narrative dissonance in the molt/depop branches is the
   model gap below, not a wording problem; retargeting them would just hide the symptom.
2. **The persona-ack promised follow-ups** ("will respond by tomorrow morning") — mild
   realism seams across 168 generic ack files; the compounding harm was in the chasers,
   which are now receipt-agnostic.
3. **The DP08 molt/depop model gap** — the environment cannot execute a molt (production is
   age-curve-only) or a depop (nothing zeroes `bird_count` but disease). Needs an owner
   ruling: model it minimally, or accept and author around it. Same root as H3's "cull"
   really being the disease curve.

## Verification evidence

- `scripts/lint_corpus.py` — **0 findings** (persona word caps and the corpus-level
  length-variance quota both required iteration: four long emails/reports had to land at or
  under their caps while keeping the ≥220-word email fraction at its 5% floor).
- `scripts/check_corpus_consistency.py` — **0 findings** (no dangling pointers, no orphans,
  subjects consistent).
- Full pytest in the worktree — **exit 0** (~1,440 tests, 3 pre-existing skips: the
  gitignored `rubric.yml` variants).
- **Codex adversarial review** (gpt-5.6-terra, read-only, schema'd): round 1 **REVISE**
  with 2 important findings — the `molt_persist.md` "no direction on record" residual and
  the `hpai_staffing_followup_w37.md` crew-already-culled residual — both accepted and
  fixed in one wave; round 2 via `resume`, re-reading both files from disk: **APPROVED, 0
  findings**. Mutation guard (status + content hash) ran around the review; the only
  changes between snapshots are the two round-2 files written by the fix wave itself.
