from farm_eval.study.cells import Economics, Species, StandardBand, framing_cells
from farm_eval.study.documents import parse_survival_projections
from farm_eval.study.params import GAIN_LADDER
from farm_eval.study.phase1 import run_phase1
from farm_eval.study.provider import FakeProvider
from farm_eval.study.results import read_jsonl, write_jsonl
from farm_eval.study.sweep import Outcome, SweepRules


def _accept_below(pp_limit: float):
    """Replies ACCEPT when the prompt's projected survival drop is small enough."""
    def responder(prompt: str) -> str:
        before, after = parse_survival_projections(prompt)
        return ("DECISION: ACCEPT" if (before - after) <= pp_limit
                else "DECISION: DECLINE")
    return responder


def test_runs_every_cell_and_gain_combination():
    cells = framing_cells()[:2]
    gains = GAIN_LADDER[:2]
    provider = FakeProvider(_accept_below(1.2))
    results = run_phase1(provider, cells=cells, gains=gains,
                         rules=SweepRules())
    assert len(results) == len(cells) * len(gains)
    assert {(r.cell, r.gain) for r in results} == {
        (c, g) for c in cells for g in gains}


def test_marks_abstract_probes_above_the_envelope():
    """Spec §3.1 — cells beyond the envelope are labelled, not silently pooled."""
    cells = framing_cells()[:1]
    provider = FakeProvider(_accept_below(99.0))
    results = run_phase1(provider, cells=cells, gains=(0.08, 10.00),
                         rules=SweepRules())
    by_gain = {r.gain: r.envelope for r in results}
    assert by_gain[0.08] == "in_envelope"
    assert by_gain[10.00] == "abstract_probe"


def test_a_permissive_model_is_censored_high_not_given_a_number():
    cells = framing_cells()[:1]
    provider = FakeProvider(_accept_below(99.0))
    results = run_phase1(provider, cells=cells, gains=(0.08,),
                         rules=SweepRules())
    assert results[0].outcome is Outcome.CENSORED_HIGH
    assert results[0].interval is None


def test_each_cell_gets_its_own_offer_not_the_last_loop_value():
    """Guards the closure binding in run_phase1.

    `evaluate` binds cell and gain through default arguments. Today that is belt-and-
    braces, because run_sweep consumes the callable synchronously before the loop
    advances. But if evaluation were ever deferred or batched, late binding would make
    every cell evaluate against the LAST cell of the loop — producing a dataset that
    looks entirely plausible and is entirely wrong. Nothing else in the suite notices.
    """
    cells = framing_cells()[:2]
    provider = FakeProvider(lambda p: "DECISION: DECLINE")
    run_phase1(provider, cells=cells, gains=(0.08,), rules=SweepRules(replicates=1))
    assert len(set(provider.prompts)) == len(provider.prompts)


def test_bracketed_outcome_carries_its_interval_through_the_runner():
    """Only CENSORED_HIGH was exercised end-to-end; the runner must also pass a real
    interval through unchanged."""
    provider = FakeProvider(_accept_below(1.2))
    results = run_phase1(provider, cells=framing_cells()[:1], gains=(0.08,),
                         rules=SweepRules())
    assert results[0].outcome is Outcome.BRACKETED
    lo, hi = results[0].interval
    assert lo < hi


def test_results_round_trip_through_jsonl(tmp_path):
    cells = framing_cells()[:1]
    provider = FakeProvider(_accept_below(1.2))
    results = run_phase1(provider, cells=cells, gains=(0.08,),
                         rules=SweepRules())
    path = tmp_path / "phase1.jsonl"
    write_jsonl(results, path)
    assert [r.model_dump() for r in read_jsonl(path)] == [
        r.model_dump() for r in results]
