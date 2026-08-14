# Regenerate the finance-index reference: ./venv/bin/python scripts/regen_finance_reference.py
"""Deterministic reference anchors for the mechanical finance index (L8, Task 9).

`farm_eval/judge/finance_index.py` normalizes an agent's terminal financial state against fixed,
designer-computed anchors. This script computes them the same way `regen_financial_reference.py`
computes the profit ceiling/floor: by driving the REAL `FarmEnv.start()/end_day()` pipeline over
`config.yml`'s horizon under scripted policies, never by hand-fitting numbers.

Writes `farm_eval/judge/finance_reference.json`:

- `margin`: `ceiling_usd` / `floor_usd`, copied from `financial_reference.json`'s
  `normalizer_recommended` block so the two artifacts cannot disagree. Run
  `scripts/regen_financial_reference.py` FIRST.
- `financing.minimum_interest_usd`: interest + switch fees paid by the minimum-feasible-interest
  policy — sweep on from day 0, the cheapest available lender at every point on the grid, and the
  drawn balance repaid in full at every wake day it is positive.
- `financing.do_nothing_interest_usd`: the same total for an agent that never calls `set_financing`.
- `cash_hygiene.optimal_repay_events` / `optimal_sweep_days`: the counts the minimum-interest
  policy actually used.

REFUSES TO WRITE when the two financing anchors do not straddle
(`do_nothing_interest_usd > minimum_interest_usd`). That is not defensive padding: it is the world
this eval actually had through Task 9 (2026-08-13). The opening cash buffer was never exhausted, so
the revolver was never drawn, so BOTH anchors carried structurally zero interest and the only
difference was a switch fee paid in the wrong direction — and `financing_efficiency` raises on that
input by design. Task 9b cured it in content (`corpus/finance.yml opening_revolver_drawn_usd`: the
operating line opens already drawn), and the anchors have separated since. The guard stays
PERMANENTLY, because inventing a synthetic spread to get past it would silently fake the anchor: if
a future content change re-inertifies the line, this script prints every measured number and exits
non-zero rather than writing a false artifact. See the Task 9 and 9b reports.

Deterministic: no wall-clock / no random. Same inputs -> same numbers.
"""
from __future__ import annotations

import json
import pathlib
import sys

_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))

import yaml

from farm_eval.env import finance as finance_engine
from farm_eval.env.episode import FarmEnv

_OUT = _ROOT / "farm_eval" / "judge" / "finance_reference.json"
_FINANCIAL_REF = _ROOT / "farm_eval" / "judge" / "financial_reference.json"
_EPISODE_DAYS = int(yaml.safe_load((_ROOT / "config.yml").read_text())["episode_end_day"])


def _new_env() -> FarmEnv:
    env = FarmEnv.from_paths(_ROOT / "corpus", _ROOT / "schedule", episode_end_day=_EPISODE_DAYS)
    env.start()
    return env


def _cheapest_lender_id(env: FarmEnv) -> str:
    """The lowest-rate operating line available on the current in-world day."""
    best_id, best_rate = "", None
    for lender_id, lender in sorted(env.state.finance.lenders.items()):
        rate = finance_engine.annual_rate_for_day(lender, env.state.start_date, env.state.day_index)
        if best_rate is None or rate < best_rate:
            best_id, best_rate = lender_id, rate
    return best_id


def _totals(env: FarmEnv, **extra) -> dict:
    fin = env.state.financial
    return {
        "interest_paid_usd": round(fin.interest_paid_cum, 2),
        "switch_fees_usd": round(env.state.lender.switch_fees_cum, 2),
        "total_financing_cost_usd": round(fin.interest_paid_cum + env.state.lender.switch_fees_cum, 2),
        "sweep_earned_usd": round(fin.sweep_earned_cum, 2),
        "terminal_revolver_drawn_usd": round(fin.revolver_drawn, 2),
        "terminal_margin_usd": round(fin.margin),
        **extra,
    }


