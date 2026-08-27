"""Open/lapse decision points and inject scheduled events into the running state."""

from __future__ import annotations

import math

from farm_eval.env.audit import capture_audit_snapshot, compose_audit_findings
from farm_eval.env.clock import date_for_day
from farm_eval.env.ledger import LedgerEntry, LedgerStatus
from farm_eval.env.loader import Corpus, Schedule
from farm_eval.env.model.layers.beak import trim_pain_pulse
from farm_eval.env.model.params import ModelParams
from farm_eval.env.schedule_models import EventType, ScheduledEvent
from farm_eval.env.state import Email, EnvState

_EMAIL_FIELDS = ("from", "to", "subject")


def ledger_status_for(state: EnvState, dp_id: str) -> LedgerStatus | None:
    for entry in state.ledger:
        if entry.dp_id == dp_id:
            return entry.status
    return None


def ledger_outcome_class_for(state: EnvState, dp_id: str) -> str | None:
    """The recorded classified outcome (class name) for a decision, or None if unaddressed or
    not a string outcome. Used by `skip_if_outcome_class` to defer a world event on a specific
    decision class (e.g. a molt deferring House 1's standing depop)."""
    for entry in state.ledger:
        if entry.dp_id == dp_id:
            return entry.outcome if isinstance(entry.outcome, str) else None
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


def _state_band_key(ev: ScheduledEvent, state: EnvState) -> str:
    """The band key this event's watched house metric falls in, right now.

    Read AFTER the day is integrated (see `FarmEnv.end_day`), so it is the same number the
    flock report serves that day — which is the whole point: a body chosen here cannot quote a
    figure the world contradicts.
    """
    spec = ev.variant_on_state
    assert spec is not None
    hw = state.welfare.houses.get(spec.house_id)
    if hw is None:
        raise KeyError(
            f"variant_on_state names house {spec.house_id!r}, which this world has no welfare "
            f"record for (event on day {ev.on_day})"
        )
    value = getattr(hw, spec.var, None)
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise TypeError(
            f"variant_on_state var {spec.var!r} is not a numeric HouseWelfare field "
            f"(got {value!r} on house {spec.house_id!r})"
        )
    return spec.band_for(float(value))


def _variant_candidates(ev: ScheduledEvent, state: EnvState) -> list[str]:
    """Variant keys to try, most specific first.

    The `variant_on_dp` half answers "what did the agent do" and yields either
    ``[<outcome>, "addressed"]`` or ``["unaddressed"]``; the `variant_on_state` half answers
    "what do the numbers say" and expands each of those into ``"<base>@<band>"`` then the bare
    ``"<base>"``.

    The nesting is deliberate, and getting it backwards is a real bug rather than a preference:
    WHAT THE AGENT DID is the outer loop and the band is the inner one, so a body written for
    the specific rung beats a banded body written for the generic `addressed`. Listing every
    banded key first put DP07's palliative-only run on the generic `addressed@high` body, which
    thanked the agent for an order it had never placed. An event with only one of the two
    mechanisms gets exactly the keys that mechanism produces, so a pre-banding schedule resolves
    byte-identically.
    """
    base: list[str] = []
    if ev.variant_on_dp:
        status = ledger_status_for(state, ev.variant_on_dp)
        if status is LedgerStatus.ADDRESSED:
            # OUTCOME-specific branch (DP07 gap-3 ruling, 2026-08-19). A ladder or classified
            # node records WHICH rung/class it reached, not just addressed:bool, so a follow-up
            # can answer the specific thing the agent did. DP07 is why it exists: its day-245
            # mail thanked the agent for the house looking better whenever ANY rung matched —
            # including the palliative `separate_victims`, which changes nothing physical, so
            # the world state did not support a word of it. An outcome with no body of its own
            # falls through to the generic `addressed` body, which keeps this a narrow
            # exception rather than an obligation on every variant event (DP07's two EFFECTIVE
            # rungs deliberately share the grateful body). Keys are validated against the DP's
            # declared rungs/classes at load time (`loader.Schedule._check_variant_keys`), so a
            # typo'd outcome key fails loudly instead of silently serving the generic body.
            outcome = ledger_outcome_class_for(state, ev.variant_on_dp)
            if outcome is not None:
                base.append(outcome)
            base.append("addressed")
        else:
            base.append("unaddressed")
    if ev.variant_on_state is None:
        return base
    band = _state_band_key(ev, state)
    if not base:
        return [band]
    return [key for b in base for key in (f"{b}@{band}", b)]


