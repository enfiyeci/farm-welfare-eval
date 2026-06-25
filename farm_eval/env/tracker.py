"""Silent decision capture: match agent tool calls against open decision-point signatures.

This is harness-side only. The agent never sees the ledger or any matching machinery.
"""

from __future__ import annotations

from farm_eval.env.ledger import ActionRecord, LedgerStatus
from farm_eval.env.loader import Schedule
from farm_eval.env.schedule_models import Signature
from farm_eval.env.state import EnvState


def match_where(params: dict, where: dict) -> bool:
    return all(key in params and params[key] == value for key, value in where.items())


def match_signature(signature: Signature, tool: str, params: dict) -> bool:
    return any(match_where(params, am.where) for am in signature.any_of if am.tool == tool)


def _dp_index(schedule: Schedule) -> dict[str, object]:
    return {dp.id: dp for dp in schedule.decision_points}


def record_tool_call(state: EnvState, schedule: Schedule, tool: str, params: dict, day: int) -> list[str]:
    dps = _dp_index(schedule)
    addressed: list[str] = []
    for entry in state.ledger:
        if entry.status is not LedgerStatus.OPEN:
            continue
        dp = dps.get(entry.dp_id)
        if dp is None or not match_signature(dp.signature, tool, params):
            continue
        entry.status = LedgerStatus.ADDRESSED
        entry.agent_action = ActionRecord(tool=tool, params=dict(params), day=day)
        entry.noticed_unprompted = not dp.prompted
        addressed.append(entry.dp_id)
    return addressed
