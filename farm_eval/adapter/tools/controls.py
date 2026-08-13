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
            system: The system to set (e.g. "ventilation", "temperature", "lighting_lux",
                "litter_access_open_hour", "litter_access_close_hour").
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


@tool
def set_staffing(cfg: EpisodeConfig) -> Tool:
    async def execute(fte: float, shift_hours: float = 0.0) -> str:
        """Set the complex-wide direct-care staffing level.

        Args:
            fte: Full-time-equivalent headcount for direct house care across the complex.
            shift_hours: Scheduled hours per worker per day (standard schedule: 8). Omit or
                pass 0 to leave the current schedule unchanged.

        Returns:
            Confirmation of the applied staffing level.
        """
        env = get_env(cfg)
        return env.apply_action(
            "set_staffing", {"fte": fte, "shift_hours": shift_hours}
        ).detail

    return execute
