"""Deterministic correspondence closure (WS5): every outbound message gets exactly one
in-world response at the next wake-up. Three tiers — authored thread (suppresses the ack),
known-persona ack/deflection bank, unknown-addressee bounce. All content is corpus-loaded;
selection is a pure function of (day, prior reply count) — no RNG, no LLM."""

from __future__ import annotations

from farm_eval.env.clock import date_for_day
from farm_eval.env.loader import Corpus
from farm_eval.env.state import Email, EnvState


def deliver_replies(state: EnvState, corpus: Corpus, after_day: int, through_day: int) -> int:
    cfg = corpus.replies
    if not cfg:
        return 0
    personas: dict = cfg.get("personas", {})
    agent_addr = corpus.company.get("agent_email", "").lower()
    authored_senders = {e.from_ for e in state.mailbox if after_day < e.day <= through_day}
    delivered = 0
    for msg in list(state.outbound):
        if msg.id in state.replied_outbound_ids or msg.day > after_day:
            continue
        state.replied_outbound_ids.append(msg.id)
        recipient = msg.to.split(",")[0].strip().lower()
        if not recipient or recipient == agent_addr:
            continue
        if recipient in personas:
            if recipient in authored_senders:
                continue  # tier 1: the authored thread answers this wake-up
            bank = personas[recipient]["bank"]
            seq = sum(1 for e in state.mailbox if e.id.startswith("reply-") and e.from_ == recipient)
            body = corpus.document(bank[(through_day + seq) % len(bank)])
            from_addr, subject = recipient, f"re: {msg.subject}"
        else:
            body = corpus.document(cfg["bounce_ref"]).replace("RECIPIENT_ADDR", recipient)
            from_addr, subject = cfg["bounce_from"], f"Undeliverable: {msg.subject}"
        state.mailbox.append(Email.model_validate({
            "id": f"reply-{through_day}-{len(state.mailbox)}",
            "day": through_day,
            "date": date_for_day(state.start_date, through_day),
            "from": from_addr,
            "to": msg.from_,
            "subject": subject,
            "body": body,
            "in_reply_to": msg.id,
        }))
        delivered += 1
    return delivered
