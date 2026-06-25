"""Run a sweep of target models over the SAME fixed environment, varying only the target role.

Because the environment is static and pre-authored, every model faces an identical world, so the
welfare headlines are directly comparable. The grader (judge) role is held fixed across the sweep.

CLI sketch (real models):
    inspect eval farm_eval/farm_task.py --model-role grader=anthropic/claude-opus-4-8 \
        --model-role target=anthropic/<id>      # one run per target

or programmatically via run_sweep([...]). Validate the judge first (docs/judge-validation.md):
welfare deltas across models are not trustworthy until Spearman rho is reported.
"""

from __future__ import annotations

from dataclasses import dataclass

from inspect_ai import eval as inspect_eval

from farm_eval.farm_task import farm_task


@dataclass
class SweepResult:
    model: str
    status: str
    welfare_headline: float | None = None
    tripwires_tripped: float | None = None


def _model_name(model) -> str:
    return model if isinstance(model, str) else getattr(model, "name", str(model))


def _extract(log) -> tuple[float | None, float | None]:
    headlines, trips = [], []
    for sample in log.samples or []:
        score = (sample.scores or {}).get("welfare_judge")
        if score and isinstance(score.value, dict):
            if score.value.get("weighted_welfare") is not None:
                headlines.append(score.value["weighted_welfare"])
            if score.value.get("tripwires_tripped") is not None:
                trips.append(score.value["tripwires_tripped"])
    headline = sum(headlines) / len(headlines) if headlines else None
    tripwires = max(trips) if trips else None
    return headline, tripwires


def run_sweep(targets, *, config_path="config.yml", config=None, grader=None, **eval_kwargs) -> list[SweepResult]:
    """Run the farm task once per target model (the target drives the agent; grader role fixed)."""
    results: list[SweepResult] = []
    for target in targets:
        # The target drives the agent via the "target" role (accepts a model name OR a Model
        # object); model= just needs a string default and is never called once roles cover all
        # generation (solver -> target, scorer -> grader).
        roles = {"target": target}
        if grader is not None:
            roles["grader"] = grader
        default_model = target if isinstance(target, str) else "mockllm/model"
        log = inspect_eval(
            farm_task(config_path=config_path, config=config), model=default_model, model_roles=roles, **eval_kwargs
        )[0]
        headline, tripwires = _extract(log)
        results.append(
            SweepResult(model=_model_name(target), status=log.status, welfare_headline=headline, tripwires_tripped=tripwires)
        )
    return results


def summarize_sweep(results: list[SweepResult]) -> str:
    """A welfare-headline-ranked comparison table (best first; missing/errored runs last)."""
    ranked = sorted(results, key=lambda r: (r.welfare_headline is None, -(r.welfare_headline or 0.0)))
    lines = ["model | welfare_headline | tripwires | status"]
    for r in ranked:
        headline = "n/a" if r.welfare_headline is None else f"{r.welfare_headline:.2f}"
        tripwires = "-" if r.tripwires_tripped is None else str(int(r.tripwires_tripped))
        lines.append(f"{r.model} | {headline} | {tripwires} | {r.status}")
    return "\n".join(lines)
