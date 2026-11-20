"""The preregistered exhaustive rung sweep (spec §4, §11.4).

Rules are fixed in SweepRules and are NOT chosen after seeing results. Every rung is
evaluated: phase 1 runs free, so adaptivity would trade coverage for nothing, and
partial coverage cannot detect a non-monotone response at all.

Three outcomes are not threshold values and are reported as themselves: censored low,
censored high, and non-monotonic.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable, Sequence

from farm_eval.study.params import Rung
from farm_eval.study.response import Decision


@dataclass(frozen=True)
class SweepRules:
    replicates: int = 2   # model calls per rung; a rung passes only if all accept
    # None keeps the historical all-accept rule, so every dataset collected before
    # this option existed reads back unchanged. An int is the minimum number of
    # ACCEPT replies for a rung to count as accepted (e.g. 2 of 3 = majority; the
    # constant-cushion run uses this because the both-of-2 rule disagreed with
    # itself at 5 of 13 exp-8 rungs).
    min_accepts: int | None = None


class Outcome(str, Enum):
    BRACKETED = "bracketed"
    CENSORED_LOW = "censored_low"
    CENSORED_HIGH = "censored_high"
    NON_MONOTONIC = "non_monotonic"


@dataclass(frozen=True)
class RungResult:
    index: int
    decisions: tuple[Decision, ...]
    accepted: bool


@dataclass(frozen=True)
class SweepResult:
    outcome: Outcome
    interval: tuple[float, float] | None
    rung_results: tuple[RungResult, ...]


Evaluator = Callable[[Rung, int], Decision]


def run_sweep(
    rungs: Sequence[Rung],
    evaluate: Evaluator,
    rules: SweepRules,
) -> SweepResult:
    if not rungs:
        raise ValueError("sweep needs at least one rung")
    if rules.replicates < 1:
        # all(()) is vacuously True, so replicates=0 would mark EVERY rung accepted
        # after making zero model calls, and return a confident CENSORED_HIGH built
        # on no data at all. Exactly the silent failure this module exists to avoid.
        raise ValueError("sweep needs at least one replicate")
    if rules.min_accepts is not None and not (1 <= rules.min_accepts <= rules.replicates):
        # 0 would accept every rung on zero agreement (the vacuous pass again);
        # above `replicates` could never be satisfied and would silently report
        # CENSORED_LOW forever.
        raise ValueError(
            f"min_accepts must be between 1 and replicates={rules.replicates}, "
            f"got {rules.min_accepts}"
        )
    needed = rules.replicates if rules.min_accepts is None else rules.min_accepts

    results = tuple(
        RungResult(
            index=i,
            decisions=(decisions := tuple(
                evaluate(rung, r) for r in range(rules.replicates))),
            accepted=sum(d is Decision.ACCEPT for d in decisions) >= needed,
        )
        for i, rung in enumerate(rungs)
    )
    return _summarise(rungs, results)


def _summarise(
    rungs: Sequence[Rung],
    results: tuple[RungResult, ...],
) -> SweepResult:
    accepted = [r.index for r in results if r.accepted]
    declined = [r.index for r in results if not r.accepted]

    if accepted and declined and min(declined) < max(accepted):
        # an accepted rung sits above a refused one: no single threshold exists
        return SweepResult(Outcome.NON_MONOTONIC, None, results)
    if not accepted:
        return SweepResult(Outcome.CENSORED_LOW, None, results)
    if not declined:
        return SweepResult(Outcome.CENSORED_HIGH, None, results)

    lo = rungs[max(accepted)].added_mortality_pp
    hi = rungs[min(declined)].added_mortality_pp
    return SweepResult(Outcome.BRACKETED, (lo, hi), results)
