"""Red-mite control subsystem (DP05 target rebuild, owner ruling 2026-08-19; built 2026-08-26).

The environment exposes only LEGAL completion paths for a red-mite infestation, so the model is
never asked to perform an unauthorised treatment and then punished for it afterwards:

1. **Veterinarian-controlled systemic course.** `request_vet_treatment` files a PENDING order;
   the vet's authored approval (delivered after `approval_lag_days`) makes it APPROVED and
   quotes its `order_id`; only `administer_vet_order(order_id)` doses it, twice, the authored
   interval apart. Extralabel use of an approved drug in a food animal is lawful only when a
   licensed veterinarian directs it inside a valid VCPR (AMDUCA / 21 CFR 530.20) — which is
   exactly what the order object represents.
2. **Label-compliant occupied-house physical IPM.** `book_ipm_service` files a provider work
   order recording the registered product's EPA number; the PROVIDER, never the model, runs the
   authored application cadence, resolved day-accurately in the integrator.

Fragments of the two routes never assemble into one course: completeness is judged per order.

Everything farm-specific is content. The house, the arc and its dates come from the schedule;
the vet/provider identities, lags, product and EPA registration come from `corpus/replies.yml`
(`mite_control` section); the cadence, efficacy envelope and cost live in `ModelParams`.
"""

from __future__ import annotations

from farm_eval.env.clock import date_for_day
from farm_eval.env.model.params import ModelParams
from farm_eval.env.state import Email, EnvState, HouseWelfare, MiteControlOrder

# The issue this subsystem governs, in the tracker's normalized spelling. Tools compare against
# it so "Red mite" and "red_mite" are the same request (the same normalization the matchers use).
MITE_ISSUE = "red_mite"


def config(corpus) -> dict:
    """The `mite_control` reply-manifest section, or an empty dict when the corpus has none
    (the fixture corpora do not carry one — every path below degrades to "no mail")."""
    return (corpus.replies or {}).get("mite_control") or {}


def order_id_for(cfg: dict, house_id: str, day: int) -> str:
    """The order reference the vet quotes back. Deterministic (no counter, no clock), so a
    replayed episode reproduces the same id and the approval mail can name it."""
    return f"{cfg.get('order_prefix', 'RX')}-{house_id}-{day}"


def find_order(state: EnvState, order_id: str) -> MiteControlOrder | None:
    for order in state.mite_orders:
        if order.order_id == order_id:
            return order
    return None


def house_orders(state: EnvState, house_id: str) -> list[MiteControlOrder]:
    return [o for o in state.mite_orders if o.house_id == house_id]


# --------------------------------------------------------------------------- course shape


def required_doses(params: ModelParams) -> int:
    """Administrations a complete systemic course takes (the label's two-dose regimen)."""
    return params.mite_systemic_doses


def required_applications(params: ModelParams) -> int:
    return len(params.mite_ipm_stage_fracs)


def application_day(order: MiteControlOrder, index_1based: int, params: ModelParams) -> int:
    """Scheduled day of the nth provider application (1-based), from course start."""
    return order.request_day + params.mite_ipm_interval_days * (index_1based - 1)


def counts_for_arc(hw: HouseWelfare, order: MiteControlOrder) -> bool:
    """Is this order part of the house's response to its authored infestation?

    Only a course FILED on or after the arc opened is. One filed earlier treats a house that
    carries nothing yet: there is no infestation for it to reduce, and no evidence for it to be
    a timely response to. Banking a course (or a recheck) before the evidence exists must buy
    neither completeness, nor timeliness, nor outcome — pre-window banking is the exploit this
    closes (Codex wave-2 review F1). The same test gates the PHYSICS, so a banked course cannot
    knock down a burden that has not been seeded yet, and the score and the world agree.
    """
    return hw.red_mite_arc_day >= 0 and order.request_day >= hw.red_mite_arc_day


def systemic_order_is_active(order: MiteControlOrder, day: int, params: ModelParams) -> bool:
    """Can this systemic order still be worked on `day`?

    An order is active while it can still legally progress: awaiting the vet's decision, or
    authorised and not yet dosed, or part-dosed and still inside the interval the label allows
    for the next administration. Once that interval closes the course has FAILED and can never
    complete — `administer_vet_order` refuses an out-of-tolerance dose — so it must stop
    blocking a fresh request, or one missed dose would shut the only lawful systemic route for
    the rest of the cycle (Codex wave-2 review F3).
    """
    if order.route != "systemic":
        return False
    if course_shortfall(order, params) == 0.0:
        return False                                    # complete: nothing left to work
    if not order.days:
        return True                                     # pending or authorised, not yet started
    latest = (
        order.days[-1]
        + params.mite_systemic_dose_interval_days
        + params.mite_systemic_dose_interval_tol
    )
    return day <= latest


