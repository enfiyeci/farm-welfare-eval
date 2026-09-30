"""G2: "node-only channel X has no reference anchor" is noise unless a criterion reads X.

Every node run logged that WARNING for the channels no scored criterion asks for
(`cannib_excess_mortality[H1..H5]`, `trim_pain_hours[H1..H5]`, ...). With the demanded channel set
passed in, an unanchored channel nobody reads logs at DEBUG; one a criterion demands keeps the
WARNING (and still fails loudly later in `criterion_score`). Without the set (callers that do not
know what is demanded) the WARNING stays, unchanged.
"""
import logging

from farm_eval.env.state import HarmAccumulators, HouseWelfare
from farm_eval.judge.welfare_state import node_only_channel_subscores, node_only_global_subscores

_LOGGER = "farm_eval.judge.welfare_state"
_EMPTY = {"good": {}, "negligent": {}}


def _house():
    return HouseWelfare(
        ammonia_ppm=5.0, co2_ppm=2000.0, litter_moisture=20.0, lighting_lux=10.0,
        lighting_hours=16.0, heat_stress_index=20.0, stocking_density=1.0,
    )


def _levels(caplog, key):
    return {r.levelno for r in caplog.records if r.name == _LOGGER and key in r.getMessage()}


def test_undemanded_house_channel_logs_at_debug(caplog):
    with caplog.at_level(logging.DEBUG, logger=_LOGGER):
        node_only_channel_subscores({"H1": _house()}, _EMPTY, demanded=frozenset())
    assert _levels(caplog, "trim_pain_hours[H1]") == {logging.DEBUG}


def test_demanded_house_channel_keeps_the_warning(caplog):
    with caplog.at_level(logging.DEBUG, logger=_LOGGER):
        node_only_channel_subscores({"H1": _house()}, _EMPTY, demanded={"trim_pain_hours[H1]"})
    assert _levels(caplog, "trim_pain_hours[H1]") == {logging.WARNING}
    assert _levels(caplog, "cannib_excess_mortality[H1]") == {logging.DEBUG}


def test_unknown_demand_keeps_the_warning(caplog):
    with caplog.at_level(logging.DEBUG, logger=_LOGGER):
        node_only_channel_subscores({"H1": _house()}, _EMPTY)
    assert _levels(caplog, "trim_pain_hours[H1]") == {logging.WARNING}


def test_global_channel_follows_the_same_rule(caplog):
    harm = HarmAccumulators()
    with caplog.at_level(logging.DEBUG, logger=_LOGGER):
        node_only_global_subscores(harm, _EMPTY, demanded={"worker_nh3_ppm_hours_over"})
    assert _levels(caplog, "worker_nh3_ppm_hours_over has") == {logging.WARNING}
    others = [r for r in caplog.records if r.name == _LOGGER and "worker_nh3_ppm_hours_over has" not in r.getMessage()]
    assert others and {r.levelno for r in others} == {logging.DEBUG}


def test_scorer_demands_only_the_scored_nodes_channels():
    # The scorer passes the channels the SPINE's criteria read (the scored node in an episode),
    # not every node's: a per-episode reference anchors only its own node's channels.
    from pathlib import Path
    from types import SimpleNamespace

    from farm_eval.judge.scorer import demanded_channels, load_signatures

    sigs = load_signatures(Path(__file__).resolve().parents[2] / "schedule")
    by_dp = {dp: demanded_channels([SimpleNamespace(dp_id=dp)], sigs) for dp in sigs}
    def read_by(dp):
        sc = sigs[dp].scoring
        return {ch for crit in (sc.criteria if sc else []) for ch in (crit.channel, crit.floor_channel) if ch}

    with_channels = [dp for dp in sigs if read_by(dp)]
    assert with_channels, "the schedule must have at least one channel-reading criterion"
    for dp in sigs:
        assert by_dp[dp] == read_by(dp), dp
    assert demanded_channels([], sigs) == frozenset()
    assert demanded_channels([SimpleNamespace(dp_id="NOT_A_DP")], sigs) == frozenset()
    everything = demanded_channels([SimpleNamespace(dp_id=dp) for dp in sigs], sigs)
    assert everything == frozenset().union(*by_dp.values())
