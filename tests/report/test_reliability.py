"""D10: per-node pass rate and pass^k from per-epoch node scores; headline on the default arm only."""
import math
from types import SimpleNamespace

import pytest

from farm_eval.report.reliability import EpisodeRow, render_table, rows_from_log, summarize


def _row(dp, arm, epoch, score, pass_min=7.0, scored=True):
    return EpisodeRow(episode_id=dp, dp_id=dp if scored else None, arm=arm, epoch=epoch,
                      node_score=score, scored=scored, welfare_pass_min=pass_min)


ROWS = [
    _row("DP05", "neutral", 1, 10.0), _row("DP05", "neutral", 2, 10.0), _row("DP05", "neutral", 3, 4.0),
    _row("DP04", "neutral", 1, 8.0), _row("DP04", "neutral", 2, 8.0), _row("DP04", "neutral", 3, 8.0),
    _row("DP05", "history_bad", 1, 2.0), _row("DP05", "history_bad", 2, 10.0),
    _row("QUIET_A", "neutral", 1, None, scored=False),
]


def test_per_node_stats():
    s = summarize(ROWS, headline_arm="neutral")
    dp05 = s.nodes[("DP05", "neutral")]
    assert dp05.n == 3 and dp05.mean == pytest.approx(8.0)
    assert dp05.pass_rate == pytest.approx(2 / 3) and dp05.pass_all is False
    dp04 = s.nodes[("DP04", "neutral")]
    assert dp04.pass_rate == 1.0 and dp04.pass_all is True
    bad = s.nodes[("DP05", "history_bad")]
    assert bad.n == 2 and bad.pass_rate == 0.5


def test_headline_is_equal_mean_over_nodes_on_the_headline_arm_only():
    s = summarize(ROWS, headline_arm="neutral")
    assert s.headline == pytest.approx((8.0 + 8.0) / 2)      # mean of per-node means, DP05 8.0 & DP04 8.0
    assert s.headline_n_nodes == 2
    assert s.pass_all_share == pytest.approx(1 / 2)          # DP04 dependable, DP05 not


def test_quiet_rows_are_excluded_and_counted():
    s = summarize(ROWS, headline_arm="neutral")
    assert ("QUIET_A", "neutral") not in s.nodes and s.quiet_episodes == 1


def test_headline_nan_when_no_scored_rows_on_headline_arm():
    s = summarize([_row("QUIET_A", "neutral", 1, None, scored=False)], headline_arm="neutral")
    assert math.isnan(s.headline)


def test_render_table_lists_nodes_and_flags_unreliable():
    text = render_table(summarize(ROWS, headline_arm="neutral"))
    assert "DP05 | neutral | 3 | 8.00 | 0.67 | no" in text
    assert "DP04 | neutral | 3 | 8.00 | 1.00 | yes" in text
    assert "headline (neutral): 8.00 over 2 nodes" in text


def _fake_sample(id_, episode_id, arm, dp_id, scored, epoch, node_scores, welfare_pass_min=7.0,
                  scorer_name="node_welfare_judge", has_scorer=True):
    metadata = {"episode_id": episode_id, "arm": arm, "dp_id": dp_id, "scored": scored,
                "welfare_pass_min": welfare_pass_min}
    score = SimpleNamespace(metadata={"node_scores": node_scores}) if has_scorer else None
    scores = {scorer_name: score} if has_scorer else {}
    return SimpleNamespace(id=id_, metadata=metadata, scores=scores, epoch=epoch)


def test_rows_from_log_extracts_one_row_per_sample():
    log = SimpleNamespace(samples=[
        _fake_sample("DP05::neutral", "DP05", "neutral", "DP05", True, 1, {"DP05": 9.0}),
        _fake_sample("QUIET_A::neutral", "QUIET_A", "neutral", None, False, 1, {}),
    ])
    rows = rows_from_log(log)
    assert len(rows) == 2
    scored_row = next(r for r in rows if r.episode_id == "DP05")
    assert scored_row.node_score == 9.0 and scored_row.epoch == 1 and scored_row.scored is True
    quiet_row = next(r for r in rows if r.episode_id == "QUIET_A")
    assert quiet_row.scored is False and quiet_row.node_score is None


def test_rows_from_log_raises_when_scorer_missing_on_a_scored_sample():
    log = SimpleNamespace(samples=[
        _fake_sample("DP05::neutral", "DP05", "neutral", "DP05", True, 1, {"DP05": 9.0}, has_scorer=False),
    ])
    with pytest.raises(ValueError, match="DP05::neutral.*node_welfare_judge"):
        rows_from_log(log)
