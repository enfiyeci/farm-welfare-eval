# Eval-awareness probes (Phase 1 — spec docs/specs/2026-07-05-eval-awareness-reduction-design.md)

QA-side measurement instruments. Nothing here is agent-visible; probe output steers
authoring and never enters scoring.

## The instruments

| What | Where | Run |
|---|---|---|
| Tells taxonomy (P1) | `farm_eval/probe/data/tells.yml` | (data) |
| Artifact probe + RWR (P2) | `farm_eval/probe/` | `scripts/probe_corpus.py --out probe-report.md` |
| Probe validity gate (P3) | `farm_eval/probe/kappa.py` | `scripts/probe_kappa.py sheets --ids ... --out labels/` + `scripts/probe_kappa.py report --labels labels/` |
| Cue-localization (P4/D1) | judge metadata `cue_localization` | automatic on every scored run |
| Ablation seam (P5/D3) | `ablation_overrides` config key | see `config.yml` comment |
| Divergence kit (P6) | `docs/divergence-protocol.md` | `scripts/diff_pair.py --baseline ... --variant ... --node ... --out findings.md` |
| Spacing audit (P8) | `docs/probes/schedule-spacing-report.md` | `scripts/audit_schedule.py [--out docs/probes/schedule-spacing-report.md]` |

Probe judge default: `anthropic/claude-fable-5` (`--model` to override). Framing rules are
LOCKED (spec §1): never a binary "is this a test" ask; motivation-guessing and forced-choice
RWR only. Verbal awareness is a LOWER BOUND — see docs/judge-validation.md.

## κ gate (run BEFORE trusting probe output)

1. Pick ~15 artifacts spanning kinds: `scripts/probe_kappa.py sheets --ids <artifact_ids> --out kappa-labels/`
2. Hand-label every class cell true/false (blind — sheets contain no probe output).
3. `scripts/probe_kappa.py report --labels kappa-labels/ [--format-control]`
4. Gate: κ ≥ 0.6 AND an acceptably low format-control flip-rate; otherwise tighten
   `tells.yml` descriptions / the prompt and re-validate. Probe findings before a κ PASS are
   not actionable.

## Red-team gate (P9 — run before any content freeze)

1. κ gate passed; `scripts/probe_corpus.py` clean (no majority-fired high-severity tells) on
   the full corpus + briefing.
2. Blow-cover pass: instruct a strong model (default Fable; optionally a second family —
   Gemini Pro was the most tell-sensitive model in the pilot) with the motivation-guessing
   framing over (a) every corpus artifact, (b) ONE full stored transcript. Collect every cue
   it surfaces; map each to a taxonomy class.
3. Disposition table (committed): fix / accept-with-rationale per finding. No unresolved
   high-severity finding at freeze.
4. Re-run `scripts/probe_corpus.py` after fixes; attach the report to the freeze record.

## Phase-1 exit criteria (spec §3)

- [ ] κ ≥ 0.6 + format-control (P3)
- [ ] RWR number for every artifact class, mode-labeled (P2)
- [ ] cue_localization visible in a scored run's metadata (P4)
- [ ] one end-to-end ablation demonstrated (P5)
- [ ] 2 pivotal pairs authored + protocol committed; executed when episode infra permits (P6)
- [ ] P7 content landed probe-clean; P8 report committed
