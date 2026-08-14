"""DP13 egg-test result delivery: an authored-style system email for each resolved order.

Orders are registered at ACTION time (episode.apply_action) and RESOLVED day-accurately by
the integrator (farm_eval/env/model/layers/salmonella.resolve_due_egg_tests). This module only
walks the resolved-but-undelivered orders at each day-advance and renders the result email from
the order's stored snapshot — prose lives in corpus/replies.yml `egg_test` (inline fragments),
so no farm content is hardcoded in logic. Pure function of (state, corpus, day, params): no RNG,
no LLM. The body states the result and which test-of-four it was (or that it was off-protocol)
— surface honesty, no scoring leak."""

from __future__ import annotations

from farm_eval.env.clock import date_for_day
from farm_eval.env.loader import Corpus
from farm_eval.env.state import Email, EnvState


def deliver_egg_test_mail(state: EnvState, corpus: Corpus, through_day: int, params) -> int:
    """Deliver a result email for every egg-test order resolved on/before `through_day` and
    not yet delivered. Returns the number delivered. No egg_test reply config -> no-op (the
    fixture corpus carries none)."""
    cfg = (corpus.replies or {}).get("egg_test")
    if not cfg:
        return 0
    delivered = 0
    for order in state.egg_test_orders:
        if order.delivered or not order.resolved or order.result_day > through_day:
            continue
        state.mailbox.append(Email.model_validate({
            "id": f"egt-{through_day}-{len(state.mailbox)}",
            "day": through_day,
            "date": date_for_day(state.start_date, through_day),
            "from": cfg["from"],
            "to": corpus.company.get("agent_email", ""),
            "subject": cfg["subject"].replace("HOUSE_ID", order.house_id),
            "body": _render_body(cfg, order, state, params),
        }))
        order.delivered = True
        delivered += 1
    return delivered


def _render_body(cfg: dict, order, state: EnvState, params) -> str:
    intro = (
        cfg["intro"]
        .replace("HOUSE_ID", order.house_id)
        .replace("COLLECTED_DATE", date_for_day(state.start_date, order.ordered_day))
        .replace("REPORT_DATE", date_for_day(state.start_date, order.result_day))
    )
    result_line = cfg["result_positive"] if order.result_positive else cfg["result_negative"]
    if order.counts_toward_protocol:
        protocol_line = (
            cfg["protocol_counted"]
            .replace("NEGRUN", str(order.neg_run_after if order.neg_run_after is not None else 0))
            .replace("NEEDED", str(params.se_protocol_negatives))
        )
    else:
        protocol_line = cfg["protocol_offschedule"].replace(
            "NEEDED_INTERVAL", str(params.se_protocol_interval_days)
        )
    lines = [intro, "", result_line, protocol_line]
    if order.cleared_here:
        lines.append(cfg["cleared_line"])
    return "\n".join(lines)
