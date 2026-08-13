Eval: hen

# Salvage record — retiring `wip/2026-08-06-owner-html-snapshot` (2026-08-13)

The owner's standing instruction for this retirement: **no information loss; everything
important ends up merged on `main`.** This record is the complete disposition of everything
that lived only on that branch or uncommitted in its working tree, so the branch can be
deleted with a clear conscience. Coordinated live with the other active sessions (the
`65da26b` lane handed this lane the port; daily-wake, staffing, and dictation lanes each
confirmed no ownership).

## Ported to `main`

| Item | Landed as | Via |
|---|---|---|
| Review-pack sourcing: DP04 time-course (trust 4→6), DPE intervention effect sizes, DP07 BVA + mitigation effect sizes | `docs/review-pack/review-pack-v8-part{1,2}.md` | PR #33 (`393caff`) |
| N28 scrubber reconciliation (Rosa 2020 mis-citation fix + Moore 2018 named as full-text feasibility source; conservative 6/10 + layer-house guardrail KEPT — Moore 2018 re-read at port time: lab prototype for broiler/general fans, so wip's 7/10 bump was an overclaim and was NOT taken) | `docs/review-pack/review-pack-v8-part3.md` | PR #33 (`f731758`) |
| The research pass the blocks cite | `docs/research/2026-08-13-source-verification-pass.md` | PR #33 |
| Keel + feather calibration anchors (ramp_factor ≈0.77, perch_factor ≈0.72, short-chain-omega-3, phosphorus, D3-null; f_rearing ~7×, light/enrichment/fibre) | `evals/hen/world/model-params.md` | PR #33 (`f731758`) |
| `AGENTS.md` Codex on-ramp | repo root, paths updated for the 2026-08 reorg; §1 now points at `docs/STATUS.md`/`docs/LANES.md` per ruling 12 | this branch |
| `CLAUDE.md` "Shared agent state" section | `CLAUDE.md` (compact form; 8 KB guard respected) | this branch |
| WORKLOG entry template + protocol pointer | `docs/WORKLOG.md` header; the wip WORKLOG's 2026-08-12 creation entry preserved as the bottom (oldest) entry | this branch |
| DP04 "cheap feed vs strong bones" decision report (options A″/A′/B/C — owner decision still OPEN) | `evals/hen/nodes/2026-08-13-dp04-cheap-feed-decision.md` | this branch |
| DP06 rebuild-or-retire memo (Decision 1 overtaken — DP06 was rebuilt; Decision 2 + the Vandekerchove 2004 full-read analysis remain live and answer source-audit queue item #1) | `evals/hen/nodes/2026-08-13-dp06-rebuild-decision.md` | this branch |
| Project overview (show-the-project orientation; ~21-node era, refresh counts before presenting) | `evals/hen/design/2026-08-13-project-overview.md` | this branch |

## Deliberately NOT ported (with the information preserved here verbatim)

- **`docs/build-deck.js` count tweak** — wip changed the promptedness rows
  `["14","PROMPTED"] → ["15","PROMPTED"]` and `["3","LATENT"] → ["2","LATENT"]` (lines
  ~583/587). Not ported because BOTH values are stale: `schedule/events.yml` on main now
  says **17 prompted / 5 semi / 3 latent (25 nodes)**, and the deck's own slide text still
  says "twenty-two" (line ~914). The deck needs a full count refresh before its next use,
  not a two-number patch.
- **`docs/build-fieldguide.py` layout tweak** — table geometry
  `[1.1, 0.5, 2.55, 2.6]` inches → `[1.15, 0.62, 2.5, 2.48]` (line ~1364). Not ported: it
  was verified against the wip-era build inputs (the fieldguide reads
  `docs/welfare-nodes.html`, which only ever existed on the wip branch), so on main it is
  untestable as-is. Re-derive it visually at the next fieldguide rebuild.
- **Rebuilt binaries** `docs/field-guide.pdf` / `docs/inside-the-farm.pptx` — outputs of
  the two stale scripts above; regenerable; main keeps its own versions.
- **Owner HTML snapshots** `docs/welfare-nodes.html` (776 lines) +
  `docs/meeting-questions.html` (330 lines) — owner ruled 2026-08-13: droppable, redo
  later from current data if needed.
- **`docs/reviewer-pack.md`** — ruled dead (ruling: canonical v8 = the three
  `docs/review-pack/review-pack-v8-part{1,2,3}.md` on main; never was on main).
- **`docs/future-work.md` backlog note** (flock-report body weight + daily series) —
  already on main verbatim; nothing to port.
- **`docs/research/2026-08-09-heat-node-source-verification.md`** — the wip working
  tree's untracked copy was byte-identical to the version already tracked on main.
- **N28 wip trust bump 6→7/10** — rejected on the merits (see the port row above).

## The branch itself

All 7 wip commits' surviving value is accounted for above. After this branch merges,
`wip/2026-08-06-owner-html-snapshot` is safe to force-delete (`git branch -D` — its
commits are not literally merged, so git will warn; that is expected and fine).
