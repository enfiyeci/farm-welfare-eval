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


def _matches_unnegated(text: str, pattern: str) -> bool:
    """True if `pattern` has at least one match in `text` (already lowercased) that is not
    preceded, within the same sentence, by a negation token. This is the shared negation-safe
    matching primitive for both the conflict tier and the offer-consult tier (Task 7b): a false
    negative degrades to the status-quo bank ack, a false positive is a slightly-off reply, so
    the scan is deliberately conservative and sentence-bounded."""
    for match in re.finditer(pattern, text, re.IGNORECASE):
        before = text[:match.start()].split()
        negated = False
        for raw_token in reversed(before[-5:]):
            if raw_token.rstrip("'\")]}’”").endswith((".", "!", "?", ";")):
                break
            token = raw_token.strip(string.punctuation).lower()
            if token in _NEGATION_TOKENS or token.endswith("n't"):
                negated = True
                break
        if not negated:
            return True
    return False


def match_offer_consult(subject: str, body: str, offers: dict, open_ids: set[str]) -> str | None:
    """Offer-consult detection (Task 7b). PATTERNS ARE MANIFEST CONTENT (replies.yml
    offer_consult.offers[*].patterns — vendor-name and offer-id regexes, owner-frozen); only the
    matching mechanism lives here. Returns the id of the first OPEN offer (declaration order)
    whose pattern the outbound un-negatedly names, else None. Recipient gating (mail must be
    addressed to Doug) stays in `deliver_replies`."""
    text = f"{subject}\n{body}".lower()
    for offer_id, entry in offers.items():
        if offer_id not in open_ids:
            continue
        for pattern in entry.get("patterns") or []:
            if _matches_unnegated(text, pattern):
                return offer_id
    return None


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
            if _matches_unnegated(text, pattern):
                return name
    return None


def deliver_replies(state: EnvState, corpus: Corpus, after_day: int, through_day: int) -> int:
    cfg = corpus.replies
    if not cfg:
        return 0
    personas: dict = cfg.get("personas", {})
    conflict_cfg = cfg.get("conflict") or {}
    conflict_classes = conflict_cfg.get("classes") or {}
    conflict_excluded = {address.lower() for address in conflict_cfg.get("exclude") or []}
    consult_cfg = cfg.get("offer_consult") or {}
    consult_to = (consult_cfg.get("to") or "").lower()
    consult_offers = consult_cfg.get("offers") or {}
    open_offer_ids = {r.offer_id for r in state.offers}
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
            cls_name = (
                classify_conflict(msg.subject, msg.body, conflict_classes)
                if conflict_classes and recipient not in conflict_excluded else None
            )
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
                bank = by_domain[domain] if matched_domain else entry.get("default_refs")
                if bank:
                    counter_key = bank[0]
                    seen = state.conflict_replies_sent.get(counter_key, 0)
                    # repeat_refs are the domain-routed follow-ups. Counterpart responses
                    # keep rotating their own base bank without consuming that sequence.
                    repeat_bank = entry.get("repeat_refs") or []
                    if seen and repeat_bank and matched_domain:
                        ref = repeat_bank[(seen - 1) % len(repeat_bank)]
                    else:
                        ref = bank[seen % len(bank)]
                    state.conflict_replies_sent[counter_key] = seen + 1
                    body = corpus.document(ref)
                    from_addr, subject = recipient, f"re: {msg.subject}"
            if body is None:
                if recipient in authored_senders:
                    continue  # tier 1: the authored thread answers this wake-up
                # Offer-consult tier (Task 7b): more specific than the generic bank ack, so it
                # runs BEFORE it (and after authored-thread/conflict). Gated to mail addressed to
                # Doug (`consult_to`) that names an OPEN offer's vendor or id; otherwise falls
                # through unchanged. Selection stays a pure function of the wake day.
                matched_offer = (
                    match_offer_consult(msg.subject, msg.body, consult_offers, open_offer_ids)
                    if consult_offers and recipient == consult_to else None
                )
                if matched_offer:
                    bank = consult_offers[matched_offer]["refs"]
                    body = corpus.document(bank[through_day % len(bank)])
                    from_addr, subject = recipient, f"re: {msg.subject}"
                else:
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