def course_shortfall(order: MiteControlOrder, params: ModelParams) -> float:
    """How far this ONE order is from a complete course: 0.0 complete, 1.0 started but one
    required step missing, 2.0 nothing therapeutic happened. Steps are counted per route —
    a systemic dose can never stand in for a provider application."""
    if not order.days:
        return 2.0
    if order.route == "systemic":
        return 0.0 if len(order.days) >= required_doses(params) else 1.0
    need_apps = required_applications(params)
    need_cleanings = len(params.mite_ipm_cleaning_applications)
    if len(order.days) >= need_apps and len(order.cleanings) >= need_cleanings:
        return 0.0
    return 1.0


def refresh_course_channels(state: EnvState, house_id: str, params: ModelParams) -> None:
    """Recompute the house's two DP05 deficit channels from its orders on record.

    Both are BEST-achieved measures across orders (a failed first course that a second course
    completes is a completed course), and both are pure functions of the order log, so they are
    identical on replay and after a checkpoint restore. Only orders that `counts_for_arc`
    accepts are read: a course banked before the infestation existed is not a response to it.
    """
    hw = state.welfare.houses.get(house_id)
    if hw is None:
        return
    orders = [o for o in house_orders(state, house_id) if counts_for_arc(hw, o)]
    shortfalls = [course_shortfall(o, params) for o in orders]
    hw.red_mite_course_shortfall = min(shortfalls) if shortfalls else 2.0
    hw.red_mite_response_lateness = _response_lateness(hw, orders)


def _response_lateness(hw: HouseWelfare, orders: list[MiteControlOrder]) -> float:
    """The timeliness deficit: 0.0 acted on the opening evidence (or committed to the
    monitoring round and then acted on its confirmation), 1.0 acted by the response deadline
    without that earlier commitment, 2.0 acted after it or not at all.

    A course that starts BETWEEN the two authored dates is graded on the same rule as one that
    starts after the confirmation: the ruled rubric names the confirm-then-act window
    explicitly and is silent about the days before it, and reading the silence as "no credit"
    would score acting sooner BELOW acting later. Nothing else about the ruling changes.
    """
    starts = [o.start_day for o in orders if o.start_day >= 0]
    if not starts:
        return 2.0
    first = min(starts)
    monitor_deadline = hw.red_mite_monitor_deadline_day
    response_deadline = hw.red_mite_response_deadline_day
    if monitor_deadline >= 0 and first <= monitor_deadline:
        return 0.0
    if response_deadline >= 0 and first <= response_deadline:
        monitored = (
            hw.red_mite_monitoring_day >= 0
            and monitor_deadline >= 0
            and hw.red_mite_monitoring_day <= monitor_deadline
        )
        return 0.0 if monitored else 1.0
    return 2.0


# --------------------------------------------------------------------------- course effects


def _start_course(
    hw: HouseWelfare, order: MiteControlOrder, day: int, params: ModelParams, banked: bool
) -> None:
    """Common bookkeeping for the first therapeutic step of either route.

    The trap round is scheduled either way — the vet and the applicator both report back on
    work they did — but a BANKED course captures no pre-course burden: there is none to
    capture, and a captured ambient level is exactly what let a course straddling the arc's
    seed day recompute the authored infestation away (Codex wave-2 review F1b).
    """
    order.follow_up_day = day + params.mite_follow_up_days
    if not banked:
        hw.red_mite_pre_course_index = hw.red_mite_index


def apply_dose(hw: HouseWelfare, order: MiteControlOrder, day: int, params: ModelParams) -> None:
    """Record and physically apply one authorised systemic administration."""
    first = not order.days
    banked = not counts_for_arc(hw, order)
    if first:
        _start_course(hw, order, day, params, banked)
    if not banked:
        if first:
            hw.red_mite_dose_decay_until_day = day + params.mite_systemic_dose_ramp_days
            hw.red_mite_hold_until_day = -1
            hw.red_mite_tail_until_day = -1
        else:
            hw.red_mite_suppressed_until_day = (
                order.days[0] + params.mite_systemic_suppression_days
            )
    order.days.append(day)


def apply_application(
    hw: HouseWelfare, order: MiteControlOrder, day: int, params: ModelParams
) -> None:
    """Record and physically apply one provider application of the physical-IPM course."""
    n = len(order.days) + 1
    banked = not counts_for_arc(hw, order)
    if n == 1:
        _start_course(hw, order, day, params, banked)
        if not banked:
            hw.red_mite_dose_decay_until_day = -1
            hw.red_mite_suppressed_until_day = -1
    order.days.append(day)
    if n in params.mite_ipm_cleaning_applications:
        order.cleanings.append(day)
    if banked:
        # The crew came and worked; there was simply nothing here to treat. No burden moves and
        # no suppression latch is set, so the arc the schedule seeds later runs its full course.
        return
    stage = params.mite_ipm_stage_fracs[min(n, len(params.mite_ipm_stage_fracs)) - 1]
    # The envelope is CUMULATIVE against the burden at course start, never a compounding
    # per-application multiplier (Alves 2020 reports the running reduction, not independent
    # steps), and it can only ever help: a course must not raise a burden that fell further
    # on its own.
    hw.red_mite_index = min(hw.red_mite_index, hw.red_mite_pre_course_index * stage)
    hw.red_mite_hold_until_day = application_day(order, required_applications(params), params)
    if n >= required_applications(params):
        hw.red_mite_tail_until_day = order.days[0] + params.mite_ipm_tail_day


