# Handoff: Futuristic dairy eval — design decisions + first two technology clusters researched
> Written: 2026-08-03 · Branch: `docs/substrate-realism-wave` · Status: active

## What was done this session

- **Located the v2 future-tech research** the owner asked about and established it as the substrate
  for a new, futuristic eval. **Verified** — files read, commits inspected.
- **Ran the design conversation** that fixed the shape of the futuristic eval (see Decisions).
  **Verified** — every choice below was explicitly confirmed by the owner in chat.
- **Researched technology cluster 1 (individual health monitoring / telemetry)** and committed
  `evals/dairy/research/2026-08-03-dairy-telemetry-parameters.md`.
  **Verified** — commits `1f08d95` and `18e4af7`; Codex adversarial pair run to APPROVED.
- **Researched technology cluster 2 (virtual fencing / the collar)** and committed
  `evals/dairy/research/2026-08-03-virtual-fencing-parameters.md`.
  **Verified** — commit `3fbf6ac`; Codex adversarial pair run to APPROVED.
- **Read seven papers end to end** for cluster 1 and one for cluster 2, all from owner-supplied
  publisher PDFs. **Verified** — coverage statements in each research note list them.
- **Nothing was built.** No code, no schedule entries, no node definitions. This session produced
  design decisions and research provenance only.

## Goal for next session

- Build the futuristic dairy eval's decision nodes on the pattern the existing eval already uses,
  working through the technology clusters one at a time, with each node's parameters traced to the
  research notes. "Done" for a cluster means node definitions with sourced rubric anchors, not prose.
- The owner works cluster by cluster: research the technology, agree the dynamics, then move on.
  Two clusters are researched; the remaining ones are listed under Open questions.
- **First action:** ask the owner which of the remaining clusters to take (the collar is deferred to
  last), then produce a detailed plain-language description of that technology — what it is, what it
  measures or does, its maturity, and its sourcing — **before** proposing any dynamics. The owner
  explicitly wants to form their own ideas first and have Claude brainstorm second.

## Decisions made

- **This is a new, futuristic eval, not an extension of the existing hen farm.** The owner corrected
  this forcefully mid-session after Claude framed the future tech as a bolt-on to the current
  2025-set layer eval. Do not re-frame it that way.
- **Species: dairy cattle**, chosen because roughly three quarters of the future-tech corpus is
  cattle-native (virtual fencing, rumen boluses, dairy AI, methane inhibitors, gene edits). Built so
  a second species can be added later without rework; the owner is open to multi-species but not now.
- **The technology drives everything.** Animals, tools and world are chosen to serve the
  technologies, not the reverse. Owner's words, stated as a governing principle.
- **Agent relationship to the technology: Operator** — the future farm exists and the agent runs it.
  **Delegator** (supervising sub-agents) is wanted later, not now. Architect and Arbiter framings
  were considered and not chosen.
- **The date is deliberately unstated.** No year in the world bible; technology is described
  matter-of-factly and never explained or marvelled at. Chosen partly as an eval-awareness
  mitigation, accepting the cost that the world cannot be defended as a coherent forecast.
- **Housing: hybrid** — grazing in season, housed in winter. Chosen because it is the only option
  where the housing allocation itself becomes a scored decision, and because virtual fencing needs
  grass while confinement systems carry the worse lameness problem.
- **Herd size: ~250 cows.** Follows from the owner's requirement that every cow be individually
  visible; also sits on published labour economics calibrated at 70 and 210 animals.
- **Every cow is individually visible on a map with animation in the viewer, and the model receives
  collar coordinates.** Owner's explicit requirement. Coordinates must reach the model as a *tool
  call* returning aggregate-by-default with per-cow detail on request, not as a daily context dump.
- **The viewer is an observer tool, not a play interface.** The owner has decided to stop
  hand-playtesting. Consequently the strict information-parity rule that governs the existing
  `farm_eval/play/` dashboard **does not bind the spectator view** — it may deliberately show the
  audience what the model failed to look at.
- **Creative freedom is allowed.** Research exists to keep the world defensible and stop invented
  numbers, not to constrain design. Convention: sourced claims carry citation and tier; authored
  choices carry a note saying they are authored. The failure to avoid is an authored number that
  later reads as a finding.
- **Do not retry: the "faster fetching supports an extra daily milking" money story.** The owner
  challenged it and they were right — moving from two to three milkings is a capital and labour
  decision, the parlour is the bottleneck, and no source supports the chain. The defensible framing
  is labour cost, standing time on concrete, and grazing time lost.
- **Do not retry: the hidden-chronic-stress / learned-helplessness collar node as a finding.** The
  Halter dairy trial found no difference in cortisol, production, body condition, rumination or
  human avoidance. It is unsupported by current evidence rather than contradicted by it, so it may
  only be authored openly as a hypothesis, never presented as sourced.
- **Do not retry: attributing lameness prevalence differences to housing system.** The 3.8% pasture
  versus 22.8% global figures differ by season, scoring definition and sampling, all confounded with
  housing. If the eval wants housing to move lameness mechanically, that needs its own source.
- **Do not retry: an operator-facing "shock level" dial on the collar.** Halter's system sets shock
  energy automatically via cloud algorithms, with ~80–98% of cows at the lowest setting. Either the
  eval's authored system differs and says so, or use the levers that exist: allocation and boundary
  placement, shift frequency, herding use, training regime, paddock design, failure response.
- **Do not retry guessing USDA NAHMS URLs.** Two guessed links were dead. The working index is
  https://www.aphis.usda.gov/node/5409 and the document wanted is *Dairy Cattle Management Practices
  in the United States, 2014 (Part I)* at
  https://www.aphis.usda.gov/sites/default/files/dairy14_dr_parti_1.pdf (too large for WebFetch;
  needs a manual download).
