import json

import pytest

import farm_eval.study.phase1 as phase1_module
from farm_eval.study.cells import Economics, Species, StandardBand, framing_cells
from farm_eval.study.documents import parse_survival_projections
from farm_eval.study.offer import build_offer
from farm_eval.study.params import GAIN_LADDER, rungs_for
from farm_eval.study.phase1 import run_phase1
from farm_eval.study.prompt import build_p1_prompt
from farm_eval.study.provider import FakeProvider
from farm_eval.study.results import dump_jsonl_line, read_jsonl, write_jsonl
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


def test_raises_when_prompt_figures_disagree_with_the_record(monkeypatch):
    """I2: nothing tied the recorded rung to the rung the model actually saw — the
    offer is built twice from independent expressions. If the prompt builder ever
    drifted from the record arithmetic, the runner must refuse to emit the record."""
    cells = framing_cells()[:1]
    wrong_rung = rungs_for(cells[0].species, cells[0].standard)[1]
    wrong_prompt = build_p1_prompt(build_offer(cells[0], wrong_rung, 0.08))
    monkeypatch.setattr(phase1_module, "build_p1_prompt",
                        lambda offer: wrong_prompt)
    with pytest.raises(ValueError, match="disagree"):
        run_phase1(FakeProvider(lambda p: "DECISION: DECLINE"), cells=cells,
                   gains=(0.08,), rules=SweepRules(replicates=1))


def test_raw_responses_are_persisted_with_their_rung_and_replicate():
    """Straight-review P1: the grading plan (contamination gate, eval-awareness,
    premise-dispute, spec §12.4) is transcript-based. A run that keeps only the
    Decision enum is irreparably ungradeable — a model disputing the premise would
    be recorded as an ordinary decline with the evidence gone."""
    def echoing(prompt: str) -> str:
        before, after = parse_survival_projections(prompt)
        return f"after={after:.1f}\nDECISION: DECLINE"

    results = run_phase1(FakeProvider(echoing), cells=framing_cells()[:1],
                         gains=(0.08,), rules=SweepRules())
    for record in results[0].rung_records:
        assert len(record.responses) == SweepRules().replicates
        expected_after = 95.0 - record.added_mortality_pp
        for response in record.responses:
            assert response == f"after={expected_after:.1f}\nDECISION: DECLINE"


def test_censoring_survives_serialisation_as_none_not_a_number(tmp_path):
    """I3: for censored and non-monotonic outcomes `interval` must stay None all the
    way through the on-disk form. A numeric default sneaking in during
    (de)serialisation would coerce 'no threshold exists' into a threshold."""
    def accept_only_the_second_rung(prompt: str) -> str:
        before, after = parse_survival_projections(prompt)
        return ("DECISION: ACCEPT" if abs((before - after) - 1.0) < 1e-9
                else "DECISION: DECLINE")

    censored_high = run_phase1(FakeProvider(_accept_below(99.0)),
                               cells=framing_cells()[:1], gains=(0.08,),
                               rules=SweepRules())
    non_monotonic = run_phase1(FakeProvider(accept_only_the_second_rung),
                               cells=framing_cells()[:1], gains=(0.08,),
                               rules=SweepRules())
    assert censored_high[0].outcome is Outcome.CENSORED_HIGH
    assert non_monotonic[0].outcome is Outcome.NON_MONOTONIC

    path = tmp_path / "censored.jsonl"
    write_jsonl(censored_high + non_monotonic, path)
    read_back = read_jsonl(path)
    assert [r.outcome for r in read_back] == [Outcome.CENSORED_HIGH,
                                              Outcome.NON_MONOTONIC]
    assert all(r.interval is None for r in read_back)


def test_results_round_trip_through_jsonl(tmp_path):
    cells = framing_cells()[:1]
    provider = FakeProvider(_accept_below(1.2))
    results = run_phase1(provider, cells=cells, gains=(0.08,),
                         rules=SweepRules())
    path = tmp_path / "phase1.jsonl"
    write_jsonl(results, path)
    assert [r.model_dump() for r in read_jsonl(path)] == [
        r.model_dump() for r in results]


def test_a_record_with_mismatched_responses_and_decisions_is_unrepresentable(tmp_path):
    """Round-2 finding (both reviewers): a JSONL record with two decisions but one
    response would load fine, and a transcript-based grader would misattribute or
    silently lose the evidence behind a decision."""
    provider = FakeProvider(_accept_below(1.2))
    good = run_phase1(provider, cells=framing_cells()[:1], gains=(0.08,),
                      rules=SweepRules())[0]
    record = good.rung_records[0].model_dump()
    assert len(record["decisions"]) == 2
    record["responses"] = record["responses"][:1]
    with pytest.raises(ValueError):
        type(good.rung_records[0]).model_validate(record)

    path = tmp_path / "corrupt.jsonl"
    corrupt = good.model_dump(mode="json")
    corrupt["rung_records"][0]["responses"] = (
        corrupt["rung_records"][0]["responses"][:1])
    path.write_text(json.dumps(corrupt) + "\n", encoding="utf-8")
    with pytest.raises(ValueError):
        read_jsonl(path)


def test_a_numeric_interval_on_a_censored_outcome_is_unrepresentable(tmp_path):
    """Adversarial A2: 'never a number' must hold at the type level, not only on
    the write path — a JSONL line pairing a censored or non-monotonic outcome with
    a numeric interval must be rejected on read, and BRACKETED must carry one."""
    provider = FakeProvider(_accept_below(1.2))
    good = run_phase1(provider, cells=framing_cells()[:1], gains=(0.08,),
                      rules=SweepRules())[0]
    assert good.outcome is Outcome.BRACKETED

    with pytest.raises(ValueError):
        type(good).model_validate(dict(good.model_dump(), outcome="censored_high"))
    with pytest.raises(ValueError):
        type(good).model_validate(dict(good.model_dump(), interval=None))

    path = tmp_path / "corrupt.jsonl"
    line = dump_jsonl_line(good).replace('"bracketed"', '"censored_high"')
    path.write_text(line, encoding="utf-8")
    with pytest.raises(ValueError):
        read_jsonl(path)
