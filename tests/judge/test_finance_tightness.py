"""Task 9b: the standing pin against a re-inert credit line.

Task 9 measured the authored world's revolver as structurally dead — minimum cash across all 518
days was exactly the opening buffer, untouched, so no policy ever drew, interest was zero for
everyone, and the two financing anchors came out INVERTED (do-nothing $0 < minimum $2,500, the
switch fee being the only spread available). `finance_index.financing_efficiency` raises on that
input by design, and `scripts/regen_finance_reference.py` refuses to write the artifact at all.

The cure was content: `corpus/finance.yml opening_revolver_drawn_usd`. These assertions are what
makes a future content change that quietly removes or hollows out that opening balance fail HERE,
loudly, instead of silently returning the axis to measuring nothing.
"""
import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
ARTIFACT = REPO / "farm_eval" / "judge" / "finance_reference.json"


@pytest.fixture(scope="module")
def ref() -> dict:
    assert ARTIFACT.exists(), (
        f"{ARTIFACT} is missing. Regenerate it with scripts/regen_finance_reference.py — and if "
        "that script exits 1, the financing anchors are degenerate again (see its docstring)."
    )
    return json.loads(ARTIFACT.read_text())


def test_the_financing_anchors_straddle(ref):
    """The exact input `financing_efficiency` needs: doing nothing must cost MORE than the
    minimum-interest policy, or the component has no scale to normalize against."""
    financing = ref["financing"]
    assert financing["do_nothing_interest_usd"] > financing["minimum_interest_usd"]


def test_the_financing_spread_is_material(ref):
    """Not merely ordered — separated. The degenerate world's entire spread was one $2,500 switch
    fee, so a spread that fails to clear a switch fee is the degeneracy wearing a different hat."""
    financing = ref["financing"]
    spread = financing["do_nothing_interest_usd"] - financing["minimum_interest_usd"]
    assert spread > 2_500.0, f"financing spread collapsed to ${spread:,.2f}"


def test_repaying_the_line_is_a_real_move(ref):
    """`cash_hygiene` divides by `max(1, optimal_repay_events)`. At 0 the denominator is faked and
    a single no-op `repay` call on a zero balance earns the whole repay half of the component."""
    assert ref["cash_hygiene"]["optimal_repay_events"] >= 1


def test_the_anchors_were_measured_over_the_configured_horizon(ref):
    import yaml

    cfg_days = int(yaml.safe_load((REPO / "config.yml").read_text())["episode_end_day"])
    assert ref["episode_end_day"] == cfg_days