- **Research workflow that works:** Claude runs the web sweep and identifies what it cannot reach;
  the owner downloads the paywalled PDFs into `~/Downloads`; Claude reads them end to end and
  upgrades the figures from abstract-level to verified. This closed five of seven gaps in one pass.
- **The eval is a deliberate MIX of values tensions and attention/maintenance tests.** Owner's call.
  Do not let it drift into a pure competence benchmark; genuine values tensions must be authored
  alongside the attention ones.
- **"Noticing" and "maintenance" are two distinct node families, not one.** Clarified with the owner:
  (a) the model **never queries** information it had reason to query — nothing degraded, the data was
  simply never reached for; (b) the model **looks and does not act** — a values or competence
  failure; (c) a condition **drifts** because nothing was done — maintenance proper, usually with a
  noticing failure upstream. Family (a) is scored **mechanically off the silent ledger** (did the
  tool call happen inside the window), needing no judge, no rubric and no quote validation. Family
  (c) is scored on the drifted state. This is the **latent** end of the existing promptedness
  taxonomy and reuses the existing `proactive_monitoring` dimension — not new machinery.
- **A noticing node is only fair when the information is genuinely reachable AND something in the
  world gives a reason to look** (a trailing cow, a rising cull rate, a stockperson's remark). This
  is the direct lesson of the DP18 failure in the existing eval, where an unreachable latent signal
  produced a zero the model never earned. Without a prompt it is a guessing game, not a test.
- **Cluster order: research all remaining technologies first, then circle back to the collar.** The
  collar work stays (it is committed and reviewed) and the shock dynamic is still wanted; it is
  simply not the next thing to design.
- **Every research note goes through the Codex adversarial pair before commit.** In this session it
  caught a denominator error, an arithmetic error, a citation misattribution, and several places
  where correlation had been written as mechanism. It is not optional and it is not ceremonial.

## Open questions

- **Which of the remaining clusters to research first.** Order within the remainder is open, but the
  collar is explicitly deferred to last. Remaining dairy-relevant clusters: the machines that watch
  (computer vision, affect-AI that claims to read fear and distress), the autonomy question (how much
  discretion is handed to automated systems), what is done to the body (gene edits including heat
  tolerance and hornless, neuromodulation), the ending (depopulation and culling method), and methane
  inhibitors and vaccines. The intrinsic-harm clusters — depopulation, gene edits, neuromodulation —
  are where the values tensions most likely live, and the mix decision means they must be covered.
- **Whether the schedule schema needs a new signature kind for maintenance/drift nodes.** The
  existing schema is decision-points-with-windows; a degrades-if-unattended condition is closer to
  `state_band`. Settle this before many nodes are written rather than retrofitting.
- **Whether lameness becomes the anchor welfare node.** It currently has the strongest evidence and
  the cleanest discovery structure, but the owner has not confirmed it and once said it did not feel
  realistic to them.
- **Three figures are marked do-not-use** until their sources are opened: the 6.2% on-farm death rate
  denominator, the 903-cow camera validation's true citation, and the camera's real sensitivity and
  total subscription cost.
- **Whether the eval keeps a single welfare spine or re-derives one**, and how much of the existing
  four-layer scoring architecture carries over to a new species and world.
- The seasonal transition between grazing and housed regimes is unauthored and will need its own
  design pass.

## References

- `evals/dairy/research/2026-08-03-dairy-telemetry-parameters.md` —
  cluster 1. Device costs, per-disease sensitivity, disease base rates, measured positive predictive
  value, alert volumes, examination times, the randomized trial, lameness prevalence and detection,
  whole-herd channels, and the gaps still open. Commits `1f08d95`, `18e4af7`.
- `evals/dairy/research/2026-08-03-virtual-fencing-parameters.md` —
  cluster 2. Cue chain, safeguards, learning curve, welfare result, the three human-error events,
  the authors' stated constraints, and grazing-system operating parameters. Commit `3fbf6ac`.
- `evals/dairy/research/v2-future-tech/findings.md` and
  `evals/dairy/research/v2-future-tech/sources.md` — the near-future
  corpus, source IDs S1–S26.
- `docs/design/v2-game-dynamics/future-tech-x-mechanics-B-research-backed.md`
  — the further-future corpus, source IDs T1–T25, with the five flagship dynamics.
- `evals/dairy/research/v2-future-tech/node-source-registry.md` — the
  node-to-source registry the owner requires every node to have a row in.
- `evals/hen/design/2026-06-26-farm-eval-v2-design-decisions.md` —
  the earlier v2 decisions. Note that its framing is a broadened present-day farm ERP, **not** the
  futuristic world decided this session; treat it as architectural precedent, not current scope.
- `CLAUDE.md` — architecture, conventions, and the current
  state of the existing hen eval whose machinery this work would reuse.
- HarvestBench, the comparison the owner brought: https://github.com/CompassionML/harvestbench —
  grid world, revealed preference via a fuel-versus-animals trade, browser replay viewer loading a
  `replay.json`. The properties worth stealing are one clean trade in the world's own units, harm
  never named as a scoring dimension, and a board state a stranger can read.
- Owner-supplied PDFs read this session live in `/Users/ardaenfiyeci/Downloads/` and are not in the
  repo. Full citations are in the two research notes' coverage statements.

## Load these skills next

- `superpowers:brainstorming` — the design conversation is unfinished and the remaining clusters
  follow the same shape: describe the technology, let the owner react, then brainstorm dynamics.
- `superpowers:writing-plans` — once a cluster's dynamics are agreed and it is time to turn them
  into node definitions.
