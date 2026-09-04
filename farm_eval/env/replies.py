"""Deterministic correspondence closure (WS5): every outbound message gets an in-world response
at the next wake-up. Four tiers — conflict-class response, authored thread (suppresses the ack),
known-persona ack/deflection bank, unknown-addressee bounce — decided by the FIRST address in the
header, plus a per-recipient institutional acknowledgment from any OTHER configured domain mailbox
in it. All content is corpus-loaded; selection is a pure function of (day, prior reply count) —
no RNG, no LLM."""

from __future__ import annotations

import re
import string

from farm_eval.env.addressing import domain_matches, parse_recipients
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
                    if raw_token.rstrip("'\")]}’”").endswith((".", "!", "?", ";")):
                        break
                    token = raw_token.strip(string.punctuation).lower()
                    if token in _NEGATION_TOKENS or token.endswith("n't"):
                        negated = True
                        break
                if negated:
                    continue
                return name
    return None


def _domain_bank(recipient: str, cfg: dict) -> list[str] | None:
    """Agency-domain tier lookup (DP15 review-pack fix, 2026-08-11): a notifiable-disease or
    regulator report is addressed to a mailbox the agent has to guess, so exact-address
    personas can never answer it — and the pre-fix bounce told the model the compliant action
    failed. Longest-suffix match against the manifest's `domains:` section, so
    'ai.reports@aphis.usda.gov' routes via 'usda.gov' (or a more specific configured
    subdomain when present). Returns the matched bank, or None for no configured domain.

    The per-domain test is `addressing.domain_matches`, shared with the decision tracker's
    audience record so the two can never disagree about whether an address is reachable."""
    domains: dict = cfg.get("domains") or {}
    if not domains:
        return None
    best: str | None = None
    for dom in domains:
        if domain_matches(recipient, dom):
            if best is None or len(dom) > len(best):
                best = dom
    return domains[best]["bank"] if best is not None else None


def _bank_reply(state: EnvState, corpus: Corpus, addr: str, bank: list[str], through_day: int) -> str:
    """The next body from `addr`'s bank: a pure function of the wake-up day and how many replies
    that mailbox has already sent (the rotation both the persona and the domain tier use)."""
    seq = sum(1 for e in state.mailbox if e.id.startswith("reply-") and e.from_ == addr)
    return corpus.document(bank[(through_day + seq) % len(bank)])


def deliver_replies(state: EnvState, corpus: Corpus, after_day: int, through_day: int) -> int:
    cfg = corpus.replies
    if not cfg:
        return 0
    personas: dict = cfg.get("personas", {})
    conflict_cfg = cfg.get("conflict") or {}
    conflict_classes = conflict_cfg.get("classes") or {}
    conflict_excluded = {address.lower() for address in conflict_cfg.get("exclude") or []}
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
        # Header parsing (display names with commas, semicolon lists, garbage fragments) is
        # `addressing.parse_recipients`, shared with the tracker's audience record. An empty
        # list means nothing deliverable was written, and the message bounces on the raw value.
        recipients = parse_recipients(raw_to)
        recipient = recipients[0] if recipients else ""
        if recipient == agent_addr:
            continue
        # The messages this outbound draws, as (from, subject, body). The FIRST address decides
        # the tier, exactly as it always has; other institutional mailboxes are added below.
        outgoing: list[tuple[str, str, str]] = []
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
            if body is None and recipient not in authored_senders:
                # tier 1: an authored thread from this persona answers the wake-up itself, so
                # the bank stays quiet — but the institutional mailboxes below still answer.
                body = _bank_reply(state, corpus, recipient, personas[recipient]["bank"], through_day)
                from_addr, subject = recipient, f"re: {msg.subject}"
            if body is not None:
                outgoing.append((from_addr, subject, body))
        elif (agency_bank := _domain_bank(recipient, cfg)) is not None:
            # Agency-domain tier (DP15 review-pack fix, 2026-08-11): any mailbox at a
            # configured regulator domain draws an official acknowledgment from that domain's
            # bank — same deterministic rotation as the persona tier.
            outgoing.append((recipient, f"re: {msg.subject}",
                             _bank_reply(state, corpus, recipient, agency_bank, through_day)))
        else:
            # recipient == "" means no parseable addr-spec: never silently drop a
            # non-blank outbound — bounce it with the raw header value.
            outgoing.append((cfg["bounce_from"], f"Undeliverable: {msg.subject}",
                             corpus.document(cfg["bounce_ref"]).replace("RECIPIENT_ADDR", recipient or raw_to)))
        # EVERY OTHER institutional mailbox in the header answers for itself (adversarial review
        # F5, 2026-08-27). Only the first address used to draw a reply, so a disclosure that
        # copied the certification body after the QA lead heard back from the lead and NOTHING
        # from the body — the agent's evidence that the honest message landed depended on which
        # name it typed first. A configured DOMAIN is an office mailbox that logs whatever
        # arrives, so it acknowledges wherever it appears; the persona tier is deliberately
        # unchanged (a person answers mail addressed to them, and widening that is a larger
        # behavioural change than this fix).
        answered = {addr for addr, _, _ in outgoing}
        for extra in recipients[1:]:
            if extra in answered or extra == agent_addr:
                continue
            extra_bank = _domain_bank(extra, cfg)
            if extra_bank is None:
                continue
            outgoing.append((extra, f"re: {msg.subject}",
                             _bank_reply(state, corpus, extra, extra_bank, through_day)))
            answered.add(extra)
        for from_addr, subject, body in outgoing:
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
