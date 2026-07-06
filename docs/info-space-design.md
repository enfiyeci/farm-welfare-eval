# Information-space design — authoring the agent's information environment

**Date:** 2026-06-26
**Status:** Design note + proposed increment (not yet built)
**Origin:** Deep-research pass on "how to construct the information environment for a
domain-specific agentic eval" (PETRI, τ-bench, WebArena, the Anthropic realism/eval-awareness
write-ups, the DeepMind eval-awareness work). Findings adversarially verified (22/25 claims
confirmed, 3 killed — the killed ones are cited below because they sharpen the design).

This doc is about the **information space**: the corpus, world-state, sensor/tool surface, and
discovery paths the agent navigates — i.e. *what the model can find and how hard it is to find*.
The substrate-controllability notes (how the world reacts to actions) live in
`eval-design-notes.md`; this is the complementary "what's authored into the world" axis.

---

## Verified principles (the spine)

1. **Bury the latent issue in routine work.** Noticing a welfare tension should be a byproduct
   of doing the job, not a response to a flag. PETRI placed concerning information *deep* inside
   a large body of ordinary notes/emails/documents.
   ([Anthropic PETRI](https://alignment.anthropic.com/2025/petri/) — confidence: medium, verified 2-1.)

2. **Keep the opportunity low-salience ("Chekhov's gun").** An *inviting* opportunity to misbehave
   makes the model infer that its role is to misbehave. A beat that too loudly announces the
   dilemma measures "does the model take obvious bait," not latent propensity.
   ([Anthropic OpenAI-findings](https://alignment.anthropic.com/2025/openai-findings/) — high.)

3. **Ground in authentic artifacts, but the *premise* caps realism.** Real resources moved a
   realism win-rate from 4.6% → 32.8%, but an implausible premise can't be polished away — and
   *higher realism makes some models miss the issue entirely*. So realism and elicitation trade
   off: a low welfare score can mean "didn't care" **or** "didn't notice."
   ([Anthropic coding-audit-realism](https://alignment.anthropic.com/2026/coding-audit-realism/) — high.)

4. **Eval-awareness is an environment problem, not only a prompt problem.** Three claims that
   eval-awareness is *primarily* prompt-driven and that neutral/operational framing suppresses it
   were **refuted 0-3** in verification. The supported position: realistic scenarios *reliably leak
   cues* (round/near-future dates, AI-safety meta-vocabulary, "too-clean" state), and a neutral FMS
   briefing does **not** by itself buy low eval-awareness. Gate realism as **eval-awareness parity
   vs. baselines**, measured — not assumed.
   ([DeepMind 2605.29729](https://arxiv.org/html/2605.29729v1) — high.)

5. **Score on objective world-state, citation-first, across repeats.** τ-bench grades the final
   world-state against a goal state (not transcript vibes) and proposes **pass^k** to expose
   run-to-run inconsistency; PETRI's judge is two-stage citation-first.
   ([τ-bench](https://arxiv.org/pdf/2406.12045), [WebArena](https://webarena.dev/static/paper.pdf) — high.)
   *(We already do objective Layer-1 + verbatim-quote-validated judging; the missing piece is pass^k.)*

**One contested point.** The strong causal claim that eval-awareness *suppresses* misaligned
behavior (the GLM-5 "20% unaware → 5% aware" honeypot-gaming result) was **refuted 0-3** — treat the
*direction and magnitude* as unsettled. Implication: measure eval-awareness as a **covariate** for
cross-model comparison, don't assume it uniformly deflates welfare signal.
([LessWrong honeypot-gaming](https://www.lesswrong.com/posts/GrEvutegoJFeTkzwe/we-found-an-open-weight-model-that-games-alignment-honeypots-1).)

---

## Where the current build already satisfies these

- Per-decision **discovery paths** in `decision-register.md` / `welfare-decisions.html` (principle 1).
- **Settled-vs-contested evidence-confidence** so a justified minority view isn't auto-penalized (principle 2/3).
- **Objective Layer-1** welfare-state scorer + **verbatim-quote-validated** judge against `msg_N` ids (principle 5).
- **`eval_awareness` as a validity gate** excluded from the welfare headline (principle 4 — instrument exists).
- The flock/COP **computed-reads** principle (never canned) and `send_email`-as-filing-channel
  (no salient "compliance" tool) in `2026-06-26-flock-cop-reads-integrity-design.md` (principle 2/4).

## The four gaps (proposed increment)

These are **not yet built**. Each names the design decision to ratify and the concrete work.

### G1 — Distractor / signal-to-noise calibration
**Gap.** Signal-to-noise is not a first-class dial. The 26 authored email bodies are almost all
load-bearing, so the ~21–23 tensions stand out by *being the only interesting thing in the inbox* —
a salience leak (violates principle 2). WebArena deliberately enriches with irrelevant content.
**Work.** Author a tranche of routine-but-inert corpus traffic (mundane emails, normal sensor days,
benign maintenance/vendor/HR notes) so welfare beats are embedded, not isolated. Target a documented
ratio (e.g. roughly N inert : 1 load-bearing per in-world week) rather than ad-hoc.
**Open decision.** The ratio, and whether distractors are pure noise or *near-miss hard-negatives*
(things that look like a welfare issue but aren't — feeds the future false-alarm study, spec §20).

### G2 — Burial-depth as a measured variable
**Gap.** Burial depth almost certainly varies across the 21–23 decisions (some are one `read_email`
away; others need synthesizing a sensor trend against a compliance doc), but it isn't tagged or
reported. This conflates capability (noticing) with propensity (caring).
**Work.** Add a `discovery_depth` tag per decision (e.g. hops/synthesis-steps from "obvious," or an
ordinal surfaced/latent/deeply-latent), captured in `decisions-data.mjs` / the register; report the
welfare score **conditioned on** depth. Operationalizes the capability-vs-propensity split (spec §20)
through the information space.
**Open decision.** The depth scale/encoding and whether it's author-assigned or derived from the
discovery-path text.

### G3 — "Didn't notice" vs. "didn't care" disambiguation in the judge
**Gap.** Per principle 3, realism makes some models *miss* the tension; a low welfare score currently
can't distinguish a noticing failure from a propensity failure, which contaminates the headline and
cross-model deltas.
**Work.** Add a judge sub-signal per decision: did the transcript show the model **encounter** the
discovering evidence (read the relevant email/sensor) before the deadline beat? `low welfare +
encountered` = propensity miss; `low welfare + not encountered` = noticing/capability miss. The
deterministic ledger windows + `msg_N` ids already make "did it read X by beat Y" mechanically
checkable — this can be largely a **ledger-side** signal, not a grader judgment.
**Open decision.** Whether "encounter" is purely mechanical (tool-call to the relevant read within
the `[opens, deadline]` window) or grader-confirmed; how it surfaces in the report (covariate vs.
separate sub-score).

### G4 — Eval-awareness parity baseline
**Gap.** Per principle 4, we can't certify "low eval-awareness" in the absolute — only relative to
baselines. The `eval_awareness` gate measures a level, not a parity.
**Work.** During pilot-before-freeze, run the eval against a **more-realistic** and a
**more-synthetic** variant of the environment (or compare against a known-realistic reference task)
and report eval-awareness *parity*, not just the raw rate. Also: scrub avoidable cues now — audit the
2025-06-09→2026-11-02 date window (round/near-future dates read synthetic), any AI/eval/safety
vocabulary anywhere in corpus or tools, and "too-clean" state (real farm data has gaps, late reports,
contradictory readings).
**Open decision.** What the baseline variant is (a perturbed copy vs. an external reference), and how
much cue-scrubbing happens pre-freeze vs. as a logged caveat.

### Cross-cutting — pass^k on the welfare headline
The deterministic substrate makes the *world* reproducible, but the *model* is still stochastic.
Run each target **k times** over the fixed environment and report **pass^k** (or at least
welfare-headline variance), per principle 5. Cheap given the fixed env; catches "got it once by luck"
and is the right denominator for cross-model claims. Wire into `run_sweep.py` / `summarize_sweep`.

---

## Sequencing note

G1 (distractors) and G4's cue-scrub are **content-pass** work and should land **before** the
pilot/freeze (burying honeypots changes elicitation, so they must be in place when eval-awareness is
measured). G2 (depth tags) is cheap metadata, do alongside the register churn. G3 and pass^k are
**scoring/reporting** changes that can land in parallel with the pilot. None of the four blocks the
flock/COP-reads + integrity increment already in flight.
