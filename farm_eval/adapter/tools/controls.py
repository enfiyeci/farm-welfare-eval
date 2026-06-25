"""Control action tools: setpoint changes routed through FarmEnv.apply_action."""

from __future__ import annotations

from inspect_ai.tool import Tool, tool

from farm_eval.adapter.context import EpisodeConfig, get_env


@tool
def adjust_setpoint(cfg: EpisodeConfig) -> Tool:
    async def execute(house_id: str, system: str, value: float) -> str:
        """Adjust an environmental setpoint for a house.

        Args:
            house_id: The house to adjust (e.g. "H4").
            system: The system to set (e.g. "ventilation", "temperature", "lighting_lux").
            value: The new setpoint value.

        Returns:
            Confirmation of the applied setpoint.
        """
        env = get_env(cfg)
        # apply_action returns addressed decision ids too; never surface them (silent ledger).
        return env.apply_action(
            "adjust_setpoint", {"house_id": house_id, "system": system, "value": value}
        ).detail

    return execute
