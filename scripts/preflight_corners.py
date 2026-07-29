"""Keyless pre-flight over the four 2x2 corner-baseline configs — run this BEFORE a paid corner run.

Executes the real checked-in `config-baseline-*.yml` (real corpus/, schedule/, judge dimensions, the
full configured horizon) with a scripted `mockllm` target and a scripted `mockllm` grader, so it
costs nothing. It proves the chain a paid run depends on:

    config loads -> corner briefing loads -> episode runs to the horizon -> judge parses ->
    welfare headline computed -> `experimental: true` reaches the score metadata

Catching a broken corner config here costs seconds; catching it during `run_baseline_corners.sh`
costs four sequential full episodes of real quota.

WHAT THIS DOES NOT DO
---------------------
**It does not produce welfare or finance baselines, and its numbers are not data.** The agent is a
fixed script and the grader's scores are synthesized here, so every corner is expected to land on
the SAME welfare headline. That identity is the invariant this script checks: the corners differ
only by briefing, and the briefing must not reach the score by any path other than the target
model's behaviour. If two corners disagree here, config is leaking into scoring — that is a real
defect, and this script fails loudly on it. Real baselines require a live target model that actually
reads the goal-prefixed briefing (`scripts/run_baseline_corners.sh`).

Usage:
    ./venv/bin/python scripts/preflight_corners.py [results.json]

Exit status is 0 only when every corner ran, every corner was stamped experimental, and all four
headlines agree.
"""
import json
import os
import pathlib
import sys
import time

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

from inspect_ai import eval as inspect_eval  # noqa: E402
from inspect_ai.model import ModelOutput, get_model  # noqa: E402

from farm_eval.farm_task import farm_task  # noqa: E402
from farm_eval.judge.dimensions import load_dimensions  # noqa: E402
from farm_eval.run_sweep import _extract  # noqa: E402
from scripts.gen_corner_briefings import CORNERS, DIRECTIVE_HEADER  # noqa: E402

# The generated corner briefing embeds DIRECTIVE_HEADER verbatim at the top, and that briefing is
# the episode's first message — so this is a quote the judge's validator can actually resolve.
# Derived rather than hardcoded: if the header is reworded, this follows it.
EVIDENCE_QUOTE = DIRECTIVE_HEADER.splitlines()[0].lstrip("#").strip()
EVIDENCE_MESSAGE_ID = "msg_0"

# Generous pools: mockllm RAISES when custom_outputs is exhausted rather than degrading, and the
# judge re-samples on a validation failure, so a tight pool would surface as a confusing harness
# error instead of the real problem.
TARGET_TURNS = 3000
# Deliberately far above what today's rubric consumes (~3 diagnostic passes + LLM criteria x
# judge_samples). Sized tight, rubric growth would spill past the score outputs and start feeding
# justification strings to a criterion grader, which swallows the parse failure as a zero and
# still exits green. Slack here is the cheaper side of that error.
GRADER_SCORE_OUTPUTS = 2000
GRADER_JUSTIFY_OUTPUTS = 200


def _grader_payload(dimensions) -> str:
    """Synthesize one grader response covering every configured dimension.

    Built from the real dimension set so a new or renamed dimension cannot silently go ungraded and
    turn a harness gap into a fake pass.
    """
    entries = []
    for dim in dimensions:
        if dim.weight > 0:
            low, high = dim.scale
            score = (low + high) // 2
            entries.append(
                f'"{dim.id}": {{"score": {score}, "quote": {json.dumps(EVIDENCE_QUOTE)}, '
                f'"message_id": "{EVIDENCE_MESSAGE_ID}"}}'
            )
        else:
            # Weight-0 gates (validity axes, tripwires) must NOT fire in a plumbing check.
            entries.append(f'"{dim.id}": {{"score": 0, "quote": "", "message_id": ""}}')
    return "{" + ", ".join(entries) + "}"


def _episode_day(sample) -> int | None:
    """Terminal in-world day index, read back out of the serialized env state."""
    for value in (sample.store or {}).values():
        if isinstance(value, dict) and "day_index" in value:
            return value["day_index"]
    return None


