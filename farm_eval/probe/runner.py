"""P2 — the probe loop. The ONLY nondeterministic piece of the probe (LLM calls; QA-side,
spec §6.5). Everything it feeds and returns goes through the pure prompt/report layers.

The A/B slot for RWR alternates by sample-index parity — deterministic pairing structure,
no RNG (repo rule: no random in farm_eval/).

`parse_motivation_response` never raises (a fully-discarded result on an unparseable
envelope), so it is called bare. `parse_rwr_response` DOES raise ValueError on an
unparseable/invalid choice; an invalid sample is recorded as "invalid" and excluded from
both `authored_wins` and the win-rate denominator (see report.py)."""

from __future__ import annotations

from farm_eval.probe.artifacts import Artifact
from farm_eval.probe.prompts import (
    build_motivation_prompt,
    build_rwr_prompt,
    parse_motivation_response,
    parse_rwr_response,
)
from farm_eval.probe.taxonomy import TellClass

PROBE_MODEL_DEFAULT = "anthropic/claude-fable-5"


async def probe_artifacts(
    artifacts: list[Artifact], taxonomy: list[TellClass], *, model, samples: int = 5
) -> list[dict]:
    results = []
    for artifact in artifacts:
        prompt = build_motivation_prompt(artifact, taxonomy)
        parsed = []
        for _ in range(samples):
            completion = (await model.generate(prompt)).completion
            parsed.append(parse_motivation_response(completion, artifact, taxonomy))
        counts: dict[str, int] = {}
        for p in parsed:
            for flag in p["flags"]:
                counts[flag["class"]] = counts.get(flag["class"], 0) + 1
        results.append(
            {"artifact_id": artifact.id, "kind": artifact.kind, "samples": parsed, "flag_counts": counts}
        )
    return results


async def rwr_pairs(pairs, *, model, samples: int = 9) -> list[dict]:
    results = []
    for authored, reference, mode in pairs:
        choices = []
        wins = 0
        for i in range(samples):
            a, b = (authored, reference) if i % 2 == 0 else (reference, authored)
            completion = (await model.generate(build_rwr_prompt(a, b))).completion
            try:
                choice = parse_rwr_response(completion)
            except ValueError:
                choices.append("invalid")
                continue
            choices.append(choice)
            authored_slot = "A" if i % 2 == 0 else "B"
            if choice == authored_slot:
                wins += 1
        results.append(
            {"artifact_id": authored.id, "reference_id": reference.id, "mode": mode,
             "authored_wins": wins, "samples": choices}
        )
    return results
