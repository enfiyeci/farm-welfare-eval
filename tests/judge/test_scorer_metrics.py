"""D3 Fix 1 — the Inspect displayed-metric mis-key.

`welfare_judge` returns `Score(value=<dict>)` where the real headline lives at
`value["welfare_headline"]`. Declaring `@scorer(metrics=[mean(), stderr()])` (simple, non-dict
metrics) applies those metrics to the raw Score.value — which for a dict-valued score is not a
number, so the CLI displays a degenerate `mean 0.000` instead of the real headline.

Pinned Inspect version (0.3.241) supports a dict-of-metrics form for dict-valued scores:
`scorer(metrics: Sequence[Metric | Mapping[str, Sequence[Metric]]] | Mapping[str, Sequence[Metric]])`
(`inspect_ai/scorer/_scorer.py`). This test introspects the registered scorer's metrics metadata
(the `SCORER_METRICS` registry entry the `@scorer` decorator stashes) to assert the declaration
keys `welfare_headline` specifically, rather than only checking behavior at the CLI-log level
(covered separately by the end-to-end smoke test in `tests/adapter/test_task.py`).
"""

from inspect_ai.scorer._scorer import SCORER_METRICS
from inspect_ai._util.registry import registry_info

from farm_eval.judge.scorer import welfare_judge


def _registered_metrics():
    # `welfare_judge` is the @scorer-decorated factory; the registry info lives on the factory
    # itself (registry_tag / scorer_register both stash SCORER_METRICS in RegistryInfo.metadata,
    # keyed off the *type* passed to @scorer, not a particular instantiation).
    return registry_info(welfare_judge).metadata[SCORER_METRICS]


def test_metrics_declaration_keys_welfare_headline():
    """The registered metrics config must be dict-shaped (or contain a dict entry) whose key is
    `welfare_headline` — NOT a bare list of simple Metric objects (which would apply mean/stderr
    to the whole dict value and silently degenerate to 0)."""
    metrics = _registered_metrics()

    def _has_welfare_headline_key(m) -> bool:
        if isinstance(m, dict):
            return "welfare_headline" in m
        if isinstance(m, (list, tuple)):
            return any(_has_welfare_headline_key(item) for item in m)
        return False

    assert _has_welfare_headline_key(metrics), (
        f"expected a dict-of-metrics keying 'welfare_headline', got: {metrics!r}"
    )


def test_metrics_declaration_is_not_a_bare_simple_list():
    """Regression guard for the original bug: `metrics=[mean(), stderr()]` with no dict entry at
    all — that form applies to the raw (dict-valued) Score.value and the CLI shows a degenerate
    mean over a dict, never the real headline."""
    metrics = _registered_metrics()
    if isinstance(metrics, (list, tuple)):
        assert any(isinstance(m, dict) for m in metrics), (
            "metrics declared as a flat list of simple Metric objects with no dict entry — "
            "this mis-keys the CLI display against a dict-valued Score"
        )
    else:
        assert isinstance(metrics, dict)
