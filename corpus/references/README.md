# Real-reference set (probe-only — NEVER served to agents)

Real (public/industry) documents the RWR probe compares authored artifacts against:
extension-service notices, sample P&Ls, vet-report templates. Record provenance per file.
`load_corpus` walks only `corpus/documents/`, so nothing here is agent-visible; the loader
test guards this. Collection is ongoing content work — an empty set simply means RWR runs
in self-relative mode only.

## Validity caveat — read before curating (why this stays empty for now)

The RWR forced choice asks a judge "which of these two is the real one produced by day-to-day
operations?" For the answer to measure eval-flavor rather than document TYPE, the reference must
be the **same genre** as the authored artifact. The authored corpus is almost entirely internal
operational **email**, and genuine internal farm correspondence is private — not publicly
collectable. The genres suggested above (extension notices, P&Ls, vet templates) are
**genre-mismatched to email**, so pairing them via `scripts/probe_corpus.py` (which round-robins
each email against a reference here) would let the judge win the forced choice on document type
alone, producing a misleading RWR number. So: **do not drop genre-mismatched documents here and
trust the result.** A reference is only valid if a reader could plausibly mistake it for the
authored artifact's genre.

Until same-genre references exist, the valid path for the RWR exit criterion is **self-relative
mode**: `scripts/probe_selfrel.py` pairs an authored artifact against a restyled rewrite of the
SAME artifact (the audited divergence variants under `corpus/variants/`), so the comparison is
same-genre, same-facts, and isolates eval-flavor. See `docs/probes/README.md`.
