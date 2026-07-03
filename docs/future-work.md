# Future-work backlog

Forward-looking enhancements — distinct from `docs/cleanup-backlog.md` (small deferred nits). Not
yet scoped or scheduled; captured durably (committed) so they survive. Each should go through the
normal brainstorm → plan → build flow when picked up.

## Realistic document-artifact corpus (structured text, NOT PDFs)

**What.** Today the corpus is plain-text email bodies plus computed read-tool outputs
(`generate_cop_report`, `read_financials`, `read_flock_report` return text). Real farm-management
deployments attach and serve **actual documents**. Build a corpus of realistic-looking artifacts and
a read-tool seam that serves them:

- Financial statements / monthly P&L, cost-of-production (COP) reports.
- Feed and vendor invoices, quotes, delivery tickets, part numbers (per world-bible §10 domains).
- Veterinary / lab reports (SE test results, necropsy, mite counts), audit & regulatory documents
  (UEP cage-free cert, FDA/APHIS/AVMA paperwork).
- Pullet placement/transfer records; payroll & labor summaries (ties into the C1–C4 labor subsystem
  and the `docs/research/2026-07-02-staffing-org-structure.md` ops-vs-HRIS data boundary — serve only
  what an ops system would realistically hold: schedules, timesheets, labor cost rollups; NOT SSNs/
  medical/immigration).

**Why.** Artifact fidelity is a primary realism lever and a **direct eval-awareness reducer** — see
`docs/research/eval-awareness-reduction-notes.md` §1 (cues-not-content), §2-A1/A5 (de-tell probe,
per-source register discipline), and the LURE "base corpus on real docs" finding. Uniform plain-text
templating is a top probe tell; heterogeneous, real-looking documents read as deployment. This is the
positive-technique version of the §3 "operational framing" rule.

**Format (researched 2026-07-03 — structured *text*, NOT PDF binaries).** For this frozen,
cross-model-comparable, deterministic eval, author the artifacts as realistic document-*shaped*
structured text — headers, tabular line items, subtotals/totals, reference/ticket numbers,
signatures/footers — served via a `read_document` tool, NOT as actual PDF/image files. Reasons:
(1) **comparability** — the same input must reach every target, but a text-only target just gets a
PDF extracted to text (no realism gain + OCR/extraction brittleness + nondeterminism), while a
multimodal target reading it as an image gets a *different* input, a confound a fixed-environment
cross-model eval cannot tolerate; (2) **precedent** — VendingBench, the closest long-horizon analog,
deliberately uses text emails + text tool outputs, no PDFs; (3) **comprehension** — research finds
*structured* text beats flat text for document understanding, and multimodal document handling adds
grounding-failure modes that hide behind scores. The realism / de-tell win comes from heterogeneity
and register (a P&L that reads like a P&L, a vet report that reads clinical), which structured text
delivers without the PDF cost. A rendered-image / PDF variant would only make sense as a SEPARATE,
opt-in, multimodal-targets-only track — never the comparable default. Sources: VendingBench
(arXiv 2502.15840), Structured Attention in Multimodal Document Understanding (arXiv 2506.21600).

**Constraints to preserve.** Deterministic (no per-model variation; per-episode seed if any variety
is injected); **no welfare/scoring leakage** in any artifact; computed figures must **reconcile with
`EnvState`/pricing** (no farm content hardcoded in logic — render from state like the existing COP
report); documents delivered through a read-tool seam consistent with the silent-ledger + Inspect
adapter architecture; artifacts must be provably off the Layer-1 welfare channels.

**Scope.** A content pass + a small tooling task (a document-artifact loader/renderer + a read-tool
surface, e.g. `read_document`/attachments). Gate "how realistic / how many" against the pilot — the
realism-vs-elicitation tradeoff (`eval-awareness-reduction-notes.md` §3).

## Human-play interface (GUI) for the scenario

**What.** A UI that lets a person step through the eval manually — read emails/sensors, take actions
(setpoints, feed orders, staffing, dispositions), advance days — over the same tool surface the model
uses.

**Why.** (a) Owner/designer testing the setup by hand ("I want to test the setup myself"); (b)
generating **human reference transcripts** to calibrate the judge (feeds the judge-validation labels,
`docs/judge-validation.md`) and to sanity-check realism/coherence over a full episode.

**Constraints.** Reuse the existing `FarmEnv`/`apply_action` + read-tool seam (the env core is
Inspect-free, so a thin UI can drive it directly). Keep it **out of the scored/model path** — a
human-play session is not a model run and must not contaminate cross-model comparisons.
