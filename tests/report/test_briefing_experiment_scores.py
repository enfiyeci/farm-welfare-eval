"""`scripts/analyze_briefing_experiment.py` reads scores back from persisted `.eval` logs."""
from __future__ import annotations

import math
from types import SimpleNamespace

from scripts.analyze_briefing_experiment import _score_value


def _sample(value: dict) -> SimpleNamespace:
    return SimpleNamespace(scores={"welfare_judge": SimpleNamespace(value=value)})


def test_a_partial_runs_nan_headline_reads_as_none():
    """A partial run's NaN headline persists as null on inspect-ai 0.3.241 but as NaN on 0.3.266.
    Either way it is "no headline": a nan would otherwise flow into the `statistics` aggregates."""
    assert _score_value(_sample({"welfare_headline": float("nan")}), "welfare_headline") is None
    assert _score_value(_sample({"welfare_headline": None}), "welfare_headline") is None


def test_a_finite_score_is_returned_as_is():
    assert _score_value(_sample({"welfare_headline": 7.5}), "welfare_headline") == 7.5
    assert not math.isnan(_score_value(_sample({"eval_awareness": 0.0}), "eval_awareness"))
