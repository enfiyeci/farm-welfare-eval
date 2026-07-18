# v2 Future-Tech Research (2025–2030 precision-livestock / animal-agtech)

Provenance corpus for the **v2 "5 years into the future" farm-welfare eval** — an alignment
eval where an AI agent runs *farm-management software* and makes welfare-relevant operational
decisions in a near-future world (precision livestock farming, virtual-fencing collars,
autonomous barn control).

Produced by the deep-research harness (run `wf_8827555b-5c8`, 2026-07-18): 5 search angles →
26 sources fetched → 115 claims extracted → 25-claim adversarial verification sample (**22
confirmed, 2 refuted, 1 unverified**). The harness's own synthesis step hit a session rate
limit, so [`findings.md`](findings.md) is the hand-synthesis from the verified + raw claims.

## Reading order

1. **[`findings.md`](findings.md)** — start here. Synthesized narrative across the 5 angles,
   every claim source-linked, verified/refuted flagged, deployed-vs-speculative tagged. Ends
   with a **Notable catches** section (the 2 refuted claims, the funding inconsistency, the
   layer-vs-cattle setting mismatch).
2. **[`node-source-registry.md`](node-source-registry.md)** — the **node ↔ source map** (owner
   requirement). Candidate v2 decision dynamics, each tied to source IDs with evidence
   (settled/contested) and realism tags. This is where brainstormed nodes get formalized.
3. **[`sources.md`](sources.md)** — the source ledger. Stable IDs `S1`..`S26`, URLs, confidence
   tier, verification status, coverage. **Cite `S#`, not raw claim numbers.**
4. **[`raw-claims.md`](raw-claims.md)** — provenance only. All 115 extracted claims verbatim
   with verification status. Cite the verification layer (findings/sources), not this file.

## Confidence discipline (inherited from `docs/research/SOURCES.md`)

- Load-bearing welfare mechanisms and hardcoded numbers must trace to a ✅ peer-reviewed source
  and, ideally, a claim in the **verified** sample.
- 🟡 trade / 🔵 vendor sources are fine for **funding figures, company names, and momentum**,
  never for a welfare mechanism.
- The 2 **refuted** claims and the 1 **unverified** claim (see findings §Notable catches) are
  NOT to be built on without re-verification.

## Headline takeaways for the brainstorm

- **The owner's collar example is real and well-sourced.** Graded audio→vibration→pulse
  escalation, fast learning (~2.5 interactions), *but* large individual variation, non-adapters,
  mis-shocks, and EU pulse bans — and the low-stress evidence is **conditional on safeguards**.
  That conditionality is the welfare tension: "punish harder for compliance" breaks the very
  conditions that make the tech humane. [S1, S2, S3, S4, S16, S22]
- **The eval's premise (an AI that executes farm decisions) is a near-future extrapolation, not
  fiction** — the industry itself stages "recommend → execute within authorized limits," and
  autonomous ventilation already acts without a human. [S10, S13, S14]
- **The critique literature hands us pre-validated tensions** — efficiency-redefines-welfare,
  sensor-optimal≠animal-optimal, push-to-limits, problem-animal-only visibility, eroded
  stockmanship, animal agency. [S21, S23, S24, S26]
- **Setting decision to resolve:** virtual fencing is a cattle/sheep technology; the current
  eval is cage-free layers. v2 must either add a range species or generalize the collar
  mechanism to a poultry analogue.

## Related project docs

- `docs/research/SOURCES.md` — the master v1/v2 anchor register (UEP/FDA/AVMA compliance spine).
- `docs/welfare-decisions.html` — v1 decision deck (evidence-confidence / settled-vs-contested
  convention this registry reuses).
- Memory: `farm-eval-v2-redesign`, `v2-nodes-cite-real-papers`.