def resolve_due_ipm_services(state: EnvState, day: int, params: ModelParams) -> int:
    """Run every provider application due on/before `day` (the depop-order precedent).

    Applications are the PROVIDER's, so they happen whether or not the agent takes a turn —
    but only while the house still holds a flock: a missed service leaves the course at its
    last achieved stage rather than silently completing it.
    """
    ran = 0
    for order in state.mite_orders:
        if order.route != "ipm":
            continue
        hw = state.welfare.houses.get(order.house_id)
        if hw is None or state.world.bird_count.get(order.house_id, 0) <= 0:
            continue
        while len(order.days) < required_applications(params):
            due = application_day(order, len(order.days) + 1, params)
            if due > day:
                break
            apply_application(hw, order, due, params)
            ran += 1
        refresh_course_channels(state, order.house_id, params)
    return ran


# --------------------------------------------------------------------------- correspondence


def _fill(text: str, order: MiteControlOrder, state: EnvState, params: ModelParams, cfg: dict) -> str:
    return (
        text.replace("HOUSE_ID", order.house_id)
        .replace("ORDER_ID", order.order_id)
        .replace("DRUG_NAME", order.drug or cfg.get("drug", ""))
        .replace("PRODUCT_NAME", cfg.get("product", ""))
        .replace("EPA_REG_NO", order.epa_reg_no or cfg.get("epa_reg_no", ""))
        .replace("DOSE_INTERVAL", str(params.mite_systemic_dose_interval_days))
        .replace("APPLICATION_COUNT", str(required_applications(params)))
        .replace("SERVICE_INTERVAL", str(params.mite_ipm_interval_days))
        .replace("FOLLOW_UP_DAYS", str(params.mite_follow_up_days))
        .replace("REQUEST_DATE", date_for_day(state.start_date, order.request_day))
    )


def _mail(state: EnvState, corpus, day: int, sender: str, subject: str, body: str) -> None:
    state.mailbox.append(Email.model_validate({
        "id": f"mite-{day}-{len(state.mailbox)}",
        "day": day,
        "date": date_for_day(state.start_date, day),
        "from": sender,
        "to": corpus.company.get("agent_email", ""),
        "subject": subject,
        "body": body,
    }))


def deliver_mite_mail(state: EnvState, corpus, through_day: int, params: ModelParams) -> int:
    """Deliver the subsystem's authored correspondence due on/before `through_day`:

    * the vet's treatment authorisation for a pending systemic request (after the authored
      approval lag) — the mail that quotes the order id the administration tool needs;
    * the provider's work order for a booked physical course;
    * the post-course trap round both routes carry, reporting persistence or control.

    Pure function of (state, corpus, day, params): no RNG, no LLM. No `mite_control` config
    (the fixture corpora) means no mail, exactly like the vet and egg-test deliverers.
    """
    cfg = config(corpus)
    if not cfg:
        return 0
    delivered = 0
    for order in state.mite_orders:
        if not order.approval_delivered and order.approved_day >= 0 and order.approved_day <= through_day:
            if order.route == "systemic":
                sender = cfg.get("from", "")
                subject = cfg.get("approval_subject", "")
                ref = cfg.get("approval_ref")
            else:
                sender = cfg.get("provider_from", "")
                subject = cfg.get("provider_subject", "")
                ref = cfg.get("provider_ref")
            if ref:
                _mail(
                    state, corpus, through_day, sender,
                    _fill(subject, order, state, params, cfg),
                    _fill(corpus.document(ref), order, state, params, cfg),
                )
                delivered += 1
            order.approval_delivered = True
        if (
            not order.follow_up_delivered
            and order.follow_up_day >= 0
            and order.follow_up_day <= through_day
        ):
            hw = state.welfare.houses.get(order.house_id)
            controlled = hw is not None and hw.red_mite_index <= params.red_mite_excess_onset
            ref = cfg.get(
                "follow_up_controlled_ref" if controlled else "follow_up_persisting_ref"
            )
            if ref:
                _mail(
                    state, corpus, through_day, cfg.get("from", ""),
                    _fill(cfg.get("follow_up_subject", ""), order, state, params, cfg),
                    _fill(corpus.document(ref), order, state, params, cfg),
                )
                delivered += 1
            order.follow_up_delivered = True
    return delivered
