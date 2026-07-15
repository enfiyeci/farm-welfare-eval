"""Vet-outcome tier (round-3 F-R2-2): deterministic correspondence for schedule_vet_visit.

Arcs are registered at ACTION time (episode.apply_action); this module only walks them at
each day-advance: ack at the next wake-up, visit report at the first wake-up on/after the
visit day (both in one wake-up when the beat gap jumps the visit day). Runs BEFORE
deliver_replies so the vet counts as an authored sender for tier-1 suppression — no
same-wake-up double reply. Pure function of (state, corpus, day): no RNG, no LLM. Report
bodies recommend and restate the vet's own guidance; they never assert the agent
treated/complied (truthfulness rule — docs/plans/2026-07-14-round3-content-pass-design.md)."""

from __future__ import annotations

from farm_eval.env.clock import date_for_day
from farm_eval.env.loader import Corpus
from farm_eval.env.state import Email, EnvState, VetVisit


def _fill(text: str, visit: VetVisit, state: EnvState) -> str:
    return (
        text.replace("HOUSE_ID", visit.house_id or "the complex")
        .replace("REASON_TEXT", visit.reason or "a general flock check")
        .replace("VISIT_DATE", date_for_day(state.start_date, visit.visit_day))
    )


def _report_ref(cfg: dict, reason: str) -> str:
    low = reason.lower()
    for row in cfg.get("report_classes") or []:
        if any(term in low for term in row.get("contains", [])):
            return row["ref"]
    return cfg["report_default_ref"]


def deliver_vet_mail(state: EnvState, corpus: Corpus, through_day: int) -> int:
    cfg = (corpus.replies or {}).get("vet")
    if not cfg:
        return 0
    delivered = 0

    def _append(ref: str, subject_tpl: str, visit: VetVisit) -> None:
        nonlocal delivered
        state.mailbox.append(Email.model_validate({
            "id": f"vet-{through_day}-{len(state.mailbox)}",
            "day": through_day,
            "date": date_for_day(state.start_date, through_day),
            "from": cfg["from"],
            "to": corpus.company.get("agent_email", ""),
            "subject": _fill(subject_tpl, visit, state),
            "body": _fill(corpus.document(ref), visit, state),
        }))
        delivered += 1

    for visit in state.vet_visits:
        if visit.stage == "reported":
            continue
        if visit.duplicate_of is not None:
            # Folded request: one short pending-ack, then done — never a second arc.
            _append(cfg["ack_pending_ref"], cfg["ack_pending_subject"], visit)
            visit.stage = "reported"
            continue
        if visit.stage == "requested":
            _append(cfg["ack_ref"], cfg["ack_subject"], visit)
            visit.stage = "acked"
        if visit.stage == "acked" and through_day >= visit.visit_day:
            _append(_report_ref(cfg, visit.reason), cfg["report_subject"], visit)
            visit.stage = "reported"
    return delivered
