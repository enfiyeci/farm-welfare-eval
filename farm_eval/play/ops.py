"""The play op registry: the model's exact tool surface, Inspect-free (spec §4).

Each op mirrors its adapter tool (farm_eval/adapter/tools/) byte-for-byte: same parameter
names/defaults, same string returns. The adapter is the frozen agent-facing layer and is NOT
refactored to delegate here; tests/play/test_ops.py pins the two surfaces to each other so
drift in either direction fails loudly.
"""

from __future__ import annotations

import json
from typing import Literal

from pydantic import BaseModel, ConfigDict

from farm_eval.env.episode import FarmEnv


class ParamSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: Literal["str", "float", "bool"]
    default: str | float | bool | None = None  # None = required (no default)


class OpSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: Literal["read", "action", "end_day"]
    params: dict[str, ParamSpec]


def _p(type_: str, default=None) -> ParamSpec:
    return ParamSpec(type=type_, default=default)


OPS: dict[str, OpSpec] = {
    # reads — order mirrors all_tools()
    "get_datetime": OpSpec(kind="read", params={}),
    "list_houses": OpSpec(kind="read", params={}),
    "read_sensor": OpSpec(kind="read", params={"house_id": _p("str"), "metric": _p("str")}),
    "list_emails": OpSpec(kind="read", params={"unread_only": _p("bool", False)}),
    "read_email": OpSpec(kind="read", params={"email_id": _p("str")}),
    "query_pricing": OpSpec(kind="read", params={}),
    "read_financials": OpSpec(kind="read", params={}),
    "read_flock_report": OpSpec(kind="read", params={"house_id": _p("str"), "date_range": _p("str", "")}),
    "generate_cop_report": OpSpec(kind="read", params={"house_id": _p("str", ""), "period": _p("str", "")}),
    # actions
    "adjust_setpoint": OpSpec(kind="action", params={"house_id": _p("str"), "system": _p("str"), "value": _p("float")}),
    "set_staffing": OpSpec(kind="action", params={"fte": _p("float"), "shift_hours": _p("float", 0.0)}),
    "place_feed_order": OpSpec(kind="action", params={
        "ration": _p("str", ""), "quantity_tons": _p("float", 0.0), "house_id": _p("str", ""),
        "additive": _p("str", ""), "target": _p("str", ""), "genetics": _p("str", ""),
    }),
    "schedule_maintenance": OpSpec(kind="action", params={
        "task": _p("str"), "house_id": _p("str", ""), "target": _p("str", ""), "method": _p("str", ""),
    }),
    "schedule_vet_visit": OpSpec(kind="action", params={"house_id": _p("str"), "reason": _p("str", "")}),
    "log_treatment": OpSpec(kind="action", params={"issue": _p("str"), "house_id": _p("str", "")}),
    "set_egg_disposition": OpSpec(kind="action", params={
        "house_id": _p("str"), "channel": _p("str"), "reason": _p("str", ""),
    }),
    "send_email": OpSpec(kind="action", params={
        "to": _p("str"), "subject": _p("str"), "body": _p("str"),
        "cc": _p("str", ""), "in_reply_to": _p("str", ""),
    }),
    # loop mechanics — executed by PlaySession.end_day(), never by run_op
    "end_day": OpSpec(kind="end_day", params={"notes": _p("str", "")}),
}


def _drop_empty(**kwargs) -> dict:
    """Mirror of farm_eval/adapter/tools/orders.py:_params — empty optionals must not
    spuriously satisfy a decision signature's where-clause."""
    return {k: v for k, v in kwargs.items() if v is not None and v != ""}


def run_op(env: FarmEnv, name: str, params: dict) -> str:
    """Execute one op exactly as the adapter tool would, returning the same string."""
    if name not in OPS:
        raise KeyError(f"unknown op: {name!r}")
    if OPS[name].kind == "end_day":
        raise ValueError("end_day is executed by PlaySession.end_day(), not run_op()")
    p = params
    if name == "get_datetime":
        return f"day {env.current_day()} | {env.current_date()}"
    if name == "list_houses":
        return json.dumps(env.list_houses())
    if name == "read_sensor":
        result = env.get_sensor(p["house_id"], p["metric"])
        if not result.available:
            return result.message
        return json.dumps({"house_id": p["house_id"], "metric": p["metric"], "value": result.value})
    if name == "list_emails":
        return json.dumps(env.list_emails(unread_only=bool(p.get("unread_only", False))))
    if name == "read_email":
        try:
            return json.dumps(env.read_email(p["email_id"]))
        except KeyError:
            return f"No email with id {p['email_id']!r}."
    if name == "query_pricing":
        return json.dumps(env.query_pricing())
    if name == "read_financials":
        return json.dumps(env.read_financials())
    if name == "read_flock_report":
        return json.dumps(env.read_flock_report(p["house_id"], p.get("date_range") or None))
    if name == "generate_cop_report":
        return json.dumps(env.generate_cop_report(p.get("house_id", ""), p.get("period", "")))
    if name == "adjust_setpoint":
        return env.apply_action(
            "adjust_setpoint",
            {"house_id": p["house_id"], "system": p["system"], "value": p["value"]},
        ).detail
    if name == "set_staffing":
        return env.apply_action(
            "set_staffing", {"fte": p["fte"], "shift_hours": p.get("shift_hours", 0.0)}
        ).detail
    if name == "place_feed_order":
        return env.apply_action("place_feed_order", _drop_empty(
            ration=p.get("ration", ""), quantity_tons=p.get("quantity_tons", 0.0) or None,
            house_id=p.get("house_id", ""), additive=p.get("additive", ""),
            target=p.get("target", ""), genetics=p.get("genetics", ""),
        )).detail
    if name == "schedule_maintenance":
        return env.apply_action("schedule_maintenance", _drop_empty(
            task=p["task"], house_id=p.get("house_id", ""),
            target=p.get("target", ""), method=p.get("method", ""),
        )).detail
    if name == "schedule_vet_visit":
        return env.apply_action(
            "schedule_vet_visit", _drop_empty(house_id=p["house_id"], reason=p.get("reason", ""))
        ).detail
    if name == "log_treatment":
        return env.apply_action(
            "log_treatment", _drop_empty(issue=p["issue"], house_id=p.get("house_id", ""))
        ).detail
    if name == "set_egg_disposition":
        # Literal params (NOT _drop_empty): the recorded {house_id, channel, reason} shape is a
        # fixed contract action matchers key on (see adapter/tools/orders.py).
        return env.apply_action("set_egg_disposition", {
            "house_id": p["house_id"], "channel": p["channel"], "reason": p.get("reason", ""),
        }).detail
    if name == "send_email":
        return env.apply_action("send_email", {
            "to": p["to"], "subject": p["subject"], "body": p["body"],
            "cc": p.get("cc", ""), "in_reply_to": p.get("in_reply_to", "") or None,
        }).detail
    raise KeyError(f"unhandled op: {name!r}")  # unreachable: every OPS entry is handled above
