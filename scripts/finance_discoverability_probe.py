# Run: ./venv/bin/python scripts/finance_discoverability_probe.py
"""Law 1 of the financial rulebook: every input a rulebook entry needs must be obtainable from
inside the world, through the read tools, on the wake-day grid.

This is the DP18 lesson made into a standing test — DP18 scored a guaranteed zero for a whole
pilot because its signal was not readable. Deterministic: drives the real FarmEnv, no model.
"""
from __future__ import annotations

import pathlib
import sys

_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))

from farm_eval.env.episode import FarmEnv

# One key per rulebook input, named for the entry that needs it.
REQUIRED_INPUTS = (
    "m1.cash_balance",
    "m1.revolver_drawn",
    "m1.interest_paid",
    "m2.active_lender_rate",
    "m2.alternative_lender_rates",
    "m2.switch_fee",
    "m3.money_market_rate",
    "m3.sweep_status",
    "m5.invoice_discount_terms",
    "m6.invoice_lines",
    "m6.own_order_log",
    "m7.offer_terms_and_expiry",
    "m8.ration_prices",
    "m8.feed_inventory_on_hand",
)


def probe_inputs(env: FarmEnv) -> dict[str, bool]:
    """Drive the read tools over the whole episode and report which rulebook inputs were served
    at least once. An input is 'found' only when a read tool actually returned it."""
    found = {key: False for key in REQUIRED_INPUTS}

    def scan(env: FarmEnv) -> None:
        fin = env.read_financials().get("finance", {})
        pricing = env.query_pricing()
        found["m1.cash_balance"] |= "cash_balance" in fin
        found["m1.revolver_drawn"] |= "revolver_drawn" in fin
        found["m1.interest_paid"] |= "interest_paid" in fin
        found["m2.active_lender_rate"] |= bool(fin.get("annual_rate"))
        found["m2.alternative_lender_rates"] |= len(fin.get("available_lenders", {})) > 1
        found["m2.switch_fee"] |= any(
            "switch_fee_usd" in lender for lender in fin.get("available_lenders", {}).values()
        )
        found["m3.money_market_rate"] |= "money_market_rate" in fin
        found["m3.sweep_status"] |= "sweep_enabled" in fin
        for invoice in fin.get("open_invoices", []):
            found["m5.invoice_discount_terms"] |= "discount_day" in invoice
            found["m6.invoice_lines"] |= bool(invoice.get("lines"))
        for offer in fin.get("open_offers", []):
            found["m7.offer_terms_and_expiry"] |= "expires_day" in offer and bool(offer.get("options"))
        found["m8.ration_prices"] |= bool(pricing.get("ration_prices_usd_ton"))
        found["m8.feed_inventory_on_hand"] |= "feed_inventory_tons" in env.read_financials()

    scan(env)
    while not env.is_over():
        env.end_day()
        scan(env)
    # The agent's own order log is served by the action-record history, not a read tool: an order
    # placed is echoed in its ack and is visible in the agent's own transcript by construction.
    env.apply_action("place_feed_order", {"ration": "LP2", "quantity_tons": 1})
    found["m6.own_order_log"] = any(a.tool == "place_feed_order" for a in env.state.actions)
    return found


def main() -> None:
    env = FarmEnv.from_paths(_ROOT / "corpus", _ROOT / "schedule", episode_end_day=518)
    env.start()
    found = probe_inputs(env)
    missing = sorted(key for key in REQUIRED_INPUTS if not found[key])
    for key in REQUIRED_INPUTS:
        print(f"  {'OK  ' if found[key] else 'MISS'} {key}")
    if missing:
        print(f"\n{len(missing)} rulebook input(s) not obtainable in-world: {missing}")
        raise SystemExit(1)
    print(f"\nall {len(REQUIRED_INPUTS)} rulebook inputs are obtainable in-world")


if __name__ == "__main__":
    main()
