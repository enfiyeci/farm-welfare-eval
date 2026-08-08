"""Open/lapse decision points and inject scheduled events into the running state."""

from __future__ import annotations

from farm_eval.env.audit import capture_audit_snapshot, compose_audit_findings
from farm_eval.env.clock import date_for_day
from farm_eval.env.ledger import LedgerEntry, LedgerStatus
from farm_eval.env.loader import Corpus, Schedule
from farm_eval.env.model.params import ModelParams
from farm_eval.env.schedule_models import EventType, ScheduledEvent
from farm_eval.env.state import Email, EnvState

_EMAIL_FIELDS = ("from", "to", "subject")


def ledger_status_for(state: EnvState, dp_id: str) -> LedgerStatus | None:
    for entry in state.ledger:
        if entry.dp_id == dp_id:
            return entry.status
    return None


def open_due_decision_points(
    state: EnvState,
    schedule: Schedule,
    day: int,
    enabled_nodes: frozenset[str] | None = None,
) -> list[str]:
    existing = {entry.dp_id for entry in state.ledger}
    opened: list[str] = []
    for dp in schedule.decision_points:
        # `enabled_nodes` (when set) restricts seeding to the named subset: a disabled node is
        # never seeded, so it is absent from scores/breakouts/coverage automatically. `None` (the
        # default) = all nodes enabled (unchanged behavior).
        if enabled_nodes is not None and dp.id not in enabled_nodes:
            continue
        if dp.opens_day <= day and dp.id not in existing:
            state.ledger.append(
                LedgerEntry(
                    dp_id=dp.id,
                    category=dp.category,
                    opened_day=day,
                    deadline_day=dp.deadline_day,
                    stakeholder=list(dp.stakeholder),
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
    if ev.payload.get("composer") == "audit_findings":
        return compose_audit_findings(state, corpus)
    if ev.variant_on_dp:
        status = ledger_status_for(state, ev.variant_on_dp)
        key = "addressed" if status is LedgerStatus.ADDRESSED else "unaddressed"
        ref = ev.variants.get(key)
        if ref is None:
            raise KeyError(f"variant {key!r} not defined for event variant_on_dp={ev.variant_on_dp!r}")
        return corpus.document(ref)
    if "body_ref" in ev.payload:
        # Tolerate a not-yet-authored body: bodies are written in the C7 corpus pass, but the
        # schedule references them before then, so a missing body_ref surfaces a visible
        # placeholder rather than crashing a live episode. (A missing VARIANT above still fails
        # loud — that is an author error, not a deferred-content placeholder.)
        ref = ev.payload["body_ref"]
        if ref not in corpus.documents:
            return f"[PLACEHOLDER body not yet authored: {ref}]"
        return corpus.documents[ref]
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
            # Raw value: pydantic parses conventional booleans ("false"/0) correctly and fails
            # loud on nonsense — a premature bool() would silently invert quoted YAML "false".
            "unread": ev.payload.get("unread", True),
        }
    )


def _apply_authorized_confinement(
    state: EnvState, ev: ScheduledEvent, params: ModelParams
) -> None:
    """Record a scheduled litter-access closure, and re-bed the house if it was a cleanout.

    Payload: `{house_id, start_day, end_day, reason}`. The window is appended to
    `state.world.authorized_confinement[house_id]` as an inclusive `(start_day, end_day)`
    pair, which exempts its days from the house's confinement ledger (the recorded exception
    UEP 2024 p. 24 allows for). `reason: litter_cleanout` additionally strips the bed:
    `litter_depth_cm` back to fresh bedding and the litter clock back to zero.

    TIMING — the one thing an author can get wrong here, so both halves of it fail loudly.
    Events fire AFTER the beat's days have been integrated (`episode.end_day`), so an event's
    effects reach the world only from the day after it fires. That cuts two ways:

      * a `litter_cleanout` must fire ON its `end_day`. The bed reset lands at fire time, so
        that is the only authoring under which "reset at the window's end day" is true; any
        other day would silently re-bed the house early. Its window is therefore a
        RETROACTIVE record of a closure the world already carried out.
      * every OTHER reason must fire strictly BEFORE `start_day`. Such a window exists to
        exempt its own days — that is the whole point of it — and a window appended on or
        after the day it opens exempts nothing that has already been integrated, while
        looking perfectly correct in the schedule.
    """
    house_id = ev.payload["house_id"]
    house = state.welfare.houses.get(house_id)
    if house is None:
        raise ValueError(f"authorized_confinement references unknown house_id: {house_id!r}")
    start_day = int(ev.payload["start_day"])
    end_day = int(ev.payload["end_day"])
    if end_day < start_day:
        raise ValueError(
            f"authorized_confinement window ends before it starts: {start_day}..{end_day}"
        )
    reason = str(ev.payload.get("reason", ""))
    if reason == "litter_cleanout":
        if ev.on_day != end_day:
            raise ValueError(
                f"litter_cleanout must be authored on its end_day (on_day={ev.on_day}, "
                f"end_day={end_day}): the bed reset is applied when the event fires"
            )
    elif ev.on_day >= start_day:
        raise ValueError(
            f"authorized_confinement (reason={reason!r}) must be authored BEFORE its window "
            f"opens (on_day={ev.on_day}, start_day={start_day}): events fire after the beat's "
            "days have been integrated, so a window only exempts days integrated after it "
            "fires — authored inside its own window it would silently exempt nothing. A "
            "litter_cleanout is the deliberate exception: its window is a retroactive record "
            "and it fires on its end_day"
        )
    windows = state.world.authorized_confinement.setdefault(house_id, [])
    window = (start_day, end_day)
    if window not in windows:
        windows.append(window)
    if reason == "litter_cleanout":
        house.litter_depth_cm = params.litter_bedding_depth_cm
        state.world.litter_age_days[house_id] = 0.0


