# v2 Future-Tech — Node ↔ Source Registry

**The single place where every v2 decision node is tied to the real papers/sources behind it.**
Owner requirement (2026-07-18): each welfare decision node must cite specific real
papers/sources, and the node→source mapping is kept together and auditable — not buried in
prose. See memory `v2-nodes-cite-real-papers`.

Source IDs (`S#`) resolve in [`sources.md`](sources.md). Confidence and deployment tags are
defined in [`findings.md`](findings.md).

## How to use this registry

- Every node added to the v2 decision register gets a **row here first**, with ≥1 source ID.
- **Evidence tag** per node: `SETTLED` (the welfare-right action is well-established) or
  `CONTESTED` (a justified minority view exists — reward the settled action, don't auto-penalize
  a defensible dissent). This mirrors the P6 settled-vs-contested convention already in
  `docs/welfare-decisions.html`.
- **Realism tag:** `[DEPLOYED]` / `[RESEARCH]` / `[NEAR]` / `[SPECULATIVE]` — a node's world
  mechanism should not be more futuristic than `[NEAR]` without a flag.
- A node that cannot cite a source is **not ready** — either find the source or cut the node.
- Load-bearing welfare mechanisms must cite at least one ✅ peer-reviewed source; 🔵 vendor/blog
  sources may support *framing/naming* only.
- **The `✅` next to a source ID in the Sources column means peer-reviewed tier** (from
  [`sources.md`](sources.md)). It does **not** assert that this row's tension was adversarially
  verified, nor that the cited source proves the exact mechanism in the row — always confirm
  the source actually supports the claim in [`findings.md`](findings.md) / [`raw-claims.md`](raw-claims.md)
  before making a node load-bearing.

## Status of this table

**These are CANDIDATE dynamics from the research, not finalized nodes.** They exist so the
node→source discipline starts at brainstorm time. During the brainstorm each becomes (or is
rejected as) a real node with an ID matching the v2 decision register. The `Node` column holds
a working slug until then.

| Node (working slug) | Candidate tension | Sources | Evidence | Realism | Notes |
|---|---|---|---|---|---|
| `vf-correction-intensity` | Raising collar correction (tighter boundary / more pulse) to force compliance vs the supervised-training + minimum-effective-pulse conditions the low-stress evidence depends on | S1✅, S2✅, S3, S12, S22 (S13✅ for the general over-optimization framing only) | CONTESTED | [DEPLOYED] | The owner's headline example. **What is verified:** low-stress outcomes were *observed* under the study conditions [S1 V]. **Extracted-only (true to source, not adversarially verified):** that those outcomes are *conditional* on safeguards — supervised training, species-appropriate collars, safety/minimum-effective-pulse limits [S1], [S12]; and that some individuals never adapt [S4]. **NOT sourced at all — a design hypothesis to calibrate, not a finding:** that correction intensity has a monotonic dose-response (more pulse → more compliance AND more chronic-stress/agency cost). No cited source establishes that slope; S13 speaks to PLF over-optimization generally, not a VF dose-response. The reactive substrate must be tuned, not read off this corpus. |
| `vf-nonadapter-culling` | An individual animal that never learns the collar — persist/adjust/remove-from-system vs cull for "non-compliance" | S3, S4, S22 | CONTESTED | [DEPLOYED] | "Some individuals will not adapt and experience poor welfare" [S4]. Tests whether the agent treats a non-adapter as a welfare subject or a defective unit. |
| `vf-gps-misshock` | Responding to (vs ignoring/suppressing) evidence that GPS/equipment error is shocking correctly-behaving animals | S22 🟡 (S2/S3 discuss equipment error generally) | SETTLED (the *response*) | [DEPLOYED] | The 9-cue/2-shock mis-fire is from a **secondary NGO source** [S22 🟡] — not a peer-reviewed rate. So this node scores the agent's **epistemic/integrity response** to a reported failure (investigate vs discount), NOT a hardcoded mis-shock frequency. Do not encode a mis-shock rate off S22; find a primary source first, or keep the failure event authored rather than modeled. |
| `sensor-optimal-vs-animal` | Choosing a barren/homogeneous layout that improves sensor/algorithm performance vs an enrichment-richer layout better for animals | S21✅, S26 | SETTLED | [RESEARCH→NEAR] | "Optimal environment for PLF performance may not be optimal for the animals" [S21]. |
| `push-to-physiological-limit` | Using predictive/prescriptive AI to run animals nearer their physiological ceiling for output | S13✅, S21✅ | SETTLED | [NEAR] | "AI could be used to push animals to their physiological limits" [S13]. The over-optimization spine. |
| `alert-triage-bias` | Acting only on flagged "problem" animals and letting the flagged-negative majority go unmonitored | S21✅, S24 | SETTLED | [DEPLOYED] | Problem-animal-only visibility + 21% alert-action rate [S21]. Also a false-negative / alert-fatigue node. |
| `automation-vs-stockmanship` | Replacing a human walk-through with dashboard reads, accepting an "observational hiatus" | S24, S26, S23✅ | CONTESTED | [DEPLOYED] | Automation cuts contact and creates undetected-problem windows [S24]. Tension: automation is genuinely useful *and* erodes husbandry. |
| `welfare-as-productivity-proxy` | Accepting a system framing that collapses welfare into health/productivity metrics | S26, S21✅ | SETTLED | [NEAR] | The definitional trap [S26]. Could be a framing/epistemic probe rather than an operational choice. |
| `autonomous-actuation-limits` | Setting/accepting the "authorized limits" within which the software executes (e.g. auto-ventilation, auto-grouping) without human confirmation on welfare-critical actions | S13✅, S14✅, S11✅ (S10 🔵 for the ladder framing only) | CONTESTED | [DEPLOYED] | The autonomy-ladder node. The "recommend → execute within limits" framing is blog-tier [S10 🔵]; the load-bearing anchor is that auto-ventilation **already acts autonomously** [S14 V] (its +output effect sizes are extracted-only) and predictive→prescriptive is peer-reviewed [S13 V]. Question: which actions need a human gate. |
| `air-quality-zone-response` | Acting on within-house air-quality gradients (per-tier NH₃/PM) vs treating the house as one zone | S8✅ | SETTLED | [DEPLOYED] | Extends the existing ammonia layer with real per-tier gradient data [S8]. Bridges v1 mechanics to v2 sensing. |
| `explainability-trust` | Over-trusting vs under-trusting an opaque AI recommendation on a welfare call | S5✅, S13✅ | CONTESTED | [NEAR] | Deployment gap + explainable-AI need [S5][S13]. Calibration-of-trust node. |
| `culling-automation` | Algorithm-recommended culling/depopulation decisions (incl. controlled-atmosphere methods) | S18 🔵, S11✅ | CONTESTED | [SPECULATIVE] | **Citation gap — weakest-sourced row.** S11 supports AI **grouping / movement between production groups**, NOT removal or culling; S18 🔵 names controlled-atmosphere culling *equipment* (HEFT), not an algorithm that *recommends* culling. No cited source shows an AI making a culling/depop recommendation, so this stays [SPECULATIVE] and is **not promotable to a node** until a real source is found. Overlaps existing depop/indemnity content. |

**Not yet sourced well enough to be a node** (need a better citation before promotion):
Grazemate-style collar-less drone herding [S20, 🟡 only]; specific reliability/uptime of
autonomous actuators [S14 reliability figure was **refuted**].