def run_corner(slug: str) -> dict:
    cfg = yaml.safe_load((ROOT / f"config-baseline-{slug}.yml").read_text(encoding="utf-8"))
    dimensions = load_dimensions(cfg["dimensions_dir"])

    # Fail loud BEFORE running: the synthetic grader quote is drawn from DIRECTIVE_HEADER, and a
    # quote that stops resolving is sanitized to a zero rather than raising — so a drifted briefing
    # would degrade into a silent green instead of an error.
    briefing = (ROOT / cfg["briefing_path"]).read_text(encoding="utf-8")
    if EVIDENCE_QUOTE not in briefing:
        raise ValueError(
            f"{slug}: briefing {cfg['briefing_path']} no longer contains {EVIDENCE_QUOTE!r}; "
            f"the pre-flight's evidence quote would fail validation silently."
        )

    target = get_model("mockllm/model", custom_outputs=[
        ModelOutput.for_tool_call(model="mockllm/model", tool_name="end_day", tool_arguments={})
        for _ in range(TARGET_TURNS)
    ])
    payload = ModelOutput.from_content(model="mockllm/model", content=_grader_payload(dimensions))
    grader = get_model("mockllm/model", custom_outputs=[
        *[payload for _ in range(GRADER_SCORE_OUTPUTS)],
        *[ModelOutput.from_content(model="mockllm/model", content="Scripted pre-flight justification.")
          for _ in range(GRADER_JUSTIFY_OUTPUTS)],
    ])

    started = time.time()
    log = inspect_eval(
        farm_task(config=cfg),
        model="mockllm/model",
        model_roles={"target": target, "grader": grader},
        display="none",
    )[0]
    elapsed = round(time.time() - started, 1)

    if log.status != "success":
        error = getattr(log, "error", None)
        return {
            "corner": slug, "status": log.status, "elapsed_s": elapsed,
            "error": str(error)[:800] if error else "unknown",
        }

    headline, tripwires, experimental = _extract(log)
    sample = log.samples[0]
    return {
        "corner": slug,
        "status": "success",
        "elapsed_s": elapsed,
        "welfare_headline": headline,
        "tripwires": tripwires,
        "experimental_run": experimental,
        "briefing_path": cfg["briefing_path"],
        "configured_end_day": cfg["episode_end_day"],
        "reached_day": _episode_day(sample),
    }


def main(argv: list[str]) -> int:
    results = []
    for slug in CORNERS:
        print(f"=== pre-flight corner: {slug} ===", flush=True)
        try:
            result = run_corner(slug)
        except Exception as exc:  # noqa: BLE001 - a pre-flight reports failures, never masks them
            result = {"corner": slug, "status": "exception",
                      "error": f"{type(exc).__name__}: {exc}"[:800]}
        print(json.dumps(result, indent=2), flush=True)
        results.append(result)

    if len(argv) > 1:
        pathlib.Path(argv[1]).write_text(json.dumps(results, indent=2), encoding="utf-8")

    print("\n=== PRE-FLIGHT SUMMARY ===", flush=True)
    for r in results:
        print(
            f"  {r['corner']:<26} status={r['status']:<10} "
            f"headline={r.get('welfare_headline')} experimental={r.get('experimental_run')} "
            f"day={r.get('reached_day')}/{r.get('configured_end_day')} {r.get('elapsed_s', '')}s",
            flush=True,
        )

    problems = []
    for r in results:
        if r["status"] != "success":
            problems.append(f"{r['corner']}: {r['status']} — {r.get('error', '')[:200]}")
            continue
        # A corner that scored without producing a usable headline is the exact plumbing failure
        # this script exists to catch; without this, four missing headlines collapse to {None} and
        # satisfy the agreement check below.
        headline = r.get("welfare_headline")
        if not isinstance(headline, (int, float)) or isinstance(headline, bool) \
                or headline != headline or headline in (float("inf"), float("-inf")):
            problems.append(
                f"{r['corner']}: no usable welfare headline (got {headline!r}) — scoring ran but "
                f"produced nothing to compare"
            )
        # Agreement across corners is only meaningful if each corner actually loaded ITS OWN
        # briefing. If every config pointed at the same (or the neutral) briefing, the headlines
        # would agree for the wrong reason and this pre-flight would bless a broken corner set.
        expected = f"prompts/baselines/{r['corner']}.md"
        if r.get("briefing_path") != expected:
            problems.append(
                f"{r['corner']}: loaded briefing {r.get('briefing_path')!r}, expected {expected!r}"
            )
        if not r["experimental_run"]:
            problems.append(
                f"{r['corner']}: experimental stamp missing — a corner run could rank as "
                f"comparable sweep data"
            )
        if r["reached_day"] != r["configured_end_day"]:
            problems.append(
                f"{r['corner']}: episode stopped at day {r['reached_day']}, "
                f"configured horizon is {r['configured_end_day']}"
            )

    headlines = {r["welfare_headline"] for r in results if r["status"] == "success"}
    if len(headlines) > 1:
        problems.append(
            f"corner headlines diverged under a fixed scripted agent and grader: {sorted(headlines)}. "
            f"The briefing is reaching the score by a path other than target behaviour."
        )

    if problems:
        print("\nFAILED:", flush=True)
        for p in problems:
            print(f"  - {p}", flush=True)
        return 1

    print(
        f"\nOK — {len(results)} corners ran to the configured horizon, all stamped experimental, "
        f"headlines agree ({headlines.pop() if headlines else 'n/a'}). "
        f"Plumbing only: these numbers are NOT baselines.",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
