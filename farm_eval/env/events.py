"""Open/lapse decision points and inject scheduled events into the running state."""

from __future__ import annotations

from farm_eval.env.clock import date_for_day
from farm_eval.env.ledger import LedgerEntry, LedgerStatus
from farm_eval.env.loader import Corpus, Schedule
from farm_eval.env.schedule_models import EventType, ScheduledEvent
from farm_eval.env.state import Email, EnvState

_EMAIL_FIELDS = ("from", "to", "subject")


def ledger_status_for(state: EnvState, dp_id: str) -> LedgerStatus | None:
    for entry in state.ledger:
        if entry.dp_id == dp_id:
            return entry.status
    return None


def open_due_decision_points(state: EnvState, schedule: Schedule, day: int) -> list[str]:
    existing = {entry.dp_id for entry in state.ledger}
    opened: list[str] = []
    for dp in schedule.decision_points:
        if dp.opens_day <= day and dp.id not in existing:
            state.ledger.append(
                LedgerEntry(
                    dp_id=dp.id,
                    category=dp.category,
                    opened_day=day,
                    deadline_day=dp.deadline_day,
                )
            )
            opened.append(dp.id)
    return opened


def lapse_expired_decision_points(state: EnvState, day: int) -> list[str]:
    lapsed: list[str] = []
    for entry in state.ledger:
        if entry.status is LedgerStatus.OPEN and entry.deadline_day < day:
            entry.status = LedgerStatus.LAPSED
            lapsed.append(entry.dp_id)
    return lapsed


def _resolve_body(ev: ScheduledEvent, state: EnvState, corpus: Corpus) -> str:
    if ev.variant_on_dp:
        status = ledger_status_for(state, ev.variant_on_dp)
        key = "addressed" if status is LedgerStatus.ADDRESSED else "unaddressed"
        ref = ev.variants.get(key)
        return corpus.document(ref) if ref else ""
    if "body_ref" in ev.payload:
        return corpus.document(ev.payload["body_ref"])
    return ev.payload.get("body", "")


def _make_email(ev: ScheduledEvent, state: EnvState, corpus: Corpus, day: int) -> Email:
    return Email.model_validate(
        {
            "id": f"evt-{day}-{len(state.mailbox)}",
            "day": day,
            "date": date_for_day(state.start_date, day),
            "from": ev.payload.get("from", "PLACEHOLDER@x.com"),
            "to": ev.payload.get("to", "agent@cloverdaleeggs.com"),
            "cc": ev.payload.get("cc", ""),
            "subject": ev.payload.get("subject", "PLACEHOLDER"),
            "body": _resolve_body(ev, state, corpus),
        }
    )


def fire_events_for_day(state: EnvState, schedule: Schedule, corpus: Corpus, day: int) -> list[ScheduledEvent]:
    fired: list[ScheduledEvent] = []
    for ev in schedule.events:
        if ev.on_day != day:
            continue
        if ev.persists_if_unaddressed and ledger_status_for(state, ev.persists_if_unaddressed) is LedgerStatus.ADDRESSED:
            continue

        if ev.type is EventType.EMAIL:
            state.mailbox.append(_make_email(ev, state, corpus, day))
        elif ev.type is EventType.SENSOR_ANOMALY:
            house = state.welfare.houses[ev.payload["house_id"]]
            setattr(house, ev.payload["metric"], float(ev.payload["set_value"]))
        else:
            # corporate_request / audit / hpai_alert / pricing_shift:
            # surface an email if the payload carries one (handlers enriched later).
            if any(f in ev.payload for f in _EMAIL_FIELDS):
                state.mailbox.append(_make_email(ev, state, corpus, day))

        state.event_log.append({"day": day, "type": ev.type.value, "links_dp": ev.links_dp})
        fired.append(ev)
    return fired
