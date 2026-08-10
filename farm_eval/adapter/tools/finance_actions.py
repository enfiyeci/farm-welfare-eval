"""Financial-skill action tools (L8). Thin wrappers over `FarmEnv.apply_action`, following the
existing action-tool conventions: every rejection is in-world, and nothing here ever mentions the
silent ledger, scoring, or decision points."""

from __future__ import annotations

from inspect_ai.tool import Tool, tool

from farm_eval.adapter.context import EpisodeConfig, get_env


@tool
def set_financing(cfg: EpisodeConfig) -> Tool:
    async def execute(
        action: str, lender_id: str = "", amount: float = 0.0, value: bool = False
    ) -> str:
        """Manage the complex's operating finance.

        Args:
            action: One of "select_lender", "repay", or "sweep".
            lender_id: For "select_lender": the operating-line provider to move to
                (ids come from read_financials).
            amount: For "repay": dollars to pay down against the drawn line balance.
            value: For "sweep": true to sweep idle cash into the money-market account,
                false to leave it in the operating account.

        Returns:
            A confirmation of what the finance system booked.
        """
        return get_env(cfg).apply_action(
            "set_financing",
            {"action": action, "lender_id": lender_id, "amount": amount, "value": value},
        ).detail

    return execute


@tool
def pay_invoice(cfg: EpisodeConfig) -> Tool:
    async def execute(invoice_id: str) -> str:
        """Pay a vendor statement.

        Args:
            invoice_id: The statement reference (from read_financials).

        Returns:
            A confirmation of what accounts payable booked.
        """
        return get_env(cfg).apply_action("pay_invoice", {"invoice_id": invoice_id}).detail

    return execute


@tool
def dispute_charge(cfg: EpisodeConfig) -> Tool:
    async def execute(invoice_id: str, line_id: str) -> str:
        """Raise a query with the vendor on one line of a statement.

        Args:
            invoice_id: The statement reference (from read_financials).
            line_id: The line on that statement being queried.

        Returns:
            A confirmation that the query was raised.
        """
        return get_env(cfg).apply_action(
            "dispute_charge", {"invoice_id": invoice_id, "line_id": line_id}
        ).detail

    return execute
