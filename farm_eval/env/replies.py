"""Deterministic correspondence closure (WS5): every outbound message gets exactly one
in-world response at the next wake-up. Four tiers — conflict-class response, authored thread
(suppresses the ack), known-persona ack/deflection bank, unknown-addressee bounce. All content
is corpus-loaded; selection is a pure function of (day, prior reply count) — no RNG, no LLM."""

from __future__ import annotations

from email.utils import getaddresses
import re
import string

from farm_eval.env.clock import date_for_day
from farm_eval.env.loader import Corpus
from farm_eval.env.state import Email, EnvState


_NEGATION_TOKENS = {"no", "not", "never", "without"}


def classify_conflict(subject: str, body: str, classes: dict) -> str | None:
    """Conflict-class detection (round-3 F-R2-3). PATTERNS ARE MANIFEST CONTENT
    (replies.yml conflict.classes[*].patterns — authored, owner-frozen, lintable); only
    the matching mechanism lives here. Conservative by design: a false negative is the
    status quo (bank ack); a false positive is a weird reply — patterns are first-person
    anchored so mail ABOUT someone else's resignation stays in the bank tier. Priority =
    manifest declaration order (first matching class wins)."""
    stripped_subject = subject.lstrip()
    if stripped_subject.lower().startswith(("re:", "fw:", "fwd:")):
        text = body.lower()
    else:
        text = f"{subject}\n{body}".lower()
    for name, cls in classes.items():
        for pattern in cls.get("patterns") or []:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                before = text[:match.start()].split()
                negated = False
                for raw_token in reversed(before[-5:]):
                    if raw_token.endswith((".", "!", "?", ";")):
                        break
                    token = raw_token.strip(string.punctuation).lower()
                    if token in _NEGATION_TOKENS or token.endswith("n't"):
                        negated = True
                        break
                if negated:
                    continue
                return name
    return None


def deliver_replies(state: EnvState, corpus: Corpus, after_day: int, through_day: int) -> int:
    cfg = corpus.replies
    if not cfg:
        return 0
    personas: dict = cfg.get("personas", {})
    agent_addr = corpus.company.get("agent_email", "").lower()
    # Lowercased to match the normalized recipient below — a mixed-case schedule `from:`
    # must not silently defeat tier-1 suppression.
    authored_senders = {e.from_.lower() for e in state.mailbox if after_day < e.day <= through_day}
    delivered = 0
    for msg in list(state.outbound):
        if msg.id in state.replied_outbound_ids or msg.day > after_day:
            continue
        state.replied_outbound_ids.append(msg.id)
        raw_to = msg.to.strip()
        if not raw_to:
            continue  # nothing addressable: marked answered, no mail
        # `getaddresses` (not a naive split-on-comma) is required because a display name
        # can itself contain a comma ("Whitaker, Glenn <g@x>"). Models plausibly write
        # semicolon-separated lists, and the strict (3.13+) parser rejects a WHOLE list
        # over one empty element (even a trailing separator), so normalize ';' to ',' and
        # drop empty chunks first. An addr-spec must contain '@' — otherwise the header is
        # garbage ("just a name") and we bounce the raw value rather than a fragment.
        normalized = ",".join(c for c in (p.strip() for p in raw_to.replace(";", ",").split(",")) if c)
        parsed = getaddresses([normalized]) if normalized else []
        recipient = next((a.strip().lower() for _, a in parsed if "@" in a), "")
        if recipient == agent_addr:
            continue
        if recipient in personas:
            body = None
            conflict_classes = (cfg.get("conflict") or {}).get("classes") or {}
            cls_name = classify_conflict(msg.subject, msg.body, conflict_classes) if conflict_classes else None
            if cls_name:
                # Conflict tier (round-3 F-R2-3): BEFORE tier-1 suppression — a resignation
                # must draw its response even when the persona also has authored mail this
                # wake-up. Voice routes by recipient domain (corporate prose must never go
                # out in the vet's name); everyone unconfigured gets the counterpart body.
                # One-shot is keyed by REF: the corporate resignation response fires once,
                # repeats get the standing shorter acknowledgment; a counterpart reply does
                # not consume the corporate one-shot.
                entry = conflict_classes[cls_name]
                by_domain = entry.get("by_domain") or {}
                domain = recipient.rsplit("@", 1)[-1]
                matched_domain = domain in by_domain
                base_ref = by_domain[domain] if matched_domain else entry.get("default_ref")
                if base_ref:
                    seen = state.conflict_replies_sent.get(base_ref, 0)
                    # repeat_ref is authored as the DOMAIN-ROUTED (corporate) follow-up, so
                    # it pairs only with by_domain refs; a repeated counterpart message just
                    # gets the counterpart body again ("still not my desk" is realistic).
                    if seen and entry.get("repeat_ref") and matched_domain:
                        ref = entry["repeat_ref"]
                    else:
                        ref = base_ref
                    state.conflict_replies_sent[base_ref] = seen + 1
                    body = corpus.document(ref)
                    from_addr, subject = recipient, f"re: {msg.subject}"
            if body is None:
                if recipient in authored_senders:
                    continue  # tier 1: the authored thread answers this wake-up
                bank = personas[recipient]["bank"]
                seq = sum(1 for e in state.mailbox if e.id.startswith("reply-") and e.from_ == recipient)
                body = corpus.document(bank[(through_day + seq) % len(bank)])
                from_addr, subject = recipient, f"re: {msg.subject}"
        else:
            # recipient == "" means no parseable addr-spec: never silently drop a
            # non-blank outbound — bounce it with the raw header value.
            body = corpus.document(cfg["bounce_ref"]).replace("RECIPIENT_ADDR", recipient or raw_to)
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
