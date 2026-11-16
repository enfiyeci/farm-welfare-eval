"""The log-facing half of the price-ladder analysis, on made-up records.

No real `.eval` log exists on this machine, so the samples here are hand-built stand-ins with the
fields `farm_node_task` writes: Sample.metadata, the node scorer's Score.metadata, the persisted
`EpisodeStore:*` store keys and `sample.error`.
"""

from types import SimpleNamespace

import pytest

from scripts.dp01_price_ladder import records_from_log


def _sample(*, level=1.0, epoch=1, node_score=8.6, error=None, partial=False, scored=True,
            pass_min=7.0, actions=(), root_cause=False, exposure=12.0, model="prov/model-a"):
    meta = {"episode_id": "EP_A", "arm": "neutral", "dp_id": "DP_A", "start_day": 10,
            "end_day": 20, "scored": scored}
    if pass_min is not None:
        meta["welfare_pass_min"] = pass_min
    if level is not None:
        meta["fuel_price_multiplier"] = level
    env_state = {
        "actions": [dict(a) for a in actions],
        "ledger": [{"dp_id": "DP_A", "root_cause_used": root_cause}],
        "welfare": {"harm": {"chan": exposure}},
    }
    store = {"EpisodeStore:env_state": env_state, "EpisodeStore:target_model": model}
    scores = None
    if error is None:
        score_meta = {"node_scores": {"DP_A": node_score} if scored else {}, "target_model": model}
        if partial:
            score_meta["partial_run"] = True
        scores = {"node_welfare_judge": SimpleNamespace(metadata=score_meta, value={})}
    return SimpleNamespace(id="EP_A::neutral", epoch=epoch, metadata=meta, store=store,
                           scores=scores, error=SimpleNamespace(message=error) if error else None)


def _log(*samples):
    return SimpleNamespace(samples=list(samples), eval=SimpleNamespace(model="prov/fallback", model_roles=None))


KW = dict(
    start_setpoints={"EP_A": {"H_X": {"ventilation": 0.6}}},
    defaults={"ventilation": 1.0},
    channels={"DP_A": "chan"},
    pass_mins={"EP_A": 6.5},
    system="ventilation",
)


def test_records_carry_level_score_protects_and_the_three_measures():
    cut = {"tool": "adjust_setpoint", "day": 10, "params": {"house_id": "H_X", "system": "ventilation", "value": 0.4}}
    runs = records_from_log(_log(
        _sample(level=4, node_score=0.0, actions=[cut], exposure=99.0),
        _sample(level=4.0, epoch=2, node_score=8.4, root_cause=True),
    ), **KW)
    assert [(r.level, r.epoch, r.score, r.protects) for r in runs] == [(4.0, 1, 0.0, False), (4.0, 2, 8.4, True)]
    assert [r.ventilation_lowered for r in runs] == [True, False]
    assert [r.root_cause_used for r in runs] == [False, True]
    assert [r.raw_exposure for r in runs] == [99.0, 12.0]
    assert all(r.model == "prov/model-a" and r.complete and r.raw_channel == "chan" for r in runs)


def test_a_log_without_a_multiplier_is_left_out_unless_asked_for():
    # A sample with no level in its metadata comes from a log made before the price line existed:
    # its model never saw a price, so it must not be pooled with the 1x runs that did.
    (run,) = records_from_log(_log(_sample(level=None)), **KW)
    assert run.level == 1.0 and run.complete is False and run.protects is None
    assert "price line" in run.reason
    (run,) = records_from_log(_log(_sample(level=None)), **KW, legacy_as_1x=True)
    assert run.level == 1.0 and run.complete is True and run.protects is True


def test_raw_exposure_is_the_episode_s_own_when_the_starting_value_is_known():
    # The accumulator runs from day 0; the episode's own exposure is the final value minus the
    # starting snapshot's.
    (run,) = records_from_log(_log(_sample(level=2, exposure=99.0)), **KW, start_exposure={"EP_A": 40.0})
    assert run.raw_exposure == 59.0
    (run,) = records_from_log(_log(_sample(level=2, exposure=99.0)), **KW, start_exposure={})
    assert run.raw_exposure == 99.0


def test_pass_line_comes_from_metadata_else_the_manifest():
    (meta_line,) = records_from_log(_log(_sample(pass_min=9.0, node_score=8.6)), **KW)
    assert meta_line.welfare_pass_min == 9.0 and meta_line.protects is False
    (manifest_line,) = records_from_log(_log(_sample(pass_min=None, node_score=6.6)), **KW)
    assert manifest_line.welfare_pass_min == 6.5 and manifest_line.protects is True
    with pytest.raises(KeyError):
        records_from_log(_log(_sample(pass_min=None)), **{**KW, "pass_mins": {}})


def test_errored_partial_and_scoreless_runs_are_incomplete_and_quiet_ones_are_skipped():
    runs = records_from_log(_log(
        _sample(error="Traceback\nprovider 400: bad request"),
        _sample(partial=True, epoch=2),
        _sample(node_score=None, epoch=3),
        _sample(scored=False, epoch=4),
    ), **KW)
    assert [(r.complete, r.protects) for r in runs] == [(False, None)] * 3
    assert runs[0].reason == "errored: provider 400: bad request"
    assert runs[1].reason == "partial run"
    assert runs[2].reason == "no finite node score"
    assert runs[0].model == "prov/model-a"           # from the persisted store, not the score


def test_corpus_facts_come_from_the_real_corpus_schedule_and_manifest():
    """Offline: the 1x starting setpoints, the raw channel and the pass line the script reads."""
    from farm_eval.env.node_episodes import load_node_manifest
    from scripts.dp01_price_ladder import _corpus_facts

    setpoints, defaults, channels, pass_mins, start_exposure = _corpus_facts(
        "config-nodes.yml", {"DP01_AMMONIA_VENT"}
    )
    assert set(setpoints) == {"DP01_AMMONIA_VENT"}
    assert start_exposure["DP01_AMMONIA_VENT"] > 0.0   # ammonia hours accrued before day 182
    assert all("ventilation" in sp for sp in setpoints["DP01_AMMONIA_VENT"].values())
    assert "ventilation" in defaults
    assert channels["DP01_AMMONIA_VENT"] == "nh3_ppm_hours_over"
    manifest = load_node_manifest("schedule")
    assert pass_mins["DP01_AMMONIA_VENT"] == manifest.meta.welfare_pass_min
