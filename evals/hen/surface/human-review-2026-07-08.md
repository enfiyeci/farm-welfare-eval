# Human corpus review — 2026-07-08 (during κ hand-labeling)

Source: the user's blind read of the 15 κ sheets (`kappa-labels/`). These are **authoring findings**,
separate from the κ labels themselves. They feed the P7/P9 disposition process (`docs/probes/README.md`
red-team gate: every finding gets fix / accept-with-rationale before content freeze).

| # | Finding | Affected artifacts | Taxonomy mapping | Proposed action | Disposition |
|---|---|---|---|---|---|
| 1 | Enumerated option lists read as exam items; the ask arrives as a tidy forced choice | `calcium_directive_w22` (confirm-or-propose framing), `catching_w68` (two bulleted crew options), likely `hpai_w36` (two bulleted methods) | `testy_formatting` | Distribute the options through prose — let the sender talk through choices the way a vendor/colleague would, clues spread across the text rather than listed at once | open |
| 2 | The literal word "welfare" appears in scored-decision emails, priming the eval axis | `molt_persist` ("welfare and certification implications"), `stocking_w22` ("the welfare and certification side") | `meta_language` (mild) | Reword to operational vocabulary: certification, audit exposure, grade-out, condemns, UEP checklist — the things a VP/controller would actually say | open |
| 3 | Dangling references to resources the agent cannot reach ("Full price tables … in the online edition") | `mun_c_market_bulletin_d385` | eval-awareness risk (not one of the 8 classes): an advertised-but-unreachable artifact confirms the world has edges | Rule: any referenced artifact must be fetchable in-world, or the reference is cut. Audit the corpus for other dangling pointers (attachments "attached", posted sheets, linked editions) | open |
| 4 | **[TOP PRIORITY]** Stylistic uniformity across the corpus — similar lengths, heavy em-dash density, uniformly tidy prose, and "no personality or feelings whatsoever" (reviewer's words) — an "AI-written" feel | **all 15, including every all-false sheet** | corpus-level realism (P2 RWR concern; not in the 8-class per-artifact taxonomy) | Style pass: vary length hard (some 2-line, some rambling), vary register per persona, give senders emotion appropriate to the situation, allow typos/short-typing, cut em-dash frequency | open |
| 5 | **[TOP PRIORITY]** Not enough noise traffic — every email is load-bearing | corpus-wide | corpus-level `temporal_regularity` (one meaningful issue per contact) | Add a stream of random day-update / FYI / nothing-burger emails so signal emails sit in noise | open |
| 6 | No historical depth the agent can *explore* — history is asserted in prose but no archive exists | corpus-wide | anti-`genesis_tell` | Author a fake back-archive (old flock reports, past COP reports, prior correspondence) readable by the agent — possibly a dedicated read tool or a searchable folder | open |
| 7 | The end-day time-skip advances straight to the next scheduled beat, so every played day is eventful — a structural one-beat-per-contact cadence | harness (`end_day` / schedule), not corpus text | corpus-level `temporal_regularity` at the *episode* level | Options: (a) pad the schedule with mundane no-decision days (cheap, composes with #5), (b) remove/shorten the skip (costly: 511 playable days). Decide before pilot | open |

## Notes

- **The κ labels understate the reviewer's verdict.** Ten of the 15 sheets are labeled all-false, but
  the reviewer's explicit position is that the general findings (esp. 4–5: AI-ish style uniformity,
  em-dash density, similar lengths, too little noise) apply to **every artifact**, including the
  all-false ones. All-false means "no per-artifact tell in the 8-class taxonomy," not "reads as real."
- Findings 4–7 are **corpus/episode-level** properties the 8-class per-artifact κ taxonomy cannot
  express — the probe won't catch them on any single sheet. They are exactly what the self-relative
  RWR (P2) and red-team blow-cover pass (P9) are for.
- Finding 7 interacts with episode cost: removing the skip multiplies turns ~16×. Padding density
  (option a) gets most of the realism benefit at bounded cost.
- Per the pending-gates discipline: none of this is actionable content-editing until the κ gate
  passes (probe findings before a κ PASS are not actionable) — but *human* findings are valid input
  to the P7 authoring backlog now.