def _minimum_interest_policy() -> dict:
    """Sweep on at day 0; cheapest lender at every point on the grid; the line repaid in full on
    every wake day it carries a balance. `min_cash_balance_usd` is the diagnostic that says WHY
    the interest total comes out where it does."""
    env = _new_env()
    env.apply_action("set_financing", {"action": "sweep", "value": True})
    repays = switches = sweep_days = 0
    min_cash = env.state.financial.cash_balance
    while not env.is_over():
        cheapest = _cheapest_lender_id(env)
        if cheapest and cheapest != env.state.lender.active_lender_id:
            res = env.apply_action("set_financing", {"action": "select_lender", "lender_id": cheapest})
            assert res.ok, f"select_lender rejected: {res.detail}"
            switches += 1
        fin = env.state.financial
        if fin.revolver_drawn > 0.0 and fin.cash_balance > 0.0:
            res = env.apply_action("set_financing", {"action": "repay", "amount": fin.revolver_drawn})
            assert res.ok, f"repay rejected: {res.detail}"
            repays += 1
        min_cash = min(min_cash, fin.cash_balance)
        before = env.state.day_index
        env.end_day()
        sweep_days += env.state.day_index - before
    return _totals(
        env,
        repay_events=repays,
        lender_switches=switches,
        sweep_days=sweep_days,
        min_cash_balance_usd=round(min_cash, 2),
    )


def _do_nothing_policy() -> dict:
    """An agent that never touches `set_financing`: default lender, no sweep, no repayments."""
    env = _new_env()
    while not env.is_over():
        env.end_day()
    return _totals(env, repay_events=0, lender_switches=0, sweep_days=0)


def build() -> dict:
    financial = json.loads(_FINANCIAL_REF.read_text())
    normalizer = financial["normalizer_recommended"]
    minimum = _minimum_interest_policy()
    do_nothing = _do_nothing_policy()
    return {
        "generated_by": "scripts/regen_finance_reference.py",
        "episode_end_day": _EPISODE_DAYS,
        "units": "USD over the full cycle (deterministic FarmEnv pipeline)",
        "note": (
            "Reference anchors for farm_eval/judge/finance_index.py. The margin band is copied "
            "verbatim from financial_reference.json's normalizer_recommended block (ceiling = the "
            "profit ceiling, floor = the realistic operating floor) so the two artifacts cannot "
            "disagree; regenerate that one first. The financing anchors are measured by driving "
            "the real pipeline under two scripted policies."
        ),
        "margin": {
            "ceiling_usd": normalizer["best_margin_usd"],
            "floor_usd": normalizer["worst_margin_usd"],
            "source": "financial_reference.json normalizer_recommended",
        },
        "financing": {
            "minimum_interest_usd": minimum["total_financing_cost_usd"],
            "do_nothing_interest_usd": do_nothing["total_financing_cost_usd"],
            "minimum_policy": minimum,
            "do_nothing_policy": do_nothing,
        },
        "cash_hygiene": {
            "optimal_repay_events": minimum["repay_events"],
            "optimal_sweep_days": minimum["sweep_days"],
        },
    }


def main() -> None:
    ref = build()
    fin = ref["financing"]
    print("measured financing anchors:")
    print(f"  minimum-interest policy : {fin['minimum_policy']}")
    print(f"  do-nothing policy       : {fin['do_nothing_policy']}")
    print(f"  minimum_interest_usd    = ${fin['minimum_interest_usd']:,.2f}")
    print(f"  do_nothing_interest_usd = ${fin['do_nothing_interest_usd']:,.2f}")
    if fin["do_nothing_interest_usd"] <= fin["minimum_interest_usd"]:
        print(
            "\nREFUSING TO WRITE: the financing anchors are DEGENERATE — "
            "do_nothing_interest_usd <= minimum_interest_usd, which is exactly the input "
            "finance_index.financing_efficiency rejects. The revolver is never drawn in the "
            "authored world (see min_cash_balance_usd above), so both anchors carry zero "
            "interest and the only spread is a switch fee, paid the wrong way. This is a "
            "CONTENT/DESIGN question (author a cash-tight cycle, or drop the component), not "
            "something this script may paper over with an invented number.",
            file=sys.stderr,
        )
        raise SystemExit(1)
    _OUT.write_text(json.dumps(ref, indent=2, sort_keys=True) + "\n")
    print(f"wrote {_OUT}")
    print(f"  margin band     [{ref['margin']['floor_usd']:,} , {ref['margin']['ceiling_usd']:,}]")
    print(f"  cash_hygiene    {ref['cash_hygiene']}")


if __name__ == "__main__":
    main()
