# Cleanup backlog — deferred nits (non-blocking)

Low-priority items consciously deferred during the Phase E + C6 + D branch
(`feat/phase-c6-env-levers`) and its final whole-branch review. None block merge, none can
produce a wrong welfare score or a silent failure in the eval as it actually runs. Recorded here
(committed, durable) so the next cleanup pass can pick them up. Grouped by kind.

## Accepted-as-is from the final whole-branch review (opus triage: all merge-acceptable)

- **E5 — inexact internal fallback label.** `farm_eval/env/episode.py`: a non-numeric feed quantity
  (`quantity_tons="abc"`) is logged to the event log under `fallback:feed_order_over_capacity`, but
  nothing is over-capacity — it's just non-numeric. Agent-facing `detail` is accurate; only the
  internal label is loose. Fix (optional): add a dedicated `fallback:feed_order_invalid` label.
  Harness-side only; raw params + detail disambiguate it today.

- **D1 — `replay_env` seed footgun.** `farm_eval/env/replay.py`: `replay_env(..., seed=...)` takes the
  seed as a parameter a caller could get wrong. A wrong seed differs ONLY in the cosmetic `EnvState.seed`
  field (never read by deterministic logic), so it surfaces immediately as a `model_dump` mismatch, not
  a silent divergence. Polish: derive the seed from the original `EnvState.seed` (which callers already
  have recorded) so it can't be passed wrong.

- **D2 — checkpoint dir-name sanitizer is non-injective.** `farm_eval/adapter/checkpoint.py`
  `_sample_dir_name`: degenerate sample_ids map to sentinel names (`""→"_"`, `"."→"__"`, `".."→"___"`)
  to prevent path traversal (the actual security hole — fully fixed). Those sentinels COULD collide with
  a real sample_id that itself sanitizes to `"_"`, so two such samples sharing a `checkpoint_dir` could
  overwrite each other's checkpoints. Unreachable in this eval (sample_ids are distinct model/dataset
  keys, never `""`/`"."`/`".."`). Fix if non-standard sample_ids ever occur: hash the sample_id instead
  of char-mapping.

- **Pasteurization egg-channel value tier is a placeholder.** `farm_eval/env/model/params.py`
  `egg_channel_value_frac`: the `pasteurization` channel shares the `breaker` value fraction (0.35).
  Documented placeholder — both channels destroy shell value, so this is reasonable, but a precise
  fraction needs pricing research. Affects the profit dimension, never the welfare spine.

- **Historical plan doc shows the pre-C1 labor formula.** `evals/hen/archive/plans/2026-06-27-phase-c1-financial-pnl.md`
  still shows the old per-dozen `labor_usd_doz=0.074` formula that C1 replaced with the staffing-driven
  per-bird-day model. LEFT DELIBERATELY — it's a dated design record, not living docs (the living
  reference `docs/model-params.md` is current). Noted here only so no one mistakes it for current design.

## De-tell nits (from the eval-awareness-reduction reconciliation, `docs/research/eval-awareness-reduction-notes.md`)

For the future eval-awareness-reduction authoring pass, NOT this branch:

- **`fallback:unknown_tool` returns a canned string.** `farm_eval/env/episode.py`: an unknown tool
  yields `f"unknown action tool: {tool!r}"` — exactly the "canned/mismatched output" the research flags
  (§1, §2-B1). Defensive-only: NOT agent-reachable, because Inspect only dispatches schema-registered
  tools, so `apply_action` never sees an unknown tool from the target. Rewrite in FMS voice only if the
  tool surface is ever broadened to make this path reachable.

- **E5 feed-cap message is mildly over-helpful.** `farm_eval/env/episode.py`: the oversized-feed-order
  rejection ends "Confirm the quantity — did you mean tons?" A real supplier system wouldn't infer the
  operator's unit error that helpfully (§2-A1 "editorializing/admission" tell). Trim to a flat
  operational rejection ("order not placed; exceeds max X t per order").

## Broader next-phase work (tracked elsewhere, listed for completeness)

The eval-awareness-reduction project (`docs/research/eval-awareness-reduction-notes.md`, pilot-gated)
owns the larger items this branch did not touch: the behavioral-divergence keystone, an irregular
welfare-decision-spacing audit of `schedule/events.yml`, deployment-framing artifacts (login banner /
FMS version / mid-tenure burn-in), and the corpus de-tell probe + per-source register heterogeneity.
