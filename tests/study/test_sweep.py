from farm_eval.study.params import Rung
from farm_eval.study.response import Decision
from farm_eval.study.sweep import Outcome, SweepRules, run_sweep

RUNGS = tuple(Rung(density_step=0.04 * i, added_mortality_pp=float(i))
              for i in range(1, 9))


def _threshold_policy(max_accepted_pp: float):
    """Accepts any rung at or below max_accepted_pp. Monotone by construction."""
    def evaluate(rung: Rung, replicate: int) -> Decision:
        return (Decision.ACCEPT if rung.added_mortality_pp <= max_accepted_pp
                else Decision.DECLINE)
    return evaluate


def test_brackets_a_monotone_threshold():
    result = run_sweep(RUNGS, _threshold_policy(4.0), SweepRules())
    assert result.outcome is Outcome.BRACKETED
    lo, hi = result.interval
    assert lo == 4.0 and hi == 5.0


def test_every_rung_is_evaluated():
    """The sweep is exhaustive by design (spec §11.4) — partial coverage is what made
    the earlier adaptive version unable to see non-monotone responses."""
    seen = []

    def evaluate(rung: Rung, replicate: int) -> Decision:
        seen.append((rung.added_mortality_pp, replicate))
        return Decision.ACCEPT

    result = run_sweep(RUNGS, evaluate, SweepRules())
    assert len(result.rung_results) == len(RUNGS)
    assert len(seen) == len(RUNGS) * SweepRules().replicates


def test_accept_everything_is_censored_high_not_a_number():
    """Spec §16.11 — a bound is never reported as the estimate."""
    result = run_sweep(RUNGS, _threshold_policy(99.0), SweepRules())
    assert result.outcome is Outcome.CENSORED_HIGH
    assert result.interval is None


def test_decline_everything_is_censored_low():
    result = run_sweep(RUNGS, _threshold_policy(0.0), SweepRules())
    assert result.outcome is Outcome.CENSORED_LOW
    assert result.interval is None


def test_a_rung_is_accepted_only_if_both_replicates_accept():
    def evaluate(rung: Rung, replicate: int) -> Decision:
        return Decision.ACCEPT if replicate == 0 else Decision.DECLINE

    result = run_sweep(RUNGS, evaluate, SweepRules())
    assert result.outcome is Outcome.CENSORED_LOW
    assert all(not r.accepted for r in result.rung_results)


def test_non_monotonic_response_is_reported_not_forced_into_an_interval():
    """Spec §4 — forcing an interval onto a non-monotone path manufactures a number.
    Reachable only because the sweep sees every rung."""
    def evaluate(rung: Rung, replicate: int) -> Decision:
        pp = rung.added_mortality_pp
        return Decision.ACCEPT if (pp <= 2.0 or pp >= 6.0) else Decision.DECLINE

    result = run_sweep(RUNGS, evaluate, SweepRules())
    assert result.outcome is Outcome.NON_MONOTONIC
    assert result.interval is None


def test_unparseable_counts_as_not_accepted_and_is_preserved():
    def evaluate(rung: Rung, replicate: int) -> Decision:
        return Decision.UNPARSEABLE

    result = run_sweep(RUNGS, evaluate, SweepRules())
    assert result.outcome is Outcome.CENSORED_LOW
    assert all(Decision.UNPARSEABLE in r.decisions for r in result.rung_results)


def test_single_rung_accepted_is_censored_high():
    result = run_sweep(RUNGS[:1], _threshold_policy(99.0), SweepRules())
    assert result.outcome is Outcome.CENSORED_HIGH


def test_empty_rung_list_is_rejected():
    import pytest
    with pytest.raises(ValueError, match="at least one rung"):
        run_sweep((), _threshold_policy(1.0), SweepRules())


def test_zero_replicates_is_rejected_rather_than_passing_vacuously():
    """all(()) is True, so replicates=0 would mark every rung accepted after zero
    model calls and report a confident CENSORED_HIGH built on no data."""
    import pytest
    with pytest.raises(ValueError, match="at least one replicate"):
        run_sweep(RUNGS, _threshold_policy(1.0), SweepRules(replicates=0))


def test_replicate_count_is_honoured():
    calls = []

    def evaluate(rung: Rung, replicate: int) -> Decision:
        calls.append(replicate)
        return Decision.ACCEPT

    run_sweep(RUNGS, evaluate, SweepRules(replicates=3))
    assert len(calls) == len(RUNGS) * 3
    assert set(calls) == {0, 1, 2}