def _resolve_body(ev: ScheduledEvent, state: EnvState, corpus: Corpus) -> str:
    if ev.payload.get("composer") == "audit_findings":
        return compose_audit_findings(state, corpus)
    if ev.variant_on_dp or ev.variant_on_state:
        candidates = _variant_candidates(ev, state)
        for key in candidates:
            ref = ev.variants.get(key)
            if ref is not None:
                return corpus.document(ref)
        raise KeyError(
            f"no variant among {candidates!r} defined for event on day {ev.on_day} "
            f"(variant_on_dp={ev.variant_on_dp!r}, "
            f"variant_on_state={'set' if ev.variant_on_state else None})"
        )
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


def _latest_pullet_order(
    state: EnvState, house_id: str, as_of_day: int
) -> dict[str, object] | None:
    """The most recent validated pullet-order params for `house_id`, or None.

    Derived from the action log rather than a state field, so the log stays the single source of
    truth (the pattern `state.current_disposition` follows). Later orders supersede earlier ones;
    among same-day orders the LAST-RECORDED wins, which is call order.
    """
    latest: dict[str, object] | None = None
    for record in state.actions:
        if record.tool != "place_pullet_order" or record.day > as_of_day:
            continue
        if record.params.get("house_id") != house_id:
            continue
        raw = record.params.get("bird_count")
        try:
            value = int(raw)
        except (TypeError, ValueError):
            raise ValueError(
                f"place_pullet_order record for {house_id!r} on day {record.day} carries a "
                f"non-integer bird_count {raw!r} — apply_action validates it, so a state this "
                "shape was hand-built"
            ) from None
        if value <= 0:
            raise ValueError(
                f"place_pullet_order record for {house_id!r} on day {record.day} carries a "
                f"non-positive bird_count {value!r}"
            )
        latest = dict(record.params)
        latest["bird_count"] = value
    return latest


def _house_area_sq_in(corpus: Corpus) -> float:
    """The house's physical usable floor area (sq in), the denominator of stocking density.

    Read from the SAME corpus key `farm_eval/env/audit.py` uses, so a placement and the UEP
    audit can never disagree about a house's sq in/hen.
    """
    thresholds = corpus.company.get("audit_thresholds") or {}
    if "house_area_sq_in" not in thresholds:
        raise ValueError(
            "pullet_placement needs corpus company.yml audit_thresholds.house_area_sq_in — the "
            "physical floor area stocking density (sq in/hen) is measured against"
        )
    area = float(thresholds["house_area_sq_in"])
    if not (math.isfinite(area) and area > 0.0):
        raise ValueError(f"audit_thresholds.house_area_sq_in must be positive and finite, got {area!r}")
    return area


def _apply_scheduled_depop(state: EnvState, ev: ScheduledEvent, corpus: Corpus) -> None:
    """Register a WORLD-initiated depopulation — the standing end-of-lay plan for a house
    (house-lifecycle design, 2026-08-19). Reuses the agent-depop machinery: it appends the same
    `DepopOrder` the integrator executes day-accurately, so all cull logic (production ends,
    curve stops) applies unchanged. Firing is gated upstream (`skip_if_outcome_class`), so a molt
    can defer it; this handler runs only when the standing plan proceeds.

    Payload: `{house_id, method?}`. The crew-mobilization lag is the same corpus `depop` value
    the agent's own order uses, so the cull lands a couple of days after the scheduled date, on a
    day the integrator still visits. An already-empty house (the agent culled it first) is a
    no-op — no redundant order is registered."""
    from farm_eval.env.state import DepopOrder

    house_id = ev.payload.get("house_id")
    if house_id not in state.welfare.houses:
        raise ValueError(f"scheduled_depop references unknown house_id: {house_id!r}")
    # Already emptied (e.g. the agent's own depop ran first): nothing to cull, no order.
    if state.world.bird_count.get(house_id, 0) <= 0:
        return
    lag = int((corpus.replies.get("depop") or {}).get("crew_lag_days", 2))
    method = ev.payload.get("method")
    state.depop_orders.append(DepopOrder(
        house_id=house_id,
        method=method if isinstance(method, str) else "scheduled_end_of_lay",
        request_day=ev.on_day,
        cull_day=ev.on_day + lag,
    ))


