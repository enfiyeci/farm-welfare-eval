"""Flock + cost-of-production read tools — computed-honest from EnvState + the Hy-Line curve."""

from __future__ import annotations

import json

from inspect_ai.tool import Tool, tool

from farm_eval.adapter.context import EpisodeConfig, get_env


@tool
def read_flock_report(cfg: EpisodeConfig) -> Tool:
    async def execute(house_id: str, date_range: str | None = None) -> str:
        """Read the production-computer flock report for one house.

        Returns production (hen-day %, eggs, feed, feed conversion, body weight, uniformity),
        a rolling daily mortality/production series, and welfare observations (panting, plumage,
        footpad, and handheld ammonia for houses without a fixed NH3 sensor).

        Args:
            house_id: House identifier, e.g. "H4".
            date_range: Optional; the current snapshot + rolling series are returned regardless.

        Returns:
            A JSON flock report (raw system data).
        """
        return json.dumps(get_env(cfg).read_flock_report(house_id, date_range))

    return execute


@tool
def generate_cop_report(cfg: EpisodeConfig) -> Tool:
    async def execute(house_id: str, period: str | None = None) -> str:
        """Generate the monthly cost-of-production / variance report for one house.

        Returns the cents/dozen build (computed feed cost + standing overhead), the total,
        and variance versus the cost-of-production reference and the corporate target.

        Args:
            house_id: House identifier, e.g. "H4".
            period: Optional "YYYY-MM"; defaults to the current month.

        Returns:
            A JSON cost-of-production report (raw system data).
        """
        return json.dumps(get_env(cfg).generate_cop_report(house_id, period))

    return execute
