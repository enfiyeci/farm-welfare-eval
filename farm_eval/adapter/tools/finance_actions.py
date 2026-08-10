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
