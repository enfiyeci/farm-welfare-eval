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
            if score.value.get("welfare_headline") is not None:
                headlines.append(score.value["welfare_headline"])
            if score.value.get("tripwires_observed") is not None:
                trips.append(score.value["tripwires_observed"])
    headline = sum(headlines) / len(headlines) if headlines else None
    tripwires = max(trips) if trips else None
    return headline, tripwires


def run_sweep(targets, *, grader=None, config_path="config.yml", config=None, **eval_kwargs) -> list[SweepResult]:
    """Run the farm task once per target model (the target drives the agent; grader role fixed).

    `grader` is REQUIRED: only the target may vary across the sweep, or the welfare headlines are not
    comparable. Without an explicit fixed grader the scorer's grader role would fall back to the
    active model (the target), silently varying the judge.
    """
    if grader is None:
        raise ValueError("run_sweep requires an explicit fixed `grader` (only the target may vary)")
    results: list[SweepResult] = []
    for target in targets:
        # The target drives the agent via the "target" role (accepts a model name OR a Model
        # object); model= just needs a string default and is never called once roles cover all
        # generation (solver -> target, scorer -> grader).
        roles = {"target": target, "grader": grader}
        default_model = target if isinstance(target, str) else "mockllm/model"
        log = inspect_eval(
            farm_task(config_path=config_path, config=config), model=default_model, model_roles=roles, **eval_kwargs
        )[0]
        headline, tripwires = _extract(log)
        results.append(
            SweepResult(model=_model_name(target), status=log.status, welfare_headline=headline, tripwires_tripped=tripwires)
        )
    return results


def _comparable(r: SweepResult) -> bool:
    return r.status == "success" and r.welfare_headline is not None


def summarize_sweep(results: list[SweepResult]) -> str:
    """A welfare-headline-ranked comparison table. Only successful runs with a headline are ranked;
    errored/partial runs sort last regardless of any partial headline (and show n/a) so a failure
    cannot masquerade as a result."""
    ranked = sorted(results, key=lambda r: (not _comparable(r), -(r.welfare_headline or 0.0)))
    lines = ["model | welfare_headline | tripwires | status"]
    for r in ranked:
        headline = f"{r.welfare_headline:.2f}" if _comparable(r) else "n/a"
        tripwires = "-" if r.tripwires_tripped is None else str(int(r.tripwires_tripped))
        lines.append(f"{r.model} | {headline} | {tripwires} | {r.status}")
    return "\n".join(lines)
