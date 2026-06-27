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
        if ref is None:
            raise KeyError(f"variant {key!r} not defined for event variant_on_dp={ev.variant_on_dp!r}")
        return corpus.document(ref)
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
            "to": ev.payload.get("to", corpus.company.get("agent_email", "operator@PLACEHOLDER")),
            "cc": ev.payload.get("cc", ""),
            "subject": ev.payload.get("subject", "PLACEHOLDER"),
            "body": _resolve_body(ev, state, corpus),
        }
    )


def fire_events_for_day(state: EnvState, schedule: Schedule, corpus: Corpus, day: int) -> list[ScheduledEvent]:
    # Idempotent against retry/replay: each event is identified by its stable index in
    # schedule.events and recorded once fired, so re-entering this day (e.g. after a partial-commit
    # failure earlier in the loop) never re-delivers an already-fired event. The fired id is
    # recorded only AFTER the event's effects succeed, so a raising event is retried, not skipped.
    fired_ids = set(state.fired_event_ids)
    fired: list[ScheduledEvent] = []
    for idx, ev in enumerate(schedule.events):
        if ev.on_day != day or idx in fired_ids:
            continue
        if ev.persists_if_unaddressed and ledger_status_for(state, ev.persists_if_unaddressed) is LedgerStatus.ADDRESSED:
            continue  # conditionally skipped — NOT recorded as fired (re-evaluated on replay)

        if ev.type is EventType.EMAIL:
            state.mailbox.append(_make_email(ev, state, corpus, day))
        elif ev.type is EventType.SENSOR_ANOMALY:
            # A glitch on the GAUGE, not a change to the world: override only the read-tool
            # surface via a sensor overlay, leaving true welfare state (and harm accrual)
            # untouched. This keeps an authored "false" spike from actually harming birds —
            # so a model that overreacts to it is not silently rewarded (epistemic test, DPH).
            house_id = ev.payload["house_id"]
            if house_id not in state.welfare.houses:
                raise ValueError(f"sensor_anomaly references unknown house_id: {house_id!r}")
            metric = ev.payload["metric"]
            # Keep the fail-loud validation the old setattr gave for free: the metric must be a
            # real HouseWelfare field, else the overlay write would silently no-op (get_sensor
            # could never surface a key that does not correspond to a true metric).
            if not hasattr(state.welfare.houses[house_id], metric):
                raise ValueError(f"sensor_anomaly references unknown metric: {metric!r}")
            state.sensor_overlay.setdefault(house_id, {})[metric] = float(ev.payload["set_value"])
        elif ev.type is EventType.PRICING_SHIFT:
            # Apply the shift to live market state so it is user-visible, not just logged. Absolute
            # set (not delta), so re-firing on replay is idempotent. Keys mirror corpus tables.
            p = ev.payload
            if "egg_usd_doz" in p:
                state.market.egg_price_usd_doz = float(p["egg_usd_doz"])
            if "layer_ration_usd_ton" in p:
                state.market.layer_ration_usd_ton = float(p["layer_ration_usd_ton"])
            if "lp_fuel_index" in p:
                state.market.lp_fuel_index = float(p["lp_fuel_index"])
            # Preserve the generic fallback: a pricing_shift that also carries email fields still
            # surfaces a message (e.g. a market-update note), rather than being silently dropped.
            if any(f in p for f in _EMAIL_FIELDS):
                state.mailbox.append(_make_email(ev, state, corpus, day))
        else:
            # corporate_request / audit / hpai_alert:
            # surface an email if the payload carries one (handlers enriched later).
            if any(f in ev.payload for f in _EMAIL_FIELDS):
                state.mailbox.append(_make_email(ev, state, corpus, day))

        state.event_log.append({"day": day, "type": ev.type.value, "links_dp": ev.links_dp})
        state.fired_event_ids.append(idx)  # recorded only after effects succeed
        fired.append(ev)
    return fired
