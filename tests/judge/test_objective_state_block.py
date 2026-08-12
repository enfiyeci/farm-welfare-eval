"""D9 (owner ruling, 2026-08-11): llm criteria on nodes that declare `signals` get an
OBJECTIVE STATE block — the window's true daily figures — so the grader checks claimed
readings against ground truth, not just the transcript."""

from farm_eval.env.ledger import LedgerEntry
from farm_eval.env.state import EnvState, HouseWelfare, WelfareState
from farm_eval.judge.scorer import build_objective_state_block


def _house():
    return HouseWelfare(
        ammonia_ppm=5.0, co2_ppm=2000.0, litter_moisture=20.0, lighting_lux=10.0,
        lighting_hours=16.0, heat_stress_index=20.0, stocking_density=1.0,
    )


class _DP:
    def __init__(self, signals, opens_day):
        self.signals = signals
        self.opens_day = opens_day


def _state():
    st = EnvState(start_date="2025-06-09")
    st.welfare = WelfareState(houses={"H2": _house()})
    st.daily_series_days = [1, 2, 3, 4, 5]
    st.daily_series = {"H2": {"water_ml": [200.0, 201.0, 150.0, 149.0, 148.0]}}
    return st


def _entry(opens, deadline):
    return LedgerEntry(dp_id="DPX", category="epistemic", opened_day=opens, deadline_day=deadline)


def test_block_serves_window_days_only():
    dp = _DP([{"metric": "water_ml", "reliability": "high"}], opens_day=3)
    block = build_objective_state_block(dp, _entry(3, 5), _state())
    assert "water_ml" in block and "H2" in block
    assert "150" in block and "148" in block     # days 3-5 present
    assert "200" not in block and "201" not in block   # days 1-2 excluded


def test_no_signals_or_no_series_means_no_block():
    dp_none = _DP([], opens_day=3)
    assert build_objective_state_block(dp_none, _entry(3, 5), _state()) is None
    dp = _DP([{"metric": "water_ml", "reliability": "high"}], opens_day=3)
    empty = _state()
    empty.daily_series = {}
    empty.daily_series_days = []
    assert build_objective_state_block(dp, _entry(3, 5), empty) is None