def fire_events_in_window(
    state: EnvState,
    schedule: Schedule,
    corpus: Corpus,
    after_day: int | None,
    through_day: int,
    params: ModelParams | None = None,
) -> list[ScheduledEvent]:
    """Fire every unfired event with after_day < on_day <= through_day.

    `after_day=None` = unbounded past (episode start: pre-day-0 backlog fires then). Emails
    are dated by their own on_day, so `no_wake` mail scheduled inside a skip arrives as
    backlog with the date it was "sent". Idempotency is unchanged: events are identified by
    their stable index in schedule.events and recorded in fired_event_ids only after their
    effects succeed.

    `params` is the run's `ModelParams` (the same object `integrate` gets), needed by the
    `authorized_confinement` handler for the fresh-bedding depth; it defaults to the shipped
    values so the many callers that fire nothing but mail need not thread it.
    """
    if params is None:
        params = ModelParams()
    fired_ids = set(state.fired_event_ids)
    fired: list[ScheduledEvent] = []
    for idx, ev in enumerate(schedule.events):
        if ev.on_day > through_day or (after_day is not None and ev.on_day <= after_day):
            continue
        if idx in fired_ids:
            continue
        if ev.persists_if_unaddressed and ledger_status_for(state, ev.persists_if_unaddressed) is LedgerStatus.ADDRESSED:
            continue  # conditionally skipped — NOT recorded as fired (re-evaluated on replay)

        if ev.type is EventType.EMAIL:
            state.mailbox.append(_make_email(ev, state, corpus, ev.on_day))
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
            # real HouseWelfare DATA field, else the overlay write would silently no-op (get_sensor
            # could never surface a key that does not correspond to a true metric). Whitelist to
            # declared model fields (NOT hasattr, which would also accept methods / dunders like
            # model_dump and let a malformed event write a bogus overlay) — mirrors STATE_SEED.
            if metric not in type(state.welfare.houses[house_id]).model_fields:
                raise ValueError(f"sensor_anomaly references unknown metric: {metric!r}")
            state.sensor_overlay.setdefault(house_id, {})[metric] = float(ev.payload["set_value"])
        elif ev.type is EventType.STATE_SEED:
            house = state.welfare.houses.get(ev.payload["house_id"])
            if house is None:
                raise ValueError(f"state_seed references unknown house_id: {ev.payload['house_id']!r}")
            field = ev.payload["field"]
            # Whitelist to declared HouseWelfare data fields (NOT hasattr, which would also
            # accept methods / dunders / model_config and let a malformed event setattr them).
            if field not in type(house).model_fields:
                raise ValueError(f"state_seed references unknown HouseWelfare field: {field!r}")
            setattr(house, field, ev.payload["value"])
        elif ev.type is EventType.AUTHORIZED_CONFINEMENT:
            _apply_authorized_confinement(state, ev, params)
            # Same generic fallback the pricing_shift branch keeps: a confinement event that
            # also carries email fields (the maintenance note that is the closure's in-world
            # face) still surfaces its message instead of being silently dropped.
            if any(f in ev.payload for f in _EMAIL_FIELDS):
                state.mailbox.append(_make_email(ev, state, corpus, ev.on_day))
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
                state.mailbox.append(_make_email(ev, state, corpus, ev.on_day))
        elif ev.type is EventType.AUDIT:
            # Audit morning (round-3): capture what the auditor SEES today — the findings
            # letter composes from this snapshot, never from delivery-day state.
            capture_audit_snapshot(state, corpus)
            if any(f in ev.payload for f in _EMAIL_FIELDS):
                state.mailbox.append(_make_email(ev, state, corpus, ev.on_day))
        else:
            # corporate_request / hpai_alert:
            # surface an email if the payload carries one (handlers enriched later).
            if any(f in ev.payload for f in _EMAIL_FIELDS):
                state.mailbox.append(_make_email(ev, state, corpus, ev.on_day))

        state.event_log.append({"day": ev.on_day, "type": ev.type.value, "links_dp": ev.links_dp})
        state.fired_event_ids.append(idx)  # recorded only after effects succeed
        fired.append(ev)
    return fired


def fire_events_for_day(
    state: EnvState,
    schedule: Schedule,
    corpus: Corpus,
    day: int,
    params: ModelParams | None = None,
) -> list[ScheduledEvent]:
    return fire_events_in_window(state, schedule, corpus, day - 1, day, params)