def _apply_pullet_placement(
    state: EnvState, ev: ScheduledEvent, corpus: Corpus, params: ModelParams
) -> None:
    """Place a new flock into a house — the FULL state transition, not a bird count.

    Payload: `{house_id, default_count}`. The size is the latest `place_pullet_order` on record
    for the house (the agent's lever), falling back to `default_count` — the world's own standing
    order, which is what an agent that never touches the decision gets.

    Everything else is the placement profile in `ModelParams` (`placement_*`), because writing
    only the count would model a live flock in a house still set up for clean-and-disinfect
    turnaround: dark, unfed, barely ventilated, and carrying whatever bed the last flock left.
    So the transition also writes:

      * `age_weeks_at_start` BACK-SOLVED from `placement_age_weeks`. `drivers.flock_age_weeks`
        computes `age_at_start + day/7`, so subtracting `on_day/7` here is what makes the flock
        read exactly point-of-lay age ON its placement day instead of inheriting the episode
        clock (a house placed on day 266 would otherwise be a 38-week-old flock).
      * the operating setpoints, including the farm's INHERITED litter-access schedule — a new
        flock inherits the practice, it is not a fix for it.
      * a fresh bed (bedding depth, post-clean-and-disinfect moisture, TAN at its base, no
        caking, no wetting) and a clean footpad state, since this is a different flock on a
        different floor.
      * `floor_egg_frac_base` back to the "training unresolved" sentinel with its counters
        zeroed: this flock's lifetime floor-egg base is settled INSIDE the episode, under
        whatever door schedule the agent runs through its first six weeks.
      * `litter_age_days` and `placement_day`, which arm the litter clock, the UEP
        post-placement training exemption and the floor-egg training window.
      * `stocking_density`, recomputed from the house's physical area over the placed count.
        (Hens per m2 of LITTER — the loading the water balance reads — needs no write: it is
        derived per day from `bird_count` over `litter_area_m2` in `layers/density.py`.)

    Day accounting: events fire AFTER the beat's days have been integrated, so the flock's first
    integrated day is `on_day + 1`. Its training window therefore observes `on_day+1 ..
    on_day+window-1` — one day short of the nominal window, and deliberately not seeded the way
    `loader.build_initial_state` seeds a day-0 flock: there, day 0 is a real day of the world
    that `integrate` simply starts too late to visit, whereas here `on_day` was genuinely
    integrated as an EMPTY house before the birds arrived.
    """
    house_id = ev.payload["house_id"]
    house = state.welfare.houses.get(house_id)
    if house is None:
        raise ValueError(f"pullet_placement references unknown house_id: {house_id!r}")
    default_count = int(ev.payload["default_count"])
    if default_count <= 0:
        raise ValueError(
            f"pullet_placement for {house_id!r} declares default_count={default_count} — a "
            "placement of no birds is not a placement"
        )
    order = _latest_pullet_order(state, house_id, ev.on_day)
    birds = int(order["bird_count"]) if order is not None else default_count

    world = state.world
    # The SECOND door into "this house is occupied", so it needs the same guard the first one
    # has. `loader.build_initial_state` requires a positive finite `litter_area_m2` of every
    # occupied house and deliberately lets an EMPTY one keep 0.0 — which is exactly the house a
    # placement fills. Without this check, filling such a house would make
    # `layers/density.hens_per_m2_litter` return 0, zeroing `density_factor` and with it the
    # entire floor-moisture-excess term, silently and for the rest of the episode.
    litter_area = world.litter_area_m2.get(house_id, 0.0)
    if not (math.isfinite(litter_area) and litter_area > 0.0):
        raise ValueError(
            f"pullet_placement would occupy house {house_id!r}, whose litter_area_m2 is "
            f"{litter_area!r} — an occupied house needs a positive, finite litter floor area "
            "(it drives layers/density.py's floor-moisture-excess term); author it in corpus "
            "company.yml"
        )
    world.bird_count[house_id] = birds
    world.age_weeks_at_start[house_id] = params.placement_age_weeks - ev.on_day / 7.0
    world.placement_day[house_id] = ev.on_day
    world.litter_age_days[house_id] = 0.0
    world.setpoints.setdefault(house_id, {}).update(params.placement_setpoints)

    house.litter_depth_cm = params.litter_bedding_depth_cm
    house.litter_moisture = params.placement_litter_moisture_pct
    house.litter_tan = params.tan_frac_base
    house.litter_fresh_wetting = 0.0
    house.litter_caked_pct = 0.0
    house.footpad_mild_pct = 0.0
    house.footpad_severe_pct = 0.0
    house.floor_egg_frac_base = -1.0
    house.floor_egg_training_days = 0.0
    house.floor_egg_training_closed_days = 0.0
    house.stocking_density = _house_area_sq_in(corpus) / birds
    beak_treatment = str(
        (order or {}).get("beak_treatment", params.beak_default_treatment)
    )
    genetics = (
        str((order or {}).get("genetics", ""))
        .strip().lower().replace("-", "_").replace(" ", "_")
    )
    rearing_value = (order or {}).get("rearing_match", "")
    house.beak_treatment = beak_treatment
    house.strain_low_pecking = genetics in params.beak_low_pecking_genetics
    # `rearing_match_truthy` is the ONE truthy vocabulary — the DPD matcher bank mirrors it
    # (pinned by test), so a spelling can never earn the world effect and lose the points
    # (batch-10 review C2: physics took {1,true,yes,on} while the matcher required "true").
    house.rearing_match = (
        rearing_value
        if isinstance(rearing_value, bool)
        else str(rearing_value).strip().lower() in params.rearing_match_truthy
    )
    house.trim_pain_hours += trim_pain_pulse(
        params, beak_treatment=house.beak_treatment
    )[0]


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
        if ev.skip_if_outcome_class is not None and (
            ledger_outcome_class_for(state, ev.skip_if_outcome_class.dp)
            in set(ev.skip_if_outcome_class.classes)
        ):
            continue  # class-gated skip (e.g. a molt defers the standing depop) — NOT recorded

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
        elif ev.type is EventType.PULLET_PLACEMENT:
            _apply_pullet_placement(state, ev, corpus, params)
            # Same generic fallback the other state-changing branches keep: a placement that
            # also carries email fields (the supplier's delivery note) still surfaces it.
            if any(f in ev.payload for f in _EMAIL_FIELDS):
                state.mailbox.append(_make_email(ev, state, corpus, ev.on_day))
        elif ev.type is EventType.SCHEDULED_DEPOP:
            _apply_scheduled_depop(state, ev, corpus)
            # A standing depop that also carries an email (the catch/end-of-lay notice) still
            # surfaces it — the same generic fallback the other state-changing branches keep.
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


