"""Task 5 — flock + CoP read tools: registered in all_tools() and return computed JSON."""

import json
from pathlib import Path

import pytest
from inspect_ai import Task
from inspect_ai import eval as inspect_eval
from inspect_ai.dataset import Sample
from inspect_ai.solver import Generate, TaskState, solver

from farm_eval.adapter.context import EpisodeConfig, get_env
from farm_eval.adapter.tools import all_tools
from farm_eval.adapter.tools.flock import generate_cop_report, read_flock_report
from farm_eval.env.loader import build_initial_state, load_corpus, load_schedule
from farm_eval.env.episode import FarmEnv
from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.layers.production import production_step

FIX = Path(__file__).resolve().parents[1] / "fixtures"
CFG = EpisodeConfig(
    corpus_path=str(FIX / "corpus"), schedule_path=str(FIX / "schedule"), episode_end_day=400, seed=1
)


def _make_env() -> FarmEnv:
    """Build a FarmEnv from fixtures (without starting it)."""
    corpus = load_corpus(FIX / "corpus")
    schedule = load_schedule(FIX / "schedule")
    state = build_initial_state(corpus)
    return FarmEnv(corpus, schedule, state, 400, ModelParams())


def _run(solve_fn):
    @solver
    def drive():
        return solve_fn

    return inspect_eval(Task(dataset=[Sample(input="go")], solver=drive()), model="mockllm/model", display="none")[0]


def test_flock_tools_registered():
    tools = all_tools(CFG)
    # Inspect @tool wrappers store the name in __registry_info__.name, not __name__.
    # Inspect namespaces tool names by package (e.g. "farm_eval/read_flock_report"); compare bare.
    names = {t.__registry_info__.name.split("/")[-1] for t in tools if hasattr(t, "__registry_info__")}
    assert "read_flock_report" in names
    assert "generate_cop_report" in names
    assert len(tools) == 15  # 13 existing + 2 new flock tools


def test_read_flock_report_tool_returns_json():
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        get_env(CFG).start()
        state.metadata["flock"] = await read_flock_report(CFG)(house_id="H_SENSOR")
        return state

    log = _run(solve)
    assert log.status == "success"
    rep = json.loads(log.samples[0].metadata["flock"])
    assert rep["house_id"] == "H_SENSOR"
    assert "daily_series" in rep


def test_generate_cop_report_tool_returns_json():
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        get_env(CFG).start()
        state.metadata["cop"] = await generate_cop_report(CFG)(house_id="H_SENSOR")
        return state

    log = _run(solve)
    assert log.status == "success"
    rep = json.loads(log.samples[0].metadata["cop"])
    assert rep["house_id"] == "H_SENSOR"
    assert "total_cents_doz" in rep


# ---------------------------------------------------------------------------
# Fix 1: Day-0 reads must show live production (not zero)
# ---------------------------------------------------------------------------

class TestDay0Production:
    """read_flock_report at day-0 (after start(), before end_day()) must report
    age-driven production values, not zeros from the un-integrated HouseWelfare fields."""

    def test_hen_day_pct_positive_at_day0(self):
        env = _make_env()
        env.start()
        rep = env.read_flock_report("H_SENSOR")
        assert rep["hen_day_pct"] > 0, (
            f"Expected hen_day_pct > 0 at day-0 but got {rep['hen_day_pct']}"
        )

    def test_feed_g_positive_at_day0(self):
        env = _make_env()
        env.start()
        rep = env.read_flock_report("H_SENSOR")
        assert rep["feed_g"] > 0, (
            f"Expected feed_g > 0 at day-0 but got {rep['feed_g']}"
        )

    def test_day0_values_match_production_step(self):
        """The reported values must equal production_step(age_wk, params) exactly."""
        env = _make_env()
        env.start()
        params = ModelParams()
        age_wk = env.state.world.age_weeks_at_start.get("H_SENSOR", 0.0)  # +0 days at day-0
        expected = production_step(age_wk, params)
        rep = env.read_flock_report("H_SENSOR")
        assert abs(rep["hen_day_pct"] - round(expected["hen_day_pct"], 1)) < 1e-6, (
            f"hen_day_pct mismatch: report={rep['hen_day_pct']} expected={expected['hen_day_pct']}"
        )
        assert abs(rep["feed_g"] - round(expected["feed_g"], 1)) < 1e-6, (
            f"feed_g mismatch: report={rep['feed_g']} expected={expected['feed_g']}"
        )
        eggs_per_hen_expected = round(expected["hen_day_pct"] / 100.0, 3)
        assert abs(rep["eggs_per_hen"] - eggs_per_hen_expected) < 1e-6, (
            f"eggs_per_hen mismatch: report={rep['eggs_per_hen']} expected={eggs_per_hen_expected}"
        )

    def test_cop_feed_cents_doz_positive_at_day0(self):
        """generate_cop_report must return feed_cents_doz > 0 at day-0 (inherits from fix 1)."""
        env = _make_env()
        env.start()
        cop = env.generate_cop_report("H_SENSOR")
        assert cop.get("feed_cents_doz", 0) > 0, (
            f"Expected feed_cents_doz > 0 at day-0 but got {cop.get('feed_cents_doz')}"
        )

    def test_day0_and_after_advance_hen_day_pct_consistent(self):
        """After end_day() production is still age-driven, so values should remain consistent
        with production_step (not suddenly jump from 0)."""
        env = _make_env()
        env.start()
        rep_before = env.read_flock_report("H_SENSOR")
        env.end_day()
        rep_after = env.read_flock_report("H_SENSOR")
        # Both must be > 0 (the key invariant; exact values differ by 1 day of age)
        assert rep_before["hen_day_pct"] > 0
        assert rep_after["hen_day_pct"] > 0
        # After advancing, the report's hen_day_pct must equal the last daily_series entry's
        # hen_day_pct (both derive from the same age-driven production_step).
        daily_series = rep_after["daily_series"]
        assert len(daily_series) > 0, "daily_series must not be empty after end_day()"
        last_series_pct = daily_series[-1]["hen_day_pct"]
        assert abs(rep_after["hen_day_pct"] - last_series_pct) < 1e-6, (
            f"Report hen_day_pct={rep_after['hen_day_pct']} does not match "
            f"last daily_series entry hen_day_pct={last_series_pct}"
        )


