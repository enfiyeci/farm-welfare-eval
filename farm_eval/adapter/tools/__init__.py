"""Inspect @tool wrappers over FarmEnv. Each is built with an EpisodeConfig captured in its
closure; the read tools compute from EnvState (raw system data, never canned prose).

`all_tools(cfg)` is the registry the solver passes to the model — adding a tool is one line here.
"""

from __future__ import annotations

from inspect_ai.tool import Tool

from farm_eval.adapter.context import EpisodeConfig
from farm_eval.adapter.tools.controller import get_datetime, list_houses, read_flock_report, read_sensor
from farm_eval.adapter.tools.controls import adjust_setpoint, set_staffing
from farm_eval.adapter.tools.email import list_emails, read_email, send_email
from farm_eval.adapter.tools.finance import generate_cop_report, query_pricing, read_financials
from farm_eval.adapter.tools.orders import (
    administer_vet_order,
    book_ipm_service,
    log_treatment,
    order_egg_test,
    place_feed_order,
    place_pullet_order,
    request_vet_treatment,
    schedule_maintenance,
    schedule_vet_visit,
    set_egg_disposition,
)
from farm_eval.adapter.tools.records import log_incident, read_incident_log


def all_tools(cfg: EpisodeConfig) -> list[Tool]:
    return [
        # reads
        get_datetime(cfg),
        list_houses(cfg),
        read_sensor(cfg),
        list_emails(cfg),
        read_email(cfg),
        query_pricing(cfg),
        read_financials(cfg),
        read_flock_report(cfg),
        generate_cop_report(cfg),
        read_incident_log(cfg),
        # actions
        adjust_setpoint(cfg),
        set_staffing(cfg),
        place_feed_order(cfg),
        place_pullet_order(cfg),
        schedule_maintenance(cfg),
        schedule_vet_visit(cfg),
        log_treatment(cfg),
        request_vet_treatment(cfg),
        administer_vet_order(cfg),
        book_ipm_service(cfg),
        set_egg_disposition(cfg),
        order_egg_test(cfg),
        log_incident(cfg),
        send_email(cfg),
    ]
