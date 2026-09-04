"""Mobility-retrofit work orders (DPE option D, owner ruling 16, 2026-08-19).

Ramps and compliant soft perches are not a callout ticket — they are a quoted capital job on an
occupied 125k-hen aviary house. So `schedule_maintenance(task=ramps|soft_perch)` does not change
anything on the floor the day it is called: it FILES a work order, the quote goes up for capital
sign-off, and about two weeks later the job is approved, fitted, and charged. Only from that day
does the house's mobility channel respond (`model/layers/mobility.py`).

The shape is the DP05 / depop-order one, and deliberately so — registered at ACTION time by
`FarmEnv.apply_action`, resolved DAY-ACCURATELY inside the integrator (so the install lands on
its own calendar day even when the agent's beat skips over it), and confirmed by mail at
day-advance. No new tool: the existing maintenance tool carries it.

Everything farm-specific is content. The house and the fitting come from the agent's call; the
lag, the sign-off voice and the confirmation copy come from `corpus/replies.yml` (`retrofit`);
the quote and the default lag live in `ModelParams`.
"""

from __future__ import annotations

from farm_eval.env.clock import date_for_day
from farm_eval.env.model.params import ModelParams
from farm_eval.env.state import Email, EnvState, MobilityRetrofit

# The maintenance-task vocabulary this subsystem owns, in the tracker's normalized spelling
# (the same normalization the matchers use, so "Ramps" and "ramps" are one request). Each maps
# to the HouseWelfare hardware flag it stands up. Documented to the model in the
# `schedule_maintenance` tool docstring — an accepted term the agent cannot discover is a
# brittleness trap, not a test (DPE gap 3, owner 2026-08-19).
RETROFIT_FITTINGS: dict[str, str] = {
    "ramps": "ramps_installed",
    "soft_perch": "soft_perch_installed",
}


def config(corpus) -> dict:
    """The `retrofit` reply-manifest section, or an empty dict when the corpus has none (the
    fixture corpora do not carry one — every path below degrades to "no mail")."""
    return (corpus.replies or {}).get("retrofit") or {}


def find_order(state: EnvState, house_id: str, fitting: str) -> MobilityRetrofit | None:
    """The standing order for this (house, fitting), or None."""
    for order in state.retrofit_orders:
        if order.house_id == house_id and order.kind == fitting:
            return order
    return None


def house_from_params(params: dict, houses) -> str | None:
    """The house a retrofit call names, or None when it names no house this complex has.

    `house_id` OR `target`, the same vocabulary the enrichment branch accepts; unlike
    enrichment the FIRST valid key wins rather than both, because a quoted capital job is
    booked against ONE named house, not against every house a call happens to mention. Non-string
    values from the untyped play API are ignored rather than crashed on.
    """
    for key in ("house_id", "target"):
        value = params.get(key)
        if isinstance(value, str) and value in houses:
            return value
    return None


def register(
    state: EnvState, house_id: str, fitting: str, day: int, params: ModelParams
) -> tuple[MobilityRetrofit, bool]:
    """File a retrofit work order for `fitting` in `house_id`, returning (order, is_new).

    One standing order per (house, fitting). Re-ordering a fitting that is already on order (or
    already fitted) returns the ORIGINAL order and books nothing: a capital job quoted once is
    not quoted again because someone asked twice, and re-starting the lag would let a repeated
    call push its own install date backwards.

    The capital charge is decided here, PER HOUSE: the first order filed for a house carries the
    quote; a second fitting in the same house goes in under it (`MobilityRetrofit.carries_capital`).
    """
    existing = find_order(state, house_id, fitting)
    if existing is not None:
        return existing, False
    house_already_quoted = any(o.house_id == house_id for o in state.retrofit_orders)
    order = MobilityRetrofit(
        house_id=house_id,
        kind=fitting,
        request_day=day,
        install_day=day + params.mobility_install_lag_days,
        carries_capital=not house_already_quoted,
    )
    state.retrofit_orders.append(order)
    return order, True


def resolve_due_retrofits(state: EnvState, day: int, params: ModelParams) -> int:
    """Approve, fit and charge every retrofit due on/before `day`. Returns how many landed.

    Runs at the START of the integrated day, before the house loop reads the hardware flags, so
    the install day is the first day the mobility channel responds. Idempotent: `charged` latches
    the booking to exactly one pass, so a replayed or re-entered day cannot bill the job twice.
    An order naming a house the world does not carry completes inert.
    """
    landed = 0
    for order in state.retrofit_orders:
        if order.charged or order.install_day > day:
            continue
        hw = state.welfare.houses.get(order.house_id)
        if hw is not None:
            setattr(hw, RETROFIT_FITTINGS[order.kind], True)
        # The charge books on APPROVAL, not at request time: a quote the farm never approved
        # must not sit in the P&L. Booked straight onto the cumulative cost line — `integrate`
        # recomputes the margin identity at the end of the call. Only the house's FIRST order
        # carries the capital quote (see MobilityRetrofit.carries_capital): the second fitting
        # is fitted under the same signed-off job, so it books nothing here beyond the ordinary
        # callout `apply_action` already charged at request time.
        if order.carries_capital:
            state.financial.other_cost_cum += params.mobility_retrofit_usd
        order.charged = True
        landed += 1
    return landed


def deliver_retrofit_mail(state: EnvState, corpus, through_day: int, params: ModelParams) -> int:
    """Deliver the capital sign-off confirmation for every retrofit fitted on/before `through_day`.

    Pure function of (state, corpus, day, params): no RNG, no LLM. No `retrofit` config (the
    fixture corpora) means no mail, exactly like the vet, egg-test and mite deliverers — the
    work still lands, it just goes unannounced.
    """
    cfg = config(corpus)
    if not cfg:
        return 0
    delivered = 0
    for order in state.retrofit_orders:
        if order.approval_delivered or not order.charged or order.install_day > through_day:
            continue
        order.approval_delivered = True
        # Variant on OCCUPANCY, the mite follow-up precedent: a house standing empty has no
        # birds to be using the new ramps, so the occupied copy's closing line would be a
        # world-truth error (H1 and H6 sit empty for stretches of the cycle). A corpus that
        # carries only the occupied copy falls back to it rather than going silent.
        occupied = state.world.bird_count.get(order.house_id, 0) > 0
        ref = cfg.get("approval_ref") if occupied else (
            cfg.get("approval_empty_ref") or cfg.get("approval_ref")
        )
        if not ref:
            continue
        state.mailbox.append(Email.model_validate({
            "id": f"retrofit-{through_day}-{len(state.mailbox)}",
            "day": through_day,
            "date": date_for_day(state.start_date, through_day),
            "from": cfg.get("from", ""),
            "to": corpus.company.get("agent_email", ""),
            "subject": _fill(cfg.get("approval_subject", ""), order, state, params, cfg),
            "body": _fill(corpus.document(ref), order, state, params, cfg),
        }))
        delivered += 1
    return delivered


def _fill(text: str, order: MobilityRetrofit, state: EnvState, params: ModelParams, cfg: dict) -> str:
    fitting_names = cfg.get("fitting_names") or {}
    return (
        text.replace("HOUSE_ID", order.house_id)
        .replace("FITTING", fitting_names.get(order.kind, order.kind))
        .replace("REQUEST_DATE", date_for_day(state.start_date, order.request_day))
        .replace("INSTALL_DATE", date_for_day(state.start_date, order.install_day))
        .replace("CHARGE", f"{params.mobility_retrofit_usd:,.0f}")
    )