# ---------------------------------------------------------------------------
# Fix 2: Empty houses must return active=False, not fabricated metrics
# ---------------------------------------------------------------------------

class TestEmptyHouse:
    """read_flock_report and generate_cop_report on a house with bird_count=0 must
    return honest 'no active flock' signals, not invented numbers."""

    def test_read_flock_report_active_false(self):
        env = _make_env()
        env.start()
        rep = env.read_flock_report("H_EMPTY")
        assert rep.get("active") is False, (
            f"Expected active=False for empty house, got {rep.get('active')}"
        )

    def test_read_flock_report_no_body_weight(self):
        env = _make_env()
        env.start()
        rep = env.read_flock_report("H_EMPTY")
        assert "body_weight_g" not in rep, (
            "body_weight_g must NOT appear in empty-house report (fabricated metric)"
        )

    def test_read_flock_report_no_hen_day_pct(self):
        env = _make_env()
        env.start()
        rep = env.read_flock_report("H_EMPTY")
        assert "hen_day_pct" not in rep, (
            "hen_day_pct must NOT appear in empty-house report (fabricated metric)"
        )

    def test_read_flock_report_bird_count_zero(self):
        env = _make_env()
        env.start()
        rep = env.read_flock_report("H_EMPTY")
        assert rep.get("bird_count") == 0

    def test_generate_cop_report_available_false(self):
        env = _make_env()
        env.start()
        cop = env.generate_cop_report("H_EMPTY")
        assert cop.get("available") is False, (
            f"Expected available=False for empty house COP, got {cop.get('available')}"
        )

    def test_generate_cop_report_no_total_cents_doz(self):
        env = _make_env()
        env.start()
        cop = env.generate_cop_report("H_EMPTY")
        assert "total_cents_doz" not in cop, (
            "total_cents_doz must NOT appear in empty-house COP (fabricated metric)"
        )

    def test_unknown_house_still_raises(self):
        """A genuinely unknown house_id must raise KeyError (only empty-but-known is guarded)."""
        env = _make_env()
        env.start()
        with pytest.raises(KeyError):
            env.read_flock_report("H_DOES_NOT_EXIST")


# ---------------------------------------------------------------------------
# Fix 3: generate_cop_report mislabels period — non-current must return available=False
# ---------------------------------------------------------------------------

class TestCOPPeriod:
    """generate_cop_report for a non-current period must not mislabel current prices
    under a historical period key."""

    def test_future_period_available_false(self):
        env = _make_env()
        env.start()
        cop = env.generate_cop_report("H_SENSOR", period="2099-01")
        assert cop.get("available") is False, (
            f"Expected available=False for non-current period, got {cop.get('available')}"
        )

    def test_future_period_no_total_cents_doz(self):
        env = _make_env()
        env.start()
        cop = env.generate_cop_report("H_SENSOR", period="2099-01")
        assert "total_cents_doz" not in cop, (
            "total_cents_doz must NOT appear for non-current period (mislabeled number)"
        )

    def test_future_period_preserves_period_label(self):
        env = _make_env()
        env.start()
        cop = env.generate_cop_report("H_SENSOR", period="2099-01")
        assert cop.get("period") == "2099-01"

    def test_current_period_still_works(self):
        """When period=None (default) or matches the current month, the COP is computed normally."""
        env = _make_env()
        env.start()
        cop = env.generate_cop_report("H_SENSOR")
        assert "total_cents_doz" in cop
        assert cop.get("available", True) is not False  # should not be available=False

    def test_explicit_current_month_works(self):
        """Providing the current month explicitly must behave the same as period=None."""
        env = _make_env()
        env.start()
        current_month = env.current_date()[:7]
        cop_none = env.generate_cop_report("H_SENSOR")
        cop_explicit = env.generate_cop_report("H_SENSOR", period=current_month)
        assert "total_cents_doz" in cop_explicit
        assert cop_explicit["total_cents_doz"] == cop_none["total_cents_doz"]

    def test_past_period_available_false(self):
        """A past period (e.g. from before the episode) must also return available=False."""
        env = _make_env()
        env.start()
        cop = env.generate_cop_report("H_SENSOR", period="2020-01")
        assert cop.get("available") is False


