from farm_eval.env.state import FinancialState
from farm_eval.env.model.economics import cop_cents_doz, margin_cents_doz


def test_cop_and_margin_per_dozen():
    # margin must be set explicitly: FinancialState.margin is computed by integrate() (not a
    # pydantic validator), so it defaults to 0.0 unless passed directly.
    f = FinancialState(revenue_cum=150.0, feed_cost_cum=40.0, other_cost_cum=50.0,
                       margin=60.0, sellable_dozen_cum=100.0)
    # total cost 90 over 100 doz = $0.90/doz = 90 cents
    assert abs(cop_cents_doz(f) - 90.0) < 1e-6
    # margin 60 over 100 doz = 60 cents
    assert abs(margin_cents_doz(f) - 60.0) < 1e-6


def test_per_dozen_zero_safe():
    f = FinancialState()  # no eggs yet
    assert cop_cents_doz(f) == 0.0
    assert margin_cents_doz(f) == 0.0


def test_cop_report_reflects_belt_run_cost():
    # Codex wave-1 review F3 (2026-08-11): the agent-visible per-house COP must mirror the
    # P&L — daily belts show higher energy cents than weekly belts. The report is a
    # current-day snapshot of standing setpoints, so one env, one day, two settings.
    from pathlib import Path
    from farm_eval.env.episode import FarmEnv

    FIX = Path(__file__).parent.parent.parent / "fixtures"
    env = FarmEnv.from_paths(FIX / "corpus", FIX / "schedule", seed=1, episode_end_day=400)
    env.start()
    while env.state.day_index < 160 and not env.is_over():   # advance into lay
        env.end_day()
    hid = next(iter(env.state.world.setpoints))

    def energy_at(belt_days):
        env.state.world.setpoints[hid]["belt_interval_days"] = belt_days
        report = env.generate_cop_report(house_id=hid)
        assert report.get("available", True), report
        return report["energy_cents_doz"]

    assert energy_at(1.0) > energy_at(7.0)
