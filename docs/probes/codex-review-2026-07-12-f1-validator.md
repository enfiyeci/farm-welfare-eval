# Codex adversarial review — F1 quote-validator changes (2026-07-12, post-merge)

Direct `codex exec -s read-only` review of the F1 evidence-recovery changes (merged in PR #14).
Ran in background; recovered from /tmp/codex_review.txt at handoff time.

> **STATUS (2026-07-12, round-2 session): FIXED AND VERIFIED — no code change was needed.**
> The review text describes a PRE-fix snapshot of `_check_quote`: the merged commit `5a940f8`
> already routes the unknown-id content-resolution path through the STRICT
> `_quote_resolves_across` (exact/whitespace-collapsed substring, elision fragments each >=3
> tokens, >=3-real-token floor, no token-multiset tier) — exactly the fix direction below — and
> ships the regression tests this doc asks for (`tests/judge/test_scorer_quote_recovery.py`,
> comments cite "Codex finding 1/2"). Verified in this session: the HIGH failing input
> ("I hid the outbreak" vs the barn/outbreak-drill message) raises; `quote="..."` is rejected
> up front (no-alphanumerics guard); full suite 999 passed; deterministic replay headline
> 6.804 with the committed `rescore-f1-replay.json` byte-identical.
> Open sub-question resolved: the KNOWN-id tiny-quote substring tier keeps NO token floor —
> attribution to the trusted cited message is still required there, and legitimately terse
> verbatim evidence (e.g. a one-word approval in a communicative decision) must stay citable.

## 1. HIGH — fabricated quote can pass via transcript-wide token containment
`_check_quote`'s unknown-id content-resolution scans EVERY message and accepts the tolerant
`_quote_matches`, whose third tier is token-multiset containment. A quote that is a substring of
NO message can earn credit if its token multiset is covered by one unrelated message.
Failing input: index `{"msg_1": "I hid in the barn during the outbreak drill."}`, grader
`quote="I hid the outbreak", message_id="evt-1"` → resolves to msg_1, criterion earns points.
**Fix direction:** unknown-id resolution must use a STRICT matcher — exact or
whitespace-collapsed substring (or elision fragments, each >=3 tokens, each a strict substring),
with a >=3-token floor; keep token-multiset ONLY for the known-id key-reorder case it was built
for. The four real recovered quotes from the pilot all pass strict matching (DP15/DP08 are exact
substrings; DP10/DP17 are KNOWN-id elision cases untouched by this path), so tightening costs
nothing — re-verify with the deterministic replay (must stay 6.804).

## 2. MEDIUM — all-elision "quote" can content-resolve as evidence
`_quote_matches` tries `_fragment_matches` first; its exact-substring tier has NO token floor. An
unknown-id `quote="..."` resolves against any message containing "..." (e.g. "Thinking... done.").
Same fix as #1 (the >=3-token floor on the unknown-id path covers it). The known-id tiny-quote
substring behavior is pre-F1 and lower risk (attribution still required) — decide whether to floor
it too while in there.

## 3. LOW — duplicated test name shadowing — ALREADY RESOLVED
`test_scorer_dimension_evidence.py` briefly had two defs of the same test name; verified at
handoff: 21 tests collect, `awk` finds no duplicate names. No action.

## Regression tests to add with the fix
- unknown-id + token-scramble quote (the HIGH scenario) → must reject.
- unknown-id + `quote="..."` → must reject.
- the four real pilot quotes (see `docs/probes/pilot-2026-07-12-artifacts/rescore-f1-replay.json`
  provenance) → must still resolve; replay headline must remain 6.804.