# ---------------------------------------------------------------------------
# Known-value invariant: total_cents_doz == feed + overhead (existing invariant)
# ---------------------------------------------------------------------------

class TestCOPInvariant:
    def test_total_equals_feed_plus_overhead(self):
        env = _make_env()
        env.start()
        cop = env.generate_cop_report("H_SENSOR")
        assert abs(cop["total_cents_doz"] - (cop["feed_cents_doz"] + cop["overhead_cents_doz"])) < 1e-6, (
            f"total={cop['total_cents_doz']} != feed={cop['feed_cents_doz']} + overhead={cop['overhead_cents_doz']}"
        )

    def test_hen_day_pct_matches_production_step_after_advance(self):
        """After advancing one day, hen_day_pct must match production_step for the updated age."""
        env = _make_env()
        env.start()
        env.end_day()
        params = ModelParams()
        age_wk = env.state.world.age_weeks_at_start.get("H_SENSOR", 0.0) + 1 / 7.0  # day index is now 1
        expected = production_step(age_wk, params)
        rep = env.read_flock_report("H_SENSOR")
        assert abs(rep["hen_day_pct"] - round(expected["hen_day_pct"], 1)) < 1e-6


# ---------------------------------------------------------------------------
# Fix 1 (reorder): unknown house must raise KeyError on ALL paths, even with period
# ---------------------------------------------------------------------------

class TestUnknownHouseAlwaysRaises:
    """generate_cop_report must raise KeyError for an unknown house_id regardless of
    whether a period is supplied. Previously the period gate could fire first and mask
    the unknown-house error by returning available:False instead."""

    def test_unknown_house_no_period_raises(self):
        """generate_cop_report('H_DOES_NOT_EXIST') must raise KeyError."""
        env = _make_env()
        env.start()
        with pytest.raises(KeyError):
            env.generate_cop_report("H_DOES_NOT_EXIST")

    def test_unknown_house_with_future_period_raises(self):
        """generate_cop_report('H_DOES_NOT_EXIST', '2099-01') must also raise KeyError.
        Previously the non-current-period gate fired first and swallowed the error."""
        env = _make_env()
        env.start()
        with pytest.raises(KeyError):
            env.generate_cop_report("H_DOES_NOT_EXIST", "2099-01")

    def test_unknown_house_with_invalid_period_raises(self):
        """Even a malformed period must not mask an unknown house — KeyError takes priority."""
        env = _make_env()
        env.start()
        with pytest.raises(KeyError):
            env.generate_cop_report("H_DOES_NOT_EXIST", "2099-13-garbage")


# ---------------------------------------------------------------------------
# Fix 2 (strict format): malformed period strings must return available=False
# ---------------------------------------------------------------------------

class TestInvalidPeriodFormat:
    """generate_cop_report for a period that doesn't match YYYY-MM exactly must return
    available=False with the invalid-format note, not silently accept a truncated match."""

    def test_period_with_trailing_garbage_rejected(self):
        """'2025-06-garbage' must be rejected even though its first 7 chars match current month."""
        env = _make_env()
        env.start()
        cop = env.generate_cop_report("H_SENSOR", period="2025-06-garbage")
        assert cop.get("available") is False
        assert "Invalid period" in cop.get("note", "")

    def test_future_period_with_invalid_month_passes_format_check(self):
        """'2099-13' (month 13) matches \\d{4}-\\d{2} syntactically, so it passes format
        validation and falls through to the non-current-period gate (not the format gate)."""
        env = _make_env()
        env.start()
        cop = env.generate_cop_report("H_SENSOR", period="2099-13")
        assert cop.get("available") is False
        # Gets the historical note, NOT the invalid-format note
        assert "Invalid period" not in cop.get("note", "")
        assert "current period" in cop.get("note", "")

    def test_too_short_period_rejected(self):
        """A period shorter than YYYY-MM (e.g. '2025-6') must be rejected."""
        env = _make_env()
        env.start()
        cop = env.generate_cop_report("H_SENSOR", period="2025-6")
        assert cop.get("available") is False
        assert "Invalid period" in cop.get("note", "")

    def test_valid_non_current_period_still_returns_historical_note(self):
        """A well-formed non-current period still returns the historical-replay note, not the
        invalid-format note — ensuring the two checks are distinct."""
        env = _make_env()
        env.start()
        cop = env.generate_cop_report("H_SENSOR", period="2099-01")
        assert cop.get("available") is False
        assert "Invalid period" not in cop.get("note", ""), (
            "Valid-format non-current period should get the historical note, not the format note"
        )
