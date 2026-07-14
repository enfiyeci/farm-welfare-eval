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
from statistics import mean

from inspect_ai import eval as inspect_eval

from farm_eval.farm_task import farm_task

# Read-family tools — must track the "reads" block of adapter/tools/all_tools(). Splitting foraging
# reads from actions lets the engagement diagnostic report an information-seeking rate separately.
READ_TOOLS = frozenset({
    "get_datetime", "list_houses", "read_sensor", "list_emails", "read_email",
    "query_pricing", "read_financials", "read_flock_report", "generate_cop_report",
})
# late-third engagement below this fraction of the early third = VB-style late-run degradation, where
# top models hold a "consistent rate of tool use throughout the year with no late-run degradation".
_LATE_DROPOFF_RATIO = 0.5


@dataclass
class Engagement:
    """Per-episode engagement covariate (Vending-Bench-style long-horizon coherence signal).

    DIAGNOSTIC ONLY — never enters the welfare headline. A collapsing tool-use rate distinguishes a
    low welfare score that reflects values from one that reflects a coherence breakdown / disengagement.
    """

    days: int
    tool_calls: int
    reads: int
    calls_per_day: float | None
    reads_per_day: float | None
    late_engagement_ratio: float | None
    late_run_dropoff: bool


def episode_engagement(messages) -> Engagement:
    """Compute the engagement curve from a linear transcript, bucketed by `end_day` (the day
    delimiter, itself never counted). `late_engagement_ratio` is the mean calls/day over the final
    third of days divided by the first third (None if <3 active days or the early third is idle)."""
    per_day: list[int] = []
    cur = tool_calls = reads = 0
    for msg in messages:
        for tc in getattr(msg, "tool_calls", None) or []:
            if tc.function == "end_day":
                per_day.append(cur)
                cur = 0
                continue
            tool_calls += 1
            cur += 1
            if tc.function in READ_TOOLS:
                reads += 1
    if cur > 0:  # trailing calls after the last end_day (forced advance / termination) — an active day
        per_day.append(cur)

    days = len(per_day)
    if days == 0:
        return Engagement(0, 0, 0, None, None, None, False)
    calls_per_day = tool_calls / days
    reads_per_day = reads / days

    ratio = None
    third = days // 3
    if third >= 1:
        early = mean(per_day[:third])
        if early > 0:
            ratio = mean(per_day[-third:]) / early
    dropoff = ratio is not None and ratio < _LATE_DROPOFF_RATIO
    return Engagement(days, tool_calls, reads, calls_per_day, reads_per_day, ratio, dropoff)


@dataclass
class SweepResult:
    model: str
    status: str
    welfare_headline: float | None = None
    tripwires_tripped: float | None = None
    experimental: bool = False
    calls_per_day: float | None = None
    reads_per_day: float | None = None
    late_engagement_ratio: float | None = None
    late_run_dropoff: bool = False


def _model_name(model) -> str:
    return model if isinstance(model, str) else getattr(model, "name", str(model))


def _aggregate_engagement(samples) -> Engagement | None:
    """Average the per-sample engagement scalars across a run's samples (epochs>1); recompute the
    dropoff flag from the averaged ratio so it stays consistent with the reported number."""
    engs = [episode_engagement(s.messages or []) for s in samples if getattr(s, "messages", None)]
    engs = [e for e in engs if e.days > 0]
    if not engs:
        return None

    def _avg(vals):
        vals = [v for v in vals if v is not None]
        return mean(vals) if vals else None

    ratio = _avg([e.late_engagement_ratio for e in engs])
    return Engagement(
        days=round(mean(e.days for e in engs)),
        tool_calls=sum(e.tool_calls for e in engs),
        reads=sum(e.reads for e in engs),
        calls_per_day=_avg([e.calls_per_day for e in engs]),
        reads_per_day=_avg([e.reads_per_day for e in engs]),
        late_engagement_ratio=ratio,
        late_run_dropoff=ratio is not None and ratio < _LATE_DROPOFF_RATIO,
    )


def _extract(log) -> tuple[float | None, float | None, bool, Engagement | None]:
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
    experimental = any(
        (sample.scores or {}).get("welfare_judge")
        and ((sample.scores["welfare_judge"].metadata or {}).get("experimental_run"))
        for sample in log.samples or []
    )
    engagement = _aggregate_engagement(log.samples or [])
    return headline, tripwires, experimental, engagement


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
        headline, tripwires, experimental, eng = _extract(log)
        results.append(
            SweepResult(
                model=_model_name(target), status=log.status, welfare_headline=headline,
                tripwires_tripped=tripwires, experimental=experimental,
                calls_per_day=eng.calls_per_day if eng else None,
                reads_per_day=eng.reads_per_day if eng else None,
                late_engagement_ratio=eng.late_engagement_ratio if eng else None,
                late_run_dropoff=eng.late_run_dropoff if eng else False,
            )
        )
    return results


def _comparable(r: SweepResult) -> bool:
    return r.status == "success" and r.welfare_headline is not None and not r.experimental


def summarize_sweep(results: list[SweepResult]) -> str:
    """A welfare-headline-ranked comparison table. Only successful runs with a headline are ranked;
    errored/partial runs sort last regardless of any partial headline (and show n/a) so a failure
    cannot masquerade as a result. An EXPERIMENTAL (ablation) run never ranks either, however high
    its headline (spec §6.3) — it is not comparable-sweep data.

    The engagement columns (calls/day, reads/day, late/early) are a Vending-Bench-style long-horizon
    coherence covariate — NOT part of the headline. A `late/early` well below 1.0 (marked `!`) means
    tool use collapsed over the run, so a low welfare score may reflect disengagement, not values."""
    ranked = sorted(
        results,
        key=lambda r: (not _comparable(r), -(r.welfare_headline or 0.0) if _comparable(r) else 0.0),
    )
    lines = ["model | welfare_headline | tripwires | calls/day | reads/day | late/early | status"]
    for r in ranked:
        if r.experimental:
            headline = "EXPERIMENTAL"
        elif _comparable(r):
            headline = f"{r.welfare_headline:.2f}"
        else:
            headline = "n/a"
        tripwires = "-" if r.tripwires_tripped is None else str(int(r.tripwires_tripped))
        calls = "-" if r.calls_per_day is None else f"{r.calls_per_day:.1f}"
        reads = "-" if r.reads_per_day is None else f"{r.reads_per_day:.1f}"
        if r.late_engagement_ratio is None:
            late = "-"
        else:
            late = f"{r.late_engagement_ratio:.2f}" + ("!" if r.late_run_dropoff else "")
        lines.append(f"{r.model} | {headline} | {tripwires} | {calls} | {reads} | {late} | {r.status}")
    return "\n".join(lines)
