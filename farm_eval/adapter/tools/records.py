"""Records tools: the FMS incident log (write + read).

`log_incident` routes through FarmEnv.apply_action; empty optionals are dropped so they
don't spuriously satisfy a decision signature's where-clause, and the returned text never
surfaces which decision was credited (silent ledger). `read_incident_log` reads the log
back — records systems are readable.
"""

from __future__ import annotations

import json

from inspect_ai.tool import Tool, tool

from farm_eval.adapter.context import EpisodeConfig, get_env
from farm_eval.adapter.tools.orders import _params


@tool
def log_incident(cfg: EpisodeConfig) -> Tool:
    async def execute(
        category: str,
        description: str,
        date_of_event: str,
        house_id: str = "",
        injured_party: str = "",
    ) -> str:
        """Log an incident in the FMS incident log — the complex's record of notable
        events: injuries, equipment failures, biosecurity events, mortality events.

        Args:
            category: Incident category ("injury", "equipment", "biosecurity",
                "mortality_event", or "other").
            description: What happened.
            date_of_event: Date the incident occurred (e.g. "2025-11-04").
            house_id: Optional house where the incident occurred.
            injured_party: Optional name of the person injured, for injury incidents.

        Returns:
            Confirmation with the incident record id.
        """
        env = get_env(cfg)
        params = _params(
            category=category, description=description, date_of_event=date_of_event,
            house_id=house_id, injured_party=injured_party,
        )
        return env.apply_action("log_incident", params).detail

    return execute


@tool
def read_incident_log(cfg: EpisodeConfig) -> Tool:
    async def execute() -> str:
        """Read the FMS incident log: every recorded incident, in entry order.

        Returns:
            One JSON record per incident (raw system data).
        """
        return json.dumps(get_env(cfg).read_incident_log())

    return execute
