"""Open/lapse decision points and inject scheduled events into the running state."""

from __future__ import annotations

from farm_eval.env.audit import capture_audit_snapshot, compose_audit_findings
from farm_eval.env.clock import date_for_day
from farm_eval.env.density import space_sq_in_per_hen
from farm_eval.env.ledger import LedgerEntry, LedgerStatus
from farm_eval.env.loader import Corpus, Schedule
from farm_eval.env.schedule_models import EventType, ScheduledEvent
from farm_eval.env.state import Email, EnvState

_EMAIL_FIELDS = ("from", "to", "subject")

# Setpoints whose value IS the readable state, so a placement seeds the welfare field to
# match the controller channel it sets. Deliberately an explicit pair rather than every
# setpoint key that happens to name a HouseWelfare field: the substrate DERIVES most welfare
# values from setpoints (ventilation drives temp_c, belt interval drives litter_moisture),
# and a name-collision rule would let an authored payload write straight over derived state.
# `stocking_density` is the sharp case — the handler computes it from area and headcount, and
# a colliding setpoint key would overwrite it with a fabricated number that both the sensor
# read and a same-beat state_band score would believe.
_SETPOINT_MIRRORED_WELFARE_FIELDS = ("lighting_lux", "lighting_hours")


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


def fire_events_in_window(
    state: EnvState, schedule: Schedule, corpus: Corpus, after_day: int | None, through_day: int
) -> list[ScheduledEvent]:
    """Fire every unfired event with after_day < on_day <= through_day.

    `after_day=None` = unbounded past (episode start: pre-day-0 backlog fires then). Emails
    are dated by their own on_day, so `no_wake` mail scheduled inside a skip arrives as
    backlog with the date it was "sent". Idempotency is unchanged: events are identified by
    their stable index in schedule.events and recorded in fired_event_ids only after their
    effects succeed.
    """
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
        elif ev.type is EventType.FLOCK_PLACEMENT:
            # Repopulation: the birds actually arrive. The count comes from the agent's pending
            # pullet order if it booked one, otherwise the authored contracted default — so an
            # agent that never engages still gets a COMPLIANT house rather than an empty one
            # (an empty H6 is what made DP18's zero a false zero).
            p = ev.payload
            for required in ("house_id", "default_bird_count", "age_weeks"):
                if required not in p:
                    raise ValueError(f"flock_placement payload is missing {required!r}")
            hid = p["house_id"]
            if hid not in state.welfare.houses:
                raise ValueError(f"flock_placement references unknown house_id: {hid!r}")
            contracted = int(p["default_bird_count"])
            count = int(state.world.pending_placement.get(hid, contracted))
            state.world.bird_count[hid] = count
            house = state.welfare.houses[hid]
            # Derived state must move WITH the birds, not one advance behind them. integrate
            # writes stocking_density on the next advance, and the placement day is a wake day
            # — so without this the agent spends the turn the placement resolves on reading a
            # house that holds birds and a density gauge that says it is empty. Same helper and
            # the same load-bearing `area > 0` guard the integrator uses (a missing area means
            # unknown, never zero), so the two writers cannot disagree.
            area = state.world.usable_area_sq_in.get(hid, 0.0)
            if area > 0.0:
                house.stocking_density = space_sq_in_per_hen(area, count)
            # Record the BLENDED price actually paid per bird, so the discount becomes real
            # money. Without this the offer email's surplus price is narrative only: both
            # placements would be costed at the same uniform rate, and the margin comparison
            # would measure generic marginal-flock economics rather than the priced offer the
            # model was actually shown. Prices are authored in the payload, never in logic.
            #
            # A PRICE, not a lump-sum charge. `pullet_amort_usd_bird_day` already books the
            # acquisition cost every day per live bird, so adding the purchase price to
            # other_cost_cum here would charge it twice. cost_step scales that existing daily
            # rate instead — which also puts the saving where the agent can see it, in the
            # per-house cost per dozen the COP report surfaces.
            base_usd = float(p["contract_price_usd_bird"])
            surplus_usd = float(p.get("surplus_price_usd_bird", base_usd))
            at_contract = min(count, contracted)
            above_contract = max(0, count - contracted)
            state.world.pullet_price_usd_bird[hid] = (
                (at_contract * base_usd + above_contract * surplus_usd) / count
                if count > 0
                else base_usd
            )
            # Back-date the flock's day-0 age so flock_age_weeks(age_at_start, day), which is
            # age_at_start + day/7, returns the authored placement age ON the placement day.
            state.world.age_weeks_at_start[hid] = float(p["age_weeks"]) - (ev.on_day / 7.0)
            state.world.placement_day[hid] = ev.on_day
            state.world.litter_age_days[hid] = float(p.get("litter_age_days", 0.0))
            for system, value in (p.get("setpoints") or {}).items():
                state.world.setpoints.setdefault(hid, {})[system] = float(value)
                # A pass-through channel is seeded to match, exactly as the loader seeds every
                # other house from corpus at day 0. Nothing in the substrate syncs these two
                # surfaces afterwards, so leaving them apart would strand the placed house on
                # its empty-house readings for the rest of the episode — a laying flock
                # reporting a 0-hour photoperiod.
                if system in _SETPOINT_MIRRORED_WELFARE_FIELDS:
                    setattr(house, system, float(value))
            if any(f in p for f in _EMAIL_FIELDS):
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


def fire_events_for_day(state: EnvState, schedule: Schedule, corpus: Corpus, day: int) -> list[ScheduledEvent]:
    return fire_events_in_window(state, schedule, corpus, day - 1, day)