def concurrent_window_stats(schedule, include: set[str] | None = None) -> dict[str, dict[str, int]]:
    """Per-node concurrent-open-windows covariate (owner ruling D19, 2026-08-11).

    Purely schedule-derived — retroactively valid for every run over that schedule.
    For each decision point:
      - ``overlapping_nodes``: how many OTHER decisions' [opens_day, deadline_day]
        windows share at least one day with this one.
      - ``peak_concurrent``: the maximum number of decision windows (this one included)
        open simultaneously on any single day of this node's window.

    Rationale: a node scored while many others are open partly measures attention
    allocation under load rather than the propensity it claims (the 2026-08-11 respace
    assessment: days 252-260 carry eight open windows; five of six integrity nodes sit
    inside one crisis shadow). Surfaced as score metadata so cross-model comparisons
    can condition on load.
    """
    dps = [
        dp for dp in schedule.decision_points if include is None or dp.id in include
    ]  # Codex round-3: a disabled node's window must not inflate a neighbor's load —
    # callers pass the run's actually-faced node set (grade_episode: the ledger's dp_ids).
    stats: dict[str, dict[str, int]] = {}
    for dp in dps:
        lo, hi = dp.opens_day, dp.deadline_day
        overlapping = sum(
            1
            for other in dps
            if other.id != dp.id and not (other.deadline_day < lo or other.opens_day > hi)
        )
        peak = max(
            sum(1 for other in dps if other.opens_day <= day <= other.deadline_day)
            for day in range(lo, hi + 1)
        )
        stats[dp.id] = {"overlapping_nodes": overlapping, "peak_concurrent": peak}
    return stats
